from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import random
import arabic_reshaper
from bidi.algorithm import get_display

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')
hero_path = os.path.join(images_dir, 'tadweer_image.jpeg')
qr_path = os.path.join(images_dir, 'qr_website.png')
output_path = os.path.join(images_dir, 'stand_design_80x200_v9_ar.png')

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

# Helper for Arabic Text
def process_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# Fonts
def get_font(size, bold=False):
    try:
        font_name = "arialbd.ttf" if bold else "arial.ttf"
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def draw_centered_text(draw, text, font, y, fill, width=WIDTH):
    text = process_text(text)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    x = (width - text_w) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def draw_wrapped_text(draw, text, font, max_width, start_x, start_y, fill, line_spacing=1.3, align="right"):
    # For Arabic, we split by words, but we need to be careful with reshaping.
    # We reshape AFTER wrapping lines.
    
    lines = []
    paragraphs = text.split('\n')
    
    for paragraph in paragraphs:
        words = paragraph.split()
        if not words: continue
        
        # RTL logic for wrapping:
        # We build lines logically (first word is first read), then reshape the whole line.
        current_line = words[0]
        for word in words[1:]:
            test_line = current_line + " " + word
            # Check width with reshaped text to be accurate
            reshaped_test = process_text(test_line)
            bbox = draw.textbbox((0, 0), reshaped_test, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    
    y = start_y
    for line in lines:
        display_line = process_text(line)
        bbox = draw.textbbox((0, 0), display_line, font=font)
        line_width = bbox[2] - bbox[0]
        line_height = bbox[3] - bbox[1]
        
        if align == "center":
            draw_x = start_x + (max_width - line_width) // 2
        elif align == "right":
            draw_x = start_x + max_width - line_width
        else: # left
            draw_x = start_x
            
        draw.text((draw_x, y), display_line, font=font, fill=fill)
        y += int(line_height * line_spacing)
    return y

def draw_background_pattern(img):
    pattern = Image.new('RGBA', img.size, (0,0,0,0))
    draw = ImageDraw.Draw(pattern)
    
    # Draw large faint circles
    for _ in range(35):
        r = random.randint(500, 1200)
        x = random.randint(-200, WIDTH + 200)
        y = random.randint(int(HEIGHT*0.1), int(HEIGHT*0.9))
        color = BG_ACCENT_LIGHT + (60,) 
        draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
        
    img.paste(pattern, (0,0), pattern)

def create_stand():
    print(f"Creating stand design v9 (Arabic): {WIDTH}x{HEIGHT} pixels...")
    img = Image.new('RGB', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # --- 1. Header Section ---
    header_height = int(HEIGHT * 0.10)
    
    # Logo (Left side for Arabic? Or Right? Usually logos stay or flip. Let's keep logo on Left for balance if text is Right, or flip it.
    # Standard: Logo Top Right or Top Left. Let's put Logo Top Right for Arabic as it's the start reading position, or keep it consistent.
    # Let's put Logo on the RIGHT for Arabic.
    logo = Image.open(logo_path).convert('RGBA')
    logo_h = int(header_height * 0.9)
    logo_ratio = logo.width / logo.height
    logo_w = int(logo_h * logo_ratio)
    logo = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo, (WIDTH - SIDE_MARGIN - logo_w, int(header_height * 0.05)), logo)
    
    # Title (Left side)
    title_font = get_font(200, bold=True)
    title_text = "تدوير تك"
    title_display = process_text(title_text)
    bbox = draw.textbbox((0, 0), title_display, font=title_font)
    title_w = bbox[2] - bbox[0]
    title_h = bbox[3] - bbox[1]
    # Draw on Left
    draw.text((SIDE_MARGIN, (header_height - title_h)//2), title_display, font=title_font, fill=BG_DARK)
    
    current_y = header_height
    
    # --- 2. Hero Section ---
    hero_height = int(HEIGHT * 0.16)
    
    # Diagonal Mask (Flip direction for variety? Or keep same. Let's keep same)
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
    
    # Slogan Overlay (Right aligned)
    slogan_font = get_font(200, bold=True)
    slogan_text = "نمنح نفاياتك قيمة"
    slogan_display = process_text(slogan_text)
    
    # Calculate position for Right alignment
    bbox = draw.textbbox((0, 0), slogan_display, font=slogan_font)
    s_w = bbox[2] - bbox[0]
    
    text_x = WIDTH - SIDE_MARGIN - s_w - 50
    text_y = current_y + 60
    
    draw.text((text_x + 10, text_y + 10), slogan_display, font=slogan_font, fill=(0,0,0))
    draw.text((text_x, text_y), slogan_display, font=slogan_font, fill=WHITE)
    
    current_y += hero_height
    
    # --- 3. Body Background & Pattern ---
    body_start_y = current_y - slant_h
    draw.rectangle([0, body_start_y + slant_h, WIDTH, HEIGHT], fill=BG_LIGHT)
    draw.polygon([(0, current_y), (WIDTH, current_y - slant_h), (WIDTH, current_y), (0, current_y)], fill=BG_LIGHT)
    
    draw_background_pattern(img)
    draw = ImageDraw.Draw(img) 
    
    content_y = current_y + 120
    
    # --- 4. Vision & Mission ---
    
    # Vision
    section_title_font = get_font(180, bold=True)
    body_text_font = get_font(135, bold=False)
    
    draw_centered_text(draw, "رؤيتنا", section_title_font, content_y, BG_DARK)
    content_y += 220
    
    vision_text = "عالم تُقلَّل فيه النفايات إلى الحد الأدنى، وتصبح كل مادة قابلة لإعادة التدوير، وتزدهر فيه المجتمعات في انسجام مع الطبيعة. نتصور حركة عالمية يصبح فيها الاستهلاك المسؤول وإعادة التدوير أسلوب حياة."
    content_y = draw_wrapped_text(draw, vision_text, body_text_font, WIDTH - (SIDE_MARGIN*2), SIDE_MARGIN, content_y, TEXT_MAIN, align="center", line_spacing=1.8)
    
    content_y += 300
    
    # Mission
    draw_centered_text(draw, "رسالتنا", section_title_font, content_y, BG_DARK)
    content_y += 220
    
    mission_text = "تعزيز مستقبل مستدام من خلال تشجيع قابلية إعادة التدوير وتقليل النفايات عبر التعليم والابتكار والمشاركة المجتمعية. نتعاون مع الأفراد والشركات والحكومات لاعتناق ممارسات صديقة للبيئة."
    content_y = draw_wrapped_text(draw, mission_text, body_text_font, WIDTH - (SIDE_MARGIN*2), SIDE_MARGIN, content_y, TEXT_MAIN, align="center", line_spacing=1.8)
    
    content_y += 300
    
    # --- 5. Our Goals (List) ---
    draw_centered_text(draw, "أهدافنا", section_title_font, content_y, BG_DARK)
    content_y += 220
    
    goals = [
        "الاستفادة من النفايات وإعادة تدويرها وتوليد الطاقة منها.",
        "العمل مع الجهات المسؤولة لوضع خطة شاملة لإدارة النفايات.",
        "الضغط على صناع القرار لسن تشريعات قانونية لبيئة أفضل.",
        "تغيير السلوكيات الجماعية من خلال ورش العمل التوعوية.",
        "ضمان الأمن البيئي لجميع أفراد المجتمع."
    ]
    
    goal_font = get_font(135, bold=False)
    bullet_r = 25
    
    for goal in goals:
        # Bullet on Right
        bullet_x = WIDTH - SIDE_MARGIN - 50 - (bullet_r*2)
        draw.ellipse([bullet_x, content_y + 50, bullet_x + bullet_r*2, content_y + 50 + bullet_r*2], fill=BG_ACCENT)
        
        # Text on Left of Bullet
        # Calculate max width for text
        text_max_w = bullet_x - SIDE_MARGIN - 50
        
        # We use draw_wrapped_text with align='right' and start_x = SIDE_MARGIN
        # The function calculates right alignment based on start_x + max_width
        
        # But wait, draw_wrapped_text returns new Y. We need to handle single line or wrapped.
        # Let's use the function.
        
        draw_wrapped_text(draw, goal, goal_font, text_max_w, SIDE_MARGIN, content_y, TEXT_MAIN, align="right", line_spacing=1.3)
        
        content_y += 280
        
    content_y += 200
    
    # --- 6. Core Values (Grid) ---
    values_bg_h = 1600
    draw.rectangle([0, content_y, WIDTH, content_y + values_bg_h], fill=BG_ACCENT_LIGHT)
    
    val_y = content_y + 120
    draw_centered_text(draw, "قيمنا الجوهرية", section_title_font, val_y, BG_DARK)
    val_y += 300
    
    values = [
        "الاستدامة", "النزاهة", "الاحترام", "المهنية",
        "السلامة", "مكافحة التمييز", "المجتمع", "التحسين"
    ]
    
    val_font = get_font(130, bold=True)
    
    cols = 2
    rows = 4
    col_w = WIDTH // cols
    row_h = 320
    
    start_val_y = val_y
    
    for i, val in enumerate(values):
        # RTL Grid: Index 0 is Top Right, Index 1 is Top Left
        r = i // cols
        c = i % cols
        
        # If c=0 (first col), it should be on Right. c=1 on Left.
        # Standard grid logic: x = c * col_w.
        # If we want RTL filling:
        # 0 -> Right Col, 1 -> Left Col
        # So if c=0, x should be second half? No.
        # Let's just place them.
        # c=0: Left side in standard math.
        # c=1: Right side.
        # We want 0 to be Right. So invert column index.
        c_rtl = (cols - 1) - c
        
        cx = c_rtl * col_w + (col_w // 2)
        cy = start_val_y + (r * row_h)
        
        val_display = process_text(val)
        
        # Checkmark icon
        # Icon to the Right of text? Or Left?
        # Usually Icon Right, Text Left in RTL lists.
        # But centered?
        # Let's put Icon above or next to it.
        # Let's do: [Icon] [Text] (Right to Left)
        
        # Calculate total width
        check_font = get_font(120, True)
        check_text = "✓"
        
        bbox_v = draw.textbbox((0,0), val_display, font=val_font)
        w_v = bbox_v[2] - bbox_v[0]
        
        bbox_c = draw.textbbox((0,0), check_text, font=check_font)
        w_c = bbox_c[2] - bbox_c[0]
        
        gap = 40
        total_w = w_v + gap + w_c
        
        start_x = cx - (total_w // 2)
        
        # Draw Check (Rightmost)
        draw.text((start_x + w_v + gap, cy), check_text, font=check_font, fill=BG_DARK)
        
        # Draw Text (Left of Check)
        draw.text((start_x, cy), val_display, font=val_font, fill=BG_DARK)

    content_y += values_bg_h + 50

    # --- 7. Footer ---
    footer_height = 900 + BOTTOM_MARGIN
    footer_y = HEIGHT - footer_height
    
    if content_y > footer_y:
        footer_y = content_y + 50
        
    curve_h = 150
    draw.rectangle([0, footer_y + curve_h, WIDTH, HEIGHT], fill=BG_DARK)
    draw.ellipse([-WIDTH*0.1, footer_y, WIDTH*1.1, footer_y + curve_h*2], fill=BG_DARK)
    
    footer_content_y = footer_y + 250
    
    # QR Code
    qr_size = 650
    qr = Image.open(qr_path).convert('RGBA')
    qr = qr.resize((qr_size, qr_size), Image.LANCZOS)
    qr_bg = Image.new('RGBA', (qr_size + 50, qr_size + 50), WHITE)
    qr_bg.paste(qr, (25, 25), qr)
    img.paste(qr_bg, ((WIDTH - qr_bg.width)//2, footer_content_y), qr_bg)
    
    # URL
    url_y = footer_content_y + qr_bg.height + 100
    url_font = get_font(150, bold=True)
    draw_centered_text(draw, "tadweer-tech-sy.org", url_font, url_y, WHITE)
    
    # Social
    social_y = url_y + 180
    social_font = get_font(120, bold=False)
    draw_centered_text(draw, "@tadweer_sy | Tadweer Tech", social_font, social_y, BG_ACCENT)
    
    img.save(output_path, 'PNG', dpi=(DPI, DPI))
    print(f"Stand design v9 (Arabic) saved to: {output_path}")

if __name__ == "__main__":
    create_stand()
