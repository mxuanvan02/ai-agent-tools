# Public artifact reproducibility: claim, README, and input--output contract

Use this note when a manuscript claims that a GitHub artifact is reproducible.

## 1. Distinguish four levels

1. **Build reproducibility:** source builds the manuscript/software.
2. **Artifact validation:** schemas, hashes, decoding, package identity, and portability checks rerun.
3. **Request reconstruction:** sanitized inputs deterministically produce provider request payloads and immutable receipts, often via `--dry-run`.
4. **Response reproduction:** the same model responses are regenerated.

Never collapse levels 2--3 into level 4. A proprietary/version-drifting hosted model, missing request environment, or withheld source-derived assets means exact response reproduction is not established.

Preferred wording:

> The release reproduces package validation and request construction on sanitized fixtures, not the original hosted-model responses.

## 2. State the executable input--output contract

For every advertised command, document:

- working directory and prerequisites;
- exact command;
- input path, file count, schema, and whether pixels are embedded or external;
- outputs written and where;
- expected PASS summary/counts;
- whether the command calls a network service or requires credentials;
- what the output proves and explicitly does not prove.

Example contract for a six-cell package diagnostic:

- input: two candidates times three evidence conditions;
- validation output: schema/hash/decode/package-count report;
- dry-run output: six constructed requests, per-cell receipts, condition JSONL, and run summary;
- clean-room output: zero host-path dependencies, expected decoded-pixel count, expected request/receipt count;
- non-claim: no correctness, sufficiency, or exact hosted-response reproduction.

## 3. README completeness gate

A README that only shows how to build the PDF is not a reproducibility guide even if runnable scripts exist. Before calling the release reproducible, ensure the README includes:

1. package validator command;
2. request-builder `--dry-run` command;
3. isolated/clean-room test command;
4. expected outputs and PASS counts;
5. optional provider-backed command separately labeled;
6. credential and network requirements;
7. limitations caused by withheld assets or provider drift.

Read the CLI parser or run `--help` before documenting flags. Do not infer package paths from a manifest alone.

## 4. Evidence sources

Inspect all of:

- root README;
- per-example READMEs;
- runtime scripts and argument parser;
- package schema/fixtures;
- release manifest and checksums;
- generated predictions, summaries, and receipts;
- rights/limitations statement.

A manifest proves file inventory and hashes, not that the README explains how to run the files.

## 5. Mutation boundary

If the user asks for explanation only (for example, “giải thích thôi”), inspect and report but do not edit the manuscript, README, repository, figures, or ZIP. Offer replacement prose separately or wait for explicit permission to patch.

## 6. Concise manuscript pattern

Keep limitations focused on: sample/evaluation boundary, provisional semantic judgments, public/private artifact boundary, and exact reproducibility boundary. Avoid inventories that duplicate the README.

A compact pattern is:

> The diagnostic is descriptive and does not support statistical or modality-necessity claims. Semantic outputs remain unadjudicated. The public release reruns validation and request construction on sanitized fixtures, but withheld source-derived assets and a hosted model prevent exact reproduction of the original responses.
