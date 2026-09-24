# Liêm chính số liệu & kết quả âm (paired stats, regen discipline)

Rút ra từ phiên bài bandwidth-scheduling (thay urgency `p_vio` → value-of-uncertainty `4p(1−p)`,
thử bài bandwidth-scheduling-CVaR trên greenhouse + ERA5 VN thật). Dùng khi điều chỉnh mô hình toán,
regen số liệu, và quyết định đóng góp nào đưa vào bài.

## 1. Dấu của hiệu paired — lỗi đã xảy ra 2 lần/phiên

Khi tính `Δ = A − B` rồi Wilcoxon/t-test: `p` nhỏ chỉ nói **khác biệt có ý nghĩa**,
KHÔNG nói chiều nào tốt hơn.

- Metric "thấp = tốt" (loss, CVaR, missed%, objective): `Δ = PD − CVaR < 0`
  ⇒ **PD tốt hơn CVaR**. Đừng đọc `|Δ| lớn + p nhỏ` thành "CVaR cải thiện".
- BẮT BUỘC in nhãn chiều cạnh p-value, ví dụ: `-> PD better` / `-> CVaR better`.
- Sau khi sinh bảng: đối chiếu mọi ô `\best{}` phải rơi ĐÚNG vào phương pháp mình
  đang tuyên bố thắng. Nếu `\best{}` toàn nằm ở baseline → claim sai, dừng lại.

## 2. Không gắn nhãn "Proposed"/headline cho cơ chế thua chính metric của nó

Nếu phương pháp đề xuất thua baseline **có ý nghĩa thống kê** trên đúng đại lượng
nó sinh ra để tối ưu (bài bandwidth-scheduling-CVaR thua PD trên CVaR-loss cả 3 kênh, p<0.05), thì:

- KHÔNG trình bày là đóng góp thắng cuộc. Bài có "Code & Data Availability" ⇒
  reviewer chạy lại thấy ngay ⇒ sập uy tín cả các đóng góp thật khác.
- Hạ vai: *controlled result* + *deployment knob*. Nói thẳng đánh đổi
  (mua an toàn đuôi bằng chút chi phí trung bình / bandwidth), và nêu chỗ nó
  trội chỉ là xu hướng chưa đạt ý nghĩa (ns).

## 3. Thất bại lặp lại trên nhiều dataset thật = kết quả âm, KHÔNG phải bug để vá

Sau 2–3 lần đã sửa bug thật + thử biến thể + lấy data đuôi-nặng thật mà cơ chế
vẫn không vượt ⇒ đó là **phát hiện Occam**, không phải lỗi cài đặt:
"VoU + primal-dual đã hút gần hết lợi ích khả thi; thêm tail-machinery chỉ tăng
chi phí." Trình bày như negative result có kiểm soát — chuẩn Q1 tôn trọng hơn
claim gượng. (Trong phiên: 6 lần liên tiếp CVaR vô ích trên 2 dataset.)

## 4. Kỷ luật regen (người dùng yêu cầu: "xoá số cũ kẻo nhầm")

- Trước mỗi lần regen toàn bộ: `rm` sạch `outputs/` rồi chạy lại theo đúng thứ tự
  phụ thuộc (main → sensitivity → nonstationary → wilcoxon → pairwise → ablation
  → scaling → cvar). Không để số cũ/mới lẫn.
- Sinh MỌI bảng manuscript từ CSV bằng 1 script generator duy nhất
  (`make_manuscript_tables.py`): số khớp tuyệt đối, tái lập, không sửa tay.
- Bảng manuscript thường có **format riêng** (tên file, ngôn ngữ, tập con policy,
  cột p-value) KHÁC bảng thô do script mô phỏng sinh ra — phải map đúng, không
  ghi đè mù.

## 5. Đổi công thức lõi → lan truyền nhất quán

- Sửa ĐÚNG 1 chỗ (vd nhánh `else` = urgency họ bài bandwidth-scheduling trong `choose_sensors`),
  giữ nguyên các baseline (max_aoi, voi_b2, …) ở nhánh riêng.
- Kiểm tra script phụ: cái nào `import` module chính ⇒ tự đồng bộ; cái nào tự chép
  lại công thức (grep `0.55*p` hoặc hằng số cũ) ⇒ phải sửa tay.
- Chuẩn "derive-then-verify": chứng minh dạng mới đúng lý thuyết TRƯỚC (VoU =
  truncation bậc dẫn đầu của value-of-information cho quyết định nhị phân an toàn,
  `g(p)=4p(1−p)` cực đại ở biên p≈0.5, =0 khi đã chắc), rồi mới chạy tốn kém.
  Tránh grid-search mù → reviewer bắt overfitting.

## 6. Data "mất" thường fetch lại được từ API công khai

ERA5 Mekong (Cần Thơ/Sóc Trăng/Cà Mau) tưởng mất → có sẵn script
`fetch_real_vn_data.py` gọi Open-Meteo archive API
(`archive-api.open-meteo.com/v1/archive?...&hourly=temperature_2m`). Trước khi
kết luận "data mất / phải synthetic", tìm fetch script + thử tái tải từ nguồn gốc.
