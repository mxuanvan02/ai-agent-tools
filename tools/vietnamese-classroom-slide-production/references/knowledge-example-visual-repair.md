# Sửa slide bị lẫn kiến thức, ví dụ và nhiệm vụ

## Bài học từ phản hồi BAI_02/03

Giáo viên phê bình nội dung mang màu sắc nội bộ, giao học sinh “làm”, thiếu hình giải thích và biến ví dụ thành điều bắt buộc. Cách sửa sai đã xảy ra: chỉ đổi từ cấm, đổi nhãn ghi vở thành “ví dụ”, rải icon trên bảng rồi báo sạch bằng checksum/đếm chữ. Không dùng các bản này làm baseline sư phạm đã duyệt.

## Quy trình sửa theo ý nghĩa

1. Lập bảng theo từng slide: kiến thức chính, ví dụ minh hoạ, lời tổ chức hoạt động, hình giải thích. Chuyển lời giao việc sang tài liệu hoạt động; thay slide đó bằng kiến thức liên quan, không chỉ thêm “gợi ý”.
2. Viết ghi vở bằng các mệnh đề tổng quát, độc lập với ví dụ. Ví dụ: “Sao lưu là tạo bản sao dữ liệu để khôi phục khi bản gốc gặp sự cố”, không phải “Đủ 12 tệp và 45 MB mới đạt”.
3. Dựng hình thể hiện quan hệ: cảm biến → chương trình → kết quả; thư mục nguồn → bản sao USB; bản sao thiếu một tệp; yêu cầu tháo → hoàn tất truy cập → xác nhận của hệ điều hành. Dữ liệu minh hoạ phải được nhận diện là minh hoạ, không giả làm kết quả đo.
4. Rà tất cả nơi lặp kiến thức: thân bài, ghi vở, bảng, nhãn hình, bìa, kết luận và notes. Không sửa câu tổng quát rồi giữ ví dụ phủ định chính câu ấy.
5. Build theo chuỗi phụ thuộc có kiểm tra mã thoát: compile → PPTX → PDF → trích xuất → render → sửa → kiểm tra lại. Lỗi build phải dừng chuỗi, không lấy PDF/PPTX cũ làm kết quả mới. Chỉ gửi bản duyệt sau kiểm tra; cập nhật Drive là thao tác riêng cần đúng phạm vi được duyệt.

## Các phân biệt kiến thức phải giữ

- Đầu vào–xử lí–đầu ra mô tả xử lí thông tin; không đồng nghĩa với khả năng tự điều chỉnh hoặc vòng phản hồi. Không lấy “không tự điều chỉnh” làm lí do duy nhất kết luận không xử lí thông tin.
- Đèn thiết bị nháy có thể biểu thị đọc hoặc ghi, tuỳ thiết kế. Đèn tắt không thay thế xác nhận tháo an toàn của hệ điều hành. Ngắt khi đang ghi *có thể* gây mất/hỏng dữ liệu, không khẳng định mọi lần rút đều hỏng.
- Số tệp và dung lượng trùng chỉ là đối chiếu ban đầu, không chứng minh nội dung giống nhau. Kiểm tra khả năng mở/nội dung hoặc đối chiếu dữ liệu phù hợp với mức bài học.
- Nêu rõ hệ đơn vị dung lượng: GB/MB thập phân khác GiB/MiB nhị phân. Nếu nguồn dùng quy ước khác, giải thích rõ và kiểm phép tính thật; không đổi quy ước một slide mà để kết quả cũ ở ghi vở.
- Đồng bộ có thể lan truyền thao tác xoá, không tự động thay thế bản sao lưu độc lập.

## Kĩ thuật và báo cáo

- Tham số keyword phải nằm ngoài list: `note_slide(s, BLUE, ['Ý 1', 'Ý 2'], heading='NỘI DUNG GHI VỞ')`. Compile sau cả nhóm sửa, không rebuild từng thay thế nhỏ.
- Kiểm tên icon từ cấu hình bộ render và kho thật trước khi dùng; không đoán đường dẫn hoặc thay bằng vật thể sai nghĩa chỉ để build chạy. Pattern tên động phải được mở rộng trước kiểm tra tồn tại.
- Mọi sửa helper dùng chung cần backup và xác định bài nào chịu tác động. Sửa riêng bài khi thay đổi không phải quy tắc chung; không vô tình xoá nguồn cần thiết khỏi các bài khác.
- `so_van_de = 0` của ink checker chỉ nghĩa không phát hiện chữ cắt theo phép đo đó. Nó không xác nhận hình kể chuyện, tính đúng kiến thức, độ dễ đọc hoặc không có nhiệm vụ trá hình.
- Khi thông báo tiến độ, nêu phần vừa sửa và phần chưa đạt. Không lặp “đang vá ngay” qua nhiều lượt, không đánh dấu hoàn thành nếu còn hình hoặc nội dung chưa xử lí. Lỗi công cụ/subagent không phải bằng chứng công việc đã chạy.
