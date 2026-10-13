# Di chuyển cả bộ bài theo PPCT và phát hành an toàn

## Sổ ánh xạ nguồn–đích

Khi số bài trong PPCT hiện hành khác số bài của deck/KHBD cũ, lập một dòng ánh xạ trước khi dựng:

| Trường | Nội dung cần khóa |
|---|---|
| Số bài phát hành mới | Ví dụ: Bài 04 |
| Mục/chủ đề PPCT | Tên và số mục chính xác |
| Tuần, tiết | Đối chiếu PPCT/KHDH |
| Deck nguồn | Đường dẫn, SHA-256, số slide, tỉ lệ |
| KHBD nguồn | Đường dẫn, tiêu đề, số liệu bắt buộc |
| Tên tệp phát hành | Tên ổn định theo thư mục đích |
| Mã sản phẩm học tập | Đổi theo số bài mới nếu KHBD/đợt phát hành yêu cầu |

Số thứ tự trong tên deck cũ chỉ là định danh nguồn, không tự động là số bài phát hành. Khi PPCT, KHBD và deck mâu thuẫn, dùng PPCT/KHDH hiện hành để xác định tuyến bài; dùng KHBD tương ứng làm nguồn nội dung; dùng deck hiện hành chủ yếu để kế thừa nhận diện và đối chiếu.

## Khóa số liệu và dấu vết cũ

Tạo danh sách neo bắt buộc trước khi viết, gồm số lượng, đơn vị, tên/mã sản phẩm, tiêu chí bảng và đối tượng trong sơ đồ. Sau khi dựng, quét cả nội dung hiển thị lẫn speaker notes để tìm:

- số liệu của bài cũ;
- số bài, số mục và mã nhóm cũ;
- thuật ngữ ngoại ngữ không cần thiết;
- tên bài hoặc footer kế thừa;
- câu hỏi xuất hiện ngoài khối luyện tập/vận dụng được phép.

Dùng ranh giới từ/số khi quét để tránh khớp giả, chẳng hạn `24 MB` không được suy ra chỉ vì chuỗi `1024 MB` chứa các chữ số gần nhau.

## Kiểm tra ký hiệu và ngắt dòng sau render

Không xem text extraction là bằng chứng hiển thị. Sau khi xuất PDF, kiểm tra riêng:

- ký hiệu dễ bị thay glyph hoặc đọc sai khi chiếu; trong tiêu đề/footer tiếng Việt, ưu tiên viết `Mục 2.8` thay cho `§2.8` nếu bản render làm ký hiệu không rõ;
- cụm nghĩa không được tách vụn, tên dịch vụ, đơn vị, mã nhóm và thuật ngữ hai tiếng;
- số trang hai chữ số, footer và nhãn hẹp;
- slide vừa sửa ở độ phân giải đầy đủ.

Một sửa đổi typography chỉ được chấp nhận sau khi dựng lại PPTX, PDF và ảnh của chính slide bị ảnh hưởng.

## Phát hành từng bài như một giao dịch

1. Xác định đúng cặp PPTX/PDF đang có ở thư mục phát hành.
2. Sao lưu bản hiện hành vào local và vùng lưu trữ Drive có timestamp; không xóa vĩnh viễn.
3. Tải cặp tệp mới lên đúng tên ổn định.
4. Tải ngược từng tệp từ Drive và tính SHA-256.
5. Chỉ đánh dấu bài hoàn tất khi checksum tải ngược trùng bản local và QA ghi nhận đúng số slide/notes/PDF pages.
6. Cập nhật bảng tiến độ ngay sau mỗi bài, rồi mới chuyển sang bài tiếp theo.

Nếu chưa có tệp cũ cùng tên, ghi rõ trạng thái “không có bản hiện hành để sao lưu” thay vì suy đoán thao tác sao lưu đã diễn ra.

## Mẫu báo cáo ngắn theo bài

`Bài XX — nguồn đã khóa | N slide/N notes | PDF N trang | P0/P1: 0 | Drive: đã phát hành | SHA-256: khớp`.
