from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200.png')

# Dimensions (80cm x 200cm @ 150 DPI)
DPI = 150
WIDTH = int(80 / 2.54 * DPI)   # ~4724 px
HEIGHT = int(200 / 2.54 * DPI) # ~11811 px

# Colors
WHITE = (255, 255, 255)
BG_LIGHT_GREEN = (232, 245, 233) # Very light green for content
BG_DARK_GREEN = (27, 94, 32)     # Footer
TEXT_DARK = (33, 33, 33)
TEXT_WHITE = (255, 255, 255)
ACCENT_GREEN = (76, 175, 80)

# Fonts
def get_font(size, bold=False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

# Helper: Draw Wrapped Text
def draw_wrapped_text(draw, text, font, max_width, start_pos, fill, line_spacing=1.2, align='left'):
    lines = []
    # Split by newlines first
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            lines.append('')
            continue
            
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
    
    x, y = start_pos
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        draw_x = x
        if align == 'center':
            draw_x = x + (max_width - line_width) // 2
        elif align == 'right':
            draw_x = x + (max_width - line_width)
            
        draw.text((draw_x, y), line, font=font, fill=fill)
        y += int(line_height * line_spacing)
        
    return y # Return next Y position

def create_stand():
    print(f"Creating stand design: {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    current_y = 0
    
    # --- 1. Header Section ---
    header_height = int(HEIGHT * 0.15)
    
    # Logo
    logo = Image.open(logo_path).convert('RGBA')
    logo_height = int(header_height * 0.8)
    logo_ratio = logo.width / logo.height
    logo_width = int(logo_height * logo_ratio)
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
    
    # Center Logo
    logo_x = (WIDTH - logo_width) // 2
    logo_y = (header_height - logo_height) // 2
    img.paste(logo, (logo_x, logo_y), logo)
    
    current_y += header_height
    
    # Title & Slogan
    title_font = get_font(180, bold=True)
    slogan_font = get_font(100, bold=False)
    
    title = "Tadweer Tech"
    slogan = "We give value to your garbage"
    
    # Draw Title
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = bbox[2] - bbox[0]
    draw.text(((WIDTH - title_w) // 2, current_y), title, font=title_font, fill=BG_DARK_GREEN)
    current_y += bbox[3] - bbox[1] + 50
    
    # Draw Slogan
    bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
    slogan_w = bbox[2] - bbox[0]
    draw.text(((WIDTH - slogan_w) // 2, current_y), slogan, font=slogan_font, fill=ACCENT_GREEN)
    current_y += bbox[3] - bbox[1] + 100
    
    # --- 2. Hero Image ---
    hero_height = int(HEIGHT * 0.25)
    hero = Image.open(hero_path).convert('RGB')
    # Resize to fit width, crop height if needed
    hero_ratio = hero.width / hero.height
    target_ratio = WIDTH / hero_height
    
    if hero_ratio > target_ratio:
        # Image is wider, crop sides
        new_height = hero_height
        new_width = int(new_height * hero_ratio)
        hero = hero.resize((new_width, new_height), Image.LANCZOS)
        crop_x = (new_width - WIDTH) // 2
        hero = hero.crop((crop_x, 0, crop_x + WIDTH, new_height))
    else:
        # Image is taller, crop top/bottom
        new_width = WIDTH
        new_height = int(new_width / hero_ratio)
        hero = hero.resize((new_width, new_height), Image.LANCZOS)
        crop_y = (new_height - hero_height) // 2
        hero = hero.crop((0, crop_y, WIDTH, crop_y + hero_height))
        
    img.paste(hero, (0, current_y))
    current_y += hero_height
    
    # --- 3. Content Section ---
    # Background for content
    content_start_y = current_y
    footer_height = int(HEIGHT * 0.15)
    content_height = HEIGHT - content_start_y - footer_height
    
    draw.rectangle([0, content_start_y, WIDTH, content_start_y + content_height], fill=BG_LIGHT_GREEN)
    
    padding = 150
    content_width = WIDTH - (padding * 2)
    current_y += 100
    
    # About Us
    h2_font = get_font(120, bold=True)
    p_font = get_font(80, bold=False)
    
    draw.text((padding, current_y), "About Us", font=h2_font, fill=BG_DARK_GREEN)
    current_y += 150
    
    about_text = "We are an initiative aiming to find solutions to the waste problem and minimize its harm to the Syrian environment. We work on utilizing and recycling waste to generate energy and create a sustainable future."
    current_y = draw_wrapped_text(draw, about_text, p_font, content_width, (padding, current_y), TEXT_DARK, line_spacing=1.3)
    
    current_y += 150
    
    # Our Goals
    draw.text((padding, current_y), "Our Goals", font=h2_font, fill=BG_DARK_GREEN)
    current_y += 150
    
    goals = [
        "Utilizing and recycling waste for energy generation.",
        "Developing comprehensive waste-management plans.",
        "Advocating for legal regulations for a better environment.",
        "Raising awareness to change collective behaviors.",
        "Ensuring environmental security for society."
    ]
    
    bullet_font = get_font(70, bold=False)
    bullet_radius = 15
    
    for goal in goals:
        # Draw bullet
        bullet_y = current_y + 30
        draw.ellipse([padding, bullet_y, padding + bullet_radius*2, bullet_y + bullet_radius*2], fill=ACCENT_GREEN)
        
        # Draw text
        text_x = padding + 80
        current_y = draw_wrapped_text(draw, goal, bullet_font, content_width - 80, (text_x, current_y), TEXT_DARK)
        current_y += 40 # Spacing between items
        
    # --- 4. Footer Section ---
    footer_y = HEIGHT - footer_height
    draw.rectangle([0, footer_y, WIDTH, HEIGHT], fill=BG_DARK_GREEN)
    
    # QR Code
    qr_size = int(footer_height * 0.7)
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    
    # Add white background to QR
    qr_bg_size = qr_size + 40
    qr_bg = Image.new('RGBA', (qr_bg_size, qr_bg_size), WHITE)
    qr_bg.paste(qr, (20, 20), qr)
    
    qr_y = footer_y + (footer_height - qr_bg_size) // 2
    qr_x = padding
    img.paste(qr_bg, (qr_x, qr_y), qr_bg)
    
    # Contact Info
    contact_x = qr_x + qr_bg_size + 100
    contact_y = footer_y + 150
    
    contact_font = get_font(90, bold=True)
    url_font = get_font(100, bold=True)
    
    draw.text((contact_x, contact_y), "Join us in building a greener future!", font=contact_font, fill=WHITE)
    contact_y += 150
    draw.text((contact_x, contact_y), "tadweer-tech-sy.org", font=url_font, fill=ACCENT_GREEN)
    
    # Save
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
