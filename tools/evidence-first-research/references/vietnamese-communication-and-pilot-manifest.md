# Giao tiếp và tạo hồ sơ thử nghiệm nhỏ

## Điều người dùng đã chốt

- Trả lời bằng tiếng Việt thuần túy, dân dã.
- Mỗi cụm chuyên môn lần đầu phải giải nghĩa ngay trong ngoặc. Ví dụ: **manifest** (bản kê khai đầu vào đã chốt), **SHA-256** (mã kiểm tra để phát hiện tệp bị thay đổi), **baseline** (cách làm đối chiếu), **structural pilot** (thử xem quy trình chạy và liên kết dữ liệu có đúng không).
- Nêu trạng thái **PASS/BLOCKED** trước; chỉ sau đó mới nói chi tiết.
- Không để thuật ngữ tiếng Anh đứng một mình rồi mới giải thích về sau.

## Cách tạo manifest cho thử nghiệm dữ liệu–hình ảnh gọn

1. Chỉ đọc và xác nhận mã đoạn đầy đủ; không ép `chunk_id` dạng chữ thành số.
2. Đối chiếu mỗi mẫu với nguồn: tài liệu, mã đoạn, mục, số ảnh.
3. Đổi đường dẫn cũ sang đường dẫn hiện hành theo quy tắc rõ ràng; mỗi ảnh phải khớp đúng một tệp. Không có ảnh hoặc nhiều ảnh trùng khớp thì BLOCKED, không tự thay tệp khác.
4. Sao lưu các tệp nguồn trước khi ghi tệp mới, và lưu SHA-256 của tệp nguồn cùng từng ảnh.
5. Tạo manifest riêng, không sửa manifest tổng hoặc ghi đè tệp đã có. Tự đọc lại để đếm số đoạn, số ảnh, số đường dẫn và số SHA-256.
6. Ghi giới hạn ngay trong manifest: việc ảnh tồn tại và có mã kiểm tra chỉ chứng minh liên kết/tái lập được; không chứng minh mô tả ảnh đúng, mô hình hiểu ảnh, hay hệ thống tốt hơn.

## Ví dụ phiên làm việc

Tập mẫu gồm 8 đoạn và 10 ảnh được ghi trong `pilot_evaluation_manifest.json`. Đây là chi tiết phiên cụ thể, không được coi là dữ liệu chuẩn hay kết quả đánh giá khoa học.
