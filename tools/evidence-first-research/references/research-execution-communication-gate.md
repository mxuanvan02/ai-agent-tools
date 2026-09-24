# Làm nghiên cứu có kiểm chứng và báo cáo dễ hiểu cho người dùng

## Khi dùng
Dùng khi làm thí nghiệm, kiểm tra dữ liệu/tệp/ảnh, viết mã nghiên cứu hoặc báo cáo trạng thái cho người dùng.

## Nguyên tắc giao tiếp bắt buộc
1. **Không phản hồi rỗng sau khi gọi công cụ.** Ngay khi có kết quả, trả lời bằng tiếng Việt dân dã: kết quả là gì, có sửa gì không, còn bị chặn ở đâu, bước tiếp theo là gì.
2. **Báo TRƯỚC khi gọi, không chỉ báo sau.** Câu đầu của tin nhắn phải nói rõ sắp dùng công cụ/skill nào và để làm gì (ví dụ: “Agent đọc `ecm_v3_core.py` để xem guard hiện tại”), rồi mới gọi. Sau khi có kết quả, mở đầu ngắn bằng **“Đã dùng: …”** và chỉ kể đúng công cụ vừa gọi; báo **PASS** hoặc **BLOCKED** trước phần giải thích.
   - Người dùng đã phải hỏi lại giữa phiên (“call tool gì thì báo lên đâu e?”) vì việc báo trước bị làm lúc có lúc không — mấy lượt đầu có báo, mấy lượt giữa gọi thẳng. Giữ nhất quán ở **mọi** lượt, kể cả khi chỉ đọc file hay chạy test nhanh; sự im lặng giữa chừng khiến người dùng không biết agent đang làm gì.
   - Skill luôn bật ở system prompt (ví dụ `i-have-adhd`) thì **không** báo như tool — nó chỉ định dạng câu trả lời. Chỉ báo những skill/tool mình chủ động gọi.
3. **Báo trước rồi PHẢI gọi ngay trong cùng lượt đó.** Đây là lỗi nặng hơn việc không báo, và đã xảy ra **hai lần trong một phiên**: agent viết “Agent bắt đầu: tìm 15 phút xem có tool sẵn…” / “Agent sửa 2 false positive, viết test, rồi…” rồi **kết thúc lượt mà không gọi tool nào**. Người dùng phải hỏi lại “sao tự động dừng rồi? Bị gì vậy e?” và “nhìn như vậy thì agent có đang làm khong đó hay lại ngắt chat rồi?”.
   - Câu mở đầu kiểu “agent bắt đầu / agent làm ngay / agent sửa…” là **lời hứa thực thi**, không phải lời dẫn. Nếu trong lượt đó không kèm tool call thì với người dùng nó y như treo máy: người dùng không phân biệt được “agent đang nghĩ” và “agent đã chết”.
   - Quy tắc cứng: khi câu đầu đã công bố sắp gọi tool, **tool call phải nằm trong cùng message đó**. Kế hoạch nhiều bước thì gọi bước 1 ngay, đừng mô tả cả 3 bước rồi dừng.
   - Nếu thật sự cần dừng để hỏi người dùng, phải nói rõ đang **chờ người dùng quyết**, không dùng câu mang nghĩa đang chạy.
   - Khi bị nhắc vì đã treo: nhận đúng một câu (“agent ngắt thật, lỗi của agent”), **không** giải thích dài, rồi gọi tool ngay trong lượt đó. Nhận lỗi mà vẫn không gọi tool là lặp lại đúng lỗi vừa nhận.
3. Mỗi từ chuyên môn phải có nghĩa ngay lần đầu, ví dụ: “manifest (bản kê khai đầu vào đã chốt)”, “dry-run (chạy thử không gọi mô hình)”, “SHA-256 (mã kiểm tra phát hiện tệp bị đổi)”. Không để tiếng Anh/chuyên ngành trơ trọi.
4. Tách bạch rõ: mã chạy đúng/đầu vào còn nguyên **không đồng nghĩa** kết quả khoa học đúng, mô hình hiểu hình, hoặc có đánh giá của con người.

## Quy trình an toàn cho pilot có ảnh
1. Chốt danh sách đầu vào bằng manifest: mã đoạn, nguồn, đường dẫn tệp, kích thước và SHA-256 của từng ảnh.
2. Sao lưu tệp nguồn trước khi tạo hoặc sửa artefact (tệp đầu ra nghiên cứu); ghi đường dẫn backup và checksum.
3. Làm kiểm tra không gọi mô hình trước: xác nhận số bản ghi, ảnh tồn tại, đường dẫn và checksum. Một lỗi phải ra `BLOCKED`, không tự thay tệp hoặc điền dữ liệu rỗng.
4. Mô hình lỗi, ảnh lỗi, hay dữ liệu trả về sai dạng: lưu nguyên trạng thái/lý do; không dùng fallback có vẻ hợp lệ làm kết quả thí nghiệm.
5. Chỉ sau khi dry-run PASS mới xin phép rõ ràng trước khi tải/chạy mô hình nếu việc này tốn mạng, dung lượng hoặc thời gian.

## Kiểm thử
- Viết kiểm thử bắt lỗi trước: ít nhất đầu vào đúng → PASS; ảnh/tệp bị đổi → BLOCKED.
- Nếu lệnh kiểm thử không chạy do môi trường, báo đúng là lỗi môi trường; tách dry-run chạy độc lập thay vì để `&&` làm nó không được chạy.
- Không tuyên bố test PASS nếu chưa có đầu ra thực tế của test runner.

## Điều không được làm
- Không đưa mô tả cũ do máy sinh thành nhãn chuẩn hay bằng chứng mô hình “hiểu ảnh”.
- Không tự tải mô hình hay gọi dịch vụ có chi phí/tài nguyên đáng kể khi chưa được cho phép.
- Không gọi thử nghiệm nhỏ là benchmark (bộ đo chuẩn để so sánh) hoặc kết quả đủ để khẳng định hơn kém.
