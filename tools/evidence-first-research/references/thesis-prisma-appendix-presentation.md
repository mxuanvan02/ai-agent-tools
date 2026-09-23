# Thesis PRISMA Appendix Presentation

Session lesson from LVTN PRISMA appendix editing.

## User preference

Người dùng wants the PRISMA appendix to be evidence-display, not prose explanation. The main chapters already explain the method; the appendix should show the audit artifacts clearly and briefly. He is especially sensitive to any text that looks like internal implementation detail, even if it is framed as a harmless note.

## Practical rules

- Keep appendix text minimal: short PRISMA flow table, concise keep/exclude criteria, then source lists. Avoid paragraph-level explanation.
- Do not add a final `Ghi chú`/note section unless Người dùng explicitly asks. Even notes like “the list is kept for transparency” can read as internal workflow commentary.
- Do not expose internal implementation details in the printed thesis appendix: code file names, variable names, script names, raw IDs, query IDs, candidate IDs, CSV/JSON filenames, magic identifiers, pipeline labels, or long machine audit maps.
- Do not print long decision/evidence tables with internal IDs. If printing all records, use reader-facing columns only: `STT`, `Năm`, `Công trình`, `KQ`, `Giai đoạn`, `Lý do`.
- Use Vietnamese headings and table captions/columns for evidence tables.
- If Người dùng asks to “show công trình từ đầu đến cuối giống Tài liệu tham khảo”, include source lists in the appendix. If both the initial corpus and core set are needed, put `Danh mục 627 bản ghi ban đầu` BEFORE `Danh mục 64 công trình lõi`.
- For the 627-record list, use `longtable` rather than an enumerated list. Mark the stage and public-facing reason for each record: `Gộp lặp`, `Sàng lọc tiêu đề/tóm tắt`, `Thẩm định toàn văn/siêu dữ liệu`, `Tập lõi`; reasons like `Trùng với bản ghi khác`, `Ngoài phạm vi nông nghiệp`, `Không thể hiện rõ thành phần mạng và điều khiển`, `Thiếu một hoặc nhiều thành phần PNCE`, `Không truy xuất đủ bằng chứng để thẩm định`.
- Only the final 64 should be marked `Giữ`. Intermediate “passed/eligible/include after metadata” statuses must not be shown as `Giữ` if they are not in the final core set; otherwise the appendix appears to contradict the PRISMA count.
- Build the PDF after editing; if the project uses `fontspec`, use XeLaTeX (`latexmk -xelatex ...`), not pdfLaTeX.

## Recommended structure

1. `Luồng PRISMA` — one table with stage/input/excluded/remaining/note.
2. `Tiêu chí giữ và loại` — one compact table.
3. `Danh mục 627 bản ghi ban đầu` — `longtable` with public-facing stage/reason columns, no internal IDs.
4. `Danh mục 64 công trình lõi` — enumerate the final included-core works like references.

## Pitfalls

- Do not over-explain the PRISMA process in the appendix. If you find yourself writing paragraph-level methodology, move it to the main chapter or cut it. The appendix should “show”, not re-argue.
- Do not preserve internal labels just because they help reproducibility. Reproducibility in the printed thesis should be expressed through clear stages and reasons, not through file names, IDs, variable names, or code terminology.
- Do not leave LaTeX comments explaining layout hacks (e.g. why `\clearpage` exists). Người dùng treats those as internal content if they surface in review or source inspection.