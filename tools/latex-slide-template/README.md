# LaTeX Slide Template

Template LaTeX chuẩn cho slide báo cáo khoa học, phù hợp với các cuộc thi và hội nghị học thuật.

## Đặc điểm

- **Format**: Beamer 16:9, font 10pt
- **Ngôn ngữ**: Tiếng Việt (UTF-8, T5 encoding)
- **Thiết kế**: Header với logo 2 bên, màu sắc chuyên nghiệp
- **Cấu trúc**: Trang bìa → Mục lục → Nội dung → Kết luận → Q&A

## Cấu trúc thư mục

```
latex-slide-template/
├── README.md
├── template/
│   ├── SlideTemplate.tex          # File LaTeX chính
│   └── logos/
│       ├── thpt_thuan_hoa.png
│       └── dhsp_hue.png
└── examples/
    └── ieeai2026/                 # Ví dụ thực tế
        ├── slide_thuyet_minh.tex
        └── poster_AInatomy.tex
```

## Cách sử dụng

### 1. Copy template

```bash
cp -r /path/to/agent-tools/tools/latex-slide-template /your/project/
cd /your/project/latex-slide-template/template
```

### 2. Chỉnh sửa thông tin

Mở `SlideTemplate.tex` và sửa:

```latex
\title[Tên ngắn]{TÊN ĐỀ TÀI ĐẦY ĐỦ}
\subtitle{Loại báo cáo -- Tên cuộc thi}
\author[Tên tác giả]{\textbf{Chủ trì:} Tên tác giả\\
\textbf{Đơn vị:} Tên đơn vị}
\date{Thời gian}
```

### 3. Biên dịch

```bash
pdflatex SlideTemplate.tex
```

## Tùy chỉnh màu sắc

Template sử dụng 3 màu chính:

```latex
\definecolor{HUEBlue}{RGB}{0, 51, 102}      # Xanh đậm (tiêu đề, khối)
\definecolor{HUEOrange}{RGB}{212, 175, 55}  # Vàng (đường kẻ, nhấn mạnh)
\definecolor{HUEGreen}{RGB}{37, 139, 93}    # Xanh lá (thành công)
```

## Cấu trúc slide chuẩn

1. **Trang bìa**: Logo, tiêu đề, chủ trì, đơn vị
2. **Mục lục**: Các phần chính
3. **Mở đầu**: Lý do, mục tiêu, đối tượng, phạm vi, phương pháp
4. **Nội dung**: Giải pháp, triển khai, tính năng
5. **Kết quả**: Số liệu, tác động, bền vững
6. **Kết luận**: Tóm tắt, kiến nghị, tài liệu tham khảo
7. **Q&A**: Slide cảm ơn

## Ví dụ: iEEAI 2026

Xem `examples/ieeai2026/` để biết cách áp dụng template cho cuộc thi "Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026".

## Lưu ý

- **Logo**: Đặt trong thư mục `logos/`, định dạng PNG hoặc PDF
- **Font**: Sử dụng `helvet` (Helvetica) cho văn bản
- **Block**: Dùng `\begin{block}{Tiêu đề}...\end{block}` cho khối nổi bật
- **Alert block**: Dùng `\begin{alertblock}{...}` cho cảnh báo/vấn đề

## Tài liệu tham khảo

- [Beamer User Guide](https://ctan.org/pkg/beamer)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)

## License

MIT License - Tự do sử dụng và chỉnh sửa.
