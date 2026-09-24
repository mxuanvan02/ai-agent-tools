# Hai bản .tex: sạch (nộp) + highlight (người dùng soát) — từ MỘT bộ sections/

> Người dùng thích: text mình THÊM vào manuscript = highlight vàng để người dùng soát,
> và khi nộp thì phải có bản SẠCH không highlight. Yêu cầu điển hình:
> "làm 2 file .tex nhé, 1 cái main.tex và 1 cái highlight để người dùng đọc".

## Nguyên tắc: KHÔNG nhân đôi nội dung

Không copy nội dung ra 2 file (sẽ lệch nhau khi sửa). Thay vào đó **2 file
`main.tex` + `main_review.tex` cùng `\input` MỘT bộ `sections/`**, chỉ khác
PREAMBLE. Sửa nội dung 1 lần, cả 2 bản tự cập nhật.

## Cơ chế review-markup

Bọc mọi đoạn text mình thêm/viết lại bằng môi trường `revblock` (không dùng
`\hl{}` inline của soul cho đoạn dài — xem pitfall).

- **`main_review.tex`** (người dùng soát) — preamble định nghĩa revblock = hộp vàng:
```latex
\usepackage{soul}\sethlcolor{yellow}
\newcommand{\rev}[1]{\hl{#1}}
\usepackage{mdframed}
\newmdenv[backgroundcolor=yellow!30,linecolor=yellow!55!black,linewidth=0.4pt,
  innertopmargin=3pt,innerbottommargin=3pt,skipabove=3pt,skipbelow=3pt,
  leftmargin=0pt,rightmargin=0pt,innerleftmargin=4pt,innerrightmargin=4pt,
  splittopskip=0pt,splitbottomskip=0pt]{revblock}
```
- **`main.tex`** (nộp) — preamble định nghĩa revblock = no-op trong suốt:
```latex
\newcommand{\rev}[1]{#1}
\newenvironment{revblock}{}{}
```

Trong `sections/`, mỗi đoạn agent thêm:
```latex
\begin{revblock}
... nội dung mới ...
\end{revblock}
```

## PITFALL (đã dính lần này)

1. **soul `\hl{}` VỠ với `\cite`/`\ref`/math.** Nếu bọc đoạn có citation/cross-ref
   bằng `\hl{}` → bibtex đẻ `\citation{\hbox{}}` rác, hoặc `\soulregister{\ref}`
   gây đệ quy vô hạn "TeX capacity exceeded". → Dùng môi trường `revblock`
   (mdframed) cho đoạn dài có cite/ref; chỉ dùng `\rev{}`/`\hl{}` cho text ngắn
   thuần chữ.
2. **mdframed cắt trang**: thêm `splittopskip=0pt,splitbottomskip=0pt` để block
   vàng chảy qua ranh giới trang không bị mất chữ. Sau build kiểm "overfull vbox
   >5pt = 0" và grep text đuôi đoạn còn trong PDF.
3. **Stray brace**: khi chuyển `\rev{...}` → `\begin{revblock}...\end{revblock}`
   nhớ xóa dấu `}` đuôi còn sót.
4. **latexmk dùng .bbl cũ**: sau khi đổi .aux (đổi preamble/section), chạy đủ
   chu trình `pdflatex → bibtex → pdflatex → pdflatex`, đừng tin 1 lần build.

## Verify 2 bản
- Cả 2 build 0 undefined, đúng số trang.
- Vision-check: `main.pdf` KHÔNG vàng, `main_review.pdf` CÓ vàng (đúng thiết kế).
- `main.tex` sạch: grep 0 chỗ `\usepackage{soul}`/`{mdframed}`.
- Nhắc người dùng: text mới = highlight = YELLOW review markup, STRIP trước khi submit
  (ở đây "strip" tự động vì bản main.tex đã no-op revblock).
