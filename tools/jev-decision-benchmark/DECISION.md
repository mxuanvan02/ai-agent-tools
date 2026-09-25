# Jev trong Hermes Harness — Trang quyết định

_Cập nhật: sau 2 PoC chạy live (guardian + monitor). Bản ghi do agent Hermes soạn cho người bảo trì repo này._

## TL;DR

Jev (TypeSafe System One) khớp với các **điểm quyết định ngữ nghĩa** trong harness
Hermes — nơi code hiện gọi "auxiliary LLM ra một phán đoán rồi parse lại". Đối chứng
đầy đủ với Qwen3.8-max (qua omniproxy) cho kết quả **phân cực rõ theo loại cổng**:

- **Guardian/verify (quyết định atomic, đường nóng): Jev THẮNG** — nhanh ~15x
  (957ms vs 14.4s/call), token ít ~40%, accuracy nhỉnh, fail-closed hơn.
- **Monitor/triage (chấm điểm batch, ngữ cảnh rộng): Qwen THẮNG** — accuracy cao hơn
  (MAE 0.85 vs 1.22), token ít hơn ~3x (batch 1 call vs Jev 20 call).

Đúng như lý thuyết TypeSafe: Jev mạnh ở quyết định nhỏ/độ-trễ-thấp/khối-lượng-lớn,
thua ở batch-scoring cần hiểu ngữ cảnh rộng. Jev KHÔNG thay được bước *sinh nội dung*.
Còn treo: xác nhận latency Qwen 14s (bất thường hay thật) và chi phí tiền/tháng.

---

## 1. Ranh giới: Jev làm được gì / không

| | Jev thay được | Vì sao |
|---|---|---|
| Chấm điểm / xếp hạng (Score) | ✅ | trả số + confidence hiệu chỉnh |
| Chọn 1 trong tập (Choice) | ✅ | phân phối xác suất typed |
| Đúng/sai (Noul) | ✅ | xác suất yes |
| Sinh văn bản (skill, tóm tắt, title) | ❌ | Jev không generate |
| Nhận ảnh/audio/video | ❌ | text-only |
| Gọi tool / tự đi web | ❌ | không phải agent |

Nguyên tắc: **ở đâu bước phụ là chấm/chọn/đúng-sai → Jev; ở đâu là sinh chữ → giữ LLM.**

---

## 2. Kết quả thật (Jev live, jev-1.13.0)

### Cổng A — Smart-approval guardian (30 lệnh shell) — 3-WAY đối chứng

| Chỉ số | Pattern | Qwen3.8-max | Jev (v2) |
|---|---|---|---|
| accuracy | 0.467 | 0.800 | **0.833** |
| dangerous-miss | 0 | **0** | **0** |
| false-deny | 0 | 0 | 0 |
| auto-approve | 0.0 | 0.467 | 0.367 |
| escalate-rate | 0.70 | 0.10 | 0.267 |
| latency TB/call | ~0 | 14.398 s | **957 ms** |
| total-tokens | 0 | 31.378 | **18.342** |

- **Jev thắng cả 3 chiều:** nhanh ~15x, token ít ~40%, accuracy nhỉnh. Guardian nằm
  trên đường nóng mỗi lệnh shell → 14s/lệnh của Qwen là không dùng được, 1s thì OK.
- Cả Qwen và Jev đều **0 dangerous-miss**, chặn sạch 2 ca prompt-injection.
- Khác biệt hành vi: Qwen thiên auto-approve (approve cả `git reset --hard`, `sudo`,
  `truncate` — ca cần hỏi người). Jev thiên escalate → đúng hướng fail-closed của anh.
- ⚠️ Latency Qwen 14s qua omniproxy có thể bất thường (routing/tải) — cần đo lại vài
  lần trước khi chốt con số "nhanh 15x".

### Cổng B — Monitor/triage (20 item, threshold ≥7, so nhãn người) — đối chứng

| Chỉ số | Jev | Qwen3.8-max |
|---|---|---|
| MAE (thang 0–10) | 1.22 | **0.85** |
| surface F1 | 0.875 | **0.941** |
| precision | 1.0 | 1.0 |
| recall | 0.778 | **0.889** |
| parse-failures | 0 | 0 |
| total-tokens | 9.080 | **3.095** |

- **Qwen thắng:** accuracy cao hơn (MAE 0.85 < 1.22), token ít hơn ~3x. Lý do: monitor
  gộp được 20 item vào 1 batch call (Qwen), trong khi Jev phải 20 call riêng (mỗi item
  1 Score) → tốn token hơn dù mỗi call nhỏ.
- Cả hai precision 1.0 (0 báo động giả) và 0 parse-failure trên tập này. Tầng parse
  mong manh của `classify_items.py` là *rủi ro tiềm tàng*, không phải lỗi thực tế ở đây.
- Kết luận: monitor/triage là **sân của LLM sinh chữ**, giữ Qwen.

---

## 3. Bốn cổng tự động của Hermes — xếp ưu tiên tích hợp

Mọi cổng có cùng hình dạng: **code giữ control-flow + 1 bước auxiliary-LLM quyết định.**

| # | Cổng | File | Jev primitive | Ưu tiên | Ghi chú |
|---|---|---|---|---|---|
| 1 | **Smart-approval** | `tools/approval_smart.py` | Score→verdict | **Cao nhất** | Đối chứng: Jev thắng (nhanh 15x, token ít 40%, fail-closed). Đường nóng → độ trễ thấp là quyết định |
| 2 | Kanban routing | `cron/` dispatcher | Choice (task→profile) | TB | Quyết định atomic → sân Jev, nhưng đụng dispatcher (rủi ro cao) |
| 3 | Curator merge-decision | `agent/curator.py` | Noul (trùng lặp?) | TB | Chỉ chèn phần *quyết định*; *viết* bản gộp vẫn LLM |
| ✗ | Monitor/triage | `cron/scripts/classify_items.py` | Score 0–10 | **Bỏ** | Đối chứng: Qwen thắng (accuracy cao hơn, token ít 3x). Giữ Qwen |

**Đảo ngược so với giả định ban đầu:** trước khi đối chứng em xếp monitor #1. Số thật
cho thấy monitor là sân LLM (batch, ngữ cảnh rộng), guardian mới là sân Jev (atomic,
đường nóng). Bài học: KHÔNG xếp ưu tiên trước khi có số đối chứng head-to-head.

Curator: phần archive theo thời gian đã là pure/no-LLM — **giữ nguyên**. Chỉ chèn Jev
vào bước *quyết định gộp skill nào*, còn *viết* bản gộp vẫn là LLM.

---

## 4. Việc còn treo (phải làm trước khi tích hợp thật)

1. **Baseline Qwen vs Jev** — BLOCKED: upstream SOTA MINH `INSUFFICIENT_BALANCE`.
   `qwen3.8-max` chỉ tới được qua omniproxy → hết số dư. Cần nạp balance rồi chạy lại
   `monitor/_run_baseline_with_gwkey.py` + guardian `--real` đối chứng.
2. **Latency Jev ~1.3s/call** — cao hơn docs (~150ms). Cần điều tra: cold start? region?
   dùng SDK chính thức có connection pooling thay urllib? Đây là chặn thực tế cho cổng
   approval (đường nóng); với monitor (chạy nền) thì chấp nhận được.
3. **Chi phí thật** — ~600 tok/call. Tính ra tiền/tháng theo usage thật, so Qwen aux.

---

## 5. Đường tích hợp (KHÔNG đụng core Hermes)

Rubric core Hermes cấm SaaS bên thứ ba vào cây nguồn ("Third-party products ... Ship
as a standalone plugin repo"). Jev = vendor riêng (`api.typesafe.ai`, `TYPESAFE_API_KEY`,
billing riêng, không qua 9router). Nên:

- **Plugin Hermes độc lập** tại `~/.hermes/plugins/` — hoặc thử nghiệm trong fork riêng.
- Adapter riêng: Jev nói `POST /v1/systemone` (state + typed questions), KHÔNG nói
  OpenAI chat/completions — không cắm như provider phụ được.
- Fail-closed giữ nguyên: Jev lỗi/không chắc → escalate/giữ hành vi an toàn cũ.

---

## 6. Khuyến nghị (sau đối chứng)

Bắt đầu bằng **Smart-approval guardian** — cổng duy nhất Jev thắng đối chứng, và thắng
ở đúng thứ quan trọng cho đường nóng: độ trễ (957ms vs 14.4s), token (ít 40%), và
hướng fail-closed. PoC v2 đã sẵn (`src/guardian.py`). Đường tích hợp = plugin Hermes
riêng thay guardian trong `tools/approval_smart.py`.

**Bỏ monitor/triage** — Qwen thắng rõ, giữ nguyên.

Trước khi build plugin:
1. Đo lại latency Qwen guardian 3–5 lần để xác nhận 14s là thật hay nhiễu omniproxy.
2. Đo latency Jev vài lần (đã thấy dao động 957ms–1.3s) để có SLA đáng tin.
3. Tính chi phí Jev tiền/tháng theo tần suất lệnh shell thật của anh.

---

## 7. TÍCH HỢP THẬT — Jevbridge làm MCP server (đã verify)

Thay vì tự viết plugin từ đầu, dùng **Jevbridge** (github.com/tacticocc/Jevbridge, MIT,
zero-dep Node) — adapter phơi Jev qua MCP. Hermes có sẵn MCP client → không đụng core.

**Đã làm & verify:**
- Clone về một path ổn định ngoài `/tmp` (commit d4e8f7d).
- Test offline: 43/43 pass. Test MCP stdio với Jev THẬT: `jev_decide` trên
  `rm -rf ./data/ledger && git push --force` → is_destructive 0.94, gate=**abort**,
  jev-1.13.0, latency 1115ms.
- Thêm khối `mcp_servers.jevbridge` vào `config.yaml` (đã backup
  `config.yaml.bak-20260922-120251`), YAML verify hợp lệ.
- Xác nhận `${TYPESAFE_API_KEY}` resolve qua `_interpolate_env_vars` (len=107).

**Còn 1 bước (cần anh làm — em không tự restart gateway từ trong gateway):**
`hermes gateway restart` từ shell ngoài. Sau đó các tool `mcp_jevbridge_jev_decide`,
`mcp_jevbridge_jev_gate`, `mcp_jevbridge_jev_computer_use`, `mcp_jevbridge_jev_recipe`
xuất hiện trong mọi phiên.

**Cảnh báo an toàn trước khi tin dùng cho guardian thật:**
- Jevbridge KHÔNG có lớp chống prompt-injection (guardian PoC của em có: strip comment,
  bọc `<command>`). Cần vá `toolCallState`/`rawInput` trước — hoặc chỉ gọi jev_decide
  với state đã làm sạch.
- KHÔNG để rơi xuống `heuristic` backend ở đường an toàn (chỉ đếm từ khóa, README tự
  cảnh báo). Ép `backend: "jev"`, cấm `auto` fallback tới heuristic cho quyết định an toàn.
