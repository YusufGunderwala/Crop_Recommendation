import json
import urllib.request
import urllib.parse
import os
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed

CACHE_FILE = "models/district_coords_cache.json"

DISTRICT_ALIASES = {
    "AHMADABAD": "Ahmedabad",
    "BARODA": "Vadodara",
    "BANAS KANTHA": "Palanpur",
    "SABAR KANTHA": "Himatnagar",
    "PANCH MAHALS": "Godhra",
    "KUTCH": "Bhuj",
    "KACHCHH": "Bhuj",
    "DANG": "Ahwa",
    "DANGS": "Ahwa",
    "TAPI": "Vyara",
    "GULBARGA": "Kalaburagi",
    "BELGAUM": "Belagavi",
    "BELLARY": "Ballari",
    "BIJAPUR": "Vijayapura",
    "MYSORE": "Mysuru",
    "TUMKUR": "Tumakuru",
    "SHIMOGA": "Shivamogga",
    "CHIKMAGALUR": "Chikkamagaluru",
    "CALICUT": "Kozhikode",
    "COCHIN": "Kochi",
    "TRIVANDRUM": "Thiruvananthapuram",
    "CANNANORE": "Kannur",
    "PALGHAT": "Palakkad",
    "QUILON": "Kollam",
    "ALLEPPEY": "Alappuzha",
    "PONDICHERRY": "Puducherry",
    "BOMBAY": "Mumbai",
    "MADRAS": "Chennai",
    "CALCUTTA": "Kolkata",
    "FIROZPUR": "Ferozepur",
    "GURGAON": "Gurugram",
    "MEWAT": "Nuh",
    "ALLAHABAD": "Prayagraj",
    "FAIZABAD": "Ayodhya",
    "MIDNAPORE": "Medinipur",
    "NICOBARS": "Car Nicobar",
    "NORTH AND MIDDLE ANDAMAN": "Mayabunder",
    "SOUTH ANDAMANS": "Port Blair",
    "KANPUR NAGAR": "Kanpur",
    "KANPUR DEHAT": "Akbarpur",
    "KHERI": "Lakhimpur",
    "JYOTIBA PHOOLE NAGAR": "Amroha",
    "MAHAMAYA NAGAR": "Hathras",
    "KASHI RAM NAGAR": "Kasganj",
    "SANT KABIR NAGAR": "Khalilabad",
    "SANT RAVIDAS NAGAR": "Bhadohi",
    "SIDDHARTH NAGAR": "Navgarh",
    "SHRAVASTI": "Bhinga",
    "BAMETARA": "Bemetara",
    "BALOD": "Balod",
    "GARIABAND": "Gariaband",
    "KONDAGAON": "Kondagaon",
    "SUKMA": "Sukma",
    "SURAJPUR": "Surajpur",
    "BALRAMPUR": "Balrampur",
    "MUNGELI": "Mungeli"
}

def clean_ascii(text):
    if not text:
        return ""
    return unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('utf-8').strip()

def fetch_coords(dist, state):
    search_name = DISTRICT_ALIASES.get(dist.upper().strip(), dist.strip())
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(search_name)}&count=10&language=en&format=json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AgriCropPrecision/1.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = [r for r in data.get("results", []) if r.get("country_code") == "IN"]
            state_l = state.lower().strip()
            matched = [r for r in results if state_l in r.get("admin1", "").lower() or r.get("admin1", "").lower() in state_l]
            res = matched[0] if matched else (results[0] if results else None)
            if res:
                return {
                    "lat": round(float(res["latitude"]), 5),
                    "lon": round(float(res["longitude"]), 5),
                    "city": clean_ascii(res.get("name", dist)),
                    "state": clean_ascii(res.get("admin1", state)),
                    "location_name": clean_ascii(f"{res.get('name', dist)}, {res.get('admin1', state)}")
                }
    except Exception:
        pass
    return None

def main():
    with open("models/district_crop_intelligence.json", "r", encoding="utf-8") as f:
        intel = json.load(f)

    d_by_s = intel.get("districts_by_state", {})

    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    to_fetch = []
    for state, dists in d_by_s.items():
        for dist in dists:
            key = f"{dist.lower().strip()}::{state.lower().strip()}"
            if key not in cache:
                to_fetch.append((dist, state, key))

    print(f"Remaining districts to geocode: {len(to_fetch)} (Already cached: {len(cache)})")

    batch_size = 50
    for i in range(0, len(to_fetch), batch_size):
        batch = to_fetch[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1} / {(len(to_fetch) + batch_size - 1)//batch_size}...")
        
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_to_item = {executor.submit(fetch_coords, dist, state): (dist, state, key) for dist, state, key in batch}
            for future in as_completed(future_to_item):
                dist, state, key = future_to_item[future]
                try:
                    res = future.result()
                    if res:
                        cache[key] = res
                except Exception:
                    pass
        
        # Save after every batch
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
        
        time.sleep(0.5)

    print(f"Completed! Total districts cached: {len(cache)}")

if __name__ == "__main__":
    main()
