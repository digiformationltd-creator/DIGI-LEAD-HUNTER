import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.verification_service import VerificationService


# ---------------------------------------------------------------------------
# WhatsApp: _verify_whatsapp reports the number's SHAPE only. It must never
# claim a number is "verified" — a real WhatsApp check happens later (the live
# search in verify_candidate), and even that only upgrades to CONFIRMED when an
# advertised wa.me link actually matches. The strongest status this low-level
# method may return is WHATSAPP_POSSIBLE.
# ---------------------------------------------------------------------------
def test_whatsapp_pakistan_format_only():
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("03164467464")
    assert status == "WHATSAPP_POSSIBLE"          # format match, NOT verified
    assert clean == "923164467464"
    assert norm == "+92 316 4467464"


def test_whatsapp_uk_format_only():
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("07123456789")
    assert status == "WHATSAPP_POSSIBLE"
    assert clean == "447123456789"


def test_website_audit_never_fakes_a_live_site():
    # An unreachable host must never be reported as a live/verified website.
    srv = VerificationService()
    status, audit = srv._audit_website("http://outdated-legacy-site.example.com")
    assert status not in ("LIVE", "HTTPS_LIVE")   # no false "has website"
    assert isinstance(audit, dict)
