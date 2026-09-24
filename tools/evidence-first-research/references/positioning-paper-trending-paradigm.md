# Positioning a paper within a trending paradigm (light, honest)

## Khi nào dùng
Người dùng nhận ra phần đang làm "gần với <paradigm hot>" (vd Digital Twin, semantic
communication, goal-oriented, edge-AI) và muốn **định vị bài bắt trend** mà KHÔNG
biến thành bài khác. Tín hiệu: "chỗ này gần với X rồi agent nhỉ", rồi "làm hướng nhẹ
đi nhé". Đây là EXECUTE đổi NGÔN NGỮ ĐỊNH VỊ, không đổi toán/method.

## Hai hướng — luôn nêu rõ trade-off trước khi làm
- **Hướng A (light positioning, mặc định khuyến nghị):** thêm 1 câu ở Intro + 1
  đoạn ngắn ở Related Work + 2-3 ref mới. Không đổi formulation/experiment. Rủi ro
  overclaim thấp NẾU tự định danh "lightweight / first-order / per-sensor" và nêu
  rõ điểm KHÁC với paradigm đầy đủ.
- **Hướng B (đào sâu thành paradigm thật):** nâng model (đa biến/physics-informed),
  thêm vòng phản hồi/điều khiển/what-if. Đây là đóng góp đủ lớn cho BÀI RIÊNG —
  khuyên KHÔNG nhồi vào bản đang submit.

Trình bảng "vì sao GIỐNG paradigm" (map từng thành phần bài ↔ khái niệm paradigm)
và "vì sao CHƯA gọi thẳng" (model nông, thiếu closed-loop, thiếu tương quan...) để
người dùng chọn hướng có cơ sở.

## Quy trình Hướng A (đã chạy thật, build sạch)
1. **Verify ref THẬT trước — không bịa citation.** Google Scholar chặn bot. Dùng
   arXiv API qua HTTPS (http trả 0 byte + bị security-flag):
   `curl -s "https://export.arxiv.org/api/query?search_query=abs:%22<paradigm>%22+AND+abs:%22<anchor>%22&max_results=8&sortBy=relevance"`
   rồi parse `<entry>` lấy title/authors/published/id. Chọn 2-3 paper KHỚP đúng câu
   chuyện bài (vd "age of staleness" khớp đúng cơ chế σ² tăng theo tuổi). Lấy
   metadata đầy đủ bằng `id_list=<id>` cho từng paper.
   - Cảnh giác cụm từ: "age of twin" cho kết quả lệch; "digital twin" + "age of
     information" mới trúng nhánh thật. Thử vài cụm.
   - Năm publish ≠ năm trong arXiv ID (ID 26xx.xxxxx có thể là 2026).
2. **Thêm `@article` vào `references.bib`** (patch cuối file, giữ format). Đếm lại
   entry vs cited.
3. **Intro: 1 câu định vị** — gọi object của bài bằng thuật ngữ paradigm + tự
   định danh phạm vi. Vd: "the gateway maintains a *lightweight per-sensor digital
   twin*—a predictive replica $\hat X_i$ whose fidelity decays with age—and the
   scheduler must decide which twins to re-synchronize under a strict probe
   budget~\cite{...}".
4. **Related Work: 1 đoạn ngắn** — đặt bài vào nhánh paradigm, nêu 2-3 ref, RỒI nêu
   rõ ≥2 ĐIỂM KHÁC để chống overclaim. Vd: "(a) fidelity metric của ta là
   *threshold-aware* chứ không phải age/error đối xứng; (b) giữ *per-arm
   independence* để có bảo chứng $O(1/\sqrt N)$, thay vì một twin đơn cao cấp."
   Tự định danh "lightweight, first-order twin" — phòng thủ trước reviewer "twin
   của người dùng quá đơn giản".
5. **Build gate:** full chain `pdflatex → bibtex → pdflatex → pdflatex`, grep
   `Citation.*undefined`=0 (bibtex log trống cho 3 key mới = resolve OK), undef
   ref=0, multiply-defined=0, overfull>60pt=0. Xác nhận số trang KHÔNG phình (định
   vị gọn). Báo người dùng bằng chứng build thật + bảng ref mới (key/paper/vai trò).

## Hướng A+ — biến định vị thành BẰNG CHỨNG SỐ (khi người dùng nói "thử chạy xem bài ta có ngon hơn không")

Sau light-positioning, người dùng hay muốn khẳng định định vị KHÔNG rỗng bằng cách
implement chính policy của paradigm làm baseline rồi chạy head-to-head. Đây là
EXECUTE mạnh nhất để bịt lỗ hổng "DT positioning có chắc không". Quy trình đã chạy
thật (DT+AoI vs bài AoI-greenhouse, 30-window, build sạch):

1. **Đọc interface policy trong code TRƯỚC.** Tìm file định nghĩa policy
   (`grep -rliE 'class.*Policy|MaxAoI|baseline'`), đọc 1 baseline gần nhất làm KHUÔN
   (vd `voi_baseline.py`): cấu trúc probe-stage + payload-stage + factory
   `make_<x>_policy(variant)`. Tái dùng `predict_success_vec`, `service_debt`,
   `topk`, `forecast_stats` y hệt — đừng tự viết lại.
2. **Thiết kế baseline TRUNG THỰC = mạnh nhất CÓ THỂ nhưng THIẾU đúng cái đặc
   trưng của method mình.** Vd DT+AoI = channel-aware + sync theo tuổi×độ-trôi-twin
   NHƯNG **không có threshold term**. Đây mới là so sánh có ý nghĩa: cô lập giá trị
   của đúng thành phần mình claim. Baseline straw-man (cố tình yếu) = vô giá trị.
   Thêm cả variant `+debt` để công bằng với fairness floor của method mình.
3. **Script head-to-head tái dùng HỆT pipeline chính:** cùng `run_window`,
   `select_starts`, cùng seed per-window (`50260 + wi*17`), cùng channel
   (`severe_burst`), cùng `B_probe/B_payload`. Đưa bài AoI-greenhouse + 2 incumbent (VoU,
   MaxAoI) vào cùng bảng để có ngữ cảnh.
4. **Smoke 2-window TRƯỚC** (bắt bug import/interface, ~1s) → rồi full 30-window
   background + notify. Nhúng paired Wilcoxon (one-sided) trên per-window loss +
   missed-violation reduction % thẳng trong script.
5. **Đọc kết quả TRUNG THỰC, kể cả khi baseline thắng một metric.** Bài học cốt
   lõi của session này: DT+AoI **thắng RMSE** (0.114 vs 0.126) nhưng **thua loss 5×
   và missed-violation 81%**. Đây CHÍNH LÀ luận điểm: tối ưu độ-tươi/độ-chính-xác
   của twin ≠ an toàn. Một negative-on-RMSE result lại CỦNG CỐ định vị: "method ta
   là DT-sync scheduler tốt hơn ở đúng tiêu chí quan trọng (safety), dù nhường
   RMSE." Đừng giấu metric thua — nó làm câu chuyện mạnh và đáng tin hơn.
6. **Lưu CSV** (`docs/<x>_comparison_30windows.csv`) để tái dùng, rồi ĐỀ NGHỊ (hỏi
   trước) thêm 2 dòng baseline vào bảng SOTA + 1 câu "wins RMSE but loses safety".
   Biến định vị từ "lời nói" thành "có số".

### Tích hợp baseline mới vào bảng SOTA hiện có (khi người dùng duyệt "thêm vào đi")

Thêm một dòng vào bảng so sánh nhiều-hàng đã build sạch KHÔNG chỉ là chèn `\\`. Đã
chạy thật (thêm DT+AoI vào Table VIII, build 17→18 trang sạch). Checklist:
1. **Khớp ĐÚNG convention ± của bảng cũ.** Đọc hàm `summarize` gốc xem ± là std hay
   CI95. Verify bằng cách RECOMPUTE dòng method-chuẩn (bài AoI-greenhouse) từ CSV mới — nếu nó
   reproduce KHỚP CHÍNH XÁC giá trị đang in trong bảng (vd 0.0028±0.0014) thì CSV
   nhất quán và mình đang dùng đúng công thức ±. Sai lệch = nhầm convention.
2. **Cột runtime: ĐO THẬT, không bịa, không để trống.** Nếu bảng có cột runtime,
   chạy một vòng có timing (`time.perf_counter()` quanh `run_window`, chia
   `horizon-1` ra ms/step, trung bình ~6 window) để lấy số thật cho baseline mới.
3. **Tạo nhóm family mới có nhãn `\multicolumn`** mô tả rõ baseline THIẾU gì
   ("Digital-twin synchronization family (channel-aware twin-AoI, no threshold
   term)") — nói thẳng điểm khác để reviewer hiểu vì sao nó thua.
4. **Cập nhật MỌI counter trong prose** sau khi thêm hàng: "thirteen baselines" →
   "fifteen", "four families" → "five", và đoạn liệt kê panel families (thêm mục
   (iv) DT family + cite). grep số đếm xuyên section, đừng để prose lệch bảng.
5. **Viết lại finding bị ĐẢO bởi baseline mới — trung thực.** Trước khi thêm, prose
   ghi "Only MaxWeight-AoI tracks better in RMSE"; sau khi thêm DT+AoI (RMSE tốt
   hơn) thành "THREE rules track better in L2... but each at ≥5.4× missed-violation".
   Thêm câu chốt định vị: "method ta là twin-sync scheduler tuned cho safety, nhường
   chút RMSE đổi safety gain lớn".
6. **Build gate + render bảng + vision-check.** Bảng `table*` (full-width float) hay
   NỔI sang trang khác prose — dùng `pdftotext -layout` tìm đúng trang chứa hàng mới,
   `pdftoppm` render trang đó, vision-check 2 dòng mới hiển thị đủ số, không tràn cột/
   đè chữ. Báo số trang mới (có thể +1 do hàng + đoạn phân tích). Overfull ở title
   preamble (line ~33) <60pt KHÔNG liên quan bảng — đừng nhầm.

Pitfall implement: tên class payload/probe phải khớp repo thật — đừng đoán
`GreedyPayload` nếu repo dùng factory `build("vou")` + `DebtAwarePayload`. LSP báo
numpy/None-type unresolved trong execute_code env là NOISE (env LSP), không phải
lỗi runtime — smoke test mới là bằng chứng.

## Pitfalls
- KHÔNG gọi thẳng tên paradigm ("This is a Digital Twin") nếu model nông — luôn
  kèm tính từ giảm nhẹ (lightweight/first-order/per-sensor) và đoạn departure.
- KHÔNG cite từ trí nhớ. Verify từng paper qua arXiv API; subagent literature nền
  hay fail im lặng → tự verify inline.
- Đề nghị (không tự làm) bước mở rộng: phản ánh 1 cụm paradigm lên Abstract để
  reviewer thấy ngay từ đầu — hỏi người dùng trước, vì abstract nhạy về scope.
- Người dùng chạy agent SONG SONG: gặp cảnh báo sibling-modified file thì đọc lại
  trước mỗi patch (lost-update protection).
