# Nhúng icon thật và các cổng QA đo được

Hai phần: (A) đưa icon vector vào PPTX, (B) bộ cổng QA đo bằng số thay cho rà mắt.

## A. Nhúng icon từ kho SVG vào PPTX

Kho icon của `ppt-master` (`templates/icons/`, 5 thư viện) dùng được cho deck tiếng Việt, nhưng phải qua ba bước.

### A1. Tên icon KHÔNG suy diễn được — phải xác minh trước khi dựng

Tên icon là tên tệp thật, phân biệt hoa thường, và **không portable giữa các thư viện**. Trong một phiên, các tên sau đều không tồn tại ở `tabler-filled`: `rotate-clockwise`, `sum`, `square-root-2`, `tool`, `printer`, `medal`, `users`, `equal`, `math-greater`, `arrow-right`, `hierarchy`, `network`, `refresh` (Bài 17 gặp thật, dựng báo `FileNotFoundError: .../refresh.svg`).

Quy tắc:

- Tra theo **vật thể vẽ được**, không theo khái niệm trừu tượng: `bulb` có, `idea` không; `trending-up` có, `growth` không.
- Trước khi dựng, chạy một vòng kiểm tra toàn bộ tên icon mà script sẽ dùng, in ra danh sách `MISSING`, rồi mới sửa.
- Khi tên thiếu, tra ứng viên bằng glob trong **đúng thư viện đang dùng** rồi chọn tên có thật. Thay thế đã dùng: `rotate-clockwise → circle-arrow-right`, `sum → circle-plus`, `square-root-2 → square-number-2`, `tool → settings`, `refresh → exchange` (Bài 17: ý cập nhật biến), `git-fork/binary-tree → binary-tree`, `sitemap` cho sơ đồ nhiều nhánh.
- Cẩn thận với chuỗi ghép f-string: `circle-number-` sẽ luôn hiện trong danh sách MISSING vì nó là tiền tố, không phải tên. Bỏ qua đúng trường hợp này, không "sửa" nó.

### A2. `fill="currentColor"` làm icon render ra trắng trơn

SVG trong kho ghi `fill="currentColor"`. Rasterize trực tiếp cho ảnh **0 pixel có mực** — nhìn như đã chèn nhưng slide trống chỗ đó.

Cách xử lý: thay `currentColor` bằng mã màu hex thật rồi mới render. Rasterizer dùng được là `cairosvg` (cài bằng `pip3 install cairosvg`). Bọc lại thành một hàm dùng chung, trả về đường dẫn PNG đã cache theo `(tên, màu, kích thước)`.

Luôn xác minh bằng số điểm có mực sau khi render, đừng tin việc lệnh chạy xong:

```python
im = Image.open(png).convert('LA')
ink = sum(1 for _, a in im.getdata() if a > 8)
assert ink > 0, 'icon render ra trang tron'
```

### A3. Thay ký hiệu chữ bằng icon ở một chỗ duy nhất

Đừng sửa hàng chục chỗ gọi. Khai báo một bảng ánh xạ `ký hiệu cũ → tên icon` (`'1'..'9'`, `'!'`, `'✓'`, `'▶'`) rồi để hàm `card()`/`flow()` tự tra bảng đó. Thêm icon cho cả deck chỉ bằng một lần sửa helper.

Dấu hiệu icon đã vào thật: dung lượng PPTX tăng rõ (144 KB → 223 KB) và số shape kiểu `PICTURE` tăng theo.

## B. Cổng QA đo được, không phụ thuộc rà mắt

Rà contact sheet vẫn là cổng cuối, nhưng phải có các cổng đo bằng số đứng trước, vì chúng bắt được lỗi mà mắt bỏ qua (icon chồng toạ độ, chữ cấn mép thẻ 3 pt) và vẫn chạy được khi công cụ thị giác không phản hồi.

Bộ cổng đã dùng, đặt chung một thư mục công cụ (`slide_sources/qa_tools/`) và **truyền đường dẫn PPTX/PDF qua tham số dòng lệnh** để dùng lại cho mọi bài:

| Cổng | Đo gì | Ngưỡng đạt |
|---|---|---|
| QA cấu trúc | số slide, notes rỗng, shape ngoài biên, thứ tự 4 slide mở đầu, chuỗi bắt buộc/cấm | `outside=[]`, notes đủ, `thieu=[]`, `forbidden=[]` |
| Cắt chữ theo mực in | toạ độ **từ đã render** trong PDF so với mép thẻ chứa nó | `so_van_de = 0` |
| Style | số icon, hộp nền tối, thẻ tô màu chồng nhau | `nen_toi=0`, `chong_lan=0` |

### B1. Cắt chữ phải đo trên bản đã render, không đo bằng font metrics

Ước lượng bề rộng chữ bằng font metrics cho **131 cảnh báo** trong khi bản chuẩn đã duyệt cho 137 — vô dụng, vì font trình bày (Aptos) không có trên máy nên metrics rơi về font dự phòng.

Cách đúng: lấy hộp bao của **từng từ đã render** bằng `pdftotext -bbox-layout`, đối chiếu với hộp bao của thẻ tô màu chứa nó (đọc từ PPTX, quy đổi EMU → pt bằng `/12700`). Cách này cho 14 vấn đề đều thật, và về 0 sau khi sửa. Ngưỡng bỏ qua descender khoảng 3 pt: vượt `duoi` cỡ 2–4 pt trên chữ có dấu là hiện tượng bình thường của thẻ chật, chỉ sửa khi đó là chữ đè lên ô bảng bên dưới.

### B2. Tách âm giả bằng baseline, đừng sửa theo cảnh báo

Trước khi sửa bất kỳ cảnh báo nào, chạy **cùng bộ dò đó** lên một deck đã được duyệt. Vấn đề nào xuất hiện ở cả hai là nhiễu của template, không phải lỗi mới. Kỹ thuật này đã loại 125/131 cảnh báo trong một lần.

### B3. Ngưỡng phải nằm ở một bộ dò dùng chung

Copy bộ dò sang bài mới rồi đổi ngưỡng gây kết luận trái ngược trên cùng một deck: `lum < 0.45` báo 26–28 "hộp nền tối" trong khi ngưỡng đã chốt `lum < 0.30` cho 0 — tất cả đều là thanh nhãn xanh nhấn mà người dùng đã duyệt. Ngưỡng chốt hiện dùng: nền tối là `lum < 0.30` **và** diện tích `>= 1.0 in²`.

### B4. Chồng lấn: chỉ so thẻ tô màu với thẻ tô màu

So mọi shape với nhau cho 159 "chồng lấn" đều là âm giả: textbox nằm **trong** thẻ chứa nó, tỷ lệ phủ 1.0 — đúng thiết kế. Chỉ so các shape có tô màu với nhau, và chỉ báo khi tỷ lệ phủ nằm trong khoảng `0.12 < r < 0.92`.

### B5. Bộ dò chuỗi cấm phải theo bài, không copy nguyên

Chạy bộ dò của bài trước lên bài sau cho một rừng `pdf_thieu`/`con_bai_tap` sai, vì danh sách chuỗi bắt buộc/cấm bị ghim cứng theo bài cũ. Mỗi bài có bộ chuỗi riêng; phần đo hình học thì dùng chung được.

Ngoài ra, khớp chuỗi cấm phải **xác minh ngữ cảnh** trước khi sửa: `Vận dụng` bị báo còn sót thực ra là chữ trong tiêu đề "Mở rộng và vận dụng" và một động từ trong speaker note, không phải slide bài tập. Cùng loại: dò `ghi vở` khớp cả "ghi vào biến" ở slide code. In ra nguyên văn ngữ cảnh rồi mới quyết định.

## C. Khi công cụ thị giác không phản hồi

Không bỏ cổng trực quan, cũng không chờ. Trình tự đã dùng:

1. Chạy đủ ba cổng đo ở mục B, kèm baseline so sánh.
2. Kiểm tra riêng những gì mắt hay bắt: icon trùng toạ độ, chữ cấn mép thẻ, glyph thiếu trong font, số trang, chuỗi bắt buộc trong PDF đã render.
3. Render contact sheet và ảnh soi cận vùng vừa sửa, **gửi cho người dùng soi mắt**, ghi rõ đây là bước chưa tự động hoá được.
4. Chỉ phát hành sau khi cả ba cổng sạch; ghi lại trong tiến độ rằng cổng trực quan do người dùng duyệt.

Về glyph: kiểm tra ký hiệu dễ lỗi (`→`, `≈`, `▶`, `✓`) có nằm trong font đang dùng. Thiếu ở font chính nhưng có ở font dự phòng hệ thống thì vẫn render đúng — so với deck baseline để khỏi báo động sai.
