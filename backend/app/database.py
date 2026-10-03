"""
Digi Formation Limited — Lead Hunter
SQLite Database Initialization & Connection
"""
import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from config import DATABASE_PATH

def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Runs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        run_id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        started_at TEXT,
        completed_at TEXT,
        status TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        radius INTEGER DEFAULT 10,
        target_count INTEGER DEFAULT 15,
        priority_filters TEXT,
        research_depth TEXT DEFAULT 'Standard',
        package_mode TEXT DEFAULT 'Full Package',
        lead_count INTEGER DEFAULT 0,
        qualified_count INTEGER DEFAULT 0,
        p1_count INTEGER DEFAULT 0,
        p2_count INTEGER DEFAULT 0,
        p3_count INTEGER DEFAULT 0,
        failed_count INTEGER DEFAULT 0,
        excluded_count INTEGER DEFAULT 0,
        errors TEXT
    )
    """)

    # 2. Leads Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id TEXT PRIMARY KEY,
        run_id TEXT,
        business_name TEXT NOT NULL,
        category TEXT NOT NULL,
        address TEXT,
        location TEXT,
        google_maps_url TEXT,
        phone TEXT,
        phone_normalized TEXT,
        whatsapp_number TEXT,
        whatsapp_status TEXT, -- WHATSAPP_VERIFIED, WHATSAPP_POSSIBLE, PHONE_ONLY, UNKNOWN
        website_url TEXT,
        website_status TEXT, -- NO_WEBSITE, OFFICIAL_WEBSITE, OUTDATED_WEAK, UNCLEAR
        website_audit TEXT, -- JSON
        rating REAL,
        review_count INTEGER,
        business_hours TEXT,
        description TEXT,
        priority TEXT, -- P1, P2, P3, EXCLUDED
        build_readiness INTEGER DEFAULT 0, -- 0-100%
        missing_info TEXT, -- JSON list
        offerings TEXT, -- JSON list of services/menu
        visual_signals TEXT, -- JSON
        user_notes TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (run_id) REFERENCES runs (run_id)
    )
    """)

    # 3. Lead Evidence Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lead_evidence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id TEXT NOT NULL,
        claim TEXT NOT NULL,
        value TEXT,
        evidence_level TEXT NOT NULL, -- E1_DIRECT, E2_STRONG, E3_INFERRED, E4_UNCERTAIN
        source TEXT,
        source_url TEXT,
        observed_at TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (lead_id) REFERENCES leads (id)
    )
    """)

    # 4. Assets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        id TEXT PRIMARY KEY,
        lead_id TEXT NOT NULL,
        asset_type TEXT NOT NULL, -- LOGO, PHOTO, MENU, PRICING, MAP
        source_url TEXT,
        local_path TEXT,
        usability_status TEXT,
        rights_notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (lead_id) REFERENCES leads (id)
    )
    """)

    # 5. Website Plans Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS website_plans (
        id TEXT PRIMARY KEY,
        lead_id TEXT NOT NULL UNIQUE,
        plan_type TEXT NOT NULL, -- P1_BUILD_READY, P2_CONSULTATION, P3_REDESIGN
        target_audience TEXT,
        objectives TEXT, -- JSON list
        cta_strategy TEXT,
        whatsapp_strategy TEXT,
        info_architecture TEXT, -- JSON
        hero_plan TEXT, -- JSON
        sections_plan TEXT, -- JSON
        visual_direction TEXT, -- JSON
        seo_plan TEXT, -- JSON
        markdown_content TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (lead_id) REFERENCES leads (id)
    )
    """)

    # 6. Packages Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS packages (
        id TEXT PRIMARY KEY,
        lead_id TEXT NOT NULL UNIQUE,
        business_name TEXT NOT NULL,
        priority TEXT NOT NULL,
        version TEXT DEFAULT '1.0',
        zip_filename TEXT NOT NULL,
        zip_path TEXT NOT NULL,
        zip_size_bytes INTEGER DEFAULT 0,
        is_valid INTEGER DEFAULT 1,
        created_at TEXT NOT NULL,
        FOREIGN KEY (lead_id) REFERENCES leads (id)
    )
    """)

    # 7. Run Events / Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS run_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL,
        stage TEXT NOT NULL,
        message TEXT NOT NULL,
        level TEXT DEFAULT 'INFO',
        timestamp TEXT NOT NULL,
        FOREIGN KEY (run_id) REFERENCES runs (run_id)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DATABASE_PATH)
