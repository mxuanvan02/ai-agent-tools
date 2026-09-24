# Manuscript section roles and evidence-bound experimental reporting

Use this note when completing a methodological or applied AI paper whose implementation artifacts are more mature than its semantic/effectiveness evidence.

## 1. Keep section roles distinct

### Abstract
Write a compact synopsis of the research problem, proposed method, operating principle, and intended contribution. Unless the venue or study design requires otherwise, do not turn the abstract into an artifact ledger. Avoid counts of packages, receipts, pilot cells, implementation failures, or caveats that belong in Results/Limitations. Include quantitative results only when they are central, validated study findings—not merely runtime diagnostics.

### Introduction
Build the argument in this order:
1. research context and why the problem matters;
2. precise failure/gap in existing approaches;
3. consequences of leaving the gap unresolved;
4. research objective;
5. high-level methodological idea;
6. explicit contributions;
7. scope and positioning.

Do not use the Introduction as a compressed Results section. Avoid implementation-status narration such as “we completed N cells” or defensive statements about failed runs. A methodological paper may state its scope positively (e.g., “the paper develops an auditable generation and validation framework”) rather than leading with what it does not prove.

### Experimental protocol
Separate:
- deterministic artifact validity (schema, hashes, package isolation, portability, clean-room reconstruction, request/receipt linkage);
- semantic validity (answerability, grounding, minimum sufficient evidence, modality necessity);
- effectiveness (baselines, ablations, yield/quality metrics, uncertainty).

Passing the first layer does not establish the second or third.

### Results
Report only completed, admissible evidence. Keep failed runs, dry-runs, placeholders, exploratory routes, and revoked artifacts outside effectiveness denominators. A small unadjudicated pilot should be labeled a machine diagnostic or case study, not a full experiment.

### Limitations and conclusion
State unresolved adjudication, source rights, leakage, sample dependence, selection bias, model dependence, and missing baseline/ablation evidence directly. Conclusions must match the strongest verified evidence layer.

## 2. Full-scenario request gate

When asked to “run all scenarios” or “finish for submission”:
1. inventory candidates, packages, predictions, annotations, rights, and provenance;
2. define the admission gate before running anything;
3. classify every item as runnable, hold, reject, placeholder, failed, or exploratory;
4. run only matched conditions with equivalent evidence boundaries;
5. never manufacture missing human labels, reference atoms, regions, programs, or scores;
6. if the full study is blocked, complete the strongest defensible paper shape and identify the exact empirical upgrade needed.

Do not repeatedly promise a full matrix after discovering that controls or candidates are not experiment-ready. Reframe once, update the plan, and proceed with the bounded study.

## 3. Multimodal evidence ladder

For T/TL/TLV studies, distinguish:
- T: text only;
- TL: text plus extractor-recoverable layout/structure;
- TLV: text, layout/structure, and actual pixel payload.

A file path is metadata, not pixel evidence. Base64/image bytes plus content hashes establish request construction, not that a model semantically used the image. Model answerability patterns do not define human semantic sufficiency.

## 4. Provider/parser evidence

When a provider emits SSE or duplicated content:
- preserve raw response hash and HTTP metadata;
- parse protocol semantics before relaxing validation;
- collapse duplicated JSON only under a narrow, documented rule (e.g., canonical-identical adjacent objects);
- reject ambiguous or different objects;
- write normalization metadata into receipts;
- test parser and caller return types before rerunning.

## 5. Academic release boundary

Split public code/manuscript release from restricted data when source rights are unresolved:
- public repository: manuscript, code, summaries, citations, license boundaries, non-sensitive reproducibility outputs;
- private dataset: source-derived images, full embedded-pixel packages, predictions, receipts, validation reports, and a restrictive data card;
- verify secrets, host paths, revoked artifacts, manifest hashes, clean clone/build, remote commit, dataset visibility, and uploaded file list.

Never infer an open license for source-derived content from local possession or research use.