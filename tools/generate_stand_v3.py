from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200_v3.png')

# Dimensions (80cm x 200cm @ 150 DPI)
DPI = 150
WIDTH = int(80 / 2.54 * DPI)   # ~4724 px
HEIGHT = int(200 / 2.54 * DPI) # ~11811 px

# Safety Margins
BOTTOM_MARGIN = int(15 / 2.54 * DPI) # 15cm safety at bottom for roll-up mechanism
SIDE_MARGIN = int(5 / 2.54 * DPI)    # 5cm side margins

# Colors
WHITE = (255, 255, 255)
BG_LIGHT = (241, 248, 233)     # Very Light Green
BG_DARK = (27, 94, 32)         # Dark Green
BG_ACCENT = (76, 175, 80)      # Medium Green
TEXT_MAIN = (33, 33, 33)       # Dark Grey
TEXT_LIGHT = (255, 255, 255)

# Fonts
def get_font(size, bold=False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def draw_centered_text(draw, text, font, y, fill, width=WIDTH):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def create_stand():
    print(f"Creating stand design v3: {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    current_y = 0
    
    # --- 1. Header Section (White, Clean) ---
    header_height = int(HEIGHT * 0.12)
    
    # Logo
    logo = Image.open(logo_path).convert('RGBA')
    logo_h = int(header_height * 0.8)
    logo_ratio = logo.width / logo.height
    logo_w = int(logo_h * logo_ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    
    # Place Logo Top Left
    img.paste(logo, (SIDE_MARGIN, int(header_height * 0.1)), logo)
    
    # Company Name Top Right
    title_font = get_font(120, bold=True)
    title_text = "Tadweer Tech"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    draw.text((WIDTH - SIDE_MARGIN - title_w, (header_height - title_h)//2), title_text, font=title_font, fill=BG_DARK)
    
    current_y += header_height
    
    # --- 2. Hero Section (Diagonal Cut) ---
    hero_height = int(HEIGHT * 0.30)
    
    # Create a mask for diagonal cut
    mask = Image.new('L', (WIDTH, hero_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    # Polygon: TopLeft, TopRight, BottomRight(higher), BottomLeft(lower)
    # Let's do a slant from bottom-left (lower) to bottom-right (higher)
    slant_h = 300
    mask_draw.polygon([(0,0), (WIDTH,0), (WIDTH, hero_height - slant_h), (0, hero_height)], fill=255)
    
    # Load and resize hero image
    hero = Image.open(hero_path).convert('RGB')
    ratio = max(WIDTH / hero.width, hero_height / hero.height)
    new_w = int(hero.width * ratio)
    new_h = int(hero.height * ratio)
    hero = hero.resize((new_w, new_h), Image.LANCZOS)
    # Center crop
    crop_x = (new_w - WIDTH) // 2
    crop_y = (new_h - hero_height) // 2
    hero = hero.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + hero_height))
    
    # Apply mask
    hero.putalpha(mask)
    
    # Paste hero
    img.paste(hero, (0, current_y), hero)
    
    # Overlay Text on Hero?
    # "We give value to your garbage"
    slogan_font = get_font(130, bold=True)
    slogan_text = "We give value\nto your garbage"
    
    # Draw text with shadow/outline for readability
    text_x = SIDE_MARGIN + 50
    text_y = current_y + 150
    
    # Shadow
    draw.text((text_x + 5, text_y + 5), slogan_text, font=slogan_font, fill=(0,0,0))
    # Main Text
    draw.text((text_x, text_y), slogan_text, font=slogan_font, fill=WHITE)
    
    current_y += hero_height
    
    # --- 3. Key Points (Icons & Text) ---
    # Background: Light Green
    body_start_y = current_y - slant_h # Overlap slightly due to slant
    body_height = HEIGHT - body_start_y - BOTTOM_MARGIN - 400 # Leave space for footer
    
    # Draw background for body
    # We need to fill from the slant downwards
    # Actually, let's just fill the rest of the page with Light Green and paste footer on top
    draw.rectangle([0, body_start_y + slant_h, WIDTH, HEIGHT], fill=BG_LIGHT)
    
    # Fix the gap created by slant (draw a polygon to fill the triangle under the image)
    draw.polygon([(0, current_y), (WIDTH, current_y - slant_h), (WIDTH, current_y), (0, current_y)], fill=BG_LIGHT)
    
    content_y = current_y + 100
    
    # Section Title
    h2_font = get_font(100, bold=True)
    draw_centered_text(draw, "BUILDING A GREENER FUTURE", h2_font, content_y, BG_DARK)
    content_y += 200
    
    # 3 Key Points
    points = [
        ("RECYCLE", "Turning waste into energy"),
        ("SUSTAIN", "Creating a circular economy"),
        ("EDUCATE", "Community awareness & training")
    ]
    
    point_font_title = get_font(80, bold=True)
    point_font_desc = get_font(60, bold=False)
    
    icon_size = 250
    spacing = (WIDTH - (SIDE_MARGIN*2)) // 3
    
    for i, (title, desc) in enumerate(points):
        center_x = SIDE_MARGIN + (spacing * i) + (spacing // 2)
        
        # Icon Circle
        circle_y = content_y
        draw.ellipse([center_x - icon_size//2, circle_y, center_x + icon_size//2, circle_y + icon_size], fill=BG_ACCENT)
        
        # Icon Text (First Letter)
        letter = title[0]
        letter_font = get_font(150, bold=True)
        bbox = draw.textbbox((0, 0), letter, font=letter_font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        draw.text((center_x - lw//2, circle_y + (icon_size - lh)//2 - 20), letter, font=letter_font, fill=WHITE)
        
        # Title
        text_y = circle_y + icon_size + 50
        bbox = draw.textbbox((0, 0), title, font=point_font_title)
        tw = bbox[2] - bbox[0]
        draw.text((center_x - tw//2, text_y), title, font=point_font_title, fill=BG_DARK)
        
        # Desc
        text_y += 100
        # Wrap desc roughly
        words = desc.split()
        line1 = " ".join(words[:len(words)//2 + 1])
        line2 = " ".join(words[len(words)//2 + 1:])
        
        bbox = draw.textbbox((0, 0), line1, font=point_font_desc)
        tw = bbox[2] - bbox[0]
        draw.text((center_x - tw//2, text_y), line1, font=point_font_desc, fill=TEXT_MAIN)
        
        if line2:
            bbox = draw.textbbox((0, 0), line2, font=point_font_desc)
            tw = bbox[2] - bbox[0]
            draw.text((center_x - tw//2, text_y + 70), line2, font=point_font_desc, fill=TEXT_MAIN)

    # --- 4. Footer (Dark Green) ---
    # Ensure it's above the bottom margin
    footer_height = 800 + BOTTOM_MARGIN
    footer_y = HEIGHT - footer_height
    
    # Draw Footer Background with a top curve
    curve_h = 100
    draw.rectangle([0, footer_y + curve_h, WIDTH, HEIGHT], fill=BG_DARK)
    draw.ellipse([-WIDTH*0.1, footer_y, WIDTH*1.1, footer_y + curve_h*2], fill=BG_DARK)
    
    # Content in Footer (Centered)
    footer_content_y = footer_y + 200
    
    # QR Code
    qr_size = 450
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    
    # White BG for QR
    qr_bg = Image.new('RGBA', (qr_size + 40, qr_size + 40), WHITE)
    qr_bg.paste(qr, (20, 20), qr)
    
    img.paste(qr_bg, ((WIDTH - qr_bg.width)//2, footer_content_y), qr_bg)
    
    # Website URL
    url_y = footer_content_y + qr_bg.height + 80
    url_font = get_font(100, bold=True)
    draw_centered_text(draw, "tadweer-tech-sy.org", url_font, url_y, WHITE)
    
    # Social Media Hint
    social_y = url_y + 150
    social_font = get_font(70, bold=False)
    draw_centered_text(draw, "@tadweer_sy | Tadweer Tech", social_font, social_y, BG_ACCENT)
    
    # Save
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design v3 saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
