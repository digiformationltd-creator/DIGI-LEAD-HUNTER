"""
REAL WhatsApp existence check — the only honest way to know a number is on WhatsApp.

libphonenumber (phone_validation_service) can only tell MOBILE vs LANDLINE. A
mobile number may still have NO WhatsApp account, which is exactly why the tool
produced fake "WhatsApp" leads. The only reliable confirmation is to ask WhatsApp
itself whether the number is registered — which requires a logged-in WhatsApp
session (Baileys `sock.onWhatsApp(jid)` returns {exists: true/false}).

This module keeps that check PLUGGABLE so the Python pipeline stays simple:

  * Set env `WHATSAPP_CHECK_URL` to a small WhatsApp-check service (a Baileys
    microservice is provided under tools/whatsapp_check_service). The service
    exposes GET {URL}?number=<E164> -> {"number": "...", "exists": true|false}.
  * With it configured, each number is REALLY verified: exists=true -> genuine
    WhatsApp lead; exists=false -> dropped as "no WhatsApp".
  * Without it (URL unset or unreachable), this returns exists=None (UNKNOWN),
    and the pipeline must NOT claim the number has WhatsApp — it stays an
    unverified mobile. No fake confirmations, ever.

No paid API. The owner scans the QR once for the Baileys service; after that
every lead run is checked against the live WhatsApp network.
"""
from __future__ import annotations

import os
from typing import Optional, Dict, Any

import httpx

_CACHE: Dict[str, Optional[bool]] = {}


def whatsapp_check_configured() -> bool:
    return bool((os.environ.get("WHATSAPP_CHECK_URL") or "").strip())


def check_whatsapp(e164_number: str, timeout: float = 15.0) -> Dict[str, Any]:
    """Return {"exists": True|False|None, "method": str}.

    True  = the number is registered on WhatsApp (verified against the network).
    False = the number is NOT on WhatsApp (drop it — it is a fake WhatsApp lead).
    None  = could not check (no service configured / unreachable) -> treat as
            UNVERIFIED; never present it as a confirmed WhatsApp number.
    """
    num = "".join(ch for ch in (e164_number or "") if ch.isdigit())
    if not num:
        return {"exists": None, "method": "no-number"}
    if num in _CACHE:
        return {"exists": _CACHE[num], "method": "cache"}

    url = (os.environ.get("WHATSAPP_CHECK_URL") or "").strip()
    if not url:
        return {"exists": None, "method": "not-configured"}

    try:
        r = httpx.get(url, params={"number": num}, timeout=timeout)
        if r.status_code != 200:
            return {"exists": None, "method": f"http-{r.status_code}"}
        data = r.json()
        exists = data.get("exists")
        exists = bool(exists) if exists is not None else None
        _CACHE[num] = exists
        return {"exists": exists, "method": "baileys-onWhatsApp"}
    except Exception as e:
        return {"exists": None, "method": f"error:{type(e).__name__}"}
