#!/usr/bin/env python3
"""Download specific launch event photos from Google Drive"""
import gdown
import os
from pathlib import Path
from PIL import Image

# File IDs extracted from Google Drive folder
FILE_IDS = {
    "2U7A0017": "1DG61GOztdRE2dRBL31yqwajH3WktQWVH",
    "2U7A0030": "1sggMClrebJfJwq1kz3b-UnMohQBG6MgM",
    "2U7A0037": "1voEiyGzi2q4DLOXgNIBCxm8aoN8jdzZv",
    "2U7A0051": "1wuUUjj_InNVRmzEOZ--K3nUzyrowheun",
    "2U7A0056": "1fj7eG4Egf1_ukAbYMQ-QArdj06KYiWVP",
    "2U7A0057": "1ptQUH9HlbnW_f_FBeRoStZN2nIAo-Nai",
    "2U7A0064": "1Y6Ub0MYRmCkx-OUPJMR7z7c955rRaa69",
    "2U7A0093": "1Tj9OMYayPKDSSTUpWmB7ZbSNHEbh1NHS",
    "2U7A0103": "1ENvkfBW4q-GXd0WHH94CHG3msQ730tZf",
    "2U7A0106": "1DzJ_UVWKA0aF6vqlCltyJWdRaT6E_ZU_",
    "2U7A0108": "1DNwTfxCH9B9h0c-CtNm9ZfrbZZbv-ueb",
    "2U7A0109": "1F03s_G_VjPP5xrQ5uQ3sQePz6CQtwwU9",
    "2U7A0110": "1KimTl-q_sKjDtFZP2PDNawB5XBumm73i",
    "2U7A0112": "1wlllY3m25alAU2s1EQM6ObE8sqOw4IGO",
    "2U7A0129": "1vvqaP4owm-b9_ie1j0EMtgqt3XBEdjFC",
    "2U7A0148": "1Uq3Felxwq8Sr8ZIu7oH7F4wHEV3dJ2I6",
    "2U7A0150": "1zLJ67F7pyAI2rSPoPb650fb73-lGKO55",
    "2U7A0171": "1EWIsiZiHo_6Sgs7u_4tG5f8WoF_gXdy_",
    "2U7A0177": "1eDAEAdYl6DK0szGPpRyWfQb2DQUMwPjo",
    "2U7A0192": "1kafg0xUuqksjp4yPpLuVt_ou6sWY3mVa",
}

# Web optimization settings
MAX_WIDTH = 1600
MAX_HEIGHT = 1200
JPEG_QUALITY = 85

OUTPUT_DIR = Path("images/events_launch")
TEMP_DIR = Path("images/events_launch_raw")

def download_and_optimize():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("DOWNLOADING LAUNCH EVENT PHOTOS FROM GOOGLE DRIVE")
    print("=" * 60)
    
    for name, file_id in FILE_IDS.items():
        url = f"https://drive.google.com/uc?id={file_id}"
        temp_path = TEMP_DIR / f"{name}.jpg"
        final_path = OUTPUT_DIR / f"{name}.jpg"
        
        print(f"\n📥 {name}.jpg")
        
        # Download
        try:
            gdown.download(url, str(temp_path), quiet=True)
            
            if not temp_path.exists():
                print(f"   ❌ Download failed")
                continue
                
            orig_size = temp_path.stat().st_size / 1024 / 1024
            print(f"   Downloaded: {orig_size:.1f} MB")
            
            # Optimize for web
            img = Image.open(temp_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)
            img.save(final_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            
            new_size = final_path.stat().st_size / 1024
            print(f"   Optimized:  {new_size:.0f} KB")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✓ DOWNLOAD COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    download_and_optimize()
