# Jev System-One: Claim-Check và Confidence Gate (MCP jevbridge)

Máy người dùng có sẵn MCP `jevbridge` (tool: `mcp__jevbridge__jev_decide`, `jev_gate`, `jev_recipe`). Backend `auto` → dùng Jev thật khi `TYPESAFE_API_KEY` có sẵn, fallback LLM adapter. Đây là System-One đúng nghĩa docs TypeSafe: trả typed judgment + probability, không sinh chữ.

## Khi nào dùng

1. **Stage 3/7 — đối chiếu claim ↔ bằng chứng:** mỗi câu khẳng định có trích nguồn trong bản thảo, chạy 1 call noul so claim với source verbatim → phát hiện "nói quá"/ngụy tạo số liệu trước khi submit. Đây là pattern *citation check* trong cookbook TypeSafe.
2. **Trước hành động không đảo ngược** (xóa file, gửi bài, publish, destructive-gate): gọi `jev_gate` để lấy execute/confirm/escalate/abort thay vì tự quyết; ngưỡng theo rủi ro (destructive cần bar cao hơn read-only).
3. **Route/phân loại đúng-sai đơn giản:** dùng jev_decide thay vì bắt LLM sinh chữ tự phân loại (rẻ hơn, nhanh hơn, có số đo được).

## Cách gọi

`tool_call` → `mcp__jevbridge__jev_decide` — **MỖI LẦN MỘT CALL** (local tool không batch nhiều entry trong 1 tool_call; muốn song song thì gửi nhiều tool_call độc lập cùng lượt).

```json
{
  "backend": "auto",
  "gate": true,
  "state": {
    "claim": "<câu khẳng định trong bài, giữ nguyên văn>",
    "source": "<bằng chứng verbatim: đoạn docs, dòng bảng số liệu, abstract paper gốc>"
  },
  "questions": {
    "claim_matches_source": {
      "type": "noul",
      "instructions": "Does the claim stay within what the source actually supports? true = the claim's certainty level matches the source; false = the claim overstates the source.",
      "criteria": {
        "true": "Claim is consistent with the source's stated scope of guarantees",
        "false": "Claim asserts stronger guarantees than the source provides"
      }
    }
  }
}
```

## Ngưỡng 3 dải (đo thật trên jev-1.13.0, 2026-09-24)

- `noul ≥ 0.8` → claim khớp source: pass.
- `noul ≤ 0.2` → claim nói quá/sai source: **BLOCK**, sửa claim hoặc bổ sung bằng chứng.
- `0.2–0.8` → escalate: người hoặc LLM đọc lại. KHÔNG auto-pass (noul ~0.5 = model thật sự không chắc, đó là tín hiệu hữu ích chứ không phải lỗi).

Ba ca kiểm chứng đã chạy (backend=jev, jev-1.13.0):

| Ca | noul | token in/out | latency |
|---|---|---|---|
| Nói quá "độ tự tin chính xác tuyệt đối" vs docs ghi calibration chỉ đo trên nhóm, không đảm bảo từng câu trả lời | **0.03** (gate 0.94 execute) | 470/22 | 363ms |
| Nói quá "accuracy 0.94 chứng minh độ chính xác tuyệt đối" vs bảng 0.94 + Limitations ghi 6% lỗi | **0.04** | 411/22 | 270ms |
| Paraphrase ĐÚNG source + thêm suy luận của mình ("nên cần ngưỡng theo rủi ro" — source không nói) | **0.58** (dải giữa) | 439/22 | 374ms |

## Bài học (đã trả giá bằng số thật)

1. **Claim phải đóng khung trong source.** Paraphrase đúng nhưng cài thêm inference của mình → rơi dải giữa (0.58) dù không sai. Tách inference thành claim riêng với source riêng (docs khác) nếu muốn giữ.
2. **Ghi lại backend trong kết quả.** `"backend": "jev"` mới là số calibrated; LLM adapter (khi thiếu TYPESAFE_API_KEY) không được huấn luyện calibration — đừng dùng ngưỡng 0.8/0.2 cho adapter mà không đo lại.
3. **ROI:** ~400–500 token in, <400ms/call → chạy song song nhiều claim độc lập OK cho bước rà cuối (Stage 7) và claim table (Stage 4). KHÔNG gắn vào mọi câu văn — âm ROI.
4. **Jev chỉ nhận text** (chưa hỗ trợ ảnh/audio). Bảng số liệu/hình phải chuyển thành text/JSON trong state trước.
5. **Calibration đo trên nhóm, không đảm bảo từng câu đúng** (docs TypeSafe) → pass noul cao ≠ chân lý; với claim hệ trọng vẫn đối chiếu nguồn gốc như quy trình cũ.
6. `jev_recipe` có sẵn 4 recipe mẫu (support-route, computer-use, destructive-gate, compaction) — xem để học protocol trước khi tự lắp câu hỏi.
