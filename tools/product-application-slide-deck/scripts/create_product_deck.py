#!/usr/bin/env python3
"""
Template script for creating product application slide decks.

Usage:
    python3 create_product_deck.py --screenshots /path/to/screenshots/ --output presentation.pptx

This script demonstrates the structure for building a 15-slide product application deck
with real screenshots, speaker notes, and highlight animations.
"""

import argparse
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.enum.shapes import MSO_SHAPE
    from PIL import Image
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False
    # Define dummy classes for type checking when dependencies are missing
    class RGBColor:
        def __init__(self, r, g, b):
            pass
    class MSO_SHAPE:
        RECTANGLE = 1


# Color palette - only defined when dependencies are available
if HAS_DEPS:
    WHITE = RGBColor(255, 255, 255)
    NAVY = RGBColor(24, 55, 91)
    BLUE = RGBColor(0, 102, 204)
    TEXT = RGBColor(45, 55, 65)
    MUTED = RGBColor(100, 110, 120)
    BORDER = RGBColor(210, 220, 230)
    PALE = RGBColor(242, 247, 252)
    GOLD = RGBColor(211, 153, 42)
    GREEN = RGBColor(37, 139, 93)
    RED = RGBColor(220, 50, 50)
else:
    # Dummy values for when dependencies are missing
    WHITE = NAVY = BLUE = TEXT = MUTED = BORDER = PALE = GOLD = GREEN = RED = None


def add_header(slide, section, n, logos):
    """Add standard header with logos and section title."""
    # Top accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, slide.slide_width, Pt(4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    # Logos
    if 'dhsp' in logos:
        slide.shapes.add_picture(logos['dhsp'], Inches(0.42), Inches(0.17),
                                width=Inches(0.58), height=Inches(0.58))
    if 'thpt' in logos:
        slide.shapes.add_picture(logos['thpt'], Inches(1.12), Inches(0.17),
                                width=Inches(0.58), height=Inches(0.58))

    # School names
    tx = slide.shapes.add_textbox(Inches(1.82), Inches(0.17), Inches(4.4), Inches(0.26))
    p = tx.text_frame.paragraphs[0]
    p.text = "Trường THPT Thuận Hoá"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY

    tx = slide.shapes.add_textbox(Inches(1.82), Inches(0.45), Inches(4.5), Inches(0.22))
    p = tx.text_frame.paragraphs[0]
    p.text = "Trường Đại học Sư Phạm, Đại học Huế"
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED

    # Section title
    tx = slide.shapes.add_textbox(Inches(6), Inches(0.27), Inches(6.8), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = section
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.RIGHT

    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(1),
                                 Inches(12.5), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()

    # Footer
    tx = slide.shapes.add_textbox(Inches(0.48), Inches(7.08), Inches(4), Inches(0.2))
    p = tx.text_frame.paragraphs[0]
    p.text = "GV: Mai Xuân Văn"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED

    tx = slide.shapes.add_textbox(Inches(12.35), Inches(7.08), Inches(0.45), Inches(0.2))
    p = tx.text_frame.paragraphs[0]
    p.text = str(n)
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED
    p.alignment = PP_ALIGN.RIGHT


def add_image(slide, path, x, y, w, h):
    """Add image preserving aspect ratio."""
    # Frame
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x - 0.04), Inches(y - 0.04),
                                  Inches(w + 0.08), Inches(h + 0.08))
    frame.fill.solid()
    frame.fill.fore_color.rgb = PALE
    frame.line.color.rgb = BORDER
    frame.line.width = Pt(0.8)

    # Calculate aspect ratio
    im = Image.open(path)
    ratio = im.width / im.height
    box_ratio = w / h

    if ratio >= box_ratio:
        draw_w = w
        draw_h = w / ratio
    else:
        draw_h = h
        draw_w = h * ratio

    # Center in frame
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2

    slide.shapes.add_picture(path, Inches(draw_x), Inches(draw_y),
                            width=Inches(draw_w), height=Inches(draw_h))


def add_highlight(slide, x, y, w, h, label=''):
    """Add red highlight rectangle for animation."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                  Inches(w), Inches(h))
    shape.fill.background()  # Transparent
    shape.line.color.rgb = RED
    shape.line.width = Pt(4)

    if label:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RED


def add_speaker_notes(slide, text):
    """Add speaker notes with video script."""
    slide.notes_slide.notes_text_frame.text = text


def main():
    parser = argparse.ArgumentParser(description="Create product application slide deck")
    parser.add_argument("--screenshots", type=Path, required=True,
                       help="Directory containing product screenshots")
    parser.add_argument("--output", type=Path, required=True,
                       help="Output PPTX file path")
    parser.add_argument("--logos", type=Path, nargs=2, metavar=("DHSP", "THPT"),
                       help="Logo files (DHSP, THPT)")

    args = parser.parse_args()

    if not HAS_DEPS:
        print("ERROR: Missing dependencies. Install with: pip install python-pptx Pillow", file=sys.stderr)
        sys.exit(1)

    if not args.screenshots.exists():
        print(f"ERROR: Screenshots directory not found: {args.screenshots}", file=sys.stderr)
        sys.exit(1)

    # Collect screenshots
    screenshots = {}
    for ext in ['*.png', '*.jpg', '*.jpeg']:
        for path in args.screenshots.glob(ext):
            key = path.stem.lower()
            screenshots[key] = str(path)

    if not screenshots:
        print(f"ERROR: No screenshots found in {args.screenshots}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(screenshots)} screenshots")

    # Load logos
    logos = {}
    if args.logos:
        logos['dhsp'] = str(args.logos[0])
        logos['thpt'] = str(args.logos[1])

    # Create presentation
    P = Presentation()
    P.slide_width = Inches(13.333)
    P.slide_height = Inches(7.5)

    # Example: Create cover slide
    slide = P.slides.add_slide(P.slide_layouts[6])
    add_header(slide, 'BÁO CÁO SẢN PHẨM', 1, logos)

    # Add main screenshot
    if 'home' in screenshots or 'trang-chu' in screenshots:
        img_key = 'home' if 'home' in screenshots else 'trang-chu'
        add_image(slide, screenshots[img_key], 0.7, 1.35, 11.95, 4.6)

    # Add tagline
    tagline = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(5.98),
                                    Inches(11.95), Inches(0.72))
    tagline.fill.solid()
    tagline.fill.fore_color.rgb = NAVY
    tagline.line.fill.background()

    tx = slide.shapes.add_textbox(Inches(0.95), Inches(6.12), Inches(11.45), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = "Học sinh không chỉ hỏi AI — các em học cách quan sát, kiểm tra và bắt lỗi AI."
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Add speaker notes
    add_speaker_notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 1/15 (20 giây)

[Lời nói]
"Kính chào Hội đồng. Tôi là Mai Xuân Văn, giáo viên Tin học Trường THPT Thuận Hoá, Đại học Sư Phạm Huế. Hôm nay tôi xin giới thiệu AInatomy — một phòng thí nghiệm AI offline giúp học sinh không chỉ hỏi AI, mà còn học cách quan sát, kiểm tra và bắt lỗi AI."

[Animation]
- Không có highlight ở slide này.
""")

    # Save
    P.save(str(args.output))
    print(f"Created: {args.output}")
    print(f"Slides: {len(P.slides)}")


if __name__ == "__main__":
    main()
