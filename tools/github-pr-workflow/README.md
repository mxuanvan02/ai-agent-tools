# github-pr-workflow

GitHub PR lifecycle with evidence gates: branch from the real base, conventional commits, open and verify a PR from the remote, monitor CI, and leave merging to the human.

## Diem noi bat

- `references/ci-troubleshooting.md`
- `references/conventional-commits.md`
- `templates/pr-body-bugfix.md`
- `templates/pr-body-feature.md`

## Cau truc

```
SKILL.md                                                  
references/ci-troubleshooting.md                          
references/conventional-commits.md                        
scripts/public_hygiene_check.py                           
templates/pr-body-bugfix.md                               
templates/pr-body-feature.md                              
```

## Kiem tra ve sinh public

```bash
python3 scripts/public_hygiene_check.py
```

Cổng này quét mọi file text trong thư mục tool và thoát 1 nếu gặp định danh cá nhân,
đường dẫn nội bộ của máy, tên mã của bài báo chưa công bố, tên cơ sở đào tạo, chuỗi
dạng secret, hoặc placeholder còn sót. Nó cũng được CI chạy.

## Cai dat

Copy thư mục này vào skills dir của agent (ví dụ `~/.hermes/skills/github/`), hoặc dùng trình quản lý skills:

```bash
npx skills add mxuanvan02/ai-agent-tools -g --all
```

## License

MIT — xem [LICENSE](LICENSE).
