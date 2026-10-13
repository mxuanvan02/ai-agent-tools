# Vietnamese Classroom Slide Production

Agent Skill: dựng và phát hành **bộ slide bài giảng THPT bằng tiếng Việt** — từ đề
cương/kế hoạch bài dạy thành deck PPTX hoàn chỉnh, qua chuỗi cổng QA **đo được**,
rồi phát hành cặp PPTX/PDF và kiểm tra hậu kỳ bằng checksum.

> Nguyên tắc lõi: **CỔNG ≠ NỘI DUNG**. Một deck đạt mọi cổng hình thức vẫn có thể
> bị giáo viên chấm 3/10 vì rỗng — không có gì để thầy đứng nói, không có gì để
> học trò thực hành. Mọi cổng chỉ là phương tiện kiểm, không phải mục tiêu.

## Điểm nổi bật

- **Ảnh thao tác thật, không ảnh minh hoạ.** Chụp bằng xterm + REPL thật trên
  Xvfb (Inkscape/Python/LibreOffice), kèm OCR verify từng ảnh so với ground truth
  tính bằng lệnh — ảnh nói sai số là lỗi nặng hơn ảnh xấu.
- **Công thức cỡ chữ khi chiếu** `pt = 72 × line_px × band_h / H_final`: ảnh càng
  nhiều dòng chữ càng nhỏ; upscale KHÔNG tăng pt, đòn bẩy thật là crop hẹp và
  chia cột tại khe trắng giữa hai dòng.
- **Cổng hình học import ngưỡng từ chuẩn nhà**, không tự đặt số — tự đặt
  `FOOTER_Y` từng khiến caption bị phân loại thành chân trang và báo oan 8/10 slide.
- **Đo trên bản render PDF, không đo rect trong file**: toàn bộ textbox là
  `spAutoFit` nên rect lưu trong file là rect CŨ; mọi cổng đọc rect đều mù với
  phần box tự nới.
- **Peer review độc lập bắt buộc trước khi báo đạt**: rubric trích nguyên văn lời
  giáo viên, cộng một reviewer đóng vai học sinh — bắt được lỗi ngữ nghĩa mà
  không cổng đo nào thấy (legend ghi sai loại nhãn đọc to, caption ngược với ảnh).

## Cấu trúc

```
SKILL.md                                        — quy trình dựng → QA → phát hành, kèm các pitfall đã trả giá
references/content-and-language.md              — chuẩn nội dung, ngôn ngữ tiếng Việt, thuật ngữ
references/programming-lesson-content-and-qa.md — slide bài lập trình: nội dung + QA riêng
references/icon-embedding-and-measurement-qa.md — nhúng icon, đo đạt bằng số
references/requirement-traceability-and-visual-qa.md — vết yêu cầu ↔ slide, QA thị giác
references/knowledge-example-visual-repair.md   — sửa ví dụ/hình minh hoạ kiến thức
references/deck-rebuild-script-pitfalls.md      — bẫy khi dựng lại deck bằng script
references/clone-contamination-guard.md         — chống nhiễm chéo giữa các deck cùng họ
references/qa-and-release.md                    — cổng QA + quy trình phát hành
references/series-migration-and-release.md      — di chuyển cả bộ slide + phát hành
references/2026-09-*.md                         — nhật ký ba đợt batch (bài học theo lô)
scripts/public_hygiene_check.py                 — cổng vệ sinh public (byte-identical với các tool khác)
```

## Kiểm tra vệ sinh public

```bash
python3 scripts/public_hygiene_check.py
```

Cổng này quét token cá nhân, đường dẫn nội bộ và mã dự án chưa công bố. Bản copy
trong repo đã được generic hoá đường dẫn (`$HOME`, `<work-dir>`, `<venv-python>`);
bản cài đặt cục bộ của người dùng giữ đường dẫn thật để chạy được.

## Cài đặt

Copy thư mục này vào skills dir của agent (vd `~/.hermes/skills/education/`),
hoặc dùng trình quản lý skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

Yêu cầu runtime: `python-pptx`, PyMuPDF (`fitz`), Pillow, NumPy;
`rapidocr-onnxruntime` cho OCR verify ảnh; LibreOffice (`soffice --headless`) để
xuất PDF; `xterm` + Xvfb để chụp ảnh thao tác thật.

## License

MIT — xem [LICENSE](LICENSE).
