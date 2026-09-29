# ECM–TQAG: Qwen TQA Generation and Release Gate

Use for any multimodal Qwen TQA generation run, audit, or publication decision.

## Decision boundary
1. Before any paid/full run, state the exact model ID, provider, whether it accepts images, estimated cost basis, generator-only role, and proposed experimental scope. Obtain người dùng's explicit approval. Do not silently substitute a model or relabel an older ledger.
2. Qwen is the generator only. Do not invoke another LLM as an automatic judge, nor use judge outputs in the study, unless người dùng explicitly asks again. Schema/trace/hash checks are allowed but must never be described as semantic quality evaluation.
3. Pilot difficult visual cases first. A parse-valid JSON item is only a transport/schema pass, not proof that the TQA is usable.

## Method–implementation alignment gate
When người dùng says **“sửa code cho đúng Method”**, preserve the scientific method and raise the implementation to it. Do **not** silently weaken, rename, or delete manuscript concepts merely to match incomplete code. If changing the Method itself may be preferable, present that as a separate decision and wait for explicit approval.

For each claimed methodological stage (for example `document graph → matched motif → restricted program → answer atoms`):
1. Recover the exact manuscript contract and map every claim to a concrete code artifact, validator, ledger field, and test. Do not treat renamed legacy fields as implementation.
2. Prefer deterministic local stages for claims that should be executable: validate source-bound typed graph nodes/edges; match a finite, versioned motif predicate; compile only a closed opcode/type grammar; execute it locally; derive answer atoms from executor output; seal the construction with a receipt.
3. The model may propose inputs to deterministic stages, but must not self-certify their outputs. A realizer receives only the sealed construction and may not alter atom IDs/values, program trace, or locked anchors.
4. Use one shared contract library for online runner validation and offline audit replay. Add positive tests plus tamper tests for every layer (graph relation/binding, motif, program, atom, receipt, selected answer, trace, anchor).
5. Bump prompt/schema/ledger versions whenever the contract changes. Stop the incompatible active run, keep its partial ledger only as provenance, and never mix or relabel it as evidence for the new method.
6. Validation order: targeted unit tests → syntax/type checks → exact dry-run design/call count → manuscript compile/layout check → versioned pilot → replay audit → full matrix only after pilot approval.
7. Report mechanical guarantees narrowly: replayability and provenance validity do not prove semantic/legal correctness, pedagogical quality, unique-best-answer validity, or counterfactual image necessity.

## Evidence and quality gate
- Preserve frozen manifest, input/prompt hashes, raw provider response, seed, decoding, model ID, and provider provenance.
- Require exactly four non-duplicate options, selected answer/index consistency, evidence anchor, and method-specific trace contract.
- Audit anchors against frozen text/structure mechanically. Separately review single-best-answer validity, non-triviality, duplicates, legal/semantic correctness, and genuine image grounding.
- Treat model refusal for insufficient evidence as valid information; never force a filler question from thin evidence.

## Interrupted runs and malformed output
- Never overwrite an original ledger.
- Resume only after reconstructing the immutable plan and proving model, seed, manifest hash, prompt/input hashes, and run IDs match. Append only missing cells.
- Keep rejected parent records. Generate replacements into a separate retry ledger with parent run ID and replacement prompt hash.
- If a raw response has a known invalid JSON escape, preserve raw text/hash and record an explicitly narrow normalization separately. Do not silently edit content or turn it into a normal original record.

## Publication gate
Before Hugging Face upload: complete generation, retain an audit report, select only reviewed clean items, remove protected textbook excerpts/images/raw prompts/credentials unless rights are confirmed, verify `hf` authentication and target repository visibility, then ask/confirm target and public/private scope if not supplied. Do not upload merely because the batch parsed.

## Reporting to người dùng
Use short Vietnamese, plain language. Lead with current counts and clearly separate: generated, parse-valid, mechanically checked, manually reviewed/usable, rejected, and pending. Do not claim a run, ledger, or path exists without checking it in the current workspace.

## Generator/judge endpoint discipline (learned from a real cross-run leak)
A pilot once silently inherited `MODEL="claude-sonnet-4.6"` from a copy-pasted runner instead of the intended Qwen generator, and a `full_v2` run executed 48 cells against the wrong generator before anyone noticed — wasting the run and blocking a valid v1↔v2 paired comparison (method and generator model became confounded). Prevent recurrence:
1. Generator calls always go to OpenRouter; judge calls always go to OmniProxy. Hard-code this mapping in the runner and make it refuse to start if role↔endpoint don't match — don't rely on remembering to pass `--model`.
2. Before trusting ANY generator run as a baseline, verify `generator_model` in the actual output rows (not the CLI args you think you passed) matches what you intend. A runner inherited from an older version can carry a stale default that silently overrides your flag.
3. Judge model must be a different family from the generator (cross-family, avoid self-preference). Re-derive this check whenever either model changes — a fix to one side ("switch generator to Qwen") can silently satisfy or break this constraint on the other side.
4. When a paid/full run is later found to have used the wrong model or endpoint, do NOT try to salvage it by reasoning around the confound — discard it as a baseline and rerun. Report the wasted cost plainly; don't reframe it as still-useful.

## Pipeline guard debugging — mechanical instrument, not model quality
When a multi-stage guard/gate pipeline (compile → execute → seal → realize, or similar) shows a high or shifting reject rate, triage BEFORE concluding the model or the guard is broken:
1. **Classify every reject reason before touching code.** Split into (a) contract violation — the guard caught something real, keep it; (b) transport failure — the response was cut/malformed in flight, needs retry or a parser fix; (c) your own instrument bug — the guard or the prompt has an internal contradiction. Never fix (a) by loosening the guard.
2. **Cross-guard threshold consistency is a real bug class.** If two functions independently enforce related budgets (e.g. one truncates an excerpt by characters, another checks it by words), they WILL drift out of sync on edge cases (short documents, non-Latin scripts with different chars/word ratios) and reject valid output for no semantic reason. Fix: derive both from one shared constant/formula, and add a round-trip self-test asserting "the sealer's own output always passes its own guard" — including a stress case with an absurdly long/short input.
3. **A catalog/schema entry whose op ordering fights the model's natural decomposition will look like a model failure but is a design bug.** If every rejected case for one specific category shares the same reason (e.g. one motif's step-2 op mismatch, 5/5 times) while the model's actual output is internally coherent, the fix is almost always to re-order the schema to match the natural quote-then-reason flow (anchored/quotable steps first, derived/reasoning step last) — not to blame the model.
4. **Truncation detection needs more than a fence check.** Streams can be cut mid-JSON without ever opening a code fence (bracket depth stays unbalanced instead). Detect truncation by tracking `{}`/`[]` depth outside string literals, not just by "opening ``` with no closing ```". Conversely, don't misdiagnose a complete-but-verbose response (valid JSON followed by trailing prose/notes) as truncation — recover it by extracting the first balanced top-level JSON object instead of discarding the row.
5. After any pipeline fix, always re-run the FULL self-test suite (all versions, e.g. v2 AND v3, plus any transport-specific test file) before re-piloting — a catalog/schema edit for one version can silently break an assertion in an older version's test file (e.g. a hardcoded enum that no longer matches after a motif's op set changed).
