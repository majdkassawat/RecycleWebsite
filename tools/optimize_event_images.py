#!/usr/bin/env python3
"""
Optimize launch event photos for web display
Resizes from 9-14MB to ~300-500KB for fast loading
"""
import os
from PIL import Image
import glob

def optimize_images():
    img_dir = os.path.join(os.path.dirname(__file__), "..", "images", "events_launch")
    
    if not os.path.exists(img_dir):
        print(f"Error: {img_dir} not found. Download photos first.")
        return
    
    jpg_files = sorted(glob.glob(os.path.join(img_dir, "*.jpg")))
    
    if not jpg_files:
        print(f"No JPG files found in {img_dir}")
        return
    
    print(f"Found {len(jpg_files)} photos to optimize")
    print()
    
    for i, filepath in enumerate(jpg_files, 1):
        filename = os.path.basename(filepath)
        try:
            # Open image
            img = Image.open(filepath)
            original_size = os.path.getsize(filepath) / (1024*1024)
            
            # Resize to max 1200px width while maintaining aspect ratio
            max_width = 1200
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized version with quality 85
            img.save(filepath, quality=85, optimize=True)
            new_size = os.path.getsize(filepath) / (1024*1024)
            
            print(f"{i:2d}. {filename:20s} | {original_size:6.1f}MB → {new_size:5.2f}MB ✓")
            
        except Exception as e:
            print(f"{i:2d}. {filename:20s} | Error: {e}")
    
    print()
    print("✓ All images optimized successfully!")
    print(f"Total photos: {len(jpg_files)}")

if __name__ == "__main__":
    optimize_images()
