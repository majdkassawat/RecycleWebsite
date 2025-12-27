from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import random

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200_v6.png')

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
BG_ACCENT_LIGHT = (200, 230, 201) # Light Accent
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

def draw_wrapped_text(draw, text, font, max_width, start_x, start_y, fill, line_spacing=1.2, align="left"):
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
        
        if align == "center":
            draw_x = start_x + (max_width - line_width) // 2
        else:
            draw_x = start_x
            
        draw.text((draw_x, y), line, font=font, fill=fill)
        y += int(line_height * line_spacing)
    return y

def draw_background_pattern(img):
    pattern = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(pattern)
    
    # Draw large faint circles
    for _ in range(20):
        r = random.randint(300, 900)
        x = random.randint(-200, WIDTH + 200)
        y = random.randint(int(HEIGHT*0.2), int(HEIGHT*0.9))
        color = BG_ACCENT_LIGHT + (40,) 
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
    img.paste(pattern, (0,0), pattern)

def create_stand():
    print(f"Creating stand design v6: {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # --- 1. Header Section ---
    header_height = int(HEIGHT * 0.10)
    
    # Logo
    logo = Image.open(logo_path).convert('RGBA')
    logo_h = int(header_height * 0.9)
    logo_ratio = logo.width / logo.height
    logo_w = int(logo_h * logo_ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (SIDE_MARGIN, int(header_height * 0.05)), logo)
    
    # Title
    title_font = get_font(130, bold=True)
    title_text = "Tadweer Tech"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    draw.text((WIDTH - SIDE_MARGIN - title_w, (header_height - title_h)//2), title_text, font=title_font, fill=BG_DARK)
    
    current_y = header_height
    
    # --- 2. Hero Section ---
    hero_height = int(HEIGHT * 0.20) # Reduced height to save space
    
    # Diagonal Mask
    mask = Image.new('L', (WIDTH, hero_height), 0)
    mask_draw = ImageDraw.Draw(mask)
    slant_h = 150
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
    slogan_font = get_font(140, bold=True)
    slogan_text = "We give value\nto your garbage"
    text_x = SIDE_MARGIN + 50
    text_y = current_y + 100
    draw.text((text_x + 6, text_y + 6), slogan_text, font=slogan_font, fill=(0,0,0))
    draw.text((text_x, text_y), slogan_text, font=slogan_font, fill=WHITE)
    
    current_y += hero_height
    
    # --- 3. Body Background & Pattern ---
    body_start_y = current_y - slant_h
    draw.rectangle([0, body_start_y + slant_h, WIDTH, HEIGHT], fill=BG_LIGHT)
    draw.polygon([(0, current_y), (WIDTH, current_y - slant_h), (WIDTH, current_y), (0, current_y)], fill=BG_LIGHT)
    
    draw_background_pattern(img)
    draw = ImageDraw.Draw(img) 
    
    content_y = current_y + 50
    
    # --- 4. Vision & Mission (Side by Side or Stacked) ---
    # Let's stack them to fill vertical space better and use larger text
    
    # Vision
    vision_title_font = get_font(100, bold=True)
    vision_text_font = get_font(70, bold=False)
    
    draw_centered_text(draw, "OUR VISION", vision_title_font, content_y, BG_DARK)
    content_y += 130
    
    vision_text = "A world where waste is minimized, every material is recyclable, and communities thrive in harmony with nature. We envision a global movement where responsible consumption and recycling become a way of life."
    content_y = draw_wrapped_text(draw, vision_text, vision_text_font, WIDTH - (SIDE_MARGIN*2), SIDE_MARGIN, content_y, TEXT_MAIN, align="center")
    
    content_y += 100
    
    # Mission
    draw_centered_text(draw, "OUR MISSION", vision_title_font, content_y, BG_DARK)
    content_y += 130
    
    mission_text = "To promote a sustainable future by encouraging recyclability and reducing waste through education, innovation, and community engagement. We collaborate with individuals, businesses, and governments to create a circular economy."
    content_y = draw_wrapped_text(draw, mission_text, vision_text_font, WIDTH - (SIDE_MARGIN*2), SIDE_MARGIN, content_y, TEXT_MAIN, align="center")
    
    content_y += 120
    
    # --- 5. Our Goals (List) ---
    # Draw a light background box for goals
    goals_start_y = content_y
    
    draw_centered_text(draw, "OUR GOALS", vision_title_font, content_y, BG_DARK)
    content_y += 140
    
    goals = [
        "Utilizing and recycling waste & generated energy.",
        "Developing comprehensive waste-management plans.",
        "Pressuring decision-makers for legal regulations.",
        "Changing collective behaviors through awareness.",
        "Ensuring environmental security for all."
    ]
    
    goal_font = get_font(75, bold=False)
    bullet_r = 15
    
    for goal in goals:
        # Bullet
        draw.ellipse([SIDE_MARGIN + 50, content_y + 30, SIDE_MARGIN + 50 + bullet_r*2, content_y + 30 + bullet_r*2], fill=BG_ACCENT)
        # Text
        draw.text((SIDE_MARGIN + 120, content_y), goal, font=goal_font, fill=TEXT_MAIN)
        content_y += 110
        
    content_y += 80
    
    # --- 6. Core Values (Grid) ---
    # Darker background strip for values
    values_bg_h = 700
    draw.rectangle([0, content_y, WIDTH, content_y + values_bg_h], fill=BG_ACCENT_LIGHT)
    
    val_y = content_y + 60
    draw_centered_text(draw, "CORE VALUES", vision_title_font, val_y, BG_DARK)
    val_y += 150
    
    values = [
        "Sustainability", "Integrity", "Respect", "Professionalism",
        "Safety", "Anti-Discrimination", "Community", "Improvement"
    ]
    
    val_font = get_font(70, bold=True)
    
    # 2 rows of 4
    cols = 2
    rows = 4
    col_w = WIDTH // cols
    row_h = 120
    
    start_val_y = val_y
    
    for i, val in enumerate(values):
        r = i // cols
        c = i % cols
        
        cx = c * col_w + (col_w // 2)
        cy = start_val_y + (r * row_h)
        
        # Checkmark icon
        check_size = 40
        draw.text((cx - 200, cy), "✓", font=get_font(60, True), fill=BG_DARK)
        draw.text((cx - 140, cy), val, font=val_font, fill=BG_DARK)

    content_y += values_bg_h + 50

    # --- 7. Footer ---
    # Remaining space is for footer
    footer_y = HEIGHT - (800 + BOTTOM_MARGIN)
    
    # Ensure we don't overlap if content grew too much (unlikely with this layout but good to check)
    if content_y > footer_y:
        footer_y = content_y + 50
        
    curve_h = 150
    draw.rectangle([0, footer_y + curve_h, WIDTH, HEIGHT], fill=BG_DARK)
    draw.ellipse([-WIDTH*0.1, footer_y, WIDTH*1.1, footer_y + curve_h*2], fill=BG_DARK)
    
    footer_content_y = footer_y + 250
    
    # QR Code
    qr_size = 450
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    qr_bg = Image.new('RGBA', (qr_size + 40, qr_size + 40), WHITE)
    qr_bg.paste(qr, (20, 20), qr)
    img.paste(qr_bg, ((WIDTH - qr_bg.width)//2, footer_content_y), qr_bg)
    
    # URL
    url_y = footer_content_y + qr_bg.height + 60
    url_font = get_font(100, bold=True)
    draw_centered_text(draw, "tadweer-tech-sy.org", url_font, url_y, WHITE)
    
    # Social
    social_y = url_y + 140
    social_font = get_font(70, bold=False)
    draw_centered_text(draw, "@tadweer_sy | Tadweer Tech", social_font, social_y, BG_ACCENT)
    
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design v6 saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
