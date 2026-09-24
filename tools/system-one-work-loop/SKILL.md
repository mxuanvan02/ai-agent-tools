---
name: system-one-work-loop
description: "Use when handed a multi-step task to run autonomously."
metadata:
  version: "1.0.0"
  license: "MIT"
  status: active
  default_on: true
  related: "loop-design-check; jev-systemone-claim-gate (evidence-first-research)"
---

# System-One Work Loop

> Thay vì người dùng ngồi canh từng bước rồi nhắn "làm tiếp", agent tự chạy vòng
> plan → build → judge, dùng **System-One làm van quyết định** (tiếp tục im lặng /
> hỏi / báo / dừng), và **chỉ ngắt về người dùng khi thật sự cần**. Người dùng
> vẫn giữ quyền phán xét mục tiêu và nút bấm cuối.

## MẶC ĐỊNH BẬT

Khi người dùng giao một task ≥3 bước rồi rời đi (không ngồi canh), agent TỰ ĐỘNG
áp dụng loop này — không cần người dùng gọi tên skill. Điều kiện kích hoạt:
task lặp/nhiều bước + nghiệm thu tự động được + có tool chạy-và-thấy-kết-quả.
Nếu THIẾU 1 điều kiện (đặc biệt: nghiệm thu KHÔNG máy-chấm-được) → KHÔNG chạy
loop, làm tay từng bước như cũ và nói rõ vì sao.

## Ranh giới cứng (điều khiển học 2 tầng — KHÔNG được vi phạm)

| Tầng | Ai giữ | Nội dung |
|---|---|---|
| Thực thi (thấp) | agent + System-One | "còn cách đích bao xa, làm tiếp gì" — máy mạnh, giao được |
| **Phán xét (cao)** | **NGƯỜI DÙNG** | "mục tiêu có ĐÚNG không, đổi/dừng không, nghiệm thu cuối" — KHÔNG giao máy |

System-One là cái VAN trong tầng thực thi, KHÔNG phải quan nghiệm thu. Ô "DONE"
cuối cùng chỉ người dùng lật. Giao nút cuối cho máy = gỡ tầng phán xét = nó lao
hết mình về một đích không ai soát lại.

## Bước 0 — Front-load (làm MỘT LẦN trước khi vào loop)

Loop sẽ KHÔNG dừng lại hỏi giữa chừng (failure mode #4: nó chạy đáp án sai tới
cùng). Nên chốt hết TRƯỚC khi chạy:

1. **Goal máy-chấm-được.** Viết tiêu chí "xong" mà một lệnh chấm yes/no được.
   - Tệ: "làm cho tốt / rà cho kỹ". Tốt: "build sạch + 0 undefined ref + mọi
     claim có nguồn pass claim-gate + diff so golden < 0.01".
   - Tự kiểm: đọc goal cho người ngoài ngành — họ chạy 1 lệnh biết xong chưa? Không → chưa đủ, viết lại.
2. **Ranh giới "KHÔNG được làm gì"** (kháng Goodhart). Vd: không xóa/nới test,
   không giảm coverage, không sửa tiêu chí nghiệm thu, không đụng deployed path.
3. **Ngưỡng escalate theo rủi ro** (xem bảng dưới).
4. **Retry cap** N (mặc định 3) → quá thì escalate người dùng, không quay vô hạn.
5. Mọi câu hỏi mơ hồ → hỏi NGAY BÂY GIỜ, một lượt, rồi mới chạy.

Nếu goal chưa máy-chấm-được sau khi cố → STOP, báo người dùng, đừng chạy loop.

**Đừng soạn tiêu chí từ trang trắng:** dùng khung sườn theo ngữ cảnh trong
`references/criteria-templates-by-domain.md` — 4 góc nhìn bất biến
(Requester/Builder/Verifier/Operator, thiếu góc nào = chưa đủ) + 6 thành phần của
một bộ tiêu chí + template điền sẵn cho: phần mềm/website (PM/dev/tester/ops),
nghiên cứu học thuật, nội dung/hành chính/giảng dạy, dữ liệu pipeline, website
dồn từ nguồn có sẵn (Notion/CMS). Phần không máy-chấm-được (gu thẩm mỹ, tính sư
phạm, "hay") PHẢI khai báo và route lên người dùng, không để agent tự chấm.
Bộ tiêu chí soạn xong phải được người dùng DUYỆT trước khi loop chạy.

## Vòng lặp — plan / build / judge

```
plan   : bẻ goal thành các bước + tiêu chí nghiệm thu máy-chấm-được (làm 1 lần)
repeat until done OR retry cap:
  build : agent làm bước kế (viết code, sửa bản thảo, chạy lệnh...)
  check : chạy nghiệm thu XÁC ĐỊNH (pytest / build log / diff / claim-gate) — KHÔNG "trông ổn"
  gate  : System-One đọc (goal, tiêu chí, kết quả check) -> execute|confirm|escalate|abort
        execute  -> làm tiếp bước sau, IM LẶNG (không nhắn người dùng)
        confirm  -> nhắn người dùng xác nhận rồi mới đi tiếp (thao tác rủi ro)
        escalate -> dừng bước này, báo người dùng kèm lý do + trạng thái
        abort    -> dừng loop, báo người dùng
goal met -> mở PR / tạo bản nháp / gói kết quả; BÁO CÁO; KHÔNG tự merge/publish/gửi
```

Ba luật sắt (đều cược vào judge):
1. **Judge độc lập** — nghiệm thu KHÔNG do chính agent vừa build tự chấm; dùng
   lệnh xác định (pytest/diff/build/claim-gate) + System-One gate trên kết quả đó.
2. **Luật xác định** — không bao giờ "trông có vẻ đúng".
3. **Build KHÔNG được sửa tiêu chí nghiệm thu để pass.**

## System-One làm van — cách gọi

Primary: MCP `jevbridge` → `jev_gate` (đọc answers từ `jev_decide`) trả
execute/confirm/escalate/abort. Hoặc `jev_decide` một choice/noul rồi tự map.
Một call/vòng (~450 token, <400ms). Recipe đầy đủ: `references/gate-recipe.md`.

Fallback offline (Jev nghẽn / thiếu TYPESAFE_API_KEY / dữ liệu nhạy cảm): **laya**
(Apache-2.0, `convaiinnovations/laya`, chạy CPU). Benchmark thật i5-12400:
verdict 3 dải trùng Jev 3/3, latency 236–320ms, nhưng noul kém dứt khoát và
checkpoint tự khai "uncalibrated" → laya chỉ để KHÔNG GIÁN ĐOẠN, quyết định rủi
ro cao vẫn chờ Jev hoặc người. Chi tiết: `references/gate-recipe.md`.

## Ngưỡng escalate theo rủi ro (đặt ở Bước 0)

| Loại hành động | Ngưỡng | Mặc định |
|---|---|---|
| Đọc/chạy test/lint/build (đảo ngược được) | thấp | execute tự do |
| Sửa file/cài dep/đổi config | trung bình | execute nếu check pass, log rõ |
| Xóa dữ liệu / force-push / merge / publish / gửi đi / production | **cao** | LUÔN confirm hoặc escalate — KHÔNG execute tự động dù confidence cao |

Confidence cao KHÔNG phải giấy phép hành động: calibration đo trên nhóm, không
đảm bảo từng câu đúng. Với hành động không-đảo-ngược-được, bar phải cao hơn hẳn.

## 5 kiểu loop chết — checklist tự soát trước khi chạy

1. Goal là khẩu hiệu → quay đốt token. → goal máy-chấm-được.
2. "Verify" = "trông ổn", agent tự khen tự dừng. → judge độc lập + luật xác định.
3. (tệ nhất) chỉ gate "pass hết test" → agent xóa test. → đích KÈM ranh giới.
4. Trông chờ nó hỏi giữa chừng → nó không hỏi. → front-load hết ở Bước 0.
5. Doc/memory cũ → càng loop càng sai. → dùng trạng thái tươi, không tin ký ức.

## Ba lằn ranh đỏ (vi phạm = KHÔNG được full-auto)

- **Phán xét ở người dùng.** Nghiệm thu cuối / ô DONE do người lật. Loop là thợ, không phải quan nghiệm thu.
- **Trách nhiệm không chuyển giao.** Việc mà thất bại không gánh nổi (merge nhầm PR, publish nhầm, tiêu tiền sai) → KHÔNG giao quyền tự động.
- **Càng tự-sửa-luật càng phải soát chặt** — không phải lỏng hơn. Chốt chặn của người phải nằm TRƯỚC hành động, không phải vá sau.

## Tiếp đất 3 bước (đừng full-auto ngày đầu)

1. Chạy TAY 1 lần một task thật (buộc phát biểu rõ "judge chấm bằng gì").
2. Đóng thành loop dispatch trong 1 turn agent (nhiều tool call, gate mỗi vòng).
3. Treo cron/subagent full-auto khi đã tin — xem `references/dispatch-patterns.md`.

## Báo cáo cho người dùng — khi nào & thế nào

- **Im lặng** khi gate=execute (làm tiếp, không nhắn).
- **Nhắn** khi: confirm (xin xác nhận), escalate (kẹt/mơ hồ/quá retry cap),
  abort (dừng), hoặc GOAL MET (xong, kèm kết quả verify được + việc chờ người lật).
- Báo cáo dạng: trạng thái hiện tại → việc đã xong (có bằng chứng: log/diff/số) →
  việc còn lại hoặc nút chờ người dùng bấm. Không recap dài.
