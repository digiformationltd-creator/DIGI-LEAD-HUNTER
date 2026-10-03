import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.classification_service import ClassificationService

def test_p1_classification():
    srv = ClassificationService()
    lead = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "review_count": 45,
        "business_hours": "09:00 - 21:00",
        "address": "Main Boulevard",
        "phone": "+92 316 4467464"
    }
    priority, score, missing = srv.classify_lead(lead)
    assert priority == "P1"
    assert score >= 85

def test_p3_classification():
    srv = ClassificationService()
    lead = {
        "website_status": "OUTDATED_WEAK",
        "whatsapp_status": "PHONE_ONLY",
        "review_count": 10,
        "address": "Commercial Strip"
    }
    priority, score, missing = srv.classify_lead(lead)
    assert priority == "P3"
