# Claim–implementation–artifact integrity gate

## Trigger
Use for academic research with prototypes, benchmarks, multimodal inputs, evidence packets, or claims about reproducibility/effectiveness.

## Required order
1. Mark affected claims/artifacts INVALID or withdrawn; do not hide the defect by wording changes.
2. Trace source → package/schema → runtime request → model response → scoring/report.
3. Fix implementation/schema first. If reproducibility is claimed, use a portable, self-contained, content-addressed artifact; do not rely on absolute host paths.
4. Rerun all matched conditions from the new artifact. Never mix old and new runs.
5. Write immutable per-attempt receipts containing package hash, payload/media hash, request hash, response status/format, and no secrets.
6. Run clean-room/portable-archive tests.
7. Audit manuscript, README, reports, ZIP, and example packet for semantic and numeric consistency.
8. Only then revise wording and release.

## Evidence levels
Separate: (a) JSON pointer/metadata, (b) bytes read by runner, (c) payload actually sent, and (d) runtime receipt/response. A path or local hash does not prove an archive is self-contained. Dry-run and clean-room tests prove construction/portability, not model effectiveness.

## Runtime and protocol rules
- Canonicalize one asset; two path fields are not two images. Prefer embedded bytes or a relative co-located asset with a manifest.
- Link predictions to immutable package and payload hashes.
- Support both OpenAI-compatible JSON and `text/event-stream`. For SSE, parse only `data:` JSON events, ignore `[DONE]`, concatenate assistant `delta.content`/message fragments in order, and retain HTTP status, content type, body length, and body SHA-256 in the receipt.
- Response parsing is a separate verification layer. Providers may wrap the answer object in Markdown or trailing prose: locate candidates with `JSONDecoder.raw_decode` from opening braces; never slice from the first `{` to the last `}`. Default to exactly one schema-matching occurrence. A narrowly documented provider quirk may be normalized only when every matching object is canonical-byte-identical and directly adjacent with no intervening content; record the object count, collapsed count, and canonical answer hash in both receipt and output. Distinct or separated objects remain ambiguous and must fail. Never silently “take the first object.”
- Preserve transport metadata when a later content/schema parse fails; do not overwrite a successful HTTP/SSE receipt with `http: null` merely because downstream extraction raised an exception.
- Each cell runs independently; use bounded retries and an immutable receipt per attempt. A failed cell must not abort other cells, and partial outputs plus an explicit run summary must still be written.
- Use a fresh output/receipt directory after any runner, schema, prompt, or parser change. Never mix failed attempts or artifacts from different runner versions into scoring.
- HTTP 200 with invalid/non-JSON/ambiguous output is still an error, never `COMPLETED`.

## Verification ladder before empirical use
1. Unit-test positive and negative parser fixtures: JSON body, SSE deltas, trailing prose, no object, malformed event, distinct/separated duplicate objects, and the explicitly supported adjacent-identical normalization case. Verify normalization metadata, not only the parsed answer.
2. Dry-run all matched cells and verify package decoding, condition isolation, request hashes, and receipt count.
3. Run a clean-room test from only released files; require zero absolute host dependencies.
4. Run the provider in a new directory; require every expected cell to be `COMPLETED` and receipts to retain transport metadata.
5. Audit package hash = receipt package hash; for pixel cells, decoded package bytes hash = request pixel hash = receipt pixel hash.
6. Score only after the full matched run passes. A parser unit test proves only the parser fixture, not provider compatibility or empirical completion.
7. Build the replacement archive without overwriting the withdrawn artifact. Re-extract the actual ZIP into a fresh temporary directory, run the verifier from inside that extraction, test archive integrity, recompute the ZIP SHA-256, and make the INVALID/superseded notice prominent in both README and delivery message.

## Claim boundary
Build success, ZIP creation, machine exact match, answerability, or vision triage are not by themselves semantic sufficiency, positive TL/TLV, multimodal gain, or human-verified effectiveness. Without appropriate adjudication, call items proposals/diagnostics. A 0/N failed run is BLOCKED/INCOMPLETE, not a negative empirical result.

## Contribution priority
The contribution is the verified final result and practical applicability: condition isolation, evidence grounding, traceability, and rerunnability. Submission is only the academic vehicle, not the contribution.
