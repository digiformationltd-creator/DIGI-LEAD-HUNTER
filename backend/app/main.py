"""
DIGIFORMATION LTD — Lead Hunter
FastAPI Application Entry Point
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import (
    COMPANY_NAME, PRODUCT_NAME, VERSION, AUTHOR,
    SUPPORT_WHATSAPP, EMAIL_PRIMARY, EMAIL_SECONDARY,
    WEBSITE_PRIMARY, WEBSITE_SECONDARY, LINKTREE_URL,
    PACKAGES_DIR
)
from database import init_db
from api.leads import router as leads_router
from api.runs import router as runs_router
from api.packages import router as packages_router
from api.analytics import router as analytics_router

# Initialize SQLite database schema
init_db()

app = FastAPI(
    title=PRODUCT_NAME,
    description="Local Business Lead Intelligence, Website Opportunity Research & Packaging Platform by DIGIFORMATION LTD.",
    version=VERSION
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(leads_router)
app.include_router(runs_router)
app.include_router(packages_router)
app.include_router(analytics_router)

# Mount packages static folder
if PACKAGES_DIR.exists():
    app.mount("/download_files", StaticFiles(directory=str(PACKAGES_DIR)), name="download_files")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": PRODUCT_NAME,
        "company": COMPANY_NAME,
        "version": VERSION
    }

@app.get("/api/info")
def company_info():
    return {
        "company": COMPANY_NAME,
        "product": PRODUCT_NAME,
        "version": VERSION,
        "support_whatsapp": SUPPORT_WHATSAPP,
        "support_whatsapp_clean": "923164467464",
        "email_primary": EMAIL_PRIMARY,
        "email_secondary": EMAIL_SECONDARY,
        "website_primary": WEBSITE_PRIMARY,
        "website_secondary": WEBSITE_SECONDARY,
        "linktree": LINKTREE_URL,
        "branding_immutable": True,
        "license": "DIGIFORMATION LTD Source-Available (Personal & Internal Use) License"
    }

# If production frontend build exists, serve it
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
