# Thiết kế kiểm định công cụ đánh giá (rubric / khung tiêu chí / phiếu thẩm định)

Dùng khi người dùng đã có một **khung tiêu chí đề xuất** trong bản thảo và hỏi
"làm sao chứng minh các tiêu chí này có giá trị?", hoặc khi cần chuyển một mục
"thiết kế kiểm định dự kiến" thành nghiên cứu thực chạy được.

Không dùng để viết prose bản thảo (đó là `academic-prose`), cũng không dùng để
bịa số liệu kiểm định.

---

## 1. Ba gói kiểm định — mỗi gói cho phép một tuyên bố KHÁC NHAU

Điểm mấu chốt về liêm chính: **gói đã chạy quyết định câu được phép viết**.
Chạy gói A rồi viết như đã chạy gói C là overclaim.

| Gói | Cần gì | Cho phép tuyên bố |
|---|---|---|
| **A. Độ giá trị nội dung** | 6–10 chuyên gia, 1 vòng | "Các tiêu chí đạt độ giá trị nội dung theo đánh giá chuyên gia" |
| **B. A + độ thống nhất** | thêm ≥2–3 thẩm định viên × tập câu | "Khung áp dụng được **thống nhất**" |
| **C. B + lỗi cài sẵn** | thêm thiết kế mù, 2 nhóm | "Khung **phát hiện được** lỗi mà checklist bỏ sót" |

Chỉ gói C chứng minh **đóng góp riêng** của khung. A và B chỉ chứng minh khung
rõ ràng và dùng được — không chứng minh nó hơn cách làm cũ.

Hệ quả với tiêu đề bài: chạy được A trở lên thì đổi từ *"Tiếp cận…"* sang
*"Xây dựng và kiểm định bước đầu…"*, và mục "thiết kế dự kiến" chuyển thành
"kết quả". Chưa chạy thì **giữ nguyên bản trung thực** — nộp được ngay.

## 2. Gói A — I-CVI, và thành phần hội đồng phải khớp lập luận của bài

Mỗi chuyên gia chấm từng tiêu chí trên thang 4 mức về mức độ phù hợp.
`I-CVI = tỷ lệ chuyên gia cho 3–4 điểm`.

- Ngưỡng giữ tiêu chí: **I-CVI ≥ 0,78** (với 6–10 chuyên gia)
- Toàn thang: **S-CVI/Ave ≥ 0,90**
- Tiêu chí dưới ngưỡng → sửa diễn đạt hoặc gộp, **không im lặng bỏ**

**Hội đồng phải phản ánh chính lập luận của bản thảo.** Nếu bài đã viết "khung
đòi hỏi hai loại chuyên môn" (ví dụ: chuyên môn nội dung + chuyên môn đo lường)
thì hội đồng phải tách đúng hai loại đó (ví dụ 5 + 3). Hội đồng một loại
chuyên môn là điểm phản biện dễ thấy nhất.

## 3. Gói B — cái bẫy kappa

Thang định danh (ví dụ 4 trạng thái *đạt / không đạt / không áp dụng / chưa đủ
căn cứ*) → dùng **kappa không trọng số** hoặc **Krippendorff alpha**.
**Tuyệt đối không weighted kappa** cho thang định danh.

Bẫy số học thực tế: 2 người × 40 câu, đồng thuận thô 34/40 = **85%** nghe rất
tốt. Nhưng nếu 30/40 câu đều được xếp "đạt" thì đồng thuận ngẫu nhiên đã cao,
kappa có thể chỉ còn **~0,55**.

→ Báo cáo **cả ba**: tỷ lệ đồng thuận thô, **phân bố biên**, và kappa. Báo một
mình kappa sẽ bị bắt lỗi; báo một mình tỷ lệ thô cũng vậy.

## 4. Gói C — bốn thứ quyết định thiết kế có vững hay không

Thiết kế: N câu = một nửa sạch + một nửa cài lỗi (chia đều theo số loại lỗi).
Hai nhóm: nhóm A dùng khung mới, nhóm B dùng checklist thông thường. Mù.

**(a) Ground truth phải được xác nhận độc lập.** Trước khi phát, ≥2 chuyên gia
phải xác nhận: câu cài lỗi *đúng là có lỗi đó*, và câu sạch *đúng là không có
lỗi tương ứng*. Thiếu bước này, ground truth chỉ là ý kiến người soạn.
Kèm theo: **audit ngược câu sạch** bằng chính taxonomy lỗi, nếu không
specificity bị nhiễu bởi lỗi vô tình.

**(b) Phải đo cả độ nhạy VÀ độ đặc hiệu.** Nếu nhóm A phát hiện nhiều hơn
*nhưng cũng báo bừa ở câu sạch nhiều hơn*, lợi thế là ảo — họ chỉ đang nghi ngờ
mọi thứ. Tách **d′** (khả năng phân biệt) khỏi **criterion c** (xu hướng báo
lỗi). Nếu sens cao hơn, spec thấp hơn tương ứng, d′ bằng nhau → khung không
giúp phát hiện tốt hơn. Đây là kết quả **rất dễ xảy ra**, nên tiên lượng trước.

**(c) Kiểm tra phân biệt.** Khung chỉ nên vượt nhóm B ở **đúng loại lỗi nó
nhắm tới**. Vượt đều ở mọi loại kể cả lỗi chính tả → đó là hiệu ứng "nhóm A
được tập huấn nên chú tâm hơn", không phải giá trị của cơ chế mới.

**(d) Salience của lỗi là biến gây nhiễu.** Lỗi trắng trợn và lỗi tinh vi cho
detection rate hoàn toàn khác. Pilot cho 3 người chấm salience (nhẹ/vừa/rõ) và
**cân bằng salience đều qua các loại lỗi**, nếu không kết luận "loại lỗi X khó
phát hiện hơn" sẽ không vững.

Định nghĩa false alarm phải **hai chiều**: (i) gắn cờ câu sạch, (ii) gắn cờ
đúng câu lỗi nhưng **sai loại lỗi**. Quyết định trước cách tính, báo cáo cả hai.

Không tiết lộ tỷ lệ lỗi (50%) cho thẩm định viên — nếu họ đoán được, criterion
bị kéo lệch nhân tạo.

## 5. Cỡ mẫu — đơn vị phân tích là NGƯỜI, không phải câu

"Nhóm" là biến ở cấp thẩm định viên, nên power phụ thuộc **số thẩm định viên**.
Số câu chỉ giảm sai số đo bên trong mỗi người.

Hai đường tính độc lập, hội tụ cùng vùng:

- **t-test hai mẫu** trên sensitivity cấp cá nhân: `n mỗi nhóm = 15,7/d²`
  (α=0,05 hai phía, power 0,80) → d=1,0 ⇒ ~17; d=0,8 ⇒ ~26; d=0,6 ⇒ ~45.
- **So sánh tỷ lệ có hiệu chỉnh clustering**: p₁=0,55, p₂=0,70, m=24 quyết
  định/người, ICC ρ=0,15 ⇒ design effect = 1+23(0,15) = 4,45; 160×4,45 = 712
  quyết định ⇒ 712/24 ≈ **30 người/nhóm**.

Khuyến nghị: confirmatory **28–30 người/nhóm**; sàn pilot **15–17** (chỉ phát
hiện d≥1,0, phải khai báo là pilot); **dưới 12** chỉ dùng kiểm tra khả thi công
cụ, không kết luận so sánh.

ρ là ẩn số lớn nhất → pilot 6–8 người để ước lượng ρ và SD, rồi tính lại.
**Đừng chốt cỡ mẫu trước khi có SD thực nghiệm.**

Muốn ước lượng sensitivity **theo từng loại lỗi** với nửa độ rộng CI ≈ ±0,10
thì 6 câu/loại là không đủ — cần 8–10 câu/loại, hoặc hai form đối xứng theo
Latin square để tăng số câu tổng mà không tăng tải mỗi người.

## 6. Taxonomy lỗi của mình thường KHÔNG khớp taxonomy kinh điển

Kiểm tra trước khi cite. Ví dụ đã gặp: 4 loại lỗi *sai căn cứ thời điểm áp
dụng / sai nguồn viện dẫn / thiếu dữ kiện quyết định / hai phương án đều bảo vệ
được* — ba loại đầu là **lỗi hiệu lực nội dung**, chỉ loại thứ tư gần với
taxonomy item-writing của Haladyna–Downing–Rodriguez.

Hệ quả: văn liệu item-writing flaw (Haladyna, Downing, Tarrant, Rush) dùng được
để biện luận **khung chung**, KHÔNG dùng để biện luận **taxonomy riêng**.
Taxonomy riêng phải tự xây và tự validate (Delphi với chuyên gia nội dung).

**Ghép cặp là điểm mạnh nên khai thác:** tạo N gốc câu, mỗi gốc có biến thể
sạch và biến thể lỗi, chia 2 form counterbalanced sao cho **không ai thấy cả
hai biến thể của cùng một gốc**. Khử được biến thiên do nội dung/chủ đề.

## 7. Dựng mẫu mới vs dùng đề thi thật

Với gói C, **dựng mẫu mới là đúng phương pháp**, không phải phương án dự phòng.
Ba lý do, nói thẳng với người dùng:

1. Đề thật có **lỗi tự nhiên chưa biết** → không có ground truth → không tính
   được sens/spec.
2. Đề thật **không cân bằng loại lỗi** — sẽ lệch hẳn về lỗi hình thức, gần như
   không có đúng loại lỗi mà khung nhắm tới.
3. Đề thật thuộc học phần cụ thể → **rủi ro liêm chính**: bài báo công bố lỗi
   trong đề thi của đồng nghiệp.

Nhưng mẫu mới chỉ có giá trị học thuật khi: **nội dung giả định, cấu trúc
thật**. Phải đo thông số hình thức từ nguồn thật công khai (độ dài câu dẫn,
cách viện dẫn văn bản, kiểu phương án) rồi mô phỏng — xem
`references/public-assessment-item-sourcing.md`.

Tiền lệ để cite cho phương pháp cài lỗi: Rush (2016), Tarrant & Ware (2008) đã
dùng câu cài lỗi có chủ đích. Ngoài ra văn liệu **seeded-error trong bình duyệt
tạp chí** (Schroter và cs.; Baxt và cs. — cần verify DOI qua Crossref trước khi
cite) mới là nơi có đúng mô hình "ground truth do tác giả tạo ra + đo detection
rate", vì văn liệu item-writing flaw chỉ đo *tần suất lỗi* hoặc *tác động lên
psychometrics*, không đo *khả năng phát hiện*.
