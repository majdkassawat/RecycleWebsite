from PIL import Image, ImageDraw, ImageFont
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200_v2.png')

# Dimensions (80cm x 200cm @ 150 DPI)
DPI = 150
WIDTH = int(80 / 2.54 * DPI)   # ~4724 px
HEIGHT = int(200 / 2.54 * DPI) # ~11811 px

# Colors
WHITE = (255, 255, 255)
BG_MAIN = (232, 245, 233)      # Light Green Background
BG_HEADER = (27, 94, 32)       # Dark Green
BG_ACCENT = (76, 175, 80)      # Medium Green
TEXT_DARK = (20, 50, 20)       # Very Dark Green
TEXT_WHITE = (255, 255, 255)

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

def draw_wrapped_text_centered(draw, text, font, max_width, start_y, fill, line_spacing=1.3):
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
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        x = (WIDTH - w) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += int(h * line_spacing)
    return y

def create_stand():
    print(f"Creating stand design v2: {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_MAIN)
    draw = ImageDraw.Draw(img)
    
    # --- 1. Header (Curved) ---
    header_h = int(HEIGHT * 0.18)
    # Draw a giant ellipse to make a curve
    draw.ellipse([-WIDTH*0.2, -header_h, WIDTH*1.2, header_h], fill=BG_HEADER)
    
    # Logo centered in header
    logo = Image.open(logo_path).convert('RGBA')
    logo_size = int(header_h * 0.8)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
    img.paste(logo, ((WIDTH - logo_size)//2, int(header_h * 0.1)), logo)
    
    current_y = header_h + 50
    
    # --- 2. Slogan ---
    slogan_font = get_font(140, bold=True)
    slogan = "We give value to your garbage"
    current_y = draw_wrapped_text_centered(draw, slogan, slogan_font, WIDTH - 200, current_y, BG_HEADER)
    
    current_y += 80
    
    # --- 3. Hero Image (Full Width Strip) ---
    hero_h = int(HEIGHT * 0.22)
    hero = Image.open(hero_path).convert('RGB')
    
    # Resize/Crop to fill width
    ratio = WIDTH / hero.width
    new_h = int(hero.height * ratio)
    hero = hero.resize((WIDTH, new_h), Image.LANCZOS)
    
    # Crop center if too tall, or just use what we have
    if new_h > hero_h:
        crop_y = (new_h - hero_h) // 2
        hero = hero.crop((0, crop_y, WIDTH, crop_y + hero_h))
    else:
        # If too short, stretch slightly or fill background? Let's stretch to fit height
        hero = hero.resize((WIDTH, hero_h), Image.LANCZOS)
        
    img.paste(hero, (0, current_y))
    
    # Add a semi-transparent overlay to make it look integrated? No, keep it vibrant.
    # Add a border line
    draw.rectangle([0, current_y, WIDTH, current_y+20], fill=BG_ACCENT)
    draw.rectangle([0, current_y+hero_h-20, WIDTH, current_y+hero_h], fill=BG_ACCENT)
    
    current_y += hero_h + 100
    
    # --- 4. About Us (Big Text) ---
    about_title_font = get_font(110, bold=True)
    about_text_font = get_font(90, bold=False)
    
    draw_centered_text(draw, "ABOUT US", about_title_font, current_y, BG_ACCENT)
    current_y += 140
    
    about_text = "We are an initiative aiming to find solutions to the waste problem and minimize its harm to the Syrian environment."
    current_y = draw_wrapped_text_centered(draw, about_text, about_text_font, WIDTH - 300, current_y, TEXT_DARK)
    
    current_y += 120
    
    # --- 5. Goals (Grid with Icons) ---
    # We will draw 4 main goals in a 2x2 grid to fill space
    goals = [
        ("RECYCLE", "Utilizing waste for energy"),
        ("PLAN", "Comprehensive waste management"),
        ("AWARENESS", "Changing collective behaviors"),
        ("SECURITY", "Environmental security for all")
    ]
    
    grid_y_start = current_y
    col_width = WIDTH // 2
    row_height = 500 # Fixed height for goal cells
    
    goal_title_font = get_font(80, bold=True)
    goal_desc_font = get_font(60, bold=False)
    
    for i, (title, desc) in enumerate(goals):
        row = i // 2
        col = i % 2
        
        x = col * col_width
        y = grid_y_start + (row * row_height)
        
        # Draw a box background for each goal?
        # Let's make them "cards"
        card_margin = 40
        card_w = col_width - (card_margin * 2)
        card_h = row_height - (card_margin * 2)
        card_x = x + card_margin
        card_y = y + card_margin
        
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h], fill=WHITE, outline=BG_ACCENT, width=5)
        
        # Draw a "fake icon" circle
        icon_r = 60
        icon_cx = card_x + card_w // 2
        icon_cy = card_y + 100
        draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r], fill=BG_HEADER)
        
        # Title
        bbox = draw.textbbox((0, 0), title, font=goal_title_font)
        tw = bbox[2] - bbox[0]
        draw.text((card_x + (card_w - tw)//2, icon_cy + 80), title, font=goal_title_font, fill=BG_HEADER)
        
        # Desc
        # Wrap desc
        draw_wrapped_text_centered(draw, desc, goal_desc_font, card_w - 40, icon_cy + 180, TEXT_DARK)

    current_y = grid_y_start + (2 * row_height) + 50
    
    # --- 6. Footer (Bottom Fill) ---
    footer_h = HEIGHT - current_y
    draw.rectangle([0, current_y, WIDTH, HEIGHT], fill=BG_HEADER)
    
    # QR Code
    qr_size = 500
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    
    # White BG for QR
    qr_bg = Image.new('RGBA', (qr_size + 40, qr_size + 40), WHITE)
    qr_bg.paste(qr, (20, 20), qr)
    
    # Center QR vertically in footer
    qr_y = current_y + (footer_h - qr_bg.height) // 2
    qr_x = 200
    img.paste(qr_bg, (qr_x, qr_y), qr_bg)
    
    # URL and CTA next to QR
    text_x = qr_x + qr_bg.width + 150
    text_y_center = qr_y + qr_bg.height // 2
    
    cta_font = get_font(100, bold=True)
    url_font = get_font(120, bold=True)
    
    draw.text((text_x, text_y_center - 100), "Join Our Mission", font=cta_font, fill=WHITE)
    draw.text((text_x, text_y_center + 20), "tadweer-tech-sy.org", font=url_font, fill=BG_ACCENT)
    
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design v2 saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
