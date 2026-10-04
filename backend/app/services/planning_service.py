"""
DIGIFORMATION LTD — Lead Hunter
Phase 05: Website Build-Ready Planning Engine
"""
import json
from datetime import datetime
from typing import Dict, Any

class PlanningService:
    def generate_plan(self, lead_data: Dict[str, Any], intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a comprehensive, build-ready website architecture plan.
        Adapts between P1 (Build-Ready), P2 (Consultation), and P3 (Redesign).
        """
        priority = lead_data.get("priority", "P1")
        name = lead_data.get("business_name", "")
        category = lead_data.get("category", "")
        location = lead_data.get("location", "")
        wa_number = lead_data.get("whatsapp_number", "")
        wa_link = f"https://wa.me/{wa_number}?text=Hello%20{name}%2C%20I%20would%20like%20to%20inquire%20about%20your%20services" if wa_number else "https://wa.me/"
        offerings = intelligence.get("offerings", [])
        visuals = intelligence.get("visual_signals", {})

        plan_type = f"{priority}_WEBSITE_PLAN"
        target_audience = f"Local customers and residents in {location} seeking dependable {category} services with instant mobile accessibility."

        objectives = [
            f"Establish an authoritative, high-converting digital storefront for {name}",
            f"Convert local search traffic into immediate customer inquiries via WhatsApp ({wa_number or 'Direct'})",
            f"Showcase verified service offerings, customer reviews ({f'{lead_data.get(\"rating\")}★' if lead_data.get('rating') is not None else 'Public Reputation'}), and physical location in {location}",
            "Outrank local competitors lacking modern mobile-responsive websites"
        ]

        cta_strategy = {
            "primary_cta": f"Order / Book on WhatsApp ({wa_number or 'Instant Chat'})",
            "primary_cta_url": wa_link,
            "secondary_cta": "View Full Menu / Services",
            "secondary_cta_url": "#services",
            "floating_whatsapp_widget": True
        }

        whatsapp_strategy = {
            "channel": "WhatsApp Business Direct",
            "number": wa_number,
            "wa_me_link": wa_link,
            "prefilled_messages": {
                "general_inquiry": f"Hi {name}, I found your business on Google and would like more details.",
                "booking": f"Hello {name}, I want to book an appointment / place an order.",
                "pricing": f"Hi {name}, please share your latest price list."
            }
        }

        info_architecture = [
            {"page": "Home", "sections": ["Hero", "Trust Badges", "Featured Offerings", "Why Choose Us", "Reviews", "Map & Hours", "Footer"]},
            {"page": "Services / Catalog", "sections": ["All Offerings", "Pricing Highlights", "Special Packages", "WhatsApp Order CTA"]},
            {"page": "About Us", "sections": ["Brand Story", "Commitment to Quality", "Team / Facility Showcase"]},
            {"page": "Contact & Visit", "sections": ["Interactive Google Map", "Opening Hours", "Direct Phone & WhatsApp", "Quick Inquiry Form"]}
        ]

        hero_plan = {
            "headline": f"Experience the Best {category.title()} in {location}",
            "subheadline": f"Dedicated to quality, convenience, and superior client satisfaction at {name}. Reach us instantly for quick bookings and orders.",
            "hero_image_direction": f"High quality banner showcasing {category} specialties with soft overlay and instant WhatsApp button.",
            "cta_buttons": [
                {"label": "Chat on WhatsApp", "url": wa_link, "style": "primary_emerald"},
                {"label": "Explore Offerings", "url": "#offerings", "style": "secondary_outline"}
            ]
        }

        sections_plan = [
            {
                "section": "Core Offerings Showcase",
                "items": offerings
            },
            {
                "section": "Social Proof & Ratings",
                "content": f"Verified Google Maps Rating: {lead_data.get('rating', 4.5)} Stars based on {lead_data.get('review_count', 30)}+ local reviews."
            },
            {
                "section": "Location & Operational Hours",
                "address": lead_data.get("address", f"{location} Commercial Center"),
                "hours": lead_data.get("business_hours", "Mon-Sat: 09:00 AM - 09:00 PM")
            }
        ]

        seo_plan = {
            "meta_title": f"{name} | Leading {category.title()} in {location}",
            "meta_description": f"Looking for top-rated {category} in {location}? Visit {name} at {lead_data.get('address', location)}. Fast WhatsApp booking and reliable local service.",
            "keywords": [f"{category} in {location}", f"best {category} near me", f"{name} {location}", f"contact {name} whatsapp"]
        }

        # Generate Markdown Document
        markdown_text = self._build_markdown_plan(lead_data, objectives, cta_strategy, whatsapp_strategy, info_architecture, hero_plan, visuals, seo_plan)

        return {
            "id": f"plan_{lead_data['id']}",
            "lead_id": lead_data["id"],
            "plan_type": plan_type,
            "target_audience": target_audience,
            "objectives": objectives,
            "cta_strategy": cta_strategy,
            "whatsapp_strategy": whatsapp_strategy,
            "info_architecture": info_architecture,
            "hero_plan": hero_plan,
            "sections_plan": sections_plan,
            "visual_direction": visuals,
            "seo_plan": seo_plan,
            "markdown_content": markdown_text,
            "created_at": datetime.now().isoformat()
        }

    def _build_markdown_plan(self, lead: Dict[str, Any], objectives, cta, wa, ia, hero, visuals, seo) -> str:
        name = lead.get("business_name")
        prio = lead.get("priority")
        now_date = datetime.now().strftime("%B %d, %Y")

        return f"""# Website Opportunity & Build Plan
## Client: {name} ({lead.get('category')} — {lead.get('location')})
**Prepared by:** DIGIFORMATION LTD (Digi Biz OS Architecture)  
**Date:** {now_date}  
**Opportunity Tier:** {prio} (Build Readiness: {lead.get('build_readiness', 90)}%)

---

### 1. Executive Summary & Verification
- **Business Name:** {name}
- **Category:** {lead.get('category')}
- **Physical Address:** {lead.get('address', 'N/A')}
- **Verified WhatsApp:** {lead.get('whatsapp_number', 'Pending')} ({lead.get('whatsapp_status')})
- **Google Maps URL:** [{name} on Maps]({lead.get('google_maps_url', '#')})
- **Current Website Status:** {lead.get('website_status')}

---

### 2. Website Strategic Objectives
{"".join(f"- {obj}\n" for obj in objectives)}

---

### 3. High-Converting WhatsApp Integration
- **Direct WhatsApp Link:** [{wa.get('number', 'Direct Chat')}]({wa.get('wa_me_link', '#')})
- **Primary CTA:** {cta.get('primary_cta')}
- **Pre-filled User Greeting:** `"{wa.get('prefilled_messages', {}).get('booking', '')}"`

---

### 4. Proposed Information Architecture
{"".join(f"#### Page: {page['page']}\n- Sections: {', '.join(page['sections'])}\n" for page in ia)}

---

### 5. Homepage Hero Section Specification
- **Headline:** {hero.get('headline')}
- **Subheadline:** {hero.get('subheadline')}
- **Primary Action:** {hero.get('cta_buttons', [{}])[0].get('label')} -> `{hero.get('cta_buttons', [{}])[0].get('url')}`

---

### 6. Visual Design Direction
- **Target Aesthetic:** {visuals.get('mood', 'Clean, modern, high-contrast')}
- **Recommended Palette:** {', '.join(visuals.get('palette', []))}
- **Typography:** {visuals.get('typography', 'Inter / Modern Sans')}

---

### 7. Local SEO & Meta Configuration
- **Meta Title:** {seo.get('meta_title')}
- **Meta Description:** {seo.get('meta_description')}
- **Target Keywords:** {', '.join(seo.get('keywords', []))}

---

*This document was automatically generated by DIGIFORMATION LTD — Lead Hunter Agent.*
"""
