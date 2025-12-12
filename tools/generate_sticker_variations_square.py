from PIL import Image, ImageDraw, ImageFont
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
qr_path = os.path.join(images_dir, 'qr_website.png')

# Constants
WIDTH = 1200
HEIGHT = 1200
SLOGAN = "We Give the Value of Your Waste"
TAGLINE = "Today's residues, tomorrow's energy"

def create_sticker(filename, config):
    # Unpack config
    bg_color = config.get('bg_color', (46, 125, 50))
    text_color = config.get('text_color', (255, 255, 255))
    logo_size = config.get('logo_size', 400)
    qr_size = config.get('qr_size', 300)
    show_tagline = config.get('show_tagline', True)
    border_width = config.get('border_width', 15)
    border_color = config.get('border_color', (255, 255, 255))
    font_scale = config.get('font_scale', 1.0)
    qr_bg_color = config.get('qr_bg_color', (255, 255, 255))
    
    # Create canvas
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw main SQUARE background
    # Fill the entire canvas
    draw.rectangle([(0, 0), (WIDTH, HEIGHT)], fill=bg_color)

    # Fonts
    try:
        slogan_size = int(65 * font_scale)
        tagline_size = int(40 * font_scale)
        font_slogan = ImageFont.truetype("arialbd.ttf", slogan_size)
        font_tagline = ImageFont.truetype("arial.ttf", tagline_size)
    except:
        font_slogan = ImageFont.load_default()
        font_tagline = ImageFont.load_default()

    # 1. Logo (Top)
    logo = Image.open(logo_path).convert('RGBA')
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    
    # Calculate vertical spacing
    total_content_height = logo_size + qr_size + 100 # Base height
    if show_tagline:
        total_content_height += 120 # Approx text height
    else:
        total_content_height += 60
        
    start_y = (HEIGHT - total_content_height) // 2
    
    # Draw Logo
    logo_x = (WIDTH - logo_size) // 2
    logo_y = start_y
    img.paste(logo, (logo_x, logo_y), logo)
    
    current_y = logo_y + logo_size + 30

    # Draw Text
    # Slogan
    bbox = draw.textbbox((0, 0), SLOGAN, font=font_slogan)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x_pos = (WIDTH - text_width) // 2
    draw.text((x_pos, current_y), SLOGAN, fill=text_color, font=font_slogan)
    current_y += text_height + 15

    # Tagline
    if show_tagline:
        bbox = draw.textbbox((0, 0), TAGLINE, font=font_tagline)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x_pos = (WIDTH - text_width) // 2
        draw.text((x_pos, current_y), TAGLINE, fill=text_color, font=font_tagline)
        current_y += text_height + 30
    else:
        current_y += 15

    # Draw QR Code
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)

    # QR Background (Square with rounded corners or just square?)
    # Let's make it a square with slight padding since the sticker is square
    qr_bg_padding = 15
    qr_bg_size = qr_size + (qr_bg_padding * 2)
    qr_bg_x = (WIDTH - qr_bg_size) // 2
    qr_bg_y = current_y
    
    if qr_bg_color:
        # Draw rounded rectangle for QR background for a softer look
        draw.rounded_rectangle(
            [(qr_bg_x, qr_bg_y), (qr_bg_x + qr_bg_size, qr_bg_y + qr_bg_size)],
            radius=20,
            fill=qr_bg_color
        )

    # Paste QR
    qr_x = (WIDTH - qr_size) // 2
    qr_y = qr_bg_y + qr_bg_padding
    img.paste(qr, (qr_x, qr_y), qr)

    # Border
    if border_width > 0:
        # Draw inner border
        draw.rectangle(
            [(border_width, border_width), (WIDTH - border_width, HEIGHT - border_width)],
            outline=border_color,
            width=border_width
        )

    # Save
    output_full_path = os.path.join(images_dir, filename)
    img.save(output_full_path, 'PNG', dpi=(300, 300))
    print(f'Generated {filename}')

# Define 10 Variations (Square)
configs = [
    # V1: Standard Green, Large Logo
    {
        'bg_color': (46, 125, 50), # Standard Green
        'logo_size': 450,
        'qr_size': 300,
        'show_tagline': True
    },
    # V2: Standard Green, Massive Logo, No Tagline
    {
        'bg_color': (46, 125, 50),
        'logo_size': 550,
        'qr_size': 280,
        'show_tagline': False,
        'font_scale': 1.1
    },
    # V3: White BG, Green Text/Border
    {
        'bg_color': (255, 255, 255),
        'text_color': (46, 125, 50),
        'border_color': (46, 125, 50),
        'qr_bg_color': None, 
        'logo_size': 450,
        'qr_size': 300,
        'show_tagline': True
    },
    # V4: Dark Green, White Text
    {
        'bg_color': (27, 94, 32), # Darker Green
        'logo_size': 450,
        'qr_size': 300,
        'show_tagline': True
    },
    # V5: Light Green, Dark Text
    {
        'bg_color': (165, 214, 167), # Light Green
        'text_color': (27, 94, 32), # Dark Green Text
        'border_color': (27, 94, 32),
        'logo_size': 450,
        'qr_size': 300,
        'show_tagline': True
    },
    # V6: Balanced (Equal Logo/QR), No Tagline
    {
        'bg_color': (46, 125, 50),
        'logo_size': 400,
        'qr_size': 400,
        'show_tagline': False,
        'font_scale': 1.2
    },
    # V7: Thick Border, Standard Green
    {
        'bg_color': (46, 125, 50),
        'logo_size': 420,
        'qr_size': 320,
        'border_width': 40,
        'show_tagline': True
    },
    # V8: Very Compact (Elements closer), Large Logo
    {
        'bg_color': (46, 125, 50),
        'logo_size': 500,
        'qr_size': 250,
        'show_tagline': True,
        'font_scale': 0.9
    },
    # V9: White BG, No Tagline, Large Logo
    {
        'bg_color': (255, 255, 255),
        'text_color': (46, 125, 50),
        'border_color': (46, 125, 50),
        'qr_bg_color': None,
        'logo_size': 500,
        'qr_size': 300,
        'show_tagline': False
    },
    # V10: Teal/Blue-ish Green
    {
        'bg_color': (0, 121, 107), # Teal
        'logo_size': 450,
        'qr_size': 300,
        'show_tagline': True
    }
]

# Generate
for i, config in enumerate(configs):
    create_sticker(f'sticker_square_v{i+1}.png', config)
