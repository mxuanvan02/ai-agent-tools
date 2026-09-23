# Căn chỉnh lại manuscript với dữ liệu đa phương thức nội bộ

## Khi nào áp dụng
Khi bài phương pháp/protocol bị nhận xét là thiếu thí nghiệm, trong khi dữ liệu, manifest, script hoặc kết quả có thể nằm ở workspace nội bộ khác với repo public.

## Nguyên tắc bắt buộc
1. **Không kết luận “không có dữ liệu/thí nghiệm” chỉ vì repo public chỉ có fixture tổng hợp.** Kiểm kê workspace nghiên cứu trước: manifest, split, JSONL, ảnh, bảng kết quả, protocol chấm người, script benchmark.
2. **Đọc mục tiêu và đóng góp đã chốt của bài trước khi cắt manuscript.** Không biến bài đánh giá phương pháp thành bài “kiểm tra phần mềm” chỉ vì bằng chứng thực nghiệm chưa được nối đúng.
3. Phân biệt ba tầng bằng chứng:
   - **toàn vẹn đầu vào:** tệp ảnh tồn tại, kích thước/hash khớp, split không lẫn tài liệu;
   - **vận hành phương pháp:** các nhánh/baseline thực sự chạy trên cùng đầu vào và lưu output;
   - **chất lượng khoa học:** người chấm độc lập xác nhận đúng đáp án, bám nguồn, chất lượng câu hỏi và nhu cầu đa phương thức.
   Không suy tầng trên từ tầng dưới.
4. Chỉ gọi một điều kiện là `text+layout` nếu có layout không gian thật (trang, bounding box, OCR coordinates). `section_title`, `header_level`, thứ tự ảnh chỉ là **cấu trúc logic**; đặt tên `TL_struct` và ghi rõ giới hạn.
5. Trước khi viết claim hay bảng kết quả, kiểm tra thân script/test, không suy từ tên file/hàm hay tên biến.

## Quy trình thực hành
1. **Khoanh đúng dự án và nguồn dữ liệu:** tách repo public (artifact) với workspace nội bộ (data/experiments).
2. **Lập inventory có số:** số tài liệu, context/chunk, chunk có ảnh, ảnh, split theo document, nhãn/chấm người, output đã có.
3. **Kiểm tra đường dẫn tài sản:** đổi đường dẫn cũ sang đường dẫn hiện tại theo quy tắc rõ ràng; tệp không khớp duy nhất hoặc hash không khớp phải loại fail-closed.
4. **Tạo manifest dẫn xuất, không sửa dữ liệu gốc:** mỗi item giữ `doc_id`, `chunk_id`, split, text, cấu trúc, ảnh, kích thước, byte, SHA-256, provenance, warnings.
5. **Kiểm tra manifest bằng verifier độc lập:** đủ điều kiện mỗi chunk, số ảnh và hash thực, không lẫn split theo document, báo cáo excluded records + lý do.
6. **Sau đó mới triển khai thử nghiệm:** cùng input, cùng model/cấu hình, các baseline đã định và ECM; output chỉ là output thô cho đến khi có kế hoạch chấm/metric.
7. **Viết lại manuscript theo vai trò mục:** walkthrough minh hoạ một item; dataset nêu inventory thật; experiment nêu runner/metric/baseline và kết quả đã kiểm chứng; limitations nêu phần chưa chấm hoặc chưa có layout tọa độ.

## Pitfalls
- Đừng dùng mô tả ảnh do model sinh thay cho ảnh thật rồi gọi là đầu vào thị giác.
- Đừng coi số QA lớn nhưng text-only là bằng chứng cho claim đa phương thức.
- Đừng coi `PASS` hash/JSON/schema là câu hỏi đúng hoặc hình cần thiết.
- Đừng đổi nội dung manuscript trước khi kiểm kê tài sản nội bộ; sao lưu source và tạo artifact dẫn xuất trước.
- Đừng “cắt sạch” minh hoạ vận hành: bỏ claim hiệu quả không có bằng chứng, nhưng có thể giữ walkthrough được gắn nhãn rõ là minh hoạ, không phải benchmark.

## Mẫu báo cáo ngắn cho người dùng
Báo kết luận trước, bằng tiếng Việt dễ hiểu:
- **Đã có gì:** số item/tài liệu/ảnh/split, vị trí artifact.
- **Đã chứng minh gì:** chỉ đúng tầng bằng chứng hiện có.
- **Chưa chứng minh gì:** rõ ràng các claim bị khóa.
- **Bước tiếp:** thao tác nhỏ nhất để đi sang tầng bằng chứng tiếp theo.
