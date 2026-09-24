# Thử nghiệm gọn để minh chứng ý tưởng trong bài hội nghị 4 trang

## Khi áp dụng

Dùng khi bài bị giới hạn khoảng 4 trang và đóng góp chính là một ý tưởng hoặc quy trình mới. Mục tiêu là tạo **bằng chứng vừa đủ cho ý tưởng**, không biến bài thành một bảng xếp hạng mô hình lớn.

## Nguyên tắc thu gọn

1. Chuyển đóng góp thành 2–3 câu hỏi kiểm chứng trực tiếp.
2. Dùng cùng đầu vào, cùng mô hình và cùng cấu hình cho các phương pháp; chỉ thay phần quy trình cần so sánh.
3. Ưu tiên mẫu nhỏ nhưng ghép cặp theo cùng nguồn. Với tài liệu, phải chia theo tài liệu/cuốn, không chia ngẫu nhiên theo trang hoặc đoạn.
4. Chỉ giữ 3 phương pháp cốt lõi và 4–5 chỉ số gắn trực tiếp với đóng góp.
5. Một bảng kết quả nhỏ và một hình quy trình thường đủ cho bài 4 trang.

## Quy trình với tài liệu chữ–hình

1. Kiểm kê PDF gốc và bản trích xuất; không trộn PDF bản thảo/nghiên cứu vào dữ liệu.
2. Chọn mẫu từ tập kiểm tra đã tách theo nguồn.
3. Dò ngược từng đoạn tới PDF, số trang và ảnh thật.
4. Sửa ánh xạ đường dẫn theo máy hiện tại, rồi kiểm tra tệp tồn tại và tính SHA-256.
5. Không tin riêng cờ `is_multimodal=true` hoặc mô tả hình do máy sinh. Chỉ coi mẫu là chữ–hình khi ảnh thật và liên kết nguồn đã được kiểm tra.
6. Mẫu thiếu ảnh hoặc không dò được nguồn phải bị loại hoặc ghi `BLOCKED`; không tự thay ảnh và không đoán trang.

## Bộ so sánh tối thiểu

- `direct`: tạo câu hỏi và đáp án trực tiếp.
- `answer_first`: tính/khóa đáp án trước rồi viết câu hỏi.
- phương pháp đầy đủ: thêm dấu vết nguồn và gói liên kết chữ–hình.

Dùng một mô hình cho cả ba nhánh. Hai nhánh đối chứng dùng chung hàm lõi thì phải gọi là **biến thể quy trình**, không gọi là triển khai độc lập hoàn toàn.

## Chỉ số phù hợp khi chưa có người chấm

- tỷ lệ đầu ra đúng cấu trúc;
- tỷ lệ liên kết được tới nguồn/ảnh;
- tỷ lệ chạy lại từ nguồn cho kết quả khớp;
- tỷ lệ gói chữ–hình đầy đủ;
- tỷ lệ từ chối và nguyên nhân.

Chấm tự động bằng mô hình chỉ là **đánh giá bằng mô hình**, không phải nhãn chuẩn hay đánh giá chuyên gia. Không tuyên bố chất lượng sư phạm, hiểu hình tốt hơn hoặc ưu thế tổng quát nếu chưa có bằng chứng tương ứng.

## Hai mức xác minh báo cáo

- **Tự nhất quán**: cấu trúc, số liệu và checksum khớp nội bộ. Checksum chỉ phát hiện thay đổi nếu chưa tính lại; không chứng minh nội dung được tạo từ nguồn.
- **Chạy lại từ nguồn**: đọc nguồn, chạy lại quy trình và so toàn bộ báo cáo chuẩn hóa. Chỉ mức này mới chứng minh khả năng tái tạo kỹ thuật.

Luôn thêm kiểm thử phá hoại: sửa đáp án, tính lại mọi checksum, rồi xác nhận nhánh chạy lại từ nguồn vẫn từ chối.

## Cách báo cáo cho người dùng

- Dùng tiếng Việt thuần túy, dân dã; dịch nhãn tiếng Anh ngay khi xuất hiện.
- Nêu `PASS`/`BLOCKED` trước.
- Tối đa khoảng 5 ý chính và một bước kế tiếp.
- Tách rõ: **mã chạy đúng**, **bằng chứng kỹ thuật**, **giá trị khoa học**.
- Sau mỗi lần dùng công cụ phải đọc kết quả và phản hồi, không để câu trả lời rỗng.

## Bẫy thường gặp

- Chọn quá nhiều mô hình/mẫu cho bài ngắn.
- Dùng kết quả cũ không cùng đầu vào/cấu hình làm đối chứng mới.
- Tin đường dẫn cũ như `/content/...` mà chưa ánh xạ sang dữ liệu thật.
- Dùng mô tả ảnh tự động làm đáp án chuẩn.
- Nhúng đường dẫn tuyệt đối vào báo cáo cần chạy ở máy khác; nên truyền nguồn qua tham số khi xác minh.
- Gọi báo cáo checksum là “đã xác minh từ nguồn” dù chưa chạy lại.
