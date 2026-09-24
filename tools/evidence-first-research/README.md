# Evidence-First Research

Agent Skill: quy trình nghiên cứu ứng dụng 11 giai đoạn (intake → RQ brief → methodology →
literature verification → synthesis/gap → draft → writing → multi-perspective review →
revision → integrity → packaging), kèm 143 file references đúc kết từ các phiên nghiên
cứu thật (bài báo IEEE IoT-J/Sensors-class, luận văn, dataset release).

> Nguyên tắc lõi: **bằng chứng trước, câu chữ sau** — wording không phải evidence;
> mọi claim phải truy được về nguồn; phát tán ý tưởng TRƯỚC, chấm/chỉ trích SAU.

## Điểm nổi bật

- **Divergent ideation protocol** (`references/divergent-ideation-protocol.md`):
  5 kỹ thuật sinh ý tưởng (cross-domain analogy có quota, subagent chống neo,
  constraint inversion, negative-result mining, đảo chiều gap-scan) + thứ tự
  vận hành cố định cấm chấm sớm. Kèm số đo thật trên Jev 1.13.0 cho thấy
  System-One là bộ lọc claim tốt nhưng là giám khảo novelty tệ (0.59 cho hướng
  an toàn vs 0.19 cho hướng cross-domain) → chỉ dùng để lọc, không xếp hạng ý tưởng.
- **Jev System-One claim-gate** (`references/jev-systemone-claim-gate.md`):
  đối chiếu claim↔source verbatim qua MCP `jevbridge` (noul, ~450 token, <400ms/call),
  ngưỡng 3 dải đo thật (≥0.8 pass / ≤0.2 BLOCK / giữa → escalate).
- **Reviewer-standard integrity**: citation verify live qua Crossref/arXiv/OpenAlex API,
  straw-man baseline detection, matched operating point, số trên hình truy về CSV,
  build-from-bundle, missing-citation handling không bịa bib entry.

## Cấu trúc

```
SKILL.md            — pipeline 11 giai đoạn + routing vào references
references/ (143)   — playbook chi tiết theo tình huống
scripts/  (5)       — bibcheck/bib_verify/bibrecheck, measure_regime_properties,
                      public_hygiene_check
```

## Kiểm tra vệ sinh public

```bash
python3 scripts/public_hygiene_check.py
```

Quét toàn bộ tool: định danh cá nhân, đường dẫn máy nội bộ, codename bài báo
chưa công bố, tên trường/viện, hình dạng secret. Fail (exit 1) nếu còn sót.

## Cài đặt

Copy thư mục này vào skills dir của agent (vd `~/.hermes/skills/research/`),
hoặc dùng trình quản lý skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

## License

MIT — xem [LICENSE](LICENSE).
