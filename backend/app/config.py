"""
Digiformation LTD — Lead Hunter
Application Configuration & Brand Constants
"""
import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = DATA_DIR / "database"
PACKAGES_DIR = DATA_DIR / "packages"
ASSETS_DIR = DATA_DIR / "assets"
LOGS_DIR = DATA_DIR / "logs"

for p in [DATABASE_DIR, PACKAGES_DIR, ASSETS_DIR, LOGS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "lead_hunter.db"

# Official Brand & Identity
COMPANY_NAME = "Digiformation LTD"
PRODUCT_NAME = "DIGI LEAD HUNTER"
SPONSORED_BY = "Digi Biz OS"
VERSION = "1.1.0"
AUTHOR = "Digiformation LTD"
COPYRIGHT = "© 2026 Digiformation LTD. All Rights Reserved."

# Official Contact Information
SUPPORT_WHATSAPP = "+92 316 4467464"
SUPPORT_WHATSAPP_CLEAN = "923164467464"
SUPPORT_WHATSAPP_URL = f"https://wa.me/{SUPPORT_WHATSAPP_CLEAN}?text=Hello%20Digi%20Formation%2C%20I%20am%20using%20Lead%20Hunter"
EMAIL_PRIMARY = "digiformation.info@digiformation.co.uk"
EMAIL_SECONDARY = "info@digibizwiz.co.uk"
WEBSITE_PRIMARY = "https://www.digiformation.co.uk/"
WEBSITE_SECONDARY = "https://www.digibizos.co.uk/"
LINKTREE_URL = "https://linktr.ee/digiformationltd"

# Server Settings
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "5173"))
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Shariah & Ethical Filter Directives
SHARIAH_COMPLIANCE_REQUIRED = True

PROHIBITED_KEYWORDS = [
    # Usury / Interest / Riba
    "interest", "riba", "payday loan", "moneylender", "pawnshop", "conventional bank",
    # Gambling / Betting
    "casino", "gambling", "betting", "bookmaker", "lottery", "slot machine", "poker",
    # Alcohol / Intoxicants
    "bar", "pub", "nightclub", "liquor", "wine", "beer", "brewery", "distillery", "cocktail", "alcohol",
    # Adult / Inappropriate
    "adult", "night club", "strip club", "escort", "massage parlour",
    # Haram foods
    "pork", "swine", "bacon only"
]

# Supported Radius Tiers (in KM)
RADIUS_TIERS = {
    "5": "5 KM (Hyper-Local)",
    "50": "50 KM (City-Wide)",
    "100": "100 KM (Regional / Metro)",
    "1000": "1,000 KM (State / Country-Wide)",
    "5000": "5,000 KM (Continental)",
    "0": "Worldwide / Global"
}
