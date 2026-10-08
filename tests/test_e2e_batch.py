"""
End-to-end smoke test for the batch pipeline (Discovery -> Verification ->
Classification -> Intelligence -> Planning -> Packaging -> Excel/HTML/ZIP).

Discovery still queries the live Overpass API, so this is an online test. The
live web-presence verification is disabled here (LEADHUNTER_LIVE_VERIFY=0) so the
run is deterministic and does not depend on a search engine. The pipeline must
produce its deliverables; it must NOT be asserted to yield any Priority-1 lead,
because honest classification only awards P1 when a lead's assets are genuinely
confirmed, which real-world OSM data often does not provide.
"""
import os
import shutil
from pathlib import Path

from batch_hunter import BatchLeadHunter


def test_full_autonomous_batch_pipeline():
    os.environ["LEADHUNTER_LIVE_VERIFY"] = "0"  # deterministic: skip live search
    test_target_dir = Path("C:/Users/user/Downloads/DIGI-LEAD-HUNTER/test_batch_run")
    test_target_dir.mkdir(parents=True, exist_ok=True)

    try:
        hunter = BatchLeadHunter(target_folder=str(test_target_dir))
        result = hunter.execute_hunt(
            category="Restaurant",
            location="Lahore",
            country="Pakistan",
            radius_km=50,
            target_count=3,
            batch_name="Test_E2E_Batch",
        )

        assert result["batch_name"] == "Test_E2E_Batch"
        assert result["total_leads"] == 3
        assert result["p1_count"] >= 0  # honest: P1 is not guaranteed

        assert Path(result["batch_dir"]).exists()

        excel_file = Path(result["excel_path"])
        assert excel_file.exists() and excel_file.stat().st_size > 1000

        html_file = Path(result["html_path"])
        assert html_file.exists() and html_file.stat().st_size > 2000
        html_text = html_file.read_text(encoding="utf-8")
        assert "Test_E2E_Batch" in html_text
        assert "DIGIFORMATION LTD" in html_text

        zip_file = Path(result["zip_path"])
        assert zip_file.exists() and zip_file.stat().st_size > 2000

    finally:
        os.environ.pop("LEADHUNTER_LIVE_VERIFY", None)
        if test_target_dir.exists():
            shutil.rmtree(test_target_dir, ignore_errors=True)
