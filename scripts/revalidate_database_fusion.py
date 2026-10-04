"""
DIGIFORMATION LTD — Lead Hunter
Fast Concurrent Forensic Database Revalidation Script
Audits all 112 historical records in data/database/lead_hunter.db using multi-threading.
"""
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(base_dir / "backend"))
sys.path.insert(0, str(base_dir / "backend" / "app"))

from services.phone_validation_service import PhoneValidationService
from services.verification_service import VerificationService
from services.classification_service import ClassificationService

DB_PATH = base_dir / "data" / "database" / "lead_hunter.db"

def process_single_lead(row_dict):
    phone_service = PhoneValidationService(default_region="PK")
    verifier = VerificationService()
    classifier = ClassificationService()

    lead_id = row_dict["id"]
    biz_name = row_dict["business_name"]
    location = row_dict["location"] or "Lahore"
    raw_phone = row_dict["phone"] or ""
    raw_web = row_dict["website_url"] or ""

    # 1. Telephony Validation
    phone_info = phone_service.validate_and_classify_phone(raw_phone, country_code="PK")
    norm_phone = phone_info.get("e164", "")
    wa_number = phone_info.get("whatsapp_number", "")
    wa_status = phone_info.get("whatsapp_status", "PHONE_UNVERIFIED")
    line_type = phone_info.get("line_type", "UNKNOWN")

    # 2. Multi-Stage Verification
    candidate_dict = {
        "business_name": biz_name,
        "location": location,
        "phone": raw_phone,
        "website_url": raw_web,
        "rating": row_dict["rating"],
        "review_count": row_dict["review_count"],
        "business_hours": row_dict["business_hours"],
        "address": row_dict["address"],
        "category": row_dict["category"]
    }

    verified_data, ev_list = verifier.verify_candidate(candidate_dict)
    web_status = verified_data["website_status"]
    final_web_url = verified_data["website_url"]

    # 3. Strict 2-Signal Classification
    priority, score, missing = classifier.classify_lead(verified_data)

    return {
        "lead_id": lead_id,
        "biz_name": biz_name,
        "norm_phone": norm_phone,
        "wa_number": wa_number,
        "wa_status": wa_status,
        "line_type": line_type,
        "final_web_url": final_web_url,
        "web_status": web_status,
        "priority": priority,
        "score": score,
        "missing": missing,
        "ev_list": ev_list,
        "is_mobile": phone_info.get("is_mobile", False)
    }

def run_concurrent_audit(max_workers=8):
    print(f"Connecting to database at {DB_PATH}...", flush=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    leads = cursor.execute("SELECT * FROM leads").fetchall()
    total = len(leads)
    print(f"Loaded {total} historical leads for concurrent revalidation (Workers: {max_workers})...\n", flush=True)

    rows = [dict(r) for r in leads]
    conn.close()

    results = []
    completed = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_single_lead, r): r["id"] for r in rows}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            completed += 1
            if completed % 10 == 0 or completed == total:
                print(f"[{completed}/{total}] Audited '{res['biz_name'][:25]}' -> Web: {res['web_status']}, WA: {res['wa_status']}, Priority: {res['priority']}", flush=True)

    print("\nWriting certified updates to SQLite...", flush=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()

    stats = {
        "total": total,
        "genuine_p1": 0,
        "p2_consultation": 0,
        "p3_modernization_or_unclear": 0,
        "websites_discovered": 0,
        "certified_no_website": 0,
        "website_status_unclear": 0,
        "whatsapp_mobile_verified": 0,
        "landlines_isolated": 0,
        "phones_unverified": 0
    }

    for res in results:
        # Tally stats
        if res["is_mobile"]:
            stats["whatsapp_mobile_verified"] += 1
        elif res["line_type"] == "FIXED_LINE":
            stats["landlines_isolated"] += 1
        else:
            stats["phones_unverified"] += 1

        if res["web_status"] == "OFFICIAL_WEBSITE":
            stats["websites_discovered"] += 1
        elif res["web_status"] == "NO_WEBSITE":
            stats["certified_no_website"] += 1
        else:
            stats["website_status_unclear"] += 1

        if res["priority"] == "P1":
            stats["genuine_p1"] += 1
        elif res["priority"] == "P2":
            stats["p2_consultation"] += 1
        else:
            stats["p3_modernization_or_unclear"] += 1

        cursor.execute("""
        UPDATE leads SET
            phone_normalized = ?,
            whatsapp_number = ?,
            whatsapp_status = ?,
            website_url = ?,
            website_status = ?,
            priority = ?,
            build_readiness = ?,
            missing_info = ?,
            updated_at = ?
        WHERE id = ?
        """, (
            res["norm_phone"],
            res["wa_number"],
            res["wa_status"],
            res["final_web_url"],
            res["web_status"],
            res["priority"],
            res["score"],
            json.dumps(res["missing"]),
            now_str,
            res["lead_id"]
        ))

        cursor.execute("""
        INSERT INTO lead_evidence (lead_id, claim, value, evidence_level, source, source_url, observed_at, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            res["lead_id"],
            "Forensic Revalidation & Fusion Quality Gate",
            f"Priority: {res['priority']} | Web: {res['web_status']} | WA: {res['wa_status']}",
            "E1_DIRECT" if res["priority"] == "P1" else "E2_STRONG",
            "MultiSearchVerifier & libphonenumber Re-Audit",
            res["final_web_url"] or None,
            now_str,
            f"Line: {res['line_type']}. Status: {res['web_status']}."
        ))

    conn.commit()
    conn.close()

    print("\n" + "="*60, flush=True)
    print("FORENSIC REVALIDATION COMPLETE — CERTIFIED METRICS", flush=True)
    print("="*60, flush=True)
    print(f"Total Historical Leads Audited:     {stats['total']}", flush=True)
    print(f"Certified NO_WEBSITE:               {stats['certified_no_website']}", flush=True)
    print(f"Discovered Standalone Websites:     {stats['websites_discovered']}", flush=True)
    print(f"Inconclusive / Throttled (UNCLEAR): {stats['website_status_unclear']}", flush=True)
    print(f"Verified Mobile (WhatsApp Capable): {stats['whatsapp_mobile_verified']}", flush=True)
    print(f"Isolated Landlines (No WhatsApp):   {stats['landlines_isolated']}", flush=True)
    print(f"Unverified / Corrupted Phone:       {stats['phones_unverified']}", flush=True)
    print(f"Genuine Certified P1 Leads:         {stats['genuine_p1']}", flush=True)
    print(f"P2 Consultation Opportunities:      {stats['p2_consultation']}", flush=True)
    print(f"P3 Modernization / Unclear:         {stats['p3_modernization_or_unclear']}", flush=True)
    print("="*60, flush=True)

    summary_file = base_dir / "data" / "revalidation_audit_summary.json"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    summary_file.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"Certified summary written to: {summary_file}", flush=True)

if __name__ == "__main__":
    run_concurrent_audit(max_workers=8)
