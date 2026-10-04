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
    "maps.google.com", "yell.com", "trustpilot.com"
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
            elif res.status_code in (202, 429, 403):
                return [], f"RATE_LIMITED_{res.status_code}"
            return [], f"HTTP_{res.status_code}"
        except httpx.TimeoutException:
            return [], "TIMEOUT"
        except Exception as e:
            return [], f"ERR_{str(e)[:30]}"

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
                        d = self._extract_domain(a_tag["href"])
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

        # Token-match check: ensure candidate domain has some similarity to business name
        name_tokens = set(re.findall(r'[a-zA-Z0-9]{3,}', clean_name.lower()))
        matched_standalone = []
        for dom in standalone_domains:
            dom_tokens = set(re.findall(r'[a-zA-Z0-9]{3,}', dom.lower()))
            if name_tokens.intersection(dom_tokens):
                matched_standalone.append(dom)
            elif any(token in dom.lower() for token in name_tokens):
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

        # 3. If at least 2 search engines successfully returned zero matching domains:
        if successful_engines >= 2 and len(matched_standalone) == 0:
            return {
                "status": "NO_WEBSITE",
                "discovered_domains": [],
                "top_candidate_domain": None,
                "engine_diagnostics": diagnostics,
                "successful_engines_count": successful_engines,
                "notes": f"Multi-search consensus confirmed across {successful_engines} search engines (0 standalone domains found)."
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
