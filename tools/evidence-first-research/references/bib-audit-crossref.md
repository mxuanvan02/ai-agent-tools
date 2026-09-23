# Bibliography forensic audit — đối chiếu Crossref/OpenAlex, sync 3 file, verify build

Quy trình đã chạy thực tế nhiều đợt trên manuscript IEEE Access (HybridStackPPI). Dùng khi
người dùng nói "rà references cho kĩ bằng API tới CSDL chuẩn", nghi ref bịa/ghép sai, hoặc vệ
sinh metadata trước khi nộp.

## Phân loại bệnh của một entry (checklist)
1. **Phantom / AI-ghép-sai** — title + journal + toạ độ (vol/issue/pages) KHÔNG khớp bất kỳ
   bản ghi thật nào. Dấu hiệu: tác giả "X and others", thiếu number/pages, tên tác giả thật
   bị gán vào tiêu đề không tồn tại. → thay bằng ref thật đúng ngữ cảnh trích dẫn.
2. **Key không khớp tác giả chính** — `\bibitem` key dùng tên/năm khác lead author thật
   (vd `xu2024kg` nhưng lead = Yang; `ding2022ensemble` nhưng lead = Liu). → đổi key theo
   `<leadlastname><year><slug>`, sửa ĐỒNG THỜI trong .tex.
3. **Sai danh tính tác giả** (NẶNG) — sai tên author đầu (vd Li *Yanjie* thay vì *Yiwei*).
4. **arXiv trong khi đã có bản peer-reviewed** — đổi `@article{...arXiv...}` sang
   `@inproceedings`/`@article` bản chính thức (IJCAI/ICLR/journal) + DOI. Nhưng GIỮ arXiv nếu
   paper thật sự arXiv-only (vd Kaplan scaling laws, Doshi-Velez) — verify trước, đừng đổi mù.
5. **@article cho paper hội nghị** — NeurIPS/ICLR/IJCAI dùng `@inproceedings` + `booktitle`
   (không phải `journal`).
6. **Thiếu DOI / sai trang / sai năm / sai hoa journal** — bổ sung từ Crossref.
7. **Comment header stale** — vd "58 cited entries retained" nhưng thực tế 57. Sửa cho khớp.

## Verify metadata bằng Crossref (chính) + OpenAlex (phụ)
- Crossref theo DOI: `https://api.crossref.org/works/<DOI>` → message.{title,author,container-title,volume,issue,page,published}.
- Crossref theo title: `https://api.crossref.org/works?query.bibliographic=<title>&rows=5`.
- Crossref theo container + năm để xác minh "cái gì THỰC SỰ nằm ở vol X issue Y pp Z":
  `query.container-title=...&filter=from-pub-date:...,until-pub-date:...`.
- OpenAlex: `https://api.openalex.org/works?search=<title>` (đối chứng).
- **Pitfall**: terminal cắt output ở ~20000 ký tự → JSON OpenAlex parse lỗi "Invalid control
  character" / "Expecting delimiter". Ghi response ra file rồi parse, hoặc dùng execute_code
  với requests + json thay vì curl | head.
- Lead author = `message.author[0]`. So `given`+`family` với tên trong .bib.

## Sync 3 file — QUY TẮC quan trọng
- Package "final" thường kèm sẵn `.bbl` (bản trích dẫn đã render). Nếu CHỈ sửa `.bib` mà bbl
  cũ vẫn còn → ref ảo vẫn lọt vào PDF khi user chỉ chạy pdflatex.
- **Nhưng** nếu rebuild bằng `latexmk -pdf` (chạy bibtex), `.bbl` TỰ SINH LẠI từ `.bib`. Vậy:
  chỉ cần sửa `.bib` (+ `.tex` cho chỗ đổi key) rồi rebuild → bbl khớp tự động. Không cần sửa
  tay bbl nữa. (Đợt đầu sửa tay cả 3 cho chắc; từ đợt 2 trở đi để latexmk lo bbl.)
- Đổi key BẮT BUỘC sửa cả `\cite{...}` trong .tex — grep mọi chỗ trước khi đổi.

## Verify sau sửa (bằng chứng thật, không tự nhận sạch)
```bash
# backup trước mọi lần sửa
ts=$(date +%Y%m%d_%H%M%S); mkdir -p _backups/$ts; cp references.bib *.tex *.bbl _backups/$ts/
# rebuild đầy đủ
latexmk -pdf -g HybridStackingPPI.tex   # EXIT 0?
# đếm phải KHỚP cả 3:
grep -c '^@' references.bib              # số entry
grep -c '\\bibitem' *.bbl                # số bibitem render
# số distinct \cite key trong tex (tách theo dấu phẩy)
# undefined citation chỉ tính ở PASS CUỐI (latexmk gộp mọi pass vào 1 .log)
grep -c 'Citation.*undefined' <(tail -n +<last-run> *.log)
grep 'There were undefined references' *.log   # phải RỖNG
# key cũ/ảo phải biến mất khỏi file chính (không tính _backups/)
# tên tác giả sai phải = NONE; pages/tên mới phải hiện trong pdftotext của PDF
```

## Gotcha LaTeX/IEEE
- `IEEEtran.bst` MẶC ĐỊNH suppress field `doi` → DOI KHÔNG hiện trên PDF dù có đủ trong .bib.
  Đây là hành vi chuẩn IEEE, KHÔNG phải lỗi. Production IEEE Access đọc DOI từ source .bib.
  Chỉ bật hiển thị nếu user yêu cầu rõ.
- Warning `LaTeX Font Warning: Font shape T1/formata/m/sl undefined` là cosmetic của template
  IEEEtran, có sẵn từ trước, KHÔNG liên quan citation — đừng nhầm với undefined reference.
- `search_files`/grep với pattern chứa `\cite{` có thể fail "Unmatched {" → dùng terminal grep
  với chuỗi escaped, hoặc pattern không có brace.

## Đóng gói bản nộp sạch
- Loại `_backups/` và rác build (`.aux .log .blg .fls .fdb_latexmk .out .synctex.gz`).
- Giữ: `.tex .bib .bbl .pdf` (đã rebuild) + `figures/` + `*.cls *.bst` + logo/png.
- Verify zip KHÔNG lọt artifact/backup và bib shipped KHÔNG còn key cũ/ảo trước khi gửi.
- Kèm `references_clean.bib` standalone nếu user xin riêng.
