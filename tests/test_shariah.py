import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "backend" / "app"))

from services.discovery_service import DiscoveryService

def test_shariah_compliance_prohibited_categories():
    srv = DiscoveryService()

    # Haram / Non-compliant businesses MUST return False
    assert srv.is_shariah_compliant("Lucky Star Casino", "Casino") is False
    assert srv.is_shariah_compliant("The Crown Pub & Bar", "Pub") is False
    assert srv.is_shariah_compliant("City Sports Betting", "Betting Shop") is False
    assert srv.is_shariah_compliant("Quick Cash Payday Loans", "Moneylender") is False
    assert srv.is_shariah_compliant("Royal Wine & Beer Shop", "Liquor Store") is False

    # Halal / Ethical businesses MUST return True
    assert srv.is_shariah_compliant("Madina Restaurant", "Halal Dining") is True
    assert srv.is_shariah_compliant("Al-Falah Dental Clinic", "Dentist") is True
    assert srv.is_shariah_compliant("Royal Furniture Studio", "Furniture") is True
    assert srv.is_shariah_compliant("Apex Auto Workshop", "Car Repair") is True
    assert srv.is_shariah_compliant("Elegance Boutique", "Clothing") is True
