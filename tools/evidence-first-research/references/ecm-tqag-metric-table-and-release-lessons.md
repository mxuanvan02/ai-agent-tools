# ECM–TQAG manuscript, metric-table, and release lessons

Use this reference when revising an evidence-first TQA manuscript, interpreting a computational table, or preparing the associated public release.

## 1. Narrative and scientific layout

- Write **contributions as methodological objects**. Each contribution must be developed by a corresponding Methodology subsection; evaluation design or execution logistics is evidence for the contribution, not a contribution itself.
- Preserve one role per section: Abstract = problem/method/evaluation/significance; Introduction = gap and contributions; Method = formal objects and procedure; Experimental = design, measurements, results; Limitations = research gaps; Availability = code/materials/rights; Conclusion = synthesis without new claims.
- Keep the Abstract brief and qualitative unless a result number is indispensable. Do not repeat table values in Abstract, Results, and Conclusion.
- Remove implementation-like manuscript prose: provider/model names, temperatures, random seeds, API details, prompt-run logistics, and ledger implementation detail. Describe the scientific design (paired conditions, protocols, frozen-question comparison) instead.
- Declarations should be one short, functional statement each. AI disclosure should only state the agreed high-level uses (e.g., grammar editing, code development, figure preparation), not model/provider details.

## 2. Notation and terminology gate

Before editing equations or captions, make a notation map and keep it stable:

- $T,L,V,M,\Pi$: document components (text, layout/structure, visual content, metadata, source-level provenance).
- $\mathsf{T},\mathsf{TL},\mathsf{TLV}$: evidence-condition labels; visually distinguish these from the components.
- $\rho$: graph-node to source-provenance mapping; $\Gamma$: item-level trace. Never collapse these meanings.
- Explain any displayed equation in prose, including symbol meaning and scope.

## 3. Citation audit

Citations must be **claim-local**, not merely a long bibliography. Map each claim family to the source that supports it, for example: document AI/VQA, educational question generation, structured reasoning, provenance, MCQ item-writing, reproducibility/auditability, and visual-dependence diagnostics.

Before delivery:
1. Compile from a clean state.
2. Verify no undefined citation/reference warning remains.
3. Compare cited keys with BibTeX keys: no missing and no unused entries, unless intentionally retained by venue policy.
4. Check that citations support the exact surrounding claim; do not cite structural validation as evidence of factual correctness, pedagogical quality, semantic grounding, or modality benefit.

## 4. Metrics-table truth gate

Never infer a metric definition from its label. Read the exact analysis rule that produced it and use its field names in the table caption and Methods.

For a cell with $n$ items, report the denominator and calculate each rate from the actual Boolean or fractional per-item values:

- **Contract validity:** count records that re-parse and match the protocol contract.
- **Answer-choice exact:** compare `answer` with `choices[answer_index]` by the analyzer's exact rule. Semantic similarity does not count unless the analyzer says so.
- **Evidence-excerpt literal match:** if the analyzer checks `evidence_excerpt` against source text, label it exactly this way. Do not call it answer support.
- **Trace source available:** source labels must correspond to evidence actually exposed by the package.
- **All-trace literal match:** item score is 1 only if every trace-support string matches its relevant text/structure source by the analyzer's rule.
- **Mean trace literal-match rate:** compute a fraction within each item first, then average those fractions across items; it is not necessarily an all-trace item rate.

When explaining a table to a reader, show one actual pass and one actual fail, state the numerator/denominator (e.g., $5/8$), explain why the values differ, and state what the metric cannot establish. `--` means *not applicable because the protocol does not expose that field*, not zero.

For image traces, a source may be available while a text-literal matcher returns false because it cannot semantically verify pixels. Never describe this as evidence that the visual trace is wrong.

## 5. Source-package and public-repository boundary

### Clean LaTeX package

Package only the files necessary to compile: source `.tex`, bibliography, actually referenced figures, and a concise build README. Exclude build products, unused assets, logs, internal ledgers, source-derived restricted content, credentials, and generated clutter. Extract the ZIP into an empty directory and compile there before sending it.

### Research-software release

The README must state: research scope, methodological artifacts/contracts, installation, offline reproduction, command semantics, data governance, limitations of structural checks, citation, and license.

Public tracked files must not contain real API keys, tokens, endpoints, provider-specific operational URLs, or concrete model identifiers. Remote execution must be opt-in through an ignored local config copied from a non-routable placeholder template (for example, `.invalid` endpoint, `MODEL_NAME_PLACEHOLDER`, and an environment-variable name only). Add ignore rules for `.env` and local/private configs; audit the tracked tree and test/build before publishing.

## 6. Validation and communication

After manuscript changes: compile, scan for unresolved references/citations, inspect table placement/rendering, and repackage if source changed. After repository changes: run focused tests, reproducibility commands, release-boundary scan, build package, inspect git diff, and only then publish.

When reporting results, lead with what changed and the evidence. State limitations candidly. Do not claim semantic correctness, legal accuracy, question quality, or a causal modality advantage without a matching validated measure.