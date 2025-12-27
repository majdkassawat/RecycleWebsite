from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import random

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200_v5.png')

# Dimensions (80cm x 200cm @ 150 DPI)
DPI = 150
WIDTH = int(80 / 2.54 * DPI)   # ~4724 px
HEIGHT = int(200 / 2.54 * DPI) # ~11811 px

# Safety Margins
BOTTOM_MARGIN = int(15 / 2.54 * DPI) # 15cm safety at bottom
SIDE_MARGIN = int(5 / 2.54 * DPI)    # 5cm side margins

# Colors
WHITE = (255, 255, 255)
BG_LIGHT = (241, 248, 233)     # Very Light Green
BG_DARK = (27, 94, 32)         # Dark Green
BG_ACCENT = (76, 175, 80)      # Medium Green
BG_ACCENT_LIGHT = (165, 214, 167) # Light Accent
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

def draw_wrapped_text_centered(draw, text, font, max_width, start_y, fill, line_spacing=1.2):
    lines = []
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        words = paragraph.split()
        if not words: continue
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    
    y = start_y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        draw_x = (WIDTH - line_width) // 2
        draw.text((draw_x, y), line, font=font, fill=fill)
        y += int(line_height * line_spacing)
    return y

def draw_background_pattern(img):
    # Create a separate layer for the pattern
    pattern = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(pattern)
    
    # Draw large faint circles
    for _ in range(15):
        r = random.randint(300, 800)
        x = random.randint(-200, WIDTH + 200)
        y = random.randint(int(HEIGHT*0.3), int(HEIGHT*0.8))
        color = BG_ACCENT_LIGHT + (30,) # Low alpha
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
    # Draw some "leaves" (ellipses)
    for _ in range(10):
        w = random.randint(200, 400)
        h = random.randint(400, 800)
        x = random.randint(0, WIDTH)
        y = random.randint(int(HEIGHT*0.3), int(HEIGHT*0.8))
        color = BG_ACCENT + (20,)
        draw.ellipse([x, y, x+w, y+h], fill=color)

    # Composite
    img.paste(pattern, (0,0), pattern)

def create_stand():
    print(f"Creating stand design v5: {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    
    # --- 1. Header Section ---
    header_height = int(HEIGHT * 0.12)
    draw = ImageDraw.Draw(img)
    
    # Logo
    logo = Image.open(logo_path).convert('RGBA')
    logo_h = int(header_height * 0.85)
    logo_ratio = logo.width / logo.height
    logo_w = int(logo_h * logo_ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (SIDE_MARGIN, int(header_height * 0.075)), logo)
    
    # Title
    title_font = get_font(140, bold=True)
    title_text = "Tadweer Tech"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    draw.text((WIDTH - SIDE_MARGIN - title_w, (header_height - title_h)//2), title_text, font=title_font, fill=BG_DARK)
    
    current_y = header_height
    
    # --- 2. Hero Section ---
    hero_height = int(HEIGHT * 0.28)
    
    # Diagonal Mask
    mask = Image.new('L', (WIDTH, hero_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    slant_h = 250
    mask_draw.polygon([(0,0), (WIDTH,0), (WIDTH, hero_height - slant_h), (0, hero_height)], fill=255)
    
    hero = Image.open(hero_path).convert('RGB')
    ratio = max(WIDTH / hero.width, hero_height / hero.height)
    new_w = int(hero.width * ratio)
    new_h = int(hero.height * ratio)
    hero = hero.resize((new_w, new_h), Image.LANCZOS)
    crop_x = (new_w - WIDTH) // 2
    crop_y = (new_h - hero_height) // 2
    hero = hero.crop((crop_x, crop_y, crop_x + WIDTH, crop_y + hero_height))
    hero.putalpha(mask)
    img.paste(hero, (0, current_y), hero)
    
    # Slogan Overlay
    slogan_font = get_font(160, bold=True)
    slogan_text = "We give value\nto your garbage"
    text_x = SIDE_MARGIN + 50
    text_y = current_y + 150
    draw.text((text_x + 8, text_y + 8), slogan_text, font=slogan_font, fill=(0,0,0))
    draw.text((text_x, text_y), slogan_text, font=slogan_font, fill=WHITE)
    
    current_y += hero_height
    
    # --- 3. Body Background & Pattern ---
    body_start_y = current_y - slant_h
    draw.rectangle([0, body_start_y + slant_h, WIDTH, HEIGHT], fill=BG_LIGHT)
    draw.polygon([(0, current_y), (WIDTH, current_y - slant_h), (WIDTH, current_y), (0, current_y)], fill=BG_LIGHT)
    
    # Apply Pattern
    draw_background_pattern(img)
    draw = ImageDraw.Draw(img) # Re-init draw to draw on top of pattern
    
    content_y = current_y + 50
    
    # --- 4. Intro Section ---
    h2_font = get_font(130, bold=True)
    draw_centered_text(draw, "BUILDING A GREENER FUTURE", h2_font, content_y, BG_DARK)
    content_y += 180
    
    intro_text = "We are an initiative aiming to find solutions to the waste problem and minimize its harm to the Syrian environment. We envision a world where waste is minimized, every material is recyclable, and communities thrive in harmony with nature."
    intro_font = get_font(85, bold=False) # Increased font size
    content_y = draw_wrapped_text_centered(draw, intro_text, intro_font, WIDTH - (SIDE_MARGIN*2), content_y, TEXT_MAIN, line_spacing=1.3)
    
    content_y += 150
    
    # --- 5. Key Points (Cards) ---
    points = [
        ("RECYCLE", "Turning waste into energy & reducing landfills."),
        ("SUSTAIN", "Creating a circular economy & eco-friendly practices."),
        ("EDUCATE", "Community awareness & youth engagement.")
    ]
    
    # Draw these as horizontal cards to fill width
    card_height = 450
    card_margin_y = 60
    
    icon_size = 250
    
    point_title_font = get_font(100, bold=True)
    point_desc_font = get_font(75, bold=False)
    
    for title, desc in points:
        card_rect = [SIDE_MARGIN, content_y, WIDTH - SIDE_MARGIN, content_y + card_height]
        
        # Card Background (White with shadow/border)
        draw.rectangle(card_rect, fill=WHITE, outline=BG_ACCENT, width=5)
        
        # Icon Circle (Left)
        icon_x = SIDE_MARGIN + 50
        icon_y = content_y + (card_height - icon_size)//2
        draw.ellipse([icon_x, icon_y, icon_x + icon_size, icon_y + icon_size], fill=BG_ACCENT)
        
        # Icon Letter
        letter = title[0]
        letter_font = get_font(150, bold=True)
        bbox = draw.textbbox((0, 0), letter, font=letter_font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        draw.text((icon_x + (icon_size - lw)//2, icon_y + (icon_size - lh)//2 - 20), letter, font=letter_font, fill=WHITE)
        
        # Text (Right)
        text_x = icon_x + icon_size + 80
        text_w = (WIDTH - SIDE_MARGIN) - text_x - 50
        
        # Title
        draw.text((text_x, content_y + 80), title, font=point_title_font, fill=BG_DARK)
        
        # Desc
        # Wrap desc
        lines = []
        words = desc.split()
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            bbox = draw.textbbox((0, 0), test_line, font=point_desc_font)
            if (bbox[2] - bbox[0]) <= text_w:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        
        desc_y = content_y + 220
        for line in lines:
            draw.text((text_x, desc_y), line, font=point_desc_font, fill=TEXT_MAIN)
            desc_y += 90
            
        content_y += card_height + card_margin_y

    # --- 6. Our Values (New Strip) ---
    # Add a strip for values
    values_y = content_y + 50
    values_h = 500
    draw.rectangle([0, values_y, WIDTH, values_y + values_h], fill=BG_ACCENT_LIGHT)
    
    val_title_font = get_font(90, bold=True)
    draw_centered_text(draw, "OUR CORE VALUES", val_title_font, values_y + 50, BG_DARK)
    
    values = ["Sustainability", "Integrity", "Inclusivity", "Innovation"]
    val_item_font = get_font(70, bold=True)
    
    # Distribute horizontally
    val_spacing = WIDTH // 4
    val_y = values_y + 250
    
    for i, val in enumerate(values):
        cx = (i * val_spacing) + (val_spacing // 2)
        
        # Draw a dot
        dot_r = 20
        draw.ellipse([cx - dot_r, val_y - 80 - dot_r, cx + dot_r, val_y - 80 + dot_r], fill=BG_DARK)
        
        bbox = draw.textbbox((0, 0), val, font=val_item_font)
        tw = bbox[2] - bbox[0]
        draw.text((cx - tw//2, val_y), val, font=val_item_font, fill=BG_DARK)

    # --- 7. Footer ---
    footer_height = 800 + BOTTOM_MARGIN
    footer_y = HEIGHT - footer_height
    
    # Draw Footer Background
    curve_h = 150
    draw.rectangle([0, footer_y + curve_h, WIDTH, HEIGHT], fill=BG_DARK)
    draw.ellipse([-WIDTH*0.1, footer_y, WIDTH*1.1, footer_y + curve_h*2], fill=BG_DARK)
    
    footer_content_y = footer_y + 250
    
    # QR Code
    qr_size = 500
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    qr_bg = Image.new('RGBA', (qr_size + 50, qr_size + 50), WHITE)
    qr_bg.paste(qr, (25, 25), qr)
    img.paste(qr_bg, ((WIDTH - qr_bg.width)//2, footer_content_y), qr_bg)
    
    # URL
    url_y = footer_content_y + qr_bg.height + 80
    url_font = get_font(110, bold=True)
    draw_centered_text(draw, "tadweer-tech-sy.org", url_font, url_y, WHITE)
    
    # Social
    social_y = url_y + 160
    social_font = get_font(80, bold=False)
    draw_centered_text(draw, "@tadweer_sy | Tadweer Tech", social_font, social_y, BG_ACCENT)
    
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design v5 saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
