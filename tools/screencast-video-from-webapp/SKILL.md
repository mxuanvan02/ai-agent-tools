---
name: screencast-video-from-webapp
description: Use when recording a demo video from a web app headlessly.
---

# Screencast video from a web app (headless Linux) + false-instrument playbook

Áp dụng khi: quay video demo từ web app chạy local/file:// trên máy Linux không có màn hình thật;
hoặc rộng hơn — khi một phép đo/cổng kiểm báo kết quả MÂU THUẪN với chỉnh sửa vừa làm (nửa B).
Đúc kết từ một lượt dựng thật: video 4:40 nộp hồ sơ, quay app offline qua CDP screencast.

## A. Pipeline quay video từ web app

### A1. Chọn screencast của trang, KHÔNG quay cả màn hình X
- Quay bằng CDP `Page.startScreencast` (format jpeg, quality ~90, everyNthFrame 1). Lệnh này bắt
  surface CỦA TRANG nên về cấu trúc không thể dính UI trình duyệt.
- `ffmpeg x11grab` trên Xvfb KHÔNG có window manager thì Chrome tự vẽ khung của nó: đã đo được màu
  khung chiếm 4,7–6,5% khung hình; cờ `--app=` chỉ giảm từ 144px xuống 57px chứ không xoá được.
  Kết luận phải dựa trên số đo: `window.innerHeight` so với chiều cao màn hình X, và % pixel ngoài
  bảng màu app.
- `Page.captureScreenshot` chỉ chụp viewport — ảnh still từ nó KHÔNG chứng minh được khung quay
  x11grab sạch. Kiểm đúng công nghệ sẽ dùng để xuất bản.

### A2. Client CDP: MỘT vòng đọc duy nhất
Hai coroutine cùng gọi `ws.recv()` → `ConcurrencyError`. Kiến trúc đúng:
- một task `_doc_vong()` đọc socket, rẽ nhánh: có `id` → set_result cho future của lệnh; có
  `method` → đẩy vào hàng đợi sự kiện.
- `cmd()` await future, không tự recv. ACK khung screencast bằng send-one-way
  (`Page.screencastFrameAck`) — không ACK thì Chrome dừng gửi, ta sẽ tưởng "screencast chỉ ra vài
  khung".
- `Page.addScriptToEvaluateOnNewDocument` override `window.confirm/alert` TRƯỚC khi reload: hộp
  thoại native trong Xvfb không ai bấm sẽ treo trang đúng giữa lúc quay.

### A3. Tiến trình: zombie là kẻ thù số một
Đã gặp thật ba lần cùng một gốc: Xvfb/Chrome lượt trước chết không được dọn → giữ display/cổng →
lượt sau fail với triệu chứng gây nhầm (`bind() failed: Address already in use` rồi Chrome rơi
xuống `ws://[::1]`; `/json` trả `[ ]` từ một Chrome zombie).
Quy tắc:
- display/port/profile PHÂN GIẢI THEO PID và TÌM CHỖ TRỐNG (bỏ qua display có socket
  `/tmp/.X11-unix/XNN`; lock mồ côi — lock còn mà PID đã chết — thì dọn).
- mọi khởi động subprocess nằm TRONG try/finally; `finally` terminate cả Chrome lẫn Xvfb.
  Lỗi thật: SystemExit nổ giữa hàm khởi động khi nó còn NGOÀI try → finally không chạy → zombie.
- pkill theo pattern đặc thù của chính phiên (`user-data-dir=<profile-của-mình>`) — cẩn thận:
  `pkill -f <pattern>` TỰ KHỚP command line của shell đang chạy nó → tự SIGTERM. Chẩn đoán bằng
  `pgrep` qua execute_code, không pkill mù; KHÔNG đụng Xvfb/Chrome của phiên khác (browser-use).
- khi ABORT phải IN bằng chứng: tiến trình sống/chết + mã thoát + nội dung thô `/json` + stderr.
  Thông báo ABORT nghèo thông tin sẽ buộc viết thêm một script chẩn đoán riêng.

### A4. Screencast chỉ gửi khung khi trang ĐỔI
Hệ quả đã gặp thật: shot nhắm 20s chỉ thu 19 khung/6,9s vì đoạn cuối tĩnh (tem phản hồi giữ nguyên).
- encode phải resample về lưới fps cố định THEO TIMESTAMP của khung, và **hold khung cuối tới đúng
  thời lượng nhắm** (`target_dur`), nếu không video cụt đúng đoạn hold.
- ghi khung XUỐNG ĐĨA ngay khi nhận, chỉ giữ (ts, path) trong RAM: shot 95s × 60fps × ~70KB ≈
  380MB nếu giữ bytes trong danh sách.
- fps đo được khi có hoạt hình: ~60; span hoạt động < target là BÌNH THƯỜNG, không phải lỗi.
- kiểm screencast có bắt chuyển động thật không: hash hai khung cách nhau vài giây phải KHÁC.

### A5. Aspect ratio lệch: scale + pad, KHÔNG stretch
Quay 1279×800 (16:10) lên đích 1920×1080 (16:9): stretch kéo dãn chữ ngang ~11%.
- `scale=-2:<H>,pad=<W>:<H>:(ow-iw)/2:0:color=<màu nền app>` — pad trùng màu nền thì vô hình.
- libx264 từ chối kích thước lẻ ("width not divisible by 2"): viewport 1279 thì pad sang 1280,
  không scale 1279→1280 (dãn chữ).
- CHỨNG MINH không méo bằng hai phép độc lập, đừng tin một phép:
  1. crop-and-compare: cắt dải giữa bản ghép theo giả thuyết giữ-tỉ-lệ, resize về kích thước thô,
     so từng pixel — lệch phải nhỏ hơn HẲN giả thuyết stretch (đã đo: 1,23 so với 4,96 /255).
  2. biên một thanh màu KHÁC nền (header trắng): rộng phải = bề ngang nội dung mong đợi ±vài px.
- viewport hụt vài px so với window-size là thường (1279 thay vì 1280); Xvfb phải CAO HƠN viewport
  đúng bằng phần khung Chrome còn lại (800+57=857) để innerHeight đạt đúng 800.

### A6. Framing: đo toạ độ + xác nhận kín vòng lặp
- KHÔNG để helper click gọi `scrollIntoView` — nó cuộn trang tới vị trí tuỳ tiện, phá framing.
  Bấm bằng `dispatchEvent(new MouseEvent('click',{bubbles:true}))`, cuộn do hàm khung quyết định.
- hàm khung: `getBoundingClientRect` của các khối cần thấy → trừ chiều cao HEADER DÍNH (sticky/fixed,
  đo thật — đã gặp 49px che khuất nội dung dù toạ độ tài liệu đúng) → cuộn `behavior:'instant'`
  → ĐO LẠI toạ độ màn hình và xác nhận từng khối trong vùng nhìn thấy; chưa đạt thì tịnh tiến tiếp
  (tối đa 2 vòng). Log in dòng XÁC NHẬN cho từng khoảnh khắc — bằng chứng framing nằm trong log.
- nội dung cao hơn viewport thì chia khoảnh khắc, mỗi khoảnh khắc một khung tĩnh (crop tĩnh được
  phép; pan/zoom animation thì không — zoom làm mờ chữ có dấu).
- nút toggle trạng thái: bấm NÚT THẬT rồi kiểm bằng DOM (`body.classList`), đừng gọi setter nội bộ
  rồi đọc getter — đã gặp setter không gán biến nội bộ nên getter báo sai dù hiệu ứng đã áp dụng.

### A7. Verify video bằng ba lớp, lớp nào cũng cần
1. `ffprobe`: độ phân giải/fps/codec/pix_fmt/duration — cần nhưng KHÔNG đủ (video đen/đơ/sai
   framing vẫn đạt hết).
2. xem khung thật bằng vision tại ranh giới shot và khoảnh khắc chính — hỏi cụ thể: có UI trình
   duyệt không, chữ bị cắt không, đúng cảnh không. Vision timeout/lỗi server liên tiếp (2 lần) thì
   chuyển sang đo hình học bằng pixel (A5), không suy diễn và không thử lại vô hạn.
3. số liệu đọc từ nội dung trên màn hình phải đối chiếu nguồn dữ liệu — spec/brief khai số khác số
   đo thật thì dùng số đo thật và khai rõ độ lệch (đã gặp: brief nói "50% và 90%", đo thật 57%/90%
   vì 50% là dự đoán của người dùng chứ không phải kết quả mô hình).

### A8. Lời bình và phụ đề
- Lời bình viết như VĂN NÓI (sẽ được đọc lên): chạy qua cổng văn phong của dự án nếu có; hai lỗi
  kinh điển là dấu hai chấm kiểu tiêu đề và động từ "chứng minh" — sửa TẠI NGUỒN sinh để lần chạy
  sau không tái phạm.
- Kiểm văn phong trên ĐÚNG tệp sẽ đọc (phụ đề .srt đã tách timestamp), không kiểm file .md kèm
  header — header markdown sẽ góp lỗi giả vào phép đo.
- Phụ đề để file .srt rời, không burn-in (sửa chính tả không cần render lại).
- Timing phụ đề ước tính ~2,7 từ/giây cho tiếng Việt.

## B. Playbook instrument-sai (lớp lỗi tốn giờ nhất)

Bốn ca thật trong cùng một dự án, cùng một hình dạng: **công cụ đo in ra con số trông như đã kiểm
chứng, trong khi phép đo hỏng.**
1. cổng đo cue "đáp án dài nhất" dùng regex chỉ hiểu chuỗi nguyên khối, không hiểu chuỗi nối nhiều
   dòng (`"a " + "b"`) → sửa nội dung mà số đứng yên (đo mù). Chữa: parse từng đoạn chuỗi theo biên
   dấu nháy rồi `ast.literal_eval`; KHÔNG xoá dấu `+` bằng regex (sẽ xoá nhầm dấu cộng nằm TRONG
   nội dung chuỗi, tạo phép đo mù mới và lần này im lặng).
2. bộ lọc log-site đòi object ở tham số thứ nhất trong khi lời gọi thật truyền nó ở tham số thứ hai
   → loại sạch 100% site rồi VẪN ghi JSON số rác ra hồ sơ. Chữa: chặn cứng — số site < ngưỡng hợp lý
   thì KHÔNG ghi output.
3. hàm kiểm patch quên tăng biến đếm → in "0 patch đã ghi" trong khi 11 patch đã ghi thật (suýt vá
   lại việc đã xong). Chữa: kiểm trạng thái ĐĨA sau khi vá (grep thứ đã thay), không tin lời in.
4. detector tìm biên nội dung bằng màu pad, mà pad trùng màu nền (chủ ý, để vô hình) → quét xuyên
   qua cả hai, báo oan 6 lỗi, trong đó 2 "lỗi" trên ảnh full-bleed về cấu trúc không thể có pad.

Quy tắc rút ra:
- **Số đo không nhúc nhích sau khi dữ liệu đổi = phép đo mù.** Đối chiếu số đo với diff vừa làm là
  phép thử rẻ nhất. Đừng sửa nội dung thêm nữa trước khi phân xử instrument.
- **Corroborate mọi FAIL bằng artifact verbatim trước khi sửa** — chiều ngược lại cũng đúng: cổng
  chỉ biết FAIL một chiều (bắt oan) sẽ bị người đọc bỏ qua luôn cả phần đúng. Ca 4 bị lật tẩy nhờ
  ca đối chứng bất khả thi (ảnh native full-bleed không thể có pad). Khi thiết kế detector, kèm một
  positive control PHẢI-bị-bắt và một negative control KHÔNG-thể-bị-bắt.
- **Instrument phải tự kiểm**: parse hụt/không khớp khuôn thì FAIL và nói rõ "phép đo mù, đừng tin
  con số", thay vì in tỉ lệ đo thiếu. Thà đỏ đúng còn hơn xanh trên phép đo sai.
- **Đo bằng lệnh, không tính nhẩm**: kỳ vọng test viết tay từ trí nhớ đã sai 2/7 ca (viết 45/6,
  thật 47/5); oracle độc lập là `len()`/hash/thống kê thật.
- **Danh sách stale/lỗi phải đếm ĐẦY ĐỦ** (không `head`): head -8 từng cắt mất chỗ stale thật; và
  phân loại TỪNG chỗ trước khi vá — chuỗi cùng hình dạng có thể là hiện trạng (phải sửa) hoặc bản
  ghi lịch sử có mốc ngày (GIỮ NGUYÊN — sửa kết quả đo cũ là làm giả bằng chứng).
- **Hash/commit hash trong tài liệu phải giữ đúng cặp backtick** nếu cổng bắt hash bằng regex có
  backtick — thay hash mà làm rơi backtick là vô hiệu hoá cổng trong im lặng (cổng mù nguy hiểm hơn
  cổng kêu oan vì không ai biết mà nghi ngờ).

## C. Bẫy thi hành chung (mỗi cái đã trả giá ít nhất một lần)
- `RC=$?` sau pipe là exit code của LỆNH CUỐI (tail/head), không phải của script. Muốn RC thật:
  chạy ra file rồi đọc, hoặc không pipe.
- vá chuỗi: patch chèn-khối-lớn phải đi CUỐI, hoặc mốc của patch sau không nằm trong vùng patch
  trước thay thế (lỗi thật: patch trước nuốt mất `function X(){` mà patch sau dùng làm mốc). Mốc
  phải đếm `count()==1` trước khi thay; mốc không duy nhất (4 lần `pipe3dHud();`) thì tìm mốc dài
  hơn và đếm lại bằng Python. Anchor có escape/docstring dễ trượt — trượt lần hai thì thay THEO
  KHOẢNG vị trí (find index A→B), hoặc viết lại cả khối sạch.
- chèn hàm vào giữa một hàm khác có thể đẩy các dòng khởi tạo xuống SAU một lệnh raise/return →
  code chết hợp lệ cú pháp (ast.parse không bắt). Kiểm bằng CÁCH CHẠY THẬT (instantiate + đọc
  thuộc tính), không chỉ parse.
- kiểm tra import của TỆP ĐÍCH trước khi dùng: `io`/`ast` thường được import cục bộ trong một hàm
  khác (`import ast as _ast` bên trong hàm g18) → gọi từ hàm của mình là NameError. except hẹp:
  `except (OSError, SubprocessError)` — `except Exception` nuốt NameError của chính mã cổng rồi đổ
  cho node/chrome, làm sai hướng sửa.
- lồng chuỗi ba dấu nháy trong chuỗi ba dấu nháy (`'''` trong `'''`) sẽ đóng sớm chuỗi ngoài →
  SyntaxError ở chỗ khó ngờ (ký tự lạ trong phần code bị hiểu nhầm). Dùng lẫn `"""` và `'''` có ý
  thức, hoặc đọc lại nguyên văn bằng repr() trước khi vá.
- two-strike rule: cùng một file/hướng fail 2 lần thì ngừng vá anchor, viết lại sạch (file ngắn
  hơn, không anchor, điều kiện đủ lấy từ ca đã chứng minh — vd diag script chạy được thì chép đúng
  bộ cờ đó).
- file tạm và bản sao lưu (`_backups/`) để NGOÀI repo: bản sao trong repo từng bị `git add -A`
  cuốn vào commit, làm tool đếm dòng mã phồng +2.435 dòng (tool đếm từ `git ls-files`) sắp in vào
  hồ sơ nộp. Ba lớp chặn: gitignore + phép đếm tự loại bản sao + cảnh báo nếu bản sao còn trong git.
- media lớn không vào git khi bản chính thức nộp bằng link/Drive: mỗi lần render lại là ghim vĩnh
  viễn dung lượng vào history (không xoá được bằng cách xoá tệp). Ignore theo pattern + mở đúng
  một ngoại lệ cho tên bản chính thức (`!path/ban_chinh_thuc.mp4`).
- đường dẫn trong tool tái lập: suy ra repo từ `__file__`, đọc env override, `shutil.which` cho
  binary, có `bao_cao()` in đường dẫn đang dùng vào log. Tài liệu hứa "dựng lại được" mà trỏ
  `/tmp/...` là lời hứa rỗng — cổng bắt đường dẫn hardcode của chính dự án sẽ đánh trượt nó.
- quét hardcode phải bỏ docstring/comment (dùng AST) kẻo báo oan ghi chú lịch sử hợp lệ.
- bản copy của app để quay: chép sang thư mục cách ly (js/css/data/vendor/index.html), quay trên
  bản sao — Chrome profile/screencast có thể sinh tệp rác vào thư mục sản phẩm nằm trong manifest
  hash, làm lệch cổng kiểm toàn vẹn.
