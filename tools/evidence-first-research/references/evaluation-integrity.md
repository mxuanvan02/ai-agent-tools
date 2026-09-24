# Evaluation integrity — lessons that repeatedly bite (người dùng papers)

Pitfalls found while revising bài bandwidth-scheduling (empirical scheduling paper, primal-dual bandwidth + urgency channel). All are about NOT fooling yourself or the reviewer with results.

## 1. A contribution can WIN on easy data and REVERSE on hard data
- The "value-of-uncertainty" urgency channel `g(p)=4p(1-p)` beat raw-probability `p` on the mild-tail greenhouse replay, so it was made the headline contribution.
- On the hard heavy-tailed ERA5 replay it LOST to raw-`p`: genuine heat episodes push `p→1`, and a decision-uncertainty form that peaks at `p=0.5` de-ranks exactly the near-certain exits that matter.
- **Rule:** before elevating a term to "main contribution", ablate it on the HARDEST target regime, not just the convenient one. If it only wins on easy data, it is not the contribution — the robust mechanism underneath (here: the primal-dual self-tuning budget, which won `p<10⁻⁴⁰`, 240/240 paired) is.
- Regime-dependence is itself a legitimate honest finding: report it in the ablation ("form X preferable when p→1") rather than hiding the reversal.

## 2. If the "Proposed" method beats the "Oracle", the ORACLE is wrong
- bài bandwidth-scheduling-PD scored better than the oracle_b row → red flag, not a triumph.
- Root cause: the "oracle" was a GREEDY PER-SLOT clairvoyant (sees true values but optimizes each slot independently, with mismatched internal weights). A greedy per-slot policy is NOT a cumulative lower bound; a feedback policy that manages AoI dynamics over time can beat it.
- **Fix chosen (honest, keeps source code intact):** relabel it "Greedy clairvoyant (per-slot reference)" with a caption footnote "per-slot reference using true values, not a cumulative lower bound", and turn the fact that bài bandwidth-scheduling-PD edges it into a discussion point (feedback beats myopic perfect-information because it manages age over time).
- A true cumulative-optimal oracle is generally NP-hard / intractable — do not claim "lower bound" for a greedy proxy.

## 3. Use the ORIGINAL source code for baselines — do not reinvent
- When a baseline (oracle) looked wrong, the instinct was to hand-roll a "correct" brute-force version. That introduced a NEW definition inconsistent with the repo and the other experiments.
- Người dùng's correction: "lấy đúng source code gốc về mà chạy" — pull the baseline's exact definition from the canonical repo (git HEAD) and port it verbatim. Diagnose/relabel rather than silently redefine.

## 4. Do not build narrative around a result until it survives verification
- Across ~7 runs a CVaR tail variant never beat the primal-dual baseline (both mild greenhouse AND hard ERA5, both CVaR-loss and missed% metrics; the wins it had were never statistically significant, p≈0.26–0.88). Correct call per người dùng: bỏ hẳn về Future Work, do not ship a "Proposed" row that loses its own metric.
- Read the SIGN of paired deltas carefully. `Δ=PD−CVaR<0` with tiny p means PD is significantly BETTER — not "CVaR significant improvement". Mis-reading sign once nearly shipped a table where every `\best{}` sat on the baseline. Always print an explicit "-> X better" tag next to each significance test.

## 5. Mechanics that saved time
- One generator script emits ALL manuscript-format tables from the fresh CSVs (`make_*_tables.py`, needs venv numpy+scipy) so paper numbers cannot drift from code. Regenerate → copy to manuscript → build.
- Pivoting datasets (greenhouse→ERA5) = re-run every dependent stage: main, wilcoxon, scaling, ablation, tradeoff figure (parametrize CSV source via env var), then regen tables. Delete stale table files not `\input` anymore.
- Page-limit trimming: prefer `\small` on the bibliography + cutting self-commentary sentences over tweaking floats. Verify page count after EACH edit; a longer replacement sentence silently pushed 8→9 pages twice.
- ERA5 real data is re-fetchable from Open-Meteo archive API (`fetch_real_vn_data.py` pattern) — "lost" VN climate data was never lost, just not committed.
