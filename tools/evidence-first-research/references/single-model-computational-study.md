# Single-model computational experiment and manuscript gate

Use this reference when an bài TQA-generation or comparable controlled LLM-generation study is requested as a **computational-only** experiment.

## Design invariants

1. Select the model snapshot before the primary run. Keep the same model for generation, fixed-question counterfactuals, baselines, and component ablations. Do not pool historical ledgers from another model.
2. Freeze the evidence manifest, conditions, seeds, decoding settings, output contracts, and run plan before executing the suite. Use new immutable output directories; retain earlier-model results only as historical artifacts.
3. Treat the experimental unit correctly: paired source chunks across conditions are paired observations, not independent API-call samples.
4. A fixed-question counterfactual must first construct a content-addressed bank from the selected generation condition, then answer identical question/choice payloads under every evidence condition. It must not regenerate or rewrite the question.
5. Require verifier plan reconstruction to receive the explicit model used by the ledger. A verifier that silently rebuilds using its runner default can falsely report a full plan mismatch after a model override.
6. Preserve contract failures (`REJECTED`) in the result ledger and denominators. Report planned, parsed/conformant, rejected, and error counts; never silently exclude malformed rows.

## Computational claims gate

- Schema/contract conformance establishes execution validity only.
- Literal trace support is a bounded proxy; it cannot validate image semantics merely because pixels were attached.
- Answer-index agreement/stability across evidence conditions is not factual accuracy, legal correctness, image benefit, causal modality effect, or generation quality.
- Do not claim SOTA without a task-matched public benchmark and matched external comparisons. Prefer “among the evaluated prompting protocols” only if verified metrics support it.
- A re-analysis of an existing Direct/Answer-first/ECM ledger is not a new component ablation. A component ablation requires newly generated outputs with one named ECM mechanism removed while matched factors remain fixed. Generic self-refinement must be compute-budget matched when used as a baseline.

## Manuscript gate

Write the study as a formal auxiliary computational evaluation aligned with the paper’s original research object and contribution. Do not carry operational logs, delegation status, user-addressed language, or internal process narration into the manuscript. State exact model, design, artifacts, metrics, exclusions, and limits. Do not mention human evaluation if the requested paper scope excludes it.

## Minimal reporting checklist

- model identifier, decoding configuration, seed, and evidence-manifest hash;
- factorial cells and condition exposure contract;
- valid, rejected, and error counts by method/condition;
- fixed-bank hash and paired-comparison denominators after contract filtering;
- explicit distinction between verified execution and semantic/factual conclusions;
- reproducible ledger, prompt audit, verifier report, and compiled manuscript.
