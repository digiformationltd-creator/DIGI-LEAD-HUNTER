import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.discovery_service import DiscoveryService

def test_deduplication():
    srv = DiscoveryService()
    items = [
        {"business_name": "Royal Cafe", "category": "Cafe"},
        {"business_name": "royal cafe", "category": "Cafe"},
        {"business_name": "Unique Hotel", "category": "Hotel"}
    ]
    deduped = srv._deduplicate(items)
    assert len(deduped) == 2
    assert deduped[0]["business_name"] == "Royal Cafe"

def test_category_tag_mapping():
    srv = DiscoveryService()
    assert srv._category_to_osm_tag("Italian Restaurant") == 'amenity="restaurant"'
    assert srv._category_to_osm_tag("Hair Salon") == 'shop="hairdresser"'
    assert srv._category_to_osm_tag("Dental Clinic") == 'amenity="dentist"'
