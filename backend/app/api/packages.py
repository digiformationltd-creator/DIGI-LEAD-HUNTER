"""
Digiformation LTD — Lead Hunter
Packages & ZIP Download API
"""
import os
from pathlib import Path
from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from database import get_connection
from models import PackageResponse

router = APIRouter(prefix="/api/packages", tags=["Packages"])

@router.get("", response_model=List[PackageResponse])
def list_packages(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM packages ORDER BY created_at DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    packages = []
    for r in rows:
        packages.append(PackageResponse(
            id=r["id"],
            lead_id=r["lead_id"],
            business_name=r["business_name"],
            priority=r["priority"],
            version=r["version"],
            zip_filename=r["zip_filename"],
            zip_size_bytes=r["zip_size_bytes"],
            download_url=f"/api/packages/{r['id']}/download",
            is_valid=bool(r["is_valid"]),
            created_at=r["created_at"]
        ))
    conn.close()
    return packages

@router.get("/{pkg_id}/download")
def download_package(pkg_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packages WHERE id = ?", (pkg_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Package not found")

    zip_path = Path(row["zip_path"])
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="ZIP archive file missing on server")

    return FileResponse(
        path=str(zip_path),
        filename=row["zip_filename"],
        media_type="application/zip"
    )

@router.get("/lead/{lead_id}/download")
def download_lead_package(lead_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM packages WHERE lead_id = ?", (lead_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Package not found for this lead")

    zip_path = Path(row["zip_path"])
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="ZIP archive file missing on server")

    return FileResponse(
        path=str(zip_path),
        filename=row["zip_filename"],
        media_type="application/zip"
    )
