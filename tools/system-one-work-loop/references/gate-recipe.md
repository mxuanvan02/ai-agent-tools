# System-One gate recipe (Jev primary, laya fallback)

## Jev qua MCP jevbridge (PRIMARY)

### Cách A — jev_decide rồi tự map

`tool_call` → `mcp__jevbridge__jev_decide`, MỘT call mỗi vòng:

```json
{
  "backend": "auto",
  "gate": true,
  "state": {
    "goal": "<tiêu chí xong máy-chấm-được>",
    "boundary": "<những gì KHÔNG được làm>",
    "last_step": "<agent vừa làm gì>",
    "check_result": "<kết quả nghiệm thu xác định: pytest/build/diff/claim-gate>",
    "retries_used": 1
  },
  "questions": {
    "progress": {
      "type": "choice",
      "instructions": "Given the goal, boundary, the step just done and its deterministic check result, what should the loop do next?",
      "criteria": {
        "continue": "Check passed and more steps remain; proceed to the next step",
        "done": "All done-criteria are met and the goal is fully satisfied",
        "confirm": "Next step is a high-risk/irreversible action (delete, merge, publish, send, production) - ask the user first",
        "escalate": "Check failed, ambiguous, blocked, or retry cap reached - hand back to the user with the reason",
        "abort": "A boundary was violated or the goal is unreachable - stop"
      }
    },
    "boundary_ok": {
      "type": "noul",
      "instructions": "Did the step just done stay within the stated boundary (did NOT do any forbidden thing)?",
      "criteria": {"true": "Stayed within boundary", "false": "Violated the boundary"}
    }
  }
}
```

Map kết quả:
- `boundary_ok` noul ≤ 0.5 → **abort** ngay (nghi phạm ranh giới), bất kể `progress`.
- `progress=continue` + gate confidence cao → **execute** (im lặng làm tiếp).
- `progress=done` → goal met → gói kết quả, BÁO CÁO, KHÔNG tự merge/publish.
- `progress=confirm` → nhắn người dùng xác nhận.
- `progress=escalate` HOẶC gate confidence thấp (dải giữa) → **escalate** người dùng.
- `progress=abort` → dừng.

### Cách B — jev_gate trực tiếp

`mcp__jevbridge__jev_gate` nhận `answers` từ jev_decide + các ngưỡng
(`executeAbove`, `confirmAbove`, `abortBelow`, `abortChoices`, `doneChoices`)
→ trả execute/confirm/escalate/abort. Đặt `doneChoices=["done"]`,
`abortChoices=["abort"]`, `destructiveId` trỏ vào noul đánh dấu thao tác nguy hiểm.

## laya fallback (OFFLINE, khi Jev không sẵn)

Cài trong venv riêng, torch CPU-only, model cache trên ổ dữ liệu (placeholder `<venv>`, `<hf-cache>`):

```bash
python3 -m venv <venv>
<venv>/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch
<venv>/bin/pip install laya
# chạy: HF_HOME=<hf-cache> LAYA_DEVICE=cpu <venv>/bin/python ...
```

API giống Jev: `agent.system_one(state=..., questions={...})`, noul ở `answers[id]["noul"]`.

```python
import laya
agent = laya.load("convaiinnovations/laya", device="cpu")  # cold-load CPU ~228s — LÀM 1 LẦN
res = agent.system_one(state=STATE, questions=QUESTIONS)
```

PHẢI chạy dạng server thường trú (`laya serve` / `LAYA_DEVICE=cpu laya-mcp-server`),
không `laya.load()` lại mỗi vòng. laya = KHÔNG GIÁN ĐOẠN, không phải nguồn quyết
rủi ro cao (checkpoint tự khai uncalibrated); thao tác không-đảo-ngược vẫn chờ
Jev hoặc người dù laya nói execute.

Benchmark thật i5-12400 (2026-09-24): verdict 3 dải trùng Jev 3/3, latency
236–320ms/call. Script benchmark tái lập nằm trong môi trường maintainer (`<bench-dir>/bench.py`, kết quả `result.json`); tự viết lại theo API ở trên nếu cần tái tạo.
