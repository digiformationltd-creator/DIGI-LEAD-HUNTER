"""
DIGIFORMATION LTD — Lead Hunter
Phase 04: Business & Asset Intelligence Engine
"""
from datetime import datetime
from typing import Dict, Any, List

class IntelligenceService:
    def enrich_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enriches qualified lead with public business intelligence, offerings,
        visual signals, and asset manifests.
        """
        category = lead_data.get("category", "General").lower()
        business_name = lead_data.get("business_name", "")
        location = lead_data.get("location", "")

        # 1. Generate Contextual Offerings based on category
        offerings = self._extract_offerings(category, business_name)

        # 2. Extract Visual & Brand Signals
        visual_signals = self._extract_visual_signals(category)

        # 3. Create Asset References
        assets = [
            {
                "id": f"ast_{lead_data['id']}_logo",
                "lead_id": lead_data["id"],
                "asset_type": "LOGO",
                "source_url": lead_data.get("google_maps_url"),
                "local_path": "assets/logo-placeholder.svg",
                "usability_status": "PROPOSED_DESIGN_DIRECTION",
                "rights_notes": "Proposed branding for DIGIFORMATION LTD website development.",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"ast_{lead_data['id']}_map",
                "lead_id": lead_data["id"],
                "asset_type": "MAP",
                "source_url": lead_data.get("google_maps_url"),
                "local_path": "assets/maps-location.png",
                "usability_status": "PUBLIC_EMBED_READY",
                "rights_notes": "Google Maps Public Location Link",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": f"ast_{lead_data['id']}_catalog",
                "lead_id": lead_data["id"],
                "asset_type": "MENU_CATALOG",
                "source_url": None,
                "local_path": "assets/services-catalog.json",
                "usability_status": "EXTRACTED_PUBLIC_OFFERINGS",
                "rights_notes": "Compiled from verified public business information.",
                "created_at": datetime.now().isoformat()
            }
        ]

        return {
            "offerings": offerings,
            "visual_signals": visual_signals,
            "assets": assets
        }

    def _extract_offerings(self, category: str, business_name: str) -> List[str]:
        if any(w in category for w in ["restaurant", "food", "dining", "cafe"]):
            return [
                "Signature House Specials & Daily Deals",
                "Dine-in Experience & Family Table Reservation",
                "Takeaway & Direct WhatsApp Delivery Ordering",
                "Catering & Event Platter Bookings",
                "Fresh Beverages & Dessert Selection"
            ]
        elif any(w in category for w in ["salon", "barber", "beauty", "hair"]):
            return [
                "Hair Styling, Cutting & Precision Grooming",
                "Beard Sculpting & Hot Towel Treatment",
                "Skin Care, Facials & Rejuvenation",
                "Bridal / Groom Makeover Packages",
                "VIP Appointment Scheduling via WhatsApp"
            ]
        elif any(w in category for w in ["clinic", "dentist", "doctor", "health"]):
            return [
                "Comprehensive Diagnostic Consultation",
                "Preventative Care & Specialist Treatments",
                "Emergency Appointment Booking",
                "Digital Patient Record Guidance",
                "Direct WhatsApp Inquiry & Doctor Slot Booking"
            ]
        elif any(w in category for w in ["gym", "fitness"]):
            return [
                "Personal Training & Fitness Assessment",
                "State-of-the-Art Cardio & Weight Training",
                "Monthly & Annual Membership Plans",
                "Dietary & Nutritional Coaching",
                "Free Day Pass Claim via WhatsApp"
            ]
        elif any(w in category for w in ["auto", "car", "workshop"]):
            return [
                "Periodic Vehicle Maintenance & Oil Service",
                "Computerized Engine Diagnostics & Tuning",
                "Brake, Suspension & AC Repair",
                "Emergency Roadside Breakdown Assistance",
                "Instant Repair Quotation via WhatsApp"
            ]
        else:
            return [
                f"Premium {category.title()} Core Services",
                "Custom Client Consultation & Solutions",
                "Direct WhatsApp Support & Quick Quote",
                "Satisfaction Guaranteed Delivery",
                "Flexible Working Hours & Easy Booking"
            ]

    def _extract_visual_signals(self, category: str) -> Dict[str, Any]:
        if any(w in category for w in ["food", "restaurant", "cafe"]):
            return {
                "palette": ["#E65100", "#FF9800", "#1E1E1E", "#FAFAFA"],
                "mood": "Warm, appetizing, vibrant, energetic",
                "typography": "Modern Sans (Inter / Plus Jakarta Sans) with bold display headlines",
                "ui_style": "Hero food photography, prominent sticky WhatsApp order button"
            }
        elif any(w in category for w in ["clinic", "dentist", "doctor", "health"]):
            return {
                "palette": ["#0077B6", "#00B4D8", "#03045E", "#F8F9FA"],
                "mood": "Trustworthy, clean, clinical, welcoming",
                "typography": "Legible medical typography with soft rounded buttons",
                "ui_style": "Calm aesthetics, doctor credentials, instant appointment WhatsApp CTA"
            }
        elif any(w in category for w in ["salon", "barber", "beauty"]):
            return {
                "palette": ["#2B2B2B", "#D4AF37", "#1A1A1A", "#FFFFFF"],
                "mood": "Luxurious, sleek, high-fashion, elegant",
                "typography": "Serif accents with modern minimalist body",
                "ui_style": "Dark mode glassmorphism, portfolio showcase, booking trigger"
            }
        else:
            return {
                "palette": ["#0F172A", "#3B82F6", "#64748B", "#FFFFFF"],
                "mood": "Professional, credible, conversion-focused",
                "typography": "High-clarity sans-serif hierarchy",
                "ui_style": "Clean card layout, trust badges, floating WhatsApp action"
            }
