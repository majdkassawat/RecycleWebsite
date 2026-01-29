#!/usr/bin/env python3
"""Update all event pages with the 20-photo gallery"""
import re

PHOTOS = [
    "2U7A0017", "2U7A0030", "2U7A0037", "2U7A0051", "2U7A0056",
    "2U7A0057", "2U7A0064", "2U7A0093", "2U7A0103", "2U7A0106",
    "2U7A0108", "2U7A0109", "2U7A0110", "2U7A0112", "2U7A0129",
    "2U7A0148", "2U7A0150", "2U7A0171", "2U7A0177", "2U7A0192"
]

def generate_gallery_html():
    """Generate the gallery HTML with all 20 photos"""
    slides = ""
    dots = ""
    
    for i, photo in enumerate(PHOTOS):
        active = "active" if i == 0 else ""
        slides += f'''                    <div class="slide {active}">
                        <img src="images/events_launch/{photo}.jpg" alt="Launch event photo {i+1}">
                        <div class="slide-caption">Launch Event - Moment {i+1}</div>
                    </div>
'''
        dots += f'                        <button class="dot {active}" data-slide="{i}" aria-label="Show event {i+1}"></button>\n'
    
    gallery = f'''            <div class="events-slider">
                <div class="slides">
{slides}                </div>

                <div class="slider-controls">
                    <button id="prevSlide" aria-label="Previous event"><i class="fas fa-chevron-left"></i></button>
                    <div class="dots">
{dots}                    </div>
                    <button id="nextSlide" aria-label="Next event"><i class="fas fa-chevron-right"></i></button>
                </div>
            </div>'''
    
    return gallery

def update_file(filepath, gallery_html):
    """Update a single event page"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the old slider section
    old_pattern = r'<div class="events-slider">.*?</div>\s*</div>\s*</section>'
    new_section = gallery_html + '\n        </div>\n    </section>'
    
    content = re.sub(old_pattern, new_section, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Generate gallery HTML once
gallery_html = generate_gallery_html()

# Update all event pages
files = [
    "events_ar.html",
    "events_de.html", 
    "events_es.html",
    "events_tr.html"
]

print("Updating event pages with 20-photo gallery...")
for filename in files:
    try:
        update_file(filename, gallery_html)
        print(f"  ✓ {filename}")
    except Exception as e:
        print(f"  ✗ {filename}: {e}")

print("\n✓ All event pages updated!")
