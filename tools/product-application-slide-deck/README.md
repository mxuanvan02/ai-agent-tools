# Product Application Slide Deck

Build applied-product presentation decks for education competitions with real screenshots, speaker notes, and highlight animations.

## Purpose

Transform product artifacts (screenshots, interaction logs, test results) into a structured 15-slide deck following competition rubrics:

- **Real product screenshots** as primary evidence (60-70% of content area)
- **Speaker notes** with detailed video scripts (5-minute demo timing)
- **Highlight shapes** for animation timing during video recording
- **Honest separation**: product QA ≠ classroom impact

## When to Use

- Presenting a **running product** (not a research proposal)
- Competition requires: context → solution → implementation → results → sustainability
- Have screenshots/interaction logs but need structured narrative
- Deck will be used for video recording with click-through animations

## Quick Start

```bash
# Validate an existing deck
python3 scripts/validate_deck.py presentation.pptx --all

# Create a new deck (template)
python3 scripts/create_product_deck.py \
    --screenshots /path/to/screenshots/ \
    --logos logo_truong.png logo_truong_dai_hoc.png \
    --school-name "Trường THPT <Tên trường>" \
    --affiliation "Đại học <Tên trường đại học>" \
    --presenter "GV: <Tên người trình bày>" \
    --output presentation.pptx
```

Tên trường, tên người trình bày và đường dẫn logo do bạn truyền vào từ dòng lệnh.
Script không chứa sẵn tên cơ quan nào, nên dùng cho bất kỳ trường nào cũng được.

## Structure

### 15-Slide Template

| # | Section | Purpose |
|---|---------|---------|
| 1 | Cover | Product screenshot + value proposition |
| 2 | Table of Contents | 5 sections per competition rubric |
| 3 | Product Introduction | Screenshot + audience + scope |
| 4 | Context & Problem | 3 pain points + screenshots |
| 5 | Solution Overview | 4-step flow + interaction screenshots |
| 6 | Real Interaction | 4-state sequence with captions |
| 7-9 | Features 1-3 | Screenshot + 3 callout cards |
| 10 | Curriculum Integration | Metrics + integration screenshots |
| 11 | Teacher Evidence | Export screenshot + benefit cards |
| 12 | Product Verification | 4 metrics + verification screenshots |
| 13 | Implementation & Limits | "ĐÃ CÓ" / "CẦN BỔ SUNG" |
| 14 | Sustainability | 3-step deployment + screenshots |
| 15 | Conclusion | Product screenshot + value cards + link |

### Speaker Notes Format

Each slide includes:
```
KỊCH BẢN — SLIDE 7/15 (25 giây)

[Lời nói]
"Một trong những tính năng cốt lõi là..."

[Animation]
- Click 1: Highlight "Đầu ra AI" — "Đây là đầu ra AI..."
- Click 2: Highlight "Bước 1" — "Bước 1: Nhận diện."
```

## Scripts

### validate_deck.py

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

### create_product_deck.py

Template script for building product application decks.

```bash
python3 scripts/create_product_deck.py \
    --screenshots /path/to/screenshots/ \
    --logos logo_truong.png logo_truong_dai_hoc.png \
    --school-name "Trường THPT <Tên trường>" \
    --affiliation "Đại học <Tên trường đại học>" \
    --presenter "GV: <Tên người trình bày>" \
    --output presentation.pptx
```

### check_structure.py

Kiểm tra cấu trúc riêng của tool: file bắt buộc có đủ không, script có biên dịch
được không, tài liệu còn đủ mục không.

```bash
python3 scripts/check_structure.py
```

## Design Principles

### Layout Rules

- **One slide = one visual purpose**
- Fixed grid: header → title → evidence region → caption/footer
- **Preserve screenshot aspect ratios** (never force into arbitrary rectangles)
- Use neutral background/padding for unused space

### Content Density

- **60-70% area**: real product screenshots
- **20-30%**: short explanatory text
- **≤10%**: policy citations or technical details

### Highlight Shapes

- Red border rectangles (4pt, no fill) over screenshot regions
- Labeled with step names (e.g., "Bước 1", "Đọc", "Phản hồi")
- Intended for PowerPoint "Appear" animations synced to speaker notes

## Honest Boundaries

### Do Not Claim

- ❌ Classroom impact without classroom data
- ❌ Student feedback without actual feedback
- ❌ Before/after measurements without baseline

### Do State Clearly

- ✅ "Đây là kiểm thử sản phẩm, không phải số liệu tác động lớp học"
- ✅ "Cần bổ sung: dữ liệu từ lớp học thật"
- ✅ "Các tỉ lệ trong slide là kết quả của mô phỏng, không phải số liệu tác động"

## Validation

```bash
# Cổng nội dung công khai (dùng chung toàn repo)
python3 scripts/public_hygiene_check.py

# Kiểm tra cấu trúc riêng của tool
python3 scripts/check_structure.py

# Run tests
python3 -m unittest discover -s tests -v

# Compile scripts
python3 -m py_compile scripts/*.py
```

`public_hygiene_check.py` là bản sao giống hệt của cổng dùng chung trong toàn repo:
nó quét mọi file trong thư mục tool tìm tên cơ quan, đường dẫn nội bộ, tên
dự án chưa công bố, khoá bí mật và ảnh nhị phân. Thêm logo hoặc tên trường thật
vào thư mục tool thì phải kiểm tra lại bằng cổng này.

## Dependencies

- `python-pptx` (presentation generation)
- `Pillow` (image aspect ratio calculation)
- `LibreOffice` (PDF conversion, optional)
- `poppler-utils` (PDF inspection, optional)

Install:
```bash
pip install python-pptx Pillow
```

## Example Workflow

1. **Gather evidence**: Collect product screenshots, interaction sequences, test results
2. **Classify deliverable**: Confirm this is an applied-product report
3. **Run template**: Use `create_product_deck.py` to generate base structure
4. **Customize content**: Edit slides to match specific product
5. **Validate**: Run `validate_deck.py --all` to check structure
6. **Export PDF**: Use LibreOffice for submission
7. **Add animations**: Open PPTX in PowerPoint, add "Appear" animations to highlights
8. **Record video**: Use speaker notes as script, click through highlights

## References

- [Vietnam AI in Education Excellence Awards 2026](https://ieeai.net/giaithuong)
- Competition rubric: 5 sections (context, solution, implementation, results, sustainability)
- 5 criteria: practicality, creativity, impact, sustainability, presentation quality

## License

MIT

## Author

Tool này do [Tên tác giả] xây dựng. Bản công khai không ghi tên cơ quan cụ thể;
tên trường, tên người trình bày và logo được truyền vào qua tham số dòng lệnh
khi dựng deck.
