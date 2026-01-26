#!/usr/bin/env python3
"""
Generate HTML for events slider with 20 launch event photos
Supports image gallery with smooth transitions
"""
import os
import glob

def generate_events_html():
    img_dir = os.path.join(os.path.dirname(__file__), "..", "images", "events_launch")
    
    jpg_files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
    
    if not jpg_files:
        print("No photos found in images/events_launch/")
        print("Please download the 20 photos first.")
        return None
    
    # Generate slide HTML
    slides_html = ""
    dots_html = ""
    
    for i, filepath in enumerate(jpg_files):
        filename = os.path.basename(filepath)
        relative_path = f"images/events_launch/{filename}"
        active_class = "active" if i == 0 else ""
        
        slides_html += f'''                    <div class="slide {active_class}">
                        <img src="{relative_path}" alt="Launch event photo {i+1}">
                        <div class="slide-caption">Launch Event Moment</div>
                    </div>
'''
        
        dots_html += f'                    <span class="dot {active_class}" onclick="currentSlide({i+1})"></span>\n'
    
    slider_code = f'''            <div class="events-slider">
                <div class="slides">
{slides_html}                </div>
                
                <!-- Navigation dots -->
                <div class="dots-container">
{dots_html}                </div>
                
                <!-- Prev/Next buttons -->
                <a class="prev" onclick="changeSlide(-1)">&#10094;</a>
                <a class="next" onclick="changeSlide(1)">&#10095;</a>
            </div>'''
    
    return slider_code

if __name__ == "__main__":
    html = generate_events_html()
    if html:
        print(html)
    else:
        print("Unable to generate HTML")
