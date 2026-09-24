# Review manuscript an toàn khi luồng có nhiều dự án

## Mục đích
Ngăn việc lấy nhầm bài, nhầm thư mục, hoặc gửi nhầm PDF khi lịch sử hội thoại có nhiều dự án nghiên cứu.

## Bắt buộc trước khi đọc sâu, sửa, build hoặc gửi
1. **Chốt danh tính artefact từ yêu cầu mới nhất.** Ghi lại: tiêu đề bài, tệp/ZIP người dùng vừa đưa, thư mục làm việc tách riêng, và tệp nguồn chính.
2. **Không suy từ tóm tắt ngữ cảnh cũ.** Tên repo, đường dẫn, PDF hoặc danh sách việc trong context chỉ là manh mối; phải kiểm tra lại hoặc hỏi người dùng.
3. **Khi nhận ZIP:** kiểm tra danh sách tệp và đường dẫn bất thường trước; giải nén vào thư mục review mới, không ghi đè bản gốc; ghi checksum cho `main.tex`, PDF, hình và BibTeX.
4. **Trước side effect:** nhắc lại một dòng “đang review/sửa bài [TITLE] trong [WORKDIR]”. Nếu title/path không khớp, dừng ngay.
5. **Trước gửi:** kiểm tra PDF được gửi có cùng thư mục review, checksum đã báo, và tiêu đề trang đầu đúng title đã chốt. Không gửi chỉ vì PDF vừa build thành công.

## Rà manuscript bằng model qua OmniProxy
- Model review chỉ là phản biện phụ; không được thay kiểm tra số liệu, nguồn và PDF.
- Xác minh trước bằng yêu cầu chữ cực ngắn và ghi cả `requested_model`, `returned_model`, HTTP status. Nếu router trả model khác, không coi kết quả là review từ model đã chọn.
- Dùng đúng API/khuôn payload đã xác minh; không tự sửa cấu hình router khi chưa được yêu cầu.
- Gửi phần nhỏ, có giới hạn thời gian. Nếu gọi API treo/lặp lỗi, dừng vòng lặp, ghi BLOCKED, và tiếp tục review cục bộ thay vì tuyên bố model đã phản biện.
- Không gửi ảnh/tài liệu nguồn cho API trước khi kiểm tra thử bằng payload vô hại nếu cần ảnh.

## Quy tắc báo cáo
- Mỗi lần dùng công cụ phải tóm kết quả ngay; không nói “đã chạy” nếu tool chưa có bằng chứng.
- Dùng tiếng Việt dễ hiểu; giải thích thuật ngữ như checksum, provenance, semantic gate ngay lần đầu.
- Tách rõ: PASS kỹ thuật (build/checksum/test) khác PASS khoa học (bằng chứng, nhãn người, đánh giá hiệu quả).

## Mẫu chốt trước khi gửi
`PASS kỹ thuật: PDF build thành công. BLOCKED khoa học (nếu có): ... . Xác nhận tệp gửi: <path>, SHA-256: <hash>, title trang đầu: <title>.`
