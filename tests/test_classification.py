import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.classification_service import ClassificationService


def test_no_website_unverified_is_capped_at_p2_and_flagged():
    # When the live search could not confirm the "no website" claim, the lead is
    # surfaced but NEVER build-ready, and the uncertainty is spelled out.
    srv = ClassificationService()
    lead = {
        "website_status": "NO_WEBSITE_UNVERIFIED",
        "whatsapp_status": "WHATSAPP_POSSIBLE",
        "whatsapp_number": "923164467464",
        "whatsapp_confidence": "UNVERIFIED",
        "phone": "+92 316 4467464",
        "address": "Main Boulevard",
    }
    priority, score, missing = srv.classify_lead(lead)
    assert priority == "P2"
    assert any("WEBSITE NOT VERIFIED" in m for m in missing)


def test_found_website_is_not_a_greenfield_lead():
    # A business that already has a live website must never be pitched as a
    # "no website" build opportunity.
    srv = ClassificationService()
    lead = {"website_status": "HTTPS_LIVE", "website_analysis": {}, "phone": "+92 300 0000000"}
    priority, score, missing = srv.classify_lead(lead)
    assert priority in ("EXCLUDED", "P3")


def test_no_website_lead_flags_unverified_whatsapp():
    # Even a genuine no-website lead must say so when its WhatsApp was not
    # actually confirmed — no silent "verified WhatsApp".
    srv = ClassificationService()
    lead = {
        "website_status": "NO_WEBSITE",
        "whatsapp_status": "WHATSAPP_POSSIBLE",
        "whatsapp_number": "923164467464",
        "whatsapp_confidence": "UNVERIFIED",
        "phone": "+92 316 4467464",
        "address": "Commercial Strip",
    }
    priority, score, missing = srv.classify_lead(lead)
    assert any("WHATSAPP NOT VERIFIED" in m for m in missing)
