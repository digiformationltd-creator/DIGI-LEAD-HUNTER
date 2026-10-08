import httpx

query = """
[out:json][timeout:25];
(
  node[shop=car_repair](31.3404,74.1787,31.7004,74.5387);
  way[shop=car_repair](31.3404,74.1787,31.7004,74.5387);
  node[shop=car](31.3404,74.1787,31.7004,74.5387);
  way[shop=car](31.3404,74.1787,31.7004,74.5387);
  node[shop=car_parts](31.3404,74.1787,31.7004,74.5387);
  way[shop=car_parts](31.3404,74.1787,31.7004,74.5387);
);
out center 300;
"""

headers = {
    "User-Agent": "DIGIFORMATION-LTD-LeadHunter/1.0 (info@digiformation.co.uk; info@digibizos.co.uk)"
}

r = httpx.post("https://overpass-api.de/api/interpreter", data={"data": query}, headers=headers, timeout=30.0)
print("Status:", r.status_code)
if r.status_code == 200:
    data = r.json()
    elements = data.get("elements", [])
    print("Found total OSM auto elements:", len(elements))
    phones = []
    for el in elements:
        tags = el.get("tags", {})
        p = tags.get("phone") or tags.get("contact:phone") or tags.get("contact:mobile") or tags.get("contact:whatsapp")
        if p:
            name = tags.get("name:en") or tags.get("name") or "Unnamed"
            phones.append((name, p, tags.get("shop")))
    print(f"Elements with phone: {len(phones)}")
    for name, p, s in phones:
        print(f"[{s}] {name} => {p}")
