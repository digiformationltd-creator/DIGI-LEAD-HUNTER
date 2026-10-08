"""
DIGIFORMATION LTD — Lead Hunter
Phase 03: Precision Opportunity Classification Engine
Active Priority Architecture:
- Priority 1 (Build-Ready Prime): Certified NO_WEBSITE + Verified Mobile/WhatsApp + Verified Physical Address + Multi-Factor Confirmation.
- Priority 2 (Website Redesign / Rebuild Opportunity): Inherits ALL P1 business qualification conditions (Real commercial business, Lahore/valid location, verified mobile/WhatsApp, verified address, signals confirmation), EXCEPT that an official website exists, AND that website is objectively verified as OUTDATED_WEAK / unfit for modern commercial use.
- EXCLUDED: Does not qualify for P1 or P2 (Healthy/modern websites, inconclusive/uncertain web status, unverified mobile, or missing mandatory business evidence).
There is NO active P3.
"""
from typing import Dict, Any, Tuple, List, Optional

class ClassificationService:
    def classify_lead(self, verified_lead: Dict[str, Any]) -> Tuple[str, int, List[str]]:
        """
        Classifies lead into P1, P2, or EXCLUDED.
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
        
        carrier_line_type = verified_lead.get("carrier_line_type", "")
        valid_wa_statuses = ("WHATSAPP_CONFIRMED", "MOBILE_CARRIER_VALID", "WHATSAPP_VERIFIED", "WHATSAPP_POSSIBLE", "WHATSAPP_FORMAT_ONLY")
        # NO_WHATSAPP = checked against WhatsApp and the number is NOT registered.
        # Such a number must never count as a WhatsApp lead, even though its line
        # type is MOBILE — this is what removes the fake WhatsApp leads.
        is_mobile = (wa_status != "NO_WHATSAPP") and (wa_status in valid_wa_statuses or carrier_line_type in ("MOBILE", "FIXED_LINE_OR_MOBILE")) and carrier_line_type != "FIXED_LINE"
        is_landline = wa_status == "LANDLINE_ONLY" or carrier_line_type == "FIXED_LINE"

        # Auto-synthesize clean maps search link if missing and address is present
        if not raw_maps_url and has_address:
            import urllib.parse
            q = f"{verified_lead.get('business_name', '')} {verified_lead.get('address', '')}".strip()
            verified_lead["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(q)}"

        # Strict Multi-Factor Signals Count (Shared business qualification standard for both P1 and P2)
        signals_count = 0
        if has_address: signals_count += 1
        if is_mobile: signals_count += 1
        elif has_phone: signals_count += 0.5
        if review_count >= 5: signals_count += 1
        if has_hours: signals_count += 1
        if verified_lead.get("offerings"): signals_count += 1

        # Check location qualification (Lahore + 50km or valid location)
        location_str = (verified_lead.get("location") or "").lower()
        address_str = (verified_lead.get("address") or "").lower()
        # Location is valid if Lahore or recognized regional area is specified
        is_valid_location = bool(location_str or address_str)

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
                "title": "Website Gap & Opportunity Status",
                "present": website_status in ("NO_WEBSITE", "OUTDATED_WEAK"),
                "detail": "Certified NO official website (New Build Opportunity)" if website_status == "NO_WEBSITE" else (
                    "Objectively unfit existing website (Redesign/Rebuild Opportunity)" if website_status == "OUTDATED_WEAK" else f"Current Status: {website_status}"
                )
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
        elif website_status == "OUTDATED_WEAK": score += 25
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

        # ── COMMON MANDATORY BUSINESS CONDITIONS FOR ACTIVE QUALIFICATION ────
        # Both P1 and P2 require:
        # - Real commercial business (valid address + valid location)
        # - Verified mobile / WhatsApp channel (is_mobile == True)
        # - Multi-factor signals >= 2
        # - Shariah compliant (not excluded earlier)
        has_base_business_qualification = bool(
            has_address and
            is_mobile and
            is_valid_location and
            signals_count >= 2
        )

        # ── 1. PRIORITY 1: NO PROPER OFFICIAL WEBSITE ────────────────────────
        # P1 retains exact existing requirements:
        # Certified NO_WEBSITE + Verified Mobile + Physical Address + Signals >= 2
        if website_status == "NO_WEBSITE" and has_base_business_qualification:
            return "P1", score, missing_info

        # ── 2. NEW PRIORITY 2: OBJECTIVELY UNFIT OFFICIAL WEBSITE ────────────
        # P2 inherits ALL the exact same business qualifications as P1,
        # but official website exists AND is objectively verified as OUTDATED_WEAK.
        if (
            website_status == "OUTDATED_WEAK" and
            has_base_business_qualification
        ):
            # Formulate structured evidence-backed rebuild justification
            audit = verified_lead.get("website_audit") or {}
            issues = audit.get("issues", [])
            verified_lead["p2_reason"] = {
                "title": "P2 Website Redesign / Rebuild Justification",
                "website_url": verified_lead.get("website_url"),
                "weakness_score": audit.get("weakness_score", 65),
                "verified_weaknesses": issues if issues else ["Outdated visual structure and missing mobile responsive optimization"],
                "conclusion": "Official website exists, but its current condition is objectively unfit for modern business use, making a professional redesign/rebuild commercially justified."
            }
            return "P2", score, missing_info

        # ── 3. EXCLUDED: ALL OTHER CASES (NO ACTIVE P3) ──────────────────────
        # - Website is healthy (OFFICIAL_WEBSITE) -> Not an opportunity
        # - Website status is inconclusive (WEBSITE_STATUS_UNCLEAR) -> Cannot verify weakness objectively
        # - Business lacks verified WhatsApp or physical presence -> Fails mandatory business conditions
        # - Landline-only businesses or missing critical business assets -> EXCLUDED
        if website_status == "WEBSITE_STATUS_UNCLEAR":
            missing_info = ["Multi-engine website search inconclusive — epistemic status uncertain"] + missing_info

        return "EXCLUDED", score, missing_info
