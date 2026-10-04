"""
DIGIFORMATION LTD — Lead Hunter Fusion Engine
Deep Website Contact Crawler & Intelligence Extractor
Features:
- Cloudflare data-cfemail XOR Decryption (entity-research.ts parity)
- Schema.org JSON-LD PostalAddress, telephone, and founder parsing
- Multi-path contact crawling (/contact, /about, /team, /imprint)
- Click-to-chat WhatsApp link extraction (wa.me, api.whatsapp.com)
"""
import re
import json
import urllib.parse
import ipaddress
import socket
from typing import Dict, Any, List, Optional
import httpx
from bs4 import BeautifulSoup

JUNK_EMAIL = re.compile(
    r"\.(png|jpe?g|gif|webp|svg|css|js)$|example\.|sentry|wixpress|@(?:2x|3x)|domain\.com|email\.com|yourname|noreply@|no-reply@",
    re.IGNORECASE
)

class DeepCrawlerService:
    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-GB,en;q=0.9,ur;q=0.8"
        }

    def decode_cf_email(self, hex_str: str) -> str:
        """
        Decodes Cloudflare email obfuscation XOR cipher.
        Source parity: entity-research.ts:148 decodeCfEmail
        """
        try:
            k = int(hex_str[:2], 16)
            chars = []
            for i in range(2, len(hex_str), 2):
                chars.append(chr(int(hex_str[i:i+2], 16) ^ k))
            return "".join(chars)
        except Exception:
            return ""

    def extract_from_html(self, html: str, source_url: str) -> Dict[str, Any]:
        """
        Extracts emails, phones, whatsapps, JSON-LD data, and social links from raw HTML.
        """
        emails = set()
        phones = set()
        whatsapps = set()
        socials = {}
        addresses = []
        people = []

        if not html:
            return {
                "emails": [], "phones": [], "whatsapps": [],
                "socials": {}, "addresses": [], "people": []
            }

        soup = BeautifulSoup(html, "html.parser")

        # 1. Cloudflare Obfuscated Email Decoding
        for tag in soup.find_all(attrs={"data-cfemail": True}):
            cf_hex = tag.get("data-cfemail", "")
            decoded = self.decode_cf_email(cf_hex)
            if decoded and "@" in decoded and not JUNK_EMAIL.search(decoded):
                emails.add(decoded.lower())

        # 2. Schema.org JSON-LD Extraction
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                raw_json = script.string
                if not raw_json:
                    continue
                data = json.loads(raw_json.strip())
                self._walk_json_ld(data, emails, phones, whatsapps, socials, addresses, people)
            except Exception:
                pass

        # 3. mailto: links & regex emails
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.lower().startswith("mailto:"):
                clean_mail = href[7:].split("?")[0].strip().lower()
                if clean_mail and not JUNK_EMAIL.search(clean_mail):
                    emails.add(clean_mail)

            # tel: links
            if href.lower().startswith("tel:"):
                clean_tel = re.sub(r"[^\d+]", "", href[4:])
                if len(clean_tel) >= 7:
                    phones.add(clean_tel)

            # WhatsApp links
            wa_match = re.search(r"(?:wa\.me\/|api\.whatsapp\.com\/send\?phone=|whatsapp:\/\/send\?phone=)\+?(\d{7,15})", href)
            if wa_match:
                whatsapps.add(f"+{wa_match.group(1)}")

            # Social links
            for soc_net in ["facebook.com", "instagram.com", "tiktok.com", "linkedin.com", "twitter.com", "youtube.com"]:
                if soc_net in href.lower() and not any(p in href.lower() for p in ["/sharer", "/share", "/intent"]):
                    social_key = soc_net.split(".")[0]
                    if social_key not in socials:
                        socials[social_key] = href

        # 4. Plaintext Regex Scans
        text = soup.get_text(separator=" ")
        for m in re.finditer(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):
            cand_mail = m.group(0).lower()
            if not JUNK_EMAIL.search(cand_mail):
                emails.add(cand_mail)

        # Obfuscated pattern: name [at] domain [dot] com
        for m in re.finditer(r"\b([A-Za-z0-9._%+-]+)\s*[\[(]\s*at\s*[\])]\s*([A-Za-z0-9-]+)\s*[\[(]\s*dot\s*[\])]\s*([A-Za-z]{2,})", text, re.I):
            cand_mail = f"{m.group(1)}@{m.group(2)}.{m.group(3)}".lower()
            if not JUNK_EMAIL.search(cand_mail):
                emails.add(cand_mail)

        return {
            "emails": sorted(list(emails))[:6],
            "phones": sorted(list(phones))[:6],
            "whatsapps": sorted(list(whatsapps))[:3],
            "socials": socials,
            "addresses": addresses[:3],
            "people": people[:3]
        }

    def _walk_json_ld(self, obj: Any, emails: set, phones: set, whatsapps: set, socials: dict, addresses: list, people: list):
        if not obj:
            return
        if isinstance(obj, list):
            for item in obj:
                self._walk_json_ld(item, emails, phones, whatsapps, socials, addresses, people)
            return
        if not isinstance(obj, dict):
            return

        # Check address
        addr = obj.get("address")
        if addr:
            if isinstance(addr, str) and len(addr) > 8:
                addresses.append(addr)
            elif isinstance(addr, dict):
                parts = [
                    addr.get("streetAddress"),
                    addr.get("addressLocality"),
                    addr.get("addressRegion"),
                    addr.get("postalCode"),
                    addr.get("addressCountry")
                ]
                formatted = ", ".join([str(p) for p in parts if p])
                if formatted:
                    addresses.append(formatted)

        # Check phone and email
        tel = obj.get("telephone")
        if isinstance(tel, str):
            phones.add(tel.strip())

        mail = obj.get("email")
        if isinstance(mail, str) and not JUNK_EMAIL.search(mail):
            emails.add(mail.replace("mailto:", "").strip().lower())

        # Check sameAs socials
        same_as = obj.get("sameAs")
        if isinstance(same_as, list):
            for link in same_as:
                if isinstance(link, str):
                    for soc in ["facebook.com", "instagram.com", "tiktok.com", "linkedin.com"]:
                        if soc in link.lower():
                            socials[soc.split(".")[0]] = link

        # Check founder/author/owner
        for role in ["founder", "owner", "employee", "author"]:
            p = obj.get(role)
            if p:
                p_name = p.get("name") if isinstance(p, dict) else (p if isinstance(p, str) else None)
                if p_name and len(p_name) < 50:
                    people.append(f"{p_name} ({role})")

        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                self._walk_json_ld(v, emails, phones, whatsapps, socials, addresses, people)

    @staticmethod
    def is_safe_url(url: str) -> bool:
        """
        SSRF Guard: Ensures domain does not resolve to private, loopback, or reserved IP ranges.
        """
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            if not hostname or hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
                return False
            # Resolve IP
            ip_str = socket.gethostbyname(hostname)
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_link_local or ip_obj.is_reserved or ip_obj.is_multicast:
                return False
            return True
        except Exception:
            return False

    def crawl_site(self, base_url: str) -> Dict[str, Any]:
        """
        Crawls the root domain plus standard contact endpoints.
        """
        if not base_url or not base_url.startswith("http") or not self.is_safe_url(base_url):
            return self.extract_from_html("", "")

        base_clean = base_url.rstrip("/")
        endpoints = ["", "/contact", "/contact-us", "/about", "/about-us"]
        combined_html = []

        with httpx.Client(timeout=self.timeout, headers=self.headers, follow_redirects=True) as client:
            for path in endpoints:
                target = base_clean + path
                try:
                    res = client.get(target)
                    if res.status_code == 200 and "text/html" in res.headers.get("content-type", ""):
                        combined_html.append(res.text[:300000])
                except Exception:
                    pass

        merged_html = "\n".join(combined_html)
        return self.extract_from_html(merged_html, base_url)
