# Slide bài lập trình: ánh xạ định danh và QA ví dụ chạy được

## 1. Không đồng nhất ba loại định danh

Một bài có thể đồng thời mang ba số/mã khác nhau:

1. **Số thứ tự trong chuỗi phát hành** — dùng ở bìa, header và tên deck mới, ví dụ `Bài 12`, `SLIDE_12_...`.
2. **Mục PPCT/KHBD** — nguồn nội dung có thẩm quyền, ví dụ `§5.16`, `KHBD_16`.
3. **Mã sản phẩm học sinh** — giữ đúng theo KHBD, ví dụ `B16_NhomXX`, dù deck được phát hành là Bài 12.

Trước khi dựng, lập bảng ánh xạ ba cột và quy định nơi mỗi định danh được phép xuất hiện. Không “sửa cho đồng bộ” mã sản phẩm theo số thứ tự phát hành. QA phải quét riêng từng loại thay vì chỉ tìm một số bài chung.

## 2. Chuyển deck nguồn lệch nhiệm vụ

Deck nguồn có thể đạt kỹ thuật (mở được, đủ notes, không tràn biên) nhưng sai nhiệm vụ định lượng. Khi ví dụ trung tâm, kết quả và ca kiểm tra khác KHBD:

- Chỉ tái sử dụng nhận diện, khung code, sơ đồ IPO, bảng kiểm và layout hữu ích.
- Thay toàn bộ mạch ví dụ; không vá vài con số vì các giá trị cũ thường lặp ở bìa, mục tiêu, notes, bài tập và kết luận.
- Lập danh sách **required** từ KHBD và **forbidden** từ deck cũ: bài toán cũ, kết quả cũ, mã cũ, header cũ và tên nhiệm vụ cũ.
- Quét cả text trên slide và speaker notes.

## 3. QA ví dụ Python và nội dung lập trình

Mỗi ví dụ chạy được cần được kiểm tra như một test case:

| Thành phần | Cần khóa |
|---|---|
| Mã nguồn | Cú pháp, kiểu dữ liệu, dấu nháy/ngoặc, phần mở rộng `.py` |
| Đầu vào | Giá trị và kiểu dữ liệu |
| Kết quả mong đợi | Giá trị, định dạng và đơn vị |
| Kết quả thực tế | Chạy bằng đúng phiên bản/môi trường dùng trong lớp khi cần nguyên văn |
| Kết luận | Đạt/khác và thay đổi tối thiểu cần sửa |

Quy tắc:

- Phân biệt phép cộng số với nối xâu ngay cạnh kết quả: `"13" + "25" → 1325` là nối hai xâu, không phải cộng số.
- Với hằng gần đúng, ghi rõ giả định và tính gần đúng: `pi ≈ 3.14`, `chu vi ≈ 31.4 đơn vị`; không trình bày như giá trị tuyệt đối chính xác.
- Nếu KHBD yêu cầu học sinh “ghi nguyên văn thông báo lỗi”, phải lấy thông báo từ môi trường Python thực tế. Thông điệp `SyntaxError` có thể khác giữa phiên bản; không tự bịa một câu lỗi rồi gọi là nguyên văn. Nếu chưa khóa phiên bản, ghi loại lỗi + dòng/vị trí và đánh dấu thông báo là minh họa.
- Ca lỗi phải thể hiện đủ `trước sửa → thông báo/hiện tượng → nguyên nhân → sau sửa → chạy lại`.
- Chạy một smoke test cho các đoạn mã trọng yếu khi có thể; required-string scan chỉ xác nhận sự hiện diện, không chứng minh mã đúng.

## 4. QA tiêu đề và thứ tự mở đầu

Không giả định phần tử text đầu tiên là tiêu đề: template thường đặt tên trường/header trước heading. Bộ dò nên:

1. Tìm heading mong đợi trong toàn bộ text của slide hoặc trong vùng hình học dành cho tiêu đề.
2. Xác nhận chuỗi mở đầu `Bìa → Mục tiêu → Yêu cầu cần đạt → Mục lục`.
3. Rà contact sheet để xác nhận bố cục, không sửa deck chỉ vì detector đọc nhầm header.

Một cảnh báo `opening_ok=false` do header là **âm giả của detector**, không phải lỗi slide; sửa phép đo rồi chạy lại QA.

## 5. Vòng sửa P2 có giá trị

Sau khi không còn P0/P1, chỉ nhận P2 nếu làm tăng độ chính xác hoặc khả năng dạy học. Với slide lập trình, ưu tiên:

- giải thích kiểu dữ liệu cạnh kết quả bất thường;
- ghi dấu gần đúng và đơn vị;
- làm rõ thông báo lỗi và dòng cần sửa;
- tăng cỡ code/bảng khi render riêng xác nhận khó đọc.

Sau chỉnh sửa, dựng lại PPTX/PDF, chạy toàn bộ QA và render riêng các slide bị tác động ở độ phân giải lớn. Chỉ sau đó mới archive, phát hành và tải ngược kiểm checksum.

## 5a. Nội dung ghi vở là KHÁI NIỆM, không phải bảng số

Slide ghi vở phải cho học sinh chép được **định nghĩa và ý chính của mục**, không phải danh sách kết quả của bài tập cụ thể. Đây là lỗi dễ mắc khi bài có nhiều chỉ tiêu định lượng: người dựng chép luôn các con số bắt buộc của KHBD vào ghi vở, thành ra học sinh chép về một bảng số vô nghĩa khi rời khỏi ví dụ.

Quy tắc viết mỗi dòng ghi vở:

1. **Mở bằng khái niệm được định nghĩa.** `Biến tích luỹ là biến dùng để giữ lại kết quả trung gian và được cập nhật dần qua mỗi lần lặp.` ✓ — `Ba yêu cầu của bài cho 55, 110 và 55.` ✗
2. **Nêu cơ chế hoặc lý do, không nêu đáp số.** `phải khởi tạo trước vòng lặp; với phép tính tổng thì giá trị khởi tạo là 0 vì khi chưa cộng số nào thì tổng bằng 0` ✓ — `khởi tạo bằng 1 thì kết quả thành 56` ✗
3. **Số chỉ được xuất hiện với vai trò ví dụ minh hoạ khái niệm**, đặt sau chữ `Ví dụ` và không phải là trọng tâm của câu: `giá trị đầu được lấy, giá trị cuối không được lấy. Ví dụ range(1, 11) sinh dãy 1 đến 10.` ✓
4. **Phát biểu ở dạng tổng quát hoá được.** Câu ghi vở tốt vẫn đúng khi thay bộ dữ liệu của bài bằng bộ khác.
5. **Kicker của slide ghi vở cũng theo nguyên tắc này** — đặt tên theo khái niệm (`Biến tích luỹ và vị trí lệnh in`), không theo chỉ tiêu (`Biến tích luỹ và ba kết quả bắt buộc`).

Các con số bắt buộc của KHBD vẫn phải hiện diện trong deck, nhưng ở slide yêu cầu cần đạt, slide chương trình, bảng vết và bảng kiểm thử — không phải ở slide ghi vở.

Cách kiểm: quét text của mọi slide ghi vở, đếm token số. Nếu một dòng ghi vở chứa từ hai con số kết quả trở lên mà không có chữ `Ví dụ`, gần như chắc chắn dòng đó đang liệt kê đáp số thay vì phát biểu khái niệm.

## 5b. Slide ghi bài phải có ở MỌI điểm chốt, không chỉ cuối bài

Deck phải có slide `Nội dung ghi vở` **ở cuối từng phần của mục lục**, không chỉ một slide tổng ở cuối bài. Bài nhiều phần mà chỉ có một slide ghi vở là **thiếu nội dung ghi bài** — phải bổ sung. Quy tắc:

- Mỗi phần (`Phần 01`…`Phần 0N`) kết thúc bằng một slide ghi vở riêng, tiêu đề `Ghi vở phần NN`.
- Giữ thêm một slide ghi vở tổng ở gần cuối bài để chốt toàn bài.
- Mỗi slide ghi vở gồm 3 kết luận, viết thành câu hoàn chỉnh theo chuẩn khái niệm ở 5a (mở bằng định nghĩa, nêu cơ chế/lý do; số chỉ xuất hiện sau chữ `Ví dụ` để minh hoạ, không liệt kê đáp số).
- QA phải đếm số slide ghi vở và so với số phần: `so_slide_ghivo >= so_phan + 1`.

## 5c. Pitfall: icon trong danh sách dọc bị ghim cứng toạ độ

Khi helper vẽ danh sách dọc (ghi vở, các bước), vòng tròn nền thường tính theo `y0 + j*step` nhưng icon bên trong dễ bị viết cứng một toạ độ → **mọi icon đè lên nhau ở dòng đầu, các dòng sau trống**. Lỗi này không bị `ink_clip_check` bắt (icon là ảnh, không phải chữ) và cũng không bị checker chồng lấn bắt (chỉ so shape có tô màu).

Cách phát hiện: liệt kê toạ độ mọi `Picture` trong slide, tìm cặp trùng `(left, top)`; đồng thời đối chiếu tâm icon với tâm vòng tròn tương ứng. Cách sửa: icon phải dùng cùng biểu thức `j` như vòng tròn, ví dụ `y_icon = y0 + j*step + (d_circle - d_icon)/2`.

Helper vẽ danh sách cũng phải chịu được số dòng lớn hơn bảng màu cố định: dùng `mau[j % len(mau)]` thay vì `mau[j]`.

## 6. Chuẩn trình bày chốt tại Bài 14 (áp cho các bài sau)

**a. Nền sáng tuyệt đối.** Không hộp nền tối. Khung mã nguồn nền trắng `#FCFDFF`, chữ mực đậm, nhận diện bằng thanh nhãn màu **sáng** ở đầu hộp (không dùng navy đặc — checker luminance sẽ bắt). Dải đầu ra nền xanh nhạt `#EAF7F0`. Bảng: hàng tiêu đề `#E2EEFA` chữ navy. Bìa nền trắng viền màu, không khối màu đặc.

**b. Icon thật thay ký hiệu.** Dùng kho `ppt-master/templates/icons` (12.027 SVG). SVG dùng `fill="currentColor"` nên **phải thay màu trước khi rasterize**, không thì ra PNG trắng trơn. `cairosvg` render đúng; ImageMagick `convert` cần `rsvg-convert` (thường thiếu). Tra tên icon bằng `rg --files -g '*<từ>*.svg'` — tên không portable giữa các thư viện. Map ký hiệu → icon một lần trong dict (`GLYPH_ICON`) rồi để helper tự tra, đừng sửa từng chỗ gọi.

**c. Không slide bài tập.** Slide bài giảng chỉ truyền tải nội dung. Bỏ hẳn `Bài tập cuối bài`, `Luyện tập`, `Vận dụng`; thay bằng slide nội dung (phân biệt khái niệm, lỗi thường gặp, ví dụ trực quan). Kế hoạch bài tập làm thành tài liệu riêng.

**d. Slide chia phần theo mục lục.** Trước mỗi nhóm nội dung, chèn một slide `PHẦN 0N` + tiêu đề lớn + một câu dẫn, khớp đúng thứ tự và tên trong slide Mục lục để người học không bị rối.

**e. Chuỗi slide khoanh từng dòng lệnh (bắt buộc cho slide code).** Không chú thích tất cả dòng trên một slide. Sinh **chuỗi slide liên tiếp**:

1. Slide đầu: chiếu nguyên đoạn lệnh, chưa khoanh gì.
2. Mỗi slide sau: **ô vuông viền đỏ** (`width ≈ 2.6pt`, nền `#FDEEEE`) khoanh đúng **một dòng**, **mũi tên** kéo ra thẻ giải thích bên ngoài, thẳng hàng với dòng được khoanh.
3. Dòng đã giải thích ở slide trước: làm mờ + đánh dấu tick, không kéo mũi tên.

Cài bằng hai hàm: `code_reveal_frame` (vẽ một khung) và `code_reveal_series` (sinh danh sách frame). Khi bung `items` → `plan`, một mục code nở thành `1 + số bước` slide, nên:

- **Không hardcode số slide cần xóa theo `len(items)`.** Đọc `n_goc=len(prs.slides)` trước khi nhân bản, xóa theo `n_goc`, rồi `assert len(prs.slides)==total`. Bỏ bước này sẽ gặp `IndexError: slide index out of range`.
- Khi thay helper cũ bằng helper mới, **xóa hết nhánh gọi hàm cũ** trước khi dựng, nếu không sẽ `NameError`.
- Kicker của các frame nên ghi `Giải thích k/n · <nhãn>` để giáo viên biết đang ở bước nào.

**f. Checker cần thêm.** Ngoài QA cấu trúc và `ink_clip_check.py`, chạy thêm: đếm hộp nền tối theo luminance (ngưỡng `< 0.62`, diện tích `≥ 0.9 in²`), đếm icon đã nhúng, đếm ô vuông viền đỏ (phải bằng tổng số bước), và quét `con_bai_tap` phải rỗng. Chồng lấn chỉ so **hai hình có tô màu**; `TextBox` nằm trong thẻ chứa nó là âm giả.
