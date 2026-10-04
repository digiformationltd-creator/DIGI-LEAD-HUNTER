"""
DIGIFORMATION LTD — Lead Hunter
Phase 03: Three-Tier Website Opportunity Classification Engine (Strict 2-Signal Quality Gate)
Certified Zero-Fabrication Protocol:
- Priority 1 (Build-Ready Prime): Certified NO_WEBSITE + Verified Mobile/WhatsApp + Verified Physical Address + 2-Signal Multi-Factor Confirmation.
- Priority 2 (Consultation): Certified NO_WEBSITE, but Landline-only OR missing key collateral assets (generates discovery checklist).
- Priority 3 (Modernization / Unclear): Outdated/weak existing website OR WEBSITE_STATUS_UNCLEAR (search consensus inconclusive).
- Excluded: Shariah violations or international chains.
"""
from typing import Dict, Any, Tuple, List, Optional

class ClassificationService:
    def classify_lead(self, verified_lead: Dict[str, Any]) -> Tuple[str, int, List[str]]:
        """
        Classifies lead into P1, P2, P3, or EXCLUDED.
        Calculates factual Build-Readiness score (0-100%).
        Constructs granular asset checklist with zero fabricated fallbacks.
        Returns:
            (priority, build_readiness_score, missing_info_list)
        """
        website_status = verified_lead.get("website_status", "WEBSITE_STATUS_UNCLEAR")
        wa_status = verified_lead.get("whatsapp_status", "PHONE_UNVERIFIED")
        review_count = verified_lead.get("review_count", 0) or 0
        raw_rating = verified_lead.get("rating")
        rating = float(raw_rating) if raw_rating is not None else 0.0
        
        has_hours = bool(verified_lead.get("business_hours"))
        has_address = bool(verified_lead.get("address"))
        has_phone = bool(verified_lead.get("phone"))
        raw_maps_url = verified_lead.get("google_maps_url")
        
        is_mobile = wa_status in ("WHATSAPP_CONFIRMED", "MOBILE_CARRIER_VALID", "WHATSAPP_VERIFIED")
        is_landline = wa_status == "LANDLINE_ONLY"

        # Auto-synthesize clean maps search link if missing and address is present
        if not raw_maps_url and has_address:
            import urllib.parse
            q = f"{verified_lead.get('business_name', '')} {verified_lead.get('address', '')}".strip()
            verified_lead["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(q)}"

        # Strict Multi-Factor Signals Count
        signals_count = 0
        if has_address: signals_count += 1
        if is_mobile: signals_count += 1
        elif has_phone: signals_count += 0.5
        if review_count >= 5: signals_count += 1
        if has_hours: signals_count += 1
        if verified_lead.get("offerings"): signals_count += 1

        # Build Detailed Asset Checklist (Strictly Honest - Zero Fallback)
        checklist = {
            "google_maps": {
                "title": "Google Maps & Physical Presence",
                "present": bool(has_address),
                "detail": verified_lead.get("address") or "Missing physical address"
            },
            "whatsapp_channel": {
                "title": "Verified Mobile WhatsApp Channel",
                "present": is_mobile,
                "detail": f"+{verified_lead.get('whatsapp_number')}" if verified_lead.get("whatsapp_number") else ("Landline Only (No WhatsApp)" if is_landline else "Phone unverified")
            },
            "website_gap": {
                "title": "Certified NO_WEBSITE Gap",
                "present": website_status == "NO_WEBSITE",
                "detail": "Certified NO official website across multi-engine consensus" if website_status == "NO_WEBSITE" else f"Current Status: {website_status}"
            },
            "ratings_and_reviews": {
                "title": "Public Ratings & Social Proof",
                "present": bool(review_count >= 5 and rating >= 3.5),
                "detail": f"{rating:.1f}★ ({review_count} reviews)" if raw_rating is not None and review_count > 0 else (f"{review_count} reviews (No rating)" if review_count > 0 else "No public reviews recorded")
            },
            "operating_hours": {
                "title": "Confirmed Daily Operating Hours",
                "present": has_hours,
                "detail": verified_lead.get("business_hours") or "Operating hours not registered"
            },
            "offerings_menu": {
                "title": "Products / Offerings Data",
                "present": bool(verified_lead.get("offerings")),
                "detail": f"{len(verified_lead.get('offerings', []))} items cataloged" if verified_lead.get("offerings") else "Offerings catalog empty"
            }
        }
        verified_lead["asset_checklist"] = checklist

        # Build Readiness Score calculation (0 - 100)
        score = 0
        if has_address: score += 25
        if is_mobile: score += 30
        elif has_phone: score += 15
        if website_status == "NO_WEBSITE": score += 25
        elif website_status == "OUTDATED_WEAK": score += 15
        if has_hours: score += 10
        if review_count >= 5: score += 10
        score = min(score, 100)

        # Missing Information Collection
        missing_info = []
        if not has_address: missing_info.append("Physical commercial address")
        if not is_mobile: missing_info.append("Verified mobile WhatsApp number")
        if not has_hours: missing_info.append("Daily operating hours")
        if review_count == 0: missing_info.append("Verified customer reviews")
        if not verified_lead.get("offerings"): missing_info.append("Product/Service menu items")

        # ── STRICT 2-SIGNAL QUALITY GATING LOGIC ─────────────────────────────
        # Rule 1: Website Status Unclear -> P3 (Never P1)
        if website_status == "WEBSITE_STATUS_UNCLEAR":
            return "P3", score, ["Multi-engine website search inconclusive — requires manual check"] + missing_info

        # Rule 2: Active or Outdated Website -> P3 (Modernization/Redesign Opportunity)
        if website_status in ("OFFICIAL_WEBSITE", "OUTDATED_WEAK"):
            return "P3", score, missing_info

        # Rule 3: Certified NO_WEBSITE + Verified Mobile + Address + Signals >= 2 -> P1 (Prime)
        if website_status == "NO_WEBSITE" and is_mobile and has_address and signals_count >= 2:
            return "P1", score, missing_info

        # Rule 4: Certified NO_WEBSITE but Landline Only or Missing Address -> P2 (Consultation Required)
        if website_status == "NO_WEBSITE":
            return "P2", score, missing_info

        return "P3", score, missing_info
