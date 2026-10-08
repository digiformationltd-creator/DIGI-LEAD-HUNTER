"""
DIGIFORMATION LTD — Lead Hunter
Leads API Endpoints
"""
import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from database import get_connection
from models import LeadResponse

router = APIRouter(prefix="/api/leads", tags=["Leads"])

@router.get("", response_model=List[LeadResponse])
def get_leads(
    priority: Optional[str] = Query(None, description="P1, P2, EXCLUDED"),
    website_status: Optional[str] = None,
    whatsapp_status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 200,
    offset: int = 0
):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT l.*, (p.id IS NOT NULL) AS has_package, (SELECT COUNT(*) FROM lead_evidence e WHERE e.lead_id = l.id) AS evidence_count FROM leads l LEFT JOIN packages p ON l.id = p.lead_id WHERE 1=1"
    params = []

    if priority and priority != "ALL":
        query += " AND l.priority = ?"
        params.append(priority)
    if website_status and website_status != "ALL":
        query += " AND l.website_status = ?"
        params.append(website_status)
    if whatsapp_status and whatsapp_status != "ALL":
        query += " AND l.whatsapp_status = ?"
        params.append(whatsapp_status)
    if search:
        query += " AND (l.business_name LIKE ? OR l.category LIKE ? OR l.location LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s])

    query += " ORDER BY l.created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()

    leads = []
    for r in rows:
        leads.append(LeadResponse(
            id=r["id"],
            run_id=r["run_id"],
            business_name=r["business_name"],
            category=r["category"],
            address=r["address"],
            location=r["location"],
            google_maps_url=r["google_maps_url"],
            phone=r["phone"],
            phone_normalized=r["phone_normalized"],
            whatsapp_number=r["whatsapp_number"],
            whatsapp_status=r["whatsapp_status"],
            whatsapp_confidence=r["whatsapp_confidence"] if "whatsapp_confidence" in r.keys() else None,
            whatsapp_verified=bool(r["whatsapp_verified"] in (1, "1", True, "true")) if "whatsapp_verified" in r.keys() and r["whatsapp_verified"] is not None else False,
            carrier_line_type=r["carrier_line_type"] if "carrier_line_type" in r.keys() else None,
            website_url=r["website_url"],
            website_status=r["website_status"],
            website_audit=json.loads(r["website_audit"]) if r["website_audit"] else None,
            rating=r["rating"],
            review_count=r["review_count"],
            business_hours=r["business_hours"],
            description=r["description"],
            priority=r["priority"],
            build_readiness=r["build_readiness"],
            missing_info=json.loads(r["missing_info"]) if r["missing_info"] else [],
            offerings=json.loads(r["offerings"]) if r["offerings"] else [],
            visual_signals=json.loads(r["visual_signals"]) if r["visual_signals"] else {},
            user_notes=r["user_notes"],
            is_used=bool(r["is_used"] if "is_used" in r.keys() else 0),
            used_at=r["used_at"] if "used_at" in r.keys() else None,
            usage_notes=r["usage_notes"] if "usage_notes" in r.keys() else None,
            created_at=r["created_at"],
            updated_at=r["updated_at"],
            has_package=bool(r["has_package"]),
            evidence_count=r["evidence_count"]
        ))
    conn.close()
    return leads

@router.post("/{lead_id}/mark-used")
def mark_lead_used(lead_id: str):
    """
    Marks a lead as permanently USED.
    A used lead is permanently remembered and excluded from future fresh lead pools.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, business_name FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    from datetime import datetime
    now_iso = datetime.now().isoformat()
    cursor.execute("""
        UPDATE leads 
        SET is_used = 1, used_at = ?, updated_at = ?
        WHERE id = ?
    """, (now_iso, now_iso, lead_id))
    conn.commit()
    conn.close()
    return {
        "status": "success",
        "lead_id": lead_id,
        "is_used": True,
        "used_at": now_iso,
        "message": f"Lead '{row['business_name']}' permanently marked as USED."
    }

@router.post("/{lead_id}/unmark-used")
def unmark_lead_used(lead_id: str):
    """
    Explicit reset action to unmark a lead if requested by user.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, business_name FROM leads WHERE id = ?", (lead_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    from datetime import datetime
    now_iso = datetime.now().isoformat()
    cursor.execute("""
        UPDATE leads 
        SET is_used = 0, used_at = NULL, updated_at = ?
        WHERE id = ?
    """, (now_iso, lead_id))
    conn.commit()
    conn.close()
    return {
        "status": "success",
        "lead_id": lead_id,
        "is_used": False,
        "message": f"Lead '{row['business_name']}' unmarked as used."
    }

@router.get("/{lead_id}")
def get_lead_detail(lead_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    lead_row = cursor.fetchone()
    if not lead_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    # Fetch Evidence
    cursor.execute("SELECT * FROM lead_evidence WHERE lead_id = ? ORDER BY id ASC", (lead_id,))
    evidence_rows = cursor.fetchall()
    evidence = [dict(ev) for ev in evidence_rows]

    # Fetch Website Plan
    cursor.execute("SELECT * FROM website_plans WHERE lead_id = ?", (lead_id,))
    plan_row = cursor.fetchone()
    plan = None
    if plan_row:
        plan = dict(plan_row)
        for field in ["objectives", "cta_strategy", "whatsapp_strategy", "info_architecture", "hero_plan", "sections_plan", "visual_direction", "seo_plan"]:
            if plan.get(field):
                try:
                    plan[field] = json.loads(plan[field])
                except Exception:
                    pass

    # Fetch Package
    cursor.execute("SELECT * FROM packages WHERE lead_id = ?", (lead_id,))
    pkg_row = cursor.fetchone()
    package = dict(pkg_row) if pkg_row else None

    # Fetch Assets
    cursor.execute("SELECT * FROM assets WHERE lead_id = ?", (lead_id,))
    asset_rows = cursor.fetchall()
    assets = [dict(a) for a in asset_rows]

    conn.close()

    lead_data = dict(lead_row)
    for field in ["website_audit", "missing_info", "offerings", "visual_signals"]:
        if lead_data.get(field):
            try:
                lead_data[field] = json.loads(lead_data[field])
            except Exception:
                pass

    return {
        "lead": lead_data,
        "evidence": evidence,
        "plan": plan,
        "package": package,
        "assets": assets
    }
