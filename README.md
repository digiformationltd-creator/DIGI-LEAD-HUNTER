# DIGI LEAD HUNTER
### AI-Powered Local Business Lead Intelligence, Website Opportunity Research & Packaging Platform
**Official Product of Digiformation LTD • Sponsored by Digi Biz OS**

[![License: Source-Available](https://img.shields.io/badge/License-Source--Available-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![React 18](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-indigo.svg)](https://vitejs.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-teal.svg)](https://fastapi.tiangolo.com/)
[![WhatsApp Support](https://img.shields.io/badge/WhatsApp-03164467464-25D366.svg?logo=whatsapp&logoColor=white)](https://wa.me/923164467464)

---

## 🌟 Executive Overview

**Lead Hunter** is an autonomous intelligence and website-opportunity research platform developed by **Digiformation LTD**. It solves the core client acquisition bottleneck for web agencies and developers by discovering local businesses on **Google Maps** that have strong customer reviews and operational presence, but **lack an official website** or possess a broken/outdated web presence.

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

Lead Hunter is proudly developed and maintained by **Digiformation LTD**:

- **WhatsApp Support Hotline:** [+92 316 4467464 (03164467464)](https://wa.me/923164467464?text=Hello%20Digi%20Formation%2C%20I%20am%20using%20Lead%20Hunter)
- **Corporate Email:** [digiformation.info@digiformation.co.uk](mailto:digiformation.info@digiformation.co.uk)
- **Product Inquiries:** [info@digibizwiz.co.uk](mailto:info@digibizwiz.co.uk)
- **Digi Formation UK:** [https://www.digiformation.co.uk/](https://www.digiformation.co.uk/)
- **Digi Biz OS Ecosystem:** [https://www.digibizos.co.uk/](https://www.digibizos.co.uk/)
- **Official Linktree:** [https://linktr.ee/digiformationltd](https://linktr.ee/digiformationltd)

---

## ⚡ 1-Click Antigravity Setup Experience

This repository is optimized for the **Antigravity AI Agent environment**. When you clone or unzip this repository into Antigravity, simply tell the agent:

```text
SETUP FOR ME
```

Antigravity will automatically:
1. Read `MASTER_SETUP.md`.
2. Install Python backend dependencies (`fastapi`, `uvicorn`, `pydantic`, `httpx`).
3. Install frontend Node modules and compile the Control Center distribution.
4. Initialize the SQLite local database (`data/database/lead_hunter.db`).
5. Run automated test suites to ensure 100% verification.
6. Launch the Control Center on `http://localhost:8000` and open your default web browser.

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
- `README.md`: Business summary, opportunity tier, and Digi Formation contact details.
- `WEBSITE_PLAN.md`: Strategic website plan, information architecture, and target audience.
- `WEBSITE_PLAN.html`: Formatted, printable presentation document ready for client review.
- `WEBSITE_BUILD_BRIEF.md`: Developer blueprint for rapid site building.
- `EVIDENCE_REPORT.md`: Factual proof ledger with timestamps and confidence scores.
- `MISSING_INFORMATION.md`: Client onboarding checklist and specific questions to ask the owner.
- `ASSET_MANIFEST.json`: Public assets, visual palettes, and location data.
- `PACKAGE_MANIFEST.json`: Cryptographic integrity validation metadata.

---

## 🛡️ Usage & License Terms

**Digi Biz OS — Lead Hunter** is published under the **Digiformation LTD Source-Available (Personal & Internal Use) License**.

### Allowed (Permitted):
- You may download and inspect the complete source code.
- You may run the application locally for your own personal use.
- You may run the application for internal client acquisition and lead generation workflows within your business or agency.
- You may make private code modifications for internal use, provided all original branding, logos, and copyright notices remain intact.

### Not Allowed (Strictly Prohibited):
- **No Commercial Resale:** You may not sell the software, sell modified versions, or charge for access to the codebase.
- **No SaaS / Paid Hosting:** You may not host this software as a public commercial service, SaaS platform, or paid API.
- **No White-Labeling:** You may not remove or obscure the Digiformation LTD or Digi Biz OS branding, logos, or copyright notices.
- **No Rebranding:** You may not re-package or re-brand this tool under another company name.

All copyright and intellectual property rights remain exclusively with **Digiformation LTD**.

---

## 💬 Direct Support Desk
Have questions, need custom lead filters, or want enterprise consulting?
- **WhatsApp:** [+92 316 4467464](https://wa.me/923164467464)
- **Email:** [digiformation.info@digiformation.co.uk](mailto:digiformation.info@digiformation.co.uk)
