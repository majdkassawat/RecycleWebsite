from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Add current directory to path to import sticker_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sticker_utils import draw_text_on_arc

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
logo_path = os.path.join(images_dir, 'logo_circular.png')

# Configuration
# 3x3 cm at 300 DPI = 354x354 pixels
WIDTH = 354
HEIGHT = 354
BG_GREEN = (165, 214, 167)
TEXT_GREEN = (27, 94, 32)
WHITE = (255, 255, 255)

WEBSITE_URL = "tadweer-tech-sy.org"

def get_fonts():
    try:
        return {
            'url_curve': ImageFont.truetype("arialbd.ttf", 24),
            'url_straight': ImageFont.truetype("arialbd.ttf", 28),
        }
    except:
        default = ImageFont.load_default()
        return {k: default for k in ['url_curve', 'url_straight']}

fonts = get_fonts()

def load_logo():
    return Image.open(logo_path).convert('RGBA')

logo_orig = load_logo()

def save_sticker(img, name):
    path = os.path.join(images_dir, name)
    img.save(path, 'PNG', dpi=(300, 300))
    print(f"Generated {path}")

# --- Variation 1: Small Circle White ---
def generate_small_circle_white():
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    margin = 5
    circle_radius = (WIDTH // 2) - margin
    center = (WIDTH // 2, HEIGHT // 2)
    
    # White Circle with Green Border
    draw.ellipse(
        [(center[0] - circle_radius, center[1] - circle_radius),
         (center[0] + circle_radius, center[1] + circle_radius)],
        fill=WHITE, outline=BG_GREEN, width=10
    )
    
    # Logo
    # Maximize logo size, leaving room for text at bottom
    logo_size = 200
    logo = logo_orig.resize((logo_size, int(logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    # Center horizontally, push up slightly
    img.paste(logo, ((WIDTH - logo.width) // 2, 40), logo)
    
    # Curved URL at bottom
    text_radius = circle_radius - 15
    draw_text_on_arc(img, WEBSITE_URL, fonts['url_curve'], center, text_radius, 90, TEXT_GREEN, is_bottom=True)
    
    save_sticker(img, 'sticker_small_circle_white.png')

# --- Variation 2: Small Circle Green ---
def generate_small_circle_green():
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    margin = 5
    circle_radius = (WIDTH // 2) - margin
    center = (WIDTH // 2, HEIGHT // 2)
    
    # Green Circle
    draw.ellipse(
        [(center[0] - circle_radius, center[1] - circle_radius),
         (center[0] + circle_radius, center[1] + circle_radius)],
        fill=BG_GREEN
    )
    
    # Logo
    logo_size = 200
    logo = logo_orig.resize((logo_size, int(logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    img.paste(logo, ((WIDTH - logo.width) // 2, 40), logo)
    
    # Curved URL at bottom (Dark Green Text for contrast on Light Green BG)
    text_radius = circle_radius - 15
    draw_text_on_arc(img, WEBSITE_URL, fonts['url_curve'], center, text_radius, 90, TEXT_GREEN, is_bottom=True)
    
    save_sticker(img, 'sticker_small_circle_green.png')

# --- Variation 3: Small Square White ---
def generate_small_square_white():
    img = Image.new('RGBA', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=BG_GREEN, width=10)
    
    # Logo
    logo_size = 220
    logo = logo_orig.resize((logo_size, int(logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    img.paste(logo, ((WIDTH - logo.width) // 2, 30), logo)
    
    # URL at bottom
    bbox = draw.textbbox((0, 0), WEBSITE_URL, font=fonts['url_straight'])
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, 280), WEBSITE_URL, font=fonts['url_straight'], fill=TEXT_GREEN)
    
    save_sticker(img, 'sticker_small_square_white.png')

if __name__ == "__main__":
    generate_small_circle_white()
    generate_small_circle_green()
    generate_small_square_white()
