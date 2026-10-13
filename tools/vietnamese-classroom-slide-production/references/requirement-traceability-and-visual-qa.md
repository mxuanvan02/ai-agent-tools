# Truy vết yêu cầu và QA trực quan cho deck bài dạy

## 1. Ma trận truy vết trước khi dựng

Với mỗi yêu cầu bắt buộc trong KHBD/PPCT, lập một hàng gồm:

| Yêu cầu nguồn | Số liệu/định dạng khóa | Slide trình bày | Minh chứng trực quan | Slide luyện tập/đánh giá | Chuỗi cần quét |
|---|---|---|---|---|---|
| Ví dụ: phân biệt vectơ–điểm ảnh | phóng đại 400% | khái niệm + so sánh | cùng một hình ở hai cách biểu diễn | hai ca kiểm tra | `400%`, `vectơ`, `điểm ảnh` |
| Ví dụ: tạo hình bằng công cụ cơ bản | đúng 4 hình | sản phẩm + hướng dẫn | từng hình được đánh số, gọi tên | kiểm đếm trong rubric/bài tập | `4 hình`, tên từng hình |
| Ví dụ: lưu định dạng gốc | mã tệp theo KHBD | tệp nguồn và bản xuất | sơ đồ SVG/định dạng gốc → PNG/PDF | mở lại tệp để kiểm tra | mã nhóm, phần mở rộng |

Không xem deck cũ là bằng chứng đáp ứng KHBD chỉ vì deck mở được, đủ notes hoặc có bố cục đẹp. Kiểm tra riêng ba tầng:

1. **Đúng nguồn:** PPCT/KHBD, số bài, mã nhóm, số liệu và sản phẩm.
2. **Đủ nội dung:** từng yêu cầu bắt buộc có slide trình bày, minh chứng và nơi đánh giá.
3. **Đúng hình thức:** phần kiến thức là câu khẳng định; câu hỏi chỉ nằm ở hoạt động/bài tập được phép.

Nếu deck cũ có mạch tốt nhưng lệch nhiệm vụ, chỉ kế thừa nhận diện và layout hữu ích; không vá rải rác nội dung cũ.

## 2. Minh họa nội dung kỹ thuật

- Dùng hình ảnh để chứng minh hiện tượng, không chỉ dùng thẻ chữ mô tả hiện tượng.
- Với so sánh vectơ–điểm ảnh, nên đặt cùng một đối tượng ở cùng mức phóng đại; thể hiện lưới pixel/răng cưa ở bản điểm ảnh và đường cong/điểm neo ở bản vectơ.
- Nếu không có phần mềm đích hoặc không xác định được phiên bản giao diện, dùng sơ đồ giao diện native PowerPoint có nhãn rõ; không giả mạo ảnh chụp màn hình.
- Khi yêu cầu “đúng N hình”, tách từng hình, đánh số và gọi tên; không tính các thẻ bố cục hay ký hiệu chú thích vào sản phẩm.
- Phân biệt rõ tệp nguồn chỉnh sửa được với bản xuất dùng để trình chiếu/chia sẻ; yêu cầu mở lại tệp nguồn là một ca kiểm tra hữu ích.

## 3. Xử lý cảnh báo từ contact sheet

Contact sheet dùng để phát hiện lỗi toàn cục, không phải nguồn kết luận cuối cho chữ nhỏ hoặc thuật ngữ.

Quy trình xác minh:

1. Ghi lại số slide và nghi ngờ cụ thể từ contact sheet.
2. Quét văn bản PPTX/notes bằng đúng cụm từ và các biến thể chính tả.
3. Render riêng slide nghi ngờ ở kích thước lớn.
4. Chỉ ghi nhận P0/P1 khi văn bản hoặc ảnh cỡ lớn xác nhận.
5. Nếu cảnh báo là giả do thu nhỏ, không sửa nội dung chỉ để “chiều” contact sheet.

Các ứng viên nên xem cỡ lớn: bảng nhiều chữ, minh họa kỹ thuật, slide có nhãn nhỏ, ký hiệu/glyph, sản phẩm cần kiểm đếm, hai ca kiểm tra, bài tập cuối bài.

## 4. Cổng QA tối thiểu

- PPTX mở được và là ZIP hợp lệ.
- Tỉ lệ 16:9; PPTX/PDF cùng số trang.
- Notes không rỗng trên mọi slide.
- Không placeholder, đối tượng ngoài biên, tràn chữ hoặc nội dung bài cũ.
- Quét riêng số bài cũ, header cũ, mã nhóm cũ, số liệu cũ và tên nhiệm vụ cũ.
- Xác nhận bằng ảnh cỡ lớn các slide trọng yếu sau contact sheet.
- Có ít nhất một vòng sửa hoặc xác minh có chủ đích rồi dựng/QA lại trước phát hành.
- Chỉ phát hành sau khi sao lưu bản cũ và tải ngược đối chiếu SHA-256.