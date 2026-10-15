# Chèn ẢNH THẬT vào deck đang có: 6 luật đã trả giá

Khác việc dựng deck mới: ở đây slide đã đầy chữ, chỉ còn một rãnh trống. Cả 6 luật
dưới sinh ra từ một lần hỏng thật trong phiên thêm ảnh terminal vào BAI_29
(2026-10-15), không phải suy đoán. Script tham chiếu: `upgrade_bai29.py`,
`geom_check29.py`, `audit_picture_footer.py` trong workspace slide.

1. **Đo shape phải ĐỆ QUY vào GROUP.** Bản đo đầu chỉ đọc `sh.has_text_frame` ở cấp
   ngoài, mà mọi shape trên slide là GROUP → báo "0 hộp cần sửa". Đó là FAIL-OPEN:
   kết luận "không có gì để làm" từ một phép đo không thấy gì — cùng lớp lỗi với
   `verify_s18` từng in "ĐẠT" trên danh sách rỗng. Trước khi tin một bộ đếm bằng 0,
   phải chứng minh bộ đếm NHÌN THẤY dữ liệu (in tổng số shape có chữ).
2. **Sửa chữ trong GROUP bằng cách VIẾT LẠI `run.text`, không xoá shape.**
   `tf.text = ...` xoá sạch định dạng mọi run; đặt `para.runs[0].text = mới` rồi làm
   rỗng các run sau thì giữ nguyên font và geometry → khung trống đã đo vẫn đúng,
   không tạo lỗ hổng bố cục.
3. **Bảng từ khoá phải có BIẾN THỂ CÓ TIỀN TỐ.** Cổng bắt câu `Trao đổi phiếu, …`
   nhưng trên slide là `2 phút · Trao đổi phiếu, …` nên lọt qua; một cột bảng
   (`Sản phẩm nộp`, `Tệp B29_NhomXX`) cũng lọt vì chỉ liệt kê mẫu hẹp. Cách an toàn:
   cho cổng bắt RỘNG (mọi chữ `PHIẾU`/`TỆP`/`VỞ`) rồi để script ABORT khi gặp câu
   chưa có trong bảng — chạy thử trên BẢN COPY trước (kiểm sha deck thật không đổi)
   để cổng phơi câu sót, thay vì tin là đủ.
4. **KHUNG TRỐNG CHẠM FOOTER — phải trừ lề, và trừ cả chỗ caption.** Khung đo được
   tới y=7.00 đúng bằng mép trên footer, nên "cho ảnh ăn hết chiều cao khung" là ảnh
   đè footer; caption đặt DƯỚI ảnh rơi xuống 7.03. Đã xảy ra ở 5/6 slide mà cả
   vision lẫn cổng chữ trong ảnh đều không bắt được — chỉ đo geometry mới ra. Sửa:
   `cao_khả_dụng = min(khung, FOOTER_Y - 0.15 - y_khung) - (CAPTION_H + 0.03 nếu có)`,
   và đặt CỔNG HÌNH HỌC trong script (`raise SystemExit` nếu đáy > giới hạn, ảnh vượt
   mép ngang) để nó tự FAIL thay vì ghi deck xấu. Verify lại bằng script đo độc lập
   đọc file ĐÃ LƯU (so sha1 blob ảnh, tính đáy ảnh/caption vs FOOTER_Y tìm theo chữ).
5. **Giới hạn bề ngang ảnh, không chỉ chiều cao.** Ảnh AR lớn (3.15) đặt theo chiều
   cao khung phình ngang 11.39in = 85% khung; vision chê "ảnh quá khổ khiến hộp nội
   dung phía trên bị lép". Trần 72% khung ngang là điểm cân bằng đã duyệt bằng mắt
   (S24: 11.39 → 9.58in, chữ vẫn 23.1pt).
6. **Script chèn ảnh KHÔNG idempotent — chạy lại là thêm ảnh THỨ HAI chồng lên.**
   Trước mỗi lần chạy lại phải `cp -p` từ backup, và verify bằng cách đếm shape
   (145 → 147 → 153 đúng bằng số lần chạy là dấu hiệu đã bị chèn trùng).

## Detector tự viết phải tự kiểm chứng trước khi kết luận về deck người khác

Bộ dò "caption đè footer" (chữ >60 ký tự, cao <0.6in, nằm dưới một ảnh) đã bắt trúng
CHÍNH HỘP CHỮ FOOTER — footer cũng >60 ký tự, cao 0.26in và luôn có ảnh phía trên.
Kết quả: **1083 vi phạm trên 34 deck đã phát hành**, mỗi slide đúng 1 lỗi. Ba dấu hiệu
nhận ra báo động giả: (a) số lỗi == số slide, (b) mọi vi phạm cùng một geometry
(`5.32x0.26in @y=7.05`), (c) đáy 7.30 vẫn nhỏ hơn chiều cao slide 7.50. Sau khi loại
shape nằm trong dải footer (`top >= FOOTER_Y - 0.05`): **0/1221 ảnh vi phạm, 34/34
deck sạch**. Luật: một detector mới PHẢI chạy trên mẫu đã biết sạch và mẫu đã biết lỗi
trước khi dùng số của nó để kết luận về kho đang phát hành; và khi số lỗi tỉ lệ thuận
với số slide thì nghi tool trước, nghi deck sau.

## Vision timeout thì kiểm bằng LỆNH, không bỏ qua ca đó

`vision_analyze` trên ảnh slide render đã timeout nhiều lần (kể cả bản thu 1100px).
Không được kết luận "đạt" cho ca đó chỉ vì không xem được: nội dung ảnh đã xác nhận
ở cấp strip TRƯỚC khi chèn (cùng một file, so sha1), phần còn lại (đè chữ, vượt mép,
caption tràn, chạm footer) là HÌNH HỌC thì đo bằng python-pptx chính xác hơn mắt.
Ngược lại, ca bị cổng OCR đánh dấu FRAGILE thì BẮT BUỘC xem pixel — cổng đã nói rõ
không được tự kết luận (b29_05: vision xác nhận đủ 3 nội dung, OCR chỉ đọc sót).
