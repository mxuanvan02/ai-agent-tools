# Giao tiếp tiến độ nghiên cứu với người dùng

## Mặc định

- Viết tiếng Việt đơn giản, dân dã; kết luận trước, giải thích ngắn sau.
- Tách bốn trạng thái: **đã làm thật**, **chưa làm**, **đang bị chặn**, **bước kế tiếp**.
- Giải nghĩa thuật ngữ ngay lần đầu dùng: “freeze” là khóa đúng mã nguồn/cấu hình; “smoke” là thử vài cuộc gọi nhỏ; “runner” là chương trình chạy toàn bộ thí nghiệm; “judge” là mô hình chấm.
- Không biến test xanh hoặc thử kết nối thành tuyên bố “thí nghiệm đã xong”. Chỉ xác nhận paid run/release khi đã đọc lại ledger, artefact, số lượng và checksum/build tương ứng.
- Khi người dùng hỏi một việc vận hành nhỏ, xử lý đúng việc đó trước; không chen cả lịch sử nghiên cứu dài vào câu trả lời.

## Mẫu báo cáo ngắn

- **Đã xong:** bằng chứng đã xác minh.
- **Chưa xong:** sản phẩm/kết quả còn thiếu.
- **Vướng ở đâu:** một nguyên nhân cụ thể, nói bằng lời phổ thông.
- **Tiếp theo:** một hành động cụ thể.

Tránh các câu như “gate đạt”, “roster đã khóa”, “schema contract xanh” nếu chưa dịch sang ý nghĩa thực tế cho người đọc.