import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.classification_service import ClassificationService

srv = ClassificationService()

def test_1_genuine_p1():
    """Test 1: Valid business without website qualifies for P1."""
    lead = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 300 1234567",
        "address": "Gulberg III, Lahore",
        "location": "Lahore",
        "review_count": 25,
        "rating": 4.2
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "P1"
    assert score >= 70

def test_2_genuine_p2_weak_website():
    """Test 2: Qualified business with objectively weak website qualifies for P2."""
    lead = {
        "website_status": "OUTDATED_WEAK",
        "website_url": "http://old-diner.pk",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 300 1234567",
        "address": "Gulberg III, Lahore",
        "location": "Lahore",
        "review_count": 25,
        "rating": 4.2,
        "website_audit": {
            "weakness_score": 85,
            "issues": ["Non-responsive layout", "No WhatsApp CTA", "Broken layout"]
        }
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "P2"
    assert "p2_reason" in lead
    assert lead["p2_reason"]["website_url"] == "http://old-diner.pk"
    assert len(lead["p2_reason"]["verified_weaknesses"]) > 0

def test_3_weak_website_without_business_qualification_excluded():
    """Test 3: Unfit website but missing phone/WhatsApp -> EXCLUDED (never P2)."""
    lead = {
        "website_status": "OUTDATED_WEAK",
        "website_url": "http://broken.pk",
        "whatsapp_status": "UNKNOWN",
        "phone": "",
        "address": "Lahore",
        "review_count": 20
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "EXCLUDED"

def test_4_healthy_website_excluded():
    """Test 4: Business with modern healthy website -> EXCLUDED."""
    lead = {
        "website_status": "OFFICIAL_WEBSITE",
        "website_url": "https://modern.pk",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 300 1234567",
        "address": "Lahore",
        "review_count": 50
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "EXCLUDED"

def test_5_unclear_website_excluded():
    """Test 5: Inconclusive website search (WEBSITE_STATUS_UNCLEAR) -> EXCLUDED (never P2)."""
    lead = {
        "website_status": "WEBSITE_STATUS_UNCLEAR",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 300 1234567",
        "address": "Lahore",
        "review_count": 25
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "EXCLUDED"

def test_6_landline_only_excluded():
    """Test 6: Landline only -> EXCLUDED."""
    lead = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "LANDLINE_ONLY",
        "phone": "042-35889900",
        "address": "Mall Road, Lahore",
        "review_count": 25
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "EXCLUDED"

def test_7_missing_address_excluded():
    """Test 7: Missing physical address -> EXCLUDED."""
    lead = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 300 1234567",
        "address": "",
        "review_count": 25
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "EXCLUDED"

def test_8_weak_website_p2_reason_structured():
    """Test 8: P2 classification populates structured p2_reason with required fields."""
    lead = {
        "website_status": "OUTDATED_WEAK",
        "website_url": "http://legacy.pk",
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "phone": "+92 321 9876543",
        "address": "DHA Phase 5, Lahore",
        "review_count": 30,
        "website_audit": {
            "weakness_score": 75,
            "issues": ["Outdated visual design", "No mobile viewport"]
        }
    }
    prio, score, missing = srv.classify_lead(lead)
    assert prio == "P2"
    p2_reason = lead.get("p2_reason")
    assert isinstance(p2_reason, dict)
    assert "website_url" in p2_reason
    assert "weakness_score" in p2_reason
    assert "verified_weaknesses" in p2_reason
    assert "conclusion" in p2_reason
    assert p2_reason["weakness_score"] == 75

def test_9_no_active_p3_ever_emitted():
    """Test 9: Verify that 'P3' is never returned as a priority for any lead permutation."""
    permutations = [
        {"website_status": "NO_WEBSITE", "whatsapp_status": "WHATSAPP_VERIFIED", "address": "Lahore", "phone": "+923001234567"},
        {"website_status": "OUTDATED_WEAK", "whatsapp_status": "WHATSAPP_VERIFIED", "address": "Lahore", "phone": "+923001234567"},
        {"website_status": "OUTDATED_WEAK", "whatsapp_status": "PHONE_ONLY", "address": "Lahore"},
        {"website_status": "OFFICIAL_WEBSITE", "whatsapp_status": "WHATSAPP_VERIFIED", "address": "Lahore"},
        {"website_status": "WEBSITE_STATUS_UNCLEAR", "whatsapp_status": "WHATSAPP_VERIFIED", "address": "Lahore"},
        {"website_status": "NO_WEBSITE", "whatsapp_status": "LANDLINE_ONLY", "address": "Lahore"},
        {"website_status": "", "whatsapp_status": ""},
    ]
    for p in permutations:
        prio, _, _ = srv.classify_lead(p)
        assert prio in ["P1", "P2", "EXCLUDED"]
        assert prio != "P3"
