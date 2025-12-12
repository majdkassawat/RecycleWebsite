from PIL import Image, ImageDraw, ImageFont
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'tadweer_sticker.png')

# Configuration
WIDTH = 1200
HEIGHT = 1200
BG_COLOR = (46, 125, 50)   # Primary green
WHITE = (255, 255, 255)
SLOGAN = "We Give the Value of Your Waste"
TAGLINE = "Today's residues, tomorrow's energy"
WEBSITE = "tadweer-tech-sy.org"

# Create canvas
img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Draw main circular background
circle_radius = 580
center = (WIDTH // 2, HEIGHT // 2)
draw.ellipse(
    [(center[0] - circle_radius, center[1] - circle_radius),
     (center[0] + circle_radius, center[1] + circle_radius)],
    fill=BG_COLOR
)

# Try to load fonts
try:
    # Windows fonts usually available
    font_slogan = ImageFont.truetype("arialbd.ttf", 65)
    font_tagline = ImageFont.truetype("arial.ttf", 40)
    font_website = ImageFont.truetype("arialbd.ttf", 45)
except:
    # Fallback
    font_slogan = ImageFont.load_default()
    font_tagline = ImageFont.load_default()
    font_website = ImageFont.load_default()

# 1. Logo (Top)
logo = Image.open(logo_path).convert('RGBA')
logo_size = 380
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (WIDTH - logo_size) // 2
logo_y = 100 # Start closer to top
img.paste(logo, (logo_x, logo_y), logo)

# 2. Text Block (Middle)
current_y = logo_y + logo_size + 30

# Slogan
bbox = draw.textbbox((0, 0), SLOGAN, font=font_slogan)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), SLOGAN, fill=WHITE, font=font_slogan)
current_y += text_height + 20

# Tagline
bbox = draw.textbbox((0, 0), TAGLINE, font=font_tagline)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), TAGLINE, fill=(230, 230, 230), font=font_tagline)
current_y += text_height + 40

# 3. QR Code (Bottom)
qr_size = 320
qr = Image.open(qr_path).convert('RGBA')
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

# Draw a white background for QR to ensure contrast
qr_bg_padding = 10
qr_bg_size = qr_size + (qr_bg_padding * 2)
qr_bg_x = (WIDTH - qr_bg_size) // 2
qr_bg_y = current_y
draw.ellipse(
    [(qr_bg_x, qr_bg_y), (qr_bg_x + qr_bg_size, qr_bg_y + qr_bg_size)],
    fill=WHITE
)

# Paste QR centered in the white circle
qr_x = (WIDTH - qr_size) // 2
qr_y = qr_bg_y + qr_bg_padding
img.paste(qr, (qr_x, qr_y), qr)

# 4. Website URL (Bottom curve area)
current_y = qr_y + qr_size + 25
bbox = draw.textbbox((0, 0), WEBSITE, font=font_website)
text_width = bbox[2] - bbox[0]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, current_y), WEBSITE, fill=WHITE, font=font_website)

# Add a nice border ring
border_width = 15
draw.ellipse(
    [(center[0] - circle_radius + border_width//2, center[1] - circle_radius + border_width//2),
     (center[0] + circle_radius - border_width//2, center[1] + circle_radius - border_width//2)],
    outline=WHITE,
    width=border_width
)

# Save
img.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker created successfully: {output_path}')
