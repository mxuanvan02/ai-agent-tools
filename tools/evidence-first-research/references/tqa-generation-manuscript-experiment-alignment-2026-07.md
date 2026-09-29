# bài TQA-generation manuscript and experimental alignment (2026-07)

## Identity lock
- The paper is about **bài TQA-generation as an evidence-first protocol for constructing traceable multimodal textbook TQA items**.
- Its experiment uses a pre-existing corpus only as the input testbed; it is neither a dataset-release paper nor a standalone model-leaderboard paper.
- Treat the manuscript supplied by the user as canonical. Do not infer the canonical paper from nearby repository folders or an earlier PDF.

## Experimental corpus wording
Use affirmative, concise prose only when requested:

> The experimental corpus comprises eight multimodal textbook chunks sampled from five Vietnamese law textbooks used in the legal-training curriculum at the Institute of Open Education and Information Technology, the university. The selected chunks contain ten source figures and tables. Each chunk is represented as three paired evidence packages: text only (T), text with document structure (TL), and text with document structure and original image pixels (TLV), yielding 24 input packages.

Do not add defensive or unnecessary negative statements (for example, that "multimodal-ready" does not prove visual necessity) unless the user specifically asks for limitations.

## Evidence and claims gate
1. Reconstruct the experiment design from verified artifacts before drafting results.
2. Name only methods actually present in the ledger. Never describe a 72-cell `Direct / Answer-first / ECM` matrix as a self-refine or component-ablation suite.
3. Separate protocol-specific structural measures from common measures. A field absent by design is `N/A`, not zero or an inferior score.
4. State exact denominator and unit for each rate; retain rejected/failing trials in the report.
5. Do not elevate schema parsing, literal matching, hash integrity, or answer-index agreement into legal correctness, semantic grounding, visual necessity, or method superiority.
6. After editing, compile the canonical manuscript, inspect warnings/references, hash the final PDF/source, and send only that compiled artifact.

## Repository release boundary
A public bài TQA-generation repository may contain schemas, code, tests, documentation, and rights-cleared synthetic fixtures. Do not publish source textbook chunks, images, private ledgers, raw model outputs, or credentials without explicit redistribution authorization.
