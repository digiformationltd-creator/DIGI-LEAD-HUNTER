"""
DIGIFORMATION LTD — Lead Hunter
Analytics & Dashboard KPI API
"""
from fastapi import APIRouter
from database import get_connection
from models import AnalyticsResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("", response_model=AnalyticsResponse)
def get_analytics():
    conn = get_connection()
    cursor = conn.cursor()

    # Exclude used leads from active tracking board counts (User rule: if 112 total and 1 marked used, active count becomes 111)
    cursor.execute("SELECT COUNT(*) FROM leads WHERE is_used = 0 OR is_used IS NULL")
    active_total_leads = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE is_used = 1")
    used_leads_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE priority = 'P1' AND (is_used = 0 OR is_used IS NULL)")
    p1_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE priority = 'P2' AND (is_used = 0 OR is_used IS NULL)")
    p2_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE priority = 'P3' AND (is_used = 0 OR is_used IS NULL)")
    p3_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM runs WHERE status IN ('INITIALIZING', 'DISCOVERING', 'VERIFYING', 'PACKAGING')")
    active_runs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM runs WHERE status = 'COMPLETED'")
    completed_runs = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM packages WHERE is_valid = 1")
    ready_packages = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE whatsapp_status IN ('WHATSAPP_CONFIRMED', 'WHATSAPP_VERIFIED', 'WHATSAPP_POSSIBLE') AND (is_used = 0 OR is_used IS NULL)")
    wa_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM leads WHERE website_status = 'NO_WEBSITE' AND (is_used = 0 OR is_used IS NULL)")
    no_web_count = cursor.fetchone()[0]

    cursor.execute("SELECT run_id, category, location, status, qualified_count, created_at FROM runs ORDER BY created_at DESC LIMIT 5")
    recent_runs = [dict(r) for r in cursor.fetchall()]

    conn.close()

    return AnalyticsResponse(
        total_leads=active_total_leads,
        p1_count=p1_count,
        p2_count=p2_count,
        p3_count=p3_count,
        active_runs=active_runs,
        completed_runs=completed_runs,
        ready_packages=ready_packages,
        whatsapp_verified_count=wa_count,
        no_website_count=no_web_count,
        used_leads_count=used_leads_count,
        recent_runs=recent_runs
    )
