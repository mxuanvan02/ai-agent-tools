# Conference-level evidence gate for protocol/system manuscripts

Use this gate when a manuscript has a formal method, executable artifact, deterministic validation, or a small diagnostic and the user asks whether it reaches conference level.

## Two legitimate routes

### Protocol/artifact paper
Claims may cover executable construction, representation, integrity validation, provenance bookkeeping, and reproducibility on the documented input contract. A clean build and synthetic fixtures support this route, but do not establish semantic quality.

### Empirical method paper
In addition to the artifact, require:

1. Real multimodal documents with source-disjoint evaluation and clear rights boundaries.
2. Fair matched-budget baselines: direct generation, answer-first, and the full method.
3. Core ablations for answer-before-question and typed graph/provenance controls.
4. Blinded independent human judgments of answer correctness, grounding, answerability, question quality, leakage, and—when claimed—modality necessity.
5. Agreement before adjudication, document-level uncertainty intervals, paired comparisons, effect sizes, and failure taxonomy.

## Metric boundary

Report structural and semantic metrics separately.

- Structural: schema validity, package completeness, hash consistency, provenance replay, isolated reconstruction, deterministic regeneration.
- Semantic: answer correctness, complete answerability, grounding accuracy, question acceptance, leakage-free rate, validated modality requirement.

Structural PASS is not semantic correctness.

## Invalid substitutions

Never use synthetic fixtures, model self-judgments, output emergence, confidence, hashes, or provenance replay as evidence of correctness, grounding, modality necessity, effectiveness, superiority, or generalization. A six-cell diagnostic is an implementation illustration, not an efficacy evaluation.

## Decision rule

Before saying `conference-ready`, state separate verdicts for:

- technical/package readiness;
- scientific/content readiness.

If empirical evidence is missing, either keep the protocol/artifact claim boundary or report `BLOCKED`. Do not repair an evidence gap with stronger prose.

Human annotation, data rights, author metadata, and venue compliance remain explicit external gates; they cannot be simulated by the artifact or an LLM judge.
