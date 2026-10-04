<p align="center">
  <img src="digi-lead-hunter-banner.jpg" alt="DIGI LEAD HUNTER" width="100%" />
</p>

# DIGI LEAD HUNTER
### Autonomous AI Lead Intelligence, Website Opportunity Hunter & Evidence Packaging Platform
**Official Product of DIGIFORMATION LTD • Sponsored by Digi Biz OS**

[![License: Source-Available](https://img.shields.io/badge/License-Source--Available-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-indigo.svg)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![WhatsApp Support](https://img.shields.io/badge/WhatsApp-03164467464-25D366.svg?logo=whatsapp&logoColor=white)](https://wa.me/923164467464)

---

## 🌟 Executive Overview

**Lead Hunter** is an autonomous intelligence and website-opportunity research platform developed by **DIGIFORMATION LTD**. It solves the core client acquisition bottleneck for web agencies and developers by discovering local businesses on **Google Maps** that have strong customer reviews and operational presence, but **lack an official website** or possess a broken/outdated web presence.

Instead of scraping raw phone numbers, Lead Hunter:
1. **Verifies business identity & Google Maps presence** across any category and city.
2. **Validates direct WhatsApp mobile channels** (supporting Pakistan +92, UK +44, US +1, and international carriers).
3. **Audits website gaps** and categorizes leads into 3 actionable tiers:
   - **Priority 1 (Build-Ready):** No website + Verified WhatsApp + Rich public assets (photos, reviews, hours).
   - **Priority 2 (Consultation):** No website + WhatsApp + Limited assets (generates client question checklists).
   - **Priority 3 (Modernization):** Outdated visual layout, broken CTA, or poor mobile UX (generates redesign pitches).
4. **Generates full website architecture plans (`WEBSITE_PLAN.md`)** with page layouts, hero copy, direct WhatsApp CTAs, and local SEO keywords.
5. **Packages deliverables into standalone ZIP archives** (`<BUSINESS_NAME>_WEBSITE_OPPORTUNITY_PACK.zip`) ready for 1-click download.

---

## 🏢 Official Company & Contact Directory

Lead Hunter is proudly developed and maintained by **DIGIFORMATION LTD**:

- **WhatsApp Support Hotline:** [+92 316 4467464 (03164467464)](https://wa.me/923164467464?text=Hello%20DIGIFORMATION%20LTD%2C%20I%20am%20using%20Lead%20Hunter)
- **Corporate Emails:** [info@digiformation.co.uk](mailto:info@digiformation.co.uk) • [info@digibizos.co.uk](mailto:info@digibizos.co.uk)
- **DIGIFORMATION LTD UK:** [https://www.digiformation.co.uk/](https://www.digiformation.co.uk/)
- **Digi Biz OS Ecosystem:** [https://www.digibizos.co.uk/](https://www.digibizos.co.uk/)
- **Official Linktree:** [https://linktr.ee/digiformationltd](https://linktr.ee/digiformationltd)

---

## ⚡ Autonomous Antigravity Prompt Execution (No UI Needed)

This repository is optimized for direct **Antigravity AI Agent prompt-based execution**. When you give Antigravity a command like:
```text
Extract 100 restaurant leads in Lahore with complete website opportunity packs
```

**Tracking UI:** Visit `http://localhost:8000` after deployment to view lead tracking dashboard. From there you can download ZIP, WORD, and EXCEL packages, and view the full evidence report.

**Google Shop Link:** Each lead includes a direct link to its Google Shopping page (e.g., `https://shopping.google.com/...`) for cross‑verification of product listings and contact numbers.

Antigravity executes the autonomous 5-phase pipeline directly in your selected workspace:
1. **Creates Automated Batch Folder:** (e.g. `Restaurant_Batch_1`) directly inside your target project directory.
2. **Generates Master Excel Spreadsheet (`.xlsx`):** Professional Microsoft Excel sheet with verified WhatsApp numbers, one-click WhatsApp chat links, Google Maps locations, ratings, and build-readiness status.
3. **Generates Interactive Opportunity Portal (`.html`):** Beautiful, responsive HTML dashboard featuring live search filters, hero concepts, and structured packages.
4. **Builds Priority-1 (Build-Ready) Deliverables:** Complete website architecture blueprints (`WEBSITE_PLAN.md`), mockups, and product/pricing packages (`PRODUCTS_AND_PACKAGES.json`).
5. **Generates Complete ZIP Archive:** A standalone `<BATCH_NAME>_COMPLETE_PACK.zip` packed and ready for distribution or client outreach.

### Running via Terminal / CLI:
```bash
python batch_hunter.py --category "Restaurant" --location "Lahore" --count 100
```

---

## 🚀 Manual Quickstart Guide

### Windows (PowerShell):
```powershell
# 1. Run automated setup script
./scripts/setup.ps1

# 2. Start the Control Center
python run.py
```

### Linux / macOS:
```bash
# 1. Make executable and run setup
chmod +x scripts/*.sh
./scripts/setup.sh

# 2. Start the Control Center
python run.py
```

Once running, navigate to:
👉 **`http://localhost:8000`** (Full Control Center UI & REST API)

---

## 📐 System Architecture & Pipelines

```text
User Search Request (Category + Location + Radius)
        ↓
Phase 01: Google Maps / OSM Overpass Discovery Engine
        ↓
Phase 02: Verification Engine (Identity, Website Status, WhatsApp Carrier Detection)
        ↓
Phase 03: 3-Tier Classification (P1 Build-Ready / P2 Consultation / P3 Redesign)
        ↓
Phase 04: Business & Asset Intelligence (Hours, Reviews, Offerings, Visual Signals)
        ↓
Phase 05: Website Build-Ready Planning (IA, Hero Plan, WhatsApp CTA Strategy, Local SEO)
        ↓
Phase 06: Evidence, Markdown, HTML Presentation & ZIP Packaging Engine
        ↓
Phase 07: Runtime Orchestration & SQLite Database Persistence
        ↓
Phase 08: Premium Glassmorphic Control Center UI
```

---

## 📦 What's Inside each Opportunity ZIP Package?

For every qualified business, the engine outputs a structured client opportunity folder and ZIP archive:
- `README.md`: Business summary, opportunity tier, and DIGIFORMATION LTD contact details.
- `WEBSITE_PLAN.md`: Strategic website plan, information architecture, and target audience.
- `WEBSITE_PLAN.html`: Formatted, printable presentation document ready for client review.
- `WEBSITE_BUILD_BRIEF.md`: Developer blueprint for rapid site building.
- `EVIDENCE_REPORT.md`: Factual proof ledger with timestamps and confidence scores.
- `MISSING_INFORMATION.md`: Client onboarding checklist and specific questions to ask the owner.
- `ASSET_MANIFEST.json`: Public assets, visual palettes, and location data.
- `PACKAGE_MANIFEST.json`: Cryptographic integrity validation metadata.

---

## 🛡️ Usage & License Terms

**Digi Biz OS — Lead Hunter** is published under the **DIGIFORMATION LTD Source-Available (Personal & Internal Use) License**.

### Allowed (Permitted):
- You may download and inspect the complete source code.
- You may run the application locally for your own personal use.
- You may run the application for internal client acquisition and lead generation workflows within your business or agency.
- You may make private code modifications for internal use, provided all original branding, logos, and copyright notices remain intact.

### Not Allowed (Strictly Prohibited):
- **No Commercial Resale:** You may not sell the software, sell modified versions, or charge for access to the codebase.
- **No SaaS / Paid Hosting:** You may not host this software as a public commercial service, SaaS platform, or paid API.
- **No White-Labeling:** You may not remove or obscure the DIGIFORMATION LTD or Digi Biz OS branding, logos, or copyright notices.
- **No Rebranding:** You may not re-package or re-brand this tool under another company name.

All copyright and intellectual property rights remain exclusively with **DIGIFORMATION LTD**.

---

## 💬 Direct Support Desk
Have questions, need custom lead filters, or want enterprise consulting?
- **WhatsApp:** [+92 316 4467464](https://wa.me/923164467464)
- **Email:** [info@digiformation.co.uk](mailto:info@digiformation.co.uk)
