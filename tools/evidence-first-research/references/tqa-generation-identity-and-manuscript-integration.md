# ECM–TQAG: identity gate and manuscript integration

## Canonical research identity
ECM–TQAG is a paper on an **evidence-first protocol for constructing traceable multimodal textbook TQA items**. Its central sequence is:

\[
G_m \rightarrow z \rightarrow (A,\Gamma) \rightarrow q \rightarrow \mathcal C.
\]

It is neither (a) a standalone legal-QA model leaderboard nor (b) the earlier dataset-release paper. ECM–TQAG is the construction method; its experimental corpus supplies the multimodal textbook chunks used to test that method.

## Canonical manuscript and source boundary
Before editing, identify the actual paper source supplied or confirmed by the user. In this work it was the `ECM_TQAG_ICTC2026/main.tex` manuscript from the user-provided archive, rather than `TQA_Pipeline/research/paper_work/paper/`.

The experimental corpus can be drawn from pre-existing multimodal textbook material, but the manuscript should describe it directly and independently as Vietnamese law textbooks used in legal training at the Institute of Open Education and Information Technology, the university. Do not frame it as copied from another paper, an internal pipeline, or a dataset-release contribution.

## Verified experimental configuration (2026-07/08)
- Corpus: 8 multimodal chunks from 5 Vietnamese law textbooks; 10 associated figures/tables.
- Inputs: paired `T` (text), `TL` (text + document structure), and `TLV` (text + structure + original pixels), yielding 24 packages.
- Fixed model: `gpt-5.6-luna`, temperature 0, seed 20260804.
- Generation matrix: 8 chunks × 3 packages × 3 protocols (Direct, Answer-first, ECM–TQAG) = 72 trials; 72 parsed/contract-conformant.
- Fixed-question comparison: 24 frozen bài TQA-generation TLV questions × 3 packages = 72 answer trials; 70 contract-conformant. Answer-index agreement: T–TL 23/23 (100.0%); T–TLV 22/23 (95.7%); TL–TLV 21/22 (95.5%). Two nonconformant records had truncated question hashes and must remain counted as contract failures.

## Manuscript alignment rules
1. Begin with the TQA construction problem, then state ECM–TQAG as the method, then introduce the corpus/testbed and evaluation.
2. Ensure every method component has a corresponding observable record/measurement: answer-first → answer/choice consistency; ECM → trace availability and literal trace support; all methods → response-contract validity.
3. State metrics precisely. Contract validity measures schema/protocol execution, literal support measures explicit string support, and fixed-question agreement measures answer-index stability. Do not relabel them as legal accuracy, semantic grounding, causal modality benefit, or general question quality.
4. Keep the final prose affirmative and academic. State what the corpus, method, experiment, and evidence establish. Do not insert defensive negative sentences or internal-process narration unless a limitation is scientifically necessary.
5. Remove stale framing wholesale (e.g., two-candidate diagnostics, unrelated dataset-release counts, Terra/multi-model references, absent ablations) rather than patching selected sentences.
6. Finish with a claim-to-artifact audit and compile from the canonical manuscript directory. Check that Abstract, Introduction contributions, Method, Experimental setup/metrics/results, Limitations, and Conclusion tell the same story.

## User-facing writing preference
For this user, do not pad a paper with caveats such as “this does not establish X” when no scientific limitation requires it. Prefer concise declarative statements of the data and contribution. Keep limitations focused, evidence-specific, and in the Limitations section rather than scattering self-defensive prose through the manuscript.
