# Tadweer Tech Website - Copilot Instructions

## Project Overview
Static multilingual website for **Tadweer Tech**, a Syrian recycling/environmental initiative. Hosted on GitHub Pages at `tadweer-tech-sy.org`.

## Architecture

### File Structure Pattern
- **Main pages**: `index.html`, `events.html` (English base)
- **Translations**: Suffix pattern `{page}_{lang}.html` → `index_ar.html`, `index_de.html`, `index_es.html`, `index_tr.html`
- **Shared assets**: Single `styles.css` and `script.js` serve all pages
- **Images**: All in `images/` - logo, event photos, QR codes, generated stickers/stands
- **Tools**: Python scripts in `tools/` for generating print materials (stickers, stands)

### Multilingual Support
- **5 languages**: EN (base), AR (Arabic), ES, DE, TR
- **Arabic pages** use `<html lang="ar" dir="rtl">` - requires RTL-specific CSS rules
- **RTL styles** in `styles.css` use `[dir="rtl"]` selector (see lines 127-156)
- **Language switcher** in nav uses `.lang-switch` class with `.active` on current language
- When adding content, **always update all 5 language versions** of a page

### CSS Variables (styles.css)
```css
--primary-color: #2e7d32;   /* Green */
--secondary-color: #0288d1; /* Blue */
--accent-color: #81c784;    /* Light Green */
```

## Key Patterns

### Page Sections
Each index page follows this section order with consistent IDs:
1. `#home` - Hero section
2. `#about` - About Us with team cards
3. `#mission` - Mission & Vision cards
4. `#conduct` - Code of Conduct grid
5. `#volunteer` - Volunteer CTA with Google Form link
6. `#contact` - Contact info and social links

### Animation Library
Uses **AOS (Animate On Scroll)** - elements get `data-aos="fade-up"` etc. attributes.
AOS is initialized in `script.js` with `duration: 1000, once: true`.

### Events Pages
- Image slider implemented in `script.js` (`initEventsSlider`)
- Slides use `.slide.active` pattern for visibility
- Dots navigation with `.dot.active` state

## Tools Directory

### Python Print Material Generators
All scripts in `tools/` use **Pillow (PIL)** for image generation:
- `generate_sticker.py`, `generate_sticker_ar.py` - Circular stickers with curved text
- `generate_stand_v*.py` - Roll-up stand designs (80x200cm at 300 DPI)
- `sticker_utils.py` - Shared `draw_text_on_arc()` function for curved text

**Print dimensions**: Scripts calculate pixels from cm at 300 DPI (e.g., 6cm = 709px)

### QR Code Generation
`tools/gen_qr.ps1` downloads QR codes from `api.qrserver.com` for:
- Website: `tadweer-tech-sy.org`
- Instagram: `@tadweer_sy`
- Facebook profile

## Workflow

### Common Tasks (via VS Code tasks.json)
- `git_stage_commit_push_simple` - Quick commit with "update" message
- `run_gen_qr` - Regenerate QR code images
- `extract_resources` - Run Python extraction script

### Adding New Content
1. Edit English version first (`index.html` or `events.html`)
2. Copy changes to all language variants (`_ar`, `_de`, `_es`, `_tr`)
3. Translate text content appropriately
4. For Arabic: ensure RTL layout works, test hero/card layouts

### External Dependencies
- **AOS**: `unpkg.com/aos@2.3.1`
- **Font Awesome**: `cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0`
- **Google Forms**: Volunteer application form (external link)
