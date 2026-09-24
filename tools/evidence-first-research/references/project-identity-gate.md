# Ngăn nhảy nhầm dự án khi làm nghiên cứu

## Quy tắc chặn trước khi có tác động

Khi phiên chứa nhiều tóm tắt cũ, nhiều thư mục, hoặc nhiều bài báo, không được đoán dự án đang làm chỉ từ tên thư mục hay tệp LaTeX/PDF.

Trước khi đọc sâu, sửa, build, hoặc gửi tệp:

1. Nhắc lại bằng một câu: yêu cầu mới nhất của người dùng, thư mục gốc, và artifact cần làm.
2. Đối chiếu với câu lệnh người dùng mới nhất; tóm tắt lịch sử chỉ là bối cảnh, không phải lệnh tiếp tục.
3. Nếu có hơn một ứng viên hoặc artifact chưa rõ: hỏi lại. Chỉ được kiểm tra ở chế độ đọc; không sửa, build hay gửi.
4. Trước khi tuyên bố “xong”, “bản cuối” hay gửi tệp, đối chiếu lại đường dẫn, tên dự án và nội dung artifact với mục tiêu đã chốt.

## Nếu đã tác động nhầm luồng

Dừng ngay. Báo ngắn, rõ: tệp nào đã bị đọc/sửa/build/gửi; backup nằm ở đâu; có thể hoàn tác bằng cách nào. Không tiếp tục cải thiện hay build thêm ở luồng sai.

## Kiểm tra trước khi gọi model bên ngoài

Chỉ gửi nội dung dự án sau khi đã chốt đúng dự án. Nếu gọi model để rà bản thảo, yêu cầu model chỉ phản biện trước; đối chiếu mọi nhận xét với số liệu gốc rồi mới sửa.
