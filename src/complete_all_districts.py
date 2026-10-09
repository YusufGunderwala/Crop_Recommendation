import json

KNOWN_COORDS = {
    # Andhra Pradesh
    "east godavari::andhra pradesh": {"lat": 16.9891, "lon": 82.2475, "city": "Kakinada", "state": "Andhra Pradesh"},
    "prakasam::andhra pradesh": {"lat": 15.5057, "lon": 80.0499, "city": "Ongole", "state": "Andhra Pradesh"},
    "spsr nellore::andhra pradesh": {"lat": 14.4426, "lon": 79.9865, "city": "Nellore", "state": "Andhra Pradesh"},
    "visakhapatanam::andhra pradesh": {"lat": 17.6868, "lon": 83.2185, "city": "Visakhapatnam", "state": "Andhra Pradesh"},
    # Arunachal Pradesh
    "anjaw::arunachal pradesh": {"lat": 28.0264, "lon": 96.5392, "city": "Hawai", "state": "Arunachal Pradesh"},
    "dibang valley::arunachal pradesh": {"lat": 28.8078, "lon": 95.8427, "city": "Anini", "state": "Arunachal Pradesh"},
    "east kameng::arunachal pradesh": {"lat": 27.3167, "lon": 93.0333, "city": "Seppa", "state": "Arunachal Pradesh"},
    "east siang::arunachal pradesh": {"lat": 28.0667, "lon": 95.3333, "city": "Pasighat", "state": "Arunachal Pradesh"},
    "kurung kumey::arunachal pradesh": {"lat": 27.9000, "lon": 93.4500, "city": "Koloriang", "state": "Arunachal Pradesh"},
    "lower dibang valley::arunachal pradesh": {"lat": 28.1400, "lon": 95.8300, "city": "Roing", "state": "Arunachal Pradesh"},
    "lower subansiri::arunachal pradesh": {"lat": 27.5300, "lon": 93.8300, "city": "Ziro", "state": "Arunachal Pradesh"},
    "papum pare::arunachal pradesh": {"lat": 27.1000, "lon": 93.6200, "city": "Yupia", "state": "Arunachal Pradesh"},
    "tawang::arunachal pradesh": {"lat": 27.5861, "lon": 91.8647, "city": "Tawang", "state": "Arunachal Pradesh"},
    "upper siang::arunachal pradesh": {"lat": 28.6167, "lon": 94.9500, "city": "Yingkiong", "state": "Arunachal Pradesh"},
    "upper subansiri::arunachal pradesh": {"lat": 27.9800, "lon": 94.2200, "city": "Daporijo", "state": "Arunachal Pradesh"},
    "west kameng::arunachal pradesh": {"lat": 27.2600, "lon": 92.4200, "city": "Bomdila", "state": "Arunachal Pradesh"},
    "west siang::arunachal pradesh": {"lat": 28.1700, "lon": 94.7300, "city": "Aalo", "state": "Arunachal Pradesh"},
    # Assam
    "cachar::assam": {"lat": 24.8333, "lon": 92.7789, "city": "Silchar", "state": "Assam"},
    "dima hasao::assam": {"lat": 25.1833, "lon": 93.0167, "city": "Haflong", "state": "Assam"},
    "kamrup::assam": {"lat": 26.3167, "lon": 91.6000, "city": "Amingaon", "state": "Assam"},
    "kamrup metro::assam": {"lat": 26.1445, "lon": 91.7362, "city": "Guwahati", "state": "Assam"},
    "karbi anglong::assam": {"lat": 25.8456, "lon": 93.4358, "city": "Diphu", "state": "Assam"},
    "marigaon::assam": {"lat": 26.2500, "lon": 92.3500, "city": "Morigaon", "state": "Assam"},
    # Bihar
    "kaimur (bhabua)::bihar": {"lat": 25.0400, "lon": 83.6100, "city": "Bhabua", "state": "Bihar"},
    "lakhisarai::bihar": {"lat": 25.1764, "lon": 86.0944, "city": "Lakhisarai", "state": "Bihar"},
    "nalanda::bihar": {"lat": 25.1979, "lon": 85.5186, "city": "Bihar Sharif", "state": "Bihar"},
    "pashchim champaran::bihar": {"lat": 26.8000, "lon": 84.5000, "city": "Bettiah", "state": "Bihar"},
    "purbi champaran::bihar": {"lat": 26.6500, "lon": 84.9167, "city": "Motihari", "state": "Bihar"},
    "sheohar::bihar": {"lat": 26.5178, "lon": 85.2936, "city": "Sheohar", "state": "Bihar"},
    # Chhattisgarh
    "dantewada::chhattisgarh": {"lat": 18.9000, "lon": 81.3500, "city": "Dantewada", "state": "Chhattisgarh"},
    "gariyaband::chhattisgarh": {"lat": 20.9600, "lon": 82.0600, "city": "Gariaband", "state": "Chhattisgarh"},
    "janjgir-champa::chhattisgarh": {"lat": 22.0167, "lon": 82.5667, "city": "Janjgir", "state": "Chhattisgarh"},
    "kabirdham::chhattisgarh": {"lat": 22.0167, "lon": 81.2500, "city": "Kawardha", "state": "Chhattisgarh"},
    "rajnandgaon::chhattisgarh": {"lat": 21.1000, "lon": 81.0333, "city": "Rajnandgaon", "state": "Chhattisgarh"},
    # Goa
    "north goa::goa": {"lat": 15.4989, "lon": 73.8278, "city": "Panaji", "state": "Goa"},
    "south goa::goa": {"lat": 15.2832, "lon": 73.9862, "city": "Margao", "state": "Goa"},
    # Himachal Pradesh
    "lahul and spiti::himachal pradesh": {"lat": 32.5714, "lon": 77.0347, "city": "Keylong", "state": "Himachal Pradesh"},
    # Jammu and Kashmir
    "bandipora::jammu and kashmir": {"lat": 34.4225, "lon": 74.6465, "city": "Bandipora", "state": "Jammu and Kashmir"},
    "baramulla::jammu and kashmir": {"lat": 34.2090, "lon": 74.3436, "city": "Baramulla", "state": "Jammu and Kashmir"},
    "leh ladakh::jammu and kashmir": {"lat": 34.1526, "lon": 77.5771, "city": "Leh", "state": "Jammu and Kashmir"},
    "rajauri::jammu and kashmir": {"lat": 33.3767, "lon": 74.3090, "city": "Rajouri", "state": "Jammu and Kashmir"},
    # Jharkhand
    "east singhbhum::jharkhand": {"lat": 22.8046, "lon": 86.2029, "city": "Jamshedpur", "state": "Jharkhand"},
    "koderma::jharkhand": {"lat": 24.4674, "lon": 85.5939, "city": "Koderma", "state": "Jharkhand"},
    "saraikela kharsawan::jharkhand": {"lat": 22.7000, "lon": 85.9300, "city": "Seraikela", "state": "Jharkhand"},
    "west singhbhum::jharkhand": {"lat": 22.5500, "lon": 85.8000, "city": "Chaibasa", "state": "Jharkhand"},
    # Karnataka
    "bangalore rural::karnataka": {"lat": 13.2929, "lon": 77.5385, "city": "Doddaballapur", "state": "Karnataka"},
    "bengaluru urban::karnataka": {"lat": 12.9716, "lon": 77.5946, "city": "Bengaluru", "state": "Karnataka"},
    "chikballapur::karnataka": {"lat": 13.4355, "lon": 77.7275, "city": "Chikkaballapur", "state": "Karnataka"},
    "dakshin kannad::karnataka": {"lat": 12.9141, "lon": 74.8560, "city": "Mangaluru", "state": "Karnataka"},
    "uttar kannad::karnataka": {"lat": 14.8153, "lon": 74.1305, "city": "Karwar", "state": "Karnataka"},
    # Kerala
    "wayanad::kerala": {"lat": 11.6080, "lon": 76.0820, "city": "Kalpetta", "state": "Kerala"},
    # Madhya Pradesh
    "agar malwa::madhya pradesh": {"lat": 23.7144, "lon": 76.0152, "city": "Agar", "state": "Madhya Pradesh"},
    "hoshangabad::madhya pradesh": {"lat": 22.7533, "lon": 77.7249, "city": "Narmadapuram", "state": "Madhya Pradesh"},
    # Maharashtra
    "buldhana::maharashtra": {"lat": 20.5312, "lon": 76.1843, "city": "Buldhana", "state": "Maharashtra"},
    "raigad::maharashtra": {"lat": 18.6414, "lon": 72.8722, "city": "Alibag", "state": "Maharashtra"},
    # Manipur
    "imphal east::manipur": {"lat": 24.8200, "lon": 93.9500, "city": "Porompat", "state": "Manipur"},
    "imphal west::manipur": {"lat": 24.8170, "lon": 93.9368, "city": "Lamphelpat", "state": "Manipur"},
    # Meghalaya
    "east garo hills::meghalaya": {"lat": 25.5900, "lon": 90.5800, "city": "Williamnagar", "state": "Meghalaya"},
    "east jaintia hills::meghalaya": {"lat": 25.3300, "lon": 92.3700, "city": "Khliehriat", "state": "Meghalaya"},
    "east khasi hills::meghalaya": {"lat": 25.5788, "lon": 91.8933, "city": "Shillong", "state": "Meghalaya"},
    "north garo hills::meghalaya": {"lat": 25.9000, "lon": 90.5800, "city": "Resubelpara", "state": "Meghalaya"},
    "ri bhoi::meghalaya": {"lat": 25.9000, "lon": 91.8800, "city": "Nongpoh", "state": "Meghalaya"},
    "south garo hills::meghalaya": {"lat": 25.3000, "lon": 90.6300, "city": "Baghmara", "state": "Meghalaya"},
    "south west garo hills::meghalaya": {"lat": 25.5000, "lon": 89.9200, "city": "Ampati", "state": "Meghalaya"},
    "south west khasi hills::meghalaya": {"lat": 25.4300, "lon": 91.2200, "city": "Mawkyrwat", "state": "Meghalaya"},
    "west garo hills::meghalaya": {"lat": 25.5167, "lon": 90.2167, "city": "Tura", "state": "Meghalaya"},
    "west jaintia hills::meghalaya": {"lat": 25.4500, "lon": 92.2000, "city": "Jowai", "state": "Meghalaya"},
    "west khasi hills::meghalaya": {"lat": 25.5200, "lon": 91.2600, "city": "Nongstoin", "state": "Meghalaya"},
    # Mizoram
    "champhai::mizoram": {"lat": 23.4561, "lon": 93.3283, "city": "Champhai", "state": "Mizoram"},
    # Odisha
    "anugul::odisha": {"lat": 20.8400, "lon": 85.1000, "city": "Angul", "state": "Odisha"},
    "boudh::odisha": {"lat": 20.8400, "lon": 84.3200, "city": "Boudh", "state": "Odisha"},
    "kandhamal::odisha": {"lat": 20.2400, "lon": 84.0400, "city": "Phulbani", "state": "Odisha"},
    # Punjab
    "fatehgarh sahib::punjab": {"lat": 30.6436, "lon": 76.3888, "city": "Sirhind", "state": "Punjab"},
    "firozepur::punjab": {"lat": 30.9237, "lon": 74.6138, "city": "Firozpur", "state": "Punjab"},
    "s.a.s nagar::punjab": {"lat": 30.7046, "lon": 76.7179, "city": "Mohali", "state": "Punjab"},
    # Rajasthan
    "jalore::rajasthan": {"lat": 25.3458, "lon": 72.6151, "city": "Jalore", "state": "Rajasthan"},
    # Sikkim
    "east district::sikkim": {"lat": 27.3314, "lon": 88.6138, "city": "Gangtok", "state": "Sikkim"},
    "north district::sikkim": {"lat": 27.5000, "lon": 88.5500, "city": "Mangan", "state": "Sikkim"},
    "south district::sikkim": {"lat": 27.1700, "lon": 88.3500, "city": "Namchi", "state": "Sikkim"},
    "west district::sikkim": {"lat": 27.3000, "lon": 88.2500, "city": "Geyzing", "state": "Sikkim"},
    # Tamil Nadu
    "thanjavur::tamil nadu": {"lat": 10.7870, "lon": 79.1378, "city": "Thanjavur", "state": "Tamil Nadu"},
    "the nilgiris::tamil nadu": {"lat": 11.4102, "lon": 76.6950, "city": "Udhagamandalam", "state": "Tamil Nadu"},
    "thiruvallur::tamil nadu": {"lat": 13.1439, "lon": 79.9083, "city": "Tiruvallur", "state": "Tamil Nadu"},
    "virudhunagar::tamil nadu": {"lat": 9.5872, "lon": 77.9579, "city": "Virudhunagar", "state": "Tamil Nadu"},
    # Tripura
    "gomati::tripura": {"lat": 23.5300, "lon": 91.4900, "city": "Udaipur", "state": "Tripura"},
    "north tripura::tripura": {"lat": 24.3200, "lon": 92.1700, "city": "Dharmanagar", "state": "Tripura"},
    "sepahijala::tripura": {"lat": 23.6300, "lon": 91.3200, "city": "Bishramganj", "state": "Tripura"},
    "south tripura::tripura": {"lat": 23.1700, "lon": 91.4900, "city": "Belonia", "state": "Tripura"},
    "unakoti::tripura": {"lat": 24.2300, "lon": 92.0200, "city": "Kailashahar", "state": "Tripura"},
    "west tripura::tripura": {"lat": 23.8315, "lon": 91.2868, "city": "Agartala", "state": "Tripura"},
    # Uttar Pradesh
    "ambedkar nagar::uttar pradesh": {"lat": 26.4326, "lon": 82.5434, "city": "Akbarpur", "state": "Uttar Pradesh"},
    "gautam buddha nagar::uttar pradesh": {"lat": 28.5355, "lon": 77.3910, "city": "Noida", "state": "Uttar Pradesh"},
    "kaushambi::uttar pradesh": {"lat": 25.5340, "lon": 81.3761, "city": "Manjhanpur", "state": "Uttar Pradesh"},
    "kushi nagar::uttar pradesh": {"lat": 26.9010, "lon": 83.9813, "city": "Padrauna", "state": "Uttar Pradesh"},
    "sant kabeer nagar::uttar pradesh": {"lat": 26.7800, "lon": 83.0500, "city": "Khalilabad", "state": "Uttar Pradesh"},
    # Uttarakhand
    "pauri garhwal::uttarakhand": {"lat": 30.1500, "lon": 78.7800, "city": "Pauri", "state": "Uttarakhand"},
    "rudra prayag::uttarakhand": {"lat": 30.2800, "lon": 78.9800, "city": "Rudraprayag", "state": "Uttarakhand"},
    "tehri garhwal::uttarakhand": {"lat": 30.3800, "lon": 78.4800, "city": "New Tehri", "state": "Uttarakhand"},
    "udam singh nagar::uttarakhand": {"lat": 28.9800, "lon": 79.4000, "city": "Rudrapur", "state": "Uttarakhand"},
    "uttar kashi::uttarakhand": {"lat": 30.7300, "lon": 78.4500, "city": "Uttarkashi", "state": "Uttarakhand"},
    # West Bengal
    "24 paraganas north::west bengal": {"lat": 22.7214, "lon": 88.4817, "city": "Barasat", "state": "West Bengal"},
    "24 paraganas south::west bengal": {"lat": 22.5366, "lon": 88.3308, "city": "Alipore", "state": "West Bengal"},
    "birbhum::west bengal": {"lat": 23.8400, "lon": 87.6100, "city": "Suri", "state": "West Bengal"},
    "coochbehar::west bengal": {"lat": 26.3239, "lon": 89.4510, "city": "Cooch Behar", "state": "West Bengal"},
    "dinajpur dakshin::west bengal": {"lat": 25.2200, "lon": 88.7600, "city": "Balurghat", "state": "West Bengal"},
    "dinajpur uttar::west bengal": {"lat": 25.6200, "lon": 88.1200, "city": "Raiganj", "state": "West Bengal"},
    "maldah::west bengal": {"lat": 25.0000, "lon": 88.1400, "city": "English Bazar", "state": "West Bengal"},
    "purulia::west bengal": {"lat": 23.3300, "lon": 86.3600, "city": "Purulia", "state": "West Bengal"}
}

def main():
    cache_path = "models/district_coords_cache.json"
    with open(cache_path, "r", encoding="utf-8") as f:
        cache = json.load(f)

    for k, v in KNOWN_COORDS.items():
        v["location_name"] = f"{v['city']}, {v['state']}"
        cache[k] = v

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)

    with open("models/district_crop_intelligence.json", "r", encoding="utf-8") as f:
        intel = json.load(f)

    missing = []
    for s, dists in intel.get("districts_by_state", {}).items():
        for d in dists:
            key = f"{d.lower().strip()}::{s.lower().strip()}"
            if key not in cache:
                missing.append((d, s))

    print(f"Total districts in cache: {len(cache)}")
    print(f"Districts remaining missing: {len(missing)}")
    if missing:
        print("Missing:", missing[:10])

if __name__ == "__main__":
    main()
