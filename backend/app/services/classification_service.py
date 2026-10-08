"""
DIGIFORMATION LTD — Lead Hunter
Phase 03: Three-Tier Website Opportunity Classification Engine

IMPORTANT — how the tiers are decided:
An asset checklist item is only marked "present" when the corresponding data was
ACTUALLY RETRIEVED from a source. Nothing is inferred from an unrelated signal
(e.g. a review count is never treated as proof that a menu or photography exists).

- Priority 1 (Build-Ready): No website, contactable phone, AND every critical build
  asset independently present in the retrieved source data.
- Priority 2 (Consultation): No website and a usable phone number, but one or more
  critical build assets could not be confirmed -> produces a client consultation
  checklist. This is the expected outcome when source data is thin, and it is the
  honest result: it says "we still need these from the client".
- Priority 3 (Modernization): A live website was fetched AND the analyzer returned
  HIGH-severity deficiency signals derived from that page's actual HTML.
- EXCLUDED: A live website was fetched and no significant deficiency was detected,
  or the lead failed a mandatory filter.
"""
from typing import Dict, Any, Tuple, List, Optional

# Website statuses that mean "the business already operates a reachable website".
LIVE_WEBSITE_STATUSES = {"HTTPS_LIVE", "LIVE", "REDIRECTED"}

# Statuses where a website URL exists but the target could NOT be read. These are
# NOT evidence that a website exists, and NOT evidence that it does not -- so a
# greenfield build pitch must never be generated from them.
# FETCH_BLOCKED means the SSRF guard refused the request (internal/unsupported target).
# ANALYSIS_UNAVAILABLE means the analyzer itself failed and produced no measurements.
UNRESOLVED_WEBSITE_STATUSES = {
    "FETCH_FAILED", "DNS_FAILED", "NON_HTML", "HTTP_ERROR",
    "ANALYSIS_UNAVAILABLE", "FETCH_BLOCKED", "INVALID_URL",
}


def _as_float(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _as_int(value: Any) -> Optional[int]:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


class ClassificationService:
    def classify_lead(self, verified_lead: Dict[str, Any]) -> Tuple[str, int, List[str]]:
        """
        Classifies lead into P1, P2, P3, or EXCLUDED.

        Returns (priority, build_readiness_score, missing_info_list).

        The build-readiness score is a RULE-BASED HEURISTIC derived from how many
        checklist items were confirmed. It is not a measurement, a percentage of
        completion, and must not be presented to a client as one.
        """
        website_status = verified_lead.get("website_status", "NO_WEBSITE")
        wa_status = verified_lead.get("whatsapp_status", "UNKNOWN")
        review_count = _as_int(verified_lead.get("review_count"))
        rating = _as_float(verified_lead.get("rating"))
        has_hours = bool(verified_lead.get("business_hours"))
        has_address = bool(verified_lead.get("address"))
        has_phone = bool(verified_lead.get("phone"))
        maps_url = bool(verified_lead.get("google_maps_url"))
        has_offerings = bool(verified_lead.get("offerings"))

        # Contactable-number check. WHATSAPP_VERIFIED is still honoured so that any
        # legacy rows keep classifying consistently, but new runs never emit it
        # because no WhatsApp verification mechanism exists.
        has_contact_channel = wa_status in [
            "WHATSAPP_POSSIBLE", "WHATSAPP_FORMAT_ONLY", "WHATSAPP_CONFIRMED", "WHATSAPP_VERIFIED",
        ] and bool(verified_lead.get("whatsapp_number"))

        # Ratings are only usable when a real figure was retrieved from the source.
        has_real_ratings = rating is not None and review_count is not None

        # Build Detailed Asset Checklist
        checklist = {
            "google_maps": {
                "title": "Maps Listing & Street Address on Record",
                "present": bool(has_address and maps_url),
                "detail": verified_lead.get("address") or "No street address present in the source record",
                "caveat": "maps_url is a generated search link, not a confirmed Google Maps profile."
            },
            "whatsapp_channel": {
                "title": "Phone Number (WhatsApp-capable format, NOT verified)",
                "present": has_contact_channel,
                "detail": (
                    f"+{verified_lead.get('whatsapp_number')} — number format matches a mobile range"
                    if has_contact_channel
                    else "No WhatsApp-capable phone number format found"
                ),
                "caveat": "Format match only. No WhatsApp account check was performed."
            },
            "website_gap": {
                "title": "No Website Listed on Source Record",
                "present": website_status == "NO_WEBSITE",
                "detail": (
                    "No website URL present in the retrieved record"
                    if website_status == "NO_WEBSITE"
                    else f"Existing website status: {website_status}"
                ),
                "caveat": (
                    "Absence of a URL is not proof that no website exists. Confirm manually."
                    if website_status == "NO_WEBSITE"
                    else None
                )
            },
            "ratings_and_reviews": {
                "title": "Public Rating & Review Count (from source data)",
                "present": bool(has_real_ratings and review_count >= 15 and rating >= 4.0),
                "detail": (
                    f"{rating}★ ({review_count} reviews)"
                    if has_real_ratings
                    else "No rating or review count available from the source data"
                ),
                "caveat": None if has_real_ratings else "Left blank rather than estimated."
            },
            "operating_hours": {
                "title": "Operating Hours Listed on Source Record",
                "present": has_hours,
                "detail": verified_lead.get("business_hours") or "Operating schedule not present in the source data",
                "caveat": None if has_hours else "Unconfirmed. Confirm with the client."
            },
            "menu_and_offerings": {
                "title": "Catalog / Menu & Product Pricing",
                "present": has_offerings,
                "detail": "Offerings present in the retrieved data" if has_offerings else "No menu or price list available from the source data",
                "caveat": None if has_offerings else "Cannot be inferred. Must be collected from the client."
            },
            "visual_media": {
                "title": "Store / Product Photography",
                "present": False,
                "detail": "Photography cannot be verified from the available data",
                "caveat": "No image or review-media inspection is performed, so this is never auto-confirmed."
            }
        }
        verified_lead["asset_checklist"] = checklist

        missing_info = []

        # 1. Live website -> modernization pitch or exclusion.
        if website_status in LIVE_WEBSITE_STATUSES:
            high_severity = self._high_severity_signals(verified_lead.get("website_analysis"))
            if high_severity:
                readiness = 80
                if not has_hours:
                    missing_info.append("Confirmed daily opening hours")
                    readiness -= 5
                missing_info.append("Modern responsive UX layout redesign")
                missing_info.append("Direct WhatsApp CTA ordering engine")
                missing_info.append(
                    "Remediate analyzer-detected page issues: " + "; ".join(high_severity[:4])
                )
                return "P3", readiness, missing_info
            return "EXCLUDED", 20, [
                "Business already operates a reachable website and no significant page deficiencies were detected"
            ]

        # 2. A website was listed but could not be read. Do not treat the unreadable
        #    target as "no website" — that would produce a greenfield pitch for a
        #    business that may well have a site.
        if website_status in UNRESOLVED_WEBSITE_STATUSES:
            return "EXCLUDED", 20, [
                f"A website is listed for this business but could not be inspected ({website_status}). "
                f"Resolve manually before pitching a website build."
            ]

        # 2b. No website in OSM AND the live search could not run. The lead is
        #     surfaced so it is not lost, but it is NEVER build-ready: it is capped
        #     at P2 and loudly flagged as unverified so no one pitches on a guess.
        if website_status == "NO_WEBSITE_UNVERIFIED":
            if not has_contact_channel:
                return "EXCLUDED", 20, [
                    "No usable phone number found on the source record; the lead cannot be contacted"
                ]
            missing_info.append(
                "WEBSITE NOT VERIFIED - the live web search could not confirm it. Check manually "
                "that the business truly has no website BEFORE pitching a build."
            )
            if verified_lead.get("whatsapp_confidence") != "CONFIRMED":
                missing_info.append(
                    "WHATSAPP NOT VERIFIED - the number only matches a mobile shape. Confirm a "
                    "WhatsApp account exists before messaging."
                )
            return "P2", 45, missing_info

        # 3. P1 vs P2 for leads with no website listed.
        if website_status == "NO_WEBSITE":
            # A P1/P2 lead whose WhatsApp was never confirmed must still say so.
            if verified_lead.get("whatsapp_confidence") != "CONFIRMED":
                missing_info.append(
                    "WHATSAPP NOT VERIFIED - number matches a mobile shape only; confirm the "
                    "WhatsApp account exists before outreach."
                )
            if has_contact_channel:
                is_p1_complete = (
                    checklist["google_maps"]["present"] and
                    checklist["whatsapp_channel"]["present"] and
                    checklist["ratings_and_reviews"]["present"] and
                    checklist["operating_hours"]["present"] and
                    checklist["menu_and_offerings"]["present"] and
                    checklist["visual_media"]["present"]
                )

                if is_p1_complete:
                    # Priority 1: every critical build asset independently confirmed.
                    readiness = 94
                    missing_info.append("High-resolution vector logo file (SVG/AI)")
                    missing_info.append("Online payment gateway merchant credentials")
                    return "P1", readiness, missing_info

                # Priority 2: at least one critical asset unconfirmed.
                readiness = 65
                if not checklist["operating_hours"]["present"]:
                    missing_info.append("Daily business opening and closing schedule")
                    readiness -= 5
                if not checklist["ratings_and_reviews"]["present"]:
                    missing_info.append("Public rating / review evidence, or customer testimonials")
                    readiness -= 5
                if not checklist["menu_and_offerings"]["present"]:
                    missing_info.append("Complete itemized menu and service price list")
                    readiness -= 5
                if not checklist["visual_media"]["present"]:
                    missing_info.append("High-resolution store, product & ambience photography")
                    readiness -= 5
                if not checklist["google_maps"]["present"]:
                    missing_info.append("Confirmed street address")
                    readiness -= 5
                missing_info.append("Vector business logo & preferred brand color scheme")

                return "P2", max(readiness, 50), missing_info

            return "EXCLUDED", 20, [
                "No usable phone number found on the source record; the lead cannot be contacted"
            ]

        # Default fallback: an unrecognised website status must not be reported as a
        # greenfield website opportunity.
        return "EXCLUDED", 20, [
            f"Unrecognised website status '{website_status}'; manual review required"
        ]

    @staticmethod
    def _high_severity_signals(analysis: Optional[Dict[str, Any]]) -> List[str]:
        """
        Collect HIGH-severity opportunity signals produced by WebsiteAnalyzer.

        Every entry is backed by HTML actually fetched from the business's own site,
        so it is safe to surface as an observed finding rather than an assumption.
        """
        if not isinstance(analysis, dict):
            return []
        signals = analysis.get("opportunity_signals")
        if not isinstance(signals, list):
            return []
        findings = []
        for sig in signals:
            if not isinstance(sig, dict):
                continue
            if str(sig.get("severity", "")).upper() != "HIGH":
                continue
            name = sig.get("signal", "ISSUE")
            evidence = sig.get("evidence", "")
            findings.append(f"{name} ({evidence})" if evidence else str(name))
        return findings
