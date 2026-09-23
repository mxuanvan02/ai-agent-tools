# Evidence-bound multimodal TQA generation and release gate

## When to use

Use for generating Vietnamese text–table–diagram–image MCQs from a frozen corpus, especially when comparing evidence conditions (for example text-only, text+structure, text+structure+vision) or preparing an auditable dataset/research artifact.

## Non-negotiable boundaries

- Treat the generator, validator, semantic reviewer, and publisher as separate roles.
- If the project owner specifies a generator family/provider, use that model **only for generation**. Do not introduce LLM judges, model comparisons, or an AI scoring stage without explicit approval.
- A response that parses as JSON is not proof that the item is correct, useful, image-grounded, or publishable.
- Never overwrite an original generation ledger. Attempts, normalizations, retries, and selected replacements require distinct provenance.
- Do not publish source textbook pages, images, long excerpts, raw prompts/responses, or credentials. A Hugging Face upload needs an explicit repository target, visibility decision, authentication, and rights review.

## Workflow

1. **Freeze and inspect the evidence unit.** Record item/chunk ID, condition, text, document structure, image paths, byte sizes, and SHA-256 hashes. Before calling a model, inspect representative hard visual cases with the *actual attached pixels*; router capability flags or model names are not enough evidence that vision works.
2. **Pilot before the matrix.** Use a small, predeclared set that includes diagrams, maps, tables, multi-image cases, and prior failure modes. Pin provider-qualified model ID, prompt version, decoding parameters, seed (where supported), manifest hash, and request/output schema.
3. **Use a strict generation contract.** Require exactly one Vietnamese MCQ, four non-duplicate choices, a valid answer index, an evidence anchor, and protocol-specific fields. Permit the explicit refusal object `{"reject_reason":"insufficient_evidence"}`. Instruct the model not to use outside knowledge, invent image labels, or infer unsupported relations.
4. **Validate in two layers.**
   - *Mechanical gate:* JSON/schema, choice count/uniqueness, index range, answer-to-index consistency, allowed anchor source, literal text-anchor match, structure/image reference format, manifest hash, and image integrity.
   - *Content gate:* check answer correctness, one-best-answer validity, distractor plausibility, educational value, duplicate items, and actual visual grounding. Mechanical pass must be described only as mechanical pass.
5. **Diagnose evidence sparsity before blaming the model.** Inspect the source chunk, neighboring chunks, and original document. A title-only cover page or figure-only page may be a valid source unit, not truncation. Exclude cover/metadata pages from a quality dataset. For an image-only figure, allow visual questions only in the image-bearing condition; do not demand a meaningful text-only MCQ.
6. **Preserve experimental comparability.** Never silently add surrounding pages or full-document context to a frozen condition. If more context is required, create a separately named enriched-window artifact with a new manifest/hash and report it as a different design.
7. **Handle rejected cells explicitly.** Distinguish:
   - `model_insufficient_evidence`: model safely refused due to insufficient input;
   - validator rejection: malformed JSON, markdown fences, thinking text, schema failure, or unsupported anchors;
   - transport/provider failure.
   Keep the raw output and rejection reason. A refusal is evidence about the input/contract, not a result to hide.
8. **Retry only after the initial batch is complete.** Reconstruct the frozen plan and verify immutable fields (experiment/model/manifest hash/input hash/prompt hash/seed) against the source ledger. Retry into a separate replacement ledger with `parent_run_id`, parent reason, replacement prompt hash, raw response, and status. Ask for a materially different, non-trivial item; retain refusal as an allowed outcome.
9. **Normalize only transport-level defects, narrowly.** For a known malformed escape such as `\*`, retain exact raw response and raw hash, record the exact one-rule normalization and normalized parse result, and ensure content fields are otherwise unchanged. Do not use normalization to repair semantic content, options, answers, or evidence anchors.
10. **Select the release subset.** Exclude rejects, failed mechanical audits, semantically dubious items, title-only items, and duplicates. For image diagrams, ask only facts visibly supported (labels, counts, adjacency/arrow direction); do not infer legal/procedural meaning not stated by the image.
11. **Package and publish last.** Build a clean release artifact containing only selected items, de-identified/non-copyright-sensitive evidence representations where allowed, a datasheet/card, license/rights notes, provenance schema, and reproducible validation. Confirm exact Hugging Face repo ID, public/private setting, and authorized account before using `hf` CLI.

## Communication for người dùng

- Speak Vietnamese plainly and lead with the status: how many generated, how many mechanically valid, how many content-qualified, and what remains.
- Do not say "done" merely because a background process started, a JSON parser passed, or a file path was assumed. Inspect the artifact and report exact counts/paths.
- Explain rejections in everyday terms: whether Qwen refused because the supplied slice lacks facts, or the local validator rejected formatting. Do not call it a semantic error without evidence.
- When a model choice has not been explicitly approved, present it as a proposal/pilot rather than a final configuration.

## Common pitfalls

- Using an advertised `supports_image` flag as proof that the route actually sees images.
- Calling independent LLM judges without authorization when the user only asked for generation.
- Reporting a full matrix as usable when many outputs are duplicate, trivial, ungrounded, or only parse-valid.
- Mixing retry results into the first-run ledger or concealing model refusals.
- Treating title-only and cover-page chunks as legitimate substantive-question inputs.
- Altering a frozen evidence condition with neighboring context to make a failed cell pass.
