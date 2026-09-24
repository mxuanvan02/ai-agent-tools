# Rà soát & làm sạch bibliography đối chiếu CSDL chuẩn (Crossref/OpenAlex)

Playbook cho lớp việc: người dùng đưa 1 paper (thường .zip chứa .tex + .bib + .bbl)
và yêu cầu "rà references cho kỹ bằng API tới CSDL chuẩn", phát hiện ref bịa/ghép
sai, hoặc vệ sinh metadata. Đã chạy thật trên HybridStackPPI (IEEE Access).

## 0. Nguyên tắc
- DERIVE-then-verify: KHÔNG đoán metadata. Mọi sửa đổi phải xác minh qua Crossref
  (và/hoặc OpenAlex) TRƯỚC khi patch. Báo rõ cái gì verify được, cái gì không.
- Backup `_backups/<ts>/` cả .tex/.bib/.bbl trước khi sửa.
- Báo đầu phản hồi dòng `🔧 Dùng: ...` (web/Crossref API · read_file · patch · terminal).

## 1. Hai loại "bệnh" tách biệt
1. **Ref bịa / ghép sai do AI (phantom / mis-spliced)** — nguy hiểm nhất.
   Dấu hiệu: tên tác giả THẬT (vd Richard B. Silverman, Ian Walsh) bị gán vào
   title + journal + volume/issue/page KHÔNG tồn tại; metadata thiếu number/pages;
   `author={X and others}` mơ hồ; "and Zhang, J and others".
2. **Vệ sinh metadata** — sai title nhẹ, thiếu DOI, `@article` cho paper hội nghị,
   key không khớp tác giả chính, cite arXiv trong khi đã có bản peer-reviewed,
   key name không khớp nội dung (vd `srinivasan2007protein` chứa Park 2009).

## 2. Cách phát hiện phantom (3 mũi đối chiếu)
Với mỗi ref nghi vấn, query Crossref theo:
- (a) **title** (`query.bibliographic`) — khớp chính xác?
- (b) **author + journal** — tác giả đó có viết bài tên này trên journal đó?
- (c) **toạ độ chính xác** journal + volume + issue + pages/year — chỗ đó thực sự là bài gì?
Nếu cả 3 đều không khớp → phantom. Thường (c) lộ ra: "vol X issue Y pp A–B" là
một bài HOÀN TOÀN khác hoặc rỗng.

Crossref REST (không cần key):
```
https://api.crossref.org/works?query.bibliographic=<title>&rows=5
https://api.crossref.org/works?query.author=<au>&query.bibliographic=<kw>&rows=6
https://api.crossref.org/works/<DOI>            # lấy metadata canonical 1 DOI
```
OpenAlex: `https://api.openalex.org/works?search=<title>&per_page=5`

## 3. PITFALL — OpenAlex bị cắt ở 20k ký tự trong terminal/execute_code
Output OpenAlex JSON dài → "Invalid control character at char 20000" /
"Expecting ',' delimiter". KHÔNG parse trực tiếp stdout. Ghi response ra file rồi
`json.load`, hoặc dùng `select=` để giảm field:
`...&select=title,authorships,primary_location,publication_year,doi`.

## 4. PITFALL QUAN TRỌNG — package "final" có .bbl pre-rendered
Nếu .zip có sẵn `HybridStackingPPI.bbl` (đã render), sửa MỖI `.bib` thì ref ảo
VẪN lọt vào PDF khi biên dịch lại (LaTeX đọc .bbl, không phải .bib). Hai lựa chọn:
- **Khuyến nghị**: chỉ sửa `.bib` (+ `.tex` cho chỗ đổi key) rồi rebuild bằng
  `latexmk` — nó chạy `bibtex` và **tự sinh lại .bbl** từ .bib mới. Dùng `latexmk -g`
  để force. Không cần sửa tay .bbl.
- Hoặc sửa tay đồng bộ cả 3 file `.bib` + `.tex` + `.bbl` (mỗi `\bibitem` khớp tay).
Khi đổi tên KEY (vd xu2024kg→yang2024kg, srinivasan2007protein→park2009critical):
phải đổi ở `.bib` (def) + mọi `\cite{}` trong `.tex` + `\bibitem{}` trong `.bbl`.

## 5. PITFALL — đọc log latexmk sai
`latexmk` gộp TẤT CẢ pass vào 1 log → "Citation `x' undefined on input line N"
từ pass-1 (trước khi bibtex resolve) vẫn xuất hiện dù PDF cuối đã resolve đúng.
ĐỪNG kết luận lỗi từ log gộp. Verify bằng:
- PDF render thật: ref hiện đúng số `[3] H. Lu, ...` (pdftotext rồi grep).
- KHÔNG có dòng tổng kết "There were undefined references" ở pass cuối.
- KHÔNG có marker `[?]` trong body PDF.
- Phân biệt "Font shape `T1/formata/m/sl' undefined" (cosmetic của template
  IEEEtran, vô hại) với citation undefined.

## 6. Quy ước sửa metadata (đã verify Crossref)
- Thiếu DOI → thêm `doi={...}` từ Crossref.
- Paper hội nghị dùng `@article`+`journal=` → đổi `@inproceedings`+`booktitle=`
  (NeurIPS, ICLR, IJCAI, ...). Thêm pages nếu Crossref có.
- arXiv đã có bản peer-reviewed → đổi sang bản chính thức (IJCAI/ICLR/journal).
  NHƯNG: paper arXiv-only thật sự (vd Kaplan scaling-laws 2001.08361,
  Doshi-Velez 1702.08608) thì GIỮ NGUYÊN — đừng ép gán DOI.
- Key không khớp tác giả chính → đổi key theo first author + năm thật
  (vd key "xu" nhưng first author Yang Jie → `yang2024kg`).
- preprint bioRxiv có field rác `pages={2021--10}` → bỏ, thêm `doi=10.1101/...`,
  `note={Preprint}`, year = first-posted.
- Title hoa/thường (Lightgbm→LightGBM, Ontoprotein→OntoProtein), `O'neill`→`O'Neill`.

## 7. Thay phantom: chọn ref THẬT khớp NGỮ CẢNH câu văn
Đọc câu chứa `\cite` để biết ý định, chọn ref thật sát nghĩa:
- "PPI là đích trị liệu / drug discovery" → vd Lu et al. 2020 Signal Transduct
  Target Ther (DOI 10.1038/s41392-020-00315-3).
- "data leakage / đánh giá quá cao do tương đồng" → vd Hamp & Rost 2015
  Bioinformatics (DOI 10.1093/bioinformatics/btu857), đi cặp với park2012flaws.
Giữ nguyên câu văn nếu ref mới vẫn khớp ý; chỉ chỉnh chữ khi cần bám nội dung ref thật.

## 8. Verify cuối (luôn chạy)
```
# key cũ không còn trong file chính (chỉ còn trong _backups/ là OK)
grep -rn "<oldkey>" --include=*.{bib,tex,bbl} . | grep -v _backups
# rebuild
latexmk -pdf -g HybridStackingPPI.tex   # EXIT 0
# PDF resolve đúng + không phantom
pdftotext HybridStackingPPI.pdf - | grep -i "<newauthor>"
pdftotext HybridStackingPPI.pdf - | grep -ci "<phantomstring>"   # = 0
```
Báo cáo: bảng (key cũ→mới, lỗi, sửa, DOI) + bằng chứng build EXIT 0 + đường dẫn backup.
