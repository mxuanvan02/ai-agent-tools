# LaTeX review-markup (chữ mới = vàng) + rebuild-verify

Áp dụng khi sửa/bổ sung câu chữ vào manuscript LaTeX của người dùng. Quy ước
của người dùng: **mọi câu/đoạn MỚI phải được tô nền vàng (review markup)**, còn
đề cương/phần khóa (vd `modau.tex`) không sửa câu chữ.

## 1. Cài macro tô vàng đa dòng (soul)

`\hl` mặc định của `soul` chỉ tô 1 dòng và dễ vỡ với UTF-8/tiếng Việt +
`fontspec`. Dùng `soul` + `xcolor`, đặt màu review rồi bọc macro riêng để
dễ gỡ khi chốt bản sạch:

```latex
\usepackage{xcolor}   % (thường đã có)
\usepackage{soul}
\definecolor{reviewyellow}{RGB}{255,242,153}
\sethlcolor{reviewyellow}
\newcommand{\reviewnew}[1]{\hl{#1}}
```

Đặt SAU các package layout (đã kiểm: chèn ngay sau `\usepackage{placeins}`
ở preamble luận văn HTTT trường ĐH chạy sạch, 0 overfull, 0 soul warning).
`soul.sty` + `soulutf8.sty` có sẵn trong TeX Live (`kpsewhich soul.sty`).
Khi chốt bản cuối, chỉ cần đổi `\reviewnew` thành no-op (`\newcommand
{\reviewnew}[1]{#1}`) là bỏ hết nền vàng mà không phải gỡ từng chỗ.

Dùng: `\reviewnew{câu mới bổ sung...}` — bọc quanh câu/đoạn thêm mới.
Trong nội dung nhớ escape đúng LaTeX: `\emph{...}`, `` ``...'' `` cho ngoặc kép.

## 2. Xử lý MÂU THUẪN thay vì chèn đè

Khi tính năng mới (vd "duyệt doanh thu") chọi với narrative đang khóa của
thân luận văn (vd "người dùng KHÔNG duyệt từng dòng, AI tự chủ"):
- KHÔNG bê thẳng thuật ngữ gây chọi vào thân bài.
- Định vị lại (reframe) cho khớp cả hai: mô tả là **"điểm kiểm soát phê
  duyệt ở mức tổng hợp / kiểm soát ngoại lệ + trách nhiệm giải trình"**,
  nhấn "không phải nhập-soát thủ công từng dòng". Cách này giữ được ý AI
  tự chủ mà vẫn phản ánh tính năng.
- Sửa TẤT CẢ các đoạn chọi (không chỉ 1 chỗ): rà cả Use Case, Kiến trúc,
  Hướng dẫn demo — cùng một reframe, dùng `\reviewnew` cho phần thêm.
- Nếu reframe vẫn lệch ý đồ gốc, HỎI người dùng trước khi sửa thân bài.

## 3. Rebuild + verify (bắt buộc, có bằng chứng)

```bash
cd thesis_latex
latexmk -xelatex -interaction=nonstopmode main.tex   # exit 0
pdfinfo main.pdf | grep -E 'Pages|Page size'         # đúng số trang + A4
grep -iE '! |error|overfull' main.log                # 0 error, đếm overfull
grep -i 'soul' main.log                              # 0 soul warning
# xác nhận chữ mới thực sự vào PDF (không chỉ compile):
pdftotext main.pdf - | grep -n 'từ_khóa_đoạn_mới'
# hoặc per-page: pdftotext -f N -l N main.pdf -
```

Chuẩn "đạt": exit 0, đúng số trang, khổ A4, 0 error, 0 overfull mới,
0 soul warning, và pdftotext tìm thấy đoạn mới ở đúng trang.

## 4. Vision-check khi backend vision hỏng

Backend vision phụ trợ hay lỗi `Invalid API key`. Khi đó KHÔNG kết luận
"render đẹp" bằng mắt được → dựa bằng chứng deterministic thay thế:
- 0 overfull hbox trong log (chữ không tràn lề),
- 0 soul warning (nền vàng không vỡ),
- pdftotext xác nhận đoạn nằm đúng trang.
Báo rõ với người dùng: "chưa vision-check được vì backend lỗi; đã verify gián
tiếp bằng overfull/soul/pdftotext; người dùng mở PDF liếc giúp chỗ vàng."
(Đây là hạn chế môi trường tạm thời, không phải kết luận vĩnh viễn.)

## Pitfalls
- Đừng sửa `main.tex` khi đang xem bản pagination (partial) mà chưa nắm
  đủ ngữ cảnh — tool cảnh báo "re-read before overwrite"; patch theo
  old_string đủ context thì an toàn.
- Luôn backup `main.tex` sang `_backups/<ts>/` trước khi sửa câu chữ.
- Giữ đúng khổ A4 + không phát sinh trang trắng do float; nếu số trang
  đổi bất thường sau khi thêm đoạn, kiểm float/overfull ngay.
