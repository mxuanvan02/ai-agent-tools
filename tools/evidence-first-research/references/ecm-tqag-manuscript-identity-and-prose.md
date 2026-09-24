# bài TQA-generation: manuscript identity, experimental role, and prose gate

## Canonical identity

**Research problem:** construct traceable multimodal textbook-QA (TQA) items/datasets from educational legal documents.

**Proposed method:** bài TQA-generation is the evidence-first generation protocol inside that construction task. Its sequence is: motif/document-graph evidence → restricted derivation → answer atoms and provenance traces → question/choices realization.

**Experimental corpus:** a pre-existing multimodal corpus supplies the input chunks, document structure, and original images. It is a testbed, not the contribution or a dataset-release story of the bài TQA-generation paper.

Do not collapse this into either wrong extreme:
- not a generic standalone MCQ-generation/model-leaderboard paper;
- not a dataset legal-QA/TQA_Pipeline dataset-release, release-lineage, split-balance, or 14k-item audit paper.

## Required corpus description

Use concise, affirmative academic wording. For the verified pilot:

> The experimental corpus comprises eight multimodal textbook chunks sampled from five Vietnamese law textbooks used in the legal training curriculum at the Institute of Open Education and Information Technology, the university. The selected chunks contain ten source figures and tables. Each chunk is represented as three paired evidence packages: text only (T), text with document structure (TL), and text with document structure and original image pixels (TLV), yielding 24 input packages.

Do not mention that the corpus came “from another paper,” project-internal repository names, or unrelated corpus/release counts.

## Experimental framing

The Experimental section evaluates bài TQA-generation as a method for constructing traceable items from that corpus:
- fixed backbone when requested (currently `gpt-5.6-luna` only);
- compare controlled generation baselines and ECM variants only when actually executed and verified;
- evidence packages T/TL/TLV are controlled input conditions;
- distinguish deterministic construction/integrity checks from semantic claims.

Schema parsing, hash/package integrity, trace-field availability, and answer-index stability are operational diagnostics. Label them exactly as such; do not call them legal correctness, image necessity/benefit, overall quality, causal modality effect, or SOTA.

## Writing style gate

Before drafting/revising:
1. Read the actual canonical manuscript supplied by the user, not an adjacent repository’s paper tree or a compacted summary.
2. State the paper identity in one sentence and check every abstract/intro/method/experiment/conclusion edit against it.
3. Use formal paper prose only. Exclude internal process narration, worker status, interaction with the user, defensive disclaimers, and unnecessary negative caveats in corpus-description paragraphs.
4. Keep limitations where scientifically necessary, but do not append reflexive “this does not establish…” sentences to every factual description. Answer the requested scope directly and concisely.
5. Never call a manuscript ready or send it until the canonical source, PDF, experiment artifacts, and claims have been aligned and verified.

## Session-specific failure to avoid

A prior revision mistakenly treated a dataset-release manuscript as canonical and reframed bài TQA-generation as an “auxiliary” study; a subsequent correction mistakenly swung to a standalone method-first framing. Both are wrong. The correct framing is **dataset construction via the bài TQA-generation method using a pre-existing multimodal corpus as experimental input**.
