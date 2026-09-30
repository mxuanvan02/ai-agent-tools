# bài TQA-generation Stage A release and durable audit pattern

## Durable locations and identity

Keep completed evaluation runs outside temporary workspaces in a dated, dedicated archive. For the 2026-08-03 bài TQA-generation Stage A snapshot:

- Internal locked archive: `/home/<user>/.hermes/artifacts/bài TQA-generation_blind_evaluation/locked_archives/stage_a_final_20260803/`
- Public repository: `https://github.com/OWNER/bài TQA-generation`
- Verified public commit: `ccd346171949bd7d02bae936f0b80e51842ae7df`
- Public artifact path: `artifacts/stage_a_model_evaluation/`
- Frozen packet SHA-256: `ef68612891484e1d41bc5b96e75e5a499a58ccb4152f9827e1f5a1812bd3fe3a`

The locked archive is a copy; do not delete or replace source artifacts after archiving.

## Archive contract

An auditable locked copy should contain:

1. frozen packet and packet hash;
2. one manifest and normalized CSV per evaluator;
3. allowed raw records for every expected item;
4. deterministic summary/reproduction script;
5. archive metadata describing scope and interpretation;
6. a recursive file hash manifest.

For each run verify, rather than infer:

- expected count equals completed count;
- failed count is zero;
- raw record count equals expected count;
- every row passes the local schema;
- resolved model belongs to the requested family;
- packet hashes match across runs;
- credential recording is false;
- summary can be regenerated from the archived records.

A runner process exiting successfully is not sufficient evidence of a successful evaluation.

## Public-release boundary

Publish only a de-identified allowlist: protocol fields, normalized ratings, deterministic script, summary, README, and hash manifest. Exclude restricted textbook content, evidence text/images, free-text notes, raw provider envelopes, deployment endpoints, and credentials. Run tests and a release-boundary/secret audit before commit.

Before claiming a push succeeded, verify repository, branch, license and remote; fetch the remote branch and require local commit SHA to equal remote SHA. Distinguish the public software/artifact repository from the local manuscript source tree.

## Manuscript wording

Use `model-based blinded evaluation`, `independent model-family evaluators`, and `descriptive agreement`. Do not call these outputs human/expert evaluation, semantic validity, factual/legal accuracy, or evaluator reliability. Do not combine partial checkpoints that used different protocols or token budgets. Lock Stage A only after each evaluator has a complete validated run; open Stage B only after that lock.

## Delivery snapshot

After manuscript edits:

1. rebuild from source;
2. check page count, references/cross-references, and visual rendering;
3. create a clean ZIP containing source, PDF, figure assets, and supplementary audit files;
4. test ZIP integrity;
5. calculate SHA-256 for PDF and ZIP;
6. save the snapshot under a stable deliverables directory;
7. send both PDF and ZIP with hashes and outstanding blockers.

A manuscript build passing does not establish venue compliance; keep venue requirements blocked until verified from the official CFP/submission source.
