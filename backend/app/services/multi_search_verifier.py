"""
DIGIFORMATION LTD — Lead Hunter Fusion Engine
Resilient Multi-Engine Search Verifier (DuckDuckGo + Bing + Mojeek)
Solves: DuckDuckGo HTTP 202 Anomaly / Rate Limit Silent Dropouts
Parity Reference: AGENTICSEEK/LANGHRAF server.ts:164-184 & entity-research.ts:123-145
"""
import re
import urllib.parse
from typing import Dict, Any, List, Tuple
import httpx
from bs4 import BeautifulSoup

SOCIAL_DOMAINS = {
    "facebook.com", "instagram.com", "tiktok.com", "wa.me", "whatsapp.com",
    "twitter.com", "x.com", "youtube.com", "linkedin.com", "pinterest.com",
    "threads.net"
}

DIRECTORY_DOMAINS = {
    "foodpanda.pk", "foodpanda.com", "tripadvisor.com", "restaurantguru.com",
    "kfoods.com", "wheree.com", "pakistanand.com", "bizsouthasia.com",
    "yellowpages.com.pk", "pakistanyp.com", "findpk.com", "justdial.com",
    "yelp.com", "foursquare.com", "wikipedia.org", "zomato.com",
    "swiggy.com", "google.com", "bing.com", "duckduckgo.com", "mojeek.com",
    "maps.google.com", "yell.com", "trustpilot.com", "oladoc.com", "marham.pk",
    "hamariweb.com", "urdupoint.com", "dha.gov.pk", "zameen.com", "graana.com",
    "ilmkiroshni.pk", "parho.com"
}

class MultiSearchVerifier:
    def __init__(self, timeout: float = 6.0):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-GB,en;q=0.9"
        }

    def _extract_domain(self, url: str) -> str:
        try:
            clean = re.sub(r"^https?://", "", url).split("/")[0].split("?")[0].strip().lower()
            return re.sub(r"^www\.", "", clean)
        except Exception:
            return ""

    def _search_ddg(self, client: httpx.Client, query: str) -> Tuple[List[str], str]:
        candidates = []
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        try:
            res = client.get(url, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for tag in soup.find_all("a", class_="result__url"):
                    raw = tag.get_text(strip=True)
                    d = self._extract_domain(raw)
                    if d and d not in candidates:
                        candidates.append(d)
                return candidates, "OK" if candidates else "EMPTY"
            # Resilient fallback to DDG Lite if HTML challenges or rate-limits
            lite_url = f"https://lite.duckduckgo.com/lite/?q={urllib.parse.quote(query)}"
            lite_res = client.get(lite_url, timeout=self.timeout)
            if lite_res.status_code == 200:
                soup = BeautifulSoup(lite_res.text, "html.parser")
                for tag in soup.find_all("a", class_="result-link", href=True):
                    raw_href = tag["href"]
                    m = re.search(r"uddg=([^&]+)", raw_href)
                    if m:
                        actual_url = urllib.parse.unquote(m.group(1))
                        d = self._extract_domain(actual_url)
                        if d and d not in candidates:
                            candidates.append(d)
                return candidates, "OK" if candidates else "EMPTY"
            return [], f"RATE_LIMITED_{res.status_code}"
        except httpx.TimeoutException:
            return [], "TIMEOUT"
        except Exception as e:
            return [], f"ERR_{str(e)[:30]}"

    @staticmethod
    def _resolve_bing_url(href: str) -> str:
        """Decode Bing's click-tracking redirect (ck/a?...&u=a1<base64url>) to the real destination."""
        if "bing.com/ck/a" not in href:
            return href
        try:
            import base64
            import binascii
            u = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("u", [""])[0]
            if u.startswith("a1"):
                u = u[2:]
            pad = "=" * (-len(u) % 4)
            return base64.urlsafe_b64decode(u + pad).decode("utf-8", "replace")
        except Exception:
            return href

    def _search_bing(self, client: httpx.Client, query: str) -> Tuple[List[str], str]:
        candidates = []
        url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=en-GB"
        try:
            res = client.get(url, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for li in soup.find_all("li", class_="b_algo"):
                    a_tag = li.find("a", href=True)
                    if a_tag and a_tag["href"].startswith("http"):
                        dest = self._resolve_bing_url(a_tag["href"])
                        d = self._extract_domain(dest)
                        if d and d not in candidates:
                            candidates.append(d)
                return candidates, "OK" if candidates else "EMPTY"
            return [], f"HTTP_{res.status_code}"
        except httpx.TimeoutException:
            return [], "TIMEOUT"
        except Exception as e:
            return [], f"ERR_{str(e)[:30]}"

    def _search_mojeek(self, client: httpx.Client, query: str) -> Tuple[List[str], str]:
        candidates = []
        url = f"https://www.mojeek.com/search?q={urllib.parse.quote(query)}"
        try:
            res = client.get(url, timeout=self.timeout)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a_tag in soup.find_all("a", class_="title", href=True):
                    href = a_tag["href"]
                    if href.startswith("http"):
                        d = self._extract_domain(href)
                        if d and d not in candidates:
                            candidates.append(d)
                return candidates, "OK" if candidates else "EMPTY"
            return [], f"HTTP_{res.status_code}"
        except httpx.TimeoutException:
            return [], "TIMEOUT"
        except Exception as e:
            return [], f"ERR_{str(e)[:30]}"

    def verify_candidate_presence(self, business_name: str, location: str) -> Dict[str, Any]:
        """
        Executes interleaved triple-engine search (DDG + Bing + Mojeek).
        Returns:
            {
                "status": "OFFICIAL_WEBSITE" | "NO_WEBSITE" | "WEBSITE_STATUS_UNCLEAR",
                "discovered_domains": List[str],
                "top_candidate_domain": Optional[str],
                "engine_diagnostics": Dict[str, str],
                "successful_engines_count": int,
                "notes": str
            }
        """
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', business_name).strip()
        query = f'"{clean_name}" {location} official website'

        diagnostics = {}
        all_candidates = []

        with httpx.Client(headers=self.headers, follow_redirects=True) as client:
            # 1. DuckDuckGo
            ddg_cands, ddg_st = self._search_ddg(client, query)
            diagnostics["duckduckgo"] = ddg_st
            all_candidates.extend(ddg_cands)

            # 2. Bing
            bing_cands, bing_st = self._search_bing(client, query)
            diagnostics["bing"] = bing_st
            all_candidates.extend(bing_cands)

            # 3. Mojeek
            moj_cands, moj_st = self._search_mojeek(client, query)
            diagnostics["mojeek"] = moj_st
            all_candidates.extend(moj_cands)

        # Count successful responses (HTTP 200)
        successful_engines = sum(1 for st in diagnostics.values() if st in ("OK", "EMPTY"))

        # Deduplicate candidates while preserving order
        unique_cands = []
        for d in all_candidates:
            if d not in unique_cands:
                unique_cands.append(d)

        # Filter out social profiles and generic directories
        standalone_domains = []
        for d in unique_cands:
            if any(soc in d for soc in SOCIAL_DOMAINS):
                continue
            if any(dir_dom in d for dir_dom in DIRECTORY_DOMAINS):
                continue
            standalone_domains.append(d)

        # Token-match check: ensure candidate domain matches DISTINCTIVE business brand tokens (not generic stopwords)
        INDUSTRY_STOP_WORDS = {
            "food", "foods", "point", "house", "restaurant", "restaurants", "cafe", "roast",
            "clinic", "clinics", "center", "centre", "medical", "hospital", "health",
            "dental", "care", "surgery", "studio", "dentist", "dentists", "land", "solutions",
            "boutique", "fashion", "fabrics", "hub", "wear", "clothes", "collection",
            "salon", "spa", "beauty", "parlour", "grooming", "barber",
            "auto", "autos", "workshop", "workshops", "repair", "service", "services", "mechanic", "electrician",
            "furniture", "interior", "interiors", "decor", "home", "showroom",
            "school", "schools", "academy", "academies", "college", "colleges", "group", "education",
            "gym", "gyms", "fitness", "club", "sports", "lounge",
            "estate", "estates", "realtors", "builders", "properties", "property", "advisor", "advisors",
            "official", "website", "online", "pakistan", "lahore", "punjab"
        }

        name_tokens = [t for t in re.findall(r'[a-zA-Z0-9]{3,}', clean_name.lower())]
        distinctive_tokens = [t for t in name_tokens if t not in INDUSTRY_STOP_WORDS and len(t) >= 4]

        matched_standalone = []
        for dom in standalone_domains:
            dom_clean = dom.lower()
            # Foreign TLDs (e.g. .in, .uk, .au) cannot be a local Pakistani single-location storefront
            if any(dom_clean.endswith(tld) or f"{tld}/" in dom_clean for tld in (".in", ".uk", ".au", ".ca", ".de", ".fr", ".ru")):
                continue

            if distinctive_tokens:
                # Require domain to contain at least one distinctive brand stem
                if any(t in dom_clean for t in distinctive_tokens):
                    matched_standalone.append(dom)
            elif len(name_tokens) >= 2:
                # If only common words, require consecutive tokens joined together
                joined_tokens = ["".join(name_tokens[i:i+2]) for i in range(len(name_tokens)-1)]
                if any(jt in dom_clean for jt in joined_tokens):
                    matched_standalone.append(dom)

        # DECISION LOGIC:
        # 1. If an official matching standalone domain is discovered:
        if matched_standalone:
            top_site = f"https://{matched_standalone[0]}"
            return {
                "status": "OFFICIAL_WEBSITE",
                "discovered_domains": matched_standalone,
                "top_candidate_domain": top_site,
                "engine_diagnostics": diagnostics,
                "successful_engines_count": successful_engines,
                "notes": f"Discovered official standalone domain via multi-search consensus: {top_site}."
            }

        # 2. If ZERO successful engines could be reached (e.g., all blocked, offline, or timed out):
        # RULE: NEVER CONVERT TIMEOUT / ANTI-BOT INTO NO_WEBSITE!
        if successful_engines == 0:
            return {
                "status": "WEBSITE_STATUS_UNCLEAR",
                "discovered_domains": [],
                "top_candidate_domain": None,
                "engine_diagnostics": diagnostics,
                "successful_engines_count": 0,
                "notes": f"All search engines timed out or encountered anti-bot barriers ({diagnostics}). Epistemic status: WEBSITE_STATUS_UNCLEAR."
            }

        # 3. If at least 1 search engine successfully returned zero matching domains:
        if successful_engines >= 1 and len(matched_standalone) == 0:
            return {
                "status": "NO_WEBSITE",
                "discovered_domains": [],
                "top_candidate_domain": None,
                "engine_diagnostics": diagnostics,
                "successful_engines_count": successful_engines,
                "notes": f"Multi-search consensus confirmed across {successful_engines} search engine(s) (0 standalone domains found)."
            }

        # 4. Inconclusive (e.g. only 1 engine answered and found 0):
        return {
            "status": "WEBSITE_STATUS_UNCLEAR",
            "discovered_domains": [],
            "top_candidate_domain": None,
            "engine_diagnostics": diagnostics,
            "successful_engines_count": successful_engines,
            "notes": f"Partial search signal ({successful_engines}/3 engines responded). Certified status remains UNCLEAR."
        }
