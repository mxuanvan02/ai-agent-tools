# Reviving a folded method-enhancement spike: non-degenerate target + hard REAL data

Use when a method-enhancement spike (CVaR / risk-aware / tail-shaping variant) FOLDED
on the first pass — no significant win over the deployed method — and người dùng says
"thử thêm" / "chạy trên tập dữ liệu khó, thực tế như bài AoI-greenhouse" / "ưu tiên dữ liệu
Việt Nam". This is the recipe that turned a fold into an airtight positive result
in the bài bandwidth-scheduling branch-B session (CVaR tail-risk on greenhouse bandwidth scheduling).

## Why the first spike folded — diagnose the REGIME, not the knobs

The first bài bandwidth-scheduling-CVaR spike showed Δ≈0, p=0.34 on tail miss-risk, and CVaR only "won"
by spending +0.5 bandwidth. Root cause was NOT a bad step-size — it was a
**degenerate regime**: the per-slot miss-risk signal was **zero-inflated** (most
slots = 0, misses only in rare bursts). When the constrained quantity is mostly
zero, its 90th percentile ≈ 0, so a CVaR-0.9 constraint **degenerates into ~a mean
constraint** and the fancy tail machinery adds nothing. The deployed mean-constraint
method is already near-optimal for a sparse signal.

Lesson: before re-running, ask "is the tail of the constrained quantity actually
non-degenerate?" If the signal is zero-inflated / saturating, NO amount of step
tuning will make a tail constraint earn its keep. Two orthogonal fixes:

### Fix A — change the TARGET VARIABLE to a continuous, non-zero-inflated one
Re-anchor the tail constraint on a quantity that is continuous and spikes at the
right moments, instead of a sparse 0/1-ish rate. In bài bandwidth-scheduling: switch the CVaR target
from sparse **miss-rate** → continuous **per-slot control loss** (rises smoothly
during stress bursts). This is changing the OBJECTIVE, not vetting a knob, so it is
a legitimate one-more-try, not knob-hunting. CVaR-loss won where CVaR-miss folded.

### Fix B — move to a HARDER, REAL dataset where the tail is non-degenerate
A calibration dataset whose violation rate is tiny will hide any tail method. Get a
dataset with double-digit event rate + burst structure. ALWAYS run a go/no-go
**tail-structure diagnostic** before the comparison:
- violation% per series (want double digits, not <1%)
- burst count + mean run-length (want clustered events, not isolated)
- print an explicit interpretation line: "nonzero burst structure + double-digit
  violation% ⇒ per-slot risk is NOT zero-inflated ⇒ CVaR constraint non-degenerate."
If that check fails, the comparison is pointless — fix the dataset/target first.

## Verifiable REAL Vietnam climate data — Open-Meteo ERA5 archive

người dùng prioritizes real VN data as evidence (thesis uses "dataset khí hậu VN"). On-disk
`vietnam_mekong_weather.csv` was only ~480 single-column synthetic points
(README literally says weather-conditioned synthetic) — NOT defensible as real.

Recipe that worked: **Open-Meteo Historical Archive API** (ERA5 reanalysis), hourly,
for Mekong Delta coordinates — Cần Thơ, Sóc Trăng, Cà Mau. Pull `temperature_2m` +
`relative_humidity_2m` for a full year ⇒ 8784 hourly points/station. Public,
coordinate-tagged, citable. Endpoint: `archive-api.open-meteo.com/v1/archive`
with `latitude,longitude,start_date,end_date,hourly=...`. Returns JSON.

Provenance honesty: this is **semi-real** — control/violation variables are simulated
ON TOP of a real climate trace. Declare it exactly that way ("mô phỏng trên trace
thời tiết VN thật"), same posture as dataset khí hậu VN, never "field-measured".

## Killing the "wins only by spending more" confound — matched-operating-point sweep

A tail method that quietly buys more bandwidth/budget is confounded. To prove it
ALLOCATES smarter rather than just spends more:
1. Make the resource (bandwidth) dual the BINDING constraint for ALL policies with
   an IDENTICAL step — same machinery on baseline and variant, no win-hunting.
2. Expose the constraint step as an env knob (`BW_STEP`) and **sweep it at 2–3
   increasing strengths** (e.g. 0.06/0.12/0.20). If the variant keeps winning while
   its realized budget is pinned to within ~1–2% of the baseline's, the win is real.
   In bài bandwidth-scheduling: CVaR-loss held p<1e-46, ~290/320 paired wins, Δbandwidth ≈ +0.02 across
   all sweep levels ⇒ airtight. CVaR-miss was rejected precisely because its win
   rode a +0.19 bandwidth gap.

## Workflow hygiene reused this session
- All of branch-B lives on a CLONE (`<project>_branchB_clone`), manuscript untouched
  until người dùng approves fold — matches his "test on clone" rule.
- Reuse the main simulator via `importlib.util.spec_from_file_location` so only the
  budget/dual logic differs; identical seeds/windows/channel ⇒ paired Wilcoxon valid.
- Verdict framing for người dùng: lead with the decision, give matched-bw evidence,
  cite 2024–2026 SoTA to pre-empt "not novel", then offer fold / future-work / dig-
  deeper as an explicit choice with the real tradeoff (writing+full-run+build cost).
