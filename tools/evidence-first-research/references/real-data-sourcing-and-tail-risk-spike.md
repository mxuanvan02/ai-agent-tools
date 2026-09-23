# Real-data sourcing (Vietnam) + turning a negative spike into a positive result

When người dùng says "thử thêm trên dữ liệu khó/thực tế như bài AoI-greenhouse, ưu tiên dữ liệu
Việt Nam sát thực tiễn" and "đề xuất phương án bổ sung nếu method chưa đủ tốt", two
things matter: (1) source REAL, verifiable VN data; (2) if a method-enhancement
spike already failed, diagnose WHY before folding — the failure may be the dataset
regime, not the idea.

## 1. Verifiable real Vietnam climate data — Open-Meteo ERA5 Historical Archive

Free, no-key, reanalysis (ERA5) hourly archive — defensible provenance (coordinates
+ source), far better than an unlabelled single-column CSV of unknown origin.

- Endpoint: `https://archive-api.open-meteo.com/v1/archive`
- Params: `latitude=`, `longitude=`, `start_date=`, `end_date=`,
  `hourly=temperature_2m,relative_humidity_2m,shortwave_radiation`, `timezone=Asia/Bangkok`.
- Mekong-delta (ĐBSCL) stations used as 3 sensors (verified Jun 2026):
  Cần Thơ ≈ (10.03, 105.78), Sóc Trăng ≈ (9.60, 105.97), Cà Mau ≈ (9.18, 105.15).
- A full year (e.g. 2024) gives 8784 hourly points/station; temp ~20–38 °C,
  RH ~31–100 % — strong diurnal swings + seasonal heat episodes.
- **Provenance honesty:** this is *semi-real* — control/violation dynamics are
  simulated on a real weather trace (the dataset khí hậu VN pattern of bài AoI-greenhouse). Declare
  it as such ("real climate replay"), never as field-measured packet logs.
- JSON from Zenodo/large APIs can throw `Invalid control character at ... char 20000`
  in strict json.loads — read with `json.loads(text, strict=False)` or stream.

## 2. Before folding a failed enhancement: diagnose the signal REGIME

Pitfall that killed the first CVaR spike: the per-slot miss-risk signal was
**zero-inflated** (mostly 0, violations only in rare bursts). The 90th percentile of
a zero-inflated series ≈ 0, so a CVaR_α constraint degenerates into ~the mean
constraint and adds nothing — it only buys more bandwidth. Lesson: a tail-risk
objective needs a **non-degenerate tail**. Diagnose first:
- Print violation %, burst count, mean run-length per series. Double-digit
  violation% + burst structure (run-length > 1) ⇒ tail is non-degenerate ⇒ CVaR has
  something to bite on. Near-zero, isolated ⇒ tail is degenerate ⇒ pivot the target.
- The fix here was twofold: (a) move the tail constraint to a **continuous** loss
  variable (per-slot control loss) that is not zero-inflated, instead of the
  zero-inflated miss-rate; (b) run on a HARDER real dataset whose tail is genuinely
  heavy (VN heat bursts). Both were needed before the result turned positive
  (CVaR-loss: −14 % tail, p<1e-50, paired Wilcoxon, vs the degenerate −0.3 % before).

## 3. Isolate "smarter allocation" from "just spend more" — matched operating point

A risk-aware policy that wins while consuming more bandwidth is **confounded**. Bind
the shared resource (bandwidth dual) hard and IDENTICALLY on all policies so they
sit at the same realized operating point (~B_target), then compare the target metric.
Verify robustness by re-running at several binding strengths (e.g. BW_STEP 0.06 →
0.12 → 0.20); if the win holds across all, it is allocation quality, not spend.
The first CVaR-miss variant won the tail but at +0.19 bandwidth → rejected as
confounded; CVaR-loss won at matched bandwidth (Δbw ~1.7 %) → airtight.

## 4. Add a FAIR risk-sensitive baseline (anti-straw-man)

Don't compare the new risk-aware variant only against the risk-neutral deployed
policy. Add a classical risk-sensitive reference (mean–variance / exponential-utility
penalty on the budget cost). If it lands BETWEEN the deployed policy and the proposed
variant, that simultaneously (a) proves the comparison is fair, and (b) shows the
proposed variant is the genuine winner, not a straw-man beat. (bài bandwidth-scheduling-MV did exactly
this here.)

## 5. Online CVaR via Rockafellar–Uryasev (the reusable math)

CVaR_α(ℓ) = min_ξ [ ξ + 1/(1−α)·E[(ℓ−ξ)_+] ]. Two coupled projected-subgradient
updates, both derivable (no hand-tuning):
- dual ascent on λ over the RU slack: λ_{t+1}=[λ_t+α_λ(ξ_t+1/(1−α)(ℓ_t−ξ_t)_+−c_tail)]_+
- VaR tracker on ξ: ξ_{t+1}=ξ_t+β/(1−α)·(1{ℓ_t>ξ_t}−(1−α)); stationary point
  P(ℓ>ξ)=1−α, i.e. ξ→VaR_α (learned from data, not tuned).
Coupling 1/(1−α) is fixed by the identity; bounded ℓ,ξ ⇒ sup_t λ_t<∞ by the same
drift argument as the existing budget-dual proposition. c_tail = the deployed mean
target makes bài bandwidth-scheduling-PD the α→0 limit (clean-ablation anchor). Verify H1 (P(ℓ>ξ)≈1−α)
to confirm the tracker is calibrated before trusting H2 payoff numbers.

## 6. Recent (2024–2026) lit to position risk-aware NCS/IoT scheduling (verified live)

- Chen, Pan, Chan, "Version Age of Information Oriented Risk-Sensitive Scheduling
  with Distributional RL", WCNC 2026, doi:10.1109/wcnc65185.2026.11555306.
- Kishida, "Risk-Aware Control ... Worst-case CVaR in Control Barrier Functions",
  CDC 2024, doi:10.1109/cdc56724.2024.10886199.
- Rockafellar & Uryasev, "Optimization of conditional value-at-risk",
  J. Risk 2000, doi:10.21314/jor.2000.038 (the foundational identity).

## 7. Page-limit reality when folding a new contribution into a tight venue

Folding a real ~1-page contribution into an 8-page conference paper (hội nghị C1) pushes it
to 9. Prose-squeeze + table-merge (fold p/r into the main results table, drop the
separate Wilcoxon table) reclaims some, but a genuine new section costs ~1 page that
layout tricks can't erase without cutting science. Don't over-tighten (linespread,
bib itemsep) into unprofessional density. Surface the tradeoff to người dùng as a
decision: (1) cut a secondary subsection, (2) move to a venue allowing more pages
(IEEE Sensors J / IoT-J expanded-conference track), or (3) split into a separate
journal paper. Let him choose; don't silently mutilate the layout.
