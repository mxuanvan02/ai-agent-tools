# Tái lập & nguồn sự thật duy nhất (khi người dùng nói "không tin được kết quả nào là thật")

Trigger: người dùng nói câu kiểu *"cứ sửa lui sửa tới… khiến người dùng rất khó tin tưởng được kết quả nào là thật"*, hoặc bản thảo có nhiều bản song song / số không rõ nguồn. Đây là **lỗi quy trình**, không phải lỗi nội dung — chữa bằng cách thiết lập lại nguồn sự thật, KHÔNG phải sửa thêm một lần nữa.

## Chẩn đoán trước, đừng sửa vội

Dấu hiệu mất niềm tin điển hình (đã gặp thật ở bài bài bandwidth-scheduling):
- Nhiều bản `.tex` song song (`X/`, `X_clean/`, `X_pkg/…`) + nhiều `.zip` rải rác ở `~`.
- Git log cho thấy một tính năng bị **thêm → bỏ → tống vào legacy/** trong vài commit (VoU/CVaR).
- Bảng trong bản thảo mang tên bảng mà repo hiện tại KHÔNG sinh ra (số mồ côi).

Cách định vị bản canonical:
```bash
# so mtime các bản .tex; tìm repo git thật
stat --format='%y  %n' */main.tex
find . -name .git -type d
git -C <repo> log --oneline --stat      # đọc câu chuyện thêm/bỏ để hiểu quyết định đã chốt
```

## Phép thử niềm tin: diff artifact sinh-lại vs bản đã commit

Chỉ tin repo khi **chạy lại ra đúng số**. Xóa bảng cũ (vào thư mục tạm), chạy lại toàn pipeline, diff:
```bash
TMP=$(mktemp -d); <chạy pipeline ghi ra $TMP>
for f in outputs/tables/*.tex; do diff -q "$f" "$TMP/$(basename $f)" && echo "[KHỚP] $f"; done
```
KHỚP tuyệt đối ⇒ số **tất định (deterministic)**, sinh từ script + data thật, không gõ tay ⇒ đây là nguồn sự thật duy nhất. Chốt repo này làm canonical; đưa các bản `.tex`/zip thừa vào `_backups/<ts>/` (KHÔNG xóa).

## Đồng bộ bản thảo về canonical

Khi bản đang định submit KHÔNG khớp repo (số khác, thậm chí câu chuyện ngược nhau): repo tái lập được thắng. Reframe bản thảo bám số repo — kể cả phải đổi framing (vd Greenhouse→ERA5 Mekong) nếu pipeline cũ đã bị bỏ. Mọi số, mọi bảng, mọi câu phải khớp repo.

## Quy tắc "method thử-và-thua"

- Method đã **test và thua** ⇒ **BỎ HẲN**, không gắn "Proposed", và **KHÔNG đưa vào Future Work**. "Đã thử thất bại rồi lại bảo tương lai sẽ làm" là tự mâu thuẫn — reviewer bắt ngay. (Người dùng sửa trực tiếp: *"test nó không ổn rồi, nên đưa vào Future Work thì kì lắm"*.)
- Giữ cái đã thua **chỉ như điểm so sánh trong ablation** (bằng chứng "đã cân nhắc và thua"), không hơn. Đây là điểm mạnh về tính trung thực, không phải điểm yếu.

## Dữ liệu thật > dữ liệu tổng hợp — và thường sửa được dễ

- Phân biệt rạch ròi: "thật về khí hậu" (ERA5 = reanalysis thật) ≠ "thật về cảm biến hiện trường" (in-field IoT). ERA5 KHÔNG phải in-field — mô tả đúng là "reanalysis climate data", đừng gọi là "measured/in-field".
- Điểm yếu hay bị reviewer đánh nhất: zone/điểm dữ liệu **nhân bản** (offset thời gian + nhiễu) để phóng to N. Nếu nguồn là dữ liệu lưới (ERA5 Open-Meteo, miễn phí, không key), thay bằng **N điểm thật** khác tọa độ là xóa sạch được chữ "synthetic/stress test". Bài bài bandwidth-scheduling: 17 zone bịa → 20 trạm ERA5 thật khắp ĐBSCL, số còn đẹp hơn.
- Sau khi đổi sang data thật: quét toàn bài + README + code + caption để diệt hết chữ "synthetic/stress test". Chừa lại chỗ hợp lệ: "synthetic Gilbert–Elliott **channels**" (mô phỏng kênh truyền là chuẩn) và câu phủ định "no synthetic traces".

## Gói tái lập giao cho người dùng

- `reproduce.sh` một lệnh: tạo venv → cài dep → fetch data (cache, skip nếu có, `REFETCH=1` để ép) → chạy experiments → regen bảng+hình. `set -euo pipefail`, `cd "$(dirname "$0")"`. **Test chạy thật end-to-end** trước khi giao (bài bài bandwidth-scheduling: 82s).
- README có CẢ đường một-lệnh LẪN đường thủ công từng bước; bảng Requirements; nêu rõ deterministic + fetch tái lập byte-identical.
- Ship **code + source data only**; `outputs/`, `figures/`, `*.tex`, `*.pdf`, `_backups/` để trong `.gitignore`. Trước commit: `git status --short` xác nhận KHÔNG lọt outputs/tex/pdf.
- Verify push đã lên: `git ls-remote origin -h refs/heads/main` khớp local HEAD SHA. Nếu remote HTTPS mà auth là SSH → đổi remote sang `git@github.com:…` rồi push.

## LaTeX: review-markup vàng cho text agent thêm

Người dùng yêu cầu text agent thêm vào manuscript = **highlight vàng** (review markup, strip trước khi submit).
- **PITFALL cứng:** `soul` `\hl{…}` RẤT dễ vỡ với `\cite`/`\ref`/math — sinh rác `\citation{\hbox{}}` trong .aux (bibtex báo "I'm skipping whatever remains"), và `\soulregister{\ref}` gây **đệ quy vô hạn** → "TeX capacity exceeded". ĐỪNG bọc đoạn có `\cite`/`\ref` bằng `\hl`.
- **Giải pháp:** dùng môi trường khối `mdframed` cho mọi đoạn review (chịu được `\cite`/`\ref`/display math):
```latex
\usepackage{mdframed}
\newmdenv[backgroundcolor=yellow!30,linecolor=yellow!55!black,linewidth=0.4pt,
  innertopmargin=3pt,innerbottommargin=3pt,skipabove=3pt,skipbelow=3pt,
  leftmargin=0pt,rightmargin=0pt,innerleftmargin=4pt,innerrightmargin=4pt,
  splittopskip=0pt,splitbottomskip=0pt]{revblock}   % splittable across pages
```
Bọc `\begin{revblock}…\end{revblock}`. `\hl` chỉ để dành cho vài chữ plain-text ngắn không có lệnh mong manh.

## Xác minh cứng trước khi gọi "xong"

Build sạch nhiều pass (pdflatex→bibtex→pdflatex×2), rồi kiểm: số trang trong limit, `undefined citation = 0`, `bibtex error = 0`, `overfull >5pt = 0`. Render trang chứa bảng/hình/công thức ra PNG và **vision-check** đúng số canonical + không vỡ math. Cite phải đúng nguồn (bài bài bandwidth-scheduling suýt cite dataset Greenhouse Nam Phi cho dữ liệu ERA5 — loại lỗi người dùng ghét nhất). Gỡ entry `.bib` và bảng mồ côi không còn dùng.
