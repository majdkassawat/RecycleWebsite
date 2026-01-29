#!/usr/bin/env python3
"""
Optimize real photos from Google Drive for web use.
Place downloaded photos in: C:\Users\kasmaj\Downloads\launch_photos\
Then run this script.
"""
import os
import sys
from pathlib import Path
from PIL import Image

# Source folder where user downloaded photos
SOURCE_DIR = Path(r"C:\Users\kasmaj\Downloads\launch_photos")
# Destination in website
DEST_DIR = Path("images/events_launch")

# Target photos (in order)
PHOTOS = [
    "2U7A0017", "2U7A0030", "2U7A0037", "2U7A0051", "2U7A0056",
    "2U7A0057", "2U7A0064", "2U7A0093", "2U7A0103", "2U7A0106",
    "2U7A0108", "2U7A0109", "2U7A0110", "2U7A0112", "2U7A0129",
    "2U7A0148", "2U7A0150", "2U7A0171", "2U7A0177", "2U7A0192"
]

# Web optimization settings
MAX_WIDTH = 1600
MAX_HEIGHT = 1200
JPEG_QUALITY = 85

def optimize_image(src_path, dest_path):
    """Resize and compress image for web"""
    img = Image.open(src_path)
    
    # Convert to RGB if needed (for PNG with alpha)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Resize maintaining aspect ratio
    img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
    
    # Save optimized
    img.save(dest_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
    
    original_size = os.path.getsize(src_path) / 1024 / 1024  # MB
    new_size = os.path.getsize(dest_path) / 1024  # KB
    
    return original_size, new_size

def main():
    print("=" * 60)
    print("LAUNCH EVENT PHOTO OPTIMIZER")
    print("=" * 60)
    
    # Check source directory
    if not SOURCE_DIR.exists():
        print(f"\n❌ ERROR: Source folder not found!")
        print(f"   Please download photos to: {SOURCE_DIR}")
        print(f"\n   Steps:")
        print(f"   1. Open Google Drive folder with launch photos")
        print(f"   2. Download the 2U7A series photos")
        print(f"   3. Place them in: {SOURCE_DIR}")
        print(f"   4. Run this script again")
        sys.exit(1)
    
    # Create destination
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    
    # Find available photos
    available = list(SOURCE_DIR.glob("2U7A*.jpg")) + list(SOURCE_DIR.glob("2U7A*.JPG"))
    print(f"\n📁 Found {len(available)} photos in source folder")
    
    if len(available) == 0:
        print(f"\n❌ No 2U7A*.jpg photos found in {SOURCE_DIR}")
        sys.exit(1)
    
    # Process photos
    processed = 0
    total_original = 0
    total_optimized = 0
    
    for photo_name in PHOTOS:
        # Find matching file (case insensitive)
        src_file = None
        for f in available:
            if f.stem.upper() == photo_name.upper():
                src_file = f
                break
        
        if not src_file:
            print(f"  ⚠ {photo_name}.jpg - NOT FOUND, skipping")
            continue
        
        dest_file = DEST_DIR / f"{photo_name}.jpg"
        
        try:
            orig_mb, new_kb = optimize_image(src_file, dest_file)
            total_original += orig_mb
            total_optimized += new_kb
            processed += 1
            print(f"  ✓ {photo_name}.jpg: {orig_mb:.1f}MB → {new_kb:.0f}KB")
        except Exception as e:
            print(f"  ✗ {photo_name}.jpg: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"✓ COMPLETE: {processed}/{len(PHOTOS)} photos optimized")
    print(f"  Original total: {total_original:.1f} MB")
    print(f"  Optimized total: {total_optimized/1024:.1f} MB")
    print(f"  Saved: {(1 - total_optimized/1024/total_original)*100:.0f}% reduction")
    print("\nNext steps:")
    print("  git add images/events_launch/")
    print('  git commit -m "Add real launch event photos"')
    print("  git push")
    print("=" * 60)

if __name__ == "__main__":
    main()
