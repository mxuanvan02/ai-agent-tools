# LaTeX Slide Template

Template LaTeX chuẩn cho slide báo cáo khoa học, phù hợp với các cuộc thi và hội nghị học thuật.

## Đặc điểm

- **Format**: Beamer 16:9, font 10pt
- **Ngôn ngữ**: Tiếng Việt (UTF-8, T5 encoding)
- **Thiết kế**: Header với vị trí logo 2 bên (đặt logo của bạn vào), màu sắc chuyên nghiệp
- **Cấu trúc**: Trang bìa → Mục lục → Nội dung → Kết luận → Q&A

## Cấu trúc thư mục

```
latex-slide-template/
├── README.md
├── scripts/
│   └── public_hygiene_check.py    # Cổng kiểm tra nội dung công khai
├── template/
│   ├── SlideTemplate.tex          # File LaTeX chính
│   └── logos/                     # Thư mục trống: đặt logo của bạn vào đây
└── examples/
    └── ieeai2026/                 # Ví dụ thực tế
        ├── slide_thuyet_minh.tex
        └── poster_AInatomy.tex
```

> **Logo.** Thư mục `template/logos/` để trống trong bản công khai. Template gọi
> `logos/logo_truong` và `logos/logo_truong_dai_hoc`; đặt file logo của bạn vào
> đó với đúng tên, hoặc bỏ comment dòng `\includegraphics` tương ứng trong
> `SlideTemplate.tex`.

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
\definecolor{PrimaryBlue}{RGB}{0, 51, 102}    # Xanh đậm (tiêu đề, khối)
\definecolor{AccentGold}{RGB}{212, 175, 55}   # Vàng (đường kẻ, nhấn mạnh)
\definecolor{SuccessGreen}{RGB}{37, 139, 93}  # Xanh lá (thành công)
```

## Cấu trúc slide chuẩn

1. **Trang bìa**: Logo, tiêu đề, chủ trì, đơn vị
2. **Mục lục**: Các phần chính
3. **Bức tranh toàn cảnh (Big Picture)**: Demo sản phẩm hoàn thiện (screenshot/video), liên hệ thực tế (Zalo/Messenger), câu hỏi dẫn dắt ("Điều gì xảy ra phía sau?"). Lý do: não xử lý thông tin cụ thể nhanh hơn trừu tượng — tạo "mỏ neo" trước khi đi vào khái niệm.
4. **Mở đầu**: Lý do, mục tiêu, đối tượng, phạm vi, phương pháp
5. **Nội dung**: Giải pháp, triển khai, tính năng
6. **Kết quả**: Số liệu, tác động, bền vững
7. **Kết luận**: Tóm tắt, kiến nghị, tài liệu tham khảo
8. **Q&A**: Slide cảm ơn

## Cấu trúc sư phạm (theo Gagne's 9 Events + Cognitive Psychology)

Khi báo cáo trước hội đồng/người nghe không chuyên, tuân thủ nguyên tắc **từ tổng quát đến chi tiết**:

1. **Tạo mỏ neo cụ thể** — Cho xem sản phẩm hoàn thiện (screenshot, demo, video) TRƯỚC khi giải thích kiến trúc. Người nghe cần hình dung "đầu ra" trước khi hiểu "đầu vào".
2. **Kích hoạt kiến thức nền** — Liên hệ với thứ quen thuộc (Zalo, Messenger, Uber) để tạo bối cảnh. Không bắt đầu bằng khái niệm trừu tượng.
3. **Đặt câu hỏi dẫn dắt** — "Khi gửi tin nhắn, điều gì xảy ra phía sau?" — tạo curiosity gap trước khi đi vào giải pháp kỹ thuật.
4. **Từ vấn đề → giải pháp** — Trình bày vấn đề trước, sau đó mới đưa giải pháp. Không đưa giải pháp rồi mới giải thích vấn đề.

Trong Beamer: thêm section "Bức tranh toàn cảnh" ngay sau mục lục, trước "Mở đầu", với 2 slide: (a) screenshot sản phẩm + caption ngắn + câu hỏi dẫn dắt; (b) sơ đồ luồng hoạt động tổng quan (TikZ đơn giản: 2 actor + 2 mũi tên Send/Recv).

**Lưu ý TikZ trong Beamer**: KHÔNG dùng `\resizebox{\textwidth}{!}{...}` cho diagram cao (>12 đơn vị TikZ) — co quá mức làm diagram biến mất hoặc render sai. Đơn giản hóa diagram (bỏ note box, chỉ giữ actor + mũi tên ngang) thay vì resize.

## Ví dụ: iEEAI 2026

Xem `examples/ieeai2026/` để biết cách áp dụng template cho cuộc thi "Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026".

## Lưu ý

- **Logo**: Đặt trong thư mục `logos/`, định dạng PNG hoặc PDF
- **Font**: Sử dụng `helvet` (Helvetica) cho văn bản
- **Block**: Dùng `\begin{block}{Tiêu đề}...\end{block}` cho khối nổi bật
- **Alert block**: Dùng `\begin{alertblock}{...}` cho cảnh báo/vấn đề

## Kiểm tra trước khi phát hành

```bash
# Quét nội dung công khai (tên cơ quan, đường dẫn nội bộ, khoá bí mật)
python3 scripts/public_hygiene_check.py

# Biên dịch thử
pdflatex SlideTemplate.tex
```

Cổng `public_hygiene_check.py` là bản sao giống hệt của cổng dùng chung trong
toàn repo. Nếu bạn thêm tên cơ quan vào template, hãy kiểm tra lại bằng cổng ấy.

## Tài liệu tham khảo

- [Beamer User Guide](https://ctan.org/pkg/beamer)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)

## License

MIT License - Tự do sử dụng và chỉnh sửa.
