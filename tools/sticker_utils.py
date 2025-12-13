from PIL import Image, ImageDraw, ImageFont
import math

def draw_text_on_arc(img, text, font, center, radius, start_angle, text_color, is_bottom=False):
    """
    Draws text along an arc.
    start_angle: Angle in degrees where the text should be centered (e.g. 270 for top, 90 for bottom).
    is_bottom: If True, text is drawn for the bottom of the circle (readable, smile curve).
    """
    draw = ImageDraw.Draw(img)
    
    # Calculate total width of text
    total_width = 0
    char_widths = []
    for char in text:
        w = font.getlength(char)
        char_widths.append(w)
        total_width += w
    
    # Circumference at this radius
    circumference = 2 * math.pi * radius
    
    # Total angle covered by text
    total_angle = (total_width / circumference) * 360
    
    # Starting angle
    # For Top (is_bottom=False): Text flows Clockwise (LTR). 
    # We want to center it at start_angle (e.g. 270).
    # So start at 270 - total_angle/2.
    
    # For Bottom (is_bottom=True): Text flows Counter-Clockwise (LTR visual).
    # We want to center it at start_angle (e.g. 90).
    # But we draw characters LTR.
    # To make it readable (smile), the first character is at the LEFT (higher angle) 
    # and last character is at the RIGHT (lower angle).
    # e.g. "ABC". A is at 120 deg, B at 90, C at 60.
    # So we start at start_angle + total_angle/2 and decrement.
    
    if is_bottom:
        current_angle = start_angle + (total_angle / 2)
    else:
        current_angle = start_angle - (total_angle / 2)
        
    for i, char in enumerate(text):
        w = char_widths[i]
        char_angle_span = (w / circumference) * 360
        
        if is_bottom:
            # For bottom, we go backwards in angle
            # Center of char
            mid_angle = current_angle - (char_angle_span / 2)
            current_angle -= char_angle_span
        else:
            # For top, we go forwards
            mid_angle = current_angle + (char_angle_span / 2)
            current_angle += char_angle_span
            
        # Position
        # 0 deg = Right, 90 = Down, 270 = Up
        rad = math.radians(mid_angle)
        x = center[0] + radius * math.cos(rad)
        y = center[1] + radius * math.sin(rad)
        
        # Rotation
        # We want the character to be upright relative to the circle center.
        # Top: At 270, char is upright (0 rot). 
        # Tangent is horizontal. Normal is vertical.
        # PIL rotate: Counter-Clockwise.
        # If we draw char upright, we need to rotate it.
        # At 270: Rotation should be 0 (if we account for the +90 offset).
        # Let's say we want the "up" vector of the char to point to center (or away?).
        # Top text: "Up" points away from center.
        # Bottom text: "Up" points to center.
        
        if is_bottom:
            # Bottom text (smile). Up points to center.
            # At 90 deg (bottom), char should be upright (0 rot).
            # At 180 deg (left), char should be rotated -90 (or 270).
            # Formula: rotation = mid_angle - 90?
            # Test: 90 -> 0. 180 -> 90. 0 -> -90.
            # Wait, PIL rotate is CCW.
            # If I want to rotate 90 deg CCW (to left), I pass 90.
            # At 180 (left side of circle), bottom text "A" should be tilted right?
            # Imagine "Made In". "M" is at left. Top of M points to center.
            # So M is rotated 90 deg CW? (-90).
            # Formula: mid_angle + 90?
            # Test: 90 -> 180 (Upside down). No.
            # Test: 90 -> 0.
            # We need rotation such that at 90, it is 0.
            # rotation = -mid_angle + 90?
            # At 90: -90 + 90 = 0.
            # At 180: -180 + 90 = -90 (CW rotation). Correct.
            rotation = -mid_angle + 90
        else:
            # Top text (rainbow). Up points away from center.
            # At 270 (top), char is upright (0 rot).
            # At 180 (left), char is rotated -90 (CW).
            # Formula: rotation = -mid_angle + 270?
            # Test: 270 -> 0.
            # Test: 180 -> 90 (CCW).
            # Wait, at 180 (left), top text "W" should be tilted left (CCW)?
            # Imagine "We". "W" is at left. Top of W points away.
            # So W is rotated -90 (CW).
            # So at 180, we want -90.
            # -180 + 270 = 90. Incorrect.
            # -mid_angle - 90?
            # At 270: -270 - 90 = -360 = 0.
            # At 180: -180 - 90 = -270 = 90 (CCW).
            # Let's visualize.
            # Circle. Top (270). Text "ABC".
            # B at 270. Upright.
            # A at 260. Tilted slightly left (CCW).
            # C at 280. Tilted slightly right (CW).
            # So as angle increases (260->280), rotation decreases (positive -> negative).
            # So rotation is proportional to -angle.
            # At 270, rot = 0.
            # rot = 270 - angle.
            # Test: 260 -> 10 (CCW). Correct.
            # Test: 280 -> -10 (CW). Correct.
            rotation = 270 - mid_angle

        # Create char image
        # Make it large enough
        char_img_size = int(font.size * 2)
        char_img = Image.new('RGBA', (char_img_size, char_img_size), (0,0,0,0))
        char_draw = ImageDraw.Draw(char_img)
        
        # Draw char centered
        # getbbox might be better to center exactly
        bbox = font.getbbox(char)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        # Offset to center
        # We want the baseline to be at the center? Or the middle of the char?
        # Usually baseline on the radius.
        # If radius is the baseline, we draw text at (width/2, height/2 - ascent?)
        # Let's just center it for now.
        
        char_draw.text(((char_img_size - cw)/2 - bbox[0], (char_img_size - ch)/2 - bbox[1]), char, font=font, fill=text_color)
        
        # Rotate
        rotated_char = char_img.rotate(rotation, resample=Image.BICUBIC, expand=True)
        
        # Paste
        # (x,y) is the position on the circle.
        # If we want the text ON the line, we should offset by half height?
        # Or if radius is the baseline.
        # Let's assume radius is the center of the text height for simplicity, or adjust radius.
        
        px = int(x - rotated_char.width / 2)
        py = int(y - rotated_char.height / 2)
        
        img.paste(rotated_char, (px, py), rotated_char)

