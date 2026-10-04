"""
DIGIFORMATION LTD — Lead Hunter
Phase 06: Evidence, Markdown, HTML & ZIP Packaging Engine
"""
import os
import re
import json
import zipfile
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from config import PACKAGES_DIR, COMPANY_NAME, SUPPORT_WHATSAPP, EMAIL_PRIMARY, WEBSITE_PRIMARY

class PackagingService:
    def create_package(self, lead: Dict[str, Any], plan: Dict[str, Any], evidence_list: List[Dict[str, Any]], intelligence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Creates a complete standardized Opportunity Package and compresses it into a ZIP archive.
        """
        name = lead.get("business_name", "Business")
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name).strip('_')
        pack_folder_name = f"{safe_name}_WEBSITE_OPPORTUNITY_PACK"
        pack_dir = PACKAGES_DIR / pack_folder_name
        pack_dir.mkdir(parents=True, exist_ok=True)

        now_str = datetime.now().isoformat()
        date_display = datetime.now().strftime("%B %d, %Y")

        # 1. README.md
        readme_content = f"""# {name} — Website Opportunity Package
**Prepared by:** {COMPANY_NAME}  
**Contact:** WhatsApp: {SUPPORT_WHATSAPP} | Email: {EMAIL_PRIMARY}  
**Website:** {WEBSITE_PRIMARY}  
**Date:** {date_display}  
**Classification:** {lead.get('priority')} | Build-Readiness: {lead.get('build_readiness', 90)}%

---

## 📋 What is this Package?
This complete intelligence package contains verified public business research, WhatsApp contact verification, and a tailored website architecture plan for **{name}**.

### Files included in this package:
1. `WEBSITE_PLAN.md`: Strategic website architecture, section breakdown, and CTA strategy.
2. `WEBSITE_PLAN.html`: Formatted, printable presentation document ready for review or client pitch.
3. `WEBSITE_BUILD_BRIEF.md`: Component-by-component development blueprint.
4. `EVIDENCE_REPORT.md`: Factual verification logs, timestamps, and confidence levels.
5. `MISSING_INFORMATION.md`: Specific details required from the business owner during onboarding.
6. `ASSET_MANIFEST.json`: Public assets, visual palettes, and location data.
7. `PACKAGE_MANIFEST.json`: Integrity verification metadata.

---

### 🛡️ Attribution & Usage
{COMPANY_NAME} — Digi Biz OS Lead Intelligence Architecture.
"""
        (pack_dir / "README.md").write_text(readme_content, encoding="utf-8")

        # 2. WEBSITE_PLAN.md
        (pack_dir / "WEBSITE_PLAN.md").write_text(plan.get("markdown_content", ""), encoding="utf-8")

        # 3. WEBSITE_PLAN.html (Printable / PDF Ready)
        html_content = self._generate_html_plan(lead, plan, intelligence, date_display)
        (pack_dir / "WEBSITE_PLAN.html").write_text(html_content, encoding="utf-8")

        rating_val = lead.get('rating')
        review_cnt = lead.get('review_count', 0)
        review_summary = f"{rating_val}★ across {review_cnt} reviews" if rating_val is not None and review_cnt else (f"{review_cnt} reviews" if review_cnt else "Public reputation establishment")

        # 4. WEBSITE_BUILD_BRIEF.md
        brief_content = f"""# Developer Build Brief: {name}
**Project:** Local Business Web Launch  
**Category:** {lead.get('category')} | **Location:** {lead.get('location')}  
**Target WhatsApp CTA:** {lead.get('whatsapp_number', 'Direct Chat')}  
**Primary Color:** {intelligence.get('visual_signals', {}).get('palette', ['#0F172A'])[0]}

### Core Sections to Scaffold:
- [x] Sticky Header with Digi-Powered WhatsApp Action
- [x] Hero Section with instant consultation hook
- [x] Verified Offerings Grid ({len(intelligence.get('offerings', []))} items)
- [x] Google Review Trust Badge ({review_summary})
- [x] Mobile-first Bottom Sticky Contact Drawer
- [x] Embed Google Maps Location Frame
"""
        (pack_dir / "WEBSITE_BUILD_BRIEF.md").write_text(brief_content, encoding="utf-8")

        # 5. EVIDENCE_REPORT.md
        evidence_md = f"# Evidence & Verification Report: {name}\n**Audit Date:** {date_display}\n\n| Claim | Value | Level | Source | Timestamp |\n| :--- | :--- | :--- | :--- | :--- |\n"
        for ev in evidence_list:
            evidence_md += f"| {ev.get('claim')} | `{ev.get('value')}` | **{ev.get('evidence_level')}** | {ev.get('source')} | {ev.get('observed_at')} |\n"
        (pack_dir / "EVIDENCE_REPORT.md").write_text(evidence_md, encoding="utf-8")

        # 6. MISSING_INFORMATION.md
        missing_list = lead.get("missing_info", [])
        missing_md = f"""# Missing Information & Client Onboarding Checklist: {name}
Before entering live website production, the following owner-supplied assets and answers should be confirmed:

### Questions to Ask Business Owner:
{"".join(f"- [ ] {item}\n" for item in missing_list)}
- [ ] Confirm official business operating hours for holidays
- [ ] Confirm direct bank/cash-on-delivery preferences
"""
        (pack_dir / "MISSING_INFORMATION.md").write_text(missing_md, encoding="utf-8")

        # 7. ASSET_MANIFEST.json
        manifest_data = {
            "business_name": name,
            "category": lead.get("category"),
            "assets": intelligence.get("assets", []),
            "visual_palette": intelligence.get("visual_signals", {}).get("palette", []),
            "generated_at": now_str
        }
        (pack_dir / "ASSET_MANIFEST.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        # 8. PACKAGE_MANIFEST.json
        package_manifest = {
            "package_id": f"pkg_{lead['id']}",
            "business_name": name,
            "priority": lead.get("priority"),
            "version": "1.0",
            "files": [
                "README.md", "WEBSITE_PLAN.md", "WEBSITE_PLAN.html",
                "WEBSITE_BUILD_BRIEF.md", "EVIDENCE_REPORT.md",
                "MISSING_INFORMATION.md", "ASSET_MANIFEST.json", "PACKAGE_MANIFEST.json"
            ],
            "created_at": now_str,
            "creator": COMPANY_NAME
        }
        (pack_dir / "PACKAGE_MANIFEST.json").write_text(json.dumps(package_manifest, indent=2), encoding="utf-8")

        # 9. Compress to ZIP
        zip_filename = f"{safe_name}_WEBSITE_OPPORTUNITY_PACK.zip"
        zip_path = PACKAGES_DIR / zip_filename

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(pack_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(pack_dir)
                    zipf.write(file_path, arcname)

        # Validate ZIP
        is_valid = zip_path.exists() and zip_path.stat().st_size > 0

        return {
            "id": f"pkg_{lead['id']}",
            "lead_id": lead["id"],
            "business_name": name,
            "priority": lead.get("priority", "P1"),
            "version": "1.0",
            "zip_filename": zip_filename,
            "zip_path": str(zip_path),
            "zip_size_bytes": zip_path.stat().st_size if is_valid else 0,
            "is_valid": is_valid,
            "created_at": now_str
        }

    def _generate_html_plan(self, lead: Dict[str, Any], plan: Dict[str, Any], intelligence: Dict[str, Any], date_display: str) -> str:
        name = lead.get("business_name")
        cat = lead.get("category")
        loc = lead.get("location")
        wa = lead.get("whatsapp_number", "Direct Chat")
        raw_rating = lead.get("rating")
        review_cnt = lead.get("review_count", 0)
        rating_display = f"{raw_rating} ★ ({review_cnt} reviews)" if raw_rating is not None and review_cnt else (f"{review_cnt} reviews (Unrated)" if review_cnt else "Unrated")
        prio = lead.get("priority")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{name} — Website Opportunity Plan</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0B0F17; color: #E2E8F0; margin: 0; padding: 40px; line-height: 1.6; }}
    .container {{ max-width: 860px; margin: 0 auto; background: #131B2A; border: 1px solid #1E293B; border-radius: 12px; padding: 40px; box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 9999px; font-weight: 700; font-size: 13px; text-transform: uppercase; }}
    .badge-p1 {{ background: #064E3B; color: #34D399; border: 1px solid #059669; }}
    .badge-p2 {{ background: #78350F; color: #FBBF24; border: 1px solid #D97706; }}
    .badge-p3 {{ background: #1E3A8A; color: #60A5FA; border: 1px solid #2563EB; }}
    h1 {{ color: #F8FAFC; margin-top: 10px; font-size: 28px; }}
    h2 {{ color: #38BDF8; font-size: 20px; border-bottom: 1px solid #1E293B; padding-bottom: 8px; margin-top: 30px; }}
    .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 20px 0; }}
    .card {{ background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 16px; }}
    .label {{ font-size: 12px; text-transform: uppercase; color: #64748B; font-weight: 600; }}
    .value {{ font-size: 16px; color: #F1F5F9; font-weight: 600; margin-top: 4px; }}
    .cta-btn {{ display: inline-block; background: #10B981; color: #022C22; font-weight: 700; padding: 12px 24px; border-radius: 8px; text-decoration: none; margin-top: 10px; }}
    footer {{ margin-top: 40px; text-align: center; font-size: 12px; color: #64748B; border-top: 1px solid #1E293B; padding-top: 20px; }}
  </style>
</head>
<body>
  <div class="container">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span class="badge badge-{prio.lower()}">{prio} — High Build-Readiness Opportunity</span>
      <span style="color: #64748B; font-size: 14px;">{date_display}</span>
    </div>

    <h1>{name}</h1>
    <p style="color: #94A3B8;">Verified local business analysis for high-converting website production and WhatsApp integration.</p>

    <div class="grid">
      <div class="card">
        <div class="label">Business Category</div>
        <div class="value">{cat.title()}</div>
      </div>
      <div class="card">
        <div class="label">Location</div>
        <div class="value">{loc}</div>
      </div>
      <div class="card">
        <div class="label">Verified WhatsApp</div>
        <div class="value" style="color: #34D399;">+{wa}</div>
      </div>
      <div class="card">
        <div class="label">Public Rating & Reviews</div>
        <div class="value">{rating_display}</div>
      </div>
    </div>

    <h2>Website Strategic Objective</h2>
    <p>Establish an authoritative local presence in {loc}, showcasing verified offerings and capturing customer traffic directly through an optimized WhatsApp channel.</p>

    <h2>Immediate Conversion Plan</h2>
    <p>A direct, frictionless WhatsApp CTA enables customers to book appointments or place orders instantly without filling out lengthy forms.</p>
    <a href="{wa_link}" class="cta-btn">Connect on WhatsApp ({wa})</a>

    <h2>Planned Page Sections</h2>
    <ul>
      <li><strong>Hero Section:</strong> High-impact introduction highlighting {cat} specialties in {loc}.</li>
      <li><strong>Verified Offerings:</strong> Clear presentation of signature services.</li>
      <li><strong>Reviews & Trust:</strong> Displaying {rating}★ local Google rating.</li>
      <li><strong>Location & Hours:</strong> Embedded Google Map and verified operational hours.</li>
    </ul>

    <footer>
      Produced by <strong>{COMPANY_NAME}</strong> — Digi Biz OS Architecture<br>
      WhatsApp Support: {SUPPORT_WHATSAPP} | Email: {EMAIL_PRIMARY}
    </footer>
  </div>
</body>
</html>
"""
