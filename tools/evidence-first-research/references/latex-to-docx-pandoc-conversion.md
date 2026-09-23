# LaTeX → DOCX conversion for venue templates (pandoc-based)

Trigger: người dùng nói "kèm bản DOCX", "convert sang Word theo template",
"đúng template hội nghị/tạp chí", hoặc venue chỉ phát template `.docx` (hội nghị C1,
một số hội nghị Việt Nam, một số tạp chí MDPI bản preprint, v.v.) trong khi
manuscript được viết bằng LaTeX.

Đây là Stage 10 EXECUTE, không chỉ là chạy pandoc. Pandoc một-phát hầu như
LUÔN cho bản docx thiếu bảng/figure/refs. Quy trình đã verify chạy thật:

## 1. Trước khi convert: dựng STAGING tree riêng

Không sửa source chính (manuscript LaTeX vẫn phải build PDF được). Tạo
`/tmp/<project>_docx_build/` rồi rsync/copy:
- `main.tex`, tất cả `sections/*.tex`, `outputs/tables/*.tex`, `refs.bib`
- `figures/` (các `.tex` tikz và PNG/PDF)
- `main.bbl` đã build từ pdflatex+bibtex (nguồn references)

Mọi sửa cho docx (gỡ resizebox, swap figure, inline bib) đều ở staging tree.

## 2. Pitfall #1: `\resizebox{\linewidth}{!}{...}` ăn mất bảng

Pandoc không parse được `\resizebox` bọc ngoài `tabular`. Hệ quả: bảng đó **bị
bỏ qua hoàn toàn** trong output docx, không cảnh báo, không lỗi. Caption có
thể vẫn hiện (nếu nằm ngoài `\resizebox`) nhưng nội dung bảng biến mất.

Cách sửa:
```python
# Strip \resizebox{\linewidth}{!}{ ... } -> giữ nguyên \begin{tabular}...\end{tabular}
s = open(p).read()
s = s.replace(r"\resizebox{\linewidth}{!}{","").rstrip()
s = re.sub(r"\}\s*\\end\{table\}", r"\\end{table}", s)
open(p,"w").write(s)
```

Áp dụng cho MỌI bảng (grep trước: `grep -l 'resizebox' outputs/tables/*.tex`).
Phiên bài bandwidth-scheduling này: 3 bảng có `\resizebox` (sota_comparison, wilcoxon,
nonstationary), nếu chỉ strip 2 thì sẽ thiếu 1 bảng trong docx mà nhìn
captions thấy đủ — verify số `<w:tbl>` trong XML để bắt.

## 3. Pitfall #2: TikZ figures không vào docx

Pandoc bỏ qua `\begin{tikzpicture}`. Phải render TikZ → PNG đứng, rồi swap
sang `\includegraphics{...png}`.

Recipe render TikZ standalone:
```latex
% /tmp/arch_standalone.tex
\documentclass[border=4pt]{standalone}
\usepackage{tikz}
\usepackage{amsmath}
\begin{document}
% PASTE nội dung tikzpicture từ figures/arch_diagram.tex vào đây
\begin{tikzpicture}...\end{tikzpicture}
\end{document}
```
```bash
pdflatex -interaction=nonstopmode /tmp/arch_standalone.tex
pdftoppm -png -r 200 /tmp/arch_standalone.pdf /tmp/arch_png
```

Rồi viết lại `figures/arch_diagram.tex` trong staging tree thành:
```latex
\begin{figure}[h!]
  \centering
  \includegraphics[width=0.9\linewidth]{figures/arch_diagram.png}
  \caption{...}
  \label{fig:arch}
\end{figure}
```

Đặt PNG vào `figures/` trong staging tree. Pandoc cần `--resource-path` thấy
được nó:
```bash
pandoc main.tex -o out.docx --resource-path=.:figures:outputs/figures
```

Cho figure dùng `.pdf` (vd matplotlib output): swap đường dẫn từ `.pdf` sang
`.png` trong section file (`sed -i 's/tradeoff_plot.pdf/tradeoff_plot.png/'`).

## 4. Pitfall #3: `\bibliography{refs}` không render

Pandoc không tự gọi bibtex. Hai cách, cách nào cũng được nhưng `\bibitem` của
IEEEtran có macro phức tạp pandoc nuốt nửa:

- ❌ Đổi sang `\input{thebib.tex}` với nội dung là `.bbl` thô — pandoc lỗi
  `Error at "thebib.tex" expecting \end{document}` ở dòng cuối có
  `\end{thebibliography}`, hoặc bỏ qua hết entries không kèm `\BIBentry...`.
- ✅ Parse `.bbl` thành `\begin{enumerate}` thuần:

```python
import re
bbl = open("main.bbl").read()
m = re.search(r"\\begin\{thebibliography\}\{\d+\}(.*?)\\end\{thebibliography\}",
              bbl, re.DOTALL)
body = m.group(1)
parts = re.split(r"\\bibitem\{([^}]*)\}", body)
# parts[0] = preamble (drop), then alternating key/text
entries = []
for i in range(1, len(parts), 2):
    text = re.sub(r"\s+", " ", parts[i+1]).strip()
    text = text.replace("``",'"').replace("''",'"').replace("~"," ")
    text = re.sub(r"\\BIBentry[A-Za-z]+\s*", "", text)
    text = re.sub(r"\\(newblock|relax)\b\s*", "", text)
    entries.append(text)

lines = [r"\section*{References}", r"\begin{enumerate}"]
for t in entries:
    lines.append(r"\item " + t)
lines.append(r"\end{enumerate}")
open("thebib.tex","w").write("\n".join(lines))
```

Trong `main.tex` (staging) thay block bibliography:
```latex
% TRƯỚC:
% \bibliographystyle{IEEEtran}
% \bibliography{refs}
% SAU:
\section*{References}
\input{thebib.tex}
```

Verify: `grep` author tên đầu tiên + cuối cùng trong `word/document.xml` để
chắc cả 17 (hoặc bao nhiêu) refs có vào.

## 5. Pitfall #4: `\input{...}` không có path đúng → ref hỏng

Pandoc resolve `\input` theo CWD lúc chạy. Phải `cd` vào staging tree trước
khi gọi pandoc, KHÔNG truyền absolute path đến main.tex từ thư mục khác.

```bash
cd /tmp/rabs_docx_build && pandoc main.tex -o /tmp/bài bandwidth-scheduling_STAIS.docx \
  --reference-doc="<path_to_template.docx>" \
  --resource-path=.:figures:outputs/figures
```

## 6. Reference-doc trick: thừa hưởng style từ template venue

Pandoc có flag `--reference-doc=<template.docx>`. Nó dùng style (fonts,
margins, paragraph styles) của template làm base cho output. Nghĩa là chỉ cần
template chính thức của venue, output sẽ ra đúng font/margin mà không phải
hardcode `\setmainfont{Times}`.

Gotcha: nếu template embed font (vd Arimo-regular.ttf trong `word/fonts/`),
docx output **không mở được bằng `python-docx`**:
```
KeyError: "There is no item named 'word/fonts/Arimo-regular.ttf' in the archive"
```
Word/LibreOffice mở được bình thường — đây là bug python-docx, không phải
docx hỏng. Verify bằng zipfile + regex trên `word/document.xml` trực tiếp:

```python
import zipfile, re
z = zipfile.ZipFile("/tmp/out.docx")
doc = z.read("word/document.xml").decode("utf-8","ignore")
print("tables:",     doc.count("<w:tbl>"))
print("images:",     doc.count("<w:drawing>"))
print("equations:",  doc.count("<m:oMath>"))   # OMML = Word native math
imgs = [n for n in z.namelist() if n.startswith("word/media")]
print("embedded images files:", imgs)
txt = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", doc))
for kw in ["Introduction","Related Work","Conclusion","References",
           "<author đầu tiên>", "<author cuối cùng>"]:
    print(kw, "->", kw in txt)
```

## 7. Verify checklist (BUỘC trước khi gửi)

- `<w:tbl>` count = số bảng trong manuscript (đã loại resizebox)
- `<w:drawing>` count = số figure
- `<m:oMath>` count > 0 (equations đã thành OMML, edit được trong Word)
- Author đầu + cuối của references có trong text (refs đầy đủ)
- Mở thử bằng LibreOffice (`soffice --headless --convert-to pdf out.docx`)
  để chắc Word render được, không chỉ tin XML count.

## 8. Báo người dùng

Bao giờ cũng nói rõ:
- Bản DOCX là CONVERT từ LaTeX, không phải nguồn chính (người dùng vẫn edit
  LaTeX, mỗi lần đổi phải convert lại).
- Equations là OMML (math native Word), edit được; nhưng nếu đổi cấu trúc
  phức tạp thì sửa LaTeX rồi convert lại nhanh hơn.
- Figures là PNG embed, không phải vector; nếu venue đòi vector thì còn vấn
  đề (in tốt nhưng zoom thì pixelate ở zoom cao).
- Hỏi người dùng xem venue NHẬN PDF-từ-LaTeX hay BẮT BUỘC `.docx` mới quyết tin
  bản nào là canonical (xem `conference-submission-format-compliance.md`).
