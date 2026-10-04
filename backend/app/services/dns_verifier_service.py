"""
DIGIFORMATION LTD — Lead Hunter Fusion Engine
DNS & Email Deliverability Verifier (RFC 5321 compliant)
Powered by open-source dnspython
"""
import re
from typing import Dict, Any, List
import dns.resolver

DISPOSABLE_PATTERNS = re.compile(
    r"@(mailinator|guerrillamail|10minutemail|tempmail|throwaway|yopmail|trashmail|sharklasers)\.",
    re.IGNORECASE
)

class DnsVerifierService:
    def __init__(self, timeout: float = 4.0):
        self.resolver = dns.resolver.Resolver()
        self.resolver.lifetime = timeout
        self.resolver.timeout = timeout

    def verify_email_deliverability(self, email: str) -> Dict[str, Any]:
        """
        Validates email syntax, disposable domain detection, and DNS MX record existence.
        Returns:
            {
                "email": str,
                "is_valid_format": bool,
                "is_disposable": bool,
                "domain": str,
                "has_mx": bool,
                "mx_records": List[str],
                "deliverability_status": "DELIVERABLE" | "NO_MX" | "DISPOSABLE" | "INVALID_SYNTAX"
            }
        """
        if not email or "@" not in email:
            return {
                "email": email or "",
                "is_valid_format": False,
                "is_disposable": False,
                "domain": "",
                "has_mx": False,
                "mx_records": [],
                "deliverability_status": "INVALID_SYNTAX"
            }

        email_clean = email.strip().lower()
        parts = email_clean.split("@")
        if len(parts) != 2 or not parts[1]:
            return {
                "email": email_clean,
                "is_valid_format": False,
                "is_disposable": False,
                "domain": "",
                "has_mx": False,
                "mx_records": [],
                "deliverability_status": "INVALID_SYNTAX"
            }

        domain = parts[1]

        if DISPOSABLE_PATTERNS.search(email_clean):
            return {
                "email": email_clean,
                "is_valid_format": True,
                "is_disposable": True,
                "domain": domain,
                "has_mx": False,
                "mx_records": [],
                "deliverability_status": "DISPOSABLE"
            }

        # Check MX Records via DNS
        try:
            answers = self.resolver.resolve(domain, "MX")
            mx_hosts = [str(r.exchange).rstrip(".") for r in answers]
            return {
                "email": email_clean,
                "is_valid_format": True,
                "is_disposable": False,
                "domain": domain,
                "has_mx": bool(mx_hosts),
                "mx_records": mx_hosts,
                "deliverability_status": "DELIVERABLE" if mx_hosts else "NO_MX"
            }
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout, Exception):
            # If MX lookup fails, fall back to A record (RFC 5321 fallback)
            try:
                a_answers = self.resolver.resolve(domain, "A")
                if a_answers:
                    return {
                        "email": email_clean,
                        "is_valid_format": True,
                        "is_disposable": False,
                        "domain": domain,
                        "has_mx": True,
                        "mx_records": [f"A-record-fallback:{domain}"],
                        "deliverability_status": "DELIVERABLE"
                    }
            except Exception:
                pass

            return {
                "email": email_clean,
                "is_valid_format": True,
                "is_disposable": False,
                "domain": domain,
                "has_mx": False,
                "mx_records": [],
                "deliverability_status": "NO_MX"
            }

    def verify_domain_liveness(self, domain: str) -> bool:
        """
        Verifies if domain has active A or AAAA records in DNS.
        """
        clean_d = re.sub(r"^https?://", "", domain).split("/")[0].strip()
        if not clean_d or "." not in clean_d:
            return False
        try:
            answers = self.resolver.resolve(clean_d, "A")
            return len(answers) > 0
        except Exception:
            try:
                answers = self.resolver.resolve(clean_d, "AAAA")
                return len(answers) > 0
            except Exception:
                return False
