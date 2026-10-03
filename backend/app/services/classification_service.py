"""
Digi Formation Limited — Lead Hunter
Phase 03: Three-Tier Website Opportunity Classification Engine
"""
from typing import Dict, Any, Tuple, List

class ClassificationService:
    def classify_lead(self, verified_lead: Dict[str, Any]) -> Tuple[str, int, List[str]]:
        """
        Classifies lead into P1, P2, P3, or EXCLUDED.
        Calculates factual Build-Readiness score (0-100%).
        Returns (priority, build_readiness_score, missing_info_list)
        """
        website_status = verified_lead.get("website_status", "NO_WEBSITE")
        wa_status = verified_lead.get("whatsapp_status", "UNKNOWN")
        review_count = verified_lead.get("review_count", 0)
        has_hours = bool(verified_lead.get("business_hours"))
        has_address = bool(verified_lead.get("address"))
        has_phone = bool(verified_lead.get("phone"))

        missing_info = []

        # 1. Evaluate P3 (Existing Website Weakness)
        if website_status == "OUTDATED_WEAK":
            readiness = 80
            if not has_hours:
                missing_info.append("Confirmed opening hours")
                readiness -= 5
            return "P3", readiness, missing_info

        # 2. Evaluate P1 vs P2 (No Official Website)
        if website_status == "NO_WEBSITE":
            # Must have WhatsApp
            if wa_status in ["WHATSAPP_VERIFIED", "WHATSAPP_POSSIBLE"]:
                # Check asset and information richness
                is_asset_rich = review_count >= 25 and has_hours and has_address and has_phone
                
                if is_asset_rich:
                    # Priority 1: No website + Verified WhatsApp + Asset Rich
                    readiness = 92
                    missing_info.append("High-resolution vector logo file (SVG/AI)")
                    missing_info.append("Direct online payment gateway preference")
                    return "P1", readiness, missing_info
                else:
                    # Priority 2: No website + WhatsApp + Limited Assets
                    readiness = 60
                    if review_count < 25:
                        missing_info.append("Customer photo gallery & interior shots")
                    if not has_hours:
                        missing_info.append("Verified daily business hours")
                    missing_info.append("Complete services / price list breakdown")
                    missing_info.append("Business logo & brand color preferences")
                    return "P2", readiness, missing_info

        # 3. If official modern website already exists with no weaknesses, downgrade or exclude
        if website_status == "OFFICIAL_WEBSITE":
            return "EXCLUDED", 20, ["Business already possesses a modern functional website"]

        # Default fallback
        return "P2", 50, ["WhatsApp verification pending", "Menu and pricing catalog required"]
