# Lấy mẫu câu hỏi đánh giá thật từ nguồn công khai Việt Nam

Dùng khi cần **khuôn cấu trúc thật** của câu hỏi trắc nghiệm (pháp luật, môn
học, thi công chức) để mô phỏng, phân tích, hoặc dựng bộ mẫu nghiên cứu — mà
không có quyền truy cập ngân hàng đề nội bộ.

Nguyên tắc nền: người dùng muốn agent **tự tìm nguồn công khai**, đừng đòi người dùng gửi
mẫu. Nhưng cũng **không được bịa câu hỏi** — bộ dữ liệu bịa chỉ phản chiếu định
kiến của model về đề thi, và nghiên cứu dựng trên đó sai từ gốc. Zero câu tốt
hơn năm câu giả.

---

## 1. Nguồn công khai đã kiểm chứng (Việt Nam)

Thứ tự ưu tiên, kèm trạng thái đo được:

| Nguồn | Kết quả thực tế |
|---|---|
| `portalmedia.moj.gov.vn` (file đính kèm Bộ Tư pháp) | có file .doc/.pdf thật, nhưng **403** khi curl trực tiếp |
| CDN/Sở/UBND tỉnh (`cdn.thuviennhadat.vn`, `*.gov.vn/sites/default/files/`) | **200, tải được** — nguồn dễ lấy nhất |
| `pbgdpl.moj.gov.vn` (Cổng PBGDPL) | 200, có trang thể lệ + bộ câu hỏi cuộc thi |
| `pbgdpl.gov.vn` | 403 (iframe wrapper) |
| `thi.pbgdpl.moj.gov.vn` | không phân giải |
| Thư viện trường (`library.hul.edu.vn`, `thuvien.*`) | redirect rỗng / cần đăng nhập — **và không lưu ngân hàng đề** |

Cách tìm: query có `site:moj.gov.vn`, hoặc `"bộ câu hỏi" trắc nghiệm "tìm hiểu
pháp luật" đáp án filetype:pdf`. Bộ câu hỏi các **cuộc thi trực tuyến tìm hiểu
pháp luật** do tỉnh ban hành kèm Quyết định là mỏ vàng: công khai, có số hiệu
văn bản, thường 60+ câu.

**Pitfall 403:** thử lại kèm `Referer` trỏ về trang chủ cùng domain và
User-Agent thật trước khi bỏ nguồn. Nếu vẫn 403 thì **báo thẳng là không lấy
được**, đừng thay bằng nguồn khác rồi mô tả như nguồn gốc.

## 2. Thư viện trường KHÔNG phải nguồn cho việc này

Lý do phương pháp, không phải lý do kỹ thuật: thư viện lưu **giáo trình, sách,
luận văn**. Nó **không lưu ngân hàng câu hỏi kèm khóa đáp án và hồ sơ câu hỏi**.
Đề thi nằm trong LMS nội bộ có xác thực. Nói điều này ngay thay vì thử 5 URL.

## 3. Đo định lượng cấu trúc — làm khuôn, không phải đọc cảm tính

Sau khi có PDF: `pdftotext -layout`, tách câu bằng regex `Câu\s+\d+`, rồi đo.
Bộ thông số cần lấy (số thật đo được từ bộ 60 câu Cao Bằng 2025):

| Đặc điểm | Cách đo | Ví dụ kết quả |
|---|---|---|
| Độ dài câu dẫn | số từ, báo **trung vị** | 26 từ (6–50) |
| Độ dài phương án | số từ, trung vị | 10 từ (2–85) |
| Ghi năm/số hiệu văn bản | % câu dẫn | 71% |
| Mở bằng "Theo Luật/Nghị định…" | % câu dẫn | 19% |
| Dạng định nghĩa/liệt kê | % | 64% |
| Có "tất cả đáp án trên" | đếm câu | **26/59 = 44%** |
| Lệch độ dài PA dài nhất vs nhì | trung vị, cực đại | 4 từ, max 51 từ |

Báo **trung vị** không phải trung bình — phương án dài 85 từ sẽ kéo lệch mean.

## 4. Hai chỉ số này dùng được làm BẰNG CHỨNG trong bản thảo

- **Tỷ lệ "tất cả đáp án trên"** (44% ở mẫu đo được) là lỗi kỹ thuật kinh điển
  Haladyna–Downing–Rodriguez (2002) khuyến nghị tránh → bằng chứng thực tế cho
  luận điểm "đề trắc nghiệm đang lưu hành có tỷ lệ vi phạm nguyên tắc cao".
- **Lệch độ dài phương án** (trung vị 4 từ, cực đại 51) là dấu hiệu làm lộ đáp
  án (length cue) → sinh viên đoán được mà không cần lập luận.

**Giới hạn phải nói rõ:** file công khai thường **không kèm khóa đáp án**, nên
KHÔNG được kết luận "phương án dài là đáp án đúng" — chưa có ground truth. Đây
là giới hạn thật của nguồn, không lấp bằng suy đoán.

## 5. Khớp cấp độ trước khi dùng làm khuôn

Bộ câu hỏi thi tìm hiểu pháp luật cho **học sinh THCS/THPT** không cùng cấp độ
với đề thi **học phần luật bậc đại học**. Nó cho thông số hình thức, nhưng
thiếu câu đòi hỏi thao tác chọn quy phạm / đối chiếu điều kiện áp dụng.

→ Dùng làm **khuôn hình thức**; nội dung pháp lý dựng riêng ở cấp độ đích. Nói
rõ sự lệch cấp độ này với người dùng thay vì im lặng dùng.

Khi dựng bộ mẫu để **đo năng lực phát hiện lỗi**, phải cân bằng độ dài phương
án — bộ mẫu không được chứa lỗi ngoài ý muốn (length cue) ngoài lỗi đã cài.

## 6. Nếu delegate việc tìm nguồn

Subagent chỉ có toolset `browser` sẽ chết nếu CDP không có browser nào lắng
nghe. Với việc **tải file tĩnh (PDF/DOC/HTML)** thì `terminal` + curl, hoặc
`web`, phù hợp hơn browser rất nhiều — cấp đúng toolset ngay từ đầu. Xem
`references/research-execution-communication-gate.md` cho nguyên tắc chung về
delegate.
