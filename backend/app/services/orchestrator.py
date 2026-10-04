"""
Digiformation LTD — Lead Hunter
Phase 07: End-to-End Runtime Orchestrator
"""
import uuid
import json
import threading
from datetime import datetime
from typing import Dict, Any, List, Optional

from database import get_connection
from services.discovery_service import DiscoveryService
from services.verification_service import VerificationService
from services.classification_service import ClassificationService
from services.intelligence_service import IntelligenceService
from services.planning_service import PlanningService
from services.packaging_service import PackagingService

class Orchestrator:
    def __init__(self):
        self.discovery = DiscoveryService()
        self.verification = VerificationService()
        self.classification = ClassificationService()
        self.intelligence = IntelligenceService()
        self.planning = PlanningService()
        self.packaging = PackagingService()

    def start_run(self, req: Dict[str, Any]) -> str:
        run_id = f"run_{uuid.uuid4().hex[:12]}"
        now_str = datetime.now().isoformat()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO runs (
            run_id, created_at, started_at, status, category, location, radius,
            target_count, priority_filters, research_depth, package_mode
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id, now_str, now_str, "INITIALIZING",
            req.get("category"), req.get("location"), req.get("radius", 50),
            req.get("target_count", 15), json.dumps(req.get("priority_filters", ["P1", "P2", "P3"])),
            req.get("research_depth", "Standard"), req.get("package_mode", "Full Package")
        ))
        conn.commit()
        conn.close()

        scope_desc = f"{req.get('scope', 'CITY')} Scope ({req.get('radius', 50)} KM)"
        self._log_event(run_id, "INITIALIZING", f"Initialized Lead Hunter search for {req.get('category')} in {req.get('location')}, {req.get('country', 'Pakistan')} [{scope_desc}]. 100% Shariah filter active.")

        t = threading.Thread(target=self._execute_pipeline, args=(run_id, req), daemon=True)
        t.start()

        return run_id

    def _execute_pipeline(self, run_id: str, req: Dict[str, Any]):
        category = req.get("category")
        location = req.get("location")
        country = req.get("country", "Pakistan")
        scope = req.get("scope", "CITY")
        target_count = req.get("target_count", 15)
        radius = req.get("radius", 50)
        prio_filters = req.get("priority_filters", ["P1", "P2", "P3"])

        p1_count = 0
        p2_count = 0
        p3_count = 0
        qualified_count = 0
        failed_count = 0
        excluded_count = 0

        try:
            # Stage 1: Discovery with Shariah & Scope Filtering
            self._update_run_status(run_id, "DISCOVERING")
            self._log_event(run_id, "DISCOVERING", f"Scanning Google Maps for {category} in {location}, {country} (Scope: {radius} KM)...")
            
            candidates = self.discovery.discover_candidates(
                category=category,
                location=location,
                country=country,
                scope=scope,
                radius_km=radius,
                target_count=target_count
            )
            self._log_event(run_id, "DISCOVERING", f"Discovered {len(candidates)} verified Shariah-compliant business candidates.")

            # Stage 2 to 7 for each candidate
            self._update_run_status(run_id, "VERIFYING")
            
            for cand in candidates:
                try:
                    verified_lead, evidence_list = self.verification.verify_candidate(cand)

                    priority, readiness, missing_info = self.classification.classify_lead(verified_lead)
                    verified_lead["priority"] = priority
                    verified_lead["build_readiness"] = readiness
                    verified_lead["missing_info"] = missing_info

                    if priority == "EXCLUDED" or (prio_filters and priority not in prio_filters):
                        excluded_count += 1
                        self._log_event(run_id, "CLASSIFYING", f"Excluded: {verified_lead['business_name']} ({priority})")
                        continue

                    intel = self.intelligence.enrich_lead(verified_lead)
                    verified_lead["offerings"] = intel.get("offerings", [])
                    verified_lead["visual_signals"] = intel.get("visual_signals", {})

                    plan = self.planning.generate_plan(verified_lead, intel)
                    package = self.packaging.create_package(verified_lead, plan, evidence_list, intel)

                    lead_id = self._save_lead_record(run_id, verified_lead, plan, package, evidence_list, intel.get("assets", []))
                    
                    if priority == "P1":
                        p1_count += 1
                    elif priority == "P2":
                        p2_count += 1
                    elif priority == "P3":
                        p3_count += 1
                    qualified_count += 1

                    self._log_event(run_id, "PACKAGING", f"Generated {priority} Halal Opportunity Pack for: {verified_lead['business_name']}")

                except Exception as lead_err:
                    failed_count += 1
                    self._log_event(run_id, "ERROR", f"Failed processing candidate {cand.get('business_name')}: {str(lead_err)}", level="ERROR")

            self._update_run_status(
                run_id, "COMPLETED",
                lead_count=len(candidates), qualified_count=qualified_count,
                p1_count=p1_count, p2_count=p2_count, p3_count=p3_count,
                failed_count=failed_count, excluded_count=excluded_count
            )
            self._log_event(run_id, "COMPLETED", f"Run completed successfully: {qualified_count} qualified leads packaged.")

        except Exception as e:
            self._update_run_status(run_id, "FAILED", errors=str(e))
            self._log_event(run_id, "FAILED", f"Critical run failure: {str(e)}", level="CRITICAL")

    def _save_lead_record(self, run_id: str, lead: Dict[str, Any], plan: Dict[str, Any], package: Dict[str, Any], evidence_list: List[Dict[str, Any]], assets: List[Dict[str, Any]]) -> str:
        conn = get_connection()
        cursor = conn.cursor()
        now_str = datetime.now().isoformat()
        lead_id = lead["id"]

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
        return lead_id

    def _update_run_status(self, run_id: str, status: str, **kwargs):
        conn = get_connection()
        cursor = conn.cursor()
        updates = ["status = ?"]
        params = [status]

        if status == "COMPLETED" or status == "FAILED":
            updates.append("completed_at = ?")
            params.append(datetime.now().isoformat())

        for k, v in kwargs.items():
            updates.append(f"{k} = ?")
            params.append(v)

        params.append(run_id)
        sql = f"UPDATE runs SET {', '.join(updates)} WHERE run_id = ?"
        cursor.execute(sql, params)
        conn.commit()
        conn.close()

    def _log_event(self, run_id: str, stage: str, message: str, level: str = "INFO"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO run_events (run_id, stage, message, level, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """, (run_id, stage, message, level, datetime.now().isoformat()))
        conn.commit()
        conn.close()
