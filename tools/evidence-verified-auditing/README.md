# evidence-verified-auditing

Bulk code/data scan discipline: a scan produces candidates, not findings; confirm against an independent oracle, classify before counting, and prove a verifier can fail before trusting a green result.

## Diem noi bat

- `references/authoring-a-prose-quality-gate.md`
- `references/building-a-verified-source-bank.md`
- `references/citation-claim-verification.md`
- `references/dedup-to-single-version.md`
- `references/derived-dataset-provenance.md`
- `references/installed-copy-vs-upstream-repo.md`
- `references/proving-a-verifier-can-fail.md`
- `references/thesis-audit-2026-08.md`

## Cau truc

```
SKILL.md                                                  
references/authoring-a-prose-quality-gate.md              
references/building-a-verified-source-bank.md             
references/citation-claim-verification.md                 
references/dedup-to-single-version.md                     
references/derived-dataset-provenance.md                  
references/installed-copy-vs-upstream-repo.md             
references/proving-a-verifier-can-fail.md                 
references/thesis-audit-2026-08.md                        
scripts/public_hygiene_check.py                           
```

## Kiem tra ve sinh public

```bash
python3 scripts/public_hygiene_check.py
```

Cổng này quét mọi file text trong thư mục tool và thoát 1 nếu gặp định danh cá nhân,
đường dẫn nội bộ của máy, tên mã của bài báo chưa công bố, tên cơ sở đào tạo, chuỗi
dạng secret, hoặc placeholder còn sót. Nó cũng được CI chạy.

## Cai dat

Copy thư mục này vào skills dir của agent (ví dụ `~/.hermes/skills/research/`), hoặc dùng trình quản lý skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

## License

MIT — xem [LICENSE](LICENSE).
