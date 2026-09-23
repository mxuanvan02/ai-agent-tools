# Giữ trục bài và bằng chứng thí nghiệm khi review manuscript

## Mục đích
Dùng khi review/sửa manuscript nghiên cứu của người dùng, nhất là khi bài đã có mục tiêu, đóng góp, phương pháp và dữ liệu/kết quả nằm ở các repo hoặc thư mục khác nhau.

## Sai lầm phải tránh
Không được suy từ **repo public/release artifact** rằng đó là toàn bộ dữ liệu hay toàn bộ thí nghiệm của nghiên cứu. Repo công khai có thể chỉ chứa mã, fixture tổng hợp và kiểm thử; dữ liệu nghiên cứu, manifest, split, nhãn người và kết quả có thể nằm ở workspace nội bộ khác.

Không được "làm sạch" manuscript bằng cách cắt phần thí nghiệm/minh hoạ chỉ vì chưa kiểm kê toàn bộ dữ liệu và kết quả nội bộ. Chỉ bỏ claim sau khi đã xác định rõ claim đó không có bằng chứng, không đúng vai trò mục, hoặc không được phép công bố.

## Cổng bắt buộc trước khi sửa experiment/limitations/conclusion
1. Viết lại bằng 1–3 câu: mục tiêu, câu hỏi nghiên cứu, đóng góp và loại bài (method, empirical, protocol, artifact). Nếu không chắc, đọc lại abstract, introduction, method và yêu cầu người dùng xác nhận thay vì tự đổi định vị bài.
2. Lập **bản đồ bằng chứng** trước mọi cắt/sửa lớn:
   - manuscript/source hiện hành;
   - repo public/release artifact;
   - workspace nghiên cứu nội bộ;
   - manifest/dataset statistics/splits;
   - script runner và result files;
   - bảng human evaluation/annotation;
   - quyền dùng và quyền công bố từng loại dữ liệu.
3. Đối chiếu từng claim với bằng chứng cụ thể: đường dẫn + trường/số liệu + script/test/log tạo ra nó.
4. Phân loại rõ:
   - **đã có bằng chứng và được phép dùng**;
   - **đã có nhưng chỉ là pilot/minh hoạ**;
   - **đã có nhưng chưa được chấm/đối chứng/kiểm chứng**;
   - **không có hoặc không được phép công bố**.
5. Chỉ sau đó mới quyết định: giữ, hạ giọng, chuyển mục, hay bỏ.

## Quy tắc vai trò từng mục
- **Abstract:** vấn đề, cách làm, đóng góp, quy mô/kết quả chỉ khi kiểm chứng được; không nhét diễn giải về quyền, link code hay nhật ký chạy.
- **Introduction:** khoảng trống, câu hỏi nghiên cứu, đóng góp; phải khớp experiment thực tế.
- **Method:** mô tả phương pháp và biến/điều kiện; không biến cảnh báo giới hạn thành phương pháp.
- **Experiments:** dữ liệu, chia tập, cách chọn mẫu, baseline, kịch bản, metric, người chấm, thống kê và kết quả. Kịch bản kiểm thử mã chỉ là một tiểu phần của thực nghiệm/hệ thống, không thay thế đánh giá dữ liệu.
- **Limitations:** giới hạn của bằng chứng và phạm vi suy luận; không chứa link code hoặc lời thanh minh vận hành dài.
- **Code Availability/Acknowledgment:** link mã, nguồn hỗ trợ, hạ tầng; tuân theo quy tắc ẩn danh/camera-ready của hội nghị.
- **Conclusion:** trả lời đúng câu hỏi nghiên cứu theo mức bằng chứng; không nâng pilot hay test kỹ thuật thành hiệu quả khoa học.

## Với dữ liệu đa phương thức
Luôn báo riêng, không gộp lẫn:
- tổng số tài liệu, ngữ cảnh, QA;
- số mục đa phương thức, số ảnh và tỷ lệ;
- phân bố theo train/dev/test ở cấp tài liệu nguồn;
- số mục đã chấm người, số annotator, double annotation, adjudication;
- số baseline/ablation đã chạy thực tế;
- phần nào là pilot, phần nào đủ để suy luận.

Nếu tập lớn chủ yếu là text-only còn multimodal rất nhỏ, phần multimodal chỉ được gọi là pilot/controlled case study trừ khi có thiết kế và cỡ mẫu đủ khác. Không dùng metric tự động mặc định 1.0 làm bằng chứng chất lượng nếu chưa truy nguyên định nghĩa metric và cách tạo nhãn.

## Kiểm tra yêu cầu hội nghị
Trước khi nói "sẵn sàng nộp", lấy trang Author Guidelines/CFP chính thức, kiểm checklist gồm: giới hạn trang, template/font/khổ giấy, ẩn danh, yêu cầu PDF eXpress, copyright, link/URL, supplementary, deadline và hệ thống nộp. Không dùng kết quả tìm kiếm mơ hồ của hội nghị trùng tên.

## Cách báo cho người dùng
- Nói trạng thái và bằng chứng trước: số dữ liệu nào có, ở đâu, dùng được để trả lời câu hỏi nào.
- Tiếng Việt ngắn, dân dã; giải nghĩa thuật ngữ khi dùng.
- Không tự chuyển mục tiêu bài chỉ vì một repo nhỏ hơn hoặc dễ kiểm tra hơn.
- Nếu đã dùng công cụ, trả lời kết quả ngay; không để phản hồi rỗng.
