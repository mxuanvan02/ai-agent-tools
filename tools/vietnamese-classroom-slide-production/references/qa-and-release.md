# QA và phát hành

## Fingerprint nguồn

Trước khi sửa, ghi lại: đường dẫn/tên file, SHA-256 hoặc kích thước, số slide, tỉ lệ trang, tiêu đề bìa và chuỗi đại diện ở vài slide. Nếu có nhiều file gần tên, không tự chọn theo suy đoán.

## Cổng cấu trúc

Kiểm tra trên file PPTX cuối:

- ZIP/OOXML hợp lệ; đúng tỉ lệ 16:9.
- Số slide đúng bản đồ bài học.
- Notes không rỗng trên mọi slide nội dung.
- Không có shape vượt biên, placeholder, chuỗi `\\n`, chữ rác hoặc nội dung từ bài khác.
- Không có nhãn/cụm bị cấm; dấu hỏi chỉ nằm ở phần bài tập được phép.

## Cổng hình ảnh

1. Xuất PDF từ PPTX cuối và đối chiếu số trang.
2. Render toàn bộ slide thành ảnh; tạo contact sheet.
3. Xem riêng slide dày nhất, ví dụ mới, bảng/biểu đồ và slide có chữ nhỏ.
4. Phân loại: P0 = chồng/cắt/mất chữ; P1 = khó đọc, tương phản thấp, ngắt dòng hoặc phân cấp sai.
5. Sửa nguyên nhân, dựng lại PPTX/PDF và kiểm tra lại. Không phát hành khi còn P0/P1.

## Quy ước tên phát hành

Dùng tên ổn định, không chứa trạng thái nội bộ như `LAM_LAI`, `FINAL`, `NEW`:

- PPTX: `BAI_XX_<TEN_BAI_KHONG_DAU>.pptx`
- PDF đối chiếu: `BAI_XX_<TEN_BAI_KHONG_DAU>.pdf`

Giữ số bài hai chữ số nếu cả thư mục dùng chuẩn đó; nếu thư mục hiện hành có quy ước khác, ưu tiên tính nhất quán của toàn bộ thư mục.

## Cập nhật Drive an toàn

- Liệt kê đúng thư mục và nhận diện file cũ bằng tên, kích thước, thời gian sửa.
- Tải bản mới lên tên tạm hoặc thư mục staging trước khi thay thế nếu backend không hỗ trợ versioning rõ ràng.
- Giữ một bản phục hồi có timestamp hoặc dựa vào Trash/version history; không xóa vĩnh viễn.
- Sau upload, đọc lại metadata/kích thước và so sánh với file local.
- Chỉ báo thành công khi file đích tồn tại và kiểm tra đọc lại đạt yêu cầu.

## Báo cáo theo lô

Với bộ nhiều bài, báo cáo ngắn theo bảng: bài, nguồn, số slide, notes, QA, tên Drive, trạng thái. Không tuyên bố “đã làm hết” khi chỉ mới tạo script hoặc bản dựng trung gian.


## Đo lỗi trình bày: đọc XML, đừng đọc text

- **`python-pptx .text` KHÔNG chứa bullet tự sinh.** Dấu `buChar`/`buAutoNum` nằm ở `pPr`, không nằm trong run, nên tìm chuỗi `"• •"` trong `paragraph.text` luôn ra 0 hit. Đã vì thế mà kết luận SAI một lỗi có thật: 40 đoạn trên 4 deck vừa khai `<a:buChar char="•"/>` vừa có text bắt đầu bằng `•` → PowerPoint vẽ HAI dấu. Muốn biết màn hình vẽ mấy dấu thì đọc XML của `pPr`, và xác nhận lại bằng vision trên ảnh zoom.
- **Sửa bullet lặp: bỏ dấu GÕ THỪA trong text, giữ `buChar`.** `buChar` mang màu/cỡ/font của template (`buClr`/`buSzTx`/`buFontTx`); xoá nó sẽ làm bullet mất style và lệch với các bullet khác trong cùng deck.
- **Lệch bullet trong PDF có thể là artifact của renderer, không phải lỗi deck.** Artifact để dạy là `.pptx` mở bằng PowerPoint, còn ảnh ta đo là PDF do `soffice` render. Tách cho rõ bằng thí nghiệm có đối chứng: dựng pptx tối thiểu với các textbox có `left/marL/indent/buChar` GIỐNG HỆT, chỉ khác độ dài chữ, rồi render và đo toạ độ glyph bằng `fitz`. Nếu bản đối chứng cũng lệch (đã đo: 5.24pt, cùng cỡ 3.36pt trên deck thật) thì đó là cách LibreOffice render hanging indent — **không "sửa" geometry vốn đúng**.

## Guard phải chặn đúng thứ thật, không chặn proxy tự chế

- Guard "số từ mỗi slide không được tăng" từng CHẶN OAN một sửa đổi đúng: slide đó đã vượt ngưỡng sẵn nên thêm 3–5 từ không làm slide nào **mới** vượt. Tiêu chí đúng: **số slide vượt ngưỡng không được tăng**. Còn rủi ro thật (tràn chữ đè ảnh) thì chặn theo từng đoạn ("bản mới không dài hơn bản cũ + 2 kí tự", vì shape có width cố định) và để cổng `ink_clip_check` trên PDF đã render phán xử — cổng đó đo va chạm thật, không phải proxy.
- **Đọc chữ ký hàm trước khi dùng nó làm guard.** `measure_path()` trả `(size, ncols, hits)`; unpack thành `sev, ncols, hits` rồi kiểm `if sev:` là kiểm **size** — tuple luôn truthy nên guard FAIL oan dù `hits=[]` (0 vết cắt). In kèm giá trị thô vào log là cách phát hiện loại lỗi này ngay.
- **Đừng dựng lát cắt từ hiệu hai toạ độ rồi giả định nó khác rỗng.** Cắt dải "khoảng trống giữa hai band" với `start = mốc_trên + cao_band + 2`, `stop = mốc_dưới - 2` cho slice RỖNG khi band cao hơn khoảng cách giữa hai mốc → `np.median([])` trả NaN → `ValueError`. Cách bền: lấy median của pixel **không-mực** trong toàn nội dung, kèm guard kiểm số pixel tối thiểu.
- **Phát hiện vạch chia dọc phải bỏ viền ngoài.** Quét cột xám chạy suốt trên toàn chiều rộng sẽ bắt luôn viền khung (cột 0 và W-1 cũng thoả) → khoảng chia thành rỗng → "0 band". Chỉ quét trong vùng nội dung, gom cụm, loại cụm quá rộng và cụm dính mép, chọn cụm hẹp gần tâm nhất.
- **Thêm guard bảo toàn mực khi dịch/chuyển nội dung ảnh:** tổng số pixel mực trước và sau phải bằng nhau từng pixel (đã dùng: 54343 → 54343). Kèm guard dải định cắt phải 0 pixel mực. Hai guard này bắt được glyph gãy mà mắt thường dễ bỏ qua.

## Cổng kết luận "đã đồng bộ" phải so với server, không so với clone local

- Một script verify so `~/.hermes/skills/...` với `~/ai-agent-tools/...` (clone **local**) và chỉ quét những file có sẵn trong thư mục references sẽ kết luận "KHÔNG cần mở PR" ngay cả khi base branch trên server chưa có nội dung mới. Phép thử quyết định: `git show origin/<base>:<đường dẫn>` có chứa luật mới không, và `git ls-tree origin/<base> <thư mục>` có file mới không.
- **`gh` cài bằng snap bị confine: không đọc được `<data>`.** Chạy `gh pr create` từ worktree trên đĩa đó ra `fatal: error opening '.../.git': Permission denied`. Cách đúng: chạy `gh` từ clone trong `$HOME` và đặt file body PR trong `$HOME` (`/tmp` cũng không đọc được). Nếu vẫn kẹt, fallback `gh api repos/<owner>/<repo>/pulls -X POST -F body=@/home/<user>/file.md` không cần git.
- **Exit code của pipeline là exit code của LỆNH CUỐI.** `gh pr create ... | tail -5; echo $?` trả 0 dù lệnh create fail. Luôn verify bằng một lệnh đọc độc lập: `gh pr list --head <branch> --state all --json number,state,url`.


## Đo "chữ có tràn không": ba tiêu chí SAI đã dùng và tiêu chí đúng

Cả ba bản probe đầu đều kết luận sai vì đo nhầm đại lượng. Bài học chung: **tiêu chí phải
là va chạm thật mà người xem thấy, không phải quan hệ giữa chữ và cái hộp vô hình.**

- **SAI 1: "mực chạm đáy khung = tràn".** Với `autofit=spAutoFit`, PowerPoint TỰ CO
  chiều cao khung đúng bằng chiều chữ nên mực LUÔN gần chạm đáy (đo thật: ink_bot=127
  trong box 128px) kể cả khi chữ hoàn toàn ổn. Tiêu chí này luôn đỏ -> vô dụng.
- **SAI 2: crop theo chiều dọc của khung nhưng lấy NGUYÊN CHIỀU RỘNG ảnh** (`band[:, :]`)
  rồi kết luận "đâm logo". Thứ bắt được là LOGO trường ở góc phải (left 11.89in), không
  phải chữ tiêu đề. Dấu hiệu nhận biết: hai bản tiêu đề KHÁC độ dài (46 vs 41 kí tự) mà
  cho số đo GIỐNG HỆT nhau (1884px = 12.56in) ở cả 4 ca. Khi hai mẫu khác nhau cho cùng
  một con số, thứ đang đo không phải thứ đang so sánh.
- **SAI 3: self-test "tiêu đề dài hơn thì mép mực phải xa hơn".** Sai với font tỉ lệ:
  bản 45 kí tự kết thúc `...bậc 2` đo được 10.03in, bản 44 kí tự kết thúc `...bậc…` đo
  được 10.05in — glyph `…` rộng ~1em còn ` 2` (space + chữ số) chỉ ~0.5em, nên bản NGẮN
  HƠN lại RỘNG HƠN. Self-test kiểu này báo oan cho probe đúng.
- **SAI 4: coi "tràn khỏi mép khung" là lỗi.** Khung có `wrap=none` thì chữ tràn khỏi hộp
  là hành vi BÌNH THƯỜNG của PowerPoint, không phải defect. Chỉ va chạm thật mới là lỗi.
- **ĐÚNG: đo mực trong đúng vùng chữ** `x = [title.left, logo_left)` (cắt bớt vùng logo),
  rồi so với mốc nhìn thấy được: cách logo >= 0.10in, cách mép slide >= 0.05in. Self-test
  phải KHÔNG phụ thuộc độ rộng glyph: (a) mép TRÁI mực sát `left` của khung (chứng minh
  đang đo chữ tiêu đề chứ không phải logo); (b) băng chữ cao 25-60pt = đúng một dòng ở
  cỡ 30pt. Đo được: 4/4 tiêu đề đầy đủ cách logo 1.62-2.31in, cách mép slide 3.07-3.76in.
- **Chuyển đổi đơn vị:** sau khi chia EMU để ra inch thì `pixel = inch * DPI`. Viết
  `scale = DPI/EMU` (=0.000164) là chia đôi đơn vị -> vùng crop rỗng -> "không thấy mực".

## Phát hành: verify bằng MD5 phía server, và kiểm cổng trên ĐÚNG nhánh artifact

- **`rclone check --checksum` so MD5 phía Google Drive nên KHÔNG cần tải file về.** Đã tải
  ngược 34 deck (~30MB) chỉ để so sha256 và bị timeout — chọn sai cách. Cẩn thận: flag
  `--files-only` KHÔNG tồn tại trong rclone 1.75.1, rclone in help và trả rc=2; nếu đọc
  rc mà không đọc output thì sẽ báo "VERIFY FAIL — Drive không khớp" oan. Cờ đỏ rc=2 kèm
  output là bảng help = lỗi cú pháp lệnh, KHÔNG phải kết quả so sánh.
- **Khi có nhiều nhánh artifact song song, phải chạy MỌI CỔNG trên đúng nhánh sắp phát
  hành.** Đã sửa bullet trên bản tải từ Drive (`full_scan_drive/`) rồi upload, trong khi
  sửa code trên `bai_*_anhthat/`; đo lại mới thấy nhánh sắp upload vẫn còn 116 chỗ bullet
  lặp. Upload ngay lúc đó sẽ ĐÈ MẤT fix đã có trên Drive, tức lùi artifact về trạng thái cũ.
- **Tổng đếm nội bộ của script không phải bằng chứng.** Script sửa báo "Hoàn thành! Đã sửa
  38 chỗ" trong khi danh sách EDITS đã bị rơi mất 12 chỗ của 4 deck (do viết lại file).
  Phải QUÉT LẠI artifact sau khi sửa và so với danh sách vi phạm ban đầu.
- **Script sửa phải IDEMPOTENT.** Khi một vòng chạy bị guard chặn giữa chừng, các deck
  trước đó đã lưu rồi; chạy lại sẽ FAIL oan vì "không tìm thấy text cũ". Cách xử lý: nếu
  prefix cũ không còn thì kiểm tra bản MỚI đã có mặt chưa — có thì bỏ qua, không thì FAIL thật.
- **Dương tính giả của detector code-invalid:** câu văn xuôi `"Gợi ý: diem_1, diem_tb;
  class là từ khoá nên phải đổi thành lop hoặc _class."` bị bắt vì prefix `diem_1, diem_tb`
  parse được như một tuple. Trước khi sửa phải ĐỌC câu đó: nó khuyên học sinh đổi tên
  biến, dấu `;` là ngắt câu tiếng Việt. Sửa sẽ phá nội dung bài.
- **Text trong slide có thể mang prefix bullet `• ` trong khi `paragraph.text` của lần đo
  trước không có** (do vòng trước đã xoá `•` gõ thừa nhưng buChar vẫn vẽ dấu). Khớp text
  để sửa phải thử CẢ hai dạng, và phải tìm shape ĐỆ QUY qua GROUP (shape_id nằm trong
  group con, không thấy ở top-level).
