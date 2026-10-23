---
name: product-application-slide-deck
description: "Build applied-product presentation decks for education competitions: 15-slide structure with real screenshots, speaker notes with video scripts, and highlight animations for demo videos"
tags: [presentation, education, competition, product-demo]
---

# Product Application Slide Deck

## Purpose

Build presentation decks for **applied-product reports** in education competitions (e.g., Vietnam AI in Education Excellence Awards). This skill transforms product artifacts (screenshots, interaction logs, test results) into a structured 15-slide deck with:

- Real product screenshots as primary evidence (60-70% of content area)
- Speaker notes with detailed video scripts (5-minute demo)
- Highlight shapes for animation timing during video recording
- Honest separation: product QA ≠ classroom impact

## When to Use

- User needs to present a **running product** (not a research proposal)
- Competition requires: context → solution → implementation → results → sustainability
- User has screenshots/interaction logs but needs structured narrative
- Deck will be used for video recording with click-through animations

## Workflow

### 1. Classify the Deliverable

**Critical decision**: Is this a research proposal, technical design, or **applied-product report**?

For applied-product reports, the required story is:
```
Classroom need → Product in use → Real interaction sequence → 
Implementation evidence → Product checks → Impact evidence & limits → 
Sustainability/scalability
```

**Do not** let architecture, code, or policy citations displace product evidence.

### 2. Gather Evidence

Collect from user's workspace:
- Product screenshots (desktop + mobile if applicable)
- Interaction sequences (4-step flows: read → predict → act → feedback)
- Test results (automated checks, coverage metrics)
- Deployment artifacts (public URLs, offline capabilities)

**Evidence hierarchy**:
1. Real screenshots > generic illustrations
2. Interaction sequences > static features
3. Product QA numbers > classroom impact claims (unless classroom data exists)

### 3. Structure the Deck (15 slides)

| # | Section | Purpose | Content |
|---|---------|---------|---------|
| 1 | Cover | First impression | Product screenshot + one-line value proposition |
| 2 | Table of Contents | Navigation | 5 sections per competition rubric |
| 3 | Product Introduction | What it is | Screenshot + target audience + scope + operation mode |
| 4 | Context & Problem | Why it matters | 3 pain points + 3 supporting screenshots |
| 5 | Solution Overview | How it works | 4-step flow + 4 interaction screenshots |
| 6 | Real Interaction | Proof it runs | 4-state sequence with captions |
| 7-9 | Features 1-3 | Core capabilities | Screenshot + 3 callout cards per feature |
| 10 | Curriculum Integration | Educational value | Metrics + 3 integration screenshots |
| 11 | Teacher Evidence | For educators | Export screenshot + 4 benefit cards |
| 12 | Product Verification | Quality assurance | 4 metrics + 3 verification screenshots |
| 13 | Implementation & Limits | Honest boundaries | "ĐÃ CÓ" / "CẦN BỔ SUNG" two-column layout |
| 14 | Sustainability | Scalability | 3-step deployment + 3 operation screenshots |
| 15 | Conclusion | Call to action | Product screenshot + 3 value cards + demo link |

### 4. Design Principles

**Layout rules**:
- One slide = one visual purpose
- Fixed grid: header (logos + section title) → title → evidence region → caption/footer
- Preserve screenshot aspect ratios (never force into arbitrary rectangles)
- Use neutral background/padding for unused space in portrait screenshots

**Content density**:
- 60-70% area: real product screenshots
- 20-30%: short explanatory text
- ≤10%: policy citations or technical details

**Highlight shapes**:
- Red border rectangles (4pt, no fill) positioned over screenshot regions
- Labeled with step names (e.g., "Bước 1", "Đọc", "Phản hồi")
- Intended for PowerPoint "Appear" animations synced to speaker notes

### 5. Speaker Notes

Each slide includes detailed speaker notes with:
- **Timing**: seconds allocated (total ≤ 300s for 5-minute video)
- **Script**: word-for-word narration in Vietnamese
- **Animation cues**: `[Click 1: Highlight "X" — "Explanation"]`

Example:
```
KỊCH BẢN — SLIDE 7/15 (25 giây)

[Lời nói]
"Một trong những tính năng cốt lõi là Đấu trường bắt lỗi AI..."

[Animation]
- Click 1: Highlight "Đầu ra AI" — "Đây là đầu ra AI mà học sinh phải kiểm tra."
- Click 2: Highlight "Bước 1" — "Bước 1: Nhận diện."
```

### 6. Scripts

#### validate_deck.py

Validate slide count, element bounds, aspect ratios, and speaker notes.

```bash
# Check slide count (default: 15)
python3 scripts/validate_deck.py output.pptx

# Check element bounds
python3 scripts/validate_deck.py output.pptx --bounds

# Check image aspect ratios
python3 scripts/validate_deck.py output.pptx --aspect-ratios

# Check speaker notes
python3 scripts/validate_deck.py output.pptx --notes

# Run all validations
python3 scripts/validate_deck.py output.pptx --all
```

#### create_product_deck.py

Template script for building product application decks.

```bash
python3 scripts/create_product_deck.py \
    --screenshots /path/to/screenshots/ \
    --logos logo_dhsp.png logo_thpt.png \
    --output presentation.pptx
```

#### public_hygiene_check.py

Verify skill structure and script compilation.

```bash
python3 scripts/public_hygiene_check.py
```

### 7. Implementation

Use `python-pptx` to generate the deck:

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image

# Helper functions
def pic(slide, path, x, y, w, h):
    """Insert image preserving aspect ratio"""
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

def highlight(slide, x, y, w, h, label=''):
    """Add red highlight rectangle for animation"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   Inches(x), Inches(y),
                                   Inches(w), Inches(h))
    shape.fill.background()  # Transparent
    shape.line.color.rgb = RGBColor(220, 50, 50)
    shape.line.width = Pt(4)
    
    if label:
        tf = shape.text_frame
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(220, 50, 50)

def notes(slide, text):
    """Add speaker notes"""
    slide.notes_slide.notes_text_frame.text = text
```

### 8. Design Principles

**Layout rules:**
- One slide = one visual purpose
- Fixed grid: header (logos + section title) → title → evidence region → caption/footer
- Preserve screenshot aspect ratios (never force into arbitrary rectangles)
- Use neutral background/padding for unused space in portrait screenshots

**Content density:**
- 60-70% area: real product screenshots
- 20-30%: short explanatory text
- ≤10%: policy citations or technical details

**Highlight shapes:**
- Red border rectangles (4pt, no fill) positioned over screenshot regions
- Labeled with step names (e.g., "Bước 1", "Đọc", "Phản hồi")
- Intended for PowerPoint "Appear" animations synced to speaker notes

### 9. Validation

Run validation before delivery:

```bash
# Check slide count
python3 tools/product-application-slide-deck/scripts/validate_deck.py output.pptx

# Check element bounds
python3 tools/product-application-slide-deck/scripts/validate_deck.py --bounds output.pptx

# Render to PDF and verify
soffice --headless --convert-to pdf output.pptx
pdfinfo output.pdf | grep Pages  # Should be 15
```

### 8. Delivery

Provide user with:
1. **PPTX file** (editable, with highlights for animation)
2. **PDF file** (for submission, ≤100MB)
3. **Validation report** (slide count, bounds check, file size)
4. **Usage instructions**:
   - Open PPTX in PowerPoint
   - Select highlight shapes → Animations → Add "Appear"
   - Set timing per speaker notes
   - Record video with click-through

## Honest Boundaries

**Do not claim**:
- Classroom impact without classroom data
- Student feedback without actual feedback
- Before/after measurements without baseline

**Do state clearly**:
- "Đây là kiểm thử sản phẩm, không phải số liệu tác động lớp học"
- "Cần bổ sung: dữ liệu từ lớp học thật"
- "Các tỉ lệ trong slide là kết quả của mô phỏng, không phải số liệu tác động"

## Dependencies

- `python-pptx` (presentation generation)
- `Pillow` (image aspect ratio calculation)
- `LibreOffice` (PDF conversion)
- `poppler-utils` (PDF inspection)

## Example Usage

```python
# Generate deck
python3 tools/product-application-slide-deck/scripts/create_product_deck.py \
    --screenshots /path/to/screenshots/ \
    --output presentation.pptx

# Validate
python3 tools/product-application-slide-deck/scripts/validate_deck.py presentation.pptx

# Convert to PDF
soffice --headless --convert-to pdf presentation.pptx
```

## References

- [Vietnam AI in Education Excellence Awards 2026](https://ieeai.net/giaithuong)
- Competition rubric: 5 sections (context, solution, implementation, results, sustainability)
- 5 criteria: practicality, creativity, impact, sustainability, presentation quality
