# Manuscript claim–release audit: bài TQA-generation lessons

## Trigger
Use for academic manuscript revision where the user requires neutral wording, evidence for every claim, complete citation review, and synchronized public artifacts.

## Claim matrix
Classify every sentence as:
1. **Literature** — cite a source whose actual scope supports the wording; verify DOI metadata and semantic fit.
2. **Method definition** — define notation, protocol, inputs, and boundaries explicitly.
3. **Artifact/result** — bind to a versioned repository, manifest, table, figure, receipt, or machine-readable record.
4. **Limitation/design proposal** — state as scope, hypothesis, or recommended future evaluation, not as an observed result.

A DOI resolving is insufficient. Check author list, title, venue/type, year, pages/article number, DOI, and whether the source supports the exact sentence. Track missing, unused, and malformed citation keys mechanically.

## Evidence boundary
Keep deterministic validation separate from semantic/effectiveness evaluation. Schema validation, hashes, image decoding, clean-room reconstruction, and complete response records establish technical integrity/bookkeeping only. They do not establish answer correctness, source grounding, human agreement, modality necessity, effectiveness, or multimodal gain. Machine-observed T/TL/TLV patterns must not be presented as semantic labels when adjudication is absent.

For formal sufficiency notation, define both complete-answer support and atom-level support, and state that atom support alone does not determine the item label: joint composition, order, cardinality, numerical operations, completeness, and alternative answers can still fail.

Define TL operationally as only text plus relations emitted by the fixed layout extractor. Information requiring pixel inspection beyond those relations belongs to TLV. Differences across packages are extractor- and package-dependent observational contrasts, not representation-invariant causal effects.

## Neutrality sweep
Remove provider/model routes when not scientifically necessary, run names, parser/debug history, revoked/invalid packet history, TODO/status language, local paths, credentials, and release workflow narration. Replace “planned/held-out/admitted/pending” where possible with reader-facing scope or dataset-status wording. State human review as outside the diagnostic scope when it was not performed. Do not hide necessary limitations; express them as neutral boundaries.

Figures need independent QA: inspect captions, notation (T/TL/TLV), escape sequences, typos, text containment, arrow/box overlap, unexplained inventory counts, and internal-status wording. LaTeX success does not validate figure semantics or visual legibility. Regenerate a figure when its text or counts change, then vision-check the rendered result.

## Release gate
After edits, rebuild with multi-pass latexmk; check zero fatal errors, undefined references, missing citations, and overfull boxes. Audit citation usage and bibliography entries, PDF text, fonts, secrets, absolute paths, and forbidden source-derived material. Run the public-release verifier, regenerate manifest/checksums, inspect git diff, commit, push, and verify local/remote SHA and release tag. Only then report completion, with exact hashes and explicit remaining limits.

## Session-specific evidence
The bài TQA-generation audit used a versioned artifact citation (`ecmtqagartifact`) for inventory, verification records, and machine outputs; a six-cell/two-candidate diagnostic; a private boundary for rights-sensitive source-derived pixels; and a neutral methodological scope. These values are examples, not defaults for future projects.
