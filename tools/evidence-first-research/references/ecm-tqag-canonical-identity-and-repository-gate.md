# ECM–TQAG identity, manuscript, and public-repository gate

## Canonical study identity
- Research problem: construct traceable multimodal TQA items from textbook evidence using the ECM–TQAG protocol.
- Experimental corpus: a pre-existing multimodal input corpus, not this paper's dataset-release contribution.
- Describe the source succinctly as Vietnamese law textbooks used in legal training at the Institute of Open Education and Information Technology, the university.
- Current experimental input statement: 8 multimodal textbook chunks from 5 textbooks, associated with 10 source figures/tables; each has T (text), TL (text + document structure), and TLV (text + structure + original image pixels), for 24 paired input packages.
- The final computational suite must use only `gpt-5.6-luna`; never mix Terra or multi-model results into the final evidence.

## Identity gate before any manuscript action
1. Locate and inspect the actual manuscript supplied or explicitly designated by the user; do not infer canonical status from a similarly named local paper tree.
2. State the paper identity in one sentence and wait only if it remains ambiguous. Do not rewrite the contribution framing from a prior project.
3. Keep ECM–TQAG central as the evidence-first construction protocol: motif/document-graph instance -> restricted derivation -> answer atoms and provenance trace -> question realization and checks.
4. Treat the multimodal corpus as experimental input. Do not import dataset-release counts, historical pipelines, or claims from another paper unless the user explicitly asks and artifacts substantiate them.
5. Before sending a PDF, verify its source path/title and that its introduction, method, experiments, and conclusion all match this identity.

## Experimental-writing gate
- Present the input corpus, conditions, model, baselines, ablations, metrics, and their meaning directly.
- Distinguish deterministic integrity/contract metrics from semantic or factual quality metrics; do not overclaim.
- Do not turn a schema-parse rate or fixed-answer-index stability diagnostic into accuracy, legal correctness, modality benefit, or method superiority.
- Never fabricate unrun ablations or human scores.
- Do not add defensive, negative, or internal-process prose merely to pre-empt criticism. State the factual design and result that matter.

## Public repository boundary
- Public repository may contain source code, schemas, synthetic rights-cleared fixtures, tests, and reproducibility instructions.
- Do not publish source textbook PDFs, source-derived chunks/images, historical model outputs, private credentials, or internal artifact paths without explicit redistribution permission.
- Align README/schema/CLI/docs with the manuscript's protocol identity; do not describe an answerability-only demo if the code supports constructed TQA items.
- Before commit/push: inspect the staged diff, run unit tests, run package/build and clean-install smoke checks, then record the commit hash and remote state. If Git identity is absent, ask the user for the repository-local author name/email rather than guessing.

## Communication style for this project
- Be concise and declarative. Give the requested artifact/status first.
- Avoid unnecessary disclaimers, self-justification, internal workflow narration, or statements about what is *not* being claimed unless a limitation is scientifically necessary.
- When corrected, acknowledge the exact mismatch, replace the incorrect framing, and apply the canonical identity gate before proceeding.
