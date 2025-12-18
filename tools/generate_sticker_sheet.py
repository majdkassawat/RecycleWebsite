from PIL import Image, ImageDraw
import os

# Paths
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
images_dir = os.path.join(root, 'images')
sticker_en_path = os.path.join(images_dir, 'tadweer_sticker.png')
sticker_ar_path = os.path.join(images_dir, 'tadweer_sticker_ar.png')
output_path_mixed = os.path.join(images_dir, 'sticker_sheet_a4_mixed.png')
output_path_en = os.path.join(images_dir, 'sticker_sheet_a4_en.png')
output_path_ar = os.path.join(images_dir, 'sticker_sheet_a4_ar.png')

# A4 Dimensions at 300 DPI
A4_WIDTH = 2480
A4_HEIGHT = 3508
BG_COLOR = (255, 255, 255) # White paper

# Sticker Dimensions
STICKER_SIZE = 709 # 6cm @ 300 DPI

# Grid Configuration
COLS = 3
ROWS = 4

# Load Stickers
sticker_en = Image.open(sticker_en_path)
sticker_ar = Image.open(sticker_ar_path)

def create_sheet(mode='mixed'):
    # Create Canvas
    sheet = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), BG_COLOR)
    
    # Calculate Spacing
    total_sticker_width = COLS * STICKER_SIZE
    remaining_width = A4_WIDTH - total_sticker_width
    h_gap = remaining_width // (COLS + 1)

    total_sticker_height = ROWS * STICKER_SIZE
    remaining_height = A4_HEIGHT - total_sticker_height
    v_gap = remaining_height // (ROWS + 1)

    for row in range(ROWS):
        for col in range(COLS):
            x = h_gap + col * (STICKER_SIZE + h_gap)
            y = v_gap + row * (STICKER_SIZE + v_gap)
            
            if mode == 'mixed':
                # Alternate rows
                if row % 2 == 0:
                    sticker = sticker_en
                else:
                    sticker = sticker_ar
            elif mode == 'en':
                sticker = sticker_en
            elif mode == 'ar':
                sticker = sticker_ar
                
            sheet.paste(sticker, (x, y), sticker)
            
    return sheet

# Generate Mixed
sheet_mixed = create_sheet('mixed')
sheet_mixed.save(output_path_mixed, 'PNG', dpi=(300, 300))
print(f'Sticker sheet created: {output_path_mixed}')

# Generate English
sheet_en = create_sheet('en')
sheet_en.save(output_path_en, 'PNG', dpi=(300, 300))
print(f'Sticker sheet created: {output_path_en}')

# Generate Arabic
sheet_ar = create_sheet('ar')
sheet_ar.save(output_path_ar, 'PNG', dpi=(300, 300))
print(f'Sticker sheet created: {output_path_ar}')
