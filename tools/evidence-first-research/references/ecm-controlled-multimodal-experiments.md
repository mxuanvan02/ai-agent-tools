# bài TQA-generation controlled multimodal experiments

## Purpose
Use this reference for an evidence-bound comparison of Direct, Answer-first, and bài TQA-generation when the same capable multimodal model is retained across conditions. The contribution is the **generation protocol and inspectable provenance**, never that ECM selected a stronger model.

## Experiment contract

### 1. Freeze the actual inputs
Do not infer scope from a similarly named or broader manifest. Verify and report separately:

- chunks;
- original images;
- input packages = chunks × conditions;
- API runs = packages × methods.

For every TLV image, verify path, byte count, and SHA-256 before planning and immediately before attaching it. Exclude machine-generated visual descriptions from the TLV evidence bundle.

### 2. Matched matrix
Hold fixed: model, endpoint, image/text source, decoding settings, timeouts, prompt versioning policy, and number of attempts. Vary only generation protocol:

- `direct`: evidence → question/choices/answer;
- `answer_first`: evidence/answer → question;
- `ecm`: motif → derivation → answer parts → trace → question.

Use condition-specific prompts:

- `T`: text only; do not mention images;
- `TL_struct`: text plus document structure; do not mention images;
- `TLV`: text/structure plus original image bytes; require an image-dependent question only for the relevant ECM-TLV condition.

A pilot such as 1 chunk × 3 conditions × 3 methods validates transport and contracts before expanding to 5 cases or the whole frozen set.

### 3. API provenance
For an OpenAI-compatible local proxy, probe `/v1/models`, then use `/v1/chat/completions`. Persist only non-secret execution information:

- base URL, requested and returned model;
- prompt version and SHA-256;
- input/manifest hash;
- raw response and raw-response SHA-256;
- image audit entries (filename, byte count, SHA-256);
- elapsed time, status, and error reason.

Never print or store credentials in reports.

### 4. Fail closed

- missing, altered, or mismatched image → `BLOCKED_INPUT_INTEGRITY`;
- backend cannot accept image input → `BLOCKED_UNSUPPORTED_IMAGE_INPUT`; never fall back silently to text;
- malformed JSON/choices/index → `REJECTED`;
- ECM missing `motif`, `derivation`, `answer_parts`, or `trace` → `REJECTED`;
- ECM-TLV with no non-empty `trace.source == "image"` → `REJECTED`.

`PARSED` proves a structural contract only. It does not prove factual correctness, quality, image dependence, or comparative advantage.

## Evidence for the contribution

Run counterfactual checks: keep a generated TLV question fixed and test whether it remains answerable from T and TL_struct alone. A question is image-dependent only after human reviewers confirm all of:

1. question/answer are correct;
2. the cited trace is visible and supports the answer;
3. removing image evidence leaves no reliable answer from text/structure.

Blind the method name and randomize outputs for at least two independent reviewers, then adjudicate disagreements. Report correctness, clarity/single-answer status, trace validity, image dependence, and rejection rate. Until this happens, use `EXECUTION_ONLY`, `STRUCTURAL_ONLY`, or `PENDING_HUMAN_REVIEW`—never claim ECM is better.

## Practical pitfalls

- Avoid nested triple-quoted prompts containing JSON; build response fixtures with `json.dumps` or write a dedicated script, then compile-check before any API call.
- Patch only after reading the target section; prefer small patches anchored by unique surrounding text.
- Do not say an experiment ran after a file write/patch. Require HTTP result, returned model, count of runs, artifact path, and checksum.
- If the runner integration is unfinished but the correctly configured API is available, use direct API calls for a clearly labelled pilot, then bring the same contract into the runner.
