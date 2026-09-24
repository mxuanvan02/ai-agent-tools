# Verifying a manuscript's numbers/figures are RUN-BACKED (not hand-drawn)

Người dùng's bar: "tất cả mọi thứ đều phải thật" — every table value and figure
in a submission must be reproducible from real code execution, not synthetic
placeholders. When he asks "số liệu/bảng/biểu đã chạy đúng chuẩn chưa", he is
NOT asking for a proofread; he is asking you to PROVE provenance. Do not call
the paper ready until you've executed the source and diffed output vs. text.

## The trap: plot-generator placeholders masquerading as results

A figures folder that builds cleanly is NOT evidence the numbers are real.
Watch for a script (e.g. `simulation_code/generate_all_plots.py`) that draws
charts from **hand-coded constants + `np.exp(...)` + injected noise** with no
model in the loop. These are placeholders. Tell-tales:
- hard-coded arrays (`energy = [8.2, 6.1, ...]`), `np.random.normal` for spread,
  closed-form curves instead of measured series;
- no `results.json` / CSV / metrics file written anywhere;
- figure timestamps all identical (one render pass), no training logs.

## Verification procedure (do this, don't just read the README)

1. **Locate the real reproduction code.** Often a separate GitHub repo
   (companion artifact), not the `Downloads/` plotting script. Check the
   author's repos: `gh repo view <user>/<repo>` or the GitHub API. README
   "Results (ours vs paper)" tables are claims — verify by running.
2. **Clone + build an isolated env.** `git clone` may time out on the `.git`
   history over slow links while still leaving all source files usable — check
   for the `.py` files before retrying. Use `uv venv` + `uv pip install`.
   Install **CPU-only torch** (`--index-url .../whl/cpu`) — far lighter than the
   CUDA wheel and enough for small TD3/FedAvg nets. Heavy installs: run
   `background=true, notify_on_complete=true` so they don't block the turn.
3. **Execute the real runner** (`python run_simulation.py`) in the background,
   then read the emitted `results.json` — that is ground truth.
4. **Diff every headline number and table against the `.tex`.** Build a
   side-by-side: paper value | repo value | match? Flag three failure classes:
   - **orphan numbers**: a percentage in prose with no source in the repo
     (e.g. "fusion +8.7%", "DT 63% after 50% mission", "sparsification 72%");
   - **internally inconsistent**: a claim that contradicts the paper's own
     table (e.g. "sensing −27.3% vs FIXED" when the table's 3.4 vs 7.1 = −52%);
   - **fabricated table rows** (e.g. "Prediction Accuracy 89.7%" with no
     experiment behind it).
5. **Replace, don't paper over.** Swap placeholder figures for the repo's real
   renders (`results/*.png`), replace the numbers/prose with `results.json`
   values, DELETE orphan/inconsistent claims and any "Sensitivity Analysis"
   section that was pure hand-drawing. Add a code-availability footnote +
   GitHub link when the user asks to ship source.
6. **Honesty gate.** If part of a table still has no experiment behind it
   (e.g. DT energy/mission-time/revisit rows), say so explicitly and offer:
   (A) extend the repo to generate those metrics for real, then re-run; or
   (B) drop the unbacked rows to qualitative text. Never silently keep them.
   Do NOT push the repo without explicit approval.

## Always rebuild + grep after edits
- `latexmk` to confirm rc=0, page count, and **no undefined refs/citations**.
  `TU/ptm/* undefined` font warnings under xelatex are harmless.
- grep the `.tex` for leftover markdown artifacts (`**bold**` → must be
  `\textbf{}`), and for the specific orphan numbers you removed, to confirm
  none survive.

## Harvesting author/affiliation/funding from prior papers (no fabrication)
When asked to "fill in affiliation / add Funding / add co-author (see paper X)":
- Pull the exact `\author`, `\affiliation`, `\thanks{... supported by ... Grant
  No. ...}` blocks from the user's OTHER manuscripts (search his repos/zips for
  `main.tex`). Grant IDs and ORCIDs must come verbatim from a real prior paper —
  never invent them.
- If an email or field is genuinely absent in every source, leave it blank and
  flag it for the user rather than guessing; he will supply it.
- "co-first author" → mark with a shared dagger symbol + "These authors
  contributed equally" note; confirm corresponding-author choice if it differs
  from the original draft.
- Backup the `.tex` to `_backups/<ts>/` before editing (his standing rule).
