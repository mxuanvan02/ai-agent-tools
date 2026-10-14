# Luật cứng rút ra khi QA slide + handout (đo được, đã trả giá)

SKILL.md đã vượt giới hạn ký tự nên các luật này nằm ở đây. Đọc khi sửa cỡ chữ, cắt chữ thừa, build handout, hoặc viết cổng kiểm.

## 1. Cổng "chữ vừa khung" phải đo cả KHOẢNG CÁCH, không chỉ số chữ

Khi chữ tràn khỏi thẻ/hộp, thủ phạm thường là `space_after` chứ KHÔNG phải câu dài.

Bằng chứng: hộp 6 đoạn × `space_after` 9pt = 54pt khoảng trắng, đủ làm tràn 9pt dù cắt chữ vẫn không hết. Cắt chữ chỉ giảm 14 → 11 lỗi; giảm `space_after` 9pt → 5pt đưa về **0 lỗi** mà công thức vẫn giữ 15pt.

Trước khi cắt chữ, in ra ba số: chiều cao hộp, tổng chiều cao chữ ước lượng, `space_after` từng đoạn. Nếu tổng khoảng cách > phần tràn, sửa khoảng cách — giữ được cỡ chữ.

Và cổng phải đo **chữ so với thẻ chứa nó**, không chỉ va chạm giữa các span — hai phép đo khác nhau, chỉ cái thứ nhất bắt được tràn mép thẻ.

## 2. Cỡ chữ TRONG ẢNH không phụ thuộc font size khi vẽ ảnh

```
pt trên màn chiếu = (chiều cao chữ ÷ chiều rộng công thức) × 72 × bề rộng hộp(in) ÷ hệ số ink/em
```

Nghĩa là vẽ lại PNG với font to hơn mà giữ nguyên tỷ lệ là **vô ích**. Chỉ ba đòn bẩy: nới hộp, rút chiều rộng nội dung, tách dòng. Đo cả ba trước khi làm.

Đã trả giá:
- Định đổi công thức sang dạng gạch chéo vì "trông gọn hơn" → đo ra **8.8pt, tệ hơn** bản gốc, vì công thức dài hơn (AR 19.1 so với 11.2).
- Phương án cho chữ to nhất (26.9pt) là phương án **bỏ chỉ số trong công thức đã đăng** → phải từ chối.
- Tách 2 dòng cho 19.6pt nhưng cao 2.30in > khe 1.78in → đè lên chữ bên dưới.

Bẫy kèm theo: dấu ngoặc `\left( \right)` cao theo `\frac` làm chữ nhỏ tương đối. Dùng `\bigl \bigr` lấy lại ~1.2 điểm.

Muốn biết bộ chữ nào khớp deck: render cùng một công thức bằng 2 bộ chữ, cắt cùng một khoảng, ghép dọc, rồi hỏi vision về **phong cách** (serif/sans, nét đều/thanh-đậm). Đừng so bằng ngưỡng lấy từ trí nhớ.

## 3. Cổng cỡ chữ phải loại ảnh ngoài canvas và ảnh nhận diện

- Ảnh có `left ≥ chiều rộng slide` (hoặc ra ngoài theo top) **không bao giờ hiển thị** → đo là báo oan. Đã gặp: 3 ảnh S1 ở left 25.69 / 13.79 / 21.10in trên slide rộng 13.333in.
- Logo/huy hiệu: chữ trên đó không ai cần đọc từ cuối phòng.

Nhưng **không được im lặng**: in ra số lượng bị loại và lý do, để người duyệt thấy cổng đã bỏ qua cái gì.

## 4. Waiver phải TỰ VÔ HIỆU HOÁ khi số đo đổi

Khi một ảnh không sửa được thật (đã đo hết mọi đòn bẩy), ghi waiver theo bộ ba `slide + wpx + hpx + pt đo được` với sai số ≤ 0.3pt. Ảnh bị vẽ lại hay thay blob thì px đổi → waiver tự chết → cổng FAIL lại. Waiver cũ không che được lỗi mới.

Mỗi mục phải có: bằng chứng đã thử (scale hộp tối đa, crop gain, trần boost, % component dưới ngưỡng) và **kịch bản nói có bù thông tin đó không**. Waiver không có phần bù bằng lời thoại là waiver yếu.

Cổng in waiver thành CANH BAO, không im lặng.

Đã trả giá: suýt hạ ngưỡng 12pt xuống cho "đỗ" — đó là phá cổng chứ không phải sửa slide.

## 5. Không vẽ lại ảnh khi nội dung trong nó không có ở nguồn nào khác

Ảnh raster mồ côi (không có script vẽ) có thể chứa số liệu chỉ tồn tại trong chính nó. Kiểm bằng grep toàn repo + file dữ liệu thật TRƯỚC khi quyết định vẽ lại.

Bằng chứng: sơ đồ S7 chứa 3 nhiệt độ (36.8 / 29.1 / 30.4) **không có trong bất kỳ file dữ liệu nào** (`ground_truth_csv.json` không; grep toàn repo chỉ khớp nhầm `136.8`). Vẽ lại = bịa số liệu → giữ nguyên, ghi waiver.

Ngược lại, ảnh công thức thì vẽ lại được vì công thức có trong bản thảo (`paper_body.tex`) — và phải đối chiếu từng thành phần với bản thảo trước khi thay.

## 6. Vision đọc chữ nhỏ trên slide KHÔNG đáng tin cho số liệu

Đã gặp hai lần:
- Đọc sai số liệu thật: đổi tên phương pháp, đổi phần trăm, đổi p-value.
- Đọc sai một từ trong tên trường trên huy hiệu ("Engineering" thay vì "Education").

Chỉ dùng vision cho: phong cách, bố cục, có bị cắt/chồng lấn không, có chữ thừa không, đọc chữ in lớn.

Mọi con số và chuỗi ký hiệu phải đối chiếu **text layer** của deck/PDF hoặc nguồn dữ liệu. Khi nghi vấn (ví dụ logo lạ trên slide), kiểm chứng bằng nguồn công khai trước khi kết luận — đừng kết luận oan, cũng đừng bỏ qua.

## 7. Hàm gộp Markdown phải idempotent

Script chèn khối vào `.md` phải XOÁ khối cũ cùng loại trước khi chèn. Chạy hai lần sẽ nhân đôi khối và mọi cổng đếm phía sau fail với con số khó hiểu.

Bằng chứng: 259 cue trong khi thật có 156, vì MD bị lồng 38 khối "KỊCH BẢN NÓI" thay vì 19.

Khi thấy số đếm lớn bất thường, nghi ngờ đầu tiên là **chèn trùng**, không phải "dữ liệu tăng".

Kèm theo: thêm loại cue mới thì phải sửa **ba chỗ** hay sót — bảng ký hiệu `KIND_VI`, regex liệt kê nhãn, và vòng canh lề song ngữ (nhánh `else` sẽ nuốt cue mới). Regex liệt kê cứng từng nhãn (`CHỈ TAY|NÓI|ĐỌC TO|CỬ CHỈ`) sẽ bỏ sót nhãn mới; dùng dạng tổng quát `〔[^〕]+〕`. Và nếu nhãn tuỳ chọn đứng TRƯỚC nhãn cue thì regex đếm giờ cũng hỏng — ghép nhãn thành `〔NÓI · NẾU DƯ GIỜ〕`.

## 8. Bẫy công cụ hay gặp lại

- `sh is skip` **luôn False** với python-pptx: mỗi lần duyệt nó tạo object wrapper mới. Lọc theo `shape_id` (đọc từ XML, ổn định).
- `set -e` + `| tail` che lỗi: chuỗi dừng ở lệnh fail nhưng exit code là của `tail`. Ghi log ra file rồi đọc.
- `\setlength{\mathindent}` chỉ tồn tại trong mode display `fleqn` → `Undefined control sequence` khi dùng với math inline.
- `argmin()` trên mảng 2 chiều trả **chỉ số phẳng** → phải `unravel_index`.
- `assert len(...) == 137` hardcode sẽ chết khi thêm cue. Dùng hằng có tên + comment nguồn con số.
- Ảnh ghép ngang 10578×208px làm `vision_analyze` **timeout**; giữ cạnh dài dưới ~1100px.
- Khi đổi kích thước ảnh trong deck, grep toàn bộ pipeline theo **kích thước px cũ** — nhiều script tra ảnh theo `(w,h)` và sẽ `KeyError`/`assert`.

## 10. Audit số liệu: phải có positive control, và phải audit cả tài liệu mình viết

Ba luật đã trả giá thật khi đối chiếu 470 con số trong deck với CSV/code:

**(a) Matcher không có positive control là vô dụng.** Lần chạy đầu báo "70 số VERIFIED" nhưng một con số BỊA (`0.08842`) vẫn khớp. Nguyên nhân: pool chứa file `*raw*.csv` per-row (45272 số) — số công bố là thống kê tóm tắt nên khớp raw là trùng ngẫu nhiên. Loại raw khỏi pool, đo false-accept bằng 40 số ngẫu nhiên: **0.0% (pool mạnh) so với 12.5% (pool raw)**. Chỉ sau đó kết quả mới đáng tin.

**(b) Số dẫn xuất không bao giờ khớp bằng value-equality.** `0.0158` báo UNACCOUNTED cho tới khi tính lại `mean(Mhat_win)` từ 240 dòng CSV = 0.015793. Trung bình, tổng, tỷ lệ, p-value đều phải **tái tạo bằng phép tính**, không phải tìm chuỗi.

**(c) Tài liệu mình tự viết là artifact ít được kiểm nhất.** Cảnh báo thống kê trong handout khẳng định "tiêu đề bảng ghi `p (Holm)` nhưng không có hiệu chỉnh Holm nào trong code" — **sai hoàn toàn**: bảng đã đăng ghi `$p$` + caption "p values are unadjusted", PDF bài báo có "Holm" 0 lần, và code Holm thật nằm ở `legacy/`. Grep cũ chỉ quét một cây đã bị thay thế. Nếu người dùng đọc theo, họ sẽ tự hại mình trước hội đồng.

Bài học vận hành: khi viết ghi chú/cảnh báo vào artifact, **ghi kèm phạm vi đã kiểm** (cây nào, ngày nào, file nào) để lần sau biết nó còn đúng không. Và ưu tiên chạy verifier của chính dự án trước khi tự tính — nó mã hoá đúng định nghĩa denominator của tác giả.

## 11. Cổng phát hiện được mà không chặn = cổng fail-open

`build_pdf.py` in ra `!! CON TOFU - phai them vao bang REPL` nhưng `sys.exit()` chỉ xét danh sách chuỗi bắt buộc → build vẫn **PASS** với ô vuông trong PDF.

Đã gặp lớp lỗi này trước đó (`return 0` khi ImportError). Quy tắc: mọi chỗ in cảnh báo phải gán một biến cờ, và kết luận cuối phải gộp **mọi** cờ. Kiểm bằng cách cố tình đưa ký tự không render được vào nguồn rồi xác nhận build FAIL.

Với font Gentium Book Plus: `⟹` (U+27F9) không có → thay bằng `→` (U+2192, đã chứng minh render tốt).

## 12. Vẽ lại sơ đồ: khổ giấy = hộp hiển thị thì cỡ chữ 1-đổi-1

Đừng kết luận "không phóng được" chỉ vì đã đo **phóng hộp ảnh PNG có sẵn** (bị chặn bởi lề, ví dụ trần 1.12x). Còn một hướng mạnh hơn nhiều: **vẽ lại với figsize đúng bằng hộp hiển thị**, khi đó

```
pt trên màn chiếu = fontsize vẽ × (box_w_in / figsize_w_in)
```

Nếu hai bề rộng bằng nhau thì hệ số ≈ 1 → vẽ 13pt ra đúng 13pt trên slide. Đã dùng cách này đưa sơ đồ Gateway từ ~11.7pt lên **13.0pt** mà box giữ nguyên từng EMU.

**Hai cái bẫy đi kèm:**

- **Tử số và mẫu số rất dễ viết ngược.** Hệ số là `box / figsize`, KHÔNG phải `figsize / box`. Khi figsize lớn hơn box thì ảnh bị **thu nhỏ** khi nhét vào → chữ trên slide phải **nhỏ hơn** fontsize vẽ. Viết ngược sẽ cho một ảnh dưới ngưỡng "đạt oan" — lỗi nguy hiểm nhất vì nó làm cổng xanh giả. Kiểm bằng cách in ra cả ba số (fontsize vẽ, box, figsize) và tự nhẩm một trường hợp bất đối xứng; ảnh có hai bề rộng gần bằng nhau sẽ **che mất** lỗi này.
- **Bộ đo dò "nhãn trục toạ độ" không áp dụng được cho sơ đồ không có trục.** Nó sẽ vớ vài mảnh vụn trong dải lề rồi báo số vô lý (sơ đồ 13pt bị báo 3.2pt; bản cũ bị báo 6.8pt). Với ảnh do chính ta vẽ, biết trước fontsize và figsize, thì **tính trực tiếp** — đó là phép tính chặt, mạnh hơn mọi phép đo pixel. Khi sửa bộ đo, nhớ quét cả những ảnh sơ đồ **khác** đang bị đo oan bằng cùng phương pháp.

**Hiệu chuẩn vi sai khi hai phép đo mâu thuẫn:** vẽ chữ ở cỡ **đã biết trước** (11/13/15/17pt) bằng đúng pipeline, đo lại, suy ra `px trên 1pt` kèm lệch chuẩn. Rồi áp hệ số đó cho ảnh thật. Cách này phân xử được tranh cãi mà không phải chọn số có lợi cho mình.

**Trước khi vẽ lại ảnh raster mồ côi, phải đối chiếu từng chuỗi chữ với nguồn.** Nhưng đối chiếu **theo token/khái niệm**, không theo nguyên chuỗi: nhãn trên sơ đồ thường diễn đạt khác thân bài một chút (`bursty wireless channel` so với `Bursty wireless loss`). Khớp nguyên chuỗi sẽ báo oan hàng loạt. Giá trị số liệu (nhiệt độ, ...) thì kiểm ở **dữ liệu thô**, không phải ở text slide — chúng thường không xuất hiện trong text.

**Cổng so sánh phải đo đúng đại lượng.** Từng viết cổng "AR giữ nguyên" nhưng lấy AR của *bbox vùng mực* thay vì AR của *file ảnh*. Vẽ lại bố cục khác thì vùng mực đổi hình dạng là đương nhiên → cổng FAIL oan. Đại lượng quyết định méo ảnh là `width/height` của file.

## 13. Định dạng đồng hồ nói

Từ ÷ wpm cho ra **phút dạng thập phân**. Đổi ra `ph:giây` phải nhân 60 trước rồi mới tách: `s = round(x*60); f"{s//60}:{s%60:02d}"`. Viết `int(x//60)` trên x đã là phút sẽ in `0:20` thay vì `19:48` — báo sai cho người dùng.

Và luôn in **nhiều tốc độ nói** (125/120/115 wpm), vì trần hội nghị tính theo phút thật chứ không theo tốc độ giả định.
