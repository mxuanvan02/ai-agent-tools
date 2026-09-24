# Manuscript layout and concise scientific writing

Use for conference-paper revision, especially when the request is to "write/rewrite every section", standardize layout, or make a manuscript submission-ready.

## Narrative contract

Before drafting, state the one-line chain and make every section serve it:

**research problem → proposed method → experimental material/design → measurements → evidence-bounded findings → contribution.**

Do not let a paper drift into a dataset-release paper, a software-demo paper, or a diagnostic note when its agreed identity is different. Treat the user-supplied canonical manuscript/template as the source of truth, not a previously edited alternative tree.

## Section-by-section layout

- **Title:** method/task identity, not an internal project slogan.
- **Abstract:** one compact paragraph: problem, approach, evaluation setting, high-level findings, contribution. Do **not** enumerate detailed percentages, trial counts, model names, seeds, hashes, caveats, or table-level metrics unless the venue specifically requires them.
- **Introduction:** motivation and gap; exact research objective; high-level method; a short numbered/parallel contribution list. Avoid repeating results in detail.
- **Method:** define inputs, representation, algorithm/protocol, output contract, and deterministic validation. Each method module must have a corresponding experimental observable where possible.
- **Experimental evaluation:** corpus/provenance and input scale; model/configuration; baselines; design; measurements; results; brief interpretation. Put detailed numerical evidence in tables and Results, not in Abstract.
- **Results:** lead with the main result, point to the table, then interpret only what the measurements support. Protocol-specific fields are not a superiority comparison against methods that do not emit those fields.
- **Limitations:** state only substantive scientific gaps—e.g., generalizability, unmeasured semantic or pedagogical quality, and open validation needs. Do not put repository, source-code, availability, or procedural reproducibility details here, and do not turn it into defensive, repetitive negation.
- **Data/Code/Materials Availability:** keep reproducibility routes, repository links, access conditions, and material-sharing statements in this dedicated back-matter section.
- **Conclusion:** restate method, validated findings, and practical contribution; no new claims.
- **Back matter:** short, factual, conventionally named sections. Do not include placeholders in a near-submission PDF once the user has supplied final wording.

## User-specific style preferences

- Prefer direct, affirmative academic prose. State what exists and what the study establishes; do not add unsolicited defensive sentences such as “this does not prove X” merely to preempt a claim the user did not ask to make.
- Keep declarations terse and functional. For example, an AI-use statement should only say the user-authorized categories of assistance; do not add model names, responsibility boilerplate, or policy commentary unless explicitly requested.
- Do not make the Abstract a miniature results table. Keep detailed counts and percentages in the Experimental/Results sections.
- For source data, use the approved institutional description and the actual input scale only; do not mention an internal pipeline, another paper, release-wide totals, or unsupported provenance details.

## Tables, figures, and rendered layout

1. Place a table declaration before the Results prose that introduces it, normally immediately after Measurements or at the beginning of the parent Experimental section.
2. For IEEE two-column layouts, use `table*` for full-width tables and `[!t]` to request top-of-page placement.
3. Never duplicate a float while moving it. After any move, verify exactly one source block and one rendered occurrence.
4. Compile until references stabilize; inspect the rendered PDF or extracted page text to confirm the table/figure appears near its first discussion. A successful LaTeX exit code alone does not validate float placement.
5. Treat underfull-box warnings as presentation issues to review, but distinguish them from compilation/reference errors.

## Scientific contributions and notation discipline

- State contributions as transferable scientific advances, not as a list of implementation actions. For a method paper, distinguish: (1) the formalism/protocol introduced, (2) the representation or object it makes explicit, and (3) the evaluation formulation that makes its properties observable.
- Make each contribution correspond to a defined method object and an experimental observable. Do not describe a dataset, repository, or one experiment as the scientific contribution unless that is the paper's agreed identity.
- Establish one notation convention before editing equations. In particular, distinguish document components (e.g., \(T,L,V\)) from condition labels (e.g., \(\mathsf{T},\mathsf{TL},\mathsf{TLV}\)); distinguish source-level provenance mappings from item-level traces; and do not reuse a symbol for different semantic levels.
- For every reported metric, define the evaluation set, valid-response subset, index domain, indicator, and denominator. Apply the same symbols in Method, Measurements, table captions, Results, and figure labels.
- When explaining a manuscript to the user, provide a separate compact notation glossary with: symbol, meaning, and English reading. Do not add a notation table to the paper unless its template, audience, or mathematical density warrants one.

## Evidence discipline

- Use only experimental results whose ledger/artifacts are verified.
- Keep the final suite/model configuration consistent across Abstract, setup, captions, results, conclusion, and declarations.
- Do not introduce unavailable baselines, ablations, human studies, or causal claims just to make the paper look broader.
- Correctly label execution/contract compliance, trace availability, literal support, and fixed-item agreement as the measurements they are.

## Completion gate

Before saying the paper is complete: read the entire final source; check all section names and all numbers mentioned in prose against artifacts; compile; eliminate unresolved references; inspect PDF page count and float placement; then report only the final paths and material verification results.
