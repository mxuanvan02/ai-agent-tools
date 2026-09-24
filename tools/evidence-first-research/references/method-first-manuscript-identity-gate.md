# Method-first manuscript identity gate

Use before delegating manuscript work, editing sections, compiling, or sending a PDF.

## 1. Freeze a paper-identity brief

Write these six fields from the user's latest instruction:

1. **Paper type and central contribution** — e.g., method-first paper, not dataset-release paper.
2. **Research problem** — the task the method solves.
3. **Object/testbed** — what role corpus, dataset, or system artifacts play.
4. **Method and comparison contract** — proposed method, permitted baselines/ablations, fixed model/evidence/budget constraints.
5. **Permitted claims and metrics** — only conclusions supported by completed, verified artifacts.
6. **Explicit exclusions** — e.g., human evaluation, unrelated models, historical runs, SOTA language, internal process prose.

The brief takes precedence over an inherited directory structure, pre-existing title, abstract, section order, or a prior paper draft.

## 2. Match manuscript architecture to the identity

For a method-first paper, use this logical order:

1. problem and contribution;
2. task/formal setting and data as testbed;
3. proposed method and components;
4. experiment design and matched baselines/ablations;
5. computational metrics and formulas;
6. evidence-bounded results and limitations.

Do not frame the method as an “auxiliary study” inside a dataset-centered paper. A corpus may be described as the source/testbed, but dataset lineage, release audit, and construction logistics must not displace the method, its components, or its evaluation logic.

## 3. Gate every delegation

Give every writing sub-agent a self-contained brief containing:

- the six identity fields above;
- exact canonical working tree and allowed files;
- confirmed artifacts and which results are still pending;
- forbidden framing/claims;
- requirement to make a minimal diff and return exact paths.

State that it must not infer study purpose from a legacy manuscript or add unverified results. Treat its summary as unverified until the parent reads back edited files and runs the relevant checks.

## 4. Pre-send check

Before sending a PDF or calling it a manuscript draft, verify title, abstract, introduction, methodology, experiments, and conclusion all answer the same central problem. Confirm the PDF path is canonical and the document contains no prohibited legacy framing. If identity is mismatched, stop; state the affected files/artifact and correct the structure before further editing.

## Session lesson

In the ECM–TQAG work, an inherited dataset-release manuscript was mistakenly revised as dataset-centered and described ECM–TQAG as an auxiliary computational study, despite the user requiring a method-first paper. The prevention is to freeze the identity brief and apply the architecture gate before any worker is dispatched or PDF is sent.
