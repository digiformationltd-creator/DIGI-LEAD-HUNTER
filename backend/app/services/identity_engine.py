"""
DIGIFORMATION LTD — Lead Hunter
Normalized Identity Matching & Permanent Duplicate Exclusion Engine
"""
import re
import urllib.parse
from typing import Dict, Any, List, Optional, Tuple
from database import get_connection

def normalize_domain(url: Optional[str]) -> str:
    """
    Normalizes domain by removing protocol, www, trailing slashes, and paths.
    https://www.example.com/ -> example.com
    http://example.com/about/ -> example.com
    """
    if not url:
        return ""
    u = url.strip().lower()
    if not u.startswith(("http://", "https://")):
        u = f"http://{u}"
    try:
        parsed = urllib.parse.urlparse(u)
        netloc = parsed.netloc or parsed.path
        netloc = re.sub(r'^www\.', '', netloc)
        netloc = netloc.split(':')[0] # strip port
        return netloc.strip().strip('/')
    except Exception:
        clean = re.sub(r'^https?:\/\/', '', u)
        clean = re.sub(r'^www\.', '', clean)
        return clean.split('/')[0].strip()

def normalize_phone(phone: Optional[str]) -> str:
    """
    Normalizes phone numbers to standard numeric suffix (last 10 or 9 digits).
    Handles +92-321-4512341, (0321) 4512341, 03214512341 -> 3214512341
    """
    if not phone:
        return ""
    digits = re.sub(r'\D', '', str(phone))
    if not digits:
        return ""
    # If starts with Pakistan country code 92, take last 10 digits
    if digits.startswith("92") and len(digits) >= 12:
        return digits[-10:]
    # If starts with 03..., drop leading 0
    if digits.startswith("0") and len(digits) >= 10:
        return digits[1:]
    # General: return last 9 or 10 digits for matching
    return digits[-10:] if len(digits) >= 10 else digits

def normalize_business_name(name: Optional[str]) -> str:
    """
    Normalizes business name by removing punctuation, spaces, case, and common noise words.
    ABC Rent A Car, ABC Rent-A-Car, abc rent a car -> abcrentacar
    """
    if not name:
        return ""
    n = name.lower()
    # Strip common noise
    n = re.sub(r'\b(ltd|pvt|inc|llc|co|corp|company)\b', '', n)
    # Remove all non-alphanumeric
    return re.sub(r'[^a-z0-9]', '', n).strip()

def normalize_address(address: Optional[str]) -> str:
    if not address:
        return ""
    return re.sub(r'[^a-z0-9]', '', address.lower()).strip()

class IdentityDeduplicationEngine:
    def __init__(self):
        pass

    def get_historical_leads(self) -> List[Dict[str, Any]]:
        """
        Retrieves all historical leads from SQLite with their normalized keys.
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, business_name, phone, phone_normalized, whatsapp_number, 
                   website_url, google_maps_url, address, location, category, is_used
            FROM leads
        """)
        rows = cursor.fetchall()
        conn.close()
        
        leads = []
        for r in rows:
            leads.append({
                "id": r["id"],
                "business_name": r["business_name"],
                "norm_name": normalize_business_name(r["business_name"]),
                "phone": r["phone"],
                "norm_phone": normalize_phone(r["phone"] or r["whatsapp_number"]),
                "norm_wa": normalize_phone(r["whatsapp_number"]),
                "norm_domain": normalize_domain(r["website_url"]),
                "maps_url": (r["google_maps_url"] or "").strip(),
                "address": r["address"],
                "norm_address": normalize_address(r["address"]),
                "category": r["category"],
                "is_used": bool(r["is_used"] if "is_used" in r.keys() else 0)
            })
        return leads

    def is_duplicate(self, candidate: Dict[str, Any], historical_leads: Optional[List[Dict[str, Any]]] = None) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Compares a newly discovered candidate against historical leads.
        Returns: (is_duplicate: bool, match_reason: str, matched_lead: dict)
        
        Match Tiers:
        1. EXACT / STRONG MATCH:
           - Same normalized domain (non-empty, non-social)
           - Same normalized phone or WhatsApp (non-empty, length >= 7)
           - Same exact Google Maps URL (non-empty)
        2. HIGH-CONFIDENCE MATCH:
           - Same normalized business name AND (similar location OR similar address)
        3. WEAK MATCH:
           - Similar name only -> NOT marked as duplicate.
        """
        if historical_leads is None:
            historical_leads = self.get_historical_leads()

        cand_name = candidate.get("business_name", "")
        cand_norm_name = normalize_business_name(cand_name)
        cand_domain = normalize_domain(candidate.get("website_url"))
        cand_phone = normalize_phone(candidate.get("phone") or candidate.get("whatsapp_number"))
        cand_wa = normalize_phone(candidate.get("whatsapp_number"))
        cand_maps = (candidate.get("google_maps_url") or "").strip()
        cand_addr = normalize_address(candidate.get("address"))
        cand_loc = (candidate.get("location") or "").lower().strip()

        # Non-dedupable domains (generic aggregators)
        generic_domains = {"facebook.com", "instagram.com", "google.com", "tiktok.com", "youtube.com"}

        for h in historical_leads:
            # 1. STRONG: Domain Match (if official domain present)
            if cand_domain and cand_domain not in generic_domains and cand_domain == h["norm_domain"]:
                used_note = " (PREVIOUSLY USED)" if h["is_used"] else ""
                return True, f"STRONG_MATCH_DOMAIN: '{cand_domain}' matches existing lead '{h['business_name']}'{used_note}", h

            # 2. STRONG: Phone or WhatsApp Match (>= 7 digits)
            if cand_phone and len(cand_phone) >= 7 and (cand_phone == h["norm_phone"] or cand_phone == h["norm_wa"]):
                used_note = " (PREVIOUSLY USED)" if h["is_used"] else ""
                return True, f"STRONG_MATCH_PHONE: '{cand_phone}' matches existing lead '{h['business_name']}'{used_note}", h

            if cand_wa and len(cand_wa) >= 7 and (cand_wa == h["norm_wa"] or cand_wa == h["norm_phone"]):
                used_note = " (PREVIOUSLY USED)" if h["is_used"] else ""
                return True, f"STRONG_MATCH_WHATSAPP: '{cand_wa}' matches existing lead '{h['business_name']}'{used_note}", h

            # 3. STRONG: Exact Google Maps Link Match
            if cand_maps and len(cand_maps) > 20 and cand_maps == h["maps_url"]:
                used_note = " (PREVIOUSLY USED)" if h["is_used"] else ""
                return True, f"STRONG_MATCH_MAPS_URL matches existing lead '{h['business_name']}'{used_note}", h

            # 4. HIGH-CONFIDENCE: Same Normalized Business Name + Location / Address
            if cand_norm_name and cand_norm_name == h["norm_name"]:
                # If either has address and they match, or locations match
                h_loc = (h.get("location") or "").lower().strip()
                same_location = bool(cand_loc and h_loc and (cand_loc in h_loc or h_loc in cand_loc))
                same_address = bool(cand_addr and h["norm_address"] and (cand_addr in h["norm_address"] or h["norm_address"] in cand_addr))
                
                if same_address or same_location:
                    used_note = " (PREVIOUSLY USED)" if h["is_used"] else ""
                    return True, f"HIGH_CONFIDENCE_MATCH: Name '{cand_name}' and location/address match '{h['business_name']}'{used_note}", h

        return False, None, None
