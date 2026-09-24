# Real-data reproduction, manuscript number-sync, figure integrity, và kỷ luật lượt

Rút ra từ phiên chuyển repo tái tạo dự án zero-touch từ số synthetic/hardcode sang
số thật data-driven, đồng bộ manuscript + hình, đẩy code GitHub.

## 1. KỶ LUẬT LƯỢT (lỗi người dùng sửa NHIỀU LẦN — ưu tiên số 1)

Người dùng cực kỳ khó chịu khi tôi nhắn một câu kiểu "agent sẽ làm X",
"để agent làm Y", "tiếp tục nhé" RỒI KẾT THÚC LƯỢT và ngồi chờ người dùng nhắc.
Người dùng đã phải hỏi lại "sao rồi", "xong chưa", "sao không thấy running",
"sao trả lời xong dừng rồi", "agent lại trả lời xong dừng rồi?".

QUY TẮC: khi đã nói sẽ làm gì, LÀM LUÔN trong cùng lượt đó tới khi ra kết quả
thật (tool output), rồi mới trả lời. KHÔNG hứa-rồi-dừng. Hoặc hoàn thành, hoặc
nêu blocker cụ thể. Câu "agent sẽ..." mà không kèm hành động ngay là vi phạm.
(Đây chính là execution-contract trong memory — tôn trọng nó tuyệt đối.)

Chẩn đoán sai từng mắc: tôi tưởng bị ngắt do gateway `restart_drain_timeout`;
người dùng đính chính rằng KHÔNG phải hạ tầng — mà là hành vi tự dừng của tôi.
Đừng đổ cho config khi gốc là mình dừng non.

## 2. VIẾT HỌC THUẬT: contributions KHÔNG nhồi số

Người dùng bác việc tôi đưa "48.5%, 23.3%, 5.4%" vào mục Contributions:
"ai đời contribution đi đưa mấy con số vào như thế?". Contributions phải ĐỊNH
TÍNH — nêu đóng góp *cái gì* (framework, policy, algorithm), số liệu để dành cho
mục Results. Sửa: bỏ hết số + highlight khỏi contributions, viết lại định tính.

## 3. AN TOÀN SỬA FILE: không ghi đè sau khi đọc thiếu

Bug nặng trong phiên: dùng script (execute_code) đọc file bằng read_file mặc
định (giới hạn ~500 dòng) rồi ghi đè lại → CẮT CỤT manuscript 1063→500 dòng.
QUY TẮC:
- Sửa manuscript/code lớn CHỈ bằng `patch` (find-replace từng chỗ), KHÔNG dùng
  write_file/script để "đọc-rồi-ghi-lại" toàn file.
- Trước mọi phiên sửa số hàng loạt: backup `_backups/<ts>/` (đã cứu phiên này).
- Sau khi khôi phục từ backup, cắm lại bằng patch tuần tự.

## 4. SỐ THẬT DATA-DRIVEN (không hardcode, tái lập)

Người dùng: "không có cái gì là gắn tĩnh hết cả", "số tính từ data KHÔNG hardcode
+ tái lập". Cách làm đã dùng:
- Loader data-driven: path qua env var + repo-relative default (KHÔNG absolute
  path máy cá nhân); cột dò từ header (không fix index); ngưỡng/label = quantile
  của chính dữ liệu; client split = shard tự nhiên (node×tháng) → non-IID thật.
- Baseline định nghĩa bằng CHÍNH SÁCH (duty + semantic on/off), số Wh TỰ TÍNH —
  KHÔNG gõ tay bảng kết quả. Cảnh giác "calibrate trá hình": hệ số như
  `comm_scale`/`COVERAGE_COEF` ép ra đúng số đích vẫn là hardcode giấu kỹ.
- Verify tái lập: chạy 2 lần cùng seed, số phải khớp bit-for-bit.
- Trung thực khi số thật xấu đi: mapping F1 gain rớt 13.5%→5.4% (±23.3), FL
  absolute thấp (44.5%). Viết thẳng "high-variance, report transparently" vào
  bài thay vì giấu. Bảng metric ghi rõ nguồn (DIVINE/IP102/WeedNet/policy).
- Đừng để 2-3 metric TRÙNG KHÍT (vd energy/time = copy của sync_reduction) —
  reviewer bắt ngay là bịa; phái sinh mỗi số từ đại lượng khác nhau.

## 5. HÌNH PHẢI KHỚP SỐ + VERIFY BẰNG VISION

Sau khi đổi số trong text/bảng, HÌNH cũ vẫn mang số cũ (vd fig vẽ 99.7%,
"paper's 20.5 Wh"). CHỦ ĐỘNG gen lại hình từ pipeline data-driven — người dùng:
"biết là hình cũ thì agent CHỦ ĐỘNG gen lại đi".
- Mỗi hình regen xong PHẢI vision_analyze để bắt: (a) số trên hình khớp text,
  (b) không còn số cũ / chữ "paper", (c) chữ không đè nhau, (d) nhãn không bị
  mũi tên cắt, (e) luồng dữ liệu đúng logic.
- Lỗi hình kiến trúc điển hình đã gặp: mũi tên sai chiều (control commands phải
  Server→Sensors), sai nguồn (A2G upload phải từ node có Semantic Encoder),
  thiếu downlink, subtitle chen title trong box, legend đè nhãn. Sửa bằng script
  matplotlib tái lập (không để PNG tĩnh không nguồn).

## 6. HIGHLIGHT VÀNG cho phần agent thêm/sửa trong manuscript

Người dùng muốn mọi chỗ agent thêm/sửa trong .tex có nền vàng để rà. Preamble:
```latex
\usepackage{xcolor}\usepackage{soul}\usepackage[framemethod=TikZ]{mdframed}
\definecolor{addyellow}{RGB}{255,245,157}\sethlcolor{addyellow}
\newcommand{\hladd}[1]{\hl{#1}}        % câu dài, xuống dòng được (soul)
\newcommand{\hlm}[1]{\colorbox{addyellow}{$#1$}}  % token toán ngắn
\newcommand{\hlt}[1]{\colorbox{addyellow}{#1}}    % token chữ ngắn
```
Pitfall: `\hl` (soul) KHÔNG nuốt `$...$` trần → bọc `\mbox{$...$}` bên trong.
`\hlm`/`\hlt` (colorbox) nuốt `$...$` OK nhưng KHÔNG xuống dòng → chỉ dùng cho
cụm ngắn (caption, ô bảng); câu dài trong body phải dùng `\hladd`+`\mbox`.
Đừng truyền `$...$` vào `\hlm` (nó tự thêm `$`) → double-math, build fail.
colorbox thêm padding ngang → bảng dễ overfull: thêm `\small` +
`\setlength{\fboxsep}{1pt}` + rút gọn nhãn cột.
LƯU Ý phạm vi: highlight chỉ áp cho MANUSCRIPT (.tex), KHÔNG áp cho code repo.

## 7. GHI CHÚ chỉ hỏi-scope khi thật cần; repo companion

- Companion GitHub repo: chỉ code + source-data pipeline; KHÔNG commit dataset
  lớn (IP102 ~3.9GB) → thêm `datasets/`, `*.tar`, `*.zip` vào .gitignore + viết
  `scripts/download_datasets.sh` tải từ nguồn thật đã verify (Zenodo DOI /
  GDrive / GitHub clone). Đồng bộ luôn `paper/numerical_results.tex` trong repo
  cho khớp số thật (nhưng file .tex trong repo không cần highlight).
- HDD offload: workspace nặng đặt dưới `/mnt/external-data/...`; filesystem HDD có thể
  KHÔNG giữ `.git` tốt (dubious ownership, thư mục con size 0) — giữ bản clone
  git khỏe ở nơi khác, chỉ đồng bộ file code sang.
- Verify build LaTeX: latexmk multi-pass, check `undefined refs/cites=0`,
  `overfull >2pt=0`, đúng số trang, rồi mới đóng gói (loại `_backups/`,
  `.fdb_latexmk`, build artifact khỏi zip).
