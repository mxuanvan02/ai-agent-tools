# explainer-ladder

Four-rung explainer ladder for learners: controlled text (ASD-STE100 spirit),
diagram, interactive HTML page, video. Higher rungs add to lower ones; every
deliverable keeps the verifiable text layer. Activated only on an explicit
"explain X for my students" style request.

## Diem noi bat

- `references/asd-ste100-vietnamese.md` - quy tac viet tieng Viet kieu ASD-STE100 cho tai lieu day hoc
- `references/ladder-tooling.md` - lenh cu the cho tung nac (Graphviz, Mermaid, HTML, video)

## Cau truc

```
SKILL.md
references/asd-ste100-vietnamese.md
references/ladder-tooling.md
scripts/public_hygiene_check.py
```

## Kiem tra ve sinh public

```bash
python3 scripts/public_hygiene_check.py
```

Cong nay quet moi file text trong thu muc tool va thoat 1 neu gap dinh danh ca
nhan, duong dan noi bo cua may, ten ma cua bai bao chua cong bo, ten co so dao
tao, chuoi dang secret, hoac placeholder con sot. No cung duoc CI chay.

## Cai dat

Copy thu muc nay vao skills dir cua agent, hoac dung trinh quan ly skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

## License

MIT. See `LICENSE`.
