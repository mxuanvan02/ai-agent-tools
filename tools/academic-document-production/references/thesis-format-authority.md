# Thesis Format — Canonical Numbers

Canonical reference: a completed Vietnamese university-level research project report
(4 chapters, ~90 pages, LaTeX source). Every number below is read out of that report's
`Libs/settings.tex` and `main.tex`, not recalled from memory.

Use this file as the default when no newer institutional document supersedes it. When
a programme office supplies its own rule, that rule wins — see *Delegation* below.

## Verified formatting (settings.tex)

| Item | Value |
|---|---|
| Document class | `book`, `a4paper`, `oneside`, `12pt` |
| Engine | XeLaTeX; `fontspec` + `polyglossia`, `\setmainlanguage{vietnamese}` |
| Body font | `Times New Roman` (system font, Unicode) |
| Page size | 210 × 297 mm |
| Left margin | **3.0 cm** |
| Right margin | **2.0 cm** |
| Top margin | **2.5 cm** |
| Bottom margin | **2.5 cm** |
| Line spacing | `\baselinestretch{1.15}` |
| Paragraph skip | `6 pt` |
| First-line indent | `1.27 cm` |
| Header | left = chapter name (uppercase), right = page number, rule `1.0 pt` |
| Bibliography | `IEEEtran` |
| Part heading | `Phần <số>`, uppercase, centred, `\Huge` bold |
| Chapter heading | `Chương <số>` + `\hrule height 1.5pt` + title `\LARGE` bold, flush right |
| Theorem names | Vietnamese: Định nghĩa, Tính chất, Định lý, Ví dụ, Bổ đề, Chú ý |
| Algorithm label | `Thuật toán` (`\ALG@name`) |

Note what is **not** 13pt and **not** 3.5 cm left. The frequently repeated
"Times New Roman 13, lề trái 3.5" belongs to other institutions' regulations; this
canonical report uses 12pt and 3.0 cm left. Do not silently apply the other number to
this genre.

## Front matter the format check looks for

Cover (double TikZ frame) → inner cover with cơ quan chủ trì + chủ nhiệm signatures →
team members → lời cam đoan → Mục lục → Danh mục bảng, biểu → Danh mục hình ảnh →
**Danh mục thuật toán** → THÔNG TIN KẾT QUẢ NGHIÊN CỨU (VN) → same in EN.

`\frontmatter` switches page numbering to roman and suppresses chapter numbering;
`\mainmatter` restarts arabic at `\part{Mở đầu}`. Getting this wrong produces a TOC
whose page numbers do not match the printed pages.

## Delegation: why a borrowed template is not a safe default

No Ministry circular sets font, margin, or line spacing for a Vietnamese thesis.
Thông tư 23/2021 (thạc sĩ) and 18/2021 (tiến sĩ) govern admission, defence, and
archival deposit. Đại học Huế QĐ 1538/QĐ-ĐHH (11/10/2021) Điều 24 khoản 4 điểm c
assigns `hình thức, cách trình bày luận văn` to the **đơn vị đào tạo**.

Institutions therefore diverge, and the divergence is large enough to break a
submission:

| | canonical report | CTU QĐ 1799 (2021) | TĐT QĐ 2055 (2020) |
|---|---|---|---|
| Body size | 12pt | 13 | 13 |
| Line spacing | 1.15 | 1.2 | 1.5 |
| Left | 3.0 cm | 3.0 cm | 3.5 cm |
| Right | 2.0 cm | 2.0 cm | 2.0 cm |
| Top | 2.5 cm | 2.0 cm | 3.5 cm |
| Bottom | 2.5 cm | 2.0 cm | 3.0 cm |
| Page number | header right | footer centre | header centre |

Same country, same degree band: body size differs by a point, line spacing by 0.35,
top margin by 1.5 cm, page number by position. A rule copied from another
institution's template is not conservative — it is wrong.

## Rules that hold across the verified documents

- A4, one side, Vietnamese in Unicode, third person.
- Tables and figures numbered by chapter (`bảng 2.1`, `hình 3.4`), each listed in its
  own danh mục.
- Table caption above, figure caption below; neither bold nor italic.
- A float is placed after the paragraph that discusses it, never right after a heading.
- Headings numbered by chapter and level, at least two sub-items at any level.
- No heading stranded at the foot of a page.

## The check before formatting

1. Name the **đơn vị đào tạo** receiving the document — not the university, the unit.
2. If that unit has issued a newer format document than the canonical report, obtain
   it; record title, decision number, date, URL, SHA-256.
3. Otherwise draft to the canonical numbers above and state in the delivery note that
   the format follows the canonical report.
4. Never present a recalled number as the institution's rule. A margin figure from a
   template found online, or from a file named after a decision number that cannot be
   produced, is a fabricated constraint.
