import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.packaging_service import PackagingService
from services.planning_service import PlanningService
from services.intelligence_service import IntelligenceService

def test_package_and_zip_creation():
    pkg_srv = PackagingService()
    plan_srv = PlanningService()
    intel_srv = IntelligenceService()

    lead = {
        "id": "test_lead_01",
        "business_name": "Test Bistro",
        "category": "Restaurant",
        "location": "Lahore",
        "priority": "P1",
        "build_readiness": 92,
        "whatsapp_number": "923164467464",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "rating": 4.7,
        "review_count": 55,
        "website_status": "NO_WEBSITE"
    }

    intel = intel_srv.enrich_lead(lead)
    plan = plan_srv.generate_plan(lead, intel)
    evidence = [{"claim": "Test Claim", "value": "Test Value", "evidence_level": "E1_DIRECT", "source": "Unit Test", "observed_at": "2026-10-04"}]

    package = pkg_srv.create_package(lead, plan, evidence, intel)
    assert package["is_valid"] is True
    assert Path(package["zip_path"]).exists()
    assert package["zip_size_bytes"] > 0
