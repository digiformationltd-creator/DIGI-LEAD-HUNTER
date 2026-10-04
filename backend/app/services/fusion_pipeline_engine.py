"""
DIGIFORMATION LTD — Lead Hunter
Fusion Pipeline Engine (LangGraph-style Cyclic State Machine)
Orchestrates:
1. Discovery (Overpass / Nominatim)
2. Multi-Engine Search Consensus (DDG + Bing + Mojeek)
3. Telephony Carrier Validation (Google libphonenumber)
4. Deep Crawling (Cloudflare XOR email decode, JSON-LD, click-to-chat)
5. DNS MX Deliverability (dnspython)
6. Strict 2-Signal Quality Gating (Zero-fabrication)
7. Packaging & Immutable Evidence Ledger
"""
import uuid
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

from database import get_connection
from services.discovery_service import DiscoveryService
from services.verification_service import VerificationService
from services.classification_service import ClassificationService
from services.intelligence_service import IntelligenceService
from services.planning_service import PlanningService
from services.packaging_service import PackagingService

logger = logging.getLogger("FusionPipelineEngine")

class FusionPipelineEngine:
    def __init__(self):
        self.discovery = DiscoveryService()
        self.verification = VerificationService()
        self.classification = ClassificationService()
        self.intelligence = IntelligenceService()
        self.planning = PlanningService()
        self.packaging = PackagingService()

    def run_pipeline(
        self,
        run_id: str,
        category: str,
        location: str,
        country: str = "Pakistan",
        scope: str = "CITY",
        radius_km: int = 50,
        target_count: int = 15,
        priority_filters: Optional[List[str]] = None,
        event_callback: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end verified pipeline with stage checkpoints.
        """
        def emit(stage: str, msg: str, level: str = "INFO"):
            if event_callback:
                try:
                    event_callback(run_id, stage, msg, level)
                except Exception:
                    pass
            logger.info(f"[{run_id}] [{stage}] {msg}")

        filters = priority_filters or ["P1", "P2", "P3"]
        now_str = datetime.now().isoformat()

        # Step 1: DISCOVERY
        emit("DISCOVERING", f"Initiating multi-source discovery for '{category}' in {location}, {country} (Scope: {radius_km} KM)...")
        candidates = self.discovery.discover_candidates(
            category=category,
            location=location,
            country=country,
            scope=scope,
            radius_km=radius_km,
            target_count=target_count
        )
        emit("DISCOVERING", f"Discovered {len(candidates)} raw candidate POIs with verified physical coordinates.")

        verified_leads = []
        p1_count = 0
        p2_count = 0
        p3_count = 0
        unclear_count = 0
        excluded_count = 0

        # Step 2: PER-CANDIDATE MULTI-STAGE VERIFICATION & PACKAGING
        for idx, cand in enumerate(candidates, 1):
            biz_name = cand.get("business_name", "Unknown")
            emit("VERIFYING", f"[{idx}/{len(candidates)}] Verifying '{biz_name}' across multi-search consensus & carrier registry...")

            try:
                # Stage 2.1: Multi-Engine Verification & Carrier Telephony
                verified_lead, evidence_list = self.verification.verify_candidate(cand)
                web_status = verified_lead.get("website_status")
                wa_status = verified_lead.get("whatsapp_status")

                if web_status == "WEBSITE_STATUS_UNCLEAR":
                    unclear_count += 1

                # Stage 2.2: Strict 2-Signal Classification
                priority, readiness, missing_info = self.classification.classify_lead(verified_lead)
                verified_lead["priority"] = priority
                verified_lead["build_readiness"] = readiness
                verified_lead["missing_info"] = missing_info

                if priority == "EXCLUDED" or (filters and priority not in filters):
                    excluded_count += 1
                    emit("CLASSIFYING", f"Excluded: '{biz_name}' (Status: {web_status}, Priority: {priority})")
                    continue

                # Stage 2.3: Intelligence Enrichment
                intel = self.intelligence.enrich_lead(verified_lead)
                verified_lead["offerings"] = intel.get("offerings", [])
                verified_lead["visual_signals"] = intel.get("visual_signals", {})

                # Stage 2.4: Architecture Planning
                plan = self.planning.generate_plan(verified_lead, intel)

                # Stage 2.5: Packaging & Cryptographic Evidence
                package = self.packaging.create_package(verified_lead, plan, evidence_list, intel)

                # Stage 2.6: Commit to SQLite Database
                self._save_lead_to_db(run_id, verified_lead, plan, package, evidence_list, intel.get("assets", []))

                if priority == "P1":
                    p1_count += 1
                elif priority == "P2":
                    p2_count += 1
                elif priority == "P3":
                    p3_count += 1

                verified_leads.append(verified_lead)
                emit("PACKAGING", f"Packaged {priority} Lead: '{biz_name}' (Web: {web_status}, WhatsApp: {wa_status})")

            except Exception as e:
                emit("ERROR", f"Verification failure on candidate '{biz_name}': {str(e)}", level="ERROR")

        # Step 3: FINALIZE
        qualified_total = len(verified_leads)
        emit("COMPLETED", f"Pipeline complete: {qualified_total} leads certified ({p1_count} P1 Prime, {p2_count} P2 Consultation, {p3_count} P3 Modernization/Unclear).")

        return {
            "run_id": run_id,
            "total_candidates": len(candidates),
            "qualified_count": qualified_total,
            "p1_count": p1_count,
            "p2_count": p2_count,
            "p3_count": p3_count,
            "unclear_count": unclear_count,
            "excluded_count": excluded_count,
            "leads": verified_leads
        }

    def _save_lead_to_db(
        self,
        run_id: str,
        lead: Dict[str, Any],
        plan: Dict[str, Any],
        package: Dict[str, Any],
        evidence_list: List[Dict[str, Any]],
        assets: List[Dict[str, Any]]
    ):
        conn = get_connection()
        cursor = conn.cursor()
        now_str = datetime.now().isoformat()
        lead_id = lead.get("id") or f"lead_{uuid.uuid4().hex[:10]}"
        lead["id"] = lead_id

        cursor.execute("""
        INSERT OR REPLACE INTO leads (
            id, run_id, business_name, category, address, location, google_maps_url,
            phone, phone_normalized, whatsapp_number, whatsapp_status, website_url,
            website_status, website_audit, rating, review_count, business_hours,
            description, priority, build_readiness, missing_info, offerings,
            visual_signals, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id, run_id, lead.get("business_name"), lead.get("category"),
            lead.get("address"), lead.get("location"), lead.get("google_maps_url"),
            lead.get("phone"), lead.get("phone_normalized"), lead.get("whatsapp_number"),
            lead.get("whatsapp_status"), lead.get("website_url"), lead.get("website_status"),
            json.dumps(lead.get("website_audit", {})), lead.get("rating"), lead.get("review_count"),
            lead.get("business_hours"), lead.get("description"), lead.get("priority"),
            lead.get("build_readiness"), json.dumps(lead.get("missing_info", [])),
            json.dumps(lead.get("offerings", [])), json.dumps(lead.get("visual_signals", {})),
            now_str, now_str
        ))

        for ev in evidence_list:
            cursor.execute("""
            INSERT INTO lead_evidence (lead_id, claim, value, evidence_level, source, source_url, observed_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lead_id, ev.get("claim"), str(ev.get("value", "")),
                ev.get("evidence_level"), ev.get("source"), ev.get("source_url"),
                ev.get("observed_at"), ev.get("notes")
            ))

        cursor.execute("""
        INSERT OR REPLACE INTO website_plans (
            id, lead_id, plan_type, target_audience, objectives, cta_strategy,
            whatsapp_strategy, info_architecture, hero_plan, sections_plan,
            visual_direction, seo_plan, markdown_content, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            plan["id"], lead_id, plan["plan_type"], plan["target_audience"],
            json.dumps(plan["objectives"]), json.dumps(plan["cta_strategy"]),
            json.dumps(plan["whatsapp_strategy"]), json.dumps(plan["info_architecture"]),
            json.dumps(plan["hero_plan"]), json.dumps(plan["sections_plan"]),
            json.dumps(plan["visual_direction"]), json.dumps(plan["seo_plan"]),
            plan["markdown_content"], now_str
        ))

        cursor.execute("""
        INSERT OR REPLACE INTO packages (
            id, lead_id, business_name, priority, version, zip_filename, zip_path, zip_size_bytes, is_valid, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            package["id"], lead_id, package["business_name"], package["priority"],
            package["version"], package["zip_filename"], package["zip_path"],
            package["zip_size_bytes"], 1 if package["is_valid"] else 0, now_str
        ))

        conn.commit()
        conn.close()
