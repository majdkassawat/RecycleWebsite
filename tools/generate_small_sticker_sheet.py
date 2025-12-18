from PIL import Image
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
output_path = os.path.join(images_dir, 'sticker_sheet_a4_small.png')

# A4 Dimensions at 300 DPI
A4_WIDTH = 2480
A4_HEIGHT = 3508
BG_COLOR = (255, 255, 255) # White paper

# Sticker Dimensions
STICKER_SIZE = 354 # 3cm @ 300 DPI

# Grid Configuration
COLS = 6
ROWS = 8

# Load Stickers
try:
    sticker_cw = Image.open(os.path.join(images_dir, 'sticker_small_circle_white.png'))
    sticker_cg = Image.open(os.path.join(images_dir, 'sticker_small_circle_green.png'))
    sticker_sw = Image.open(os.path.join(images_dir, 'sticker_small_square_white.png'))
except FileNotFoundError:
    print("Error: Small stickers not found. Run tools/generate_small_stickers.py first.")
    exit(1)

# Create Canvas
sheet = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), BG_COLOR)

# Calculate Spacing
total_sticker_width = COLS * STICKER_SIZE
remaining_width = A4_WIDTH - total_sticker_width
h_gap = remaining_width // (COLS + 1)

total_sticker_height = ROWS * STICKER_SIZE
remaining_height = A4_HEIGHT - total_sticker_height
v_gap = remaining_height // (ROWS + 1)

# Draw Grid
for row in range(ROWS):
    for col in range(COLS):
        x = h_gap + col * (STICKER_SIZE + h_gap)
        y = v_gap + row * (STICKER_SIZE + v_gap)
        
        # Determine which sticker to use
        # Pattern: CW, CG, SW repeating
        pattern_idx = row % 3
        if pattern_idx == 0:
            sticker = sticker_cw
        elif pattern_idx == 1:
            sticker = sticker_cg
        else:
            sticker = sticker_sw
            
        sheet.paste(sticker, (x, y), sticker)

# Save Sheet
sheet.save(output_path, 'PNG', dpi=(300, 300))
print(f'Sticker sheet created: {output_path}')
