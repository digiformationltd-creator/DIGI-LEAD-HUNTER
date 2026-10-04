import httpx
import json
import urllib.parse

lat, lon = 31.5204, 74.3587
delta = 0.055
bbox = f"{lat - delta},{lon - delta},{lat + delta},{lon + delta}"
query = f"""
[out:json][timeout:25];
(
  node["amenity"="restaurant"]({bbox});
  node["amenity"="fast_food"]({bbox});
  node["amenity"="cafe"]({bbox});
  way["amenity"="restaurant"]({bbox});
  way["amenity"="fast_food"]({bbox});
);
out center 400;
"""

headers = {"User-Agent": "Antigravity/1.0"}
try:
    r = httpx.post("https://overpass-api.de/api/interpreter", data={"data": query}, headers=headers, timeout=25.0)
    print("status:", r.status_code)
    if r.status_code == 200:
        elems = r.json().get("elements", [])
        print("Total elements in 5KM Lahore radius:", len(elems))
        named = [e for e in elems if e.get("tags", {}).get("name") or e.get("tags", {}).get("name:en")]
        print("Named places:", len(named))
        for e in named[:15]:
            t = e.get("tags", {})
            name = t.get("name:en") or t.get("name")
            phone = t.get("phone") or t.get("contact:phone") or t.get("contact:whatsapp")
            print("-", name, "| Phone:", phone, "| Street:", t.get("addr:street"))
except Exception as ex:
    print("Error:", ex)
