# How DIGI Lead Hunter Works: Autonomous Pipeline & Business Value

> **By DIGIFORMATION LTD • Sponsored by Digi Biz OS**  
> *Transforming public local business data into high-converting web agency opportunities — 100% free and open-source.*

---

## 🎯 The Core Problem We Solve

Web developers, digital agencies, and freelancers waste hundreds of hours manually browsing Google Maps looking for clients. Most of the time:
1. They encounter businesses that **already have websites**.
2. They pitch businesses with **landline phones that don't have WhatsApp**.
3. They arrive empty-handed without any concrete concept, mockup, or proposal ready.

**DIGI Lead Hunter** automates the entire discovery-to-pitch workflow with an autonomous 5-stage verification and evidence engine.

---

## ⚡ The 5-Stage Autonomous Pipeline

```text
  [ User Search Criteria: Category + City + Radius ]
                          │
                          ▼
  ┌────────────────────────────────────────────────────────┐
  │ 1. Discovery Engine (OpenStreetMap / Overpass POI)    │
  │    • Extracts authentic physical local establishments  │
  │    • Zero synthetic or fake entries generated          │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. Multi-Engine Verification & Anti-False-Positive    │
  │    • Live consensus search (DuckDuckGo, Bing, Mojeek)  │
  │    • Filters social pages (Facebook, Instagram, Yelp)  │
  │    • Verifies genuine "NO_WEBSITE" status with proof   │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. Deep Telephony & WhatsApp Channel Detection         │
  │    • Formats international numbers with libphonenumber │
  │    • Validates mobile carrier status vs landlines      │
  │    • Generates instant 1-click WhatsApp chat links     │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. Quality Gate & Priority Classification              │
  │    • Priority 1 (Build-Ready): No site + Mobile WA     │
  │    • Priority 2 (Consultation): Missing asset details  │
  │    • Priority 3 (Modernization): Outdated / Non-mobile │
  └──────────────────────────┬─────────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────────┐
  │ 5. Automated Deliverable & Pitch Packaging             │
  │    • Generates WEBSITE_PLAN.md & client presentations  │
  │    • Assembles ready-to-send ZIP opportunity packs     │
  │    • Live synchronization with Localhost Dashboard     │
  └────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Benefits for Agencies & Developers

### 1. Zero Paid API Costs ($0 Overhead)
No expensive Google Cloud billing, SerpAPI subscriptions, or Twilio credits. The entire engine runs locally using open geospatial data and offline carrier analysis libraries.

### 2. High-Conversion Priority 1 Filtering
Instead of cold-calling dead numbers, the engine exclusively promotes **Priority 1 (Build-Ready)** leads that have confirmed mobile numbers, active customer engagement, and a verified absence of an official website.

### 3. Complete Pre-Built Pitch In Every Lead
You don't pitch with just "Do you need a website?". Each lead includes:
- **`WEBSITE_PLAN.md`:** Pre-planned information architecture, target audience analysis, and hero copy.
- **`WEBSITE_PLAN.html`:** Clean, printable presentation you can share directly with the owner.
- **1-Click WhatsApp Link:** Instant pre-filled outreach message to start the conversation in seconds.

### 4. 100% Privacy & Data Ownership
All discovered leads and generated client proposals stay strictly on your local machine in SQLite. Your agency's pipeline is completely private.

---

## 🏁 Getting Started

Clone the repository and launch the dashboard in under two minutes:

```bash
git clone https://github.com/digiformationltd-creator/DIGI-LEAD-HUNTER.git
cd DIGI-LEAD-HUNTER
python run.py
```

Then visit **`http://localhost:8000`** to run your first autonomous lead hunt!
