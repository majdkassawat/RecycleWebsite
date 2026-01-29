# How to Add Real Launch Event Photos

The current images are **placeholders**. You need to download the real photos from Google Drive.

## Step 1: Download Photos from Google Drive

1. Open this Google Drive folder: [Launch Event Photos](https://drive.google.com/drive/folders/YOUR_FOLDER_ID)
2. Select these 20 photos (or download all and we'll pick the best):
   - 2U7A0017.jpg
   - 2U7A0030.jpg
   - 2U7A0037.jpg
   - 2U7A0051.jpg
   - 2U7A0056.jpg
   - 2U7A0057.jpg
   - 2U7A0064.jpg
   - 2U7A0093.jpg
   - 2U7A0103.jpg
   - 2U7A0106.jpg
   - 2U7A0108.jpg
   - 2U7A0109.jpg
   - 2U7A0110.jpg
   - 2U7A0112.jpg
   - 2U7A0129.jpg
   - 2U7A0148.jpg
   - 2U7A0150.jpg
   - 2U7A0171.jpg
   - 2U7A0177.jpg
   - 2U7A0192.jpg

3. Download them to: `C:\Users\kasmaj\Downloads\launch_photos\`

## Step 2: Run the Optimization Script

```powershell
cd c:\Users\kasmaj\TFS\Repositories\RecycleWebsite
python tools/optimize_real_photos.py
```

## Step 3: Commit and Deploy

```powershell
git add images/events_launch/
git commit -m "Add real launch event photos"
git push
```

The photos will be live on the website within 1-2 minutes after pushing.
