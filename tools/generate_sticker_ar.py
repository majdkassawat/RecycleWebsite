from PIL import Image, ImageDraw, ImageFont
import os
import arabic_reshaper
from bidi.algorithm import get_display

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'tadweer_sticker_ar.png')

# Configuration
# 6x6 cm at 300 DPI = 709x709 pixels
WIDTH = 709
HEIGHT = 709
BG_COLOR = (165, 214, 167)   # Light green
TEXT_COLOR = (27, 94, 32)    # Dark green
WHITE = (255, 255, 255)

# Arabic Text
JOIN_US_TEXT = "انضم إلينا"
SLOGAN = "نحن نعطي قيمة لنفاياتك"
TAGLINE = "نفايات اليوم، طاقة الغد"

# Reshape and reorder Arabic text
def process_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

JOIN_US_TEXT = process_arabic(JOIN_US_TEXT)
SLOGAN = process_arabic(SLOGAN)
TAGLINE = process_arabic(TAGLINE)

# Create canvas
img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw main circular background
# Leave a small margin for the cut line
margin = 10
circle_radius = (WIDTH // 2) - margin
center = (WIDTH // 2, HEIGHT // 2)
draw.ellipse(
    [(center[0] - circle_radius, center[1] - circle_radius),
     (center[0] + circle_radius, center[1] + circle_radius)],
    fill=BG_COLOR
)

# Try to load fonts
try:
    # Windows fonts usually available
    # Adjusted sizes for 709px (6cm)
    font_join = ImageFont.truetype("arialbd.ttf", 35)
    font_slogan = ImageFont.truetype("arialbd.ttf", 30)
    font_tagline = ImageFont.truetype("arial.ttf", 25)
except:
    # Fallback
    font_join = ImageFont.load_default()
    font_slogan = ImageFont.load_default()
    font_tagline = ImageFont.load_default()

# Layout Calculation
# Order: Slogan -> Logo -> Join Us -> Tagline -> QR

# 1. Logo (Aspect Ratio Preserved)
logo = Image.open(logo_path).convert('RGBA')
max_logo_size = 300 # Max dimension
w, h = logo.size
aspect_ratio = w / h

if w > h:
    new_w = max_logo_size
    new_h = int(max_logo_size / aspect_ratio)
else:
    new_h = max_logo_size
    new_w = int(max_logo_size * aspect_ratio)

logo = logo.resize((new_w, new_h), Image.LANCZOS)
logo_w, logo_h = logo.size

# 2. QR Code
qr_size = 130
qr = Image.open(qr_path).convert('RGBA')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

# Calculate Heights
bbox_slogan = draw.textbbox((0, 0), SLOGAN, font=font_slogan)
h_slogan = bbox_slogan[3] - bbox_slogan[1]

bbox_join = draw.textbbox((0, 0), JOIN_US_TEXT, font=font_join)
h_join = bbox_join[3] - bbox_join[1]

bbox_tagline = draw.textbbox((0, 0), TAGLINE, font=font_tagline)
h_tagline = bbox_tagline[3] - bbox_tagline[1]

qr_bg_padding = 8
qr_bg_size = qr_size + (qr_bg_padding * 2)

# Gaps
gap_slogan_logo = 10
gap_logo_join = 10
gap_join_tagline = 5
gap_tagline_qr = 15

total_height = h_slogan + gap_slogan_logo + logo_h + gap_logo_join + h_join + gap_join_tagline + h_tagline + gap_tagline_qr + qr_bg_size

start_y = (HEIGHT - total_height) // 2
current_y = start_y

# Draw Slogan
w_slogan = bbox_slogan[2] - bbox_slogan[0]
draw.text(((WIDTH - w_slogan) // 2, current_y), SLOGAN, fill=TEXT_COLOR, font=font_slogan)
current_y += h_slogan + gap_slogan_logo

# Draw Logo
logo_x = (WIDTH - logo_w) // 2
img.paste(logo, (logo_x, current_y), logo)
current_y += logo_h + gap_logo_join

# Draw Join Us
w_join = bbox_join[2] - bbox_join[0]
draw.text(((WIDTH - w_join) // 2, current_y), JOIN_US_TEXT, fill=TEXT_COLOR, font=font_join)
current_y += h_join + gap_join_tagline

# Draw Tagline
w_tagline = bbox_tagline[2] - bbox_tagline[0]
draw.text(((WIDTH - w_tagline) // 2, current_y), TAGLINE, fill=TEXT_COLOR, font=font_tagline)
current_y += h_tagline + gap_tagline_qr

# Draw QR
qr_bg_x = (WIDTH - qr_bg_size) // 2
draw.rounded_rectangle(
    [(qr_bg_x, current_y), (qr_bg_x + qr_bg_size, current_y + qr_bg_size)],
    radius=15,
    fill=WHITE
)
qr_x = (WIDTH - qr_size) // 2
qr_y = current_y + qr_bg_padding
img.paste(qr, (qr_x, qr_y), qr)

# Save
img.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker created successfully: {output_path}')
print(f'Size: {WIDTH}x{HEIGHT}px (6x6 cm @ 300 DPI)')
