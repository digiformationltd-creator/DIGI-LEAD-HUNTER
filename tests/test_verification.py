import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.verification_service import VerificationService

def test_whatsapp_pakistan_verification():
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("03164467464")
    assert status == "WHATSAPP_VERIFIED"
    assert clean == "923164467464"
    assert norm == "+92 316 4467464"

def test_whatsapp_uk_verification():
    srv = VerificationService()
    norm, clean, status = srv._verify_whatsapp("07123456789")
    assert status == "WHATSAPP_VERIFIED"
    assert clean == "447123456789"

def test_website_audit():
    srv = VerificationService()
    status, audit = srv._audit_website("http://outdated-legacy-site.example.com")
    assert status == "OUTDATED_WEAK"
    assert audit["weakness_score"] > 50
