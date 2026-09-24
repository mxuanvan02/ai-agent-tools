# bài TQA-generation manuscript and release lessons (2026-07)

## Canonical framing
- Research problem: construct traceable multimodal textbook-QA items from textbook evidence.
- bài TQA-generation is the central construction protocol in that pipeline, not a separate encoder and not a dataset-release claim.
- Construction chain: typed motif → restricted derivation → answer atoms and provenance traces → four-option question → structural checks.

## Experimental corpus wording
Describe only the supported, submission-relevant source facts: eight multimodal chunks from five Vietnamese law textbooks used in legal training at the Institute of Open Education and Information Technology, the university; ten associated figures/tables; three paired input packages (`T`, `TL`, `TLV`) for 24 total inputs. Do not mention internal pipeline names, other papers, or unrelated corpus-scale counts.

## Evidence and claims gate
- Final experimental model/configuration: `gpt-5.6-luna`, temperature 0, seed 20260804.
- Generation design: 8 chunks × 3 evidence packages × 3 protocols (Direct, Answer-first, bài TQA-generation) = 72 trials.
- Fixed-question design: 24 frozen ECM questions × 3 packages = 72 planned answer trials; 70 contract-conformant. Paired answer-index agreements: T–TL 100.0%, T–TLV 95.7%, TL–TLV 95.5%.
- Use only metrics actually emitted/verified by the ledger. Contract/schema validity is execution compliance; it is not legal correctness, overall question quality, modality benefit, or a method-superiority result.
- Do not claim component ablations, self-refinement, human evaluation, multi-model findings, or visual causal effects unless the corresponding valid artifacts exist.

## Manuscript prose preference
Use affirmative, evidence-led prose. State what the method, corpus, design, and results establish. Do **not** insert pre-emptive negative sentences such as “this does not establish X” solely as a defensive disclaimer. Keep limitations in their dedicated section and only where needed to delimit a supported claim.

## Back matter, final values
Use real finalized text, never leave placeholders in a submission PDF:
- Acknowledgment: thank the Institute of Open Education and Information Technology, the university, for research data and laboratory environment.
- Funding: project code DHH2026.
- Conflict of Interest: authors declare no competing interests.
- Generative-AI disclosure: AI assisted grammar/language editing, software development, and illustrative-figure preparation; identify the experimental model separately; authors retain responsibility for final content.

## Public release boundary
The public repository may contain code, contracts, schemas, tests, documentation, and synthetic rights-cleared fixtures. Do not publish source-derived textbook chunks/images or internal execution records without separate permission. Before declaring a repository update complete, verify tests, package/build or relevant smoke checks, git diff, commit identifier, and remote push result.

## Final verification
After edits: compile LaTeX to clean resolution of references and verify rendered PDF. Audit factual claims against the final ledger, then confirm the canonical source path and PDF checksum before sending.