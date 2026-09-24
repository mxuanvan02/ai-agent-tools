# Làm sạch references.bib + đối chiếu Crossref — recipe đã kiểm chứng

Nguồn: phiên rà file `references.bib` của bài HybridStackPPI (IEEE Access), 125 → 120 entry, build cuối 0 undefined / 0 bibtex warning.

## Nguyên tắc lõi (QUAN TRỌNG NHẤT)

**Đối chiếu Crossref sinh RẤT NHIỀU false positive — KHÔNG sửa mù.** Trong phiên này Crossref flag 90/125 entry "diff" nhưng sau khi re-verify chặt chỉ còn ~10 lỗi thật, phần còn lại là bib VỐN ĐÚNG. Sửa mù theo Crossref sẽ làm HỎNG các entry đang đúng. Luôn tách "lỗi cấu trúc chắc chắn" khỏi "diff metadata cần người quyết".

### Hai nguồn false positive kinh điển
1. **Year online-first vs year of print/issue**: Crossref trả năm xuất bản online-first; bib thường ghi năm của số/volume in. Nếu bib khớp volume + issue thì năm bib ĐÚNG theo quy ước trích dẫn — đừng đổi. (ví dụ: `huang2009`, `chou2005`, `martin2005`, `oughtred2019`, `kumar2024/2022`, `chatr2017`, `hu2022`, `blohm2014`, `vig2020`, `elnaggar2021`.)
2. **Crossref match nhầm reprint/erratum/record rác**: bài kinh điển (Nature/Cell/NeurIPS) hay bị match sang bản in lại hoặc record lỗi với year/volume/pages vô lý (vd Vaswani "Attention" trả năm 2026, Breiman trả 2020). Bib gốc của bài kinh điển gần như luôn đúng.

## Phân loại sau khi rà — 3 nhóm

- **Lỗi cấu trúc CHẮC CHẮN sửa** (BibTeX báo lỗi/warning thật): trùng key, entry rác bọc `\hl{}` (artifact từ highlight-diff), thiếu `author`/`editor`. Xử lý ngay.
- **KHÔNG đụng**: nhóm false positive ở trên — bib vốn đúng.
- **Cần người dùng quyết**: cặp trùng nội dung khác key (cùng 1 bài, 2 cite key). KHÔNG tự xóa khi chưa biết manuscript cite key nào.

## Quy trình chuẩn

1. **Backup trước**: copy `references.bib` vào `_backups/bib_<ts>/`.
2. **Parse + rà cục bộ** (script python): đếm entry, phát hiện trùng key, entry `_hl`/`\hl{}`, cùng title khác key, thiếu author.
3. **Đối chiếu Crossref** (`api.crossref.org/works?query.bibliographic=<title>&mailto=...`, sleep 0.4s/query, timeout 25s, chạy NỀN có notify vì 120+ entry mất ~8–10 phút). So year/volume/number/pages, lấy DOI nếu thiếu.
4. **Re-verify CHẶT các entry bị flag**: chỉ coi là REAL_DIFF khi token-Jaccard(title) ≥ 0.85 **VÀ** họ tác giả đầu xuất hiện trong author list Crossref. Lọc bỏ "chỉ thiếu DOI" (không phải lỗi) và "no_strict_match" (bib likely correct / preprint / book).
5. **Trước khi XÓA bất kỳ entry trùng nào**: grep manuscript `.tex` xem cite key nào thực sự `\cite`. Giữ key được cite, bỏ key cited=0. (Phiên này: giữ `Chen2019PIPR` cited=1, bỏ `chen2019multifaceted` cited=0.)
6. **Corporate author** cho consortium (UniProt, Gene Ontology): `author={{UniProt Consortium}}` (hai ngoặc nhọn giữ nguyên tên, hết warning "empty/need author").

## Verify build (bắt buộc, không tự nhận "sạch")

- Smoke-test nhanh: `bibtex` trên `.aux` tối thiểu với `plain.bst` → exit 0, đếm warning.
- Thay bib đã sửa vào manuscript (backup bib cũ `.bak_<ts>`), verify md5 khớp bản đã sửa.
- Rebuild đầy đủ: `pdflatex → bibtex → pdflatex → pdflatex` (3 pass pdflatex để khớp references), tất cả exit 0.
- Kiểm log: **0 citation/reference undefined** (grep `LaTeX Warning:.*undefined` cụ thể, KHÔNG grep trần chữ "undefined").
  - **PITFALL**: grep trần "undefined" bắt nhầm `LaTeX Font Warning: Font shape 'T1/formata/m/sl' undefined` — đây là cảnh báo font cosmetic của template IEEE Access, VÔ HẠI, có sẵn từ bản gốc. Đừng báo nhầm là lỗi.
- Xác nhận cite key đích render trong PDF (`pdftotext | grep`), bbl không còn key đã xóa.
- Overfull/underfull tồn dư nếu có sẵn từ bản gốc thì không phải do mình — nói rõ.

## Lưu ý gửi file (Telegram)
- Telegram chặn file > 20MB ("document is too large or size could not be verified"). Source zip nặng (vd 23MB) KHÔNG gửi được; PDF nhẹ hơn thì gửi được.
- Lỗi "size could not be verified" cũng xuất hiện cả khi nhận file người dùng gửi lên > 20MB → hướng dẫn người dùng tải thẳng vào `~/Downloads/` thay vì gửi qua Telegram, hoặc đóng gói source sạch (bỏ `.aux/.log/.synctex/.fls/.fdb_latexmk/.bbl/.blg`) cho xuống < 20MB.
- Tên file có khoảng trắng + ngoặc `( )` dễ hỏng upload — đề xuất đổi tên không dấu cách.
