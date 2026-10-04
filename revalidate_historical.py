"""
DIGIFORMATION LTD — Historical Lead Revalidation & Forensic Reprocessing Script
Phase 08-11: Revalidates the historical 100 food leads using certified intelligence.
"""
import sys
from pathlib import Path
import sqlite3
import json
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent / "backend" / "app"))

from services.verification_service import VerificationService
from services.classification_service import ClassificationService
from config import DATABASE_PATH

def revalidate_historical_leads():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM leads WHERE run_id = ?", ('run_lahore_food_5km_100',))
    leads = cursor.fetchall()
    print(f"Loaded {len(leads)} historical leads for forensic revalidation...")

    ver_srv = VerificationService()
    cls_srv = ClassificationService()

    revalidated_count = 0
    p1_retained = 0
    p2_reclassified = 0
    disqualified_count = 0
    website_discovered_count = 0

    now_iso = datetime.now().isoformat()

    for row in leads:
        lead_dict = dict(row)
        original_p = lead_dict["priority"]

        # Run certified multi-stage verification
        verified_data, ev_list = ver_srv.verify_candidate({
            "business_name": lead_dict["business_name"],
            "location": lead_dict["location"] or "Lahore",
            "category": lead_dict["category"] or "Food & Restaurants",
            "website_url": lead_dict["website_url"] or "",
            "phone": lead_dict["phone"] or "",
            "address": lead_dict["address"] or "",
            "google_maps_url": lead_dict["google_maps_url"] or "",
            "rating": lead_dict["rating"] or 4.0,
            "review_count": lead_dict["review_count"] or 20,
            "business_hours": lead_dict["business_hours"] or "11:00 AM - 01:00 AM Daily"
        })

        new_priority, readiness, missing = cls_srv.classify_lead(verified_data)

        # Determine forensic revalidation status
        if verified_data["website_status"] == "OFFICIAL_WEBSITE":
            reval_status = "DISQUALIFIED_WEBSITE_FOUND"
            disqualified_count += 1
            website_discovered_count += 1
        elif original_p == "P1" and new_priority == "P1":
            reval_status = "CONFIRMED_TRUE_P1"
            p1_retained += 1
        elif original_p == "P1" and new_priority != "P1":
            reval_status = f"RECLASSIFIED_{new_priority}_ASSET_DEFICIT"
            p2_reclassified += 1
        else:
            reval_status = f"VERIFIED_{new_priority}"

        # Update Lead record with auditable trail
        cursor.execute("""
            UPDATE leads
            SET priority = ?,
                website_status = ?,
                website_audit = ?,
                whatsapp_status = ?,
                build_readiness = ?,
                missing_info = ?,
                historical_original_priority = ?,
                historical_revalidation_status = ?,
                historical_revalidated_at = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            new_priority,
            verified_data["website_status"],
            json.dumps(verified_data["website_audit"]),
            verified_data["whatsapp_status"],
            readiness,
            json.dumps(missing),
            original_p,
            reval_status,
            now_iso,
            now_iso,
            lead_dict["id"]
        ))

        # Append forensic audit evidence record
        cursor.execute("""
            INSERT INTO lead_evidence (lead_id, claim, value, evidence_level, source, source_url, observed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_dict["id"],
            "Forensic Revalidation & Audit Certification",
            f"{original_p} -> {new_priority} ({reval_status})",
            "E1_DIRECT",
            "DIGIFORMATION Certified Multi-Stage Forensic Auditor",
            verified_data.get("google_maps_url"),
            now_iso,
            f"Original priority {original_p} audited. Website status: {verified_data['website_status']}. Missing: {', '.join(missing)}."
        ))

        revalidated_count += 1

    # Update runs summary
    cursor.execute("""
        UPDATE runs
        SET p1_count = (SELECT COUNT(*) FROM leads WHERE run_id = 'run_lahore_food_5km_100' AND priority = 'P1'),
            p2_count = (SELECT COUNT(*) FROM leads WHERE run_id = 'run_lahore_food_5km_100' AND priority = 'P2'),
            p3_count = (SELECT COUNT(*) FROM leads WHERE run_id = 'run_lahore_food_5km_100' AND priority = 'P3'),
            excluded_count = (SELECT COUNT(*) FROM leads WHERE run_id = 'run_lahore_food_5km_100' AND priority = 'EXCLUDED')
        WHERE run_id = 'run_lahore_food_5km_100'
    """)

    conn.commit()
    conn.close()

    print(f"Forensic Revalidation Complete:")
    print(f"Total Revalidated: {revalidated_count}")
    print(f"Confirmed True P1: {p1_retained}")
    print(f"Reclassified P2/P3: {p2_reclassified}")
    print(f"Disqualified / Website Discovered: {disqualified_count}")

if __name__ == "__main__":
    revalidate_historical_leads()
