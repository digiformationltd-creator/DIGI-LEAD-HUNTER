"""
DIGIFORMATION LTD — Lead Hunter Fusion Engine
Telephony & WhatsApp Carrier Verification Engine
Powered by Google libphonenumber (phonenumbers package)
"""
import re
from typing import Dict, Any, Tuple
import phonenumbers
from phonenumbers import number_type, PhoneNumberType, geocoder, carrier

class PhoneValidationService:
    def __init__(self, default_region: str = "PK"):
        self.default_region = default_region

    def validate_and_classify_phone(self, raw_phone: str, country_code: str = "PK") -> Dict[str, Any]:
        """
        Parses, validates, formats, and detects line carrier type (Mobile vs Landline).
        Enforces strict WhatsApp compatibility rules:
        - MOBILE numbers can support WhatsApp.
        - FIXED_LINE numbers cannot support standard WhatsApp messaging.
        """
        if not raw_phone or not raw_phone.strip():
            return {
                "raw_phone": raw_phone or "",
                "is_valid": False,
                "e164": "",
                "national_format": "",
                "line_type": "UNKNOWN",
                "is_mobile": False,
                "whatsapp_status": "PHONE_UNVERIFIED",
                "whatsapp_number": "",
                "carrier_name": "",
                "region_description": ""
            }

        # Check for explicit WhatsApp click-to-chat link
        has_click_to_chat = bool(re.search(r"(?:wa\.me\/|api\.whatsapp\.com\/send\?phone=)\+?(\d{7,15})", raw_phone))

        clean_text = raw_phone.strip()
        region = country_code.upper() if country_code else self.default_region

        try:
            parsed = phonenumbers.parse(clean_text, region)
            is_valid = phonenumbers.is_valid_number(parsed)

            if not is_valid:
                return {
                    "raw_phone": raw_phone,
                    "is_valid": False,
                    "e164": "",
                    "national_format": raw_phone,
                    "line_type": "INVALID_NUMBER",
                    "is_mobile": False,
                    "whatsapp_status": "PHONE_UNVERIFIED",
                    "whatsapp_number": "",
                    "carrier_name": "",
                    "region_description": ""
                }

            e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            ntype = number_type(parsed)

            # Determine line carrier type
            line_type_str = "OTHER"
            is_mobile = False

            if ntype in (PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE):
                line_type_str = "MOBILE"
                is_mobile = True
            elif ntype == PhoneNumberType.FIXED_LINE:
                line_type_str = "FIXED_LINE"
                is_mobile = False
            elif ntype == PhoneNumberType.TOLL_FREE:
                line_type_str = "TOLL_FREE"
                is_mobile = False
            elif ntype == PhoneNumberType.VOIP:
                line_type_str = "VOIP"
                is_mobile = False

            carrier_str = carrier.name_for_number(parsed, "en") or ""
            geo_desc = geocoder.description_for_number(parsed, "en") or ""

            # WhatsApp Status determination
            digits_only = re.sub(r"\D", "", e164)
            if has_click_to_chat:
                wa_status = "WHATSAPP_CONFIRMED"
                wa_number = digits_only
            elif is_mobile:
                wa_status = "MOBILE_CARRIER_VALID"
                wa_number = digits_only
            elif line_type_str == "FIXED_LINE":
                wa_status = "LANDLINE_ONLY"
                wa_number = ""
            else:
                wa_status = "PHONE_ONLY"
                wa_number = ""

            return {
                "raw_phone": raw_phone,
                "is_valid": True,
                "e164": e164,
                "national_format": national,
                "line_type": line_type_str,
                "is_mobile": is_mobile,
                "whatsapp_status": wa_status,
                "whatsapp_number": wa_number,
                "carrier_name": carrier_str,
                "region_description": geo_desc
            }

        except phonenumbers.NumberParseException:
            return {
                "raw_phone": raw_phone,
                "is_valid": False,
                "e164": "",
                "national_format": raw_phone,
                "line_type": "PARSE_ERROR",
                "is_mobile": False,
                "whatsapp_status": "PHONE_UNVERIFIED",
                "whatsapp_number": "",
                "carrier_name": "",
                "region_description": ""
            }
