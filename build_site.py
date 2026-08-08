import json
import os
import re
import urllib.request
import urllib.parse

def extract_vehicle_image(url, timeout=10):
    """Fetch a car listing page and extract the main vehicle image URL."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Find img src attributes
        img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        
        # Filter for vehicle images
        vehicle_images = []
        for img in img_matches:
            img_lower = img.lower()
            if any(kw in img_lower for kw in ['dealer.com', 'vehicle', 'exterior', 'photo', 'pic', 'inventory', 'img_']):
                if 'w=410' not in img and 'garage.png' not in img:
                    vehicle_images.append(img)
        
        if vehicle_images:
            # Prefer dealer.com images
            for img in vehicle_images:
                if 'dealer.com' in img.lower():
                    return img
            return vehicle_images[0]
    except Exception as e:
        print(f"  Warning: Could not fetch {url}: {e}")
    return None

def ensure_photo_urls(cars):
    """Check each car for placeholder images and try to extract real ones."""
    for car in cars:
        photo_url = car.get('photo_url', '')
        if 'craigslist' in photo_url or 'placeholder' in photo_url or not photo_url:
            print(f"Extracting image for: {car['name']}")
            new_url = extract_vehicle_image(car.get('url', ''))
            if new_url:
                car['photo_url'] = new_url
                print(f"  Found: {new_url}")
            else:
                print(f"  No image found, keeping placeholder")

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kayla's Dopamine Rides! 🚗💥</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400..1000;1,9..40,400..1000&family=Outfit:wght@100..900&family=Unbounded:wght@200..900&family=Bangers&display=swap" rel="stylesheet">
    
    <!-- Tailwind CSS v4 via Browser -->
    <script src="https://unpkg.com/@tailwindcss/browser@4"></script>
    
    <style>
        :root {
            --bg: #0D0D1A;
            --fg: #FFFFFF;
            --muted: #2D1B4E;
            --c1: #FF3AF2; /* Magenta */
            --c2: #00F5D4; /* Cyan */
            --c3: #FFE600; /* Yellow */
            --c4: #FF6B35; /* Orange */
            --c5: #7B2FFF; /* Purple */
        }
        
        body {
            background-color: var(--bg);
            color: var(--fg);
            font-family: 'DM Sans', sans-serif;
            overflow-x: hidden;
            position: relative;
        }

        h1, h2, h3, h4, h5, h6, .display-font {
            font-family: 'Unbounded', sans-serif;
        }
        
        .bangers-font {
            font-family: 'Bangers', cursive;
        }
        
        /* Typography Shadows */
        .shadow-single-c5 { text-shadow: 2px 2px 0px var(--c5); }
        .shadow-double { text-shadow: 2px 2px 0px var(--c5), 4px 4px 0px var(--c1); }
        .shadow-triple { text-shadow: 2px 2px 0px var(--c5), 4px 4px 0px var(--c1), 6px 6px 0px var(--c2); }
        .shadow-mega { text-shadow: 4px 4px 0px var(--c5), 8px 8px 0px var(--c1), 12px 12px 0px var(--c2); }
        
        /* Gradients */
        .text-gradient {
            background: linear-gradient(90deg, var(--c1), var(--c2), var(--c3), var(--c1));
            background-size: 300% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-shift 4s ease infinite;
        }
        
        /* Patterns */
        .pattern-dots {
            background-image: radial-gradient(circle, var(--c1) 1.5px, transparent 1.5px);
            background-size: 30px 30px;
            opacity: 0.15;
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }
        
        .pattern-stripes {
            background-image: repeating-linear-gradient(
                45deg,
                transparent,
                transparent 15px,
                rgba(255, 230, 0, 0.08) 15px,
                rgba(255, 230, 0, 0.08) 30px
            );
            position: fixed;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }
        
        .pattern-checker {
            background-image: conic-gradient(
                from 90deg at 1px 1px,
                transparent 90deg,
                rgba(0, 245, 212, 0.08) 0
            );
            background-size: 50px 50px;
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }

        .pattern-mesh {
            background:
                radial-gradient(ellipse at 20% 30%, rgba(255,58,242,0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 70%, rgba(0,245,212,0.15) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(123,47,255,0.1) 0%, transparent 60%);
            position: absolute;
            inset: 0;
            z-index: 0;
            pointer-events: none;
        }

        /* Hard Box Shadows */
        .box-shadow-double-1 { box-shadow: 8px 8px 0 var(--c3), 16px 16px 0 var(--c1); }
        .box-shadow-double-2 { box-shadow: 8px 8px 0 var(--c4), 16px 16px 0 var(--c2); }
        .box-shadow-double-3 { box-shadow: 8px 8px 0 var(--c1), 16px 16px 0 var(--c5); }
        .box-shadow-double-4 { box-shadow: 8px 8px 0 var(--c2), 16px 16px 0 var(--c3); }
        .box-shadow-double-5 { box-shadow: 8px 8px 0 var(--c5), 16px 16px 0 var(--c4); }
        
        /* Glows */
        .glow-base { box-shadow: 0 0 20px rgba(255, 58, 242, 0.5), 0 0 40px rgba(0, 245, 212, 0.3); }
        
        /* Animations */
        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50%      { transform: translateY(-20px) rotate(5deg); }
        }
        .animate-float { animation: float 6s ease-in-out infinite; }
        
        @keyframes float-reverse {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50%      { transform: translateY(20px) rotate(-5deg); }
        }
        .animate-float-reverse { animation: float-reverse 5s ease-in-out infinite; }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(255, 58, 242, 0.5); }
            50%      { box-shadow: 0 0 40px rgba(255, 58, 242, 0.8), 0 0 60px rgba(0, 245, 212, 0.5); }
        }
        .animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
        
        @keyframes gradient-shift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        @keyframes spin-slow {
            from { transform: rotate(0deg); }
            to   { transform: rotate(360deg); }
        }
        .animate-spin-slow { animation: spin-slow 20s linear infinite; }
        
        @keyframes wiggle {
            0%, 100% { transform: rotate(-3deg); }
            50%      { transform: rotate(3deg); }
        }
        .animate-wiggle { animation: wiggle 1s ease-in-out infinite; }

        @keyframes bounce-subtle {
            0%, 100% { transform: translateY(0); }
            50%      { transform: translateY(-10px); }
        }
        .animate-bounce-subtle { animation: bounce-subtle 2s ease-in-out infinite; }

        /* Card Hover Effects */
        .max-card {
            transition: all 300ms ease-out;
        }
        .max-card:hover {
            transform: scale(1.02) rotate(2deg) translateY(-8px);
        }

        .max-button {
            transition: all 200ms ease-out;
        }
        .max-button:hover {
            transform: scale(1.1);
        }
        .max-button:active {
            transform: scale(0.95);
        }

        /* Utils for borders to make it easier inline */
        .border-c1 { border-color: var(--c1); }
        .border-c2 { border-color: var(--c2); }
        .border-c3 { border-color: var(--c3); }
        .border-c4 { border-color: var(--c4); }
        .border-c5 { border-color: var(--c5); }
        
        .bg-c1 { background-color: var(--c1); }
        .bg-c2 { background-color: var(--c2); }
        .bg-c3 { background-color: var(--c3); }
        .bg-c4 { background-color: var(--c4); }
        .bg-c5 { background-color: var(--c5); }
        
        .text-c1 { color: var(--c1); }
        .text-c2 { color: var(--c2); }
        .text-c3 { color: var(--c3); }
        .text-c4 { color: var(--c4); }
        .text-c5 { color: var(--c5); }

    </style>
</head>
<body class="antialiased min-h-screen">
    <!-- Global Patterns -->
    <div class="pattern-dots"></div>
    <div class="pattern-stripes"></div>

    <!-- Massive Background Typography -->
    <div class="fixed top-1/4 -left-20 text-[16rem] font-black opacity-10 text-[#FF3AF2] uppercase transform -rotate-12 pointer-events-none display-font leading-none z-0">
        VROOM
    </div>
    <div class="fixed bottom-0 -right-20 text-[20rem] font-black opacity-10 text-[#00F5D4] uppercase pointer-events-none display-font leading-none z-0">
        BEEP
    </div>

    <!-- Floating Shapes -->
    <div class="fixed top-[15%] left-[10%] text-6xl animate-wiggle z-30 pointer-events-none">✨</div>
    <div class="fixed top-[30%] right-[15%] text-7xl animate-float z-30 pointer-events-none">🚀</div>
    <div class="fixed bottom-[20%] left-[5%] text-5xl animate-bounce-subtle z-30 pointer-events-none">🔥</div>
    <div class="fixed top-[60%] right-[5%] text-6xl animate-float-reverse z-30 pointer-events-none">💰</div>

    <div class="relative z-10 container mx-auto px-6 py-24 md:py-32 max-w-7xl">
        
        <header class="text-center mb-24 relative">
            <div class="pattern-mesh"></div>
            <div class="inline-block relative">
                <h1 class="text-6xl md:text-8xl lg:text-9xl font-black uppercase tracking-tighter text-gradient shadow-mega mb-6 relative z-10 display-font rotate-1">
                    KAYLA'S RIDES
                </h1>
                <div class="absolute -top-10 -right-10 text-6xl animate-spin-slow">💫</div>
            </div>
            <p class="text-2xl md:text-4xl font-bold uppercase shadow-double max-w-4xl mx-auto tracking-widest text-[#FFE600] bangers-font mt-4">
                Reliable, Affordable, & Ready for the Road! 🛣️💨
            </p>
        </header>

        <!-- Dynamic Grid of Cars -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12 relative z-20">
            {car_cards}
        </div>
        
    </div>

</body>
</html>
"""

CAR_CARD_TEMPLATE = """
            <div class="max-card relative bg-[#2D1B4E]/80 backdrop-blur-sm border-4 {border_color} {border_style} rounded-3xl p-6 flex flex-col justify-between {shadow_class} {transform_class} {z_class}">
                <!-- Background pattern for card -->
                <div class="pattern-checker opacity-[0.03] rounded-2xl pointer-events-none"></div>
                
                <div class="relative z-10">
                    <div class="relative rounded-2xl overflow-hidden border-4 {img_border_color} mb-6 h-64 shadow-single-c5">
                        <img src="{photo_url}" alt="{name}" class="w-full h-full object-cover">
                        <div class="absolute top-4 right-4 bg-{accent_bg} text-[#0D0D1A] font-black px-4 py-2 rounded-full uppercase text-sm border-2 border-[#0D0D1A] animate-pulse-glow transform rotate-3">
                            {price_str}
                        </div>
                    </div>
                    
                    <h2 class="text-2xl font-black uppercase text-white shadow-double mb-4 leading-tight display-font">
                        {name}
                    </h2>
                    
                    <div class="space-y-3 mb-8 text-lg font-bold">
                        <div class="flex items-center gap-3 bg-[#0D0D1A]/50 p-3 rounded-xl border-2 border-dashed {border_color_2}">
                            <span class="text-2xl">📍</span>
                            <span class="text-white/90">{location} ({distance} mi)</span>
                        </div>
                        <div class="flex items-center gap-3 bg-[#0D0D1A]/50 p-3 rounded-xl border-2 border-solid {border_color_3}">
                            <span class="text-2xl">⛽</span>
                            <span class="text-white/90">{mpg} MPG</span>
                        </div>
                        <div class="flex items-center gap-3 bg-[#0D0D1A]/50 p-3 rounded-xl border-2 border-dotted {border_color_1}">
                            <span class="text-2xl">🛣️</span>
                            <span class="text-white/90">{mileage} Miles</span>
                        </div>
                    </div>
                </div>

                <a href="{url}" target="_blank" class="max-button w-full text-center bg-gradient-to-r from-[{grad_from}] via-[{grad_via}] to-[{grad_to}] border-4 {button_border} rounded-full py-4 px-8 font-black uppercase tracking-widest text-lg md:text-xl text-white shadow-[0_0_20px_rgba(255,58,242,0.6)] relative overflow-hidden z-10">
                    View Deal ⚡
                </a>
            </div>
"""

def build_site():
    json_path = os.path.join(os.path.dirname(__file__), 'used_cars.json')
    if not os.path.exists(json_path):
        print(f"Error: Could not find {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        cars = json.load(f)

    # Extract real vehicle images for any placeholder URLs
    ensure_photo_urls(cars)

    # Save updated JSON with real image URLs
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cars, f, indent=2)

    # Accent colors array
    colors = ['c1', 'c2', 'c3', 'c4', 'c5']
    hex_colors = {
        'c1': '#FF3AF2',
        'c2': '#00F5D4',
        'c3': '#FFE600',
        'c4': '#FF6B35',
        'c5': '#7B2FFF'
    }
    
    border_styles = ['border-solid', 'border-dashed', 'border-double']

    cards_html = []
    
    for i, car in enumerate(cars):
        # Rotate colors using modulo
        primary_idx = i % 5
        secondary_idx = (i + 1) % 5
        tertiary_idx = (i + 2) % 5
        
        primary_color = colors[primary_idx]
        secondary_color = colors[secondary_idx]
        tertiary_color = colors[tertiary_idx]
        
        border_style = border_styles[i % 3]
        
        # Determine shadow
        shadow_idx = (i % 5) + 1
        shadow_class = f"box-shadow-double-{shadow_idx}"
        
        # Determine transform (asymmetry)
        is_odd = i % 2 != 0
        transform_class = "md:translate-y-12" if is_odd else ""
        if i % 3 == 0:
            transform_class += " rotate-1"
        elif i % 3 == 1:
            transform_class += " -rotate-1"
            
        z_class = f"z-[{20 + i}]"
        
        price_str = f"${car['price']:,.0f}" if car.get('price') else "Price TBD"
        
        card = CAR_CARD_TEMPLATE.format(
            border_color=f"border-{secondary_color}",
            border_style=border_style,
            shadow_class=shadow_class,
            transform_class=transform_class,
            z_class=z_class,
            img_border_color=f"border-{primary_color}",
            photo_url=car.get('photo_url', ''),
            accent_bg=tertiary_color,
            price_str=price_str,
            name=car.get('name', 'Unknown Car'),
            border_color_1=f"border-{colors[(i+0)%5]}",
            border_color_2=f"border-{colors[(i+1)%5]}",
            border_color_3=f"border-{colors[(i+2)%5]}",
            location=car.get('location', {}).get('city', 'Unknown'),
            distance=car.get('location', {}).get('distance_miles_from_95051', '?'),
            mpg=car.get('estimated_mpg', '?'),
            mileage=car.get('mileage', '?'),
            url=car.get('url', '#'),
            grad_from=hex_colors[primary_color],
            grad_via=hex_colors[tertiary_color],
            grad_to=hex_colors[secondary_color],
            button_border=f"border-{colors[(i+3)%5]}"
        )
        cards_html.append(card)

    final_html = HTML_TEMPLATE.replace('{car_cards}', ''.join(cards_html))
    
    output_path = os.path.join(os.path.dirname(__file__), 'index.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
        
    print(f"Successfully generated {output_path} with {len(cars)} cars.")

if __name__ == '__main__':
    build_site()
