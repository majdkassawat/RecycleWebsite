# Launch Event Photos Integration Guide

## Step 1: Download Photos from Google Drive

**Folder:** https://drive.google.com/drive/folders/1X4NliNM53KsrQYmyEFe_WlAX2mX5g0Dm?usp=drive_link

**Select these 20 files:**
1. 2U7A0017.jpg
2. 2U7A0030.jpg
3. 2U7A0037.jpg
4. 2U7A0051.jpg
5. 2U7A0056.jpg
6. 2U7A0057.jpg
7. 2U7A0064.jpg
8. 2U7A0093.jpg
9. 2U7A0103.jpg
10. 2U7A0106.jpg
11. 2U7A0108.jpg
12. 2U7A0109.jpg
13. 2U7A0110.jpg
14. 2U7A0112.jpg
15. 2U7A0129.jpg
16. 2U7A0148.jpg
17. 2U7A0150.jpg
18. 2U7A0171.jpg
19. 2U7A0177.jpg
20. 2U7A0192.jpg

**How to download:**
- Use Ctrl+Click to select multiple files
- Click "Download" button (top right)
- Extract ZIP to: `images/events_launch/`

## Step 2: Optimize Images

```bash
python tools/optimize_event_images.py
```

This will:
- Resize photos from 9-14MB to ~300-500KB
- Maintain image quality
- Prepare for web display

## Step 3: Generate Slider HTML

```bash
python tools/generate_events_slider.py
```

This creates the responsive slider HTML with all 20 photos.

## Step 4: Update Events Pages

The HTML will be generated and inserted into:
- `events.html` (English)
- `events_ar.html` (Arabic)
- `events_de.html` (German)
- `events_es.html` (Spanish)
- `events_tr.html` (Turkish)

## Result

Beautiful image gallery with:
- ✓ 20 high-quality launch event photos
- ✓ Responsive design (works on mobile/desktop)
- ✓ Navigation arrows and dot indicators
- ✓ Smooth transitions between photos
- ✓ Optimized for fast loading
