# Manuscript review: project identity, section roles, and evidence boundaries

Use this note for manuscript review/revision, especially protocol or artifact papers.

## 1. Project identity gate

Before any read, edit, build, package, send, or submission action:

1. Confirm the exact manuscript title, repository or source directory, and target PDF/package.
2. Treat that identity as the mutation boundary for the whole task.
3. Do not switch to a similarly named paper or a project mentioned only in compressed context.
4. If identity/path does not match, stop to locate it; do not edit a guessed substitute.

## 2. Assign a role to every section

Read the entire source and classify paragraphs before cutting claims:

| Section | Proper job |
|---|---|
| Abstract/Introduction | problem, protocol contribution, bounded scope |
| Method/Protocol | how records are produced, linked, checked |
| Walkthrough | source → structure → answer/trace → question → evidence packages; explanatory only |
| Validation scenarios | executable checks, with what each proves and does not prove |
| Evaluation | quality/effectiveness claims only when supported by released/rights-cleared data and evaluation design |
| Limitations | missing scientific evidence and scope limits only |
| Code Availability | code URL and scope of released artifact only |

Do not place repository URLs, release logistics, runtime receipts, or lengthy redistribution explanations inside Limitations unless a venue explicitly requires them there.

## 3. Protocol/artifact evidence rule

Do not turn an internal pilot or a synthetic transport check into semantic evidence.

- If source-derived outputs cannot be independently audited or released, remove numerical/qualitative performance claims based on them.
- Do **not** erase all explanatory material: retain or create a walkthrough that makes the protocol legible.
- A synthetic fixture can establish that a contract is exercised; it cannot establish textbook-question quality, source grounding, modality necessity, or model improvement.
- Separate deterministic checks (schema, receipt/hash, identity, dimensions, reconstruction) from model-relative semantic judgments.

## 4. Describe tests only after reading their bodies

README and test names are leads, not evidence. Read the assertions and report exactly:

- subject modified or validated;
- expected failure/pass condition;
- whether a test compares repeated executions or only runs once;
- whether a hash covers a package, response record, configuration, or another object.

Never infer terms such as “deterministic,” “tamper-proof,” “repeatable,” or “payload integrity” merely from a test name.

For a paper, group test facts into meaningful scenarios, e.g.:
1. valid matched packages;
2. malformed/mismatched/altered records rejected;
3. offline validation and verification boundary;
4. explicit boundary to external services.

For every scenario, state: **what it checks** and **what it does not establish**.

## 5. Change and verification gate

1. Back up all altered source files and write SHA-256 checksums.
2. Make the smallest edit consistent with section roles.
3. Build the PDF.
4. Check build log: errors, undefined citations/references, overfull boxes.
5. Render/inspect affected pages, including figures, captions, URLs, and bibliography.
6. Inspect the final ZIP manifest: remove files no longer referenced by manuscript/source; regenerate checksum list.
7. Before sending or submitting, state PASS/BLOCKED with actual evidence, and do not claim a tool action/result before it has occurred.

## 6. Layout is a real acceptance gate

A successful LaTeX build is insufficient. Inspect two-column flow, long URLs, reference balancing, page-end whitespace, figure/caption placement, and whether source layout hacks actually improve the rendered PDF. Compare renderings instead of relying on intuition.
