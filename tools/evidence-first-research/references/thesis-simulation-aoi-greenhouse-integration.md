# Thesis simulation chapter and bài AoI-greenhouse integration

Use when người dùng asks whether the thesis simulation chapter should follow the bài AoI-greenhouse paper, whether the results are taken from bài AoI-greenhouse, or how to phrase the relationship between thesis simulation, bài AoI-greenhouse, and related products such as bài bandwidth-scheduling.

## Durable lesson

Do **not** overstate that the thesis chapter "takes results directly from the bài AoI-greenhouse paper" unless the exact paper source table/figure has been checked. Phrase the relationship precisely:

- The thesis simulation can be the **benchmark/pipeline nền** that connects the systematic review to bài AoI-greenhouse.
- The results should be cited as coming from the **reproducible simulation pipeline** and its CSV outputs, e.g. `05_Simulation/simulation/results/q1_benchmark_summary.csv`.
- bài AoI-greenhouse should be described as the **direct continuation/development branch** from that benchmark: when transmission is constrained, scheduling should use update value plus channel state.
- bài bandwidth-scheduling should be positioned as a **related resource-allocation branch**, not the main simulation spine, unless the chapter explicitly uses bài bandwidth-scheduling data.

Safe wording in Vietnamese:

> Phần mô phỏng được tái lập từ pipeline mô phỏng nền liên quan đến nhánh bài AoI-greenhouse. Kết quả trong bảng được lấy từ các tệp CSV của pipeline mô phỏng; bài AoI-greenhouse là hướng phát triển trực tiếp từ cơ chế đánh đổi này sang bài toán lập lịch cập nhật theo giá trị thông tin và trạng thái kênh.

Avoid:

> Kết quả lấy trực tiếp từ bài báo bài AoI-greenhouse.

unless the exact bài AoI-greenhouse manuscript table/figure and source data have been verified.

## Verification steps before editing prose

1. Locate active thesis chapter: `01_Manuscript_LVTN/LVTN/Chapter/noidung_chap4.tex`.
2. Locate simulation truth source: usually `05_Simulation/simulation/results/q1_benchmark_summary.csv` and any copied CSV under `01_Manuscript_LVTN/LVTN/figures/ch04/`.
3. Compare table values in Ch. 4 against CSV programmatically or by direct read:
   - scenario/method rows (`TT-MPC`, `ET-MPC`, etc.)
   - `rmse_mean`, `iae_mean`, `energy_mean`, `tx_rate_mean`
   - derived reductions: `(TT-MPC - ET-MPC) / TT-MPC`
4. If a bài AoI-greenhouse paper PDF/source is available, check it separately before claiming direct provenance. A PDF-only artifact is not enough unless the same numbers/figures can be traced.
5. Update prose to distinguish: **pipeline result** vs **paper result** vs **future/related branch**.
6. Rebuild with XeLaTeX and report PDF path.

## Provenance phrasing pattern

In Ch. 4, keep the chain short:

1. Ch. 3 identifies a gap: network constraints are often simplified.
2. Ch. 4 runs/uses a reproducible simulation pipeline to test the trade-off.
3. The benchmark shows ET-MPC saves transmission/energy but increases RMSE/IAE.
4. bài AoI-greenhouse is motivated by this result: not every transmission should be treated equally; updates should be ranked by value and channel state.
5. bài bandwidth-scheduling is a related extension for risk-aware bandwidth/resource allocation.

## Pitfalls

- Do not mix `q1_benchmark_summary.csv` (thesis benchmark: TT/ET MPC/PID) with `cvoi_multiloop_summary.csv` (CAW/VoU-style scheduling policies such as `cvoi`, `aoi`, `risk`, `round_robin`) unless the chapter explicitly introduces both experiments.
- If Ch. 4 says `q1_benchmark_summary.csv`, then the table should only claim TT/ET benchmark results, not bài AoI-greenhouse policy superiority.
- If người dùng wants the chapter to be "như bài CAW" more strongly, first decide whether to replace/add an experiment from the CAW/VoU CSVs; do not silently relabel q1 benchmark as CAW results.
- Keep wording concise; người dùng prefers shorter thesis prose and dislikes long defensive explanations.
