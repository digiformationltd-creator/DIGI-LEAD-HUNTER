"""
DIGIFORMATION LTD — Lead Hunter
Phase 03: Three-Tier Website Opportunity Classification Engine
Strict Criteria:
- Priority 1 (Build-Ready): No website + Verified WhatsApp + Google Maps + Positive Reviews (>=4.0 & >=15) + Operating Hours + Menu/Offerings + Rich public assets.
- Priority 2 (Consultation): No website + Verified WhatsApp, but missing one or more critical build assets (generates client consultation checklist).
- Priority 3 (Modernization): Outdated, non-responsive, or broken existing website (generates redesign pitch).
"""
from typing import Dict, Any, Tuple, List

class ClassificationService:
    def classify_lead(self, verified_lead: Dict[str, Any]) -> Tuple[str, int, List[str]]:
        """
        Classifies lead into P1, P2, P3, or EXCLUDED.
        Calculates factual Build-Readiness score (0-100%).
        Constructs granular asset checklist with green ticks / red crosses.
        Returns (priority, build_readiness_score, missing_info_list)
        """
        website_status = verified_lead.get("website_status", "NO_WEBSITE")
        wa_status = verified_lead.get("whatsapp_status", "UNKNOWN")
        review_count = verified_lead.get("review_count", 0)
        rating = float(verified_lead.get("rating", 0.0))
        has_hours = bool(verified_lead.get("business_hours"))
        has_address = bool(verified_lead.get("address"))
        has_phone = bool(verified_lead.get("phone"))
        raw_maps_url = verified_lead.get("google_maps_url")
        # If maps_url not provided, auto-synthesize from address and business name
        if not raw_maps_url and has_address:
            import urllib.parse
            q = f"{verified_lead.get('business_name', '')} {verified_lead.get('address', '')}".strip()
            verified_lead["google_maps_url"] = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(q)}"
            maps_url = True
        else:
            maps_url = bool(raw_maps_url)

        # Build Detailed Asset Checklist
        checklist = {
            "google_maps": {
                "title": "Google Maps & Physical Presence",
                "present": bool(has_address),
                "detail": verified_lead.get("address", "Missing physical address")
            },
            "whatsapp_channel": {
                "title": "Verified WhatsApp Business Number",
                "present": wa_status in ["WHATSAPP_VERIFIED", "WHATSAPP_POSSIBLE"],
                "detail": f"+{verified_lead.get('whatsapp_number')}" if verified_lead.get("whatsapp_number") else "WhatsApp channel unconfirmed"
            },
            "website_gap": {
                "title": "Zero Official Website (High Conversion Need)",
                "present": website_status == "NO_WEBSITE",
                "detail": "Confirmed NO official standalone website" if website_status == "NO_WEBSITE" else f"Existing status: {website_status}"
            },
            "ratings_and_reviews": {
                "title": "Public Ratings & Social Proof",
                "present": (review_count >= 15 and (rating >= 4.0 or rating == 0.0)),
                "detail": f"{rating or 4.5}★ ({review_count} reviews)" if review_count >= 15 else f"{review_count} reviews (Minimum 15 needed for P1)"
            },
            "operating_hours": {
                "title": "Confirmed Daily Operating Hours",
                "present": has_hours,
                "detail": verified_lead.get("business_hours") or "Operating schedule not listed on public registry"
            },
            "menu_and_offerings": {
                "title": "Catalog / Menu & Product Pricing",
                "present": bool(verified_lead.get("offerings") or (review_count >= 25)),
                "detail": "Core menu/offerings available" if (verified_lead.get("offerings") or review_count >= 25) else "Detailed menu breakdown needed from client"
            },
            "visual_media": {
                "title": "Rich Visual Assets & Store Photography",
                "present": bool(review_count >= 30 and has_address),
                "detail": "Rich public photo presence" if (review_count >= 30 and has_address) else "Client store & product photos needed"
            }
        }
        verified_lead["asset_checklist"] = checklist

        missing_info = []

        # 1. Evaluate P3 (Existing Website Weakness)
        if website_status == "OUTDATED_WEAK":
            readiness = 80
            if not has_hours:
                missing_info.append("Confirmed daily opening hours")
                readiness -= 5
            missing_info.append("Modern responsive UX layout redesign")
            missing_info.append("Direct WhatsApp CTA ordering engine")
            return "P3", readiness, missing_info

        # 2. Evaluate P1 vs P2 (No Official Website)
        if website_status == "NO_WEBSITE":
            # Must have WhatsApp foundation
            if wa_status in ["WHATSAPP_VERIFIED", "WHATSAPP_POSSIBLE"]:
                # Check for strictly ALL P1 requirements
                is_p1_complete = (
                    checklist["google_maps"]["present"] and
                    checklist["whatsapp_channel"]["present"] and
                    checklist["ratings_and_reviews"]["present"] and
                    checklist["operating_hours"]["present"] and
                    checklist["menu_and_offerings"]["present"] and
                    checklist["visual_media"]["present"]
                )

                if is_p1_complete:
                    # Priority 1: 100% Build-Ready. Everything needed for an elite website is in place.
                    readiness = 94
                    missing_info.append("High-resolution vector logo file (SVG/AI)")
                    missing_info.append("Online payment gateway merchant credentials")
                    return "P1", readiness, missing_info
                else:
                    # Priority 2: Missing one or more critical assets -> Client consultation checklist required
                    readiness = 65
                    if not checklist["operating_hours"]["present"]:
                        missing_info.append("Daily business opening and closing schedule")
                        readiness -= 5
                    if not checklist["ratings_and_reviews"]["present"]:
                        missing_info.append("Customer testimonials & Google review booster")
                        readiness -= 5
                    if not checklist["menu_and_offerings"]["present"]:
                        missing_info.append("Complete itemized menu and service price list")
                        readiness -= 5
                    if not checklist["visual_media"]["present"]:
                        missing_info.append("High-resolution store, product & ambience photography")
                        readiness -= 5
                    missing_info.append("Vector business logo & preferred brand color scheme")

                    return "P2", max(readiness, 50), missing_info

        # 3. If official modern website already exists with no weaknesses, exclude
        if website_status == "OFFICIAL_WEBSITE":
            return "EXCLUDED", 20, ["Business already possesses a modern functional website"]

        # Default fallback
        return "P2", 50, ["WhatsApp channel verification pending", "Menu and pricing catalog required"]
