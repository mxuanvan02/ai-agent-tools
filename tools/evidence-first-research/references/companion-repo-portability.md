# Companion / reproducibility repo — portability & dependency discipline

người dùng's convention: a paper's companion repo ships **CODE + SOURCE DATA only**, and every reported number must be regenerable end-to-end by the released pipeline (the "Paper 'xong'" gate). The grader/reviewer runs it on a **fresh machine that has none of your local packages**. So the repo must run with the smallest possible dependency surface.

## The recurring defect
One script in an otherwise stdlib-only repo quietly `import pandas`s (or another heavy dep) just to read a CSV and filter rows. On your dev box it works; on the reviewer's Mac it dies with `ModuleNotFoundError: No module named 'pandas'`. The tell: the repo's OTHER scripts are all stdlib-only (`import csv, math, random, statistics`) and only ONE file breaks the pattern.

## Fix policy — match the repo, don't grow the dependency
- **Prefer rewriting the outlier to stdlib** over adding the dep to `requirements.txt`. For CSV read + filter, `csv.DictReader` replaces pandas cleanly:
  ```python
  # pandas:  df = pd.read_csv(f); sev = df[df.network=="severe_burst"].set_index("policy")
  import csv
  with open(SUMMARY, newline="", encoding="utf-8") as f:
      sev = {row["policy"]: row for row in csv.DictReader(f) if row["network"] == "severe_burst"}
  if not sev:
      raise SystemExit(f"No matching rows in {SUMMARY}")
  ```
- Then chase EVERY pandas-ism the rewrite leaves behind — Pyright/LSP diagnostics surface them one by one: `df.loc[k]` → `sev[k]`, `k in df.index` → `k in sev`, `r.attr` → `float(r["attr"])`, `df.col.max()` → `max(float(r["col"]) for r in sev.values())`. Values from `DictReader` are **strings** — wrap numerics in `float(...)`.
- **Keep a heavy dep only when it's genuinely load-bearing.** matplotlib for actually rendering a figure is fine to keep; pandas for reading one CSV is not. If you keep one, add it to `requirements.txt` + a README note, or offer the user a stdlib-SVG fallback (lower figure quality) and let them choose.

## Verify by actually running on a clean interpreter — not just fixing syntax
On this host `python3` has no pip and PEP 668 blocks system installs; use `uv`:
```bash
uv venv /tmp/rabs_venv
uv pip install --python /tmp/rabs_venv/bin/python matplotlib   # note: `uv venv` ships NO pip; use `uv pip install`, not `venv/bin/pip`
/tmp/rabs_venv/bin/python code/make_tradeoff_plot.py
```
A green run that prints the plotted points (read from the CSV) and writes the PDF/PNG is the evidence the fix works — "removed the import and the syntax is clean" is NOT sufficient.

## Which copy to edit
The reviewer's traceback path (e.g. `/Users/<user>/Downloads/.../bài bandwidth-scheduling/code/...`) is their local clone of the GitHub repo, NOT your working tree. Fix in the canonical repo copy, then the change has to be **synced to the repo and pushed** — and per người dùng's gate, **never push without explicit approval**. Tell him the fix location and ask before syncing/pushing.
