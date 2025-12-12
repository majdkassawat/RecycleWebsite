from PIL import Image, ImageDraw, ImageFont
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'tadweer_sticker.png')

# Configuration
# 6x6 inches at 300 DPI = 1800x1800 pixels
WIDTH = 1800
HEIGHT = 1800
BG_COLOR = (165, 214, 167)   # Light green
TEXT_COLOR = (27, 94, 32)    # Dark green
WHITE = (255, 255, 255)
JOIN_US_TEXT = "Join Us"
SLOGAN = "We give value to your garbage"
TAGLINE = "Today's waste, tomorrow's energy"

# Create canvas
img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw main circular background
# Leave a small margin for the cut line
margin = 20
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
    # Adjusted sizes for 1800px
    font_join = ImageFont.truetype("arialbd.ttf", 70)
    font_slogan = ImageFont.truetype("arialbd.ttf", 60) # Smaller than before relative to size
    font_tagline = ImageFont.truetype("arial.ttf", 50)
except:
    # Fallback
    font_join = ImageFont.load_default()
    font_slogan = ImageFont.load_default()
    font_tagline = ImageFont.load_default()

# Layout Calculation
# We have ~1600px vertical space inside the circle to play with.
# Order: Logo -> Join Us -> Slogan -> Tagline -> QR

# 1. Logo (Top, Bigger than QR)
logo = Image.open(logo_path).convert('RGBA')
logo_size = 900 # 1.5x bigger (approx from 600)
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# 2. QR Code (Bottom, Smaller than Logo)
qr_size = 350 # Reduced to fit
qr = Image.open(qr_path).convert('RGBA')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

# Calculate positions to center everything vertically
# Total height estimation:
# Logo (900) + Gap (15) + Join Us (80) + Gap (10) + Slogan (70) + Gap (10) + Tagline (60) + Gap (20) + QR (350)
# Total approx = 1515px. Available height ~1760px.
# Start Y = (1800 - 1515) / 2 = 142px

start_y = 140

# Draw Logo
logo_x = (WIDTH - logo_size) // 2
logo_y = start_y
img.paste(logo, (logo_x, logo_y), logo)

current_y = logo_y + logo_size + 15

# Draw "Join Us"
bbox = draw.textbbox((0, 0), JOIN_US_TEXT, font=font_join)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), JOIN_US_TEXT, fill=TEXT_COLOR, font=font_join)
current_y += text_height + 10

# Draw Slogan
bbox = draw.textbbox((0, 0), SLOGAN, font=font_slogan)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), SLOGAN, fill=TEXT_COLOR, font=font_slogan)
current_y += text_height + 10

# Draw Tagline
bbox = draw.textbbox((0, 0), TAGLINE, font=font_tagline)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), TAGLINE, fill=TEXT_COLOR, font=font_tagline)
current_y += text_height + 20

# Draw QR Code
# White background for QR
qr_bg_padding = 20
qr_bg_size = qr_size + (qr_bg_padding * 2)
qr_bg_x = (WIDTH - qr_bg_size) // 2
qr_bg_y = current_y

draw.rounded_rectangle(
    [(qr_bg_x, qr_bg_y), (qr_bg_x + qr_bg_size, qr_bg_y + qr_bg_size)],
    radius=30,
    fill=WHITE
)

qr_x = (WIDTH - qr_size) // 2
qr_y = qr_bg_y + qr_bg_padding
img.paste(qr, (qr_x, qr_y), qr)

# Add a nice border ring
border_width = 20
draw.ellipse(
    [(center[0] - circle_radius + border_width//2, center[1] - circle_radius + border_width//2),
     (center[0] + circle_radius - border_width//2, center[1] + circle_radius - border_width//2)],
    outline=TEXT_COLOR,
    width=border_width
)

# Save
img.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker created successfully: {output_path}')
print(f'Size: {WIDTH}x{HEIGHT}px (6x6 inches @ 300 DPI)')
