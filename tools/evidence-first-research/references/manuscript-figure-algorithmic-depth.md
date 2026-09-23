# Nâng cấp figure pipeline để thể hiện chiều sâu thuật toán

Khi nào dùng: người dùng xem figure pipeline/architecture và nói "còn đơn giản quá",
"chưa thể hiện chuyên sâu về thuật toán", hoặc xin vẽ chi tiết giống các bài NCS
nông nghiệp / tối ưu UAV-EAV-as-sensor. Đây là EXECUTE: vẽ lại TikZ tại chỗ.

## Chẩn đoán: figure "đơn giản" thiếu gì

Sơ đồ khối ban đầu thường chỉ vẽ LUỒNG hộp (box → arrow → box), bỏ sót cơ chế
thuật toán mà chính TÊN method ngụ ý. Checklist thiếu hụt điển hình:
- Block ứng với feature làm nên tên method (vd "Channel-Aware" mà không có channel
  block nào).
- Belief filter / state estimator (chỉ vẽ "VoU computation", không vẽ predict→update).
- Công thức index/score tường minh (chỉ ghi tên "VoU computation" thay vì
  `I_i = p_i(t)·VoU_i + w_debt·D_i`).
- Vòng phản hồi (feedback loop) — thiếu mũi tên outcome quay lại cập nhật state,
  nên không thể hiện được tính restless/POMDP/online.

## Các thành phần nên thêm (ví dụ bài AoI-greenhouse per-arm channel)

1. **Channel/state lane riêng** (màu mới, vd `chanGreen`): block "Per-arm G–E belief"
   chứa `p̂_i^B: predict → update` và `p_i(t)=E[p_ok | p̂_i^B]`.
2. **Mũi tên tín hiệu feed vào pipeline:** `p_i(t)` bơm vào CẢ hai stage (channel-
   weight index), vẽ bằng màu của lane đó.
3. **Vòng phản hồi:** từ block Schedule/output, mũi tên nét đứt mang nhãn delivery
   outcome `o_i(t)` quay về channel block với nhãn "Bayes update p̂_i^B" — đây là cái
   thể hiện restless/closed-loop.
4. **Công thức index tường minh mỗi stage:** annotation node màu theo stage, đặt ở
   hàng riêng (KHÔNG cùng dòng tiêu đề stage).
5. **Nhãn thách thức (challenge → module):** C1 starvation / C2 threshold safety /
   C3 burst-loss hedging gắn dưới module tương ứng.

## Yêu cầu nối tiếp hay gặp: thể hiện LUỒNG DỮ LIỆU uplink/downlink

Sau khi figure đã có chiều sâu thuật toán, người dùng thường yêu cầu tiếp: \"thể hiện
thêm cả luồng dữ liệu — nhận uplink cái gì, gửi downlink cái gì, qua mỗi phase
truyền cái gì từ đâu đến đâu (sau khi tính toán)\". Đây là yêu cầu RIÊNG, khác với
\"chiều sâu thuật toán\". Phải đọc §System Model để biết CHÍNH XÁC protocol trước khi
vẽ (đừng bịa hướng truyền). Checklist một vòng giao thức (ví dụ probe-then-transmit):
- **Input/state → Stage 1:** state nội bộ (vd `{μ_i,σ_i²}`, band R) chảy vào stage tính.
- **DL (downlink, gateway→sensor):** probe request `P(t)` xuống medium; gắn nhãn **DL**.
- **UL (uplink, sensor→gateway):** metadata `m_i` lên Stage 2; gắn nhãn **UL**.
- **DL:** payload grant `U(t)` xuống medium.
- **UL:** full reading `X_i` + outcome `o_i` về belief state — ĐÓNG VÒNG (đây là
  loop hay bị thiếu ở bản trước: payload-uplink cập nhật estimator).
- **Feedback:** `o_i → Bayes update` về channel block.
- Mỗi phase ghi rõ NHẬN GÌ → TÍNH RA GÌ → GỬI ĐI ĐÂU.
Thêm một **block \"Wireless medium + N sensors/field\"** ở đáy làm nơi mọi DL/UL cắm
vào; tag DL màu đen, UL màu khác (vd `vouBlue!75!black`) để phân biệt hai chiều.

## Pitfall layout: công thức tràn/đè tiêu đề

Công thức index dài (nhất là payload với 4 số hạng) DỄ tràn ra ngoài khung hộp viền
đứt và đè lên nhãn "Stage N: ...". Cách xử lý:
- Đặt annotation node xuống hàng TRỐNG giữa các hàng hộp (vd `at (x, -0.95)` thay vì
  `(x, 0.95)` sát tiêu đề), `font=\scriptsize`, `fill=white, inner sep=1pt`.
- Nếu vẫn quá dài, rút về dạng khái niệm trong figure và để công thức đầy đủ trong
  §Method text (figure không cần là bản sao 1-1 của equation).
- Định nghĩa màu lane mới trong `main.tex` preamble bằng `\definecolor` TRƯỚC khi
  dùng trong style figure.

## Pitfall TikZ: nhãn DL/UL chen nhau, mũi tên đè text (vòng lặp render-vision)

Khi thêm nhiều mũi tên DL/UL + công thức + nhãn challenge vào cùng vùng, các nhãn
text DỄ đè nhau hoặc đè lên equation. Thực tế phải lặp 3-4 vòng render→vision mới
sạch. Các fix đã chạy thật:
- **Công thức index dài (payload 4 số hạng):** ĐỪNG đặt cạnh tiêu đề stage hay xen
  giữa các mũi tên dọc. Đặt hẳn xuống MỘT DÒNG RIÊNG bên dưới block medium, không vật
  cản — đó là nơi duy nhất đủ rộng cho equation dài.
- **Hai nhãn mũi tên dọc gần nhau** (vd \"UL: meta\" và \"DL: payload grant\"): tách bằng
  cách đẩy `pos=` khác nhau trên hai đường + đặt `left`/`right` ngược phía + thêm
  `fill=white` để che đường kẻ phía sau. Rút gọn nhãn (\"metadata\"→\"meta\") khi cần.
- **Nhãn đè viền hộp:** dời `pos=` của node nhãn ra xa biên (vd 0.40→0.62) + `fill=white`.
- **Mũi tên feedback đè cạnh hộp medium:** route bằng đường gãy tường minh
  `(med.west) -- (x_ngoài, y) |- (target.west)` thay vì `-|` cắt ngang qua hộp.
- **KHÔNG dùng số học trong tọa độ** kiểu `(5.6,\rO+0.4)` — TikZ đọc literal sai. Định
  nghĩa hằng riêng (`\def\rMt{-7.2}`) cho mép trên block và dùng nó.
- Mỗi vòng: render PNG → `vision_analyze` HỎI CỤ THỂ \"nhãn X và Y có chạm nhau không,
  mũi tên Z có đè hộp không, có chữ nào cắt cụt không\" (đừng hỏi chung chung), sửa,
  render lại. Lặp tới khi vision báo \"clean\". Build sạch + 0 overfull KHÔNG phát hiện
  được va chạm nhãn — chỉ ảnh render mới thấy.

## Quy trình verify BẮT BUỘC (build sạch KHÔNG đủ)

1. Backup figure cũ: `cp figures/fig_architecture.tex _backups/fig_<ts>/`.
2. Vẽ lại, full build chain, grep `Overfull .hbox` >60pt = 0, undefined = 0.
3. **Render trang chứa figure ra ảnh và vision-check:**
   `pdftoppm -png -r 150 -f <page> -l <page> main.pdf /tmp/fig` → vision_analyze hỏi
   cụ thể: block mới có hiện không, mũi tên feed/feedback có không, công thức có bị
   CẮT CỤT / ĐÈ tiêu đề / TRÀN lề không. Build pass mà chữ vẫn có thể bị clip ở mép
   hộp — chỉ render ảnh mới phát hiện.
4. Sửa vị trí cho hết đè, render lại, vision-check lần nữa cho tới khi sạch.
5. Gửi người dùng PDF + nêu rõ figure giờ thể hiện feature/feedback/công thức gì.

## Lệnh hữu ích

```bash
# render đúng 1 trang
pdftoppm -png -r 150 -f 4 -l 4 main.pdf /tmp/fig2
# đếm overfull > 60pt ở pass cuối
grep -oE 'Overfull .hbox \(([0-9.]+)pt' build.log | grep -oE '[0-9.]+' | awk '$1>60' | wc -l
```
