from PIL import Image, ImageDraw, ImageFont
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'tadweer_sticker.png')

# Configuration
# 6x6 cm at 300 DPI = 709x709 pixels
WIDTH = 709
HEIGHT = 709
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
# Order: Logo -> Join Us -> Slogan -> Tagline -> QR

# 1. Logo (Top, Bigger than QR)
logo = Image.open(logo_path).convert('RGBA')
logo_size = 300 # Scaled down for 6cm
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

# 2. QR Code (Bottom, Smaller than Logo)
qr_size = 130 # Scaled down for 6cm
qr = Image.open(qr_path).convert('RGBA')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

# Calculate positions to center everything vertically
# Total height estimation:
# Logo (300) + Gap (10) + Join (35) + Gap (5) + Slogan (30) + Gap (5) + Tagline (25) + Gap (15) + QR (130)
# Total approx = 555px. Available height ~709px.
# Start Y = (709 - 555) / 2 = 77px

start_y = 77

# Draw Logo
logo_x = (WIDTH - logo_size) // 2
logo_y = start_y
img.paste(logo, (logo_x, logo_y), logo)

current_y = logo_y + logo_size + 10

# Draw "Join Us"
bbox = draw.textbbox((0, 0), JOIN_US_TEXT, font=font_join)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), JOIN_US_TEXT, fill=TEXT_COLOR, font=font_join)
current_y += text_height + 5

# Draw Slogan
bbox = draw.textbbox((0, 0), SLOGAN, font=font_slogan)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), SLOGAN, fill=TEXT_COLOR, font=font_slogan)
current_y += text_height + 5

# Draw Tagline
bbox = draw.textbbox((0, 0), TAGLINE, font=font_tagline)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), TAGLINE, fill=TEXT_COLOR, font=font_tagline)
current_y += text_height + 15

# Draw QR Code
# White background for QR
qr_bg_padding = 8
qr_bg_size = qr_size + (qr_bg_padding * 2)
qr_bg_x = (WIDTH - qr_bg_size) // 2
qr_bg_y = current_y

draw.rounded_rectangle(
    [(qr_bg_x, qr_bg_y), (qr_bg_x + qr_bg_size, qr_bg_y + qr_bg_size)],
    radius=15,
    fill=WHITE
)

qr_x = (WIDTH - qr_size) // 2
qr_y = qr_bg_y + qr_bg_padding
img.paste(qr, (qr_x, qr_y), qr)

# Save
img.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker created successfully: {output_path}')
print(f'Size: {WIDTH}x{HEIGHT}px (6x6 cm @ 300 DPI)')
