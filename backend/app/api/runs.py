"""
DIGIFORMATION LTD — Lead Hunter
Runs API Endpoints
"""
import json
from typing import List
from fastapi import APIRouter, HTTPException
from database import get_connection
from models import RunCreateRequest, RunDetailResponse, RunEventItem
from services.orchestrator import Orchestrator

router = APIRouter(prefix="/api/runs", tags=["Runs"])
orchestrator = Orchestrator()

@router.post("", response_model=dict)
def create_run(req: RunCreateRequest):
    run_id = orchestrator.start_run(req.dict())
    return {
        "status": "QUEUED",
        "run_id": run_id,
        "message": f"Lead Hunter search initiated for {req.category} in {req.location}."
    }

@router.get("", response_model=List[dict])
def list_runs(limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM runs ORDER BY created_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    runs = []
    for r in rows:
        item = dict(r)
        if item.get("priority_filters"):
            try:
                item["priority_filters"] = json.loads(item["priority_filters"])
            except Exception:
                pass
        runs.append(item)
    conn.close()
    return runs

@router.get("/{run_id}", response_model=RunDetailResponse)
def get_run(run_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Run not found")

    cursor.execute("SELECT * FROM run_events WHERE run_id = ? ORDER BY id ASC", (run_id,))
    event_rows = cursor.fetchall()
    events = [RunEventItem(
        stage=e["stage"],
        message=e["message"],
        level=e["level"],
        timestamp=e["timestamp"]
    ) for e in event_rows]

    conn.close()

    r = dict(row)
    p_filters = ["P1", "P2", "P3"]
    if r.get("priority_filters"):
        try:
            p_filters = json.loads(r["priority_filters"])
        except Exception:
            pass

    return RunDetailResponse(
        run_id=r["run_id"],
        created_at=r["created_at"],
        started_at=r["started_at"],
        completed_at=r["completed_at"],
        status=r["status"],
        category=r["category"],
        location=r["location"],
        radius=r["radius"],
        target_count=r["target_count"],
        priority_filters=p_filters,
        research_depth=r["research_depth"],
        package_mode=r["package_mode"],
        lead_count=r["lead_count"],
        qualified_count=r["qualified_count"],
        p1_count=r["p1_count"],
        p2_count=r["p2_count"],
        p3_count=r["p3_count"],
        failed_count=r["failed_count"],
        excluded_count=r["excluded_count"],
        errors=r["errors"],
        events=events
    )
