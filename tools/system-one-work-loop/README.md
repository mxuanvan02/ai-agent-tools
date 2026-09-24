# System-One Work Loop

Agent Skill: vòng lặp công việc tự chủ **plan → build → check → gate**, trong đó một
System-One model (TypeSafe Jev qua MCP `jevbridge`, fallback offline `laya`) làm VAN
quyết định sau mỗi bước: `execute` → agent im lặng làm tiếp, `confirm/escalate/abort`
→ mới ngắt về người dùng. Người dùng giao task ≥3 bước rồi rời đi; agent chỉ quay lại
khi **xong** (kèm bằng chứng verify được) hoặc **kẹt/cần xác nhận**.

> Nguyên tắc lõi (điều khiển học 2 tầng): System-One giữ tầng THỰC THI ("còn cách
> đích bao xa"), người dùng giữ tầng PHÁN XÉT ("đích có đúng không, nghiệm thu cuối").
> Loop mở PR/bản nháp nhưng KHÔNG BAO GIỜ tự merge/publish/gửi/tiêu tiền.

## Điểm nổi bật

- **Default-on** cho multi-step work trong SKILL.md: điều kiện kích hoạt + điều kiện
  từ chối chạy loop (goal không máy-chấm-được → STOP, không chạy).
- **Front-load một lần trước khi chạy** (chặn failure mode "loop không hỏi giữa chừng"):
  goal máy-chấm-được, boundaries chống Goodhart, ngưỡng escalate theo rủi ro, retry cap.
- **Gate recipe đo được**: JSON mẫu `jev_decide`/`jev_gate` (choice `progress` 5 hướng +
  noul `boundary_ok`), mapping verdict, kèm benchmark laya-vs-Jev thật trên CPU
  (i5-12400: verdict 3 dải trùng 3/3, 236–320ms/call; laya uncalibrated → chỉ làm
  fallback không gián đoạn).
- **Criteria templates by domain** (`references/criteria-templates-by-domain.md`):
  4 góc nhìn bất biến Requester/Builder/Verifier/Operator (thiếu góc nào = bộ tiêu chí
  chưa đủ), giải phẫu 6 thành phần, và 5 template điền sẵn: phần mềm/website
  (PM–Dev–Tester–Ops), nghiên cứu học thuật, nội dung/hành chính/giảng dạy,
  dữ liệu/ETL, website dồn từ nguồn có sẵn (Notion/CMS). Kèm 5 bẫy soạn tiêu chí.
- **Dispatch patterns** 3 mức tự động: loop trong một turn (mặc định) → subagent song
  song → cron/background (chỉ khi đã tin), kèm skeleton tài liệu-điều-phối cho việc
  dạng maintenance.

## Cấu trúc

```
SKILL.md                                  — quy trình loop + ranh giới cứng + checklist 5 kiểu loop chết
references/gate-recipe.md                 — JSON mẫu gọi Jev/jevbridge + laya fallback (offline)
references/criteria-templates-by-domain.md— khung tiêu chí theo ngữ cảnh (4 góc, 6 thành phần, 5 template)
references/dispatch-patterns.md           — 3 mức dispatch + skeleton doc-driven
scripts/public_hygiene_check.py           — cổng vệ sinh public (không token cá nhân/đường dẫn nội bộ)
```

## Kiểm tra vệ sinh public

```bash
python3 scripts/public_hygiene_check.py
```

## Cài đặt

Copy thư mục này vào skills dir của agent (vd `~/.hermes/skills/orchestration/`),
hoặc dùng trình quản lý skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

Yêu cầu để gate chạy đúng nghĩa: MCP `jevbridge` (+ `TYPESAFE_API_KEY`) cho Jev;
tùy chọn `laya` (pip, CPU được) cho fallback offline.

## License

MIT — xem [LICENSE](LICENSE).
