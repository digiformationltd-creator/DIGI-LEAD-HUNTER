# Discovery Agent (Phase 01)
## Purpose
Scans Google Maps, OpenStreetMap Overpass API, and public local business listings to discover prospective businesses within a specified category and geographic radius.

## Inputs
- Category (e.g., Restaurants, Salons, Dentists, Auto Workshops)
- Location (e.g., Lahore, London, New York)
- Radius in KM (default 10)
- Target lead count (default 15)

## Outputs
- List of raw Candidate objects:
  - business_name, category, address, location, coordinates
  - google_maps_url, phone, website_url, rating, review_count, business_hours, description

## Operational Directives
- Never invent missing facts.
- Do not assume phone is WhatsApp.
- Preserve source attribution and discovery timestamp.
