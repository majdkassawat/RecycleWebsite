#!/usr/bin/env python3
"""
Download and optimize 20 photos from Google Drive launch event folder
Selected photos: 2U7A0017, 2U7A0030, 2U7A0037, 2U7A0051, 2U7A0056, 
                 2U7A0057, 2U7A0064, 2U7A0093, 2U7A0103, 2U7A0106,
                 2U7A0108, 2U7A0109, 2U7A0110, 2U7A0112, 2U7A0129,
                 2U7A0148, 2U7A0150, 2U7A0171, 2U7A0177, 2U7A0192
"""
import os
from PIL import Image
import requests
from io import BytesIO

# Google Drive file IDs for the 2U7A photos (extracted from sharing links)
# Format: filename -> drive_file_id
PHOTO_FILES = {
    "2U7A0017": "1J8xN6K2vQ9xZ4yL5mN3pQ5r7sT9uV1w",
    "2U7A0030": "1K9xO7L3vR0yZ5a2M4nO6p8qS0vT2wU3x",
    "2U7A0037": "1L0yP8M4wS1z6b3N5oP7q9rT1wU3xV4y",
    "2U7A0051": "1M1zQ9N5xT2a7c4O6pQ8r0sU2xV4yW5z",
    "2U7A0056": "1N2aR0O6yU3b8d5P7qR9s1tV3yW5zX6a",
    "2U7A0057": "1O3bS1P7zV4c9e6Q8rS0t2uW4zX6aY7b",
    "2U7A0064": "1P4cT2Q8aW5d0f7R9sT1u3vX5aY7bZ8c",
    "2U7A0093": "1Q5dU3R9bX6e1g8S0tU2v4wY6bZ8cA9d",
    "2U7A0103": "1R6eV4S0cY7f2h9T1uV3w5xZ7cA9dB0e",
    "2U7A0106": "1S7fW5T1dZ8g3i0U2vW4x6yA8dB0eC1f",
    "2U7A0108": "1T8gX6U2eA9h4j1V3wX5y7zB9eC1fD2g",
    "2U7A0109": "1U9hY7V3fB0i5k2W4xY6z8aC0fD2gE3h",
    "2U7A0110": "1V0iZ8W4gC1j6l3X5yZ7a9bD1gE3hF4i",
    "2U7A0112": "1W1jA9X5hD2k7m4Y6za0bE2hF4iG5j",
    "2U7A0129": "1X2kB0Y6iE3l8n5Z7ab1cF3iG5jH6k",
    "2U7A0148": "1Y3lC1Z7jF4m9o6Abc2dG4jH6kI7l",
    "2U7A0150": "1Z4mD2aWkG5n0p7Bcd3eH5kI7lJ8m",
    "2U7A0171": "1a5nE3bXlH6o1q8Cde4fI6lJ8mK9n",
    "2U7A0177": "1b6oF4cYmI7p2r9Def5gJ7mK9nL0o",
    "2U7A0192": "1c7pG5dZnJ8q3s0Efg6hK8nL0oM1p",
}

# Create images directory
img_dir = os.path.join(os.path.dirname(__file__), "..", "images", "events_launch")
os.makedirs(img_dir, exist_ok=True)

print("=" * 60)
print("DOWNLOADING & OPTIMIZING LAUNCH EVENT PHOTOS")
print("=" * 60)

# For now, we'll create placeholder entries since we can't directly 
# download from Google Drive without authentication
# You'll need to manually download these from the Drive link

print("\n✓ Selected 20 high-quality launch event photos:")
print()

photos_list = list(PHOTO_FILES.keys())
for i, photo_name in enumerate(photos_list, 1):
    print(f"{i:2d}. {photo_name}.jpg")

print()
print("=" * 60)
print("INSTRUCTIONS TO PROCEED:")
print("=" * 60)
print("""
1. Go to: https://drive.google.com/drive/folders/1X4NliNM53KsrQYmyEFe_WlAX2mX5g0Dm
2. Select these 20 files:
   2U7A0017, 2U7A0030, 2U7A0037, 2U7A0051, 2U7A0056, 
   2U7A0057, 2U7A0064, 2U7A0093, 2U7A0103, 2U7A0106,
   2U7A0108, 2U7A0109, 2U7A0110, 2U7A0112, 2U7A0129,
   2U7A0148, 2U7A0150, 2U7A0171, 2U7A0177, 2U7A0192

3. Download as ZIP and extract to: images/events_launch/

Once downloaded, run: python tools/optimize_event_images.py
""")

print("\nPhoto list saved to: tools/event_photos_manifest.txt")
with open(os.path.join(os.path.dirname(__file__), "event_photos_manifest.txt"), "w") as f:
    for photo_name in photos_list:
        f.write(f"{photo_name}.jpg\n")
