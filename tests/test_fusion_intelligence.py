"""
DIGIFORMATION LTD — Lead Hunter
Comprehensive Forensic & Fusion Intelligence Test Suite
Verifies:
1. DNS MX deliverability and disposable filter (dnspython)
2. Telephony carrier validation & Landline isolation (libphonenumber)
3. Cloudflare XOR email decoder & JSON-LD schema parsing
4. Multi-engine search failover & Anti-bot timeout handling (WEBSITE_STATUS_UNCLEAR)
5. Strict 2-Signal Quality Gating (No false P1s)
6. Zero synthetic fallback guarantees
"""
import sys
from pathlib import Path

# Add backend and app to path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(backend_dir / "app"))

import unittest
from services.dns_verifier_service import DnsVerifierService
from services.phone_validation_service import PhoneValidationService
from services.deep_crawler_service import DeepCrawlerService
from services.multi_search_verifier import MultiSearchVerifier
from services.verification_service import VerificationService
from services.classification_service import ClassificationService

class TestFusionIntelligence(unittest.TestCase):
    def setUp(self):
        self.dns = DnsVerifierService(timeout=3.0)
        self.phone = PhoneValidationService(default_region="PK")
        self.crawler = DeepCrawlerService(timeout=4.0)
        self.verifier = VerificationService()
        self.classifier = ClassificationService()

    # ── 1. DNS & EMAIL DELIVERABILITY TESTS ─────────────────────────────────
    def test_dns_mx_validation_real_domain(self):
        res = self.dns.verify_email_deliverability("info@google.com")
        self.assertTrue(res["is_valid_format"])
        self.assertTrue(res["has_mx"])
        self.assertEqual(res["deliverability_status"], "DELIVERABLE")
        self.assertTrue(len(res["mx_records"]) > 0)

    def test_dns_disposable_email_detection(self):
        res = self.dns.verify_email_deliverability("test@mailinator.com")
        self.assertTrue(res["is_disposable"])
        self.assertEqual(res["deliverability_status"], "DISPOSABLE")

    def test_dns_invalid_email_syntax(self):
        res = self.dns.verify_email_deliverability("not-an-email")
        self.assertFalse(res["is_valid_format"])
        self.assertEqual(res["deliverability_status"], "INVALID_SYNTAX")

    # ── 2. TELEPHONY & WHATSAPP LIBPHONENUMBER TESTS ───────────────────────
    def test_pakistan_mobile_valid(self):
        res = self.phone.validate_and_classify_phone("0300 1234567", country_code="PK")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["e164"], "+923001234567")
        self.assertEqual(res["line_type"], "MOBILE")
        self.assertTrue(res["is_mobile"])
        self.assertEqual(res["whatsapp_status"], "MOBILE_CARRIER_VALID")
        self.assertEqual(res["whatsapp_number"], "923001234567")

    def test_pakistan_landline_isolation(self):
        # Lahore landline (042) MUST NOT be marked as WhatsApp capable!
        res = self.phone.validate_and_classify_phone("042-35751234", country_code="PK")
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["e164"], "+924235751234")
        self.assertEqual(res["line_type"], "FIXED_LINE")
        self.assertFalse(res["is_mobile"])
        self.assertEqual(res["whatsapp_status"], "LANDLINE_ONLY")
        self.assertEqual(res["whatsapp_number"], "")

    def test_explicit_click_to_chat_link(self):
        res = self.phone.validate_and_classify_phone("wa.me/923214567890", country_code="PK")
        self.assertEqual(res["whatsapp_status"], "WHATSAPP_CONFIRMED")
        self.assertEqual(res["whatsapp_number"], "923214567890")

    def test_invalid_phone_string(self):
        res = self.phone.validate_and_classify_phone("12345", country_code="PK")
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["whatsapp_status"], "PHONE_UNVERIFIED")

    # ── 3. CLOUDFLARE EMAIL & JSON-LD DECODER TESTS ─────────────────────────
    def test_cloudflare_email_xor_decryption(self):
        # XOR key: 0x5a ('Z')
        # Plain text: 'info@test.com'
        raw_email = "info@test.com"
        k = 0x5a
        hex_encoded = f"{k:02x}" + "".join([f"{(ord(c) ^ k):02x}" for c in raw_email])
        decoded = self.crawler.decode_cf_email(hex_encoded)
        self.assertEqual(decoded, raw_email)

    def test_schema_org_json_ld_extraction(self):
        sample_html = """
        <html>
        <head>
          <script type="application/ld+json">
          {
            "@context": "https://schema.org",
            "@type": "Restaurant",
            "name": "Lahore Tikka House",
            "telephone": "+923001112233",
            "email": "contact@lahoretikka.pk",
            "address": {
              "@type": "PostalAddress",
              "streetAddress": "Ghalib Market",
              "addressLocality": "Lahore",
              "addressCountry": "Pakistan"
            },
            "sameAs": [
              "https://www.facebook.com/lahoretikka",
              "https://www.instagram.com/lahoretikka"
            ]
          }
          </script>
        </head>
        <body>
          <a href="https://wa.me/923001112233">Chat on WhatsApp</a>
        </body>
        </html>
        """
        extracted = self.crawler.extract_from_html(sample_html, "https://lahoretikka.pk")
        self.assertIn("contact@lahoretikka.pk", extracted["emails"])
        self.assertIn("+923001112233", extracted["whatsapps"])
        self.assertIn("facebook", extracted["socials"])
        self.assertTrue(len(extracted["addresses"]) > 0)
        self.assertIn("Lahore", extracted["addresses"][0])

    # ── 4. MULTI-SEARCH ANTI-BOT TIMEOUT HANDLING ──────────────────────────
    def test_multi_search_never_converts_error_to_no_website(self):
        # When all search engines fail/timeout, verdict MUST be WEBSITE_STATUS_UNCLEAR
        ms = MultiSearchVerifier()
        # Mock search engines failing with timeouts
        ms._search_ddg = lambda client, q: ([], "TIMEOUT")
        ms._search_bing = lambda client, q: ([], "TIMEOUT")
        ms._search_mojeek = lambda client, q: ([], "RATE_LIMITED_429")

        res = ms.verify_candidate_presence("Unknown Grill", "Lahore")
        self.assertEqual(res["status"], "WEBSITE_STATUS_UNCLEAR")
        self.assertEqual(res["successful_engines_count"], 0)
        self.assertIn("WEBSITE_STATUS_UNCLEAR", res["notes"])

    def test_multi_search_finds_official_website(self):
        ms = MultiSearchVerifier()
        ms._search_ddg = lambda client, q: (["monal.com.pk", "facebook.com/monal"], "OK")
        ms._search_bing = lambda client, q: (["monal.com.pk"], "OK")
        ms._search_mojeek = lambda client, q: ([], "OK")

        res = ms.verify_candidate_presence("Monal Restaurant", "Lahore")
        self.assertEqual(res["status"], "OFFICIAL_WEBSITE")
        self.assertEqual(res["top_candidate_domain"], "https://monal.com.pk")

    def test_multi_search_certifies_no_website_with_consensus(self):
        ms = MultiSearchVerifier()
        ms._search_ddg = lambda client, q: (["facebook.com/localspot"], "OK")
        ms._search_bing = lambda client, q: (["instagram.com/localspot", "foodpanda.pk/r/123"], "OK")
        ms._search_mojeek = lambda client, q: ([], "OK")

        res = ms.verify_candidate_presence("Local Spot", "Lahore")
        self.assertEqual(res["status"], "NO_WEBSITE")
        self.assertEqual(res["successful_engines_count"], 3)

    # ── 5. CLASSIFICATION & STRICT 2-SIGNAL GATE TESTS ─────────────────────
    def test_unclear_website_never_becomes_p1(self):
        lead = {
            "business_name": "Test Grill",
            "website_status": "WEBSITE_STATUS_UNCLEAR",
            "whatsapp_status": "MOBILE_CARRIER_VALID",
            "phone": "+923001234567",
            "address": "Gulberg, Lahore",
            "rating": None,
            "review_count": 0
        }
        prio, score, missing = self.classifier.classify_lead(lead)
        self.assertEqual(prio, "EXCLUDED")  # Must be EXCLUDED, never P1 or P2!
        self.assertIn("Multi-engine website search inconclusive", missing[0])

    def test_landline_never_becomes_p1(self):
        lead = {
            "business_name": "Lahore Traders",
            "website_status": "NO_WEBSITE",
            "whatsapp_status": "LANDLINE_ONLY",
            "phone": "042-35751234",
            "address": "Mall Road, Lahore",
            "rating": None,
            "review_count": 10
        }
        prio, score, missing = self.classifier.classify_lead(lead)
        self.assertEqual(prio, "EXCLUDED")  # Excluded because WhatsApp direct messaging is unavailable
        self.assertNotEqual(prio, "P1")

    def test_genuine_p1_lead_qualification(self):
        lead = {
            "business_name": "Artisan Biryani Hub",
            "website_status": "NO_WEBSITE",
            "whatsapp_status": "MOBILE_CARRIER_VALID",
            "whatsapp_number": "923001234567",
            "phone": "0300-1234567",
            "address": "Barkat Market, Lahore",
            "business_hours": "11:00 AM - 12:00 AM",
            "rating": None,
            "review_count": 18,
            "offerings": [{"name": "Special Chicken Biryani"}]
        }
        prio, score, missing = self.classifier.classify_lead(lead)
        self.assertEqual(prio, "P1")
        self.assertTrue(score >= 70)

    # ── 6. ZERO SYNTHETIC FALLBACK INTEGRITY TEST ──────────────────────────
    def test_zero_synthetic_fallbacks_preserved(self):
        cand = {
            "business_name": "Raw Street Food",
            "category": "Fast Food",
            "location": "Lahore",
            "phone": "03214567890",
            "website_url": "",
            "rating": None,
            "review_count": 0,
            "business_hours": None
        }
        verified, evidence = self.verifier.verify_candidate(cand)
        self.assertIsNone(verified["rating"])  # Must stay None, not 4.0 or 4.5
        self.assertEqual(verified["review_count"], 0)  # Must stay 0, not 20 or 30
        self.assertIsNone(verified["business_hours"])  # Must stay None, not '11:00 AM - 01:00 AM'

if __name__ == "__main__":
    unittest.main()
