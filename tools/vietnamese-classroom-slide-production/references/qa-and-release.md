# QA và phát hành

## Fingerprint nguồn

Trước khi sửa, ghi lại: đường dẫn/tên file, SHA-256 hoặc kích thước, số slide, tỉ lệ trang, tiêu đề bìa và chuỗi đại diện ở vài slide. Nếu có nhiều file gần tên, không tự chọn theo suy đoán.

## Cổng cấu trúc

Kiểm tra trên file PPTX cuối:

- ZIP/OOXML hợp lệ; đúng tỉ lệ 16:9.
- Số slide đúng bản đồ bài học.
- Notes không rỗng trên mọi slide nội dung.
- Không có shape vượt biên, placeholder, chuỗi `\\n`, chữ rác hoặc nội dung từ bài khác.
- Không có nhãn/cụm bị cấm; dấu hỏi chỉ nằm ở phần bài tập được phép.

## Cổng hình ảnh

1. Xuất PDF từ PPTX cuối và đối chiếu số trang.
2. Render toàn bộ slide thành ảnh; tạo contact sheet.
3. Xem riêng slide dày nhất, ví dụ mới, bảng/biểu đồ và slide có chữ nhỏ.
4. Phân loại: P0 = chồng/cắt/mất chữ; P1 = khó đọc, tương phản thấp, ngắt dòng hoặc phân cấp sai.
5. Sửa nguyên nhân, dựng lại PPTX/PDF và kiểm tra lại. Không phát hành khi còn P0/P1.

## Quy ước tên phát hành

Dùng tên ổn định, không chứa trạng thái nội bộ như `LAM_LAI`, `FINAL`, `NEW`:

- PPTX: `BAI_XX_<TEN_BAI_KHONG_DAU>.pptx`
- PDF đối chiếu: `BAI_XX_<TEN_BAI_KHONG_DAU>.pdf`

Giữ số bài hai chữ số nếu cả thư mục dùng chuẩn đó; nếu thư mục hiện hành có quy ước khác, ưu tiên tính nhất quán của toàn bộ thư mục.

## Cập nhật Drive an toàn

- Liệt kê đúng thư mục và nhận diện file cũ bằng tên, kích thước, thời gian sửa.
- Tải bản mới lên tên tạm hoặc thư mục staging trước khi thay thế nếu backend không hỗ trợ versioning rõ ràng.
- Giữ một bản phục hồi có timestamp hoặc dựa vào Trash/version history; không xóa vĩnh viễn.
- Sau upload, đọc lại metadata/kích thước và so sánh với file local.
- Chỉ báo thành công khi file đích tồn tại và kiểm tra đọc lại đạt yêu cầu.

## Báo cáo theo lô

Với bộ nhiều bài, báo cáo ngắn theo bảng: bài, nguồn, số slide, notes, QA, tên Drive, trạng thái. Không tuyên bố “đã làm hết” khi chỉ mới tạo script hoặc bản dựng trung gian.