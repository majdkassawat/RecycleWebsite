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
BG_COLOR_1 = (46, 125, 50)   # Primary green
BG_COLOR_2 = (129, 199, 132) # Light green accent
WHITE = (255, 255, 255)
SLOGAN = "We Give the Value of Your Waste"
TAGLINE = "Today's residues, tomorrow's energy"
WEBSITE = "tadweer-tech-sy.org"

# Create canvas with solid background
img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
draw = ImageDraw.Draw(img)

# Draw clean circular background
circle_radius = 560
draw.ellipse(
    [(WIDTH//2 - circle_radius, HEIGHT//2 - circle_radius),
     (WIDTH//2 + circle_radius, HEIGHT//2 + circle_radius)],
    fill=BG_COLOR_1
)

# Load and resize logo (top center)
logo = Image.open(logo_path).convert('RGBA')
logo_size = 320
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
logo_x = (WIDTH - logo_size) // 2
logo_y = 120
img.paste(logo, (logo_x, logo_y), logo)

# Load and resize QR code (bottom center)
qr = Image.open(qr_path).convert('RGBA')
qr_size = 280
qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
qr_x = (WIDTH - qr_size) // 2
qr_y = HEIGHT - 380
img.paste(qr, (qr_x, qr_y), qr)

# Try to load fonts, fallback to default
try:
    font_large = ImageFont.truetype("arialbd.ttf", 50)
    font_small = ImageFont.truetype("arial.ttf", 32)
    font_website = ImageFont.truetype("arialbd.ttf", 36)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_website = ImageFont.load_default()

# Add slogan in middle section
middle_y = logo_y + logo_size + 60

# Main slogan
bbox = draw.textbbox((0, 0), SLOGAN, font=font_large)
text_width = bbox[2] - bbox[0]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, middle_y), SLOGAN, fill=WHITE, font=font_large)

# Tagline
middle_y += 70
bbox = draw.textbbox((0, 0), TAGLINE, font=font_small)
text_width = bbox[2] - bbox[0]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, middle_y), TAGLINE, fill=(240, 240, 240), font=font_small)

# Website URL below QR
website_y = qr_y + qr_size + 20
bbox = draw.textbbox((0, 0), WEBSITE, font=font_website)
text_width = bbox[2] - bbox[0]
x_pos = (WIDTH - text_width) // 2
draw.text((x_pos, website_y), WEBSITE, fill=WHITE, font=font_website)

# Add decorative circular border
border_width = 12
draw.ellipse(
    [(border_width, border_width), (WIDTH - border_width, HEIGHT - border_width)],
    outline=WHITE,
    width=border_width
)

# Save high-resolution image
img.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker created successfully: {output_path}')
print(f'Size: {WIDTH}x{HEIGHT}px')
print('Ready for printing at 300 DPI (approx 4x4 inches)')
