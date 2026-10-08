"""
DIGIFORMATION LTD — Lead Hunter
Packages & ZIP Download API
"""
import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from database import get_connection
from models import PackageResponse

router = APIRouter(prefix="/api/packages", tags=["Packages"])

@router.get("", response_model=List[PackageResponse])
def list_packages(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM packages ORDER BY created_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    packages = []
    for r in rows:
        packages.append(PackageResponse(
            id=r["id"],
            lead_id=r["lead_id"],
            business_name=r["business_name"],
            priority=r["priority"],
            version=r["version"],
            zip_filename=r["zip_filename"],
            zip_size_bytes=r["zip_size_bytes"],
            download_url=f"/api/packages/{r['id']}/download",
            is_valid=bool(r["is_valid"]),
            created_at=r["created_at"]
        ))
    conn.close()
    return packages

@router.get("/{pkg_id}/download")
def download_package(pkg_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packages WHERE id = ?", (pkg_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Package not found")

    zip_path = Path(row["zip_path"])
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="ZIP archive file missing on server")

    return FileResponse(
        path=str(zip_path),
        filename=row["zip_filename"],
        media_type="application/zip"
    )

@router.get("/lead/{lead_id}/download")
def download_lead_package(lead_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packages WHERE lead_id = ?", (lead_id,))
    row = cursor.fetchone()

    # If package exists and file is present, return it
    if row:
        zip_path = Path(row["zip_path"])
        if zip_path.exists():
            conn.close()
            return FileResponse(
                path=str(zip_path),
                filename=row["zip_filename"],
                media_type="application/zip"
            )

    # If package file is missing, dynamically generate it on demand from lead data
    cursor.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
    lead_row = cursor.fetchone()
    if not lead_row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    lead_data = dict(lead_row)
    for field in ["missing_info", "offerings", "visual_signals", "website_audit"]:
        if lead_data.get(field):
            try:
                import json
                lead_data[field] = json.loads(lead_data[field])
            except Exception:
                pass

    # Fetch evidence
    cursor.execute("SELECT * FROM lead_evidence WHERE lead_id = ?", (lead_id,))
    evidence_list = [dict(ev) for ev in cursor.fetchall()]

    from services.intelligence_service import IntelligenceService
    from services.planning_service import PlanningService
    from services.packaging_service import PackagingService

    intel = IntelligenceService().enrich_lead(lead_data)
    plan = PlanningService().generate_plan(lead_data, intel)
    pkg = PackagingService().create_package(lead_data, plan, evidence_list, intel)

    # Save or update package record in db
    cursor.execute("""
        INSERT OR REPLACE INTO packages (id, lead_id, business_name, priority, version, zip_filename, zip_path, zip_size_bytes, is_valid, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pkg["id"], lead_id, pkg["business_name"], pkg["priority"],
        pkg["version"], pkg["zip_filename"], pkg["zip_path"], pkg["zip_size_bytes"],
        1, pkg["created_at"]
    ))
    conn.commit()
    conn.close()

    return FileResponse(
        path=pkg["zip_path"],
        filename=pkg["zip_filename"],
        media_type="application/zip"
    )
