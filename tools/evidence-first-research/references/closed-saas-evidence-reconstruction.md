# Nghiên cứu hệ thống SaaS đóng — từ tài liệu công khai đến mô hình kỹ thuật

Dùng khi cần phân tích một sản phẩm web/SaaS nhưng không có mã nguồn hoặc quyền truy cập nội bộ; ví dụ hệ thống xếp lịch, LMS, ERP hoặc công cụ tối ưu vận hành.

## Mục tiêu

Tạo báo cáo có bằng chứng mà không biến suy luận kiến trúc/thuật toán thành tuyên bố về nội bộ nhà cung cấp.

## Quy trình

1. **Chốt đúng sản phẩm và phạm vi**
   - Xác định tên miền chính, tên miền ứng dụng con và đối tượng sử dụng.
   - Giới hạn câu hỏi nghiên cứu: luồng nghiệp vụ, dữ liệu đầu vào, ràng buộc, đầu ra, thao tác thủ công, hay thuật toán.

2. **Ưu tiên nguồn bên thứ nhất**
   - Trang sản phẩm chính thức.
   - Trung tâm trợ giúp, FAQ, bài hướng dẫn, video chính thức và trang mẫu/demo.
   - Tìm liên kết ngay trong DOM/trang trợ giúp trước khi dùng công cụ tìm kiếm bên ngoài.
   - Nếu máy tìm kiếm chặn bot hoặc trả kết quả nhiễu, chuyển sang điều hướng trực tiếp website, không suy diễn rằng tài liệu không tồn tại.

3. **Trích xuất nội dung động có hệ thống**
   - Dùng snapshot để nhận diện mục và liên kết.
   - Khi snapshot bị cắt hoặc giao diện ẩn nội dung, đọc `document.body.innerText`, lọc anchor theo từ khóa và lấy `href` trực tiếp từ DOM.
   - Với video, ưu tiên mô tả/trang hướng dẫn đi kèm; chỉ dùng nội dung video khi đã lấy được transcript đáng tin cậy.

4. **Lập bảng chứng cứ trước khi mô hình hóa**

   | Claim | Nguồn | Trích dẫn/tóm tắt sát nghĩa | Mức tin cậy |
   |---|---|---|---|
   | Tính năng được công bố | URL chính thức | Nội dung trực tiếp | Đã xác minh |
   | Cách vận hành suy ra | Nhiều hành vi/tài liệu | Chuỗi lập luận | Suy luận kỹ thuật |
   | Thuật toán nội bộ | Không có tài liệu | Không khẳng định | Chưa biết |

5. **Tái dựng luồng nghiệp vụ**
   - Xác định thứ tự phụ thuộc dữ liệu, ví dụ: danh mục → cấu hình mẫu → đối tượng cụ thể → phân công → sinh tác vụ → chạy bộ giải → chỉnh sửa.
   - Ghi rõ bước nào là nhập liệu, kiểm tra tính khả thi, tự động hóa và human-in-the-loop.

6. **Mô hình hóa có ranh giới bằng chứng**
   - Có thể diễn giải thực thể, biến quyết định, ràng buộc cứng/mềm và hàm mục tiêu như một mô hình kỹ thuật hợp lý.
   - Mọi phần như vậy phải gắn nhãn **“phân tích/suy luận kỹ thuật, không phải kiến trúc nội bộ đã được nhà cung cấp xác nhận.”**
   - Không suy tên thuật toán từ nhãn marketing như “AI”, “thông minh” hoặc “tối ưu”. Chỉ nêu CP-SAT, ILP, genetic algorithm… khi có nguồn trực tiếp.

7. **Kiểm tra các trường hợp biên**
   - FAQ thường cung cấp bằng chứng tốt nhất về vô nghiệm, dữ liệu sai, ràng buộc quá chặt và cơ chế xử lý thủ công.
   - Tách rõ: hệ thống chặn lỗi, cảnh báo, để tác vụ chưa xếp, tự nới ràng buộc, hay yêu cầu người dùng sửa.

8. **Báo cáo theo tầng**
   - Kết luận nhanh.
   - Phạm vi và tính năng đã xác minh.
   - Quy trình nghiệp vụ.
   - Ràng buộc và mô hình dữ liệu.
   - Phần suy luận kỹ thuật.
   - Hạn chế/chưa xác minh.
   - Kế hoạch kiểm thử thực nghiệm.
   - Danh sách URL nguồn chính thức.

## Mẫu áp dụng: hệ thống xếp thời khóa biểu

Các nhóm cần kiểm tra:

- Miền thời gian: ngày, buổi, tiết, một/hai buổi.
- Tài nguyên: lớp, giáo viên, phòng (nếu có bằng chứng).
- Chương trình: môn, định mức tiết/tuần, cụm tiết liên tiếp.
- Khả dụng: ngày nghỉ, tiết nghỉ, tiết tránh.
- Đồng bộ đa tài nguyên: ghép lớp, ghép giáo viên.
- Sức chứa: tổng tiết không vượt ô khả dụng.
- Kết quả: tiết đã xếp, tiết chưa xếp, cảnh báo, khóa/cố định và tinh chỉnh thủ công.

## Bài học từ OLM TKB

Nguồn chính thức cho thấy OLM TKB có quy trình tám bước: khởi tạo; môn học; tổ chuyên môn; giáo viên; khối/nhóm; lớp/khung chương trình; phân công; tinh chỉnh thủ công. FAQ xác nhận các cấu hình như ngày nghỉ/tiết tránh, chuỗi tiết `2,1,1`, nhóm lớp theo tổ hợp, ghép lớp/ghép giáo viên và khả năng còn tiết chưa xếp khi ràng buộc quá chặt. Trang sản phẩm gọi cơ chế tự động là “AI”, nhưng không công bố thuật toán; vì vậy chỉ được mô tả như một bộ xếp lịch có ràng buộc, không gán tên solver cụ thể.

Nguồn khởi đầu:

- https://tkb.olm.vn/
- https://olm.vn/chu-de/olm-tkb-xep-thoi-khoa-bieu-tu-dong-nhanh-chong-2055097718
- Bài “Những câu hỏi thường gặp khi dùng OLM TKB” trên hệ thống OLM, đăng 17/08/2024.

## Pitfalls

- Không lấy kết quả tìm kiếm hoặc snippet làm bằng chứng cuối nếu có trang nguồn chính thức.
- Không đưa số liệu marketing (“hàng nghìn trường”, v.v.) thành kết luận độc lập nếu chưa cần thiết.
- Không coi bình luận người dùng chưa được trả lời là tính năng đã hỗ trợ.
- Không nói “không hỗ trợ” chỉ vì tài liệu công khai chưa đề cập; dùng “chưa xác minh được”.
- Khi tác vụ nghiên cứu phụ thất bại, tiếp tục bằng nguồn trực tiếp và DOM extraction; không đưa lỗi hạ tầng nghiên cứu vào báo cáo nội dung.
