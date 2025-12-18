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
qr_path = os.path.join(images_dir, 'qr_website.png')

# Configuration
WIDTH = 709
HEIGHT = 709
BG_GREEN = (165, 214, 167)
TEXT_GREEN = (27, 94, 32)
WHITE = (255, 255, 255)

SLOGAN = "We give value to your garbage"
TAGLINE = "Today's waste, tomorrow's energy"
JOIN_US = "Join Us"

def get_fonts():
    try:
        return {
            'title': ImageFont.truetype("arialbd.ttf", 45),
            'subtitle': ImageFont.truetype("arial.ttf", 30),
            'small_bold': ImageFont.truetype("arialbd.ttf", 30),
            'slogan_curve': ImageFont.truetype("arialbd.ttf", 35),
            'tagline_curve': ImageFont.truetype("arial.ttf", 25)
        }
    except:
        default = ImageFont.load_default()
        return {k: default for k in ['title', 'subtitle', 'small_bold', 'slogan_curve', 'tagline_curve']}

fonts = get_fonts()

def load_assets():
    logo = Image.open(logo_path).convert('RGBA')
    qr = Image.open(qr_path).convert('RGBA')
    return logo, qr

logo_orig, qr_orig = load_assets()

def save_sticker(img, name):
    path = os.path.join(images_dir, name)
    img.save(path, 'PNG', dpi=(300, 300))
    print(f"Generated {path}")

# --- Variation 1: Square, Green BG, Vertical Stack ---
def generate_square_green():
    img = Image.new('RGBA', (WIDTH, HEIGHT), BG_GREEN)
    draw = ImageDraw.Draw(img)
    
    # Layout: Logo Top, Text Middle, QR Bottom
    
    # 1. Logo
    logo_size = 300
    logo = logo_orig.resize((logo_size, int(logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    img.paste(logo, ((WIDTH - logo.width) // 2, 50), logo)
    
    # 2. Text
    # Slogan
    bbox = draw.textbbox((0, 0), SLOGAN, font=fonts['title'])
    w = bbox[2] - bbox[0]
    # If too wide, split? 709px width. Text might fit.
    # Let's wrap if needed, but for now assume fit or scale down
    draw.text(((WIDTH - w) // 2, 380), SLOGAN, font=fonts['title'], fill=TEXT_GREEN)
    
    # Tagline
    bbox = draw.textbbox((0, 0), TAGLINE, font=fonts['subtitle'])
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, 440), TAGLINE, font=fonts['subtitle'], fill=TEXT_GREEN)
    
    # 3. QR and Join Us
    qr_size = 150
    qr = qr_orig.resize((qr_size, qr_size), Image.LANCZOS)
    
    # Draw "Join Us" above QR
    bbox = draw.textbbox((0, 0), JOIN_US, font=fonts['small_bold'])
    w_join = bbox[2] - bbox[0]
    draw.text(((WIDTH - w_join) // 2, 500), JOIN_US, font=fonts['small_bold'], fill=TEXT_GREEN)
    
    img.paste(qr, ((WIDTH - qr_size) // 2, 540), qr)
    
    save_sticker(img, 'sticker_en_square_green.png')

# --- Variation 2: Square, White BG, Green Border, Modern Layout ---
def generate_square_white():
    img = Image.new('RGBA', (WIDTH, HEIGHT), WHITE)
    draw = ImageDraw.Draw(img)
    
    # Border
    border_width = 20
    draw.rectangle([0, 0, WIDTH-1, HEIGHT-1], outline=BG_GREEN, width=border_width)
    
    # Layout: Logo Top Left, QR Bottom Right, Text filling space
    
    # Logo Top Left
    logo_size = 250
    logo = logo_orig.resize((logo_size, int(logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    img.paste(logo, (50, 50), logo)
    
    # QR Bottom Right
    qr_size = 180
    qr = qr_orig.resize((qr_size, qr_size), Image.LANCZOS)
    img.paste(qr, (WIDTH - qr_size - 50, HEIGHT - qr_size - 50), qr)
    
    # Text
    # Slogan - Large, Top Right aligned? Or centered in remaining space?
    # Let's put Slogan below Logo, left aligned
    draw.text((50, 320), "We give value", font=fonts['title'], fill=TEXT_GREEN)
    draw.text((50, 370), "to your garbage", font=fonts['title'], fill=TEXT_GREEN)
    
    # Tagline
    draw.text((50, 440), TAGLINE, font=fonts['subtitle'], fill=TEXT_GREEN)
    
    # Join Us next to QR
    draw.text((WIDTH - qr_size - 180, HEIGHT - 150), JOIN_US, font=fonts['small_bold'], fill=TEXT_GREEN)
    
    save_sticker(img, 'sticker_en_square_white.png')

# --- Variation 3: Circle, White BG, Green Text (Inverted) ---
def generate_circle_white():
    img = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    
    margin = 10
    circle_radius = (WIDTH // 2) - margin
    center = (WIDTH // 2, HEIGHT // 2)
    
    # White Circle with Green Border
    draw.ellipse(
        [(center[0] - circle_radius, center[1] - circle_radius),
         (center[0] + circle_radius, center[1] + circle_radius)],
        fill=WHITE, outline=BG_GREEN, width=20
    )
    
    # Same layout as original but on white
    # Logo
    max_logo_size = 340
    logo = logo_orig.resize((max_logo_size, int(max_logo_size * logo_orig.height / logo_orig.width)), Image.LANCZOS)
    img.paste(logo, ((WIDTH - logo.width) // 2, (HEIGHT - logo.height) // 2 - 40), logo)
    
    # QR
    qr_size = 135
    qr = qr_orig.resize((qr_size, qr_size), Image.LANCZOS)
    img.paste(qr, ((WIDTH - qr_size) // 2, HEIGHT - 230), qr)
    
    # Join Us
    bbox = draw.textbbox((0, 0), JOIN_US, font=fonts['small_bold'])
    w = bbox[2] - bbox[0]
    draw.text(((WIDTH - w) // 2, HEIGHT - 270), JOIN_US, font=fonts['small_bold'], fill=TEXT_GREEN)
    
    # Curved Text
    text_radius = circle_radius - 30
    draw_text_on_arc(img, SLOGAN, fonts['slogan_curve'], center, text_radius, 270, TEXT_GREEN, is_bottom=False)
    draw_text_on_arc(img, TAGLINE, fonts['tagline_curve'], center, text_radius, 90, TEXT_GREEN, is_bottom=True)
    
    save_sticker(img, 'sticker_en_circle_white.png')

if __name__ == "__main__":
    generate_square_green()
    generate_square_white()
    generate_circle_white()
