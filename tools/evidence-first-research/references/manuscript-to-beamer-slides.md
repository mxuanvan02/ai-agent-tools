# Soạn slide Beamer trình bày từ manuscript (dùng template viện/trường)

Khi người dùng gửi một file template `.tex` (Beamer) và nói "soạn slide trình bày
về nội dung manuscript, ngắn gọn, ít chữ nhiều hình, có toán + giải thích, sắp
đúng thứ tự". Đây là EXECUTE: tái dùng template, thay nội dung bằng manuscript,
build sạch + verify render. Quy trình đã chạy thật (deck 21 trang, build 0 lỗi).

## 0. Giải nén + đọc template TRƯỚC khi soạn
- Template thường chỉ là 1 file `.tex`; **logo/asset (univ-logo.pdf, Khoa CNTT.pdf...) hay
  THIẾU trong zip**. Kiểm `find <dir> -iname '*logo*' -o -iname '*.pdf' -o -iname '*.png'`.
- Đọc full template để học: theme (`\useinnertheme`), palette màu thương hiệu
  (`\definecolor{HOEITBlue}...`), `headline`/`frametitle` tùy chỉnh, recurring TOC
  (`\AtBeginSection`), cấu trúc bìa + slide cảm ơn. GIỮ NGUYÊN các thứ này.

## 1. Logo-fallback pattern (build không vỡ khi thiếu asset)
Đừng để `\includegraphics{univ-logo}` làm build chết khi thiếu file. Định nghĩa macro
fallback hiện text khi không có file:
```latex
\newcommand{\logoDHH}[1]{\IfFileExists{univ-logo.pdf}{\includegraphics[height=#1,keepaspectratio]{univ-logo}}%
  {\IfFileExists{univ-logo.png}{\includegraphics[height=#1,keepaspectratio]{univ-logo}}%
  {\textcolor{HOEITBlue}{\textbf{\small ĐH HUẾ}}}}}
```
Dùng `\logoDHH{0.6cm}` ở headline + bìa + slide cảm ơn. Báo người dùng: "khi có file
logo, copy vào thư mục deck rồi build lại, logo tự hiện, không cần sửa code."

## 2. Thứ tự slide cho một BÁO CÁO MANUSCRIPT (khác đề cương/proposal)
Mạch chuẩn, mỗi section là một `\section` để recurring TOC chạy:
1. **Bài toán & Động lực** — vấn đề + 3 thách thức (C1/C2/C3) nêu SỚM.
2. **Mô hình hệ thống** — toán nền (dynamics, channel, cost function), vì sao
   không dùng metric ngây thơ (MSE).
3. **Phương pháp đề xuất** — pipeline figure (full-width) + chỉ số/công thức
   chính, tách từng số hạng map 1-1 về 3 thách thức (tô màu theo C1/C2/C3).
4. **Phân tích lý thuyết** — lemma/theorem, mỗi cái kèm block "Kết luận" diễn giải.
5. **Kết quả thực nghiệm** — slide SETUP riêng ("cố định tham số TRƯỚC rồi mới
   chạy") + bảng/hình kết quả + so SoTA + câu chuyện regime.
6. **Kết luận** — 4 ý gọn.
Map 3-thách-thức-sớm → 3-số-hạng-chỉ-số là "xương sống" giữ mạch xuyên suốt.

## 3. Preference trình bày của người dùng (ÍT CHỮ, NHIỀU HÌNH/TOÁN)
- Mỗi slide toán PHẢI có 1 dòng **"Đọc công thức"** giải thích bằng lời thường
  (vd chỉ số I_i: "ưu tiên node vừa sát ngưỡng, vừa kênh tốt, vừa không bị bỏ quên").
- Lemma/Theorem luôn kèm `alertblock`/`block` "Kết luận" diễn giải nghĩa, không để
  công thức trần.
- Dùng `columns` 2 cột (toán trái / diễn giải-hình phải), `block`/`alertblock` cho
  điểm nhấn, bảng `booktabs` gọn cho kết quả. Tô màu số hạng theo challenge.
- Số liệu LẤY TỪ manuscript đã verify (đừng retype sai): grep bảng kết quả trong
  `sections/04_evaluation.tex`, contributions trong `01_introduction.tex`, abstract.

## 3b. Tường minh hóa cho người NGHE chưa quen ký hiệu (người dùng tự nhận "mức chưa đủ")
Người dùng nhiều lần nói nội dung toán "đúng đắn nhưng khó hiểu", chưa nắm cả ký hiệu
cơ bản (dấu `$\sim$`, hàm `$\mathcal N$`, `$O(1/\sqrt N)$`, "per-arm"). Khi người dùng
nói "điều chỉnh slide tường minh dễ hiểu hơn" / "giải thích sơ qua mấy cái agent thêm":
- **Thêm một slide "Bảng ký hiệu nhanh" ngay sau mục lục**: bảng 2 cột
  `Ký hiệu | Đọc là / nghĩa`, giải nghĩa MỌI ký hiệu sẽ gặp bằng tiếng Việt thường
  (`$\sim$` = "phân phối theo", KHÔNG phải xấp xỉ; `$\mathcal N(\mu,\sigma^2)$` =
  phân phối chuẩn tâm μ độ rộng σ²; `$\overline\Phi$` = "độ nguy hiểm/xác suất vượt";
  per-arm = "riêng từng cảm biến"; `$O(1/\sqrt N)$` = sai lệch tới tối ưu nhỏ dần
  khi N tăng). Kèm 1 dòng trực giác cuối slide. Từ đó các slide sau cứ thế tra.
- **Mỗi slide toán đổi dòng "Đọc công thức" thành block "Đọc bằng lời"** giải nghĩa
  TỪNG ký hiệu trong công thức + ý nghĩa trực giác, không chỉ một câu tóm. Vd
  `$O(1/\sqrt N)$`: kèm bảng số trực quan (N=100→10%, 400→5%, 1000→3%) + câu
  "mạng càng đông càng tiệm cận tối ưu". Vd kênh: thêm câu "tự lành" nếu người dùng đã hỏi
  cơ chế đó (bỏ node vài vòng → niềm tin kéo về mức nền → node lại đáng gửi).
- Giải thích ký hiệu cho người dùng BẰNG LỜI trong chat trước (bảng glossary + ví dụ số),
  rồi mới đưa bản rút gọn vào slide — người dùng thường xác nhận hiểu rồi mới muốn sửa deck.
- Bài học: "tường minh" với MANUSCRIPT = đầy đủ toán + notation chuẩn; "tường minh"
  với SLIDE/giải thích cho người dùng = bớt toán nặng, thêm diễn giải lời, glossary. Hai
  nghĩa khác nhau, đừng nhồi notation nặng vào slide.

## 4. Tái dùng TikZ figure 2-cột của manuscript vào slide
- Copy `figures/fig_architecture.tex` sang thư mục deck; copy các PNG chủ lực
  (benchmark, theory_validation).
- Figure gốc thiết kế cho khổ 2 cột → bọc `\resizebox{0.98\textwidth}{!}{\input{...}}`
  để vừa slide 16:9. Bỏ caption thừa (slide có frametitle rồi).
- Cần đồng bộ palette: định nghĩa lại `\definecolor{vouBlue}...{chanGreen}` trong
  preamble deck (figure phụ thuộc các màu này).

## 5. VERIFY = build chain + render + vision (build sạch KHÔNG đủ)
- `pdflatex` chạy **≥2 lần** cho recurring TOC + `\tableofcontents` ổn định.
- Overfull ~1.39pt từ headline rule là vô hại — bỏ qua.
- **Render slide rủi ro cao (pipeline figure) ra PNG rồi vision-check**:
  `pdftoppm -png -r 110 deck.pdf /tmp/sl` → vision hỏi "figure vừa khung không, chữ
  có đè/cắt/quá nhỏ không". Recurring TOC ĐẨY SỐ TRANG → đừng đoán số trang figure,
  render hết rồi quét, hoặc vision-check vài trang quanh section đó.
- Pitfall đã gặp: figure 2-cột thu vào slide thì chữ nhỏ — phóng `resizebox` lên
  0.98 + bỏ caption; nếu vẫn nhỏ, cân nhắc vẽ figure rút gọn riêng cho slide.
- **Overfull `\vbox` (tràn dọc, slide quá cao)**: khi `\resizebox{0.98\textwidth}{!}{...}`
  một TikZ pipeline cao làm slide tràn ~20pt (grep `Overfull \vbox` trong log), đổi
  sang RÀNG BUỘC CHIỀU CAO: `\resizebox{!}{0.78\textheight}{\input{...}}`. Vẫn
  vision-check lại figure không méo/cắt sau khi đổi. Overfull vbox ~1.5pt còn lại
  là vô hại (do block nội dung), bỏ qua.

## 5b. Tách hình multi-panel của manuscript cho dễ đọc khi chiếu
Hình paper hay nhồi 6+ panel (2×3) — chiếu lên thì legend/tick quá nhỏ. Người dùng
hay nói \"tách ra cho dễ\". Cách đã chạy thật (PIL, không cần tái chạy matplotlib):
```python
from PIL import Image
im = Image.open(\"theory_validation.png\")   # vd 2705x1461, layout 2 hàng x 3 cột
W,H = im.size; cw,rh = W/3, H/2
for r in range(2):
  for c in range(3):
    im.crop((int(c*cw),int(r*rh),int((c+1)*cw),int((r+1)*rh))).save(f\"theory_panel_{'abcdef'[r*3+c]}.png\")
# ghép 2 panel chủ lực thành 1 hình ngang cho slide:
a=Image.open(\"theory_panel_a.png\"); cpanel=Image.open(\"theory_panel_c.png\")
combo=Image.new(\"RGB\",(a.width+cpanel.width,max(a.height,cpanel.height)),\"white\")
combo.paste(a,(0,0)); combo.paste(cpanel,(a.width,0)); combo.save(\"theory_ac_combo.png\")
```
- Grid-crop đều theo W/cols, H/rows thường đủ sạch (panel matplotlib có lề trục
  riêng nên không cắt mất nhãn) — NHƯNG vẫn vision-check combo trước khi nhúng:
  \"mỗi panel có đủ axis label + legend + curve, không bị cắt ở mép/biên giữa không?\"
- Chỉ chọn 1-2 panel ĐẮT GIÁ NHẤT cho slide (vd bounds-tightness + fairness-converge),
  không nhồi cả 6; phần còn lại để backup slide. Panel rời to gấp ~3 lần khi nhồi.

## 5c. Slide negative-result (spike thử ý tưởng thay thế)
Khi đã chạy spike một ý tưởng thay thế (vd AE+AoI thay VoU) và nó THUA, người dùng
thích đưa vào deck như negative result trung thực (reviewer Q1 đánh giá cao). Đặt
slide NGAY SAU phần \"câu chuyện regime\", TRƯỚC Kết luận, để mạch logic:
*method thắng SoTA → thử thay bằng X → thua → củng cố vì sao thành phần lõi không
thể thay thế*. Layout: bảng số ×baseline (Intel/KETI) trái + `alertblock` \"Vì sao
thua (khớp Lemma)\" phải, dòng đáy in nghiêng chốt \"kết quả củng cố luận điểm bài\".
Số LẤY TỪ spike đã chạy thật, không bịa.

## 5d. Khử-English: giọng Việt hàn lâm tự nhiên (người dùng correction lặp lại)
Người dùng nhiều lần chê deck \"còn cảm giác English quá\", \"hạn chế text\", \"câu chữ
tự nhiên hơn, hàn lâm hơn\". Đây là PREFERENCE cứng — soạn slide xong PHẢI rà một
lượt khử thuật ngữ Người dùng lẫn lộn và dịch-máy. Quy tắc đã chạy thật:
- **DỊCH sang tiếng Việt hàn lâm** các từ lẫn English/dịch máy: starvation→\"bỏ đói\",
  burst-loss→\"mất gói theo chùm\", fade sâu→\"nghẽn sâu\", refresh→\"cập nhật lại\",
  blacklist→\"loại vĩnh viễn\", MSE thuần→\"sai số bình phương đơn thuần\",
  leading-order→\"xấp xỉ/thành phần bậc thấp\", Lemma suppression→\"Bổ đề triệt tiêu\",
  heuristic→\"công thức kinh nghiệm\", primary→\"bộ chính\", robustness→\"kiểm bền vững\",
  near-uniform→\"gần đồng nhất\", block-clustered→\"phân cụm theo khối\",
  Method/Missed%→\"Phương pháp/Bỏ lỡ%\", error bar→\"thanh sai số\",
  safety-loss→\"tổn thất an toàn\", missed-violation→\"tỉ lệ bỏ lỡ vượt ngưỡng\",
  SoTA→\"phương pháp tiên tiến gần đây\", Rule→bỏ/\"có-số-hạng\", freshness→\"độ tươi\",
  Negative result→\"kết quả phủ định\", novelty→\"độ mới lạ\", Policy→\"Chính sách\",
  recon→\"tái tạo\", Spike→\"thử nghiệm nhanh\", seed→\"hạt giống\",
  random-walk→\"bước ngẫu nhiên\", overfit→\"học vẹt\", round-robin→\"luân phiên đều\",
  probe-then-transmit→\"thăm dò--rồi--truyền\".
- **GIỮ NGUYÊN** thuật ngữ chuẩn không nên dịch (dịch ra sẽ kỳ, reviewer quen tên Người dùng):
  tên method (bài AoI-greenhouse), AR(1), Gilbert--Elliott, per-arm, VoU, AoI, AoII, RMSE,
  Whittle, Wilcoxon, autoencoder/AE, MLP, $O(1/\sqrt N)$, mean-field. Cân nhắc chú
  thích Việt lần đầu xuất hiện (vd \"per-arm (riêng từng cảm biến)\").
- Đổi tiêu đề block lặp \"Đọc công thức\"/\"Đọc bằng lời\" → **\"Diễn giải\"** cho trang
  trọng, thống nhất.
- Rút câu dài, bỏ chữ thừa trong ngoặc nếu công thức ở trên đã nói (vừa khử-English
  vừa giảm text). Sau khi rút, build lại — câu ngắn hơn có thể đổi layout (xem 5e).

## 5e. Khử chồng nhãn khi tái dùng TikZ 2-cột (de-collision) + pitfall \\\\ trong node
Figure manuscript 2-cột nhồi vào slide → nhãn trên mũi tên (DL/UL, $p_i(t)$, $\{\mu_i,\sigma_i^2\}$)
hay ĐÈ lên đường/đè nhau, chữ nhỏ. Người dùng chọn hướng \"nới nhãn giữ figure chi tiết\"
(thay vì vẽ lại bản gọn). Cách đã chạy thật trên BẢN COPY trong thư mục Slides
(KHÔNG đụng `figures/` manuscript):
- Tăng cỡ chữ nhãn `\scriptsize`→`\footnotesize`, `inner sep` 1→2pt.
- Nền trắng ĐỤC để chữ luôn nổi trên đường: thêm `fill=white, fill opacity=0.92,
  text opacity=1` vào node options (opacity nền không làm mờ chữ).
- Làm rõ nhãn mơ hồ: thêm hậu tố hướng (vd \"UL: reading $X_i,o_i$\\\\\scriptsize(về gateway)\").
- **PITFALL build-error:** dùng `\\` xuống dòng TRONG một TikZ `node{...}` báo
  \"Something's wrong--perhaps a missing \item\" → PHẢI thêm `align=left` (hoặc
  `align=center`) vào node options thì `\\` mới hợp lệ.
- VERIFY: render slide pipeline ra PNG, vision-check từng chỗ đã sửa
  (\"nhãn X có nền đục, đọc rõ, không đè đường không?\"). LƯU Ý: vision đọc bản render
  hay NHẦM ký tự do nét nhỏ (\"VoU\"→\"label\", \"UL\"→\"DL\") — đối chiếu file gốc bằng
  grep trước khi tin vision báo \"typo\", đừng sửa theo lỗi-đọc của vision.

## 5f. Slide \"chứng minh bằng lời\" (proof-sketch trực quan) — khi người dùng xin \"cách chứng minh\"
Khi người dùng nói \"trình bày THÊM cách chứng minh, nói đơn giản thôi, đưa toán vào\ngiải thích cho trực quan\", người dùng muốn slide RIÊNG đi sâu CÁCH một lemma/theorem được\nchứng minh — KHÁC slide phát biểu (4.x) chỉ nêu statement + block \"Kết luận\". Đặt\nslide proof NGAY SAU slide phát biểu, đánh số `4.1b`, `4.2b` (b = proof của a).\nCông thức đã chạy thật (deck +2 slide proof, build 0 lỗi, 25 trang):\n- **Cấu trúc cột trái = 3 bước đánh số B1/B2/B3**, mỗi bước 1 câu dẫn + 1 công\n  thức `\\[...\\]`; bước cuối là kết quả `\\boxed{...}`. Ví dụ Bổ đề triệt tiêu:\n  B1 viết 2 đại lượng cạnh tranh ($\\overline\\Phi$ vs $ES$) → B2 lấy tỉ số + khai\n  triển Mills $\\phi/\\overline\\Phi=z+1/z+\\dots$ → B3 đổi biến $z=(u-\\mu)/\\sigma$ ra\n  $\\boxed{ES/\\overline\\Phi\\to(u-\\mu)\\varepsilon}$. Ví dụ $O(1/\\sqrt N)$: B1 nới\n  lỏng ràng buộc → per-arm LP → $\\pi^\\star$; B2 đếm dao động, $N$ kênh độc lập ⟹\n  độ lệch $\\sim\\sqrt N$ (CLT); B3 chia quy mô $\\sqrt N/N=1/\\sqrt N$.\n- **Cột phải = 2 block diễn giải**: một block \"đọc công thức bằng lời\" (mỗi ký\n  hiệu nghĩa gì, vd $\\phi$=chiều cao chuông, $\\overline\\Phi$=diện tích đuôi, tỉ số\n  Mills=\"đuôi rơi nhanh cỡ nào\") + một `alertblock` **\"Trực giác hình học\"** dùng\n  ẩn dụ đời thường: đuôi vượt ngưỡng \"vừa hiếm vừa mỏng\" nên độ-sâu không kịp đóng\n  góp; hoặc \"tung $N$ đồng xu: tổng lệch $\\sqrt N$ nhưng TỈ LỆ lệch $1/\\sqrt N$\".\n  Ẩn dụ trực quan là cái người dùng quý nhất ở slide proof.\n- Nêu **MẤU CHỐT** của proof (điều kiện làm nó chạy) thành 1 block riêng: vd\n  \"kênh độc lập per-arm\" là lý do có $\\sqrt N$ — chung kênh thì sai lệch cộng hưởng\n  cỡ $N$, chia ra vẫn $O(1)$, không co về 0.\n- Đáy slide: 1 dòng nghiêng \"kiểm chứng số\" neo proof về dữ liệu thật (vd\n  $\\|\\hat\\mu_N-\\mu^\\star\\|_1$ khớp $1/\\sqrt N$ với $R^2{=}0.83$).\n- VERIFY: build chain ≥2 lần + render đúng trang proof ra PNG\n  (`pdftoppm -png -r 90 -f <page> -l <page>`) + vision-check \"3 bước B1/B2/B3 đủ,\n  công thức boxed hiện đúng, không tràn mép/đè chữ\". Recurring TOC đẩy số trang —\n  render vài trang quanh section, đừng đoán. Overfull vbox <4pt vô hại.\n- Đồng bộ số stale TRƯỚC khi thêm slide: grep deck cho các hằng đã đổi ở manuscript\n  (vd $\\varepsilon$, $\\alpha$, $\\sigma$%RANGE, % cải thiện) — verify lại từ CSV batch\n  hiện tại rồi sync deck, đừng để slide ôm số cũ trong khi bài đã sửa.\n\n## 6. Workspace\nĐặt deck trong thư mục riêng `SAS/Research/<project>_Slides/` với `figures/` con,
KHÔNG trộn vào thư mục manuscript. Báo người dùng bằng chứng build thật (số trang,
exit 0, errors 0) + `MEDIA:` đường dẫn PDF.
