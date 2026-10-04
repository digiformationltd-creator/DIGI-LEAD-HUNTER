"""
DIGIFORMATION LTD — Lead Hunter
Pydantic Models & Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class RunCreateRequest(BaseModel):
    category: str = Field(..., description="Business category (e.g. Restaurants, Clinics, Boutiques, Auto Workshops)")
    location: str = Field(..., description="Target City or Area")
    country: Optional[str] = Field("Pakistan", description="Country (e.g. Pakistan, United Kingdom, USA, UAE, Worldwide)")
    scope: Optional[str] = Field("CITY", description="CITY, COUNTRY, or WORLDWIDE")
    radius: int = Field(50, description="Radius in KM: 5, 50, 100, 1000, 5000, or 0 (Worldwide)")
    target_count: int = Field(15, description="Target lead count")
    priority_filters: List[str] = Field(default_factory=lambda: ["P1", "P2"])
    research_depth: str = Field("Standard", description="Standard or Deep")
    package_mode: str = Field("Full Package", description="Full Package, Evidence, or Website Plan")
    shariah_compliant_only: bool = Field(True, description="Strictly exclude interest, alcohol, gambling, and haram businesses")
    specific_business: Optional[str] = None

class LeadEvidenceItem(BaseModel):
    claim: str
    value: Optional[str] = None
    evidence_level: str
    source: str
    source_url: Optional[str] = None
    observed_at: str
    notes: Optional[str] = None

class LeadResponse(BaseModel):
    id: str
    run_id: Optional[str] = None
    business_name: str
    category: str
    address: Optional[str] = None
    location: Optional[str] = None
    google_maps_url: Optional[str] = None
    phone: Optional[str] = None
    phone_normalized: Optional[str] = None
    whatsapp_number: Optional[str] = None
    whatsapp_status: str
    website_url: Optional[str] = None
    website_status: str
    website_audit: Optional[Dict[str, Any]] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    business_hours: Optional[str] = None
    description: Optional[str] = None
    priority: str
    build_readiness: int
    missing_info: Optional[List[str]] = None
    offerings: Optional[List[str]] = None
    visual_signals: Optional[Dict[str, Any]] = None
    user_notes: Optional[str] = None
    created_at: str
    updated_at: str
    has_package: bool = False
    evidence_count: int = 0
    is_shariah_compliant: bool = True

class RunEventItem(BaseModel):
    stage: str
    message: str
    level: str
    timestamp: str

class RunDetailResponse(BaseModel):
    run_id: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    status: str
    category: str
    location: str
    country: Optional[str] = "Pakistan"
    scope: Optional[str] = "CITY"
    radius: int
    target_count: int
    priority_filters: List[str]
    research_depth: str
    package_mode: str
    lead_count: int
    qualified_count: int
    p1_count: int
    p2_count: int
    p3_count: int
    failed_count: int
    excluded_count: int
    errors: Optional[str] = None
    events: List[RunEventItem] = []

class PackageResponse(BaseModel):
    id: str
    lead_id: str
    business_name: str
    priority: str
    version: str
    zip_filename: str
    zip_size_bytes: int
    download_url: str
    is_valid: bool
    created_at: str

class AnalyticsResponse(BaseModel):
    total_leads: int
    p1_count: int
    p2_count: int
    p3_count: int
    active_runs: int
    completed_runs: int
    ready_packages: int
    whatsapp_verified_count: int
    no_website_count: int
    recent_runs: List[Dict[str, Any]]
