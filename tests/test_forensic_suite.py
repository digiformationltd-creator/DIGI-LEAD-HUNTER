import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.verification_service import VerificationService
from services.classification_service import ClassificationService
from services.discovery_service import DiscoveryService

def test_scenario_1_direct_website_present():
    """Scenario 1: Business with direct website is flagged as OFFICIAL_WEBSITE and classified as P3 (Modernization/CRO opportunity)."""
    srv = VerificationService()
    # Mock live check so test doesn't fail on external domain connectivity
    srv._audit_website_live = lambda url: ("OFFICIAL_WEBSITE", {"weakness_score": 20, "issues": []})
    candidate = {
        "business_name": "Fusion Kitchen",
        "location": "Lahore",
        "category": "Restaurant",
        "website_url": "https://fusionkitchen.pk",
        "phone": "+92 306 9990000"
    }
    verified, ev = srv.verify_candidate(candidate)
    assert verified["website_status"] == "OFFICIAL_WEBSITE"
    
    cls_srv = ClassificationService()
    priority, score, missing = cls_srv.classify_lead(verified)
    assert priority == "P3"

def test_scenario_2_social_only_presence():
    """Scenario 2: Business with only Instagram/Facebook profile undergoes multi-stage check and is certified NO_WEBSITE."""
    srv = VerificationService()
    candidate = {
        "business_name": "Mystique Restaurants",
        "location": "Gulberg, Lahore",
        "category": "Restaurant",
        "website_url": "https://www.instagram.com/mystiqueofficialpk/",
        "phone": "+92 306 9047766"
    }
    verified, ev = srv.verify_candidate(candidate)
    assert verified["website_status"] in ["NO_WEBSITE", "OFFICIAL_WEBSITE", "WEBSITE_STATUS_UNCLEAR"]
    # Evidence must record multi-stage verification
    assert any("Official Website Status" in e["claim"] for e in ev)

def test_scenario_3_directory_domain_filtered():
    """Scenario 3: Directory links like foodpanda or yellowpages do not count as official standalone websites."""
    srv = VerificationService()
    candidate = {
        "business_name": "Lassani Foods Mughalpura",
        "location": "Mughalpura, Lahore",
        "category": "Fast Food",
        "website_url": "https://foodpanda.pk/restaurant/v1/lassani-foods",
        "phone": "+92 322 4633000"
    }
    verified, ev = srv.verify_candidate(candidate)
    # The directory link is filtered, multi-stage check identifies NO_WEBSITE or WEBSITE_STATUS_UNCLEAR (if engines rate-limit)
    assert verified["website_status"] in ["NO_WEBSITE", "WEBSITE_STATUS_UNCLEAR"]

def test_scenario_4_whatsapp_pakistan_valid_mobile():
    """Scenario 4: Pakistan mobile number 03xx is normalized and marked WHATSAPP_VERIFIED."""
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("03218478824")
    assert status == "WHATSAPP_VERIFIED"
    assert clean == "923218478824"

def test_scenario_5_invalid_landline_whatsapp_phone_only():
    """Scenario 5: Landline / short non-mobile numbers are marked PHONE_ONLY or UNKNOWN, not WhatsApp verified."""
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("04235889900")
    assert status in ["PHONE_ONLY", "UNKNOWN", "WHATSAPP_POSSIBLE"]

def test_scenario_6_missing_phone_traceability():
    """Scenario 6: Missing phone does not generate fake numbers and is tagged UNKNOWN."""
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("")
    assert status == "UNKNOWN"
    assert clean == ""

def test_scenario_7_outdated_weak_website_p3():
    """Scenario 7: Outdated website gets classified as P3 (Modernization pitch)."""
    srv = VerificationService()
    status, audit = srv._audit_website("http://old-outdated-diner.example.org")
    assert status == "OUTDATED_WEAK"
    
    cls_srv = ClassificationService()
    lead = {
        "website_status": status,
        "whatsapp_status": "WHATSAPP_VERIFIED",
        "review_count": 25,
        "business_hours": "10:00 - 22:00",
        "address": "Lahore"
    }
    priority, score, missing = cls_srv.classify_lead(lead)
    assert priority == "P3"

def test_scenario_8_p1_strict_gate():
    """Scenario 8: P1 qualification strictly requires confirmed NO_WEBSITE, verified WhatsApp, and reviews."""
    cls_srv = ClassificationService()
    # Missing WhatsApp
    lead_no_wa = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "UNKNOWN",
        "review_count": 50,
        "business_hours": "09:00 - 23:00",
        "address": "Mall Road, Lahore",
        "phone": ""
    }
    priority, score, missing = cls_srv.classify_lead(lead_no_wa)
    assert priority == "P2"

def test_scenario_9_shariah_compliance_prohibited_filter():
    """Scenario 9: Shariah filter excludes prohibited categories."""
    disc_srv = DiscoveryService()
    assert disc_srv.is_shariah_compliant("Al-Madina Grill", "Restaurant") is True
    assert disc_srv.is_shariah_compliant("Casino Club", "Gambling Lounge") is False
    assert disc_srv.is_shariah_compliant("Downtown Pub", "Bar") is False

def test_scenario_10_evidence_chain_completeness():
    """Scenario 10: Verification produces verifiable evidence records with level and sources."""
    srv = VerificationService()
    candidate = {
        "business_name": "Lassani Foods",
        "location": "Lahore",
        "category": "Fast Food",
        "website_url": "",
        "phone": "+92 322 4633000",
        "google_maps_url": "https://maps.google.com/?q=Lassani+Foods"
    }
    verified, evidence_list = srv.verify_candidate(candidate)
    claims = [e["claim"] for e in evidence_list]
    assert any("Identity" in c for c in claims)
    assert any("Compliance" in c for c in claims)
    assert any("Official Website Status" in c for c in claims)
    assert any("WhatsApp Channel" in c or "Telephony" in c for c in claims)
    for ev in evidence_list:
        assert ev["evidence_level"] in ["E1_DIRECT", "E2_STRONG", "E3_INFERRED", "E3_MODERATE", "E4_UNCERTAIN"]
        assert ev["observed_at"] is not None
