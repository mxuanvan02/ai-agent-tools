# Paid run → manuscript → clean release: checklist

## 1. Freeze and accounting
- Treat append-only ledger `CALL_STARTED` records with terminal records as the authoritative HTTP-attempt count across every replacement freeze and smoke run.
- Never sum execution-checkpoint `calls`: it may represent planned cells, imported cells, or multiple replicates.
- Reconcile separately: historical attempts, current-freeze smoke, fresh paid attempts, imported/satisfied artifacts, and cumulative total against the hard cap.
- Distinguish planned cells, fresh HTTP attempts, usable interfaces, and gate-valid chunk-level statistical units.

## 2. Fail-closed import and ITT
- A paid HTTP-200 response that fails parser/schema/guard validation remains a terminal ITT outcome; do not retry it merely to improve yield.
- Cross-freeze import requires independent verification of origin/current freeze, exact task and payload reconstruction, provider/model identity, idempotency metadata, sidecar path and byte hash, and current outcome classification.
- Imported records are satisfied artifacts, not new paid attempts. Preserve rejected artifacts and downstream unavailable outcomes.

## 3. Analysis before prose
- Build a digest-stamped statistics JSON first, then derive manuscript numbers from it.
- Recompute ITT vectors from raw execution/checkpoint artifacts; enforce chunk pairing and census size.
- Use exact McNemar and exact Clopper–Pearson intervals as preregistered. A low-yield stop rule may block component probes or judging while the complete ITT paired table remains estimable; call a nonsignificant result inconclusive, never equivalence.
- If a sensitivity floor fails, report the control counts, separation, replicate disagreement, threshold, and stop verdict. Suppress Delta_perm/bootstrap/visual-necessity/judge claims when the protocol requires a passing floor.
- Mark upstream-dependent zero-yield arms as vacuous/unavailable, not as measured null performance.

## 4. Manuscript and release QA
- Search all sections and includes for stale pre-results tense, old-design numbers, unsupported claims, and inconsistent denominators before editing.
- Rebuild the PDF after every final source/layout edit. Inspect log for overfull/underfull boxes and inspect every page visually.
- Remove manual bibliography triggers that create an almost-empty final page unless the venue explicitly requires them; then equalize columns deliberately.
- Keep table footnotes outside `tabular` where possible.
- Build a clean ZIP only after QA. Exclude copyrighted textbook text/images, credentials, absolute local paths, backups, caches, generated build junk, and artifacts from superseded designs. Include manifests, non-sensitive summaries, source, figure generators, and checksums. Do not claim the release is complete until the final PDF and ZIP have both been rebuilt and verified.

## 5. Private experiment/run handoff
- Treat a public reproducibility repository and a private run archive as separate products. Public Git receives code, protocol, tests, schemas, documentation, and rights-cleared synthetic fixtures only. Private archives may contain authorized corpus inputs, raw provider responses, result sidecars, execution ledgers, and freeze/smoke artifacts.
- Preserve the original run directory names and append-only evidence files. For an ECM-style run handoff, include the paid run's `EXECUTION.jsonl`, `RUN_LEDGER.jsonl`, import manifests, primary-statistics artifact, sensitivity verdict, `results/`, and `responses/`; include the matching freeze manifest/dry-run ledger and smoke results/ledger/responses.
- Do not invent a named artifact merely because the requester uses an informal label such as “gate ledger.” First enumerate the run tree and report where gate evidence actually lives. If no dedicated file exists, say so and point to the exact existing files.
- Package from an explicit allowlist into a fresh staging directory. Add an inventory/README and per-file SHA-256 manifest; verify every staged hash, test ZIP integrity, and scan member names and text for credentials and machine-local absolute paths before delivery.
- Keep raw paid-run archives private unless redistribution is explicitly authorized. Do not push restricted run records or textbook-derived material to a public repository.

This reference captures the verified ECM–TQAG reconciliation lessons; adapt names and paths to future projects.
