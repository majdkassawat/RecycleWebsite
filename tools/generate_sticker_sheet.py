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
output_path_variations = os.path.join(images_dir, 'sticker_sheet_a4_variations.png')

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

# Load Variations
try:
    sticker_sq_green = Image.open(os.path.join(images_dir, 'sticker_en_square_green.png'))
    sticker_sq_white = Image.open(os.path.join(images_dir, 'sticker_en_square_white.png'))
    sticker_ci_white = Image.open(os.path.join(images_dir, 'sticker_en_circle_white.png'))
except FileNotFoundError:
    print("Warning: Variation stickers not found. Run tools/generate_variations.py first.")
    sticker_sq_green = sticker_en
    sticker_sq_white = sticker_en
    sticker_ci_white = sticker_en

# Load Small Stickers
try:
    sticker_small_cw = Image.open(os.path.join(images_dir, 'sticker_small_circle_white.png'))
    sticker_small_cg = Image.open(os.path.join(images_dir, 'sticker_small_circle_green.png'))
    sticker_small_sw = Image.open(os.path.join(images_dir, 'sticker_small_square_white.png'))
    small_stickers = [sticker_small_cw, sticker_small_cg, sticker_small_sw]
except FileNotFoundError:
    print("Warning: Small stickers not found. Run tools/generate_small_stickers.py first.")
    small_stickers = []

def create_sheet(mode='mixed'):
    # Create Canvas
    sheet = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), BG_COLOR)
    
    if mode == 'mixed_sizes':
        # Custom layout for Mixed Sizes (Small English + Large Arabic)
        # Rows: Small, Small, Large(Ar), Small, Small, Large(Ar)
        row_types = ['small', 'small', 'large_ar', 'small', 'small', 'large_ar']
        
        # Calculate Gaps
        # Heights: Small=354, Large=709
        # Total Content Height = (4 * 354) + (2 * 709) = 1416 + 1418 = 2834
        # Remaining = 3508 - 2834 = 674
        # Gaps = 7 (Top, Bottom, and 5 between rows)
        v_gap = 674 // 7
        
        current_y = v_gap
        
        small_idx = 0
        
        for r_type in row_types:
            if r_type == 'small':
                # 6 Columns
                # Width = 6 * 354 = 2124
                # Remaining = 2480 - 2124 = 356
                # Gaps = 7
                h_gap = 356 // 7
                
                for c in range(6):
                    x = h_gap + c * (354 + h_gap)
                    sticker = small_stickers[small_idx % 3]
                    sheet.paste(sticker, (x, current_y), sticker)
                    small_idx += 1
                
                current_y += 354 + v_gap
                
            elif r_type == 'large_ar':
                # 3 Columns
                # Width = 3 * 709 = 2127
                # Remaining = 2480 - 2127 = 353
                # Gaps = 4
                h_gap = 353 // 4
                
                for c in range(3):
                    x = h_gap + c * (709 + h_gap)
                    sheet.paste(sticker_ar, (x, current_y), sticker_ar)
                    
                current_y += 709 + v_gap
                
        return sheet

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
            elif mode == 'variations':
                # Row 0: Original Circle Green
                # Row 1: Circle White
                # Row 2: Square Green
                # Row 3: Square White
                if row == 0:
                    sticker = sticker_en
                elif row == 1:
                    sticker = sticker_ci_white
                elif row == 2:
                    sticker = sticker_sq_green
                else:
                    sticker = sticker_sq_white
                
            sheet.paste(sticker, (x, y), sticker)
            
    return sheet

# Generate Mixed Sizes
if small_stickers:
    output_path_mixed_sizes = os.path.join(images_dir, 'sticker_sheet_a4_mixed_sizes.png')
    sheet_mixed_sizes = create_sheet('mixed_sizes')
    sheet_mixed_sizes.save(output_path_mixed_sizes, 'PNG', dpi=(300, 300))
    print(f'Sticker sheet created: {output_path_mixed_sizes}')

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

# Generate Variations
sheet_vars = create_sheet('variations')
sheet_vars.save(output_path_variations, 'PNG', dpi=(300, 300))
print(f'Sticker sheet created: {output_path_variations}')
