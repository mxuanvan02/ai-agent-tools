---
name: vietnamese-classroom-slide-production
description: Thiết kế, viết lại, kiểm tra và phát hành bộ slide bài dạy THPT bằng tiếng Việt từ đúng deck hiện hành và nguồn KHBD/PPCT. Dùng khi cần giữ nhận diện nền–header–footer nhưng dựng lại nội dung, bổ sung ví dụ STEM/AI/IoT, ghi chú giáo viên, QA PPTX/PDF và cập nhật tuần tự lên Drive.
version: 1.0.0
---

# Vietnamese Classroom Slide Production

## Luật cứng: cổng số từ KHÔNG được đạt bằng cách xoá chữ

Cổng design "≤60 từ/slide" chỉ đạt hợp lệ khi nội dung được CHUYỂN VÀO ẢNH, không phải bị xoá đi. Ảnh không bị đếm từ nên đạt cả cổng mật độ lẫn cổng nội dung.

Sau MỌI lần cắt chữ, bắt buộc kiểm hai bước trước khi báo xong:
1. Đếm shape thân slide (y trong 1.45–6.9) và số ảnh có width > 2in. Slide có ≤4 shape thân VÀ 0 ảnh = RỖNG → fail, không được gửi.
2. Render PDF rồi vision_analyze ít nhất 2 slide đã cắt, hỏi thẳng "có vùng trống lớn bất thường / chữ mồ côi lơ lửng không". Chữ giữ lại vì keep-list mà mất ngữ cảnh xung quanh sẽ thành dòng mồ côi — đó là lỗi, không phải tiết kiệm.

Đã trả giá: tối ưu con số cổng thay vì slide dạy được, kết quả 18/20 slide chỉ còn 1–2 dòng chữ lơ lửng trên nền trắng dù cả hai cổng đều PASS.

Khi cổng nội dung và cổng thiết kế kéo ngược nhau trên cùng một template chữ dày, không chọn một trong hai bằng cách cắt — giải bằng ảnh.

## Phạm vi

Dùng cho một bài hoặc cả bộ bài giảng THPT. Kết hợp bắt buộc với `powerpoint` để thao tác PPTX và `academic-prose` để viết tiếng Việt học thuật–sư phạm.

## Cổng nội dung theo phản hồi của giáo viên

- **Ghi vở là khái niệm và nguyên lí tổng quát.** Giữ nhãn `NỘI DUNG GHI VỞ`; không đổi thành `Gợi ý ghi vở (ví dụ)`. Khi giáo viên nói “đó là ví dụ thôi”, đối tượng là thiết bị/tình huống/số liệu minh hoạ, không phải kiến thức cần ghi. Không đưa số tệp, mã nhóm, nhiệm vụ hay số lượng ví dụ thành điều kiện ghi nhớ.
- **Tách kiến thức – ví dụ – tổ chức lớp.** KHBD là nguồn truy vết, không phải văn bản để chép lên slide. Mã nhóm, nộp bài, đổi vai, điền ô, nhật kí nhiệm vụ và ca kiểm tra bắt buộc thuộc tài liệu hoạt động riêng. Mục tiêu/YCCĐ vẫn có thể dùng động từ năng lực; thân bài trình bày lời giải thích và ví dụ đã phân tích, không giao việc. Đổi “bắt buộc” thành “gợi ý” mà giữ nguyên nhiệm vụ vẫn không đạt.
- **Hình phải giải thích cơ chế.** Không dùng số lượng icon làm bằng chứng trực quan. Thay bảng chữ bằng hình thiết bị đủ lớn, dữ liệu đặt cạnh đối tượng và mũi tên có ý nghĩa; không rải icon nhỏ đè lên bảng. Icon thay thế phải đúng vật thể, không dùng cối xay gió thay quạt hoặc giọt nước thay máy giặt.
- **Sửa toàn bộ các nơi cùng nói một kiến thức.** Sau khi sửa ghi vở, rà ví dụ, tiêu đề, chú thích, notes và kết luận để loại mâu thuẫn. Quét từ chỉ tạo danh sách nghi vấn; phải đọc nội dung thật. `0 cắt chữ`, `0 từ cấm`, số ảnh và checksum không chứng minh chất lượng sư phạm hay thị giác. Ít cảnh báo hơn baseline không tự biến lỗi còn lại thành âm giả.
- **Không lặp lời hứa thay thao tác.** Mỗi cập nhật tiến độ phải gắn thay đổi hoặc kết quả mới. Lệnh thiếu tham số phải sửa tham số; không gọi lại rỗng. Subagent trả lỗi API dù nhãn `completed` vẫn chưa thực hiện công việc: chuyển sang làm trực tiếp hoặc đường khác, không tuyên bố đã sửa. Khi đang duyệt lại, chỉ tạo bản local và gửi duyệt; không tự ghi đè Drive. **Patch qua `execute_code` phải kiểm tra giá trị trả về** (`r.get('success')`), không tự `print('OK')`: patch fail vẫn in OK rồi build ra deck từ code cũ, và mọi QA sau đó đo trên bản chưa sửa. Xác minh độc lập bằng `grep -c '<chuỗi mới>'` trên file nguồn và `pdftotext` đúng trang đã sửa; chuỗi mới = 0 hit nghĩa là chưa sửa được gì. **Exit code của pipeline là của lệnh cuối**: `python3 build.py | tail -3; echo $?` luôn trả 0 dù build fail, phải `python3 build.py > log 2>&1; echo $?`. Số đo QA chỉ có giá trị trên bản build mới nhất, nên đối chiếu mtime PPTX/PDF trước khi tin kết quả.

- **Mỗi cổng PHẢI có đối chứng dương, và không được diễn giải "thiếu khóa" thành "thất bại".** Cổng tự chế đã cho em kết luận sai bốn lần liên tiếp trên cùng một ảnh, tất cả do lỗi CẤU TRÚC cổng chứ không phải do ảnh: (1) cổng so `norm(text)` trong khi `norm = re.sub(r'[^0-9a-zA-Z]','',s)` XÓA SẠCH dấu tiếng Việt, nên `norm('Tin học') == norm('Tin hoc')` — cổng không thể phân biệt ảnh có dấu với ảnh mất dấu; (2) ngưỡng tách dòng `ink > 3` loại đúng hai hàng mực 3px là dấu chấm dưới chữ `ọ`, khiến `>>o<<` và `>>ọ<<` cho ra mask giống hệt nhau và cổng kết luận "xterm không vẽ được dấu" (sai — đo lại đúng: `>>o<<` cao 17px, `>>ọ<<` cao 23px, `>>ấ<<` cao 26px); (3) cổng chọn dòng probe bằng ngưỡng tỉ lệ `width < 0.45*strip` nên gộp cả dòng bash echo lệnh vào tập probe, đếm 7 dòng thay vì 6 và FAIL mà chưa đo gì; (4) cổng `not rec.get('identical', True)` — khi hai glyph KHÁC KÍCH THƯỚC thì dict không có khóa `identical`, `.get` trả mặc định True, cổng kết luận harness sai dù "khác kích thước" chính là một dạng phân biệt được; (5) tiền đề `any(c.encode() in raw for c in 'ọđấể')` dò bốn chữ cứng nên báo "file không có dấu" cho file chứa `'Mã số 1023'`. Hai luật bắt buộc: cổng phải chạy ĐỐI CHỨNG DƯƠNG trên dữ liệu đã biết đúng trước khi kết luận về dữ liệu thật (em dựng ảnh PIL cùng font rồi yêu cầu cổng phải phân biệt được `o`/`ọ`, nếu không thì tự hủy — nhờ đó bốn kết luận sai không đi vào báo cáo); và mọi nhánh diễn giải phải liệt kê tường minh đủ trường hợp (khác kích thước / cùng kích thước khác pixel / không so được), không để mặc định mơ hồ. Ưu tiên so hai biến thể TRÊN CÙNG MỘT ẢNH để triệt tiêu font, cỡ chữ, baseline và đường chụp thay vì so với ảnh tham chiếu dựng lại.
- **Đo chữ có dấu trong ảnh terminal: CẤM dùng OCR, và phép đo phải là so hai biến thể TRÊN CÙNG MỘT ẢNH.** Ba luật đã trả giá, kèm số đo thật: (1) OCR rapidocr MÙ dấu tiếng Việt — 12/12 phép thử trên ảnh PIL chắc chắn có dấu vẫn đọc mất dấu (`"S = 'Mã số 1023'"` → `"S 'Ma s6'1023"`, `"print('Trường THPT Thuận Hóa')"` → `"print('Truong THPT Thuan H6a')"`), và hàm `norm()` của dự án (`re.sub(r'[^0-9a-zA-Z]','',s)`) XOÁ SẠCH dấu nên `norm('Tin học') == norm('Tin hoc')` — mọi cổng needles/gt đi qua nó không thể phát hiện ảnh mất dấu. (2) Phép đo đúng: in hai biến thể `>>Tin học<<` và `>>Tin hoc<<` trên CÙNG một ảnh xterm; font monospace nên cùng số kí tự ⇒ Δw=0, còn dấu chấm dưới/mũ làm Δh>0. Đo được Δh = +6/+6/+4 px với Δw=0 ở cả ba cặp → xterm VẼ ĐƯỢC dấu. Vậy ảnh cũ hiện `\u1ecdc` là do không GÕ/DÁN được chữ có dấu, không phải do font; sửa bằng cách giữ code trong file `.py` UTF-8 rồi `cat` + `python3` nó trong bash (dùng class `BashTerm` có sẵn trong `term_fix.py`, KHÔNG phải `Term` vốn là REPL Python). (3) Khi buộc phải định vị dòng để đo từng ảnh: định vị bằng BỀ RỘNG KỲ VỌNG `len(text) × unit` (unit ≈ 17.7 px/kí tự ở BashTerm font 22, calib bằng chính phép thử trên) rồi PHÂN BIỆT các band cùng bề rộng bằng IoU với ảnh PIL dựng lại của đúng chuỗi đó (đã đo: 4 band cùng 279px cho IoU 0.633 / 0.105 / 0.103 / 0.103). Đừng định vị bằng chữ OCR đọc được — nó sẽ khớp nhầm dòng lệnh bash dài 1643px và dựng tham chiếu font 90px để so với dòng 30px. (4) Hàm tách dòng phải có `min_ink=0` + `gap_merge≈4` (dấu phụ chỉ 2–3px mực và cách thân chữ 2 hàng trắng; ngưỡng `ink>3` cắt mất dấu) VÀ phải CHẶN `max_h≈42px` sau khi gộp: pitch dòng terminal ~37px, một dòng thật cao 29–31px, nên band 60px chắc chắn là hai dòng bị gộp (xảy ra khi hàng mờ 2–12px nối hai dòng). Mọi cổng loại này phải có ĐỐI CHỨNG DƯƠNG (ảnh PIL đã biết đáp án) và ĐỐI CHỨNG ÂM (dòng ASCII, Δh phải = 0) và phải TỰ DỪNG khi đối chứng hỏng.
- **Trước khi viết cổng mới, kiểm tra công cụ sẵn có bằng grep — em đã hai lần chế lại thứ đã tồn tại.** `term_pipeline.capture(script=...)` gửi cú pháp shell `python3 file.py` vào xterm mở bằng `-e python3 -i -q` (REPL Python) nên ra `File "<stdin>", line 1 ... SyntaxError`; năm file nguồn chưa từng chạy, ảnh chụp toàn báo lỗi mà cổng vẫn chấm ĐẠT vì needles là chữ số ngắn (`'10'`, `'2'`) có mặt trong text lỗi. Đồng thời em vá thêm tham số `interp='shell'` vào `Term` trong khi `term_fix.py` đã có sẵn class `BashTerm` proven (đã dùng cho BAI_31) — phải dùng cái có sẵn, không chế song song. Ảnh terminal đã phát hành được dựng bằng `recrop3` (crop sát chữ + chia cột để đạt ≥13.2pt), KHÔNG phải `crop_strip`: hàm sau crop theo bbox mực tối mà scrollbar xterm tạo ~115 cột tối suốt chiều cao nên bbox phủ cả ảnh, cho ra ảnh 1764×1018 toàn nền trắng và chữ nhỏ lại. Trước khi viết hàm đo/crop ảnh terminal, grep xem đã có hàm nào làm việc đó và ảnh đã phát hành được sinh ra bằng hàm nào.

- **Chia cột strip terminal: điểm cắt phải nằm ở hàng trống TUYỆT ĐỐI và phải verify SAU khi upscale.** Hai lỗi đo được: (1) `find_line_bands` coi hàng có `v <= 2` mực là hàng trắng, nên hàng còn 1–2px (đỉnh dấu mũ, nét mảnh) vẫn được chọn làm điểm cắt → glyph bị cắt ngang; audit 31 strip đã phát hành ra đúng 1 ca (`b24_02_duyet_xau` mép trên cột 2, mực dính sát viền). (2) Sửa bằng cách đòi khoảng trống ≥2 hàng vẫn CHƯA ĐỦ: `recrop` upscale 2x bằng LANCZOS ở bước cuối, kernel có ringing nên mực RỈ sang hàng trống → strip thành phẩm vẫn còn 7px dính mép. Phải đòi khoảng trống rộng hơn (`min_gap=6`) và **dựng ra file tạm, đo lại vết cắt, chỉ ghi vào artifact khi đạt**; chưa đạt thì tăng `min_gap` (6→10→14→20→28) rồi dựng lại, không hy vọng một lần ăn ngay. Tiêu chí đo vết cắt phải CHẶT: mực dính sát viền (0–3 hàng sau khi trừ viền khung 3px và đường phân cách cột) mới là bị cắt; descender nguyên vẹn nằm cách mép 11 hàng trắng thì KHÔNG tính — cổng lỏng (`có mực >4px trong 14 hàng sát mép`) đã báo oan 30/31 strip. Mọi thay đổi hàm dựng ảnh dùng chung phải kèm REGRESSION CONTROL: dựng lại bằng tham số mặc định và so sha256 với strip đã phát hành (đạt 12/12), tham số mới phải opt-in để không âm thầm đổi artifact cũ.
- **Cổng đếm từ/đếm shape phải so với BASELINE ĐÚNG, và structure gate phải parse XML chứ không regex.** Hai lỗi: (1) sửa chữ làm tăng số từ, nên phải so bản live với backup tạo TRƯỚC lần sửa chữ đó — so với backup tạo sau thì luôn ra 0 thay đổi và bỏ lọt regression. Đo đúng baseline cho kết quả: 8 slide đổi ±1–2 từ, 0 slide mới vượt ngưỡng 60 từ. (2) structure gate viết bằng regex `<p:(\w+)[ />]` trên nội dung `spTree` sẽ bắt cả tag LỒNG SÂU (`cNvPr`, `cNvGrpSpPr` là con của `nvGrpSpPr`, hoàn toàn hợp lệ) → 83 âm giả. Phải parse bằng lxml và kiểm whitelist chỉ trên CON TRỰC TIẾP của `spTree`; invariant đếm cặp `<p:sp>`/`<p:nvSpPr>` thì vẫn đếm trên toàn cây. Bằng chứng nhanh để biết cổng sai hay file sai: so sha256 của part bị nghi (`slideMaster1.xml`) giữa backup và bản đã sửa — nếu KHÔNG ĐỔI thì ta chưa từng đụng part đó, vậy cổng sai.
- **Ảnh đặt vào slide phải tính pt tại chiều cao THẬT, không tại hằng số mà strip được tối ưu cho.** `recrop` tối ưu số cột theo `BAND_H = 2.10in` (hằng cứng), nhưng band thật trên slide đo được chỉ 1.84in (`room_top` = đáy card phía trên, `room_bottom` = đỉnh caption phía dưới). Strip vì thế đạt 14.8pt@2.10in nhưng chỉ 13.0pt khi đặt thật — dưới sàn 13.2. Hai việc phải làm: (a) hàm đặt ảnh phải tính `pt_thật = pt_note × h_đặt / 2.10` và so với sàn bằng con số đó, không so với pt trong note; (b) phải dùng CẢ band dọc — neo `top` cũ cố định rồi chỉ tìm room phía dưới sẽ bỏ phí khoảng trống phía trên ảnh (đo được 0.55in bị bỏ phí, trong khi chỉ thiếu 0.03in), và lề dọc 0.10in mỗi bên cũng đáng kể (giảm còn 0.06in là đủ cứu ca đó). Chọn box bằng cách fit đúng AR vào cả `avail_w` và `avail_h` rồi canh giữa band, không thu cỡ chữ, không cắt ảnh.

- **Notification của job nền đến trễ KHÔNG phải trạng thái hiện tại — và job đã bị thay thế vẫn ghi đè được artifact.** Một job cũ báo "đã dựng 9 strip, còn 2 vết cắt" đến SAU khi bản hội tụ đã được promote; tin theo nó sẽ làm lại việc đã xong. Cách phân xử duy nhất là ĐO, không suy từ thứ tự thông báo: (a) sha256 của blob ảnh NHÚNG TRONG deck — đọc thẳng từ zip `ppt/media/*.png`, loại logo trường bằng sha prefix — so với sha strip trên đĩa; (b) mtime timeline của strip, deck, và các script để biết ai ghi sau cùng. Trong ca thật, job cũ đã ghi đè 8 strip, nhưng rebuild hội tụ và promote chạy sau nên artifact cuối vẫn đúng; chỉ một strip bị đổi thật và đã được dựng lại. Phòng ngừa tận gốc: **script đo/dựng lại ảnh phải ghi ra đường dẫn TẠM rồi mới promote** — job cũ ghi thẳng vào `final/` nên mới có khả năng xoá bản hội tụ. Giữ một script trạng thái CHỈ ĐỌC (đo sha + size + vết cắt + timeline, in verdict) làm cổng regression cho đúng lớp bug này, theo nguyên tắc test-nơi-đã-tìm-thấy-bug.
- **So skill local với bản repo phải trừ phần sanitize trước khi kết luận lệch.** Repo công khai đã ẩn danh (`$HOME`, `chủ dự án`) nên md5 thô luôn lệch dù nội dung giống hệt; một lần so thô suýt mở PR thừa. Cách đúng: nạp bảng `REPLACEMENTS` thật từ script sanitizer (không chép lại bảng, vì bảng đổi thì phép kiểm âm thầm sai), áp lên bản local TRONG BỘ NHỚ, rồi so md5 từng file với bản repo. Khớp hết nghĩa là đã đồng bộ; còn lệch thì in đúng số dòng khác.

- **Mọi token làm mốc trong cổng dựng trên OCR phải ASCII-safe; chữ có dấu chỉ được kiểm bằng pixel.** Đã dính **4 lần** cùng một bẫy: OCR thay dấu bằng chữ số hoặc chữ cái gần giống — đo được trong log thật: `Tuổi:` → `Tu6i:` và `TuOi:`, `Nhập:` → `Nhap:`, `Xin chào` → `Xin chao`. Hệ quả: cổng báo FAIL oan (điều kiện "output phải xuất hiện ở band sau" không bao giờ thoả) dù ảnh **đã đúng**, và lỗi thật bị che. Luật: token mốc phải là số/giá trị ASCII (`'16'`, `'45'`, `'2010'`) hoặc chuỗi đã gập dấu; còn dấu thì đo bằng IoU pixel có-dấu-vs-gập-dấu. Khi so theo band phải so sau `fold`+`squash` vì OCR còn tách từ (`Nam sinh: ((`).
- **Cổng "smoke test" in ra rỗng là FAIL-OPEN, nguy hiểm hơn không có cổng.** Bản kiểm dấu bằng OCR từng in `diacritic_missing=[]` — trông như ĐẠT — trong khi chính nguồn dữ liệu của nó không đọc được token có dấu, tức cổng **không chứng minh được gì ở cả hai chiều**. Đã suýt promote artifact dựa trên cổng đó. Luật: cổng nào cũng phải có **đối chứng dương VÀ âm** chạy trước khi tin verdict xanh (ảnh PIL chuẩn: hỏi bản có dấu phải ra `DIACRITIC_RENDERED`, hỏi bản gập dấu phải KHÔNG ra), và phải **mutation-test** bằng chính hình dạng defect cũ. `echo_verdict` đạt 7/7 ca với 5 ca phải ĐỎ đều đỏ — đó mới là bằng chứng cổng sống.
- **Ảnh dạy học phải hiện đúng lệnh học sinh được dạy, không hiện công cụ nội bộ của pipeline.** Đã chụp ảnh có dòng `./py -u b18_vn_nhap_in.py` — `./py` là wrapper riêng để rút ngắn dòng lệnh, học sinh không bao giờ gõ nó và Bài 18 dạy `python3 <file>`. Cách đúng: `cd` vào thư mục script rồi dùng `python3 -u <tên file>` (28 kí tự, vẫn ngắn hơn nhiều so với 104 kí tự của đường dẫn tuyệt đối — lý do gốc từng làm strip phình 9950px). Lưu ý **không thay python venv bằng symlink**: `ln -s <venv>/bin/python3 ~/.local/bin/p3` rồi `p3 -c "import pptx"` ra `ModuleNotFoundError`, vì CPython resolve symlink về binary thật rồi tìm `pyvenv.cfg` **kế bên binary đó**, không thấy nên không nạp site-packages; muốn dùng tên ngắn phải là **wrapper exec đúng đường dẫn tuyệt đối**.
- **`input()` chụp bằng pipe stdin là DẠY SAI chính khái niệm đang dạy.** `printf 'An\n2010\n' | python3 script.py` làm stdin thành **pipe, không phải tty**, nên line discipline không có gì để echo; cộng thêm `stty -echo` thì màn hình hiện `Nhập tên: Xin chào, An` — lời nhắc dính liền kết quả, học sinh không biết dữ liệu từ đâu ra và dễ tưởng `input()` nhận cả cụm đó (reviewer vai học sinh tìm ra; đo lại và xác nhận là lỗi thật). Cách sửa: **gõ dữ liệu thật vào tty** bằng xdotool/xclip, và bật lại `stty echo` **SAU KHI đã gõ xong các dòng lệnh** (gõ lúc echo còn tắt thì chính dòng `stty echo` không hiện ra). Thứ tự ngược sẽ echo dòng lệnh dài và làm strip phình trở lại.
- **Band hàng phải đo bằng MỰC và nhóm theo (CỘT, band), không dùng giả định "một dòng OCR = một dòng màn hình".** OCR tự tách một dòng vật lý thành nhiều dòng (`Nhập: 45` → `Nhap:` + `45`) nên mọi cổng dựng trên giả định đó FAIL oan. Và strip do recrop dựng là **N cột ghép ngang**: hai dòng terminal khác nhau ở hai cột có thể nằm cùng một khoảng y (đo thật trên strip 2084×496: `input('Nhap:` ở x 292–1153 cột 0, `./py` ở x 2149–2422 cột 1) — nhóm chỉ theo y sẽ trộn chữ hai cột và thấy lời nhắc dính output. OCR chỉ còn vai trò **định vị** band.

Đo "chữ có tràn không" thì đừng so chữ với cái hộp: `spAutoFit` làm khung tự co theo chữ nên mực luôn chạm đáy khung, và `wrap=none` thì tràn khỏi hộp là bình thường. Đo mực trong đúng vùng chữ rồi so với mốc NHÌN THẤY ĐƯỢC (logo, mép slide) — xem `references/qa-and-release.md`.

Khi sửa cỡ chữ, cắt chữ thừa, build handout hoặc viết cổng kiểm: đọc `references/slide-qa-hard-lessons.md` (13 luật cứng có số đo — vd thủ phạm tràn hộp thường là `space_after` chứ không phải câu dài; ảnh có `left` ≥ chiều rộng slide thì không bao giờ hiển thị nên đo là báo oan).

Trước khi kết luận một lỗi trình bày là có thật hay không: đọc `pPr` XML chứ đừng đọc `paragraph.text` (bullet tự sinh không nằm trong text), và dựng bản đối chứng cùng geometry để tách lỗi renderer khỏi lỗi deck — xem `references/qa-and-release.md`.

Xem `references/knowledge-example-visual-repair.md` để áp dụng các ca sửa và cổng kiểm tra từ BAI_02/03.

- **Đạt cổng kỹ thuật KHÔNG có nghĩa là có nội dung dạy được.** Cổng thiết kế và cổng kỹ thuật đo được hình thức và cấu trúc; chúng không đo được kiến thức thật, năng lực số thật, hay dữ liệu thực hành thật. Một deck Module 2 có thể đạt 60+ điểm thiết kế mà giáo viên vẫn chấm "âm điểm" vì "nội dung chả có gì đáng học, đứng nói thôi cũng chả có gì để nói, thực hành cũng chả có gì để thực hành". Trước khi dựng, phải đối chiếu với PPCT thật (`drive_clb/01_PPCT/PL_II_*.docx`) để biết deck phải nêu những mã năng lực, minh chứng, công cụ cụ thể, địa điểm và điều kiện thực hiện nào — không suy từ tên bài. Mỗi bài dạy phải có **một bộ tệp dữ liệu thật** để học trò mở được ngay trên máy, không phải "mô tả bằng lời". Quy trình nằm ngay trong file này: mục *Bộ dữ liệu thực hành phải tạo sẵn, đặt tên đúng chuẩn* (dữ liệu thật), *Ảnh chụp màn hình cho slide: 5 luật đã trả giá* và *Chú thích trên ảnh chụp: 4 luật đã trả giá* (ảnh thao tác thật).

- **Tra cứu sự kiện/kiến thức trước khi viết, không dùng ký ức model.** Khi bài dạy cần nhắc một sự kiện, khái niệm, hay thông số kỹ thuật (ví dụ: quy tắc 3-2-1 backup, sự cố GitLab 2017, dung lượng Google Drive miễn phí), **chạy `web_search` với nguồn uy tín trước khi viết slide**. Đã gặp: model ghi "Google Drive miễn phí 5GB" trong khi Google chính thức ghi "up to 15 GB shared across Drive, Gmail, Photos" từ 2013 — thầy đọc đến đó sẽ dừng slide, mất uy tín. Quy tắc: với mỗi phát biểu có con số/tên sự kiện/quy tắc, phải có URL nguồn công khai trong ghi chú giáo viên; không có URL = không viết.

- **"Nội dung rỗng" là phản hồi sư phạm nặng hơn "cổng trượt" — deck đạt cổng vẫn bị chấm 3/10.** Chủ dự án dùng cụm "nội dung chả có gì đáng học, đứng nói thôi cũng chả có gì để nói, thực hành cũng chả có gì để thực hành" cho một chuỗi deck Module 2 dù cổng thiết kế đã được nâng cấp. Bằng chứng đo được: deck 13-14 cũ trên Drive 0/19 slide vượt ngưỡng 60 từ, nặng nhất 46 từ — tức cổng N4.2 thấy nó "đạt" mà giáo viên thấy "rỗng". Hai phép đo mâu thuẫn vì cổng chỉ đếm hình thức; cổng không đo được "học trò mở miệng hỏi được gì sau 5 phút đọc slide". Trước khi báo "đạt cổng", phải tự đặt câu hỏi: slide này có gì để giáo viên đứng nói, có gì để học trò thực hành, có gì để thầy hỏi lớp? Nếu trả lời ba câu đều "không có gì" thì deck rỗng dù cổng xanh. Đã ghi vào memory: `CỔNG ≠ NỘI DUNG`.

- **Cổng N4.2 (≤60 từ/slide) đếm `len(txt.split())` trên text NỐI MỌI SHAPE, không trừ chân trang và không phân biệt shape.** Đã kiểm chứng: cổng đếm tổng tất cả text frame trong một slide (header + kicker + nội dung + chân trang), nên mỗi slide có sàn thực tế khoảng 41 từ (60 − 19 từ footer) chứ không phải 60. Cổng cũng đếm tổng chứ không đếm riêng từng shape — một shape 16 từ + 11 từ + 9 từ + 4 từ + 9 từ + 3 từ cộng lại thành 52 từ/slide là FAIL. Khi vi phạm, cách sửa DUY NHẤT là tách nội dung thành nhiều slide (mỗi slide chỉ chứa 1-2 dòng trọng tâm), KHÔNG cắt bớt kiến thức vì như vậy chính là tạo ra "deck rỗng" mà chủ dự án cảnh báo ở pitfall trên. Nếu một slide bảng 7-9 dòng bắt buộc phải dài, hãy tách thành 2-3 slide cùng chủ đề, mỗi slide mang 2-3 dòng và kèm ảnh/bảng minh hoạ.

- **Tên công cụ phải nêu, không được viết chung chung.** Cổng C3.3 rubric ghi rõ: "nếu chỉ nói phần mềm/công cụ/ứng dụng chung chung thì cho 0". Đã đo: deck Module 2 dạy "lưu trữ đám mây" nhắc "đám mây" 9 lần nhưng **Google Drive 0 lần, OneDrive 0, Dropbox 0, iCloud 0, Mega 0** — học trò ngồi trước máy không biết mở cái gì. Khi dựng bài có dạy công cụ, phải grep trong bản thảo xem tên công cụ đã xuất hiện chưa (`grep -ci 'google drive\|onedrive\|dropbox\|icloud\|mega\|google lens\|camscanner\|microsoft lens\|tesseract' deck_text_dump.txt`) — nếu 0 thì phải thêm tên cụ thể kèm URL/điều kiện dùng (tài khoản trường hay cá nhân, có cần cài app hay không).

- **Bộ dữ liệu thực hành phải tạo sẵn, đặt tên đúng chuẩn để dùng làm ví dụ xuyên suốt.** Khi bài dạy cần học trò thực hành đổi tên tệp, dựng cây thư mục, hay phân quyền, phải có sẵn **một bộ tệp mẫu thật** với tên tệ (viết hoa không nhất quán, có dấu cách, có ngày tháng, có `(final)`, có `untitled.csv`...) để dùng làm đầu vào bài thực hành. Tạo bằng `touch` với tên có chủ đích rồi đóng gói `.zip` (`bo_tep_ten_te.zip`); dùng xuyên suốt nhiều slide để học trò quen mặt dữ liệu. Không để học trò tự nghĩ ra — mỗi nhóm sẽ nghĩ một kiểu, không so sánh được.

- **Cây thư mục mẫu phải upload lên Drive thật để có link chia sẻ thật, không phải link giả.** Dùng `rclone copy` đẩy lên thư mục Drive công khai của CLB (`00_THPT_THUAN_HOA/12_CLB_NLS_AI/...`), sau đó lấy link bằng `rclone link <remote_path>` (trả về `https://drive.google.com/open?id=...`). Khi mở bằng trình duyệt mà không cần đăng nhập thì link đó dùng được trong slide. **Kiểm tra link thật** bằng `goto_url(link)` rồi đọc `document.body.innerText` — nếu chỉ thấy "Đăng nhập" mà không thấy danh sách tệp, link đó không dùng được cho slide chiếu (học trò ở nhà mở cũng phải đăng nhập). Chỉ giữ link đã xác minh.

- **Chụp ảnh thao tác thật trên GUI local bằng Xvfb + dbus-run-session, không dùng mockup.** Khi cần ảnh chụp cửa sổ thật (Nautilus, xterm, giao diện app) để chứng minh thao tác:
  1. Chạy app qua `xvfb-run -a --server-args="-screen 0 1920x1080x24"` kèm `dbus-run-session bash -c '...'`.
  2. App GTK cần dbus session (`dbus-run-session`), nếu không sẽ crash hoặc treo khi load `xfconf`/`gvfs`.
  3. Dùng `import -window root` (X11 ImageMagick) chụp TOÀN BỘ root, rồi PIL crop theo bounding box đo được — `import -window <wid>` FAIL trên Xvfb vì MIT-SHM.
  4. Verify bằng **vision đọc lại nội dung** ảnh (đọc nguyên văn một dòng ta biết trước từ bản thảo) — nếu vision nói "ảnh trắng" hoặc "không đọc được" thì ảnh đó không dùng được, kể cả script báo thành công.
  5. Trên Xvfb không có window manager, app GTK vẫn chạy nhưng cửa sổ ở góc trên-trái. Đây là đặc trưng của Xvfb headless, không phải lỗi.

- **File rỗng (`touch empty.txt`) KHÔNG được coi là "tệp thật" cho slide trình bày.** Nếu cần tệp thật để mở bằng app (CSV có dữ liệu, txt có nội dung), phải `printf` nội dung có chủ đích rồi verify `wc -c` > 0. Slide chụp danh sách tệp trống → học trò sẽ thấy ngay là "dựng cho có", mất uy tín. Đã mắc: tạo 10 tệp tên tệ nhưng 8/10 rỗng; phải đổ nội dung tối thiểu vào 2-3 tệp tiêu biểu (`untitled.csv` có header + 2 dòng, `ban nhot.txt` có 1 dòng nhắc) để slide nói "có 8 tệp trống + 2 tệp có nội dung" khớp với thực tế.

## Quy trình

0. **Khảo sát TÀI SẢN và LUẬT CỔNG trước khi dựng lại từ đầu.** Khi anh yêu cầu dựng lại toàn bộ (không vá), trước khi viết bất kỳ dòng script nào, chạy 4 lệnh:
   - `find … -iname '*.pptx' -not -path '*clb*'` — tìm bộ slide chính khoá buổi sáng hoặc bộ "ảnh thật" anh muốn tận dụng; **đo cổng thiết kế trên đó trước khi quyết định "tận dụng"** — bộ đó có thể chấm 40.2/100, thấp hơn deck CLB 60.6/100 hiện tại, copy là đi lùi. Đã gặp: bộ chính khoá Tin học 10 (`bai_*_anhthat/`) chấm 40.2/100, chỉ lấy kỹ thuật ảnh thao tác, không lấy layout hay màu.
   - `grep -nE '^N[1-7]\.' build/design_gate.py` và `grep -nE '^C[1-5]\.' build/content_gate.py` — đọc TOÀN BỘ cơ chế đo, đặc biệt: N1.1 (≤5 cỡ, loại cỡ 36+ khi làm thang), N2.5 (dải màu nhấn phủ ≥25%, có sắc, độ sáng <0.85, không nền tối), N3.4 (AA 4.5:1, đo luminance), N6.1 (tiêu đề nhất quán ≤0.05in — KHÔNG loại slide bìa/divider), C1.1 (bản đồ Module), C1.2 (≥3 chặng), C4.1 (≥6 bài thực hành), C4.3 (sản phẩm cần đạt).
   - `python3 -c "from design_tokens import TYPE_SCALE, COLOR_ROLES; …"` — liệt kê tất cả khoá token trước khi dựng, vì `helpers_clb.rect()` cần `RGBColor` chứ không nhận string hex; phải `hex_to_rgb()` từng cái.
   - `find $HOME/slide_sources/qa_tools -name '*.py'` — biết vị trí `icon_raster.py` mà `helpers_clb` import từ đường dẫn tuyệt đối (không có thì `import` sẽ vỡ âm thầm).

   Đã mắc: bắt tay dựng mà chưa đọc N6.1, đặt tiêu đề bìa ở y=2.01, cổng quy cùng nhóm với tiêu đề 0.271in → lệch 1.76in. Đọc cổng TRƯỚC khi viết script là 2 phút; sửa sau khi dựng xong là 20 phút.

1. **Khóa nguồn và ba lớp định danh**: xác định đúng thư mục, tên file và bản hiện hành; ghi fingerprint gồm đường dẫn, SHA-256, số slide, kích thước, tiêu đề bìa và vài chuỗi đại diện. Không dùng file gần tên hoặc bản trung gian. Tách rõ: (a) số bài/tên phát hành theo PPCT mới, (b) mục và số KHBD làm nguồn nội dung, (c) mã sản phẩm học sinh do KHBD quy định. Không tự đổi mã sản phẩm chỉ vì số bài phát hành đã đổi. Khi deck cũ mâu thuẫn với PPCT/KHBD hiện hành, PPCT/KHBD là nguồn quyết định; lập bảng ánh xạ `deck cũ → bài phát hành → KHBD → mã sản phẩm` trước khi dựng.
2. **Lập bản đồ bài học và ma trận truy vết**: đọc KHBD/PPCT/YCCĐ; khóa riêng các số liệu, mã nhóm, tên sản phẩm và ca kiểm tra bắt buộc. Trước khi dựng từ một deck trước đó, phải quét toàn bộ script/notes/slide text để phát hiện số liệu, tiêu đề, ví dụ, mã sản phẩm và tên bài cũ; không chỉ đổi `H.MUC`, `H.HEADER` và tên file. Chạy một `forbidden scan` theo bài nguồn (cả chữ có dấu/không dấu) trước và sau khi dựng, rồi kiểm tra verbatim các slide ghi vở và slide mở đầu. Với từng yêu cầu, chỉ rõ slide trình bày, minh chứng trực quan, nơi luyện tập/đánh giá và chuỗi cần quét khi QA. Không kế thừa số liệu, mã định danh hoặc nhiệm vụ của bài nguồn sau khi đã đổi ánh xạ. Nếu KHBD ghi sai số liệu (ví dụ B20 ghi 26 kí tự/4 dấu cách trong khi Python đo 25/5), phải chạy smoke test bằng Python thật, lấy số máy làm chuẩn cho deck trên mọi slide/bảng/bằng chứng, ghi chú sai lệch trong header script và báo lại giáo viên — không dạy số sai chỉ vì KHBD in sai.

   **Checklist chống lẫn khi clone từ deck trước (bắt buộc):** `H.MUC`/`H.HEADER`, `SRC`/`OUTDIR`/`OUT` (mỗi bài một thư mục rebuild riêng), `core_properties` (title/subject/comments/tuần-tiết), `PROG`, toàn bộ `CODE_SERIES` (label/lines/output/steps), `items` (heading/kicker/kind), cover (`BÀI · MỤC`, tiêu đề lớn, 3 bullet, `codebox` label/output), các nhánh `elif kind ==` (`toc`/`requirements`/`actual`/`naming`/`pitfall`/`application`/`ghivo*`/`summary`/`closing`/`sec*`), và `notes` dict. Sau khi dựng, quét cấm phải 0 hit với mọi token của bài nguồn (số liệu, mã `Bxx`, từ khóa) và đủ hit với token bài mới; nếu còn sót thì sửa script và dựng lại trước khi phát hành.
3. **Kế thừa template**: chỉ giữ nền, header/footer, logo, bảng màu, kiểu chữ và mô-típ nhận diện khi người dùng yêu cầu làm lại toàn bộ. Nếu deck cũ có mạch tốt nhưng lệch nhiệm vụ KHBD, không vá rải rác: giữ nhận diện và các layout hữu ích rồi dựng lại phần thân.
4. **Dựng nội dung**: tuân thủ thứ tự `Bìa → Mục tiêu → Yêu cầu cần đạt → Mục lục`; mỗi slide thân bài có một ý chính và một yếu tố trực quan có chức năng.
5. **Viết học thuật–sư phạm**: dùng câu ngắn, chính xác, tự nhiên; bỏ khẩu hiệu, nhãn sản xuất và cụm đánh giá thừa. Chỉ dùng tiêu đề `Ví dụ`; không gắn nhãn `Ví dụ STEM/Thực tế/Toán học`.
6. **Thiết kế ví dụ**: ưu tiên tình huống ngoài SGK có liên hệ trực tiếp với bài; có thể dùng AI/LLM, IoT, dữ liệu cảm biến, toán hoặc vật lí ở mức vừa đủ. Đặt con số, đơn vị, mũi tên và quy tắc quyết định cạnh đối tượng minh họa.
7. **Slide CHỈ truyền tải nội dung — KHÔNG có slide bài tập** (chủ dự án chốt): mục tiêu ban đầu của bộ slide là truyền tải kiến thức, kế hoạch bài tập làm thành tài liệu riêng sau. Không tạo slide `Bài tập cuối bài`, `Luyện tập`, `Vận dụng`, `Bài tập vận dụng`, `Luyện tập theo trạm`, phiếu 3–2–1 hay rubric chấm điểm. Nội dung KHBD thuộc phần luyện tập/vận dụng vẫn được dùng, nhưng chuyển thành slide nội dung: `Ví dụ · <tình huống>`, `Lỗi thường gặp khi ...`, `Phân biệt A và B`, `Mở rộng ...`. Giữ `Nội dung ghi vở` tại điểm chốt và `Tóm tắt nội dung chính` ở cuối. Không dùng slide chốt bằng chứng sản phẩm hay kiểm tra nhiệm vụ làm kết bài.

   QA phải chặn: quét tiêu đề slide theo danh sách cấm ở trên, mục tiêu `con_bai_tap = []`. Hai âm giả hay gặp — checker quét cả speaker notes, và cụm `vận dụng` xuất hiện như động từ trong tiêu đề phần (`Phần 04 · Mở rộng và vận dụng`) hoặc trong notes. Xác minh bằng `pdftotext` + xem đúng text của slide trước khi kết luận; nếu chỉ là động từ thì vẫn nên đổi từ (`Mở rộng thang xếp loại`) để tín hiệu checker sạch.

   Deck đã phát hành trước khi có quy định này còn 2–6 slide bài tập; khi retrofit, thay bằng slide nội dung tương ứng chứ không xoá trắng làm hụt số slide.
8. **Ghi chú giáo viên**: viết ghi chú không rỗng cho mọi slide nội dung; đưa diễn giải, chuyển ý, thời lượng và lưu ý sư phạm vào notes thay vì làm dày bề mặt slide.
9. **QA và sửa theo hai tầng**: trước hết kiểm tra cấu trúc, text, notes, bounds, placeholder, dấu tiếng Việt và các chuỗi bắt buộc/cấm; sau đó xuất PDF 16:9 để rà contact sheet. Xem cảnh báo từ contact sheet là giả thuyết, không phải kết luận: xác minh thuật ngữ bằng văn bản trích xuất rồi render riêng slide nghi ngờ ở độ phân giải đầy đủ. Quét cả slide lẫn notes để tìm số bài, mã nhóm, số liệu và thuật ngữ cũ; dùng ranh giới từ/số để tránh khớp giả. Bộ dò thứ tự mở đầu phải tìm heading trong toàn slide hoặc vùng tiêu đề, không lấy phần tử text đầu tiên vì header trường thường đứng trước. Với bài lập trình, chạy smoke test các đoạn mã/kết quả trọng yếu khi có thể; required-string scan chỉ chứng minh nội dung hiện diện, không chứng minh mã chạy đúng. Kiểm tra riêng ký hiệu dễ lỗi glyph, số trang hai chữ số và cụm nghĩa bị ngắt dòng. Bắt buộc có ít nhất một vòng sửa–dựng lại–kiểm tra lại; không phát hành chỉ dựa trên contact sheet thu nhỏ.

   **Cổng veracity-protestation (bắt buộc mọi deck):** chạy `python3 ~/.hermes/skills/academic-prose/scripts/veracity_protestation_scan.py <deck.pptx>` — bắt mọi câu chữ tự chứng thực ("THAO TÁC THẬT", "ảnh chụp thật", "không phải ảnh vẽ", "đo được, không ước lượng", "not simulated"). Nguyên tắc: bằng chứng tự trình bày; nếu tính xác thực quan trọng thì thay tính từ bằng pointer kiểm tra được (đường dẫn remote, link chia sẻ, lệnh, ngày đo). Hit là ứng viên: đọc lại câu, xoá phần protest hoặc thay pointer; sentence contrast có chủ đích (dữ liệu thật vs tổng hợp) được license tự động. Chi tiết: `~/.hermes/skills/academic-prose/references/veracity-protestation-gate.md`. Ca gốc sinh ra cổng: slide rclone/Drive demo tiết 13–14, 5/5 câu text là protestation (2026-10-12).
   **Khi vision API không dùng được (503 / hết account):** không bỏ gate trực quan và cũng không lặp lại lời gọi thất bại quá một lần. Thay bằng ba checker đo thật trên bản render:
   - `ink_clip_check.py <pptx> <pdf> <out.json>` tại `$HOME/slide_sources/qa_tools/`: lấy toạ độ từ thật bằng `pdftotext -bbox-layout`, đối chiếu với hình chữ nhật có tô màu trong PPTX để phát hiện chữ bị cắt qua mép thẻ. Đây là bằng chứng mạnh nhất thay cho mắt người.
   - Kiểm tra chồng lấn thẻ (shape có tô màu giao nhau vượt ngưỡng) và độ phủ glyph tiếng Việt của font thực đang dùng.
   - Quét chuỗi bắt buộc trên **văn bản PDF** (không chỉ XML của PPTX) để chắc nội dung thật sự được render.

   **Bắt buộc so baseline:** chạy đúng checker đó lên một deck đã duyệt trực quan đạt (ví dụ bài liền trước) rồi chỉ xử lý phần chênh lệch. Không có baseline thì checker dựa trên font metrics sẽ báo hàng trăm âm giả, vì Aptos thường không có trên máy Linux và LibreOffice thay bằng Noto Sans — kiểm tra bằng `fc-list | grep -i aptos` trước khi tin kết quả đo bề rộng chữ. Lỗi thật thường là lệch toạ độ do em tính sai (bảng `n` dòng cao `n × row_h` nhưng chú thích đặt chồng lên hàng cuối), không phải chênh vài `pt` ở descender chữ có dấu.

   Các phép đo dự phòng chỉ là QA kỹ thuật một phần, không thay thế duyệt hình. Nếu công cụ thị giác chỉ tóm tắt bài, OCR hoặc hỏi muốn làm gì tiếp, đó không phải kết quả kiểm bố cục. Yêu cầu kiểm lại với số slide và vùng cụ thể, hoặc xem render trực tiếp; ghi trạng thái `chưa xác minh trực quan` nếu vẫn thiếu bằng chứng. Khi giáo viên yêu cầu “làm xong toàn bộ rồi gửi”, không chuyển phần kiểm tra còn thiếu sang giáo viên và gọi bản đó hoàn tất. Có thể giao bản nháp khi được yêu cầu, nhưng phải ghi rõ giới hạn; không phát hành Drive khi cổng hình còn treo.
10. **Phát hành và dọn kho**: tên tệp chính thức bắt buộc theo mẫu `BAI_<số 2 chữ số>_<TÊN_BÀI>.pptx` và `.pdf` (ví dụ `BAI_14_LENH_VAO_RA.pptx`), dùng số bài phát hành mới chứ không dùng số `SLIDE_` của nguồn cũ. Trước khi đổi tên/thay thế/xóa, snapshot toàn bộ tệp hiện hành vào `_ARCHIVE/<timestamp>` và kiểm tra số lượng + MD5/SHA-256. Sau đó phát hành cặp PPTX/PDF, tải ngược từ Drive và đối chiếu SHA-256. Khi người dùng yêu cầu dọn bản cũ, phải liệt kê đầy đủ tệp cũ, xác minh bản thay thế tồn tại và archive khớp checksum, rồi mới xóa; kiểm tra hậu kỳ `old_remaining=[]`, `replacement_missing=[]`, và đúng 2 tệp mỗi bài. Không để sót tên `SLIDE_...` trong thư mục chính. Chỉ cập nhật tiến độ khi checksum trùng.

## Quy tắc thiết kế

- **Nền sáng tuyệt đối, không dùng hộp nền tối.** Hộp mã nguồn phải nền trắng (`#FCFDFF`) + chữ đậm màu mực, nhận diện bằng thanh nhãn màu ở đầu hộp; dải đầu ra dùng nền xanh nhạt. Bìa không dùng khối navy đặc phủ nửa slide. Hàng tiêu đề bảng dùng xanh rất nhạt + chữ navy, không dùng nền đậm chữ trắng. Kiểm bằng checker: đo `luminance` mọi shape có tô màu, chặn khi `lum < 0.5` và `area ≥ 1.2 in²`; mục tiêu `so_nen_toi_that = 0`.
- **Icon thật thay ký tự/số trong vòng tròn.** Dùng kho `ppt-master/templates/icons/` (12.027 SVG, 5 thư viện). Pipeline: chọn 1 thư viện chính (ví dụ `tabler-filled`) → rasterize SVG sang PNG bằng `cairosvg` → `add_picture`. **Bẫy 1:** SVG dùng `fill="currentColor"`, phải thay bằng mã màu thật trước khi render, nếu không PNG ra trắng trơn (0 pixel mực). **Bẫy 2:** `convert`/ImageMagick không render được (thiếu `rsvg-convert` delegate) — cài `cairosvg` qua pip. **Bẫy 3:** tên icon không portable giữa các thư viện, phải `rg --files` kiểm tra tên thật trước khi dùng; tra theo vật thể vẽ được (`bulb`, `keyboard`), không tra theo khái niệm (`idea`, `input`). Danh sách thiếu đã gặp (tabler-filled) — đợt 2026-09-13: `refresh.svg`, `ban.svg`, `cut.svg`, `text-size.svg`, `typography.svg`, tên trần `scissors` → thay bằng `exchange`, `forbid`, `file-scissors`, `clipboard-typography`; đợt 2026-09-14 (BAI_29–30): `user-check.svg` → `user`, `code.svg` → `file-code`/`code-circle`, `compare.svg` → `replace`/`exchange`, `shield-x.svg` → `shield-check` (đã kiểm chứng tồn tại bằng `rg --files`). Mẫu `circle-number-%d` ghép bằng f-string là âm giả khi quét thiếu — phải loại trừ pattern `%d`/tiền tố trước khi kết luận. Cách rẻ nhất để đổi cả deck: map `số/ký hiệu → tên icon` rồi để chính hàm `card()`/`note_slide()` tự tra map, không sửa từng chỗ gọi. Luôn chạy `verify_icon` trước khi dựng để chặn `FileNotFoundError` giữa chừng.
- Cẩn thận đặt tham số hàm tên `icon` khi đã có hàm toàn cục `icon()` — tham số sẽ che hàm và gây `TypeError` lúc dựng; đặt tên khác (`pic`) hoặc đổi tên hàm.
- Phân cấp xanh–cam theo template; thẻ bo góc, icon và sơ đồ native PowerPoint.
- Không dùng ảnh trang trí không mang thông tin; không để chữ tiếng Việt quan trọng đóng cứng trong ảnh nếu có thể dùng shape/text.
- Chữ quan trọng khi chiếu thường 18–22 pt trở lên; khoảng cách khối tối thiểu khoảng 0,3 inch; lề khoảng 0,5 inch.
- Không lặp một layout cho toàn bộ deck; thay đổi hợp lí giữa sơ đồ, tiến trình, bảng, so sánh, biểu đồ và ví dụ tính toán.
- **Bằng chứng mạnh nhất cho "chữ trong ảnh đủ to" là để vision đọc NGUYÊN VĂN một dòng ta biết trước.** Mọi phép tính pixel đều là gián tiếp; nếu model đọc đúng dòng ground-truth từ bản render ở kích thước sẽ chiếu, kết luận là trực tiếp. Ngược lại, nếu nó không đọc được thì mọi con số pt đều vô nghĩa.
- **Đo chiều cao mực bằng ngưỡng đã thất bại HAI lần — đừng thử lần ba.** Ngưỡng toàn cục (`<150`) đếm cả nền xám 203 và bóng đèn thành "mực" (báo 45,67% ink trong khi thật ~2%); ngưỡng thích ứng theo percentile lại chọn giá trị vô lý (205) và chỉ bắt cạnh mạnh nhất (báo dòng chữ cao 8px và 1px). Cách đúng: **dùng hình học đã biết** (`BODY_PX × scale × 72`) và kiểm chéo bằng MỘT phép đo tự xác nhận (trên ảnh sạch, đo ra 38/38/40px = đúng `BODY_PX`).
- **Khi giải kích thước ở HAI chỗ, công thức phải dùng cùng các số hạng.** Đã mắc: bước "suy ra chiều cao dải cắt tối đa" tính `(band - LABEL_IN)` nhưng bước kiểm tra dùng `(band - 2*PAD - LABEL_IN)` → bước trước chọn dải 200px, bước sau từ chối (0,83in > 0,77in). Tốt nhất là gọi chung một hàm.
- **Chiều cao nhãn phải tính từ metric chữ, không đoán.** Một dòng 12pt cao `12 × 1,2 = 14,4pt = 0,20in`; đặt `0,30in` là over-allocate 0,08in × 3 slide = mất một dòng chữ vô ích.
- **`grep` với `(` không escape trong BRE sẽ báo `Unmatched (` — dùng `grep -F` cho mẫu chữ nguyên văn.** Đã làm sai rồi hiểu nhầm kết quả thành "patch fail"; verify patch phải bằng `grep -F` hoặc đọc diff.
- **Đừng để hai file cùng khai báo một hình học.** Script vẽ ảnh và script chèn ảnh từng mỗi nơi một bộ `1650/2200/150/40`; đổi một chỗ thì chỗ kia âm thầm lệch và dải cắt sẽ cắt ngang giữa dòng chữ. Nâng thành hằng số cấp module + hàm `line_boxes()` dùng chung.
- **Đo dải trống TRƯỚC khi chọn nội dung để chèn.** Thứ tự ngược (chọn dải ảnh "nhiều chữ nhất" rồi mới đo chỗ trống) luôn dẫn tới chọn quá khổ rồi bị từ chối.
- **Báo rõ phạm vi đã thêm.** Chỉ một slide được ghi chú giáo viên yêu cầu ảnh đối lập, nhưng ảnh đã chèn vào ba slide; phải nói để người dùng cắt bớt nếu muốn, không lặng lẽ mở rộng.
- **Ảnh chèn vào slide phải được vẽ ở ĐÚNG kích thước sẽ đặt (scale = 1,00).** Vẽ figure 12,4 in rồi đặt xuống 2,2 in làm chữ 12pt còn 1,92pt — không đọc được khi chiếu, mà cổng QA vẫn PASS vì nó chỉ đo chữ thật trong pptx, không đo chữ nằm trong PNG. Chứng minh scale bằng phép đo `PNG_px / dpi == figsize_in`, và in ra số pt chữ sẽ hiện trên slide.
- **Đo dải trống thật của slide trước khi chèn ảnh.** Lấy đáy thấp nhất của các shape nội dung (bỏ qua header và footer) làm mép trên. Nếu dải trống quá thấp (1,26 in) thì ảnh vuông vẽ theo tỉ lệ thường sẽ bị thu tới mức không đọc được — khi đó vẽ ảnh **dạng dải ngang** (strip) đúng bằng chiều cao dải trống.
- **Chữ chú thích của ảnh phải là text box PowerPoint, không nằm trong ảnh.** Lý do: cổng QA đo được font/chồng đè/tràn lề của text thật, còn chữ trong PNG thì không cổng nào bắt được lỗi. Lấy style từ box có sẵn trong deck (đo `run.font.size`, `color.rgb`, và để font thừa hưởng theme `+mn-lt` thay vì đặt tên font cứng).
- **UNO bridge để dựng ảnh Calc thật đã fail 4 lần liên tiếp — đổi sang openpyxl + LibreOffice CLI, đừng thử UNO lần nữa.** Chuỗi fail: `from com.sun.star.sheet.FilterOperator import EQUAL` → ImportError (máy không có module constant trong sys.path) → `loadComponentFromURL` trả None → `createFilterField`/`AutoFilter` AttributeError → treo 400s. Cách CHẠY ĐƯỢC: dựng TRẠNG THÁI bảng tính bằng openpyxl (`ws.auto_filter.ref`, `ws.row_dimensions[i].hidden = True` để lọc thật, `PatternFill` để tô ô), rồi `soffice --headless --convert-to pdf`, rồi PyMuPDF `page.get_pixmap(matrix=..., clip=rect)` cắt đúng vùng. Kiểm chứng trạng thái bằng số dòng đếm độc lập từ CSV (ví dụ ô trống đúng ở dòng 13), không tin khai báo. **KHÔNG `pkill soffice` khi máy có `DISPLAY`** — có thể giết LibreOffice người dùng đang mở, đó là hành động không đảo ngược được; chỉ kill đúng PID có profile của chính mình.
- **Chấm "có ảnh thao tác thật" phải so sha256 blob + xem vị trí/kích thước, KHÔNG đếm PICTURE.** Đã gặp: 4 PICTURE đếm được đều là MỘT logo trường lặp lại (cùng sha `d112270c…`), và còn 15 shape nhét chính blob đó làm `blipFill` nền header nên đếm PICTURE còn thiếu. Ảnh nội dung thật = blob có sha DUY NHẤT, rộng ~9–10in, nằm ở thân slide (y > 4in), mỗi ảnh một sha khác nhau.
- **Sửa chuỗi trong ô bảng phải thay theo ĐOẠN hoặc gán thẳng run, vì chuỗi hay bị TÁCH qua 2 textbox/run.** Đã gặp slide 12 ô "Quyền truy cập": TextBox 26 = "…thứ không nên xem", TextBox 27 = "không"; slide 7: "Bắt lỗi: LỆCH ĐỊNH" + "DẠNG". `run.text.replace()` không bao giờ khớp khi chuỗi nằm vắt qua run. Cách đúng: ghép mọi run trong paragraph, thay, ghi lại run đầu rồi xoá run thừa — hoặc gán thẳng `runs[0].text = CHUỖI_MỚI`.
- **Sau mỗi replace, đọc ngược file và ĐẾM số lần chuỗi mới xuất hiện — một cặp replace có thể là NO-OP mà vẫn báo thành công.** Đã gặp: strip text về SENT rồi gọi `replace(SENT → SENT)` nên text thật vẫn còn đuôi cũ → kết quả mã NLS lặp 2 lần và câu đọc bị gãy. `success` của patch/save không chứng minh chuỗi đã đổi; chỉ số đếm sau khi đọc ngược mới chứng minh.
- **Khi đang đi GIẢM một dấu câu, đừng tự thêm dấu đó vào nội dung mới.** Vừa giảm 39 dấu hai chấm xuống 5 thì caption ảnh mới chèn lại mở đầu "Ảnh thật: …" = thêm ngược 4 dấu hai chấm mới. Chuỗi/caption viết mới phải qua CÙNG bộ lọc dấu câu đang áp cho deck.
- **Sửa mốc giờ thì bảng lộ trình phải TÍNH LẠI TỪ NOTES ĐÃ ÁP, không tính tay từ mốc cũ.** Bảng lộ trình từng map cứng theo tọa độ y + cộng mốc cũ → sau khi dời giờ slide 15/16, bảng cộng 86 phút còn notes chạy 90, hai dòng cuối lệch. Cách đúng: parse mốc `[phút a–b]` từ notes SAU khi sửa, cộng theo nhóm slide, ghi vào bảng, rồi `assert tổng == 90`.
- **Chọn font phải kiểm cmap glyph bằng fontTools, không tin danh sách font "hỗ trợ tiếng Việt".** Noto Sans đủ dấu tiếng Việt nhưng **thiếu U+2192 (→)** nên render ra ô vuông tofu, chỉ báo bằng UserWarning rất dễ bỏ qua. Đo 207 font trên máy có đủ glyph; Liberation Sans, DejaVu Sans, Arimo đều đạt.
- **Chặn tofu/tràn lề/chồng đè bằng cổng assert trước khi ghi file, không để UserWarning.** Ba cổng: `assert_no_tofu` (soi cmap), `audit_margins` (bbox ra ngoài canvas), `audit_overlaps` (giao bbox). Cổng phải `raise SystemExit` để không thể lọt qua.
- **`audit_overlaps` phải đo bbox CHỮ, bỏ mũi tên.** `Annotation.get_window_extent()` gộp cả mũi tên vào bbox nên báo đè ảo khi mũi tên đi qua chữ khác; gọi `Text.get_window_extent(txt, renderer)` thay thế. Badge số đính vào mép hộp chú thích là thiết kế có chủ đích, phải lọc khỏi danh sách lỗi.
- **`fig.text` không tự xuống dòng.** Dòng ghi nguồn dài sẽ tràn khỏi cạnh phải và bị cắt mà không cổng nào bắt được nếu chưa bật audit. Wrap bằng `textwrap` với số ký tự/inch **đo thật** (đo ra 11,18 ký tự/inch ở 10,5pt với chuỗi `x`, chữ tiếng Việt có dấu rộng hơn nên lấy 10,0) — không dùng giá trị đoán.
- **Nếu hai lần chỉnh geometry cho cùng một phần tử mà vẫn lỗi, đổi loại giải pháp.** Nhãn trục X rơi ra ngoài canvas vì dải ảnh chỉ cao 1,28 in: nâng `bottom` hai lần vẫn tràn. Cách đúng là bỏ `set_xlabel` treo dưới trục và đưa ý nghĩa trục vào **bên trong** vùng vẽ (góc trống của miền dữ liệu), vì nó không tốn chiều cao.
- **Trước khi tính chuyện chèn ảnh, kiểm tra deck đó có cần tài khoản ngoài không.** Trình duyệt headless không đăng nhập Google và vault không mở được ô nhập trong session Discord, nên ảnh chụp thao tác trên Drive/ChatGPT phải chờ người dùng tự lưu đăng nhập. OCR thì không cần sudo: `rapidocr-onnxruntime` cài thuần pip, đọc 14 dòng tiếng Việt trong 2,2 giây.
- **Ghi nguồn ảnh vào ghi chú giáo viên, không ghi vào trong ảnh.** Trong ảnh thường đã hết chỗ; ghi vào sẽ đè chữ khác. Ghi chú giáo viên là chữ thật nên QA đo được, và học sinh không nhìn thấy.
- **Nhận diện chân trang phải kèm điều kiện VÙNG, không chỉ chuỗi.** Regex `^\d+\s*/\s*\d+$` (để bắt số trang "12 / 18") bắt nhầm **dòng dữ liệu** trong bảng ở giữa slide (`0/5`, `3/5`, `4/5` = số lần chạy phép thử), kéo `footer_top` lên 1,91in và quy oan 16 dòng thân bài là "đè chân trang 3,22in" — trong khi đo thật: thân bài chỉ tới 5,13in, chân trang thật ở 7,06in, còn dư 1,93in. Bắt buộc: dòng chỉ được coi là chân trang nếu `y0 > page_h - 90pt`.
- **Khi hai phép đo mâu thuẫn, nghi ngờ CHECKER trước, đừng vội sửa deck.** Báo cáo "tràn 3,22in" từ render mâu thuẫn với rect lưu trong file (thân bài sâu nhất 5,36in). Về hình học, trang cao 7,50in nên một dòng chữ không thể nằm sâu hơn đáy trang 3,22in — mâu thuẫn đó tự nó là bằng chứng checker sai.
- **Trước khi kết luận "checker mù", hãy kiểm tra fixture có thật sự hỏng không.** Đã mắc BỐN lần, mỗi lần một kiểu: (1) python-pptx gắn `spAutoFit` cho MỌI textbox nên fixture "cố tình tràn" không hề tràn; (2) fixture chỉ xuống tới 6,66in trong khi chân trang ở 7,11in; (3) dựng fixture bằng `page.insert_image()` trên PDF có sẵn mà KHÔNG xoá ảnh gốc → file ra 5 rect thay vì 2, hai ảnh chồng nhau THẬT nên cổng báo chồng lấn là ĐÚNG, ta lại tưởng cổng oan; (4) `insert_image` mặc định GIỮ TỈ LỆ + CĂN GIỮA nên rect thật ≠ rect yêu cầu (đòi 700×160 ra 320×160 ở x 290–610), text "chồng lấn" đặt ở x=60 hoá ra nằm NGOÀI ảnh → cổng PASS đúng, fixture mới sai. Ba luật rút ra: **fixture tổng hợp dựng từ đầu** (mọi rect do ta đặt, tính trước bằng số được) thay vì mutate artifact thật; **assert hình dạng fixture sau khi dựng** (`assert count_rects == kỳ_vọng`, `assert abs(y1 - (y1_cũ+dy)) < 0.6`) vì fixture hỏng sẽ lọt qua y như lần trước; và khi cần ảnh lấp đúng rect phải传 `keep_proportion=False`, rồi **đo lại bằng `get_image_rects`** trước khi tin toạ độ.
- **Cổng hình học phải IMPORT ngưỡng từ chuẩn nhà, không tự đặt số.** Tự đặt `FOOTER_Y = page_h - 90 = 450pt` khiến caption thật ở 451–456pt bị phân loại nhầm THÀNH chân trang → 8/10 slide báo lỗi oan, và vì caption bị nuốt nên bộ dò caption trả `captions=0` (dấu hiệu tự khai báo lỗi: caption ta vừa chèn mà bộ dò không thấy). Đúng: `sys.path.insert(0,'$HOME/clb_nls/build'); from qa_deck import CONTENT_MAX` (6.86in = 493.92pt) và mốc chân trang lấy từ PDF thật của deck ĐÃ DUYỆT (đo ra y0=508.4pt).
- **Control test 2 chiều phải có cả ca "hợp lệ phải PASS", không chỉ ca "vi phạm phải FAIL".** Chỉ test chiều FAIL thì một cổng báo-lỗi-oan-hàng-loạt vẫn đạt control test. Bộ tối thiểu 4 ca: GOOD (PASS) · ảnh vượt CONTENT_MAX (FAIL) · chữ đè ảnh (FAIL) · caption vượt CONTENT_MAX (FAIL).
- **Cổng đọc rect trong file bị MÙ với phần text box tự nới.** Bộ deck có 13.946 textbox đều là `spAutoFit`: khi nâng cỡ chữ, PowerPoint/LibreOffice tự nới box nhưng **rect lưu trong file vẫn là rect cũ**. Nên cổng z-order và cổng "đè chân trang" dựa trên rect đều không thấy phần nới thêm. Muốn đo thật phải dùng **bản render PDF** (`page.get_text('dict')` → bbox từng dòng).
- **Cổng "fixed-box overflow" vô nghĩa trên bộ deck toàn `spAutoFit`.** Đo ra 0 box cố định / 13.946 box autofit → cổng đó không bao giờ có thể báo lỗi. Phải nói thẳng điều này thay vì trình "0 lỗi" như một bằng chứng.
- **Sửa regex/logic nhận diện xong phải chạy lại CONTROL TEST cả hai chiều.** Đổi logic có thể làm hỏng khả năng bắt lỗi thật mà không ai thấy.
- **Ngưỡng QA tự đặt phải hiệu chuẩn trên artifact đã duyệt TRƯỚC khi dùng làm cổng.** Nếu deck anh đã duyệt cũng "vi phạm" ngưỡng đó thì ngưỡng là máy đẻ âm giả — mang đi sửa là phá bộ đang ổn định để thoả một tiêu chuẩn không tồn tại. Đo bằng chứng: lệch hai cột tới 1.68in là bình thường khi cột trái là ảnh, thẻ thừa đáy 0.60in vẫn đạt chuẩn nhà.
- **Script phát hành phải trỏ vào báo cáo QA của ĐÚNG build nó phát hành.** Trỏ nhầm sang thư mục QA của build trung gian sẽ khiến cổng SKIP toàn bộ (may) hoặc phát hành nhầm build cũ (nguy hiểm). Chốt chặn: so `mtime` của file QA/PDF với file pptx, cũ hơn thì dừng (`freshness_guard`).
- **Luôn chạy `--dry` trước `--apply` khi phát hành hàng loạt.** Dry-run là thứ bắt được lỗi trỏ nhầm thư mục QA ở trên; nếu chạy thẳng `--apply` thì bản chưa nâng font đã lên Drive.
- **Không tin script tự báo thành công.** Xác minh bằng công cụ độc lập: `rclone check <local> <remote> --one-way` so hash phía server, 0 khác biệt mới gọi là đã phát hành.
- **`--differ`, `--missing-on-dst`, `--missing-on-src`, `--match`, `--error` BẮT BUỘC phải kèm đường dẫn file** (`--differ /tmp/differ.txt`); để cờ TRẦN làm rclone thoát rc=2 và in usage. Bẫy nguy hiểm: script đếm `differ=0 missing=0` từ stdout RỖNG của lệnh chưa hề chạy rồi suýt kết luận sai — phải đọc `wc -l` của CHÍNH tệp kết quả và in dòng `NOTICE: ... 0 differences found / N matching files` ở stderr làm bằng chứng. Luôn assert `check_rc == 0` trước khi đọc số đếm.
- **Lọc nhiễu rclone theo DÒNG, không theo chuỗi con.** Dòng `NOTICE: gdrive: This remote uses rclone's shared Google Drive client_id...` nằm ở stderr; gộp `stdout + stderr` rồi chỉ `replace('NOTICE:','')` sẽ để sót phần còn lại và bị đếm thành một file (báo cáo 37 trong khi Drive có 36). Giữ stdout riêng khi đếm danh sách.
- **`rclone lsf --format "spi"` phân tách bằng dấu `;`, không phải khoảng trắng.** Parse bằng `awk '{print $3}'` cho ra rác (báo "1 ID duy nhất" trên 36 file). Phải `awk -F';'`.
- **Quét placeholder `{TEN_VIET_HOA}` trên đúng build phát hành.** Token dạng này hiện ngay trên màn hình chiếu, học sinh thấy dấu ngoặc nhọn. Điền giá trị bằng bằng chứng trong chính deck (tên biến `DIEU_MOI_NHOM`, câu song song ở slide khác, ghi chú giáo viên) — không đoán; điền sai làm câu tự mâu thuẫn.
- **Đo cỡ chữ thật trong PDF bằng PyMuPDF, không đọc `run.font.size`.** Run không đặt size tường minh sẽ kế thừa từ paragraph/layout/master và bị bộ dò bỏ sót. `page.get_text('dict')` → `span['size']` là ground truth.
- **Tiến trình nền không kế thừa venv.** Script cần thư viện (PyMuPDF, python-pptx) phải gọi đường dẫn interpreter tuyệt đối `<venv-python>`; gọi `python3` trong `background=true` sẽ dùng `/usr/bin/python3` và fail âm thầm (exit 1 bị ghi vào file, không ai thấy).
- **Python đệm stdout khi ghi ra file**, nên log tiến độ không cập nhật dù tiến trình đang chạy. Đo tiến độ bằng trạng thái thật phía đích (đếm file trên remote), không đọc log.
- **Slide hai cột phải khóa đáy bằng giá trị đo được.** Vẽ cột dài trước, lấy đáy thật làm mốc, rồi cho phần tử cuối của cột kia kéo dài đúng đáy đó (`auto=False`). Hàm dự đoán chiều cao (`note_h`/`card_h`) phải nhận đúng cỡ chữ mà hàm vẽ sẽ dùng, nếu không chiều cao dự đoán lệch chiều cao thật và hai cột sẽ lệch nhau.
- **Bộ dò hình học phải tính cả chữ và ảnh, không chỉ shape có tô màu**, và không lọc `H < 0.45` vì dải nền hàng bảng thường cao 0.40–0.44in (lọc nhầm sinh báo lệch cột ảo). Phải loại header/footer (`T < 1.35` hoặc `T >= 6.95`), nền full-slide và đường kẻ mảnh. Với `table_block` chỉ hàng chẵn mới có nền tô nên đáy bảng thật nằm ở đường kẻ cuối, không phải ở shape tô màu cuối.
- Slide bìa, divider và slide hỏi đáp cố ý thưa chữ (gap đáy 0.9–1.2in) và cột phải là cụm trang trí; không áp tiêu chí cân bằng hai cột cho chúng.

## Đánh giá độc lập trước khi báo đạt hoặc phát hành (bắt buộc)

Chủ dự án: *"Nên tự có chuyên gia đánh giá độc lập theo các tiêu chí anh đã đưa ra."* Em vừa là người soạn vừa là người chấm thì điểm của em vô giá trị.

1. **Viết rubric thành văn bản, trích NGUYÊN VĂN lời giáo viên** cho từng tiêu chí, kèm thang điểm và câu hỏi phải trả lời bằng bằng chứng. File mẫu: `$HOME/clb_nls/review/rubric_anh_van.md` (4 nhóm A Kiến thức 30đ · B Năng lực số 30đ · C Thực hành 30đ · D Hình thức-ngôn ngữ 10đ).
2. **Dựng gói bằng chứng thô** để người chấm đọc bằng lệnh, không phải tin bản tóm tắt của em: `deck_text_dump.txt`, `notes_dump.txt`, dữ liệu thực hành, đáp án, `qa_all_output.txt`, `score_rubric.json`.
3. **Máy chỉ chấm phần nhị phân/định lượng** (`build/score_rubric.py`): có mã NLS, có tên công cụ, có mức hướng dẫn bạn, số bài thực hành, số dấu câu, số ảnh, ký tự mỗi slide. Máy KHÔNG chấm được kiến thức đúng hay sâu — giao người.
4. **Giao 3 subagent song song, mỗi người một nhóm tiêu chí, có `output_schema`** để kết quả so sánh được. KHÔNG cho họ biết em tự đánh giá thế nào, và ghi rõ họ được phép BÁC điểm máy.
5. **Cảnh báo điểm máy có thể sai theo hướng có lợi cho em.** Đã gặp: `score_rubric.py` đếm 4 `PICTURE` rồi báo `D1 có ảnh: ĐẠT`, nhưng cả 4 là CÙNG MỘT logo trường lặp ở header mỗi slide — không phải ảnh nội dung. Đếm shape không phân biệt được logo và ảnh giảng dạy; phải so `sha256(blob)` và xem ảnh nằm ở header hay ở thân slide trước khi chấm D1.
6. Chỉ báo "deck đạt" khi có điểm độc lập, và phải đăng nguyên văn lời chê nặng nhất thay vì chỉ lấy phần khen.
7. **Kiểm chứng cả lời của chuyên gia độc lập bằng lệnh — reviewer không thay thế đo lường.** Đã gặp: child nhóm C khẳng định "học trò sẽ nghẽn khi mở CSV trong Calc vì thiếu hướng dẫn mã hoá", nhưng đo ra tệp CÓ BOM UTF-8 + CRLF nên Calc tự nhận, không hỏi. Một claim khác của cùng child (slide 15 cần 16 phút trong khung 11 phút) thì đúng và chỉ ra lỗi thật do em gây ra: in đáp án lên slide thực hành, học trò sẽ chép số thay vì kiểm tra. Cùng một reviewer, nửa đúng nửa sai → phải đo từng claim.
8. **Child fail vì `output_schema` KHÔNG có nghĩa là child không làm việc.** Một child chạy 798 giây, đọc đủ 6 tệp bằng chứng, viết xong phân tích, rồi bị bác vì trả lời không khớp schema sau 1 lần retry. Nội dung vẫn nằm nguyên trong `live_transcripts` → đọc transcript để CỨU kết quả, không dispatch lại mù (tốn thêm 13 phút và có thể fail lại y hệt). Phòng bệnh: giữ `required` trong schema ở mức tối thiểu (chỉ những field mình thật sự sẽ đọc), để field tự do dạng string thay vì ép nested object nhiều tầng.
9. **Không sửa artifact khi chuyên gia đang chấm chính artifact đó.** Sửa giữa chừng làm kết quả đánh giá hết hiệu lực và phải chạy lại cả vòng. Ghi findings vào tệp, chờ đủ mọi bản nhận xét rồi sửa một lần, QA một lần.
10. **Cộng giờ kịch bản bằng lệnh trước khi tin mốc thời gian trong notes.** Mốc `[a–b]` cộng đủ 90 phút trên giấy vẫn có thể tràn, vì một hoạt động (4 em × 3 phút trong nhóm 4 người) cần 12–16 phút nhưng chỉ được cấp 11. Trích mọi cặp `[a–b]`, nhân số lượt × số phút mỗi lượt, so với khoảng được cấp; chỗ nào cần > cấp là lỗi phải sửa trước khi phát hành.

## Cổng giao bản sửa đầy đủ

Áp dụng cổng nội dung ở đầu skill và `references/knowledge-example-visual-repair.md`, không tạo thêm một bộ quy tắc trùng lặp.

- Khi giáo viên nói “làm xong toàn bộ rồi gửi”, hoàn thiện tất cả bài trong phạm vi đang sửa trước khi giao; không gửi bản dở rồi yêu cầu giáo viên phát hiện lại những lỗi đã biết.
- Lập danh sách lỗi theo slide và chỉ đóng từng lỗi sau khi đọc lại bản xuất cùng render liên quan. Bản đang bị giáo viên bác bỏ không được dùng làm baseline đã duyệt.
- Kết quả vision chỉ tóm tắt/OCR nội dung là **không trả lời yêu cầu QA**, dù công cụ báo thành công. Kiểm lại bằng câu hỏi bố cục cụ thể và ảnh đủ rõ; không chuyển trạng thái trực quan sang đạt chỉ dựa vào mã thành công.
- Nếu còn cổng chưa kiểm được, ghi đúng là bản chưa hoàn tất và nêu phần bị chặn; không dùng lời mời duyệt để thay thế công việc người dùng đã yêu cầu hoàn thiện. Giao bản xem trước chỉ khi người dùng muốn bản xem trước hoặc chấp nhận giới hạn đó.

## Tài liệu nạp theo nhu cầu

- `references/content-and-language.md`: chuẩn nội dung, ví dụ và ngôn ngữ.
- `references/qa-and-release.md`: cổng QA, quy ước tên và cập nhật Drive.
- `references/series-migration-and-release.md`: ánh xạ PPCT cũ–mới, khóa dấu vết bài cũ, QA typography và phát hành từng bài như một giao dịch.
- `references/programming-lesson-content-and-qa.md`: dùng cho bài lập trình; tách ba lớp định danh, kiểm thử mã/kết quả, xử lý số gần đúng, nối xâu, thông báo lỗi và âm giả khi dò tiêu đề.
- `references/deck-rebuild-script-pitfalls.md`: bẫy khi viết script dựng deck bằng python-pptx — tách helper và tham số hoá định danh, không hardcode số slide khi nhân bản, toạ độ trong vòng lặp, tên tham số che tên hàm, khung tự co để không cấn footer, và quy tắc compile lại sau mỗi lần patch script.
- `references/icon-embedding-and-measurement-qa.md`: nhúng icon vector thật vào PPTX (xác minh tên icon trước khi dựng, xử lý `fill="currentColor"` render ra trắng) và bộ cổng QA đo được — đo cắt chữ trên bản đã render, tách âm giả bằng baseline, ngưỡng dùng chung, và cách xử lý khi công cụ thị giác không phản hồi.
- `references/clone-contamination-guard.md`: checklist chống lẫn nội dung khi clone deck bài trước (Bài 22→23) — quét token cấm trước/sau dựng, mỗi bài một thư mục rebuild riêng, ghi vở là khái niệm, bug `note_slide` che hàm `icon()`.
- `references/2026-09-14-bai27-30-batch.md`: batch cuối §5.31–§6.34 — smoke 30 điểm / 7 từ / phiếu 4 ô, 4 icon thay thế đã verify, fix tràn O4 dòng dài.
- `references/2026-09-14-bai02-retrofit.md`: mẫu retrofit deck cũ → chuẩn BAI_14–30 (§1.2: 3 TB + 2 đối chứng, 28 slide) và khóa số liệu BAI_03 (§1.7: 12 tệp / 45 MB / 4 bước).
- `references/vision-and-capture-infrastructure.md`: hạ tầng dựng ảnh — Open WebUI tự chủ
  khi mọi trang AI công cộng chặn máy tự động hoá, và bảng chẩn đoán vision relay
  (`402`/`429`/`503` là chuyện account/quota, không phải model sai).
- `references/photo-insertion-into-live-deck.md`: chèn ảnh chạy thật vào deck ĐANG CÓ — đệ quy GROUP khi đo, viết lại `run.text` thay vì xoá shape, trừ lề footer và chỗ caption, trần 72% bề ngang, script không idempotent phải khôi phục backup, detector mới phải tự kiểm chứng (vụ 1083 báo động giả), và vision timeout thì kiểm hình học bằng lệnh.
- `references/corpus-wide-text-rewrite.md`: sửa chữ HÀNG LOẠT trên cả kho deck — tách luật ra module dùng chung (dry-run và bản ghi thật phải import cùng một file), số chuỗi khác nhau mới quyết định cách làm, thứ tự luật là quy tắc, bật `re.I` kèm giữ HOÁ, đếm biến thể trước khi viết regex, cổng phải so sai phân (2 detector hỏng trong một phiên: 525 và 1083 âm giả), và so bản local vs bản phát hành phải chuẩn hoá cả hai phía (bug dịch-một-ô báo "213 vị trí lệch" oan).
- Đồng thời đọc `powerpoint/references/classroom-lesson-deck-revision.md` và `powerpoint/references/python-pptx-classroom-deck-qa.md`.

## Cổng THIẾT KẾ riêng, và bảy lỗi detector đã trả giá

Cổng kỹ thuật (`qa_all.py`, `qa_deck.py`) KHÔNG bắt được lỗi thẩm mỹ. Deck
17–18 PASS 7/7 cổng kỹ thuật mà giáo viên vẫn chấm 3/10: "motif 1 màu,
template cũng 1 màu, chả có thiết kế trước gì cả". Muốn bắt lỗi đó phải chạy
thêm `build/design_gate.py` (tiêu chí đầy đủ ở `review/tieu_chi_thiet_ke_slide.md`):
7 nhóm, 100 điểm, mỗi tiêu chí có ngưỡng số. Deck đó đo ra 35.5/100 — khớp
điểm giáo viên chấm, tức cổng đo thật chứ không nới tay.

Nguyên nhân gốc của lỗi thẩm mỹ: viết nội dung thẳng lên slide, mỗi chỗ tự
chọn một cỡ chữ và một màu theo cảm tính. Deck 17–18 tích luỹ **12 cỡ chữ
khác nhau** (12 · 12.8 · 13.5 · 14.2 · 15 · 15.8 · 16.5 · 17.2 · 30 · 36 ·
37.5 · 40.5) — đó là số rơi rác, không phải thang chữ. Thứ tự bắt buộc:
design brief → `design_tokens.py` (màu theo vai trò + thang chữ theo vai trò)
→ layout variants → **một slide mẫu gửi giáo viên duyệt mắt** → mới nhân rộng.

Bảy lỗi detector, mỗi lỗi là một PASS/FAIL giả:

1. **Đo một vế sẽ thưởng cho lỗi.** "Số kiểu bố cục ≥ 5" cho deck này PASS
   20/20 vì ra 18 cụm/19 slide. Đọc ngược dấu hiệu: nhiều kiểu ở đây là
   **không có hệ layout**, không phải đa dạng. Phải đo hai vế ngược nhau:
   đa dạng (≥5 cụm) VÀ tái sử dụng (≥60% slide nằm trong cụm dùng lại ≥2 lần).
2. **So màu phải loại màu gần trắng.** Bản đầu so `#F0F9FF` với `#B45309`
   rồi kết luận "lệch 178°, PASS". Chỉ so màu có saturation ≥ 0.25 và
   luminance 0.15–0.85.
3. **Không so một màu với chính nó.** Bản đầu FAIL "#E2E8F0 trên #E2E8F0 =
   1.00:1" vì ghép mọi cặp màu trong bảng. Tương phản phải lấy màu chữ của
   run so với màu nền THẬT của shape chứa run đó.
4. **Đếm shape thô cho PASS giả.** Bản đầu đếm mọi autoshape thành "minh hoạ"
   nên 19/19 slide PASS. Phải loại nền phủ >80% diện tích và mảnh vụn <0.4 in².
5. **Cổng đo chữ RENDER bỏ lọt HỘP SHAPE tràn.** Caption slide 7/8 bị đẩy tới
   mép phải 13.65in (slide rộng 13.33in) do script dời `left` mà quên co
   `width`. `qa_all.py` G5 vẫn PASS vì đo chữ render, caption canh trái nên
   chữ không thò ra. Bắt lỗi này phải đo toạ độ hộp shape.
6. **Ngưỡng lề phải đúng cho từng loại phần tử.** Áp lề trên 0.40in cho mọi
   phần tử bắt oan 33 tiêu đề slide (y = 0.27in); áp chuẩn nội dung 6.86in
   cho chân trang bắt oan 90 phần tử. Phân loại footer / full-bleed / lỗi thật
   trước khi kết luận, không đếm thô.
7. **Hai cổng đánh nhau.** Cổng thiết kế bản đầu đòi "≥1 slide nền đậm mỗi 8
   slide" trong khi skill này quy định nền sáng tuyệt đối và `qa_all.py` G7
   chặn nền tối mới thêm. Sửa: ngắt nhịp bằng **dải màu nhấn bão hoà phủ
   ≥25%**, nền vẫn sáng; thêm tiêu chí chống xung đột "không thêm nền tối".
   Trước khi đặt một tiêu chí mới, kiểm nó không bắt làm điều cổng khác cấm.

Quy tắc viết cổng: tiêu chí không tự động hoá được thì khai `NA` và **loại
khỏi mẫu số**, không âm thầm tính PASS. Số 0 nghĩa là "detector không thấy
gì", không phải "đạt" — mẫu rỗng thì trả `NA`. Sau khi sửa detector phải
chạy lại và **giải thích được vì sao con số đổi** (53.4 → 30.5 → 35.5, mỗi
bước đều có nguyên nhân ghi lại được).

Chụp ảnh phần mềm cho slide phải đi qua ĐÚNG chu trình 4 bước đo được, không nhảy cóc (đã trả giá 6 lần trong một phiên 2026-10-11):

1. **Chứng minh hạ tầng trước khi nhân rộng.** Dựng driver thao tác GUI thật (Xvfb + app + xtest click/type + `import -window root` rồi crop theo geometry — `import -window <wid>` FAIL trên Xvfb vì MIT-SHM). Verify bằng pixel-diff từng thao tác VÀ OCR đọc lại kết quả, không tin lời khai "đã bấm". Toạ độ KHÔNG đoán: calib bằng hình có toạ độ biết trước (vẽ 2 mốc đỏ ở SVG (100,100) và (500,400), tìm bbox màu đỏ trong ảnh -> scale + origin; sai số kiểm chéo phải ~0px).
2. **Menu thì mở bằng MNEMONIC, không click theo OCR bbox của thanh menu.** rapidocr GỘP cả thanh menu thành một bbox (`ObjectPathTextFiltersExtensionsHelp`) -> lấy tâm bbox đó bấm NHẦM menu bên cạnh (bấm ra Filters thay vì Path). Popup menu thì OCR tách từng dòng nên toạ độ tin được.
3. **Chụp ĐỦ bằng chứng rồi mới compose.** Boolean op (Union/Difference) làm đối tượng mất fill -> phải tô lại màu THẬT (mở Fill and Stroke, OCR tìm ô RGBA rồi click + gõ hex) và verify bằng pixel màu trội trong ảnh + status bar. Bằng chứng CỨNG nhất cho lệnh đã chạy: đọc lại chính tệp đã lưu (`grep textPath` sau Put on Path).
4. **Compose strip 2 tầng: menu thật (bằng chứng nhận diện app) + canvas crop sát hình.** Focus box tính từ toạ độ SVG đã calib (không đo mờ). Strip width = body width (tối thiểu ~520px giữ trọn menu File..Help) — dán body hẹp lên nền full-width sinh 2/3 ảnh là nền xám vô ích (vision bắt được).
5. **Cỡ chữ trong ảnh khi chiếu: `pt = 72 × line_px × pic_w_in / W_final`.** Upscale KHÔNG đổi pt. Đòn bẩy thật là CROP HẸP và CHIA CỘT: ảnh terminal nhiều dòng đặt vào dải thấp (~2.1in) thì chữ chỉ 3pt; chia 2-3 cột tại KHE TRẮNG giữa 2 dòng (tìm bằng row-profile, không cắt giữa dòng) -> H giảm N lần -> pt tăng N lần. Bắt buộc loại cột tối liên tục (>55-80% chiều cao) = viền cửa sổ + scrollbar TRƯỚC khi lấy bbox, nếu không bbox phình cả cửa sổ. **Công thức đo pt từ ĐỈNH ẢNH (chiều cao) chứ không phải chiều ngang**: `pt = 72 × line_px × band_h / H_final` — ảnh càng NHIỀU DÒNG (H lớn) chữ càng nhỏ, upscale 2x chỉ chống mờ khi PPT scale chứ không tăng pt. Đặt ngưỡng: mọi ảnh phải đạt ≥13pt tại band dự trù; in số đo từng ảnh ra log, không ước lượng bằng mắt.

**IDLE/Tk trên Xvfb KHÔNG render text (đã fail 4 lần liên tiếp -> dừng theo two-strike rule).** Chuỗi lỗi: vùng text trắng OCR 0 dòng trên mọi display mới; font config `~/.idlelib/config-main.cfg` không áp dụng (đo ASCII-art: dòng chữ chỉ ~13px = font 10pt); resize/move/click/wiggle đều không cứu. Nguyên nhân sâu: Tk vẽ shell qua tiến trình con RPC (`idlelib.run`) không render kịp trên Xvfb. **Đường chạy được: `xterm -fa 'DejaVu Sans Mono' -fs 22 -bg white -fg black -e python3 -i -q`** — tự vẽ ngay, font đặt thẳng command line. Code có tiếng Việt: dán qua `xclip -selection clipboard` + `shift+Insert` (xdotool type không gõ được dấu); hoặc tránh dấu bằng escape `\u00edn`. Lệnh shell (`printf '100\n' | python3 script.py`) PHẢI chạy trong xterm+bash, gõ vào REPL sẽ SyntaxError.

**KHÔNG BAO GIỜ kill tiến trình theo pattern.** `ps | grep idlelib | xargs kill` tự giết shell của chính mình (command line của lệnh chứa pattern) — gặp 2 lần, một lần SIGTERM một lần SIGKILL. Cách đúng: script Python đọc `/proc/<pid>/cmdline`, loại trừ PID của chính mình + toàn bộ tổ tiên (`/proc/<pid>/stat` field 4), rồi `os.kill`. Hoặc ghi PID lúc launch vào file rồi kill đúng PID đó.

**OCR đọc sai ≠ ảnh sai, và needle sai ≠ ảnh sai — phải đọc raw OCR trước khi sửa.** Gặp trong một phiên: 7 ca "miss" thì 3 ca là OCR nhầm ký tự đơn (`9`→`6`, `TypeError`→garble) và 1 ca là needle viết theo trí nhớ trong khi Python 3.11 thật nói `invalid decimal literal` thay vì `invalid syntax`. Xác minh ca nghi vấn bằng vision "đọc NGUYÊN VĂN dòng ta biết trước"; needle phải lấy từ ground truth TÍNH BẰNG LỆNH.

Chụp ảnh giao diện phần mềm cho slide: **chiều cao dải trống quyết định cỡ chữ, không phải chiều rộng**.
chữ, không phải chiều rộng**. Công thức `pt = font_px × zoom × band_h × 72 /
crop_h`. Chrome Calc (menu + toolbar + formula bar) là hằng số ~110–170px
không scale theo zoom, nên giữ nguyên cả cửa sổ trong dải 1.2in thì chữ trong
ô teo dưới 12pt. Giải pháp đã verify bằng vision: **ảnh ghép 2 tầng** — tầng
trên là thanh menu thật (bằng chứng đây là Calc), tầng dưới là lưới cắt sát
tới đúng dòng cần dạy — ra 13.3–16.1pt. Cắt bằng toạ độ OCR thật, KHÔNG ngoại
suy công thức (hai lần ngoại suy ra ảnh cắt mất nội dung: mất dòng 13, mất
cặp trùng 007/007). OCR hay nhận nhầm nút `A` (font color) trên toolbar thành
chữ cột A → phải chọn cluster chữ cái có nhiều chữ nhất thay vì `min(y0)`.

## Cổng NỘI DUNG riêng, và bài học về kết luận của reviewer độc lập

Cổng kỹ thuật và cổng thiết kế vẫn không bắt được lỗi nội dung. Đã xây
`build/content_gate.py` (tiêu chí ở `review/tieu_chi_noi_dung_day_hoc.md`): 5
nhóm C1 mạch module · C2 kiến thức có cấu trúc · C3 năng lực số · C4 thực
hành · C5 nhất quán với dữ liệu thật. Lý do phải có ngưỡng số: rubric gốc
cho nhóm nội dung 90 điểm nhưng chỉ có câu hỏi, nên ba vòng chấm độc lập cho
A2 hai mức điểm khác nhau (6 rồi 7) trên cùng một deck.

Module 2 đo ngày 10/10/2026: deck 17–18 **86% ĐẠT**, deck 13–14 **58%**, deck
15–16 **45%**. Ba deck cùng module chênh nhau 41 điểm vì chỉ một deck được
sửa sâu.

**Kết luận của reviewer độc lập cũng chỉ là một tuyên bố, phải kiểm lại bằng
lệnh.** Một vòng chấm khẳng định "không có bản ghi 9A1, tổng lỗi thật = 16,
Lỗi thời = 0" và trừ điểm A2 vì cho rằng ghi chú GV mâu thuẫn với tệp. Đo lại:
cột Lop = `{'10A1': 15, '10A3': 19, '10A2': 7, '9A1': 1}`, đáp án máy =
Thiếu 4 · Sai 4 · Trùng 2 · Lệch định dạng 6 · Lỗi thời 1 = **17**. Hai bản
CSV trong repo có SHA-256 giống hệt nhau (`ecf05ea79093169f`) nên không phải
tệp bị thay giữa hai lần đo. **Ghi chú GV đúng, reviewer sai, điểm bị trừ
oan.** Trước khi sửa theo reviewer, phải tự đếm lại trên tệp thật.

Ba detector bẫy đã gặp khi viết cổng nội dung:

1. **Không regex số trên toàn văn bản để đọc một cột bảng.** Đọc quỹ thời
   gian bằng regex ra 235/231/578 phút cho buổi 90 phút vì bắt cả số thứ tự,
   số tệp, số slide. Bảng lộ trình **không phải** shape `has_table` (rỗng trên
   cả 3 deck) mà là textbox rời: phải gom shape chứa số thuần theo cùng toạ
   độ `left`, nhóm đông nhất là cột cần đọc. Kết quả thật: 82 · 76 · 90 phút.
2. **Slide tự khai quỹ thời gian rồi xếp hoạt động lệch.** 13–14 khai 90 phút
   nhưng cộng ra 82 (thiếu 8), 15–16 khai 90 nhưng cộng ra 76 (thiếu 14). Đây
   là lỗi số học trong giáo án: thầy sẽ trống 8–14 phút cuối buổi mà không
   biết vì sao. Phải có tiêu chí cộng lại và đối chiếu con số tự khai.
3. **Nhánh NA trả `ok=True` là PASS giả nguy hiểm nhất.** Tiêu chí đối chiếu
   tên lớp với tệp dữ liệu, khi không tìm thấy tệp, đã in chữ "NA" nhưng trả
   `ok=True` — khiến nhóm C5 được 10/10 cho hai deck không hề có dữ liệu thực
   hành và nâng xếp loại tổng lên sai. Mọi nhánh NA phải trả `ok=None`.

Hai lỗi nội dung cụ thể làm học trò chết trong lớp, phát hiện bằng cách ĐẾM
từ chứ không phải đọc lướt: deck dạy "lưu trữ đám mây" nhắc "đám mây" 9 lần
nhưng **Google Drive 0 lần, OneDrive 0, Dropbox 0**; deck dạy OCR nhưng
**Google Lens 0, CamScanner 0, Tesseract 0, chữ "điện thoại" cũng 0 lần**, chỉ
viết "ứng dụng OCR đã được phép". Khi dạy một công cụ, phải đếm xem tên công
cụ đó có mặt trong deck không — nêu chung chung thì học trò ngồi trước máy
không biết mở cái gì.

## Chú thích trên ảnh chụp: 4 luật đã trả giá

Khi chủ dự án yêu cầu "đóng khung + mũi tên + giải thích" ngay trên ảnh chụp thật
(câu trả lời AI, màn hình phần mềm), viết script PIL nhưng giữ 4 luật sau. Mỗi
luật đều sinh ra từ một lần vẽ hỏng, không phải suy đoán.

1. **Toạ độ khung lấy từ OCR thật, kèm khoảng y để lọc.** OCR trả về hàng chục
   mục; một từ khoá như `ngay_sinh` khớp ở NHIỀU chỗ khác nhau (bảng tổng quan,
   mục chi tiết, kết luận) nên khung sẽ bao trùm nửa ảnh. Phải lọc theo
   `ymin <= y0 <= ymax` đo từ bản đồ OCR trước. OCR không định vị được thì
   **bỏ qua khối đó**, không vẽ vào chỗ đoán — khung sai chỗ tệ hơn không khung.
2. **Huy hiệu số đặt trong RÃNH TRỐNG dành riêng, không đặt ở góc khung.** Đặt
   ở góc khung thì đè lên chữ của ảnh: đo được 7/6 huy hiệu đè chữ, cái nặng
   nhất che 840px² chữ. Chừa `GUTTER` (đã dùng 64px) bên trái ảnh, tâm huy hiệu
   giữa rãnh, và kẹp `cy` để các huy hiệu không chồng nhau (`cy - prev >= 2r+6`).
3. **Mũi tên ngang phải kiểm khoảng trống trước khi vẽ.** Khung rộng sát mép
   bảng thì `điểm đầu > điểm cuối` → mũi tên NGƯỢC. Đo được 2/6 mũi tên ngược
   (khung rộng tới x=894 trong khi bảng bắt đầu x=944). Chỉ vẽ khi
   `panel_x - 26 - ax0 >= 30`, ngược lại in ra thông báo và để số + màu tự liên kết.
4. **Cổng cỡ chữ theo canvas THẬT, kiểm trước khi ghi ảnh.**
   `pt = font_px × (place_inch / canvas_px) × 72`. Ảnh 1440px ghép thêm bảng
   780px thành canvas 2254px thì chữ 19px chỉ còn 7.2pt, dưới sàn 12pt.
   Tính `min_font = canvas_w × 12 / (11.83 × 72)`, chọn font lớn hơn, in ra số
   pt đạt được và `sys.exit` nếu dưới sàn. Muốn chữ to thì CẮT ảnh về đúng
   vùng cần dạy (bỏ sidebar, lề trắng) thay vì tăng font.

**Verify ảnh chú thích bằng hình học, không bằng OCR.** OCR không tách được chữ
số trắng trên nền huy hiệu màu thành mục riêng, nên đếm huy hiệu bằng OCR báo 0
(sai phương pháp, không phải ảnh lỗi). Đúng cách là quét pixel tìm đúng mã màu
huy hiệu, cộng với kiểm: khung nằm trong vùng ảnh, khung không chồng nhau,
chữ thấp nhất < chiều cao canvas, chữ phải nhất < chiều rộng canvas.

**Vision timeout thì chuyển sang hình học, không retry mù.** Trong một phiên
vision timeout liên tiếp 3 lần; mỗi lần retry tốn thời gian mà không thêm bằng
chứng. Phép kiểm hình học đo được và bắt đúng 2 lỗi thật mà vision chưa kịp thấy.

## Ảnh chụp màn hình cho slide: 5 luật đã trả giá

Khi bài dạy cần ảnh thao tác thật (giao diện AI, Calc, web), giữ 5 luật này. Mỗi
luật sinh ra từ một lần đo sai hoặc vẽ hỏng, không phải suy đoán.

1. **Ảnh chụp chat AI thường bị MẶT NẠ MỜ CUỘN ở đỉnh vùng tin nhắn.** Open WebUI
   phủ gradient trắng lên phần đầu câu trả lời. Đã đo min pixel TRONG hộp chữ OCR:
   dòng đầu min=124..186 trong khi các dòng dưới min=22..40. Không sửa được bằng
   tăng tương phản (đã thử tới k=2.2, mực đã bị pha trắng nên thông tin mất). Cách
   đúng là TỰ DÒ vùng sạch: y_clean = đáy của hộp chữ mờ thấp nhất, cắt từ đó, rồi
   verify lại mực trên ảnh đã cắt.
2. **Đo cỡ chữ trong ảnh bằng TRUNG VỊ chiều cao hộp OCR trên ẢNH GỐC.** Hai phép
   đo sai đã trả giá: (a) quét min pixel trên cả dải 30% đỉnh ảnh rồi kết luận
   "SẠCH" — min thấp đến từ viền bong bóng chat chứ không phải chữ; (b) đo chiều
   cao hộp OCR trên ảnh ĐÃ CẮT — OCR bẻ một dòng thành nhiều mảnh (ra 16px thay vì
   21px) nên kết luận "chữ dưới sàn" oan cho 3 ảnh.
3. **Công thức cỡ chữ khi chiếu:** `pt = h_px × (rộng_đặt_in / rộng_ảnh_px) × 72`.
   Suy ra hai ràng buộc phải kiểm TRƯỚC khi dựng slide:
   `rộng_đặt ≥ rộng_ảnh × 12 / (h_px × 72)` và `cao_đặt ≤ thân_slide`.
   Ảnh 1440px đặt 11.83in cho chữ 20px chỉ 11.8pt, hụt sàn. Điều kiện khả thi tổng
   quát để khỏi dò tham số: `cao_vùng_cắt ≤ 31.86 × h_px`.
4. **Không nướng bảng giải thích dài vào ảnh.** Ảnh chú thích 1650×891px đặt lên
   slide cho chữ 10.3pt vì canvas phình theo bảng chữ. Giải thích cặn kẽ phải nằm
   ở GHI CHÚ GIÁO VIÊN (cổng chỉ đếm shape trên slide, không đọc notes); trên ảnh
   chỉ để nhãn ngắn và huy hiệu số trong RÃNH TRỐNG dành riêng.
5. **Đo MỰC trên PDF đã render, không đo chồng HỘP shape.** Hộp chồng nhau 0.37in²
   là bình thường khi chữ ngắn hơn hộp; qa_deck đo mực và báo overlap=0. Detector tự
   viết mà so hộp sẽ báo oan.
6. **Quy đổi toạ độ OCR phải trừ CẢ HAI trục.** Crop bắt đầu ở x=325 mà chỉ trừ
   `off_y` thì mọi khung dịch phải 325px: khung số 1 vẽ từ x=609 tới x=1228 trong
   khi bảng giải thích bắt đầu ở x=957, viền cắt ngang chữ bên phải. Vision bắt
   được trên slide render, log thì vẫn báo "OK" vì cổng chỉ kiểm cỡ chữ.
   Verify đúng cách là PIXEL DIFF: so vùng ảnh của bản chú thích với ảnh gốc, đếm
   pixel vừa khác nhau vừa có mực tối ở bản gốc. Phải ra 0.
7. **Điều kiện vẽ mũi tên phải là "nằm trọn trong rãnh", không phải "đủ dài".**
   Kiểm `room >= 26` vẫn cho mũi tên vẽ từ x=67 tới x=292 trong khi ảnh bắt đầu
   x=78, xuyên 214px qua chữ trông như gạch xoá. Phải thêm `px0 <= IMG_X + 8`.
   Nguyên tắc chung: khi vẽ đè lên ảnh chụp, điều kiện chặn phải so với MÉP ẢNH,
   không so với chiều dài khả dụng.

## Chèn slide vào GIỮA deck đang có: 6 việc bắt buộc

Khác hẳn dựng deck mới. Đã trả giá bằng deck 27 slide (chèn trùng), notes sai số
slide, và một mốc phút lệch 4 phút có sẵn mà không cổng nào bắt.

1. **Guard chống chạy trùng.** Script đọc và ghi CÙNG MỘT tệp nên chạy hai lần là
   chèn hai lần. Chốt số slide gốc và dò tiêu đề slide mới TRƯỚC khi backup.
2. **Không hardcode `slide_layouts[6]`.** Deck dựng sẵn có thể chỉ có MỘT layout ở
   index 0 (đã đo: master của deck 17-18 có đúng 1 layout). Lấy layout từ
   `prs.slides[0].slide_layout`.
3. **Retiming toàn bộ.** Notes chứa BA lớp tham chiếu sẽ lệch khi chèn: số slide
   trong tiêu đề ("Slide 7 — ..."), mốc phút ("[phút 17–23]"), và tham chiếu chéo
   trong thân ("đối chiếu nguồn ở slide 8"). Phải map TỰ ĐỘNG theo timeline, không
   viết tay số — viết tay đã ra số sai (ghi `[5–7]` trong khi span mới là `[4–8]`).
   Đọc span gốc TRƯỚC khi chèn, vì bước retiming ghi đè dòng tiêu đề notes.
4. **Mốc chuyển tiếp là HỢP LỆ.** Notes hay ghi "[10–17] năm loại lỗi ở slide 6" —
   mốc đó là span của slide KẾ, không phải của slide chứa nó. Detector bắt mọi mốc
   phải nằm trong span của chính nó sẽ báo oan 15/15 mốc. Kiểm đúng: mốc phải BẰNG
   span của một slide nào đó trong timeline.
5. **Cắt phút thì phải sửa chữ theo, và không được sinh khoảng rỗng.** Slide còn 4
   phút mà notes vẫn bảo "cho lớp chép (1 phút)" và "gọi hai đến ba em trình bày" là
   tự mâu thuẫn. Co giãn mốc theo tỉ lệ có thể làm tròn sụp thành `[45–45]` (0 phút)
   khi span mới ngắn hơn số mốc cũ — phải ép mỗi mốc dài ≥ 1 phút.
6. **Không dùng helper của bộ deck khác.** `helpers_clb.header()` hardcode kicker
   14.0pt trong khi deck 17-18 dùng 14.2 (26 lần), làm deck phình từ 12 lên 13 cỡ
   chữ và N1.1 (ngưỡng ≤ 5 cỡ) tệ hơn. Viết header cục bộ khớp hình học ĐO ĐƯỢC, và
   thêm CỔNG KIỂM CỠ CHỮ trước khi save: so tập cỡ của slide mới với tập cỡ đọc từ
   backup, FAIL nếu sinh cỡ lạ.

## Điều kiện hoàn tất

Chỉ báo hoàn tất bản local khi file cuối mở được; PPTX/PDF cùng số trang; đủ notes; nội dung và render đã được kiểm tra, không còn P0/P1, tràn khung, placeholder hay nội dung sai nguồn; `con_bai_tap = []` (không còn slide bài tập/luyện tập/vận dụng); `so_nen_toi_that = 0`; `ink_clip_check` báo `so_van_de = 0`; **và `build/design_gate.py` đạt ≥ 70/100** (dưới 70 là "không dùng, phải làm lại từ design tokens") **và `build/content_gate.py` đạt ≥ 85%** nội dung. Đạt cổng kỹ thuật chỉ là điều kiện cần, không đủ để báo đạt. Giao bản duyệt hoàn tất khi tệp được gửi đúng đích với bằng chứng giao nhận. Chỉ khi được phép phát hành Drive mới thêm điều kiện archive đã xác minh và cặp tệp tải ngược có SHA-256 trùng bản local. Không tự upload để thoả điều kiện hoàn tất của một yêu cầu chỉ gửi duyệt.

Số liệu báo cáo phải là số đo thật, kèm đường dẫn và checksum — không mô tả suông.

### Giới hạn của bằng chứng QA và kỷ luật tiến độ

- **QA deck CLB chạy QUA MỘT CỔNG DUY NHẤT: `python3 $HOME/clb_nls/build/qa_all.py <pptx> --baseline <pptx_goc>`.** Cấm gọi tay từng script QA rồi ghép kết quả bằng trí nhớ — đó là nguồn gốc của cả 3 lỗi gọi sai trong một lượt (thiếu tham số, gate đo rỗng exit 0, đoán tên khóa JSON). Chữ ký tool và schema JSON đã xác minh nằm trong `qa_all.py`; sửa gate nào thì phải chạy lại control test hai chiều (gate phải FAIL trên fixture hỏng: thư mục rỗng → RỖNG→FAIL; thêm khối navy 12in² → G7 FAIL). `overlap_glyph_check.py` bị loại khỏi cổng vì phần 3 hard-code chuỗi bài Python BAI_17.
- **Trước khi parse JSON của một tool, in `list(d.keys())` hoặc đọc schema một lần — không đoán tên khóa trong code.** Đã đoán sai 2 lần trong một lượt (`so_nen_toi_that` thật là `so_hop_nen_toi`; `so_run_da_do` thật là `typography.so_run`); cả hai trả `None` rồi suýt được hiểu là 0/PASS. Schema `qa_deck.py --json` đã chốt trong docstring của `gate_qa_deck`.
- **Gate đo RỖNG nguy hiểm hơn gate FAIL.** `pdf_font_audit.py` nhận THƯ MỤC chứ không nhận đường dẫn file; đưa file vào nó in `kiem 0 PDF ... TONG: 0 file` rồi exit 0, trông như PASS. Mọi cổng QA phải in SỐ ARTIFACT ĐÃ ĐO và chỉ được coi là đạt khi số đó > 0. Cùng lỗi: đọc `so_nen_toi_that` cho ra `None` rồi tưởng là 0 — khóa thật của `dark_fill_check.py` là `so_hop_nen_toi`, `tong_dien_tich_toi_in2`, `chi_tiet`. In `list(d.keys())` trước khi trích số, đừng đoán tên khóa.
- **Kiểm tra xem checker có thuộc đúng bài không trước khi tin kết quả.** `overlap_glyph_check.py` hard-code chuỗi của bài Python hoán đổi biến (`a = 7`, `b = temp`, `print(a, b)`, `B17_NhomXX`, `BÀI 13`); chạy nó trên deck CLB khác chủ đề thì `pdf_text_all_ok: false` là ÂM GIẢ, và baseline cũng `false` y hệt. `false` ở cả hai bản nghĩa là checker không áp dụng, không phải "không lỗi".
- **Đếm động từ bằng regex KHÔNG phải bằng chứng về chất lượng thực hành.** Cùng một bộ deck, hai detector cho hai kết quả ngược nhau (438 thao tác/741 ghi chép, rồi 3021/55) chỉ vì khác mẫu và khác phạm vi (slide body so với kèm speaker notes). Dùng chỉ số nhị phân kiểm được bằng mắt: deck CÓ/KHÔNG mã NLS `x.y`, CÓ/KHÔNG nêu tên một công cụ mở được, CÓ/KHÔNG yêu cầu mức "hướng dẫn được bạn". Khi hai phép đo mâu thuẫn, nghi checker trước và đừng trình con số chưa hiệu chuẩn cho giáo viên.
- Báo riêng: nội dung, trực quan, cấu trúc, đồng bộ PPTX/PDF, giao file và phát hành Drive. `ink_clip_check = 0` chỉ chứng minh không phát hiện kiểu cắt chữ mà bộ dò đo được; không chứng minh hết chồng lấn, đúng kiến thức, đủ hình hay đúng giọng sư phạm. Số icon không phải thước đo hình giải thích.
- Không miễn cảnh báo nền tối chỉ vì “ít hơn baseline”. Đối chiếu từng đối tượng với ngưỡng đã chốt; ngoại lệ cần có lí do được chấp nhận, không tự đổi tiêu chuẩn để đạt.
- Sau một sửa đổi kiến thức, quét mọi nơi phát biểu cùng ý: ví dụ, ghi vở, tiêu đề, bảng, bìa, kết bài và notes. Không để ghi vở đúng nhưng phần ví dụ vẫn nói ngược lại.
- Sửa source → kiểm cú pháp → dựng PPTX → xuất PDF → đọc lại và xem render; sửa sau bước nào thì các bằng chứng phía sau bước đó hết hiệu lực. Backup trước khi sửa; thay đổi helper dùng chung phải xét ảnh hưởng đến các bài khác.
- Không lặp lời “em sửa ngay” hoặc đọc lại vùng không đổi. Mỗi cập nhật phải gắn với hành động có đối số đầy đủ và kết quả mới. Subagent trả lỗi API không phải công việc hoàn tất; chuyển cách thực hiện, không giao lại nguyên yêu cầu rồi nhận cùng lỗi.
- Khi giáo viên yêu cầu duyệt lại, chỉ giao bản local đã kiểm tra; không tự cập nhật Drive. Chỉ đánh dấu giao đúng thread khi có bằng chứng đích thread và tệp đính kèm; `success` kèm ID kênh gốc đơn thuần chưa đủ.

## Vẽ lại chart: màu phải gắn theo TÊN biến thể, không theo vị trí

Khi vẽ lại chart để phóng chữ mà chép lại danh sách màu, **luôn gắn màu theo tên (dict) thay vì theo vị trí (list)**. Lỗi thật đã xảy ra: `colors = [GREEN, "#2F6FB2", AMBER, ...]` thay vì `[GREEN, AMBER, "#2F6FB2", ...]` → hoán đổi amber ↔ xanh dương giữa hai thanh ablation. Hậu quả: kịch bản nói *"the blue bar – removing AoI"* chỉ vào thanh sai ngay trên bục, trước giám khảo.

Vì sao không cổng QA nào bắt được: màu không ảnh hưởng `ink_clip`, z-order, glyph, hay số liệu — mọi cổng đều PASS trong khi chart sai. Chỉ có **đối chiếu mô tả màu trong lời thoại** mới phát hiện ra.

Bắt buộc khi vẽ lại chart:
1. `COLOR_BY_NAME = {...}` rồi `colors = [COLOR_BY_NAME[k] for k, _ in order]`.
2. Thêm `assert` ràng buộc từng cặp màu theo đúng chữ trong notes/kịch bản (vd `assert color[no_aoi] == BLUE` vì notes gọi nó là "the blue bar").
3. So bảng màu với script gốc bằng cách **map tên hàm** — tên hàm thường khác nhau giữa hai script (`s03_temperature` vs `s03`) nên giao rỗng và phép so âm thầm không kiểm tra gì.
4. Kiểm chứng cuối bằng **pixel thật** trên ảnh trong deck VÀ ảnh trong handout: đếm pixel từng màu, xác nhận thứ tự dọc khớp thứ tự thanh, và số pixel tỉ lệ với giá trị (thanh dài hơn = giá trị lớn hơn).

## Bốn lỗi cơ học hay gặp khi vá slide/kịch bản bằng script

1. **So sánh baseline phải chọn theo `mtime`, không theo tên.** `sorted(glob('*.old_*'))[-1]` lấy theo thứ tự chữ cái → dễ so với bản cũ hơn bản liền trước, mọi chênh lệch đọc ra đều sai quy nguyên nhân. Khi tool build tự đổi tên bản cũ (`x.pdf.old_<sha8>`), chọn `max(key=mtime)`.
2. **Character class trong regex phải chứa dấu gạch nối** khi khớp nhãn/tiêu đề: `[A-Z ]` sẽ trượt `TRADE-OFF PICTURE`. Đặt `-` ở cuối class (`[A-Z0-9 \-]`) để khỏi bị hiểu là khoảng.
3. **Script *chèn* khối vào MD phải làm idempotent trước khi chạy lại** — MD artifact đã có khối đó thì chạy lại sẽ nhân đôi. Sửa thành tìm biên khối cũ và *thay*; đồng thời nới assert "không mất nội dung cũ" ra chỉ kiểm phần NGOÀI khối, nếu không assert bắn oan và file không được ghi.
4. **Không hardcode số liệu/nguồn trong script sinh tài liệu.** Tên deck, sha256, tổng số từ, giờ kết thúc phải tính từ dữ liệu thật; nếu không, chỉ cần sửa một câu là handout in ra nguồn sai (đã gặp: "2425 từ / 19:24 / deck FINAL" vẫn in sau khi bài đã thành 2431 từ / 19:27).

Khi sửa lời nói trong kịch bản: **sửa ở nguồn** (`deck19_content.json` + notes pptx + `kich_ban_vi_p*.json`), không sửa thẳng MD — MD là artifact sinh ra. Nhưng **không chạy lại script *chèn*** (`merge_kich_ban.py`, `embed_images.py`) vì MD đã có đủ khối; thay vào đó vá tại chỗ theo `cues19.json` đã tái sinh. Sửa lời làm đổi số từ → phải tái sinh đồng hồ (heading + dòng word-count + bảng ĐỒNG HỒ), nếu không handout sai giờ đúng lúc người nói đang bấm đồng hồ.

`os.system(f"... {pdf} ...")` với đường dẫn từ biến môi trường là command-injection sink — dùng `subprocess.run([...], check=True)`. Lưu ý: scanner an toàn khớp cả **chữ trong comment**, nên viết comment giải thích tránh nhắc nguyên văn `os.system(...)` nếu không muốn bị báo lại.

## Thêm chữ vào slide: python-pptx KHÔNG tự nới khung, và thẻ nền cũng phải nới

`auto_size=SHAPE_TO_FIT_TEXT` chỉ là **khai báo trong XML**; python-pptx không tính lại chiều cao khi thêm paragraph. LibreOffice render theo chiều cao đã lưu → **paragraph thêm vào bị cắt mất**, trong khi đọc lại file bằng python-pptx vẫn thấy đủ chữ. Đã gặp thật: thêm bullet thứ 6, file có 6, bản render chỉ có 5.

Hai việc bắt buộc mỗi lần thêm chữ:
1. Đặt `shape.height = Inches(...)` **tường minh**, tính từ số dòng wrap thật.
2. Nới luôn **thẻ nền** chứa khung chữ đó (thường là `Rounded Rectangle` riêng biệt). Đã gặp thật: khung chữ nới đủ nhưng thẻ nền vẫn 3.75in trong khi chữ xuống 6.30in → `ink_clip_check` báo chữ tràn mép thẻ, `phu_trong_the=0.61`.

Đo chiều cao cần bằng **pitch thật lấy từ bản render** (hiệu y0 giữa hai dòng liên tiếp) cộng khe giữa các paragraph (`space_after` EMU/12700), không dùng `số_dòng × font × 1.45`. Ước lượng kiểu đó đã sai 0.57in vì không tính xuống dòng: 5 bullet thực tế wrap thành 13 dòng.

## Đo độ vừa chữ phải hiệu chuẩn theo bản render, và nhớ trừ thụt lề đầu dòng

`usable_width ≠ shape.width × 72`. Danh sách có dấu đầu dòng (`▸`, hanging indent) làm chữ bắt đầu thụt vào — đo thật trên render: chữ bắt đầu x=652.1pt trong khi hộp bắt đầu 637.9pt → **mất 14.2pt**. Bỏ sót khoản này khiến một phép đo báo "vừa" với biên 3.7pt (1.4%), và bản render đã wrap thành 2 dòng gây đè chữ.

Cách làm: chọn một chuỗi **đã biết chiều rộng thật trên bản render**, tính `k = rộng_render / rộng_PIL` (đo được k≈1.01), rồi dùng `k` cho mọi chuỗi khác. Yêu cầu biên dư ≥4% mới coi là an toàn. Nếu không biến thể nào đủ chỗ thì **giữ chữ gốc trên slide và đưa chi tiết vào handout** — đừng ép chữ lên slide chỉ để thỏa một góp ý trình bày.

## Verify trên BẢN RENDER, không verify trên file — và đừng phân loại span theo tọa độ

Mọi cổng QA đọc file `.pptx` (z-order so box khai báo, đọc lại bằng python-pptx) đều **không thấy** lỗi đè chữ thật, vì chúng so khung đã khai báo chứ không so chữ đã render. Chỉ PyMuPDF trên PDF render mới thấy.

Khi phân loại span, **không dùng ngưỡng tọa độ để quyết định một span thuộc nhóm nào**. Đã lặp lại đúng một loại lỗi này 4 lần:
1. Ngưỡng y → span cần tìm rơi vào cả hai nhóm và bị loại âm thầm khỏi cả hai, kết luận "không render" trong khi có render.
2. Lọc `x ≥ ...` ở bước lấy span → loại hết dải chữ trải ngang trang (bắt đầu x=72pt), rồi so va chạm với **danh sách rỗng** và báo PASS giả.
3. Bỏ lọc x nhưng vẫn xếp nhóm theo x → **số trang ở footer** (`15/19`, x=922) bị tính là bullet, báo gap −52.9pt (đè chữ) trong khi gap thật +12.3pt.
4. Chỉ hết lỗi khi: loại dải footer trước (`y0 ≥ footer_top`), xếp nhóm **theo nội dung chữ**, và `assert` tổng ba nhóm bằng tổng số span để không span nào bị bỏ rơi âm thầm.

Khi đo va chạm, phân loại theo nội dung và **in ra cả nhóm bị loại** để tự kiểm tra — nếu một nhóm rỗng thì phép đo vô nghĩa, không phải PASS.

## Góp ý của reviewer phải được kiểm chứng trước khi ghi lên slide

Reviewer độc lập đã đề nghị hai lần **sai sự thật**, và nếu nghe theo sẽ đưa nhãn sai lên slide của một bài báo:
- "viết `Spearman rho = 0.59`" → code đã công bố chỉ có `def pearson()` và in `Pearson(Mhat, m)`. Phải ghi Pearson.
- "viết `miss 0.008/slot`" → code tính `miss_rate_step = d/(a+d)` là một **tỉ lệ**, không phải tốc độ theo slot.

Nguyên tắc: mọi nhãn thống kê, đơn vị, tên chỉ số đưa lên slide phải truy được về **code hoặc bảng đã công bố**. Nếu không truy được thì giữ nguyên chữ gốc và ghi chú trong handout. Ngược lại, khi reviewer nêu một con số chưa kiểm định, hãy tra bảng đã công bố để xác nhận **sự vắng mặt** của nó (caption ghi rõ phạm vi, vd "Severe-burst paired Wilcoxon tests") rồi thêm rào "chưa kiểm định" — **không được bịa p-value** để làm slide trông đầy đủ.

## Peer review: gói dữ liệu phải đủ, và phải nhỏ

Hai ràng buộc mâu thuẫn, phải thỏa cả hai:
- **Đủ**: bản `.md` đưa reviewer phải chứa **notes nguyên văn** (lời nói trên bục), không chỉ text trên slide. Đã xảy ra: reviewer không verify được 7 sửa đổi phía kịch bản và đánh dấu toàn bộ là UNVERIFIABLE → vòng review mất tác dụng.
- **Nhỏ**: giới hạn ~15–40KB và nói rõ "chỉ đọc file này". Đã xảy ra: reviewer được cho ~110KB thì chết ở bước gọi model, 0 verdict trên đĩa dù nhãn báo `completed`. Với vòng delta, trích riêng các slide đã sửa thành một file nhỏ thay vì đưa lại toàn bộ.

Nhãn `completed` của subagent **không phải bằng chứng**: luôn kiểm tra file verdict thật trên đĩa (tên reviewer, verdict, số critical). Nếu thiếu file thì coi như chưa review và làm lại, đừng kể công.

## `overlap_glyph_check.py` hardcode token của bộ Tin học THPT — không áp dụng cho deck khác

`~/slide_sources/qa_tools/overlap_glyph_check.py` chỉ nhận 3 tham số (`pptx pdf out`) và **hardcode danh sách token bắt buộc** ở dòng ~92: `'class','B17_NhomXX','BÀI 13','ten lop','2diem','3 7','3 3'`. Mọi deck ngoài họ đó (ví dụ deck hội nghị <venue-A>/<venue-B>) đều trả `pdf_text_all_ok: false` — **kể cả bản baseline đã được duyệt**. Quy tắc: khi một cổng QA báo fail đồng thời trên cả baseline lẫn bản sửa, nghi ngờ **phạm vi áp dụng của cổng** trước khi sửa deck; grep danh sách token để xác nhận. Không được trình `false` đó như một lỗi của bản mới, cũng không được bỏ qua im lặng.

Cổng dùng được cho deck hội nghị (không lệ thuộc token): `ink_clip_check.py` (đo toạ độ thật), `audit_zorder.py`, quét glyph bằng `fontTools` cmap của font thật (`msttcorefonts/Arial.ttf`), và so phân phối cỡ chữ trên render.

## Sửa cỡ chữ hàng loạt: phóng chữ PHẢI đi kèm đo lại mực trên render

Khi nâng cỡ chữ toàn deck (map theo bucket, ví dụ 12.5→14.5pt), thẻ/hộp có chiều cao cố định sẽ tràn. Ba bẫy đã trả giá:

1. **Đừng lấy số "mức tràn" của checker làm đầu vào để nới hộp.** Đo được nghịch lý: nới đáy thẻ thêm 13.1pt nhưng checker báo tràn **tăng** 3.1→8.6pt, trong khi text render của hai bản **giống hệt từng pixel**. Cách đúng: tự đo `day muc = max(y1)` của word bbox trong cửa sổ x của thẻ, rồi đặt đáy hộp = đáy mực + đệm.
2. **Lọc theo x chưa đủ khi slide có hai thẻ xếp dọc chung dải x.** Thẻ phải `x=652..918 y=133..349` và thẻ dưới `x=43..917 y=385..490`: chỉ lọc theo x sẽ nhặt chữ của thẻ dưới (y=436) rồi kết luận "cần nới 107.1pt" — lớn hơn cả chiều cao thẻ 200pt, tự nó là bằng chứng vô lý. Bắt buộc chặn thêm `y_max = top của phần tử bên dưới`.
3. **Verify bằng `>=` tuyệt đối sẽ fail vì làm tròn Pt/EMU.** Hai thẻ dư **đúng** 4.0pt vẫn FAIL do giá trị thật là 421.0999… So sánh phải có dung sai (`(bot - ink) >= 3.9`).

Khi thẻ không còn chỗ để nới (dải kết luận bên dưới), **cắt chữ thay vì nới**: đo số ký tự/dòng thật từ render (ví dụ box 280pt chứa ~44 ký tự ở 13pt) rồi rút bullet về đúng một dòng. Chỉ sửa **run cuối** của bullet 3 run (`▸` + lead đậm + rest) để giữ format; không gộp run khi paragraph có `baseline` (subscript `x̂⁻`, `aᵢ,ₜ`, `Bₜ`) — gộp sẽ mất chữ nhỏ trên/dưới.

**Cổng an toàn khi thay text:** so tập số theo **giá trị** chứ không theo chuỗi (`53.0%` ≡ `53%`), và cấm đưa ký tự Unicode mà font thật của deck không có. Đã mắc: đổi `p < 10-3` → `10⁻³` và `CO2` → `CO₂` làm sinh `U+207B`/`U+2082` **thiếu trong Arial** → ô vuông trên máy chiếu Windows, đồng thời `⁻` bị tách thành line riêng nên render báo "chồng chữ". Kiểm bằng cmap của `msttcorefonts/Arial.ttf`: ký tự >126 mới phải **có trong Arial** hoặc **có sẵn trong baseline**.

## Checker viết trên PDF text extraction PHẢI chuẩn hoá khoảng trắng trước

`page.get_text()` của PyMuPDF **làm mất khoảng trắng** giữa các token (`CHỈ TAY 1/9` → `CHỈTAY1/9`, `53 phần trăm` → `53phầntrăm`). Mọi matcher dạng `s.startswith('•[')` hoặc regex có space đều **bỏ sót âm thầm** rồi kết luận sai (đã gặp: báo `136/137` cue thiếu số thứ tự, báo `0/137` dòng VN, báo thiếu chuỗi `53 → 62`). Quy tắc: định nghĩa một hàm `norm = re.sub(r'\s+','',s)` và so **mọi** chuỗi qua `norm`, cả trong danh sách chuỗi bắt buộc.

Đừng bao giờ tự thêm chuỗi vào danh sách bắt buộc khi **chưa grep nó trong MD nguồn** — `53 → 62` là chữ nằm **trong ảnh slide**, không phải text, nên nó không bao giờ có trong PDF text. Kiểm bằng `grep -n` trước khi coi đó là lỗi.

## Assert phải khớp ĐỊNH DẠNG THẬT của output, không khớp ý định

Cổng `assert n_numbered == n_cue` báo `0/137` trong khi cổng ngay trước đó (`n_item == n_cue`) pass với `137`. Nguyên nhân: hàm thay thế sinh `- **[NÓI 1/4]**` (số **trong** ngoặc) nhưng regex kiểm tra lại tìm `] 1/4**` (số **ngoài** ngoạc). Trước khi tin một assert fail, đọc **output thật của chính hàm thay thế đó**; đừng sửa dữ liệu để thoả một assert viết sai.

Tương tự: `zip(sorted(old), sorted(new))` để so cặp là **sai phương pháp** — nó ghép mục của slide này với mục của slide khác rồi báo 131/137 "đổi text" trong khi không mục nào bị đổi. Phải ghép theo **chỉ số đã biết** từ vòng lặp ghi.

## Legend/hướng dẫn sử dụng phải khớp HÀNH VI thật của từng loại cue

Vision review bắt được lỗi mà **không cổng đo nào thấy**: legend ghi "Tiếng Anh = đọc trên bục" trong khi cue `[CHỈ TAY]` là chỉ dẫn tay không đọc to, lại render cùng màu cùng cỡ chữ câu nói → nguy cơ đọc nhầm "Point to the highlighted row…" ngay trên bục. Đây là lỗi **ngữ nghĩa**, chỉ phát hiện được khi đọc trang như người dùng. Quy tắc: mọi legend phân loại phải liệt kê **đủ** các loại nhãn đang dùng và nói rõ loại nào đọc to, loại nào không.

Ghi chú biên tập (timestamp mâu thuẫn, "xem bảng ở cuối", trạng thái verify) **không được nằm trên trang dùng ở bục** — nó mâu thuẫn với khung giờ trên heading và gây phân tâm. Chuyển xuống bảng tra cứu đầu tài liệu hoặc phụ lục.

## Raw inline TeX chỉ giữ được emphasis khi nằm BÊN TRONG cặp `*`

Đo bằng fixture 3 phương án trên cùng nội dung (PyMuPDF đọc `span['size']`, `span['color']`, `span['font']`):

| Cách viết | size | color | Italic | dấu `*` lộ |
|---|---|---|---|---|
| `*\color{gray}\small VN: …*` | 9.0 | `#7f807f` | ✅ | 0 |
| `\begingroup\color{gray}\small *VN: …*\endgroup` | 9.0 | `#7f807f` | ❌ | 2 |
| fenced div `::: vndich` + `\newenvironment` | 10.0 | `#000000` | ❌ | 0 (không tác dụng) |

Đặt raw TeX **trước** dấu `*` làm pandoc mất khả năng nhận emphasis: dấu `*` in ra thành chữ và font không nghiêng. `\color` cần `\usepackage{xcolor}` trong file nạp qua `pandoc -H`, thiếu sẽ `Undefined control sequence`.

Đọc kết quả fixture phải soi **cả bốn** chỉ số. Đã mắc: kết luận "phương án A hoạt động" chỉ vì size và color đúng, bỏ qua dấu `*` lộ và font không Italic → build thật ra bản hỏng.

## Bài học phiên 2026-10-09 — chèn kịch bản nói vào tài liệu giải thích (deck 19 slide)

1. **`re.sub` với chuỗi thay thế chứa backslash sẽ sinh ký tự điều khiển → TeX chết.** `re.sub(pat, '\needspace{5\baselineskip}', s)` bị xử lý escape: `\n`→newline, `\b`→**backspace 0x08** → XeLaTeX报 `! Text line contains an invalid character.` và `exit=43`. Phải dùng **lambda**: `re.sub(pat, lambda m: '\n' + r'\needspace{5\baselineskip}' + '\n\n', s)`. Kèm hai cổng assert trước khi build: (a) số lệnh chèn **bằng** số mục tiêu, (b) `not [ch for ch in s if ord(ch)<32 and ch not in '\n\t\r']`.
2. **Trước khi kết luận "cặp dòng bị cắt ngang trang", phải loại FOOTER.** Checker lấy `lines[-1]` của trang trước để xem có phải cue gốc không, nhưng `lines[-1]` là **số trang ở footer** (`'10'`, `'11'`, y1=723.9 trên trang cao 841.9) → kết luận sai `3/13`. Sửa bằng `if re.fullmatch(r'\d{1,3}', t) and y1 > page_h-130: skip`.
3. **Cue gốc tự xuống dòng, nên đừng kiểm bằng `startswith`.** 130/137 cue tiếng Anh wrap thành ≥2 dòng → dòng cuối trang trước là phần nối tiếp, không bắt đầu bằng `[NÓI]`. Logic đúng: *dòng cuối trang trước không phải bản dịch và không phải heading* → `13/13` xác nhận page break.
4. **Sửa page break bằng `needspace` thay vì đổi bố cục.** `kpsewhich needspace.sty` có sẵn; chèn `\needspace{5\baselineskip}` trước mỗi cue (5 dòng = cue wrap 2–3 dòng + bản dịch 1–2 dòng) và nạp qua `pandoc -H header.tex`. Kết quả đo lại: 137/137 cặp có `dy = 17.93pt` đúng một dòng, **0 cặp dính**, 0 cặp bị cắt trang.
5. **Đếm "chồng lấn" thô luôn đẻ âm giả khi số trang thay đổi.** 999 cặp overlap nhưng **100% có `oy = 2.6pt`** (đúng line spacing) và `0` cặp `oy > 8pt` ở cả baseline lẫn bản mới. Chuẩn hóa theo trang thì giảm (24.11 → 16.38). Quy tắc: so **phân phối `oy`** và **mật độ/trang**, không so tổng.
6. **Chữ nhỏ phải đọc nội dung + so tập cỡ chữ với baseline.** 976 span `<8.5pt` nhưng toàn bộ là `NotoSansMono` (inline code `p_vio`, `δ`, `CI`), tập cỡ chữ **giống hệt** baseline `[8.3, 8.4]`, mật độ giảm 31.81 → 16.00/trang. Không sinh cỡ chữ mới = không phải lỗi.
7. **Regex "dòng có cả ASCII lẫn dấu tiếng Việt" KHÔNG phát hiện được chữ dính nhau.** Nó báo 447 ca nhưng toàn bộ là tiếng Việt thuần chứa ASCII (`ERA5`, `CI`, `<venue-A>-PD`), và PDF text extraction **mất khoảng trắng** ở cả baseline (`BẢNG TỪ KHÓA` → `TỪKHÓA`). Muốn biết hai câu có dính không thì đo **tọa độ y**, không đọc chuỗi.
8. **Timestamp do người viết ước lượng trong speaker notes có thể tự mâu thuẫn.** Deck 19 slide: S13 ghi kết thúc `11:45` nhưng S14 ghi bắt đầu `11:40` (chồng lấn), cộng 4 khoảng trống 5–10s; notes tự khai kết thúc `17:40` nhưng đếm từ thật ra `19:24`. Khi làm tài liệu đồng hồ, **tính lại từ số từ @ wpm** và công khai cả hai.
9. **Kế hoạch cắt thời gian chỉ được bỏ nguyên câu, không "nói ngắn lại".** Mỗi dòng cắt ghi rõ số từ của cue đó → số giây tiết kiệm là phép chia thật (MỨC A: 12 cue/277 từ → `17:11`; MỨC B: 20 cue/559 từ → `14:56`). Và **không bao giờ cắt** các slide tự báo cáo chống lại chính mình (phạm vi định lý, kiểm định `p=0.36`, ablation) — đó là thứ mua niềm tin của cả bài.
10. **Dòng "Đã dùng" chỉ liệt kê tool đã gọi thật.** Đã ghi `vision_analyze` vào dòng đó trong khi chỉ gọi `terminal` — vi phạm quy tắc không bịa.

## Bài học phiên 2026-09-14 — BAI_02 polish (vision 503, NhómXX, \n lộ chữ)

Phiên này user soi 2 lỗi chặn phát hành trên BAI_02 retrofit và yêu cầu bổ sung kể chuyện bằng hình:

1. **Tiêu đề bìa lộ `\n` thô** — `add_text(cover, 'VAI TRÒ THIẾT BỊ\\nTHÔNG MINH & TIN HỌC', ...)` render thành chữ `\n` trên slide (literal `\\n` = 1, `pdftotext` hiện `VAI TRÒ THIẾT BỊ\\nTHÔNG MINH`). Sửa: tách thành 2 `add_text` riêng (`VAI TRÒ THIẾT BỊ` ở y=2.02 h=0.86 và `THÔNG MINH VÀ TIN HỌC` ở y=2.78 h=0.86), không nhúng `\n` trong một textbox. Quy tắc: không dùng `\n` trong `add_text`/`codebox` cho tiêu đề bìa; tách dòng bằng 2 shape.
2. **Mã nhóm thuộc tài liệu giao nhiệm vụ, không thuộc slide kiến thức.** Cách vá cũ bằng cách thêm ví dụ `B2_Nhóm03` vào bìa, yêu cầu và kết bài đã bị giáo viên bác bỏ. Với bộ slide chỉ truyền tải kiến thức, bỏ mã nhóm và quy tắc nộp sản phẩm khỏi bề mặt; giữ định danh nguồn trong hồ sơ truy vết riêng. Chỉ giải thích mẫu mã nhóm trong tài liệu bài tập khi giáo viên yêu cầu tài liệu đó. Không biến nhiệm vụ thành “ví dụ gợi ý” để giữ nguyên nội dung giao việc.
3. **Kể chuyện bằng hình, không chỉ bảng chữ** — user yêu cầu `dùng vision + ppt-master để hoàn thiện, bổ sung nhiều hình ảnh, dùng hình để kể chuyện`. Khi `vision_analyze` 503 (`model is disabled: gpt-5.6-luna`) và `image_generate` 503 (`omniproxy`), không lặp lại lời gọi quá 1 lần và không bỏ gate trực quan: thay bằng `ink_clip_check.py` + kiểm chồng lấn + quét PDF text + so baseline deck đạt trước. Ảnh kể chuyện lấy từ `ppt-master/templates/icons` (12.027 SVG) raster qua `cairosvg` → `add_picture`; ví dụ BAI_02: `device-watch`/`device-cctv`/`device-speaker` cho 3 TB, `factory`/`cloud-data-connection` cho CMCN 4.0.
4. **Rà từng câu bằng `academic-prose`** — user chỉ định `Dùng academic-prose coi từng câu từng chữ`. Trước khi dựng lại, chạy gate `academic-prose` cho mọi label/câu trên slide và speaker notes (đủ chủ ngữ, đúng thuật ngữ `thiết bị thông minh / vào–xử lí–ra`, bỏ nhãn sản xuất).
5. **Gửi đúng thread Discord** — 2 lần gửi nhầm kênh gốc `discord:1545388750916292610` thay vì thread `SOẠN SLIDE BÀI GIẢNG TIN HỌC 10` (`discord:1545388750916292610:1548004414881660929`). Khi gửi file PPTX/PDF phải chỉ định `target` đủ `chat_id:thread_id`; bare platform `telegram`/`discord` sẽ rơi ra kênh gốc.