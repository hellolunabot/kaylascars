import json
import urllib.request
import re
import math
import ssl

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    a = math.sin(dLat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dLon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# 95051 coordinates (approx)
zip_lat = 37.3615
zip_lon = -121.9839

# Known 25+ MPG cars keywords
mpg_keywords = ["prius", "corolla", "civic", "mazda3", "mazda 3", "elantra", "jetta", "golf", "passat", "camry", "accord", "sentra", "altima", "focus", "fiesta", "cruze", "malibu", "soul", "optima", "forte", "leaf", "bolt", "volt", "spark", "yaris", "fit", "versa", "mirage", "rio", "impreza", "legacy"]

url = "https://sfbay.craigslist.org/search/sby/cta?max_auto_miles=80000&max_price=20000&postal=95051&search_distance=50"

# Allow unverified HTTPS contexts
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')

# Use regex to find the JSON-LD script
pattern = re.compile(r'<script type="application/ld\+json" id="ld_searchpage_results"[^>]*>(.*?)</script>', re.DOTALL)
match = pattern.search(html)

if match:
    data_str = match.group(1).strip()
    data = json.loads(data_str)
    items = data.get('itemListElement', [])
    
    cars = []
    
    for item in items:
        prod = item.get('item', {})
        name = prod.get('name', '').lower()
        
        # Check if it's a car model with good MPG
        has_good_mpg = any(kw in name for kw in mpg_keywords)
        
        # Some are just ads ("we buy cars")
        if "buy" in name or "sell" in name or "cash" in name:
            continue
            
        offers = prod.get('offers', {})
        price_str = offers.get('price', '0')
        try:
            price = float(price_str)
        except:
            price = 0
            
        if price > 20000 or price < 1000:
            continue
            
        if has_good_mpg:
            image = prod.get('image', [])
            photo_url = image[0] if isinstance(image, list) and len(image) > 0 else image
            
            geo = offers.get('availableAtOrFrom', {}).get('geo', {})
            lat = geo.get('latitude')
            lon = geo.get('longitude')
            distance = round(haversine(zip_lat, zip_lon, lat, lon), 1) if lat and lon else 0
            
            address = offers.get('availableAtOrFrom', {}).get('address', {})
            city = address.get('addressLocality', 'Unknown City')
            
            # Simple URL extraction if possible from HTML, else fallback to search URL
            item_url = url
            # Look for <a href="([^"]+)">Name</a>
            url_pattern = re.compile(r'<a href="([^"]+)"[^>]*>' + re.escape(prod.get('name', '')) + r'</a>')
            url_match = url_pattern.search(html)
            if url_match:
                item_url = url_match.group(1)
            else:
                # Alternatively look for the item using generic listing URL pattern in Craigslist
                pass
            
            car_data = {
                "name": prod.get('name'),
                "price": price,
                "photo_url": photo_url,
                "url": item_url,
                "location": {
                    "city": city,
                    "distance_miles_from_95051": distance,
                    "dealer_name": "Private Seller / Independent"
                },
                "estimated_mpg": "25+",
                "mileage": "<= 80,000"
            }
            cars.append(car_data)
            
            if len(cars) >= 10:
                break
                
    with open('/Users/mwhuss/Workspace/Personal/used-cars/used_cars.json', 'w') as f:
        json.dump(cars, f, indent=2)
        
    print(f"Saved {len(cars)} cars to used_cars.json")
else:
    print("Could not find JSON-LD data")
