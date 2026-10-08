"""
Live web-presence verification — the step that stops FAKE leads.

The rest of the pipeline discovers businesses from OpenStreetMap (Overpass). OSM
only rarely carries a `website` tag and never proves a phone has WhatsApp, so a
pipeline that trusts the OSM record alone produces two kinds of fake lead:

  * "No website" leads for businesses that DO have a website (it just was not
    recorded in OSM), and
  * "WhatsApp" leads for numbers that have no WhatsApp account.

This module adds the missing active check. Given a business name + city it runs
a real web search (Bing HTML — the one engine that answers reliably from a
server; DuckDuckGo/Mojeek/Brave return a CAPTCHA/empty page) and:

  1. Looks for an OFFICIAL website (excluding social networks, food aggregators
     and directories) → if found, the business is NOT a no-website lead.
  2. Collects any WhatsApp channel the business ADVERTISES online (wa.me /
     api.whatsapp.com links on the SERP and on the official page) → that is a
     genuine confirmation signal, far stronger than matching a phone's shape.

Nothing here claims more than it checked. A confirmed website/WhatsApp is backed
by a real URL; the absence of one is reported as "searched, none found", not as
proof. No paid API and no login — httpx + BeautifulSoup only.
"""
from __future__ import annotations

import base64
import binascii
import re
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, quote_plus, urlparse

import httpx
from bs4 import BeautifulSoup


def _resolve_bing_url(href: str) -> str:
    """Bing wraps every organic result in a click-tracking redirect
    (https://www.bing.com/ck/a?...&u=a1<base64url>). The real destination is the
    base64url payload after the leading "a1". Without decoding it, every result
    host looks like "bing.com" and the search is useless — which is exactly why
    the first version of this verifier found nothing. Non-Bing hrefs pass through
    unchanged."""
    if "bing.com/ck/a" not in href:
        return href
    try:
        u = parse_qs(urlparse(href).query).get("u", [""])[0]
        if u.startswith("a1"):
            u = u[2:]
        pad = "=" * (-len(u) % 4)
        return base64.urlsafe_b64decode(u + pad).decode("utf-8", "replace")
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return href

_UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-GB,en;q=0.9",
}

# Hosts that are NEVER an "official business website" — social profiles, food
# aggregators, map/review directories and link shorteners. A hit on one of these
# does not count as the business having its own site.
_NOT_OFFICIAL = (
    "facebook.", "fb.com", "instagram.", "tiktok.", "twitter.", "x.com",
    "linkedin.", "youtube.", "youtu.be", "pinterest.", "snapchat.",
    "wa.me", "whatsapp.com", "t.me", "telegram.",
    "foodpanda.", "foodpanda.pk", "deliveroo.", "ubereats.", "zomato.",
    "tripadvisor.", "yelp.", "google.", "bing.", "maps.",
    "daraz.", "olx.", "locanto.", "justdial.", "cybo.", "yellowpages",
    "businesslist.", "worldplaces.", "findlocal", "nearfinderpk", "pk.locanto",
    "wikipedia.", "wikimapia.", "foursquare.", "booking.", "agoda.",
    "linktr.ee", "bit.ly", "goo.gl", "rb.gy", "surl.",
)

_WA_RE = re.compile(
    r"(?:wa\.me/|api\.whatsapp\.com/send/?\?phone=|whatsapp://send\?phone=|chat\.whatsapp\.com/)\+?(\d{8,15})",
    re.I,
)


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s or "")


def _name_tokens(name: str) -> List[str]:
    # Significant words from the business name, used to decide whether a search
    # result really belongs to this business (not a random article).
    stop = {"the", "and", "fast", "food", "cafe", "restaurant", "pvt", "ltd",
            "co", "the", "lahore", "karachi", "islamabad", "pakistan"}
    toks = re.findall(r"[a-z0-9]+", (name or "").lower())
    return [t for t in toks if len(t) >= 4 and t not in stop]


def _bing(query: str, timeout: float = 20.0, retries: int = 3) -> Tuple[List[Dict[str, str]], str, bool]:
    """One Bing HTML search. Returns (organic results, raw html, ok).

    `ok` is True only when Bing actually served a real results page (status 200
    with the organic-results container present). That lets the caller tell
    "searched, found nothing" apart from "search was blocked / rate-limited" —
    the difference between an honest NO_WEBSITE and an UNVERIFIED one. Bing
    throttles bursts, so a blocked attempt is retried with a short backoff."""
    import time
    url = "https://www.bing.com/search?setlang=en&cc=GB&q=" + quote_plus(query)
    last_html = ""
    for attempt in range(1, retries + 1):
        try:
            r = httpx.get(url, headers=_UA, timeout=timeout, follow_redirects=True)
        except Exception:
            time.sleep(1.5 * attempt)
            continue
        last_html = r.text or ""
        served = r.status_code == 200 and ("b_algo" in last_html or 'id="b_results"' in last_html)
        if not served:
            time.sleep(1.5 * attempt)  # throttled / interstitial → back off and retry
            continue
        soup = BeautifulSoup(last_html, "html.parser")
        out: List[Dict[str, str]] = []
        seen: set[str] = set()
        for li in soup.select("li.b_algo"):
            a = li.select_one("h2 a[href]")
            if not a:
                continue
            href = _resolve_bing_url(a.get("href") or "")
            if not href.startswith("http") or href in seen:
                continue
            seen.add(href)
            title = a.get_text(" ", strip=True)
            cap = li.select_one(".b_caption p") or li.select_one("p")
            snippet = cap.get_text(" ", strip=True) if cap else ""
            out.append({"url": href, "title": title, "snippet": snippet})
        # Fallback: Bing sometimes serves a layout where li.b_algo does not parse
        # cleanly (lite/JS variant). Pull the organic destinations straight from
        # the click-redirect links in the raw HTML so the search still works.
        if not out:
            for m in re.finditer(r'href="(https://www\.bing\.com/ck/a\?[^"]+)"', last_html):
                real = _resolve_bing_url(m.group(1).replace("&amp;", "&"))
                h = _host(real)
                if not real.startswith("http") or not h or "bing.com" in h or real in seen:
                    continue
                seen.add(real)
                out.append({"url": real, "title": "", "snippet": ""})
        return out, last_html, True
    return [], last_html, False


def _host(url: str) -> str:
    try:
        return (urlparse(url).hostname or "").lower().lstrip("www.")
    except Exception:
        return ""


def _is_official_candidate(url: str, title: str, tokens: List[str]) -> bool:
    host = _host(url)
    if not host or any(b in host for b in _NOT_OFFICIAL):
        return False
    hay = (host + " " + (title or "")).lower()
    # The result belongs to this business only if one of its distinctive name
    # tokens shows up in the domain or the page title. This keeps a random news
    # article or an unrelated site from being mistaken for "they have a website".
    return any(t in hay for t in tokens) if tokens else False


def research_presence(
    name: str,
    city: str = "",
    country: str = "",
    osm_phone: str = "",
    fetch_page: bool = True,
    timeout: float = 20.0,
) -> Dict[str, Any]:
    """
    Actively verify a business's web + WhatsApp presence.

    Returns a dict:
      website_found        : official site URL, or None if a real search found none
      website_candidates   : all non-social candidate URLs seen (for evidence)
      whatsapp_confirmed   : list of numbers the business advertises via wa.me
      whatsapp_match       : True if osm_phone matches a confirmed wa.me number
      sources              : URLs consulted (evidence trail)
      searched             : True if the web search actually ran
    """
    result: Dict[str, Any] = {
        "website_found": None,
        "website_candidates": [],
        "whatsapp_confirmed": [],
        "whatsapp_match": False,
        "sources": [],
        "searched": False,
    }
    if not name:
        return result

    tokens = _name_tokens(name)
    q = " ".join(p for p in [name, city, country] if p).strip()
    results, raw, ok = _bing(q, timeout=timeout)
    result["searched"] = ok  # True only if Bing actually served a results page
    result["sources"].append("https://www.bing.com/search?q=" + quote_plus(q))

    # --- WhatsApp advertised on the SERP itself ---
    # A SERP carries wa.me links for ADS and OTHER businesses too, so a number
    # scraped from the page at large proves nothing about THIS business. We only
    # trust a SERP-level wa.me when its digits match the candidate's own phone;
    # unrelated numbers are ignored. (The business's OWN page, fetched below, is
    # trusted in full.)
    osm_tail = _digits(osm_phone)[-9:]
    wa: set[str] = set()
    for m in _WA_RE.finditer(raw or ""):
        num = "+" + m.group(1)
        if osm_tail and osm_tail in _digits(num):
            wa.add(num)

    # --- Official website from organic results ---
    official: Optional[str] = None
    for res in results:
        if _is_official_candidate(res["url"], res["title"], tokens):
            result["website_candidates"].append(res["url"])
            if official is None:
                official = res["url"]

    # --- Fetch the official page (if any) and scan it for an advertised WhatsApp ---
    if official and fetch_page:
        try:
            pr = httpx.get(official, headers=_UA, timeout=timeout, follow_redirects=True)
            result["sources"].append(official)
            if pr.status_code == 200:
                for m in _WA_RE.finditer(pr.text):
                    wa.add("+" + m.group(1))
        except Exception:
            pass

    result["website_found"] = official
    result["whatsapp_confirmed"] = sorted(wa)

    if osm_phone and wa:
        d = _digits(osm_phone)[-9:]  # compare last 9 digits (ignore country-code form)
        result["whatsapp_match"] = any(d and d in _digits(n) for n in wa)

    return result
