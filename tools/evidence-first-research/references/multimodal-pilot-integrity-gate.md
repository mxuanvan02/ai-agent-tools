# Mẫu thử đa phương thức: kiểm tra đầu vào trước khi gọi mô hình

## Mục tiêu
Khi làm thử nghiệm chữ–hình cho người dùng, tách rõ hai việc:
- **Tệp đầu vào còn nguyên và liên kết đúng**: có thể kiểm tra tự động.
- **Mô hình hiểu ảnh/nội dung đúng**: phải chạy mô hình thật và/hoặc có người đánh giá; không suy ra từ bước kiểm tra tệp.

## Quy trình fail-closed (thiếu gì thì chặn, không bù bằng dữ liệu giả)
1. Lập manifest (bản kê khai đầu vào đã chốt): `chunk_id`, `doc_id`, số ảnh, đường dẫn thật, dung lượng, SHA-256 (mã kiểm tra tệp bị đổi).
2. Sao lưu manifest và tệp nguồn trước khi sửa; ghi SHA-256 của bản sao.
3. Dry-run (chạy thử không gọi mô hình) phải kiểm tra:
   - schema/phiên bản manifest;
   - `record_count` khai báo khớp số record thực;
   - `image_count` khai báo khớp số ảnh thực;
   - ảnh tồn tại, không trùng đường dẫn, dung lượng khớp và SHA-256 khớp.
4. Báo cáo phải ghi riêng `manifest_checks` (lỗi nằm trong bản kê khai) và `checks` (lỗi từng ảnh), cùng trạng thái PASS/BLOCKED.
5. Viết kiểm thử tối thiểu: đầu vào nguyên vẹn PASS; ảnh thay đổi BLOCKED; sai số đoạn BLOCKED; sai số ảnh BLOCKED.
6. Chỉ sau dry-run PASS mới xét chạy mô hình. Nếu thiếu phần cứng, driver, thư viện, hoặc quyền tải mô hình: dừng ở BLOCKED; không tải nặng hay tạo mô tả thay thế để làm số liệu trông có vẻ hoàn tất.

## Cách nói với người dùng
- Mở đầu bằng PASS/BLOCKED và nêu đúng phạm vi đạt/chưa đạt.
- Giải thích thuật ngữ ngay trong ngoặc: manifest (bản kê khai...), dry-run (chạy thử...), SHA-256 (mã kiểm tra...).
- Sau mọi tool call phải xử lý kết quả bằng phản hồi có nội dung; tuyệt đối không gửi câu trả lời rỗng.
- Không gọi “PASS” cho chất lượng mô hình nếu mới chỉ PASS kiểm tra tệp.

## Lỗi dễ phạm
- Chỉ ghi số lượng khai báo trong report nhưng không đối chiếu với danh sách thật.
- Khi VLM lỗi, thay bằng mô tả rỗng/mặc định rồi coi như kết quả thật.
- Dùng mô tả ảnh do máy sinh làm nhãn chuẩn hoặc kết quả đánh giá người.
- Nối nhiều lệnh bằng `&&` làm bước kiểm tra sau không chạy khi bước trước lỗi; với bước nghiệm thu độc lập, chạy riêng hoặc báo rõ bước nào chưa chạy.
