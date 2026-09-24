# Thesis ready-submit polish: layout, code-leakage sweep, packaging

Khi người dùng nói "rà soát kỹ luận văn, đủ ready-submit chưa" + "spawn subagent
song song" rồi "lên plan trước rồi làm" — đây là EXECUTE đa-bước. WORKFLOW của
người dùng (lặp lại 3 lần trong một phiên, là PREFERENCE cứng):

1. **PLAN-FIRST.** Trình plan đánh số (todo list) + xin gật đầu TRƯỚC khi sửa.
   Người dùng hay ngắt "lên plan trước rồi làm chớ" nếu nhảy vào sửa ngay.
2. **RUNNING PROGRESS.** Trong lúc làm, báo từng bước đã đổi gì. Người dùng hỏi "đang
   làm đến đâu", "ở giữa người dùng không thấy báo cáo" nếu im lặng quá lâu.
3. **Telegram:** KHÔNG bảng Markdown nặng (render lỗi) — prose nhẹ, danh sách ngắn.

## Multi-lens review (READ-ONLY) — chia theo FILE, không theo việc

3 subagent song song, toolsets `[terminal, file]`, CẤM sửa file (người dùng chạy nhiều
agent → tránh lost-update; PARENT là nơi DUY NHẤT ghi):
- Lăng kính A — số liệu: đếm lại MỌI số từ CSV gốc (Python thuần `open()`, KHÔNG
  `hermes_tools.read_file` vì nhiễm tiền tố `N|`), đối chiếu .tex.
- Lăng kính B — cấu trúc/tham chiếu: build + log/.aux → undefined ref/cite,
  multiply-defined, label-không-ref, float-too-large, overfull>60pt, bbl đầy thân.
- Lăng kính C — ngôn ngữ/dấu câu/overclaim.

Subagent có thể bị INTERRUPT (waiting-for-model) → chạy lại riêng lăng kính đó,
đừng bỏ. PARENT VERIFY mọi finding số liệu từ CSV trước khi patch (subagent C ở
phiên này flag "tên tác giả lệch cite-key" = FALSE-POSITIVE: cite key chỉ là nhãn,
khác tên tác giả là bình thường — kiểm `author=` trong .bib rồi mới kết luận).

Khi sửa: SỬA TUẦN TỰ (parent), không spawn subagent ghi. Người dùng nói "spawn subagent
làm cho nhanh" nhưng việc SỬA nhiều file nhỏ thì parent tự patch nhanh hơn +
an toàn hơn điều phối ghi song song — giải thích ngắn rồi tự làm.

## Longtable conversion + FLOAT-ORDERING fix (bug thật, khó thấy)

"Float too large for page by 889pt" trên một `table` thường (tabularx 4-5 hàng
nhiều chữ) = bảng cao hơn trang, nguy cơ tràn/cắt. Fix: đổi sang `longtable`
(chia trang). Recipe: bỏ `\begin{table}[!htbp]\centering` + `\end{table}`, đặt
`\caption{...}\label{...}\\` NGAY sau `\begin{longtable}{cols}`, thêm
`\endfirsthead`/`\endhead`/`\bottomrule\endfoot`. Cột `X` (tabularx) phải đổi
thành `p{Ncm}` cố định (longtable không có X).

PITFALL hệ quả — THỨ TỰ SỐ HIỆU BẢNG ĐẢO: longtable GHIM tại chỗ (in sớm) còn
`table` float TRÔI xuống xa. Bảng 2.4 (longtable) in TRƯỚC 2.1–2.3 (float trôi
xuống) → Danh mục bảng hiển thị 2.4 trang 66, 2.1 trang 79: lộn xộn, hội đồng bắt.
Chẩn đoán: đọc `.aux` (số hiệu gán theo thứ tự source — đúng) + `.lot` (thứ tự +
trang in — lộn). FIX: thêm `\clearpage` NGAY TRƯỚC longtable để xả hết float đang
chờ (2.1–2.3) ra in trước, rồi longtable in sau → thứ tự khớp. Verify lại `.lot`:
số hiệu phải tăng dần theo trang.

VERIFY longtable: render TỪNG trang nó trải qua (vd 3 trang) ra PNG + vision-check
đủ hàng, header lặp mỗi trang, số liệu đúng, không tràn. Build sạch KHÔNG đủ.
CẢNH BÁO số-trang: số trong `.lot`/`.aux` là số trang LOGIC (in), lệch số trang
PDF VẬT LÝ do front-matter La Mã → khi render `pdftoppm` phải tìm trang vật lý
bằng `pdftotext`-grep caption, đừng dùng số .lot trực tiếp (render nhầm trang).

## Code-identifier leakage sweep (PREFERENCE MẠNH — người dùng dị ứng)

Người dùng bắt gắt khi tên file code / đường dẫn / định danh lộ vào THÂN BÀI ("gì mà có
mấy dòng về file code... rà soát phải có chiến lược"). Quét HỆ THỐNG, đừng bắt
ngẫu nhiên:
```
grep -rnE '\\texttt\{[^}]*\.(json|csv|sh|py|txt)|\\url\{[^}]*\.(json|csv|sh|py)|[A-Za-z0-9_]+/[A-Za-z0-9_]+\.(sh|py)|\\(verb|lstinline)' Chapter/ main.tex
```
Phân 3 NHÓM, xử lý KHÁC nhau (không cào bằng):
- **NHÓM 1 — thân bài (chap1-4, modau, ketluan): PHẢI bỏ.** Tên script/CSV/đường
  dẫn `05_Simulation/.../run_all.sh`, `q1_benchmark_summary.csv` trong prose/
  caption/bảng-tham-số → thay bằng mô tả tự nhiên ("pipeline mô phỏng công khai")
  + trỏ `Phụ lục~\ref{appendix:...}`. Giữ tính tái lập, không lộ tên file.
- **NHÓM 2 — GIỮ nguyên (chủ đích):** phụ lục audit trail (`phuluc_audit.tex`) —
  raw filename LÀ provenance để phản biện/tái lập, giữ raw. Cú pháp truy vấn
  Boolean `(Plant) AND (Network)` = nội dung phương pháp. Link GitHub repo =
  Data/Code Availability hợp lệ.
- Verify sau sửa: grep lại thân bài (loại phuluc_audit) phải = 0 match.

## Packaging hygiene (Stage 10)

- Xóa rác là thao tác KHÓ HỒI → liệt kê chính xác cái sắp xóa trước (security scan
  có thể chặn mass-deletion, người dùng approve). Xóa `_backups/`, `_corrupt_*`,
  `Chapter/_backups/`. GIỮ `.venv_fig` (cần regen hình) nhưng EXCLUDE khỏi zip.
- **Dual-PDF trap:** zip thường có 2 bản `main.pdf` (`build/main.pdf` mới +
  `main.pdf` root STALE từ `cp` cũ). Kiểm `md5sum` cả hai; nếu lệch, copy bản
  build mới đè root cho khớp 1 bản. `grep -c main.pdf` đếm cả file PDF khác tên
  (vd `fig_publication/CAW_VoU_..._main.pdf` hợp lệ) — đọc đường dẫn đầy đủ, đừng
  hoảng vì số đếm.
- Zip exclude: `.venv*`, `__pycache__`, `_backups*`, `*.aux/.log/.fls/.fdb*/.bbl/
  .blg/.out/.toc/.lof/.lot`. Verify `unzip -l | grep -iE 'venv|pycache|backup'` = 0.
- modau.tex KHÓA = đề cương: nếu lăng kính C đề xuất sửa "ưu việt/ưu thế vượt
  trội" ở Mở đầu → KIỂM cụm đó có trong đề cương gốc (`pdftotext` + normalize
  whitespace vì PDF ngắt dòng giữa cụm) → nếu CÓ thì GHI NHẬN, KHÔNG sửa.
