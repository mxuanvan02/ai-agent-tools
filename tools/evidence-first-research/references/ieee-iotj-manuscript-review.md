# IEEE Internet of Things Journal Manuscript Review Notes

Use for the user's IoTJ manuscript reviews.

## IoTJ venue checks

- Scope fit: IoT architecture, enabling technologies, communication/networking protocols, services/applications, testbeds, standards, sensor/big-data/future-Internet integration.
- Submission substance: original and substantial work; avoid simultaneous/near-duplicate submission; expanded conference versions need archival-quality extension.
- Peer review: single-anonymous, at least two independent reviewers; plagiarism screening before acceptance.
- Format: IEEE double-column journal template; abstract 150-250 words, one paragraph, no citations or displayed equations.
- Practical constraint: mandatory page charge after the first 8 published pages, so long manuscripts should justify length and avoid reviewer fatigue.

### Page-length policy — verified facts (don't repeat the "8-page hard limit" misconception)

Người dùng may believe "IoTJ giới hạn 8 trang" — this is WRONG and changes how you advise cutting. Verified live from ieee-iotj.org/guidelines-for-authors (Mandatory Page Charges section):
- **8 published pages = the FREE threshold, NOT a hard cap.** Over-length papers are still accepted; you are billed **$175 per page in excess of the first eight published pages** (mandatory, non-negotiable). Length does not by itself cause rejection.
- The guideline only "advises economy" — a cost nudge, not an acceptance criterion.
- "Published pages" = the typeset/published version (usually ~10–15% tighter than the submitted IEEEtran draft), not the submission page count.
- **Typical IoTJ paper length ≈ 11–14 pages** (double-column); 8–10 = lean/focused, 15–18 = theory-heavy + broad experiments (still common, just incurs page charges). Do not claim a live-scraped distribution unless you actually fetched it — IEEE Xplore / DBLP API / Google are often blocked from this environment (ERR_CONNECTION_RESET, CAPTCHA, terminal http_code=000); say it's an estimate when you couldn't fetch.
- When người dùng asks to shorten, the real question is "save page charges" vs "be more concise" — frame it that way. Recommend the **~12–14 page sweet spot** (cuts cost, keeps depth); do NOT recommend forcing down to 8 if it means gutting the theory/multi-dataset story (that throws away the competitive edge). Concrete levers: push long proofs to Appendix (~2–3 pages), condense related work + merge robustness tables (~1–2 pages), cut Intro/Conclusion repetition (~0.5 page).

## Four-pass review pattern

1. Venue/storyline pass: title, abstract, intro, contribution list, related work, IoTJ fit, novelty/positioning, overclaim risk.
2. Technical pass: system model, assumptions, algorithm-theory alignment, theorem/proof correctness, notation consistency, boundary cases.
3. Empirical pass: datasets, preprocessing, baselines, metrics, statistics, ablations, sensitivity, reproducibility, runtime/deployment realism.
4. Compliance/package pass: PDF freshness, page count, build warnings, citations/references, figures/tables, data/code availability, submission package consistency.

## IoTJ-specific reviewer sensitivities

- Make the IoT deployment scenario concrete: gateway/sensors, metadata probe vs payload pull, communication budget, slot duration assumptions, sensor burden.
- Avoid making the paper look like a generic scheduling/theory paper with IoT examples; frame the contribution as deployable IoT system design.
- Separate theorem claims from deployed implementation details. If guarantees apply to an idealized variant, state that in title/abstract/contributions.
- For safety-critical IoT, justify thresholds and metrics; avoid objectives that merely mirror the proposed method without sensitivity/Pareto analysis.
- Cross-dataset claims need consistent threshold rules or an explicit reason for dataset-specific rules.
- SOTA baselines should distinguish direct reproductions from author-designed adaptations and disclose information advantages.
- Multiple p-values need a correction strategy or an explicit exploratory/confirmatory split.
- Runtime claims need hardware/software environment and a concrete IoT slot-duration reference.

## Recommended report shape

- Start with file location and readiness verdict.
- Then list major findings first, severity ordered, with file/section references.
- Follow with IoTJ fit, theory, evaluation, format/build, and prioritized revision roadmap.
- End with submit readiness: submit now / major revision first / reject-risk, plus smallest next steps.

## IoTJ revision pattern learned from bài probe-transmit

- If the title/abstract says "provable fairness," verify the deployed algorithm is exactly the variant covered by the theorem; otherwise rename to a safer deployment-oriented title.
- For probe-then-transmit papers, explicitly define metadata probing vs payload pull so reviewers do not read "probe" as channel/CSI probing.
- For debt/fairness mechanisms, keep bounded normalized deficits separate from accumulating age-of-service debt; bounded share deficits are usually soft regularizers, while hard deadlines need unbounded age-style debt.
- In proofs, prefer stepwise algebra: score inequality -> bounded urgency margin -> debt dominance -> service deadline. If a monotonic blocking-set argument is not rigorous, remove matching/tight upper-bound language.
- When choosing a deployed variant, make all main tables use that variant. Put optional improvements such as correlation credit in ablation only, even if they are numerically slightly better.
- Add a compact reproducibility table early in Evaluation: dataset, sensors/variables, windowing, threshold rule, purpose, seeds/statistical protocol.
- Split statistics into confirmatory main tests and exploratory sensitivity sweeps; use multiple-comparison correction or explicitly mark exploratory p-values.
