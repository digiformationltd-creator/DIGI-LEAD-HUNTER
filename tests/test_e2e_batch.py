"""
Automated End-to-End Test Suite for Phase 1 to 7 Batch Pipeline
Tests Discovery, Verification, Classification, Intelligence, Planning, Packaging, and Master Excel/HTML/ZIP generation.
"""
import pytest
from pathlib import Path
import os
import shutil

from batch_hunter import BatchLeadHunter

def test_full_autonomous_batch_pipeline():
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
            batch_name="Test_E2E_Batch"
        )

        assert result["batch_name"] == "Test_E2E_Batch"
        assert result["total_leads"] == 3
        assert result["p1_count"] >= 1

        batch_path = Path(result["batch_dir"])
        assert batch_path.exists()

        # 1. Master Excel Sheet
        excel_file = Path(result["excel_path"])
        assert excel_file.exists()
        assert excel_file.stat().st_size > 1000

        # 2. Master HTML Opportunity Portal
        html_file = Path(result["html_path"])
        assert html_file.exists()
        assert html_file.stat().st_size > 2000
        html_text = html_file.read_text(encoding="utf-8")
        assert "Test_E2E_Batch" in html_text
        assert "Digiformation LTD" in html_text

        # 3. Master Standalone ZIP
        zip_file = Path(result["zip_path"])
        assert zip_file.exists()
        assert zip_file.stat().st_size > 2000

        # 4. Priority-1 Directory
        p1_dir = batch_path / "priority_1_opportunities"
        assert p1_dir.exists()
        p1_folders = list(p1_dir.glob("P1_*"))
        assert len(p1_folders) >= 1

        first_p1 = p1_folders[0]
        assert (first_p1 / "WEBSITE_PLAN.md").exists()
        assert (first_p1 / "PRODUCTS_AND_PACKAGES.json").exists()
        assert (first_p1 / "assets_and_visuals" / "proposed_logo.svg").exists()
        assert (first_p1 / "assets_and_visuals" / "product_showcase_banner.svg").exists()

    finally:
        if test_target_dir.exists():
            shutil.rmtree(test_target_dir, ignore_errors=True)
