# Đồ án có sản phẩm hỗ trợ quyết định: quy tắc trình bày và nghiệm thu

Áp dụng khi đồ án không chỉ phân tích mà còn bàn giao kiến trúc, nguyên mẫu, quy trình tự động hóa, biểu mẫu, demo và slide.

## 1. Trục nội dung bắt buộc

Không mở đầu bằng công nghệ, lần chạy, kiểm thử hay danh sách hiện vật. Trình bày theo chuỗi:

1. Thực trạng cụ thể của người dùng.
2. Pain point và hậu quả thực tế.
3. Khoảng trống của cách làm hiện tại.
4. Câu hỏi nghiên cứu (RQ).
5. Ý tưởng/đóng góp.
6. Phương pháp thiết kế.
7. Kiến trúc và cơ chế hoạt động từng bước.
8. Thiết kế thử nghiệm: công bố trước input, giả định/mock data, expected output và tiêu chí.
9. Kết quả hệ thống theo `input → xử lý → output → vai trò đối với RQ/đóng góp`.
10. Thảo luận, giới hạn và khả năng suy rộng.

## 2. Viết cho người đọc, không viết như nhật ký kỹ thuật

- Nói bản chất và tác dụng trước, tên công nghệ sau (trong ngoặc nếu cần).
- Không xếp từ khóa như fixture, execution, QA, guardrail, pipeline, connector, credential, metadata, release, build.
- Nếu buộc giữ tên riêng/trường trạng thái, giải nghĩa tiếng Việt ngay lần đầu.
- Không đưa vào PDF học thuật: cách biên dịch, cấu hình bí mật, import workflow, cách đóng ZIP, lệnh chạy, nhật ký QA. Chuyển chúng sang README kỹ thuật.
- Không dùng câu nửa Người dùng nửa Việt hoặc văn phong hậu trường.
- Không để execution/QA định nghĩa contribution; chúng chỉ là bằng chứng phụ.

## 3. Đầu ra của hệ thống hỗ trợ quyết định

Đầu ra phải trả lời được:

- Sự kiện/điều kiện nào kích hoạt?
- Người dùng đang ở vai trò nào và phải làm gì?
- Thực hiện trước ngày nào; cách tính hạn?
- Cần giấy tờ và biểu mẫu nào?
- Hệ thống điền sẵn trường nào; người dùng xác nhận/bổ sung trường nào?
- Nộp/lưu ở đâu; cần giữ bằng chứng gì?
- Căn cứ nào, hiệu lực tại thời điểm nào?
- Dữ kiện nào còn thiếu?
- Khi nào phải hỏi thêm, chuyển chuyên gia hoặc từ chối kết luận?

Không tuyên bố AI tự phán quyết pháp lý. Tự động hóa phần chắc chắn; hỏi thêm phần thiếu; chuyển duyệt phần hệ quả cao; từ chối khi nguồn không đủ.

## 4. Bao phủ tình huống đúng cách

Không nói “bao phủ toàn bộ mọi trường hợp”. Xây bộ hữu hạn có hệ thống bằng:

- lớp tương đương;
- giá trị biên (dưới/bằng/trên ngưỡng);
- bảng quyết định;
- chuyển trạng thái;
- positive, negative, ambiguous và stale-source cases.

Mỗi scenario phải có oracle độc lập, input cụ thể, câu hỏi bổ sung, rule/source, output mong đợi và mapping tới RQ/contribution.

## 5. Sản phẩm và demo

Không đổ hàng chục thẻ tình huống dài liên tiếp. Dẫn người dùng step-by-step:

1. Nhập tình trạng/giao dịch.
2. Xác nhận dữ kiện đã biết.
3. Trả lời câu hỏi làm rõ.
4. Xem phân loại và lý do.
5. Xem kế hoạch hành động.
6. Mở biểu mẫu điền sẵn và hướng dẫn phần còn thiếu.
7. Xác nhận/chuyển người duyệt.
8. Theo dõi hạn và bằng chứng hoàn thành.

Demo phải dùng sản phẩm thật và dữ liệu mô phỏng được công bố trước, không chỉ ảnh hoặc số tổng.

## 6. Kiến trúc và n8n

Kiến trúc phải phản ánh contribution hiện hành, không tái sử dụng pipeline cũ chỉ vì đã có ảnh. Tối thiểu thể hiện:

`nguồn dữ liệu → hồ sơ sự kiện → phân loại/điều kiện → kho quy tắc có phiên bản và căn cứ → hỏi thêm/review/từ chối → kế hoạch hành động → biểu mẫu/lịch/nhiệm vụ → người dùng/chuyên gia`.

n8n là một hiện vật/sản phẩm của đồ án nếu được nêu như vậy: workflow phải import và chạy thật, execution sạch, output khớp sản phẩm, không credential, ảnh Editor/Execution đọc được. Không mô tả các workflow độc lập thành một tích hợp end-to-end nếu chưa có bằng chứng.

## 7. Slide

Trước khi dựng slide chi tiết, khóa sườn tổng quát. Sau đó đi step-by-step; mỗi slide chỉ có một thông điệp chính. Tránh block thừa khoảng trắng, slogan, câu meta, nhãn QA và trộn ngôn ngữ. Dùng ảnh sản phẩm thật; slide phụ lục mới chứa chi tiết execution.

## 8. Vision QA và exit gate

Không QA bằng contact sheet duy nhất. Phải kiểm từng:

- trang PDF ở kích thước đầy đủ;
- sơ đồ;
- bảng;
- màn hình sản phẩm;
- biểu mẫu;
- ảnh n8n;
- slide.

Kiểm độ đọc trên điện thoại, crop, tràn, khoảng trắng, chữ quá nhỏ, Người dùng–Việt, số liệu và consistency. Sau mỗi vòng vision phải sửa rồi render lại. Chỉ gọi “bản cuối” khi báo cáo, sản phẩm, demo, n8n và slide thống nhất; PDF/PPTX/ZIP mở được; checksum và bằng chứng build/render/test tồn tại.

## 9. Điều phối song song

Chỉ song song các nhánh có đầu ra tách biệt. Chỉ định owner/path riêng để tránh nhiều agent sửa cùng file. Coordinator giữ integration gate và tự xác minh file thật; timeout hoặc self-report của subagent không phải bằng chứng hoàn tất. Nếu thay đổi cấu hình concurrency, xác minh config hợp lệ và lưu ý phiên đang chạy có thể vẫn giữ giới hạn cũ cho tới khi restart.