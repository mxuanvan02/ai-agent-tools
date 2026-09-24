# Manuscript LaTeX revision — techniques & pitfalls

Áp dụng khi sửa lớn một manuscript LaTeX cho người dùng (đổi phương pháp cốt lõi, thêm/bỏ section, regen bảng/hình, giữ page limit). Đi kèm với `execution-discipline` (kỷ luật thực thi + kết quả âm) và `manuscript-reproduction-audit`.

## Review markup (bắt buộc)
Người dùng muốn MỌI text agent thêm mới vào manuscript được đánh dấu để người dùng review, rồi strip trước khi nộp.

### `soul`'s `\hl{}` KHÔNG dùng để bọc đoạn có công thức/cite/ref
`\hl` là lệnh **fragile**, hỏng theo nhiều cách:
- **Math mode**: `! File ended while scanning use of \hl`.
- **`\cite`/`\ref` bên trong**: sinh rác `\citation{\hbox{}}` / `\citation{\char\hyphenchar\font}` vào `.aux` → bibtex báo `I'm skipping whatever remains of this command` (9+ error) → **toàn bộ citation undefined**, dù key có thật trong `.bib`.
- **ĐỪNG chữa bằng `\soulregister{\ref}`**: gây **đệ quy vô hạn** → `! TeX capacity exceeded [input stack size=10000]`, không ra PDF. (`\soulregister{\cite}` ít nguy hơn nhưng vẫn tránh.)
- `\hl` chỉ an toàn cho **text thuần ngắn**, 1 dòng, KHÔNG cite/ref/math.

### Hai cách markup CHẠY ĐƯỢC (chọn theo phạm vi)
1. **Đoạn/khối có công thức, cite, ref, display equation, lemma/proposition → dùng `mdframed` `revblock`** (hộp nền vàng, robust nhất):
   ```latex
   \usepackage{mdframed}
   \newmdenv[backgroundcolor=yellow!30,linecolor=yellow!55!black,linewidth=0.4pt,%
     innertopmargin=3pt,innerbottommargin=3pt,skipabove=3pt,skipbelow=3pt,%
     leftmargin=0pt,rightmargin=0pt,innerleftmargin=4pt,innerrightmargin=4pt,%
     splittopskip=0pt,splitbottomskip=0pt]{revblock}   % splitkeys=cho phép ngắt trang sạch
   ```
   Bọc: `\begin{revblock} ... \end{revblock}`. Xử lý ngon `\cite`, `\ref`, `\begin{equation}`, `align`, `\newtheorem{lemma/proposition}`, và tự ngắt trang (nhờ splittopskip/splitbottomskip=0pt — thiếu 2 khoá này mdframed dễ nuốt/tràn khi khối vắt qua ranh trang).
2. **Màu (inline, cho đoạn không tiện bọc khối)** — chạy cả text lẫn math:
   ```latex
   \definecolor{reviewnew}{rgb}{0.00,0.00,0.75}
   \newcommand{\hlnew}[1]{{\color{reviewnew}#1}}
   ```

### Strip trước nộp
- `revblock`: đổi định nghĩa thành môi trường rỗng (hoặc xoá `\begin/\end{revblock}`), giữ nội dung.
- `\hlnew`/`\rev`: `\renewcommand{...}[1]{#1}` (identity). Ghi comment nhắc ngay cạnh macro.

### Pitfall ngoặc (áp cho cả `\rev{}`/`\hlnew{}`)
- Bọc cả `\subsection{...}` + `\input{...}` trong một `\hlnew{...}` RẤT dễ hở ngoặc → "File ended while scanning use of ...". Đếm `{` vs `}` per-file trước build. An toàn: mỗi `\hlnew{...}` gói trọn 1 dòng/1 khối.
- Khi **convert `\rev{...}` → `revblock`** hàng loạt: nhớ xoá dấu `}` đóng cũ còn sót ở cuối đoạn (nguồn gây "extra }"), và mỗi `\begin{revblock}` phải có `\end{revblock}` tương ứng.

## Reconcile manuscript ↔ repo tái lập (chống "sửa lui sửa tới")

Khi người dùng mất niềm tin ("không biết số nào là thật"), gốc bệnh thường là **nhiều bản .tex song song + nhiều .zip + git log thêm-bỏ-thêm** một feature:
1. Nguồn sự thật = repo có git + script sinh bảng/hình từ data. `git log --stat` đọc câu chuyện thêm/bỏ feature (vd VoU→drop→legacy/).
2. Kiểm tái lập: chạy lại pipeline vào /tmp, `diff` bảng/CSV mới vs bản commit. KHỚP tuyệt đối ⇒ số tất định, tin được; lệch ⇒ chỉ mặt số "mồ côi".
3. Bản .tex đang submit có thể `\input` bảng mồ côi (tên bảng KHÁC repo sinh) và kể câu chuyện NGƯỢC repo (PDF nói thua, repo nói thắng). Bản PDF cũ = loại; repo = canonical.
4. Nếu pipeline đã đổi dataset (greenhouse→ERA5), đồng bộ TẤT CẢ: title, keywords, abstract, intro, system-model wording, safety band/hằng số, bảng, figure, data-availability. Quét sạch tên dataset cũ trong BODY (giữ trong reference list vì là tên bài người khác).
5. **Cite sai nguồn** (lỗi người dùng ghét nhất): sau reframe, kiểm mọi `\cite` gắn dataset — dễ sót cite trỏ entry dataset CŨ (vd `hull2024greenhouse`="South African Greenhouse Tunnel" bị gắn nhầm cho data ERA5). Entry .bib không còn cite ⇒ bibtex tự bỏ qua (vô hại), nên dọn cho gọn.

## Method ĐÃ thử & THUA: KHÔNG Future Work
Người dùng chốt (sửa lại quy tắc cũ): một method mình đã test và thua (vd CVaR/VoU thua raw-p trong ablation) đưa vào Future Work là **tự mâu thuẫn** ("thử flop rồi nhưng tương lai sẽ theo đuổi"). Đúng cách: bỏ khỏi Proposed VÀ khỏi Future Work; giữ làm **điểm so sánh trong ablation** (bằng chứng "đã cân nhắc, thua trên regime này"). Future Work chỉ chứa hướng CHƯA thử.

## Dẫn xuất lý thuyết cho hằng số heuristic = rigor, KHÔNG phải novelty
Hằng số update "gõ tay" (vd projected dual update) ⇒ dẫn xuất: viết bài toán ràng buộc tường minh (min E[risk] s.t. avg bandwidth/AoI/miss ≤ target), lập Lagrangian, chỉ ra update CHÍNH LÀ projected (super)gradient ascent → hằng số thành shadow price + step size; thêm Lemma bounded-multipliers + Proposition feasibility O(1/T). Nói THẲNG: đây là rigor (Lyapunov/drift-plus-penalty/dual ascent đã có sẵn, Neely 2010), KHÔNG phải toán mới — hợp tầm hội nghị, đừng thổi thành đóng góp lý thuyết.

## Giữ page limit (6–8 trang hội nghị C1/hội nghị)
Khi tràn 1–5 dòng sang trang cuối (thường là vài mục references cuối):
1. Đừng tỉa prose từng chữ lặt vặt — thường không dứt điểm và tốn nhiều vòng.
2. Cách sạch & chuẩn: thu nhỏ font references — `\renewcommand{\thebibliography}[1]{\small\oldthebibliography{#1}...}`. References nhỏ hơn body là quy ước phổ biến, kéo lại 3–5 dòng ngay.
3. Nếu cần cắt content: bỏ câu tự-bình-luận (meta như "this is a stronger claim than...") thay vì cắt số liệu.
4. Sau mỗi lần sửa: build **3 pass** (pdflatex → bibtex → pdflatex ×2) rồi đếm `pdfinfo main.pdf | grep Pages`. Undefined refs cần đủ pass để `.aux` đồng bộ; nếu vẫn undefined sau 3 pass thì là label thật bị thiếu, không phải pass.

## Regenerate tables/figures from CSV (tái lập + đồng bộ)
- Manuscript thường có bảng **format thủ công riêng** (tên/cột khác tên bảng script sinh ra) → KHÔNG có cầu tự động. Viết một `make_manuscript_tables.py` sinh thẳng đúng format manuscript từ CSV nguồn, số khớp tuyệt đối, tái lập được. Map tên: `sota_comparison.tex` ← `rabs_summary.csv`, v.v.
- Sau regen: đối chiếu từng ô bảng-PDF vs CSV nguồn (grep) để xác nhận đồng bộ; đừng tin mtime.
- Hình: chỉ regen hình manuscript THỰC SỰ `\includegraphics`, bỏ hình cũ (AI overview) khỏi body. Vision-check hình sau regen: điểm đúng toạ độ, không nhãn đè, không tràn khung. Nhãn đè cluster → chỉ annotate điểm tách biệt, để cụm chồng cho legend lo.

## Đổi phương pháp cốt lõi (VD: heuristic → có-nền-lý-thuyết)
- DERIVE trước, verify sau (kỷ luật Q1 của người dùng).
- Sửa code đúng 1 chỗ (hàm scoring), giữ nguyên baselines; xoá sạch outputs cũ rồi chạy lại TOÀN BỘ pipeline theo thứ tự phụ thuộc để tránh lẫn số cũ/mới.
- Khi đổi phương pháp, đồng bộ lan truyền: tên bài + keywords + abstract + intro contributions + related-work + conclusion + toàn bộ số văn xuôi.

### "Dẫn xuất lý thuyết" nghĩa là gì — nói thẳng rigor vs novelty (người dùng hỏi lại điều này)
- Dẫn xuất = viết một **bài toán tối ưu có ràng buộc tường minh** rồi CHỨNG MINH luật cập nhật (các dòng code) chính là nghiệm số của nó. Mọi hằng số bừa (step size, target, penalty) biến thành đại lượng có nghĩa: **shadow price** (nhân tử λ), **step size** (α của dual ascent), **baseline price** (hằng số c).
- Với primal–dual/AoI-aware scheduling: khung là **Lyapunov drift-plus-penalty (Neely 2010) + dual subgradient ascent cho constrained MDP** — SÁCH GIÁO KHOA, KHÔNG mới. Dẫn xuất cho **rigor** (phòng thủ reviewer "sao lại 0.010"), KHÔNG cho **novelty**. Nói thẳng cho người dùng điều này, đừng gắn "đóng góp lý thuyết mới" cho cái chỉ là đặt-lên-nền-có-sẵn.
- Sản phẩm tối thiểu đủ tầm hội nghị (hội nghị C1 6–8 trang): 1 tiểu mục ~½ trang gồm Lagrangian + luật dual ascent + **Lemma (bounded multipliers)** + **Proposition (asymptotic feasibility, kiểu `(1/T)Σg ≤ (λ_max)/(αT) = O(1/T)`)**, mỗi cái kèm proof sketch. Dùng `\newtheorem{lemma}{Lemma}` + `{proposition}`.
- ĐỪNG đẩy lên "novelty thật" (regret bound riêng cho coupling) trong bài hội nghị 8 trang: xác suất thua cao, loãng, dễ bị bắt "claim quá tay". Để Future Work.

## Đồng bộ manuscript về REPO tái lập (canonical source) — chống "sửa lui sửa tới → mất niềm tin"
Tín hiệu người dùng: "sửa tới sửa lui... khó tin kết quả nào là thật", "lúc thêm X rồi lại bỏ". Gốc thường KHÔNG phải sai số mà là **môi trường lộn xộn**: nhiều bản `.tex` song song + nhiều `.zip` + git log thêm/bỏ/tống-legacy một phương pháp (VD VoU/CVaR thêm→bỏ→legacy trong 3 commit).

Quy trình xử (đã chạy thành công cả phiên):
1. **Định vị nguồn sự thật**: tìm repo git (thường mới nhất, có `.git`) vs các thư mục `.tex`/zip mồ côi. So mtime + có git không.
2. **Kiểm chứng tái lập TRƯỚC khi sửa chữ nào**: xoá bảng/CSV cũ (trong thư mục TẠM, không đụng bản gốc), chạy lại pipeline, **diff** bảng `.tex` + summary CSV mới sinh vs bản commit. KHỚP 100% ⇒ số tái lập được, tin được. Đây là "phép thử niềm tin" — làm nó thay vì thuyết phục bằng lời.
3. **Chỉ mặt số mồ côi**: bung zip đang định nộp, diff bảng của nó vs bảng repo. Nếu KHÁC (VD Bw 1.49 vs 1.23, kể chuyện ngược) ⇒ bản nộp ôm số cũ không sinh ra được từ pipeline nào ⇒ nộp là toang (reviewer chạy lại ra số khác). Nói thẳng bằng bảng đối chiếu đen-trắng.
4. **Chốt 1 canonical**: repo = nguồn sự thật DUY NHẤT. Lấy văn xuôi mới nhất làm khung, thay TOÀN BỘ bảng/số/hình bằng cái repo sinh. Bản `.tex`/zip thừa → `_backups/<ts>/` (KHÔNG xoá), chờ người dùng duyệt nội dung trước khi dọn.
5. **Bảng script sinh ≠ bảng manuscript cũ**: repo có thể sinh BỘ bảng khác (sota/wilcoxon/scalability/ablation) so với bài cũ (sota/wilcoxon/sensitivity/nonstationary/CVaR). Đồng bộ = **swap cả bộ bảng** + viết lại narrative, không chỉ thay số.
6. **Phương pháp không tái lập được (script đã vào `legacy/`) → về Future Work**, KHÔNG để làm "Proposed" (đúng nguyên tắc: không gắn Proposed cho cái thua/không tái lập).
7. **Câu chuyện trung thực**: nếu số thật cho thấy chỉ thắng một phần (VD thắng composite objective + băng thông nhưng THUA miss-rate, Wilcoxon `p=0.36, r<0`), viết đúng "trade-off băng thông–an toàn", KHÔNG viết "an toàn hơn". Nêu thẳng metric không thắng trong cả eval lẫn Limitations.
8. **Gate cuối**: build 3-pass sạch (0 undefined cite, 0 bibtex error, 0 overfull), đếm trang ≤ limit, và **vision-check** từng trang bảng/hình render đúng số canonical trước khi gọi là xong.
