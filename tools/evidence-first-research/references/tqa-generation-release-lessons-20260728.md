# bài TQA-generation release lessons (2026-07-28)

## Claim taxonomy
Classify every statement before writing or publishing:

1. **Deterministic artifact validation** — schema, hashes, embedded-byte decoding, clean-room portability, receipt binding.
2. **Machine-observed diagnostic** — one fixed answerer’s outputs under T/TL/TLV; descriptive only.
3. **Human semantic evidence** — independent judgments of question-answer completeness, atom grounding, source-region validity, leakage, and minimum sufficient operational package.
4. **Effectiveness evidence** — frozen baselines/ablations, controlled budgets, adjudicated labels, denominators, and source-clustered analysis.

Do not promote evidence from one tier to the next. In particular, model abstention/success does not prove modality necessity; a request containing an image proves only that the client sent pixels.

## Manuscript section discipline
- **Abstract:** summarize problem, proposed method, scope, and intended contribution. Avoid pilot counts and qualitative result claims when the abstract is meant to describe what the paper does.
- **Introduction:** motivation, research gap, objective, methodological contributions, and scope. Do not use it as a results table.
- **Method:** define T=text, TL=text+layout/structure, TLV=text+layout+visual pixels; state that these are extractor-relative operational packages.
- **Results:** report only completed observations, exact denominators, exclusions, and status. Separate artifact integrity from semantic validation.
- **Limitations:** explicitly state missing human adjudication, rights restrictions, non-random candidate selection, model dependence, and lack of generalization.

## Formal safeguards
Sufficiency must be question-conditioned: evaluate `(q, X, A)`, not only whether `X` entails answer atoms. Include joint completeness, ordering, aggregation, alternatives, and an explicit Full-insufficient value such as `bottom`. Separate machine trace consistency from independent source-grounding validity and region-localization correctness.

Use "controlled evidence-ablation audit" or qualify "counterfactual" narrowly as package-level withholding. Do not call extractor-dependent `T/TL/TLV` labels representation-invariant semantic or causal modality effects.

## Canonical experiment boundary
For the bài TQA-generation release, the defensible canonical evidence was two proposals × three conditions = six completed runtime cells, with deterministic package/receipt validation. Four negative-control candidates were held because evidence localization, answer atoms/programs, matched packages, human annotation/adjudication, and rights records were incomplete. Dry-runs, parser-development runs, placeholders, heterogeneous archived runs, and revoked packets were excluded from canonical results.

The safe report format is a candidate-flow diagram/table, an artifact-integrity table, a machine-response table, and a descriptive T/TL/TLV heatmap. Use `NOT_PERFORMED`, `PENDING`, or `NA` for absent human/effectiveness evidence; never fill missing metrics with zero or invent baselines, ablations, confidence intervals, or agreement statistics.

## Release boundary and verification
Treat the manuscript/submission package, public experiment-code repository, and private rights-sensitive dataset as separate products unless the release design explicitly combines them. For a code-centric public repository, include installable source, strict schemas/runtime validation, synthetic rights-cleared fixtures, tests, CI, documentation, and licensing; keep manuscript files and source-derived media outside that tracked tree. Keep raw/source-derived images, embedded pixel packages, credentials, absolute host paths, retained private receipts, and internal packet/debug terminology out whenever redistribution or disclosure is unresolved.

Verification is not complete at a local build or successful push. Stage the intended tree explicitly, inspect staged paths, run tests/build/schema and secret-path-rights scans, push, verify local and remote commit SHAs, create a versioned release, and then clone the exact remote commit into a fresh directory and repeat install/test/build/CLI smoke checks. Synchronize package version, citation metadata, manuscript artifact URL, tag, and release notes. If private dataset authentication or synchronization fails, report that component as pending rather than describing the whole release as complete. After tool execution, always return a non-empty status summary with exact hashes, URLs, and remaining blockers.
