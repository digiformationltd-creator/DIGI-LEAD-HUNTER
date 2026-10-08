export interface Lead {
  id: string;
  run_id?: string;
  business_name: string;
  category: string;
  address?: string;
  location?: string;
  google_maps_url?: string;
  google_shop_url?: string;
  phone?: string;
  phone_normalized?: string;
  whatsapp_number?: string;
  whatsapp_status: string;
  whatsapp_confidence?: string;
  whatsapp_verified?: boolean;
  carrier_line_type?: string;
  website_url?: string;
  website_status: 'NO_WEBSITE' | 'OFFICIAL_WEBSITE' | 'OUTDATED_WEAK' | 'UNCLEAR';
  website_audit?: any;
  rating?: number;
  review_count?: number;
  business_hours?: string;
  description?: string;
  priority: 'P1' | 'P2' | 'EXCLUDED';
  build_readiness: number;
  missing_info?: string[];
  offerings?: string[];
  visual_signals?: any;
  user_notes?: string;
  is_used?: boolean;
  used_at?: string;
  usage_notes?: string;
  created_at: string;
  updated_at: string;
  has_package: boolean;
  evidence_count: number;
}

export interface RunEvent {
  stage: string;
  message: string;
  level: string;
  timestamp: string;
}

export interface RunDetail {
  run_id: string;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  status: string;
  category: string;
  location: string;
  radius: number;
  target_count: number;
  priority_filters: string[];
  research_depth: string;
  package_mode: string;
  lead_count: number;
  qualified_count: number;
  p1_count: number;
  p2_count: number;
  p3_count: number;
  failed_count: number;
  excluded_count: number;
  errors?: string;
  events: RunEvent[];
}

export interface PackageItem {
  id: string;
  lead_id: string;
  business_name: string;
  priority: string;
  version: string;
  zip_filename: string;
  zip_size_bytes: number;
  download_url: string;
  is_valid: boolean;
  created_at: string;
}

export interface AnalyticsData {
  total_leads: number;
  p1_count: number;
  p2_count: number;
  p3_count: number;
  active_runs: number;
  completed_runs: number;
  ready_packages: number;
  whatsapp_verified_count: number;
  no_website_count: number;
  used_leads_count?: number;
  recent_runs: any[];
}
