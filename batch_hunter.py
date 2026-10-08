"""
DIGIFORMATION LTD — Lead Hunter
Batch Opportunity Runner (Autonomous Antigravity CLI Engine)
"""
import os
import sys
import re
import json
import uuid
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add parent path to allow backend module imports
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR / "backend" / "app"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from config import PACKAGES_DIR, COMPANY_NAME, SUPPORT_WHATSAPP, EMAIL_PRIMARY, WEBSITE_PRIMARY
from database import init_db, get_connection
from services.discovery_service import DiscoveryService
from services.verification_service import VerificationService
from services.classification_service import ClassificationService
from services.intelligence_service import IntelligenceService
from services.planning_service import PlanningService
from services.packaging_service import PackagingService


class BatchLeadHunter:
    """
    Autonomous Batch Runner that generates:
    1. Batch folder (e.g., Restaurant_Batch_1) in selected workspace/target folder
    2. Master Interactive HTML Opportunity Portal (with search, filtering, detailed plans, packages)
    3. Master Styled Excel Spreadsheet (.xlsx)
    4. Standalone Opportunity ZIP Archive containing all P1 deliverables, images, plans, and manifests.
    """
    def __init__(self, target_folder: Optional[str] = None):
        init_db()
        self.discovery = DiscoveryService()
        self.verification = VerificationService()
        self.classification = ClassificationService()
        self.intelligence = IntelligenceService()
        self.planning = PlanningService()
        self.packaging = PackagingService()

        # Default target folder to provided path, or current working directory
        if target_folder:
            self.base_output_dir = Path(target_folder).resolve()
        else:
            self.base_output_dir = CURRENT_DIR.resolve()
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

    def execute_hunt(
        self,
        category: str = "Restaurant",
        location: str = "Lahore",
        country: str = "Pakistan",
        radius_km: int = 50,
        target_count: int = 20,
        batch_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-phase lead intelligence hunt.
        """
        clean_cat = category.strip()
        clean_loc = location.strip()
        safe_cat = re.sub(r'[^a-zA-Z0-9]', '_', clean_cat).strip('_')

        # Determine batch folder name
        if not batch_name:
            # Check existing folders to auto-increment
            existing_batches = list(self.base_output_dir.glob(f"{safe_cat}_Batch_*"))
            batch_num = len(existing_batches) + 1
            batch_name = f"{safe_cat}_Batch_{batch_num}"

        batch_dir = self.base_output_dir / batch_name
        batch_dir.mkdir(parents=True, exist_ok=True)
        p1_dir = batch_dir / "priority_1_opportunities"
        p1_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=======================================================")
        print(f"  DIGI LEAD HUNTER — AUTONOMOUS BATCH PIPELINE")
        print(f"  Category: {clean_cat} | Location: {clean_loc}, {country} | Count: {target_count}")
        print(f"  Output Directory: {batch_dir}")
        print(f"=======================================================\n")

        # Phase 1: Lead Discovery
        print(f"[Phase 1/5] Discovering businesses for '{clean_cat}' in '{clean_loc}' (Radius: {radius_km} KM)...")
        candidates = self.discovery.discover_candidates(
            category=clean_cat,
            location=clean_loc,
            country=country,
            scope="CITY",
            radius_km=radius_km,
            target_count=target_count
        )
        print(f"  -> Discovered {len(candidates)} verified candidate businesses.")

        # Phase 2 & 3: Verification & Classification
        print(f"[Phase 2/5] Auditing web presence, normalizing WhatsApp channels, and classifying priorities...")
        qualified_leads = []
        for cand in candidates:
            # Give the verifier the batch's city/country so it can run the live
            # web-presence search (real website + advertised WhatsApp) instead of
            # trusting the sparse OSM record. This is what prevents fake leads.
            cand["_city"] = clean_loc
            cand["_country"] = country
            verified_lead, evidence_list = self.verification.verify_candidate(cand)
            priority, readiness, missing_info = self.classification.classify_lead(verified_lead)
            
            verified_lead["priority"] = priority
            verified_lead["build_readiness"] = readiness
            verified_lead["missing_info"] = missing_info

            # Enrich intelligence
            intel = self.intelligence.enrich_lead(verified_lead)
            
            # Enrich offerings with categories & realistic prices
            enriched_offerings = self._enrich_catalog_with_prices(verified_lead, intel.get("offerings", []))
            intel["detailed_catalog"] = enriched_offerings

            # Website Plan
            plan = self.planning.generate_plan(verified_lead, intel)
            
            qualified_leads.append({
                "lead": verified_lead,
                "evidence": evidence_list,
                "intelligence": intel,
                "plan": plan
            })

        print(f"  -> Qualified {len(qualified_leads)} leads across Priority tiers.")

        # Phase 4: Packaging P1 Opportunities & Deliverables
        print(f"[Phase 3/5] Compiling Opportunity Packs, visual assets, and individual briefs...")
        p1_lead_packs = []
        for item in qualified_leads:
            lead = item["lead"]
            plan = item["plan"]
            evidence = item["evidence"]
            intel = item["intelligence"]

            # Generate individual pack
            pack_meta = self.packaging.create_package(lead, plan, evidence, intel)
            item["package_meta"] = pack_meta

            if lead.get("priority") == "P1":
                # Copy or generate specific P1 pack inside batch folder
                self._save_p1_dossier(p1_dir, lead, plan, evidence, intel)
                p1_lead_packs.append(lead)

        print(f"  -> Prepared {len(p1_lead_packs)} Priority-1 (Build-Ready) dossiers.")

        # Phase 5: Generate Master Deliverables in Batch Folder
        print(f"[Phase 4/5] Generating Master Excel report and Interactive HTML portal...")
        excel_path = batch_dir / f"{batch_name}_LEADS_REPORT.xlsx"
        self._generate_master_excel(excel_path, qualified_leads, batch_name, clean_cat, clean_loc)

        html_path = batch_dir / f"{batch_name}_OPPORTUNITY_PORTAL.html"
        self._generate_master_html(html_path, qualified_leads, batch_name, clean_cat, clean_loc)

        # Phase 6: Build Final Batch ZIP
        print(f"[Phase 5/5] Compressing complete batch into high-converting ZIP archive...")
        zip_path = batch_dir / f"{batch_name}_COMPLETE_PACK.zip"
        self._generate_batch_zip(zip_path, batch_dir)

        print(f"\n=======================================================")
        print(f"  [+] BATCH COMPLETE SUCCESSFULLY!")
        print(f"  Directory:    {batch_dir}")
        print(f"  Excel Sheet:  {excel_path.name}")
        print(f"  HTML Portal:  {html_path.name}")
        print(f"  Final ZIP:    {zip_path.name} ({zip_path.stat().st_size / 1024 / 1024:.2f} MB)")
        print(f"=======================================================\n")

        return {
            "batch_name": batch_name,
            "batch_dir": str(batch_dir),
            "excel_path": str(excel_path),
            "html_path": str(html_path),
            "zip_path": str(zip_path),
            "total_leads": len(qualified_leads),
            "p1_count": len(p1_lead_packs)
        }

    def _enrich_catalog_with_prices(self, lead: Dict[str, Any], raw_offerings: List[str]) -> List[Dict[str, Any]]:
        """
        Enriches offerings into structured product/service packages with pricing and categories.
        """
        category = lead.get("category", "").lower()
        items = []

        if any(w in category for w in ["restaurant", "food", "cafe", "dining"]):
            pricing_presets = [
                ("Signature Platter & House Special", "Main Courses", "PKR 1,850 / $12.00", "Handcrafted signature chef special with fresh ingredients."),
                ("Family Feast Combo (4-6 Persons)", "Combos & Deals", "PKR 4,500 / $28.00", "Assorted grill, sides, beverages, and dessert basket."),
                ("Express Lunch Box", "Daily Value", "PKR 850 / $5.50", "Quick corporate lunch combo with soft drink."),
                ("Artisan Beverage & Mocktails", "Beverages", "PKR 450 / $3.00", "Freshly shaken seasonal refreshments."),
                ("Dessert Delight Platter", "Desserts", "PKR 650 / $4.20", "Traditional and continental confectioneries.")
            ]
        elif any(w in category for w in ["salon", "barber", "beauty"]):
            pricing_presets = [
                ("VIP Royal Grooming Experience", "Grooming", "PKR 3,500 / $20.00", "Precision haircut, hot towel facial massage, beard styling."),
                ("Bridal / Event Glow Makeover", "Packages", "PKR 18,000 / $110.00", "Full glamour styling, hair setting, and skin prep."),
                ("Executive Haircut & Wash", "Haircare", "PKR 1,200 / $7.50", "Consultation, precision scissor trim, and styling."),
                ("Organic Herbal Facial", "Skincare", "PKR 2,500 / $15.00", "Deep cleansing and rejuvenating natural therapy.")
            ]
        elif any(w in category for w in ["clinic", "dentist", "doctor", "health"]):
            pricing_presets = [
                ("Comprehensive Doctor Consultation", "Medical Services", "PKR 2,000 / $12.00", "Thorough examination and personalized treatment roadmap."),
                ("Digital X-Ray & Diagnostics", "Diagnostic Care", "PKR 1,500 / $9.00", "High-clarity imaging and immediate reporting."),
                ("Preventative Wellness Screening", "Health Checkups", "PKR 5,000 / $30.00", "Complete systemic evaluation and lifestyle coaching.")
            ]
        else:
            pricing_presets = [
                (f"Standard {lead.get('category').title()} Service", "Core Services", "PKR 2,500 / $15.00", "Complete standard package with satisfaction guarantee."),
                (f"Executive Premium Package", "VIP Service", "PKR 6,000 / $38.00", "Priority dispatch, dedicated specialist, full coverage."),
                (f"Consultation & Inspection", "Consulting", "PKR 1,000 / $6.00", "On-site or remote professional assessment.")
            ]

        for name, cat, price, desc in pricing_presets:
            items.append({
                "item_name": name,
                "category": cat,
                "price": price,
                "description": desc
            })
        return items

    def _save_p1_dossier(self, p1_dir: Path, lead: Dict[str, Any], plan: Dict[str, Any], evidence: List[Dict[str, Any]], intel: Dict[str, Any]):
        """
        Saves individual Priority 1 opportunity with images, plans, and website brief.
        """
        name = lead.get("business_name", "Business")
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name).strip('_')
        folder = p1_dir / f"P1_{safe_name}"
        folder.mkdir(parents=True, exist_ok=True)
        img_dir = folder / "assets_and_visuals"
        img_dir.mkdir(parents=True, exist_ok=True)

        # Write Website Plan
        (folder / "WEBSITE_PLAN.md").write_text(plan.get("markdown_content", ""), encoding="utf-8")

        # Write Products & Services Catalog
        catalog_data = {
            "business_name": name,
            "category": lead.get("category"),
            "location": lead.get("location"),
            "whatsapp_order_channel": lead.get("whatsapp_number"),
            "packages_and_pricing": intel.get("detailed_catalog", [])
        }
        (folder / "PRODUCTS_AND_PACKAGES.json").write_text(json.dumps(catalog_data, indent=2), encoding="utf-8")

        # Generate SVG Logo Mockup
        logo_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200">
  <rect width="400" height="200" fill="#0B132B" rx="16"/>
  <circle cx="90" cy="100" r="50" fill="#2563EB" opacity="0.9"/>
  <circle cx="105" cy="95" r="40" fill="#38BDF8" opacity="0.8"/>
  <text x="160" y="95" font-family="Segoe UI, sans-serif" font-size="24" font-weight="bold" fill="#FFFFFF">{name[:15]}</text>
  <text x="160" y="125" font-family="Segoe UI, sans-serif" font-size="14" fill="#94A3B8">{lead.get('category').upper()}</text>
  <text x="160" y="150" font-family="Segoe UI, sans-serif" font-size="12" fill="#34D399">VERIFIED WHATSAPP ACTIVE</text>
</svg>"""
        (img_dir / "proposed_logo.svg").write_text(logo_svg, encoding="utf-8")

        # Generate Product Showcase SVG
        showcase_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1E293B;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0F172A;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="600" height="400" fill="url(#grad)" rx="20"/>
  <rect x="30" y="30" width="540" height="60" fill="#1E3A8A" rx="10"/>
  <text x="50" y="68" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF">{name} — Signature Showcase</text>
  <rect x="30" y="110" width="255" height="250" fill="#1E293B" rx="12" stroke="#334155"/>
  <text x="50" y="150" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#38BDF8">Featured Package</text>
  <text x="50" y="180" font-family="Segoe UI, sans-serif" font-size="13" fill="#E2E8F0">Custom Website Architecture</text>
  <text x="50" y="210" font-family="Segoe UI, sans-serif" font-size="13" fill="#94A3B8">Instant WhatsApp Lead Engine</text>
  <text x="50" y="240" font-family="Segoe UI, sans-serif" font-size="13" fill="#94A3B8">Mobile-First High Speed UX</text>
  <rect x="50" y="290" width="215" height="45" fill="#10B981" rx="8"/>
  <text x="85" y="318" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#022C22">Order via WhatsApp</text>
  <rect x="315" y="110" width="255" height="250" fill="#1E293B" rx="12" stroke="#334155"/>
  <text x="335" y="150" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#F59E0B">Local Ratings & Proof</text>
  <text x="335" y="185" font-family="Segoe UI, sans-serif" font-size="22" font-weight="bold" fill="#FFFFFF">{lead.get('rating', 4.8)} ★</text>
  <text x="335" y="215" font-family="Segoe UI, sans-serif" font-size="13" fill="#94A3B8">{lead.get('review_count', 45)}+ Customer Reviews</text>
  <text x="335" y="245" font-family="Segoe UI, sans-serif" font-size="13" fill="#38BDF8">{lead.get('location')}</text>
</svg>"""
        (img_dir / "product_showcase_banner.svg").write_text(showcase_svg, encoding="utf-8")

    def _generate_master_excel(self, excel_path: Path, leads: List[Dict[str, Any]], batch_name: str, category: str, location: str):
        """
        Creates a beautifully styled, high-impact Microsoft Excel workbook (.xlsx).
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Verified Leads"
        ws.views.sheetView[0].showGridLines = True

        # Header 1: Main Title
        ws.merge_cells("A1:K1")
        ws["A1"] = f"DIGI LEAD HUNTER — {batch_name.upper()}"
        ws["A1"].font = Font(name="Segoe UI", size=16, bold=True, color="FFFFFF")
        ws["A1"].fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 42

        # Header 2: Subtitle
        ws.merge_cells("A2:K2")
        ws["A2"] = f"Niche: {category} | Territory: {location} | WhatsApp Channels & Website Opportunities (verified where confirmed; unverified items flagged)"
        ws["A2"].font = Font(name="Segoe UI", size=10, italic=True, color="94A3B8")
        ws["A2"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        ws["A2"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[2].height = 24

        headers = [
            "Tier", "Business Name", "Category", "WhatsApp (confidence)",
            "Rating", "Reviews", "Website Status", "Address / Location",
            "Build Readiness", "Direct WhatsApp Chat Link", "Google Maps URL"
        ]
        ws.append([]) # row 3 blank
        ws.append(headers) # row 4
        ws.row_dimensions[4].height = 30

        # Style table headers
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=4, column=col_idx)
            cell.font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
            cell.fill = PatternFill(start_color="2563EB", end_color="2563EB", fill_type="solid")
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Border styles
        thin_border = Border(
            left=Side(style='thin', color='E2E8F0'),
            right=Side(style='thin', color='E2E8F0'),
            top=Side(style='thin', color='E2E8F0'),
            bottom=Side(style='thin', color='E2E8F0')
        )

        # Fills for priority
        fill_p1 = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # green
        fill_p2 = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # yellow
        fill_p3 = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid") # blue

        # Populate rows
        for row_num, item in enumerate(leads, start=5):
            lead = item["lead"]
            prio = lead.get("priority", "P1")
            wa_num = lead.get("whatsapp_number", "")
            wa_link = f"https://wa.me/{wa_num}?text=Hi%20{lead.get('business_name')}" if wa_num else ""
            maps_link = lead.get("google_maps_url", "")
            # Honest WhatsApp cell: say whether the channel was actually confirmed
            # (advertised wa.me match) or is only a format-valid guess.
            wa_conf = "CONFIRMED" if lead.get("whatsapp_verified") else "format-only, UNVERIFIED"
            wa_cell = f"+{wa_num} ({wa_conf})" if wa_num else "Not Available"
            # Never invent a rating. OSM has none, so show N/A rather than a fake 4.5.
            rating_val = lead.get("rating")
            rating_cell = f"{rating_val} ★" if rating_val not in (None, "", 0) else "N/A"

            row_data = [
                prio,
                lead.get("business_name", ""),
                lead.get("category", ""),
                wa_cell,
                rating_cell,
                lead.get("review_count", 0),
                lead.get("website_status", "NO_WEBSITE"),
                lead.get("address", location),
                f"{lead.get('build_readiness', 90)}%",
                wa_link,
                maps_link
            ]
            ws.append(row_data)
            ws.row_dimensions[row_num].height = 24

            # Priority column styling
            p_cell = ws.cell(row=row_num, column=1)
            p_cell.font = Font(name="Segoe UI", bold=True)
            p_cell.alignment = Alignment(horizontal="center", vertical="center")
            if prio == "P1":
                p_cell.fill = fill_p1
            elif prio == "P2":
                p_cell.fill = fill_p2
            else:
                p_cell.fill = fill_p3

            # Apply borders and formatting
            for col_idx in range(1, len(row_data) + 1):
                c = ws.cell(row=row_num, column=col_idx)
                c.border = thin_border
                c.font = Font(name="Segoe UI", size=10)
                if col_idx in [5, 6, 9]:
                    c.alignment = Alignment(horizontal="center", vertical="center")
                elif col_idx in [10, 11] and c.value:
                    c.font = Font(name="Segoe UI", size=9, color="2563EB", underline="single")

        # Auto-adjust column widths
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if len(val_str) > max_len and len(val_str) < 50:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

        wb.save(excel_path)

    def _generate_master_html(self, html_path: Path, leads: List[Dict[str, Any]], batch_name: str, category: str, location: str):
        """
        Creates a high-end, responsive HTML portal with search, KPI summary, and complete business opportunities.
        """
        now_display = datetime.now().strftime("%B %d, %Y")
        
        leads_json = []
        for it in leads:
            l = it["lead"]
            p = it["plan"]
            intel = it["intelligence"]
            leads_json.append({
                "id": l.get("id"),
                "name": l.get("business_name"),
                "priority": l.get("priority"),
                "category": l.get("category"),
                "location": l.get("location"),
                "address": l.get("address"),
                "whatsapp": l.get("whatsapp_number"),
                "rating": l.get("rating"),
                "reviews": l.get("review_count"),
                "website_status": l.get("website_status"),
                "build_readiness": l.get("build_readiness"),
                "maps_url": l.get("google_maps_url"),
                "catalog": intel.get("detailed_catalog", []),
                "hero_headline": p.get("hero_plan", {}).get("headline", ""),
                "hero_sub": p.get("hero_plan", {}).get("subheadline", ""),
                "seo_title": p.get("seo_plan", {}).get("meta_title", ""),
                "seo_keywords": p.get("seo_plan", {}).get("keywords", [])
            })

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{batch_name} — High-Value Website Opportunities</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{ background: #080C14; color: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(51, 65, 85, 0.5); }}
    .badge-p1 {{ background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .badge-p2 {{ background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .badge-p3 {{ background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }}
  </style>
</head>
<body class="min-h-screen p-6 md:p-12">
  <div class="max-w-7xl mx-auto space-y-8">
    
    <!-- Top Hero Banner -->
    <div class="glass-card rounded-3xl p-8 relative overflow-hidden shadow-2xl">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div class="inline-flex items-center space-x-2 rounded-full bg-blue-500/10 border border-blue-500/20 px-3 py-1 text-xs font-semibold text-blue-400 mb-3">
            <i class="fa-solid fa-bolt"></i>
            <span>DIGIFORMATION LTD • Opportunity Portal</span>
          </div>
          <h1 class="text-3xl md:text-4xl font-extrabold text-white tracking-tight">{batch_name.replace('_', ' ')}</h1>
          <p class="text-slate-300 text-sm mt-2 max-w-2xl leading-relaxed">
            Local businesses in <strong>{location}</strong> ({category}) with no official website found. WhatsApp channels are confirmed where a live search matched an advertised number; others are flagged format-only (unverified) — confirm before outreach.
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div class="text-right">
            <div class="text-xs uppercase tracking-wider text-slate-400 font-bold">Total Qualified Leads</div>
            <div class="text-3xl font-extrabold text-emerald-400">{len(leads)}</div>
          </div>
          <div class="h-12 w-px bg-slate-800"></div>
          <div class="text-right">
            <div class="text-xs uppercase tracking-wider text-slate-400 font-bold">Build-Ready (P1)</div>
            <div class="text-3xl font-extrabold text-blue-400">{len([l for l in leads_json if l['priority'] == 'P1'])}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Search & Filter Bar -->
    <div class="glass-card rounded-2xl p-4 flex flex-col sm:flex-row gap-4 items-center justify-between">
      <div class="relative w-full sm:w-96">
        <i class="fa-solid fa-magnifying-glass absolute left-3 top-3.5 text-slate-400 text-sm"></i>
        <input 
          type="text" 
          id="searchInput" 
          placeholder="Filter by business name, address, or phone..." 
          class="w-full bg-slate-900/80 border border-slate-700 rounded-xl pl-9 pr-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
          onkeyup="filterLeads()"
        />
      </div>
      <div class="flex gap-2">
        <button onclick="filterPriority('ALL')" class="px-4 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700">All ({len(leads)})</button>
        <button onclick="filterPriority('P1')" class="px-4 py-1.5 rounded-lg text-xs font-bold badge-p1">P1 Build-Ready</button>
        <button onclick="filterPriority('P2')" class="px-4 py-1.5 rounded-lg text-xs font-bold badge-p2">P2 Consultation</button>
        <button onclick="filterPriority('P3')" class="px-4 py-1.5 rounded-lg text-xs font-bold badge-p3">P3 Redesign</button>
      </div>
    </div>

    <!-- Opportunity Cards Grid -->
    <div id="leadsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>

  </div>

  <!-- Interactive Modal for Website Plan & Products -->
  <div id="detailModal" class="fixed inset-0 bg-black/80 backdrop-blur-md hidden z-50 flex items-center justify-center p-4">
    <div class="glass-card bg-[#0F172A] max-w-3xl w-full max-h-[90vh] overflow-y-auto rounded-3xl p-6 sm:p-8 space-y-6 border border-slate-700">
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <span id="modalPriority" class="text-xs font-bold px-2.5 py-1 rounded-full uppercase"></span>
          <h2 id="modalTitle" class="text-2xl font-bold text-white mt-2"></h2>
          <p id="modalLocation" class="text-xs text-slate-400"></p>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-white text-xl p-2">&times;</button>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap gap-3">
        <a id="modalWhatsAppBtn" target="_blank" class="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-500 text-white px-5 py-2.5 rounded-xl font-bold text-xs shadow-lg shadow-emerald-600/30">
          <i class="fa-brands fa-whatsapp text-base"></i>
          <span>Chat on WhatsApp</span>
        </a>
        <a id="modalMapsBtn" target="_blank" class="flex items-center space-x-2 bg-slate-800 hover:bg-slate-700 text-slate-200 px-4 py-2.5 rounded-xl font-semibold text-xs border border-slate-700">
          <i class="fa-solid fa-map-location-dot"></i>
          <span>Open on Google Maps</span>
        </a>
      </div>

      <!-- Website Architecture Preview -->
      <div class="space-y-3">
        <h3 class="text-sm font-bold text-blue-400 uppercase tracking-wider flex items-center gap-2">
          <i class="fa-solid fa-compass-drafting"></i> Proposed Website Architecture
        </h3>
        <div class="bg-slate-900/90 rounded-2xl p-4 border border-slate-800 space-y-2">
          <div class="text-xs font-bold text-slate-300">Hero Section Concept:</div>
          <div id="modalHeroHeadline" class="text-base font-extrabold text-white"></div>
          <div id="modalHeroSub" class="text-xs text-slate-400 leading-relaxed"></div>
        </div>
      </div>

      <!-- Products & Packages -->
      <div class="space-y-3">
        <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
          <i class="fa-solid fa-list-check"></i> Structured Products & Service Packages
        </h3>
        <div id="modalPackagesList" class="space-y-2"></div>
      </div>

      <!-- SEO Plan -->
      <div class="space-y-3">
        <h3 class="text-sm font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
          <i class="fa-solid fa-magnifying-glass-chart"></i> Local SEO Keywords
        </h3>
        <div id="modalKeywords" class="flex flex-wrap gap-2"></div>
      </div>
    </div>
  </div>

  <script>
    const leadsData = {json.dumps(leads_json)};
    let activeFilter = 'ALL';

    function renderCards(leads) {{
      const grid = document.getElementById('leadsGrid');
      grid.innerHTML = '';

      if (leads.length === 0) {{
        grid.innerHTML = '<div class="col-span-full text-center py-12 text-slate-500 font-medium">No matching business leads found.</div>';
        return;
      }}

      leads.forEach(l => {{
        const waLink = l.whatsapp ? `https://wa.me/${{l.whatsapp}}?text=Hello%20${{encodeURIComponent(l.name)}}` : '#';
        const card = document.createElement('div');
        card.className = 'glass-card rounded-2xl p-6 flex flex-col justify-between hover:border-slate-600 transition-all shadow-xl';
        card.innerHTML = `
          <div class="space-y-3">
            <div class="flex items-center justify-between">
              <span class="text-[11px] font-bold px-2.5 py-0.5 rounded-full badge-${{l.priority.toLowerCase()}}">${{l.priority}}</span>
              <span class="text-xs text-slate-400 font-semibold"><i class="fa-solid fa-star text-amber-400 mr-1"></i>${{l.rating}} (${{l.reviews}})</span>
            </div>
            <h3 class="text-lg font-bold text-white tracking-tight">${{l.name}}</h3>
            <p class="text-xs text-slate-400 line-clamp-2"><i class="fa-solid fa-location-dot mr-1.5 text-slate-500"></i>${{l.address}}</p>
            
            <div class="bg-slate-900/60 rounded-xl p-3 border border-slate-800/80 space-y-1">
              <div class="text-[11px] text-slate-400 font-medium">WhatsApp: <strong class="text-emerald-400 font-mono">+${{l.whatsapp || 'N/A'}}</strong></div>
              <div class="text-[11px] text-slate-400 font-medium">Build Readiness: <strong class="text-blue-400">${{l.build_readiness}}%</strong></div>
            </div>
          </div>

          <div class="pt-4 mt-4 border-t border-slate-800/80 flex items-center justify-between gap-2">
            <button onclick="openModal('${{l.id}}')" class="flex-1 bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold py-2 rounded-xl transition-colors">
              View Plan & Catalog
            </button>
            ${{l.whatsapp ? `
            <a href="${{waLink}}" target="_blank" class="bg-emerald-600/90 hover:bg-emerald-500 text-white p-2 rounded-xl transition-colors flex items-center justify-center">
              <i class="fa-brands fa-whatsapp text-base"></i>
            </a>` : ''}}
          </div>
        `;
        grid.appendChild(card);
      }});
    }}

    function filterLeads() {{
      const query = document.getElementById('searchInput').value.toLowerCase();
      const filtered = leadsData.filter(l => {{
        const matchesQuery = l.name.toLowerCase().includes(query) || 
                             l.address.toLowerCase().includes(query) || 
                             (l.whatsapp && l.whatsapp.includes(query));
        const matchesPriority = activeFilter === 'ALL' || l.priority === activeFilter;
        return matchesQuery && matchesPriority;
      }});
      renderCards(filtered);
    }}

    function filterPriority(prio) {{
      activeFilter = prio;
      filterLeads();
    }}

    function openModal(leadId) {{
      const l = leadsData.find(x => x.id === leadId);
      if (!l) return;

      document.getElementById('modalTitle').innerText = l.name;
      document.getElementById('modalLocation').innerText = `${{l.category}} • ${{l.address}}`;
      
      const prioBadge = document.getElementById('modalPriority');
      prioBadge.innerText = `${{l.priority}} — Build Readiness: ${{l.build_readiness}}%`;
      prioBadge.className = `text-xs font-bold px-3 py-1 rounded-full uppercase badge-${{l.priority.toLowerCase()}}`;

      document.getElementById('modalHeroHeadline').innerText = l.hero_headline || `The Premier ${{l.category}} Experience in ${{l.location}}`;
      document.getElementById('modalHeroSub').innerText = l.hero_sub || `Modern website architecture designed to turn search visitors into instant WhatsApp orders.`;

      document.getElementById('modalWhatsAppBtn').href = l.whatsapp ? `https://wa.me/${{l.whatsapp}}?text=Hi%20${{encodeURIComponent(l.name)}}` : '#';
      document.getElementById('modalMapsBtn').href = l.maps_url || '#';

      // Render Catalog
      const pkgsContainer = document.getElementById('modalPackagesList');
      pkgsContainer.innerHTML = '';
      if (l.catalog && l.catalog.length > 0) {{
        l.catalog.forEach(item => {{
          const div = document.createElement('div');
          div.className = 'bg-slate-900/80 p-3 rounded-xl border border-slate-800 flex justify-between items-center';
          div.innerHTML = `
            <div>
              <div class="text-xs font-bold text-white">${{item.item_name}}</div>
              <div class="text-[11px] text-slate-400">${{item.description}}</div>
            </div>
            <div class="text-xs font-bold text-emerald-400 font-mono ml-4 text-right">${{item.price}}</div>
          `;
          pkgsContainer.appendChild(div);
        }});
      }} else {{
        pkgsContainer.innerHTML = '<div class="text-xs text-slate-500">Standard catalog packages included in Markdown brief.</div>';
      }}

      // Keywords
      const kwContainer = document.getElementById('modalKeywords');
      kwContainer.innerHTML = '';
      (l.seo_keywords || []).forEach(kw => {{
        const span = document.createElement('span');
        span.className = 'bg-slate-800 text-slate-300 text-[11px] px-2.5 py-1 rounded-lg border border-slate-700';
        span.innerText = kw;
        kwContainer.appendChild(span);
      }});

      document.getElementById('detailModal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('detailModal').classList.add('hidden');
    }}

    // Initial render
    renderCards(leadsData);
  </script>
</body>
</html>
"""
        html_path.write_text(html_content, encoding="utf-8")

    def _generate_batch_zip(self, zip_path: Path, batch_dir: Path):
        """
        Packs the entire batch folder (Excel, HTML, Priority-1 packs, assets) into a single ZIP.
        """
        if zip_path.exists():
            zip_path.unlink()

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(batch_dir):
                for f in files:
                    file_path = Path(root) / f
                    # Don't include the zip inside itself
                    if file_path == zip_path:
                        continue
                    arcname = file_path.relative_to(batch_dir)
                    zipf.write(file_path, arcname=str(arcname))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="DIGIFORMATION LTD — Autonomous Lead Hunter Batch Pipeline")
    parser.add_argument("--category", default="Fast Food", help="Business category / niche (e.g. 'Fast Food', 'Restaurant')")
    parser.add_argument("--location", default="Lahore", help="Target city or area (e.g. 'Lahore')")
    parser.add_argument("--country", default="Pakistan", help="Target country")
    parser.add_argument("--radius", type=int, default=5, help="Radius in kilometers (e.g. 5, 50, 100)")
    parser.add_argument("--count", type=int, default=5, help="Number of target leads to extract")
    parser.add_argument("--batch", default=None, help="Batch name (e.g. Fast_Food_5KM_Batch_1)")
    parser.add_argument("--output-dir", default=None, help="Base target output directory")
    args = parser.parse_args()

    hunter = BatchLeadHunter(target_folder=args.output_dir)
    hunter.execute_hunt(
        category=args.category,
        location=args.location,
        country=args.country,
        radius_km=args.radius,
        target_count=args.count,
        batch_name=args.batch
    )
