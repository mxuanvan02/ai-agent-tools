# Cô đọng manuscript cho page limit / page charges (IEEE IoTJ và tương tự)

Khi người dùng hỏi "viết ngắn hơn được không?" / "tạp chí giới hạn N trang" / "agent
triển khai đi" (cô đọng bản thảo) — đây là EXECUTE. Dùng quy trình dưới.

## 1. Xác minh chính sách trang THẬT trước khi cắt (đừng tin trí nhớ người dùng)

Người dùng hay nhớ nhầm "IoTJ giới hạn 8 trang". ĐÍNH CHÍNH bằng nguồn live, vì nếu
cắt sai hướng sẽ mất toán/đóng góp vô ích.

**Đã verify (ieee-iotj.org/guidelines-for-authors, mục "Mandatory Page Charges"):**
> "billed **$175 per page in excess of the first eight published pages**. These
> charges are mandatory... authors are advised to practice economy."

Nghĩa thật:
- **8 trang = ngưỡng MIỄN PHÍ, KHÔNG phải giới hạn cứng.** Bài dài hơn vẫn đăng,
  KHÔNG bị reject vì độ dài. Quá 8 trang trả $175/trang (bản *published*).
- IoTJ là journal; regular paper thực tế thường **11–14 trang** (phổ biến nhất),
  8–10 (gọn), 15–18 (nhiều lý thuyết+thực nghiệm). 8 trang là kiểu giới hạn của
  CONFERENCE/letters, không phải IoTJ regular.
- Abstract IoTJ: 150–250 từ, một đoạn, không citation/equation hiển thị.
- Open Access fee (nếu chọn): $2695, tính riêng với over-length charges.

→ Đề xuất mục tiêu HỢP LÝ (~12–14 trang chặt) thay vì ép xuống 8 (mất chiều sâu).
Nói rõ con số chi phí ước tính để người dùng quyết: vd 18 trang → ~10 trang vượt ×
$175 ≈ $1,750.

## 2. ĐO trước khi cắt: cái gì THỰC SỰ chiếm chỗ?

Bài học cốt lõi của session này: cô đọng prose 10+ đoạn dài chỉ rút **1 trang**
(18→17) vì bản thảo dài do **BẢNG + HÌNH**, không phải chữ.

Trước khi sửa chữ, đếm:
```
wc -l sections/*.tex | sort -n            # section nào dài
for f in sections/*.tex; do detex "$f"|wc -w; done | sort -rn  # word count thật
grep -rcE 'begin\{table'  sections/*.tex | grep -v ':0'   # đếm bảng
grep -rcE 'begin\{figure' sections/*.tex | grep -v ':0'   # đếm hình
grep -rcE 'begin\{table\*\}|begin\{figure\*\}' sections/*.tex  # full-width
```
Nếu §Evaluation có 10+ bảng → prose-cutting sẽ kém hiệu quả. Báo người dùng THẲNG con
số này và đề xuất giảm trang bằng cách động vào bảng/hình:
1. **Gộp nhiều bảng → 1 bảng lớn** (results + recent-SoTA + full-SoTA; 3 bảng
   sensitivity). Thường hiệu quả, NHƯNG xem CẢNH BÁO bên dưới — bảng gộp 13 dòng +
   header nhóm có thể to gần bằng tổng 2 bảng cũ → **không giảm trang nào**.
2. Chuyển bảng phụ (sensitivity, danger ablation, tail) vào Appendix (~1–2 trang).
   Đây là cách giảm trang ĐÁNG TIN hơn gộp bảng/hình.
3. Gộp nhiều hình rời (bprobe/lambda/channel) thành 1 figure multi-panel — CHỈ khi
   mỗi PNG là một plot đơn. Nếu mỗi PNG đã chứa nhiều subplot, xem CẢNH BÁO bên dưới.

### CẢNH BÁO: gộp bảng/hình có thể KHÔNG giảm trang và còn hại chất lượng

Bài học session thật (đã phải REVERT):
- **Gộp 3 hình sensitivity `figure*` 3-panel:** mỗi PNG vốn đã chứa 2 subplot
  (loss + missed), ép xuống `0.32\textwidth` làm **chữ trục li ti, khó đọc**, mà
  **vẫn 17 trang** (không giảm). Net-negative → revert về 3 hình `0.95\linewidth`
  riêng. Quy tắc: TRƯỚC khi gộp hình, kiểm mỗi PNG là 1 plot hay nhiều subplot
  (`pdftoppm` render thử + vision-check legibility); nếu đã nhiều subplot thì gộp
  ngang = không đọc được khi chiếu/in.
- **Gộp 2 bảng so sánh → 1 bảng 13 dòng + `\multicolumn` family-header:** render
  đẹp, đúng, nhưng **vẫn 17 trang** vì bảng gộp to gần bằng tổng 2 bảng cũ.

→ Đừng hứa trước số trang sẽ giảm khi gộp bảng/hình. Build + `pdfinfo … | grep
Pages` SAU mỗi lần gộp để đo thật. Nếu không giảm, giá trị thật của việc gộp là
**chất lượng/liêm chính** (bỏ bảng trùng, fix provenance — xem 4b), KHÔNG phải số
trang; nói THẲNG điều này với người dùng và pivot sang Appendix (mục 2 cách 2) nếu mục
tiêu là giảm trang. Sẵn sàng revert ngay nếu việc gộp làm xấu legibility.

## 3. Cô đọng prose AN TOÀN (giữ 100% bảng/số/đóng góp)

- Backup TRƯỚC: `cp -r sections main.tex *.bib _backups/precondense_<ts>/`.
- Gộp câu rườm, bỏ "We therefore", "It is worth noting", "Notably"; gộp align
  nhiều dòng thành một câu khi không mất bước toán.
- KHÔNG cắt: equation cốt lõi (belief/index/theorem), con số verify, contribution.
- Giữ nguyên mọi `\label`/`\eqref`/`\cite` khi viết lại đoạn.

## 4. Đẩy proof dài vào Appendix (kỹ thuật IoTJ chuộng)

### TAIL dominates: cắt Evaluation gần như KHÔNG giảm trang

Bài học session thật (bài AoI-greenhouse 15→14): người dùng duyệt cắt Evaluation (gộp 3 hình→1
3-panel, gộp 2 ablation, bỏ 1 bảng công thức) kỳ vọng ~11 trang, thực tế chỉ xuống
14. Lý do: phần ĐUÔI — §Theory (2 proof + figure* 6-panel) + Appendix + 41 refs
2-cột — chiếm phần lớn 3 trang cuối, mà cắt Evaluation không đụng tới đuôi. Cắt
giữa bài chỉ làm chữ dày lên ở vùng giữa; phần tiết kiệm bị float lớn + ref-list
hấp thụ, không vượt nổi ranh giới 1 trang. → TRƯỚC khi hứa số trang, `pdftotext -f N
-l N` 3 trang ĐUÔI xem cái gì chiếm chỗ. Nếu đuôi là theory/appendix/refs (ngoài
phạm vi cắt), nói THẲNG: cắt Evaluation chỉ rút ~1 trang, sâu hơn phải động theory/
proof = đóng góp lõi (cần người dùng duyệt). Đừng ước "~11 trang" rồi không đạt.

### Đòn cắt sạch nhất: APPENDIX/PROOF TỰ KHAI BÁO TRÙNG LẶP

Đọc Appendix tìm câu tự-thú trùng lặp. Bug thật: Appendix A mở đầu "The main text
now contains the complete proof of Theorem 2; here we **restate** the key dominance
step..." → Lemma + proof Theorem đã có trong thân, appendix chỉ lặp. Xóa phần lặp =
giảm trang mà KHÔNG mất chứng minh nào (giữ proof chỉ-có-ở-appendix: corollary,
fairness, bounded-deficit).

**GOTCHA xóa lemma để lại `\ref` treo:** thân bài có `Lemma~\ref{lem:dominate}` /
"full argument in Appendix" trỏ tới phần vừa xóa → undefined ref + câu hứa sai. Sau
khi xóa block trùng: grep `\ref{<label-đã-xóa>}` + grep câu "in Appendix"/"full ...
argument", viết lại proof sketch trong thân thành TỰ CHỨA (gộp 3 bước dominance/
blocking/counting thành đoạn gọn), bỏ tham chiếu chết. Build + grep undef=0 + `??`=0.

### Float lớn để lại NỬA TRANG TRỐNG → `\raggedbottom` + thu/rút caption

Triệu chứng: một trang chỉ ~40/77 dòng vì `figure*` full-width (vd 6-panel) bị đẩy
lên đầu trang sau, để lại nửa trang trống. Khử:
- `\raggedbottom` ở preamble (cho phép trang ngắn thay vì giãn — bản thân không
  giảm trang nhưng cho các đòn khác hiệu lực).
- Thu nhẹ figure* (`width=0.84\textwidth`) + RÚT GỌN caption 6-panel ("(a)--(b) ...;
  (c) ...;" thay "Panel (a) shows...") — hợp economy người dùng + claw lại vài dòng.
- IEEEtran bib: `\setlength{\IEEEbibitemsep}{-1.2pt}` nén khoảng giữa ref; đủ gập
  1-2 ref đuôi (~4 dòng) về trang trước → giảm đúng 1 trang.
Mỗi đòn build + `pdfinfo | grep Pages`; khi chỉ còn 1 ref tràn sang trang cuối thì
một đòn nhỏ (rút caption HOẶC nén bibitemsep) là đủ chạm mốc.

### CHẨN ĐOÁN GỐC khi 1 ref/1 dòng tràn sang trang cuối (đừng vá layout toàn cục)

Bài học session bài bandwidth-scheduling 2026-06-26 (bài dùng `article` + `\thebibliography`,
KHÔNG phải IEEEtran). Triệu chứng: bài 9 trang nhưng trang 9 chỉ chứa ĐUÔI
bibliography (1–2 mục ref ~200–500 ký tự). Sai lầm phiên TRƯỚC: vá layout toàn cục
lặp đi lặp lại (giảm `bottom` margin, `\raggedbottom`, thu figure 0.50→0.44→0.40,
nén prose) — KHÔNG đòn nào chạm mốc 8 trang vì cái tràn là **bibliography spacing**,
không phải nội dung. ĐO trước khi vá: `for p in $(seq 1 N); do echo "p$p: $(pdftotext
-f $p -l $p main.pdf - | wc -c)"; done` — nếu trang cuối <600 ký tự và toàn ref →
đây là tràn-bib, fix bằng bib-spacing chứ KHÔNG phải layout.

Fix đúng cho `\thebibliography` (non-IEEEtran): nén `\itemsep` trong renewcommand
bib. Bài đã có `\renewcommand{\thebibliography}[1]{\oldthebibliography{#1}
\setlength{\itemsep}{-1pt}\setlength{\parsep}{0pt}\scriptsize}` → siết `itemsep`
theo nấc nhỏ dần (−1 → −3 → −6pt), build + đếm trang sau MỖI nấc, dừng ngay khi
trang cuối biến mất. Phiên này −1pt(2 ref tràn) → −3pt(1 ref) → −6pt(0, về đúng 8
trang). Vì bib đã `\scriptsize`, nén itemsep an toàn, KHÔNG đụng một chữ nội dung.
Quy tắc tổng quát: tràn-bib-1-ref là lỗi spacing, fix tại spacing-of-bibliography
(IEEEtran→`\IEEEbibitemsep`; `\thebibliography`→`\itemsep`), đừng siết margin/figure
toàn cục. Lưu ý exit_code: `grep -c undefined log` trả 0 làm chuỗi `&&` dừng với
exit 1 — KHÔNG phải build lỗi, verify bằng `pdfinfo`.

Pattern: trong thân bài để **proof sketch** ngắn (2–4 câu, trỏ
`Appendix~\ref{app:proofs}`), chuyển full proof (3-step, nhiều align) sang
`99_appendix_proofs.tex`.

**GOTCHA multiply-defined label:** khi copy block proof có `\label{...}` sang
appendix mà KHÔNG xóa label ở chỗ cũ → "Label multiply defined". Cũng coi chừng
label trùng SẴN CÓ từ trước (vd `eq:pvio` định nghĩa ở cả §2 và §5). Cách xử lý:
- grep `label{<name>}` xuyên `sections/*.tex` tìm chỗ trùng.
- grep `eqref{<name>}`/`ref{<name>}` xem ai tham chiếu. Nếu KHÔNG ai ref tới bản
  trùng → đổi tên nó an toàn (vd `eq:pvio` → `eq:pvio_uni` cho bản đơn biến §5).

## 4b. GỘP BẢNG: kiểm provenance số liệu TRƯỚC khi gộp (liêm chính)

Gộp bảng là cách giảm trang hiệu quả nhất (mục 2), nhưng có bẫy liêm chính nghiêm
trọng. Bài học session thật:

- Nhiều bảng so sánh cùng "giao thức 30-window" nhưng hàng method chuẩn (bài AoI-greenhouse)
  có số **lệch nhau giữa các bảng** (loss 0.0027 vs 0.0028, runtime 97.4 vs 111.2)
  → dấu hiệu chúng sinh từ **các batch thí nghiệm KHÁC NHAU** (intel_benchmark vs
  whittle_exact vs sota_comparison). Gộp ẩu thành 1 hàng method = **bịa ra một bảng
  "đồng nhất" mà số thực ra không cùng nguồn** → các baseline bị so với một method-batch
  khác → không công bằng.
- Thêm bẫy: **CSV gốc trong repo có thể KHÔNG khớp số đang in trong bài** (bảng được
  sinh từ một batch cũ hơn code hiện tại). Đây là lỗ hổng data-provenance.

Quy trình AN TOÀN khi người dùng duyệt gộp bảng:
1. Định vị mọi bảng định gộp, đọc hàng method-chuẩn của TỪNG bảng, so số. Khác nhau
   → KHÔNG gộp ẩu.
2. Tìm CSV/artifact gốc backing từng bảng (`find docs results -name '*.csv'`),
   verify lại mean±1.96·sd/√n + Wilcoxon paired bằng venv repo (scipy) — đối chiếu
   với số trong bài. Lệch → báo người dùng lỗ hổng provenance.
3. **Cách A (rigor, khuyến nghị):** chạy lại MỘT batch thống nhất cho TẤT CẢ baseline
   + method trong cùng harness (cùng window/seed/channel) → một bảng duy nhất, số
   nhất quán tuyệt đối, fix luôn provenance. Harness `*_30windows.py` thường đã hỗ
   trợ chạy hết policy trong `POLICY_ORDER` một lần; backup CSV cũ trước khi ghi đè.
4. **Cách B (nhanh, kém chặt):** gộp trình bày, giữ số từng baseline như bài, bỏ
   hàng method trùng, chấp nhận sai lệch nhỏ. Không xử lý được gốc → chỉ dùng khi
   người dùng chấp nhận.
5. Để người dùng CHỌN A/B trước khi chạy job nặng (Cách A tốn compute). Sau khi có
   batch mới: cập nhật cả bảng + mọi p-value/bội số trong prose (grep mọi lần lặp
   con số), build, đếm trang.

GOTCHA đơn vị: cột `missed_vio` trong CSV có thể ở dạng raw (0.044 = 0.044%), đừng
nhân 100 nhầm. Verify bằng cách đối chiếu một giá trị với bài.

LAYOUT bảng gộp nhiều họ: khi gộp baseline thành 1 bảng `table*` dài, nhóm theo họ
phương pháp bằng `\multicolumn{N}{l}{\textit{Tên họ}} \\` làm hàng phân nhóm (không
cần package mới). Vision-verify render: hàng italic header trải đúng, cột p-value/
(W/L/T) cuối không bị cắt lề phải. Cách này giữ bảng dài vẫn dễ đọc.

GOTCHA in summary: script in console có thể lệch cột (in `overshoot_p90` vào chỗ
`runtime` do nhầm index) → runtime hiện 0.0. Đừng tin console; đọc thẳng CSV để lấy
số chính thức.

## 4c. PARALLEL-AGENT WRITE CONFLICT (người dùng chạy agent song song trên repo)

Người dùng thường chạy nhiều agent song song trên cùng repo. Khi patch một file `.tex`,
nếu thấy cảnh báo kiểu:
> "file was modified by sibling subagent '...' but this agent never read it"
→ một agent KHÁC đang sửa cùng file đồng thời. Patch vừa rồi có thể đã **ghi đè**
trạng thái mới của agent kia (lost-update), và ngược lại.

Quy tắc:
- **Đọc lại file ngay** (read_file) trước khi patch tiếp, để diff trên trạng thái mới
  nhất, giảm va chạm.
- **DỪNG TAY và hỏi người dùng** khi cảnh báo này fire trên một file đang sửa nhiều
  lần: (1) agent tiếp tục (chấp nhận rủi ro, đọc-lại-trước-mỗi-patch), (2) tạm dừng file
  này đợi agent kia xong, (3) người dùng tắt agent kia. Đừng tự quyết tiếp tục — rủi ro mất
  việc của cả hai bên.
- Artifact đã verify-and-saved an toàn (CSV batch mới, file đã build) KHÔNG mất khi
  dừng — trấn an người dùng để quyết định dừng không bị coi là phí công.

## 5. Verify build (gate bắt buộc, contract người dùng)

Full chain rồi grep pass CUỐI:
```
pdflatex … ; bibtex main ; pdflatex … ; pdflatex …
grep -cE '^!' log                              # errors = 0
grep -cE 'LaTeX Warning: Reference' log        # undef cross-ref = 0
grep -cE 'Citation.*undefined' log             # undef cite = 0
grep -cE 'multiply.defined' log                # = 0
grep -oE 'Overfull \\hbox \(([0-9.]+)pt' log | grep -oE '[0-9.]+' | awk '$1>60'|wc -l  # = 0
pdfinfo main.pdf | grep Pages                  # đếm trang trước/sau
```
Lưu ý: `LaTeX Font Warning: Font shape ... undefined` (vd OT1/ptm/m/scit italic
small-caps) KHÔNG phải undefined reference — bỏ qua, không phải lỗi thật.

Báo người dùng: số trang trước→sau, build sạch (0/0/0/0), backup path, và NÓI THẲNG
nếu prose-cutting chỉ rút được ít trang vì bảng/hình mới là thứ chiếm chỗ.
