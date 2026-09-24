# Evidence-first multimodal TQA generation manuscript protocol

Use when the research contribution is **generation of genuinely multimodal TQA items**, not retrieval, online QA, or a generic multimodal encoder.

## 1. Scope lock and contamination gate

Before writing, state one sentence defining the paper owner and central empirical object. For a generation paper:

> The paper studies whether evidence-first construction produces grounded TQA items whose claimed layout/pixel modality is semantically necessary.

Create the lineage map before importing any result:

`claim/result -> run artifact -> dataset/corpus -> paper/project owner`.

If any link belongs to another paper, exclude it from the abstract, tables, discussion, conclusion, README, release package, and diagrams. Shared PDFs, workspace, topic, or authorship do not transfer result ownership. A text-retrieval diagnostic cannot stand in for a multimodal-generation experiment.

## 2. Method spine

Use one invariant throughout manuscript, figure, schema, and evaluation:

\[
G_m \rightarrow z \rightarrow A \rightarrow q \rightarrow \mathcal C,
\]

where:

- \(G_m\): typed evidence motif mined from a provenance-preserving cross-modal graph;
- \(z\): executable reasoning program;
- \(A=\{a_i\}\): answer atoms fixed by execution;
- \(q\): language realization conditioned on fixed atoms;
- \(\mathcal C\): counterfactual semantic-sufficiency audit.

Order is non-negotiable: evidence relation first, answer atoms second, wording last. Do not generate Q/A from OCR and attach a nearby figure afterward.

## 3. Formal core

Represent a document as

\[
D=(T,L,V,M,P),
\]

with text/OCR \(T\), layout \(L\), pixels/visual regions \(V\), metadata \(M\), and source provenance \(P\). Build

\[
G=(N,E,\rho),\qquad N=N_T\cup N_L\cup N_V\cup N_M,
\]

where the provenance map is explicit:

\[
\rho:N\cup E\rightarrow(h,p,r,v,c),
\]

and \(h,p,r,v,c\) denote PDF hash, one-based page, region, extractor version, and confidence. Define a motif and its induced graph without conflating them:

\[
m=(N_m,E_m,\tau),\qquad G_m=G[N_m,E_m].
\]

Use one output schema everywhere (paper, figure, README, and release):

\[
x=(q,a,A,z,\Gamma,\mu,\rho),\qquad a=\operatorname{Verbalize}(A),
\]

where \(\Gamma\) maps atoms to evidence regions and \(\mu\) is the minimum sufficient **evidence condition**. Require atom-level grounding:

\[
\forall a_i\in A:\quad \Gamma(a_i)\neq\varnothing\ \land\ \Gamma(a_i)\models a_i.
\]

Use the predefined nested evidence chain

\[
\mathcal X=\{X_T,X_{TL},X_{TLV}\},\quad
X_T=T,\ X_{TL}=T\cup L,\ X_{TLV}=T\cup L\cup V.
\]

Call this an experimental evidence chain, not the full modality power set. Operationalize semantic sufficiency under a written annotation protocol \(\mathcal H\):

\[
\operatorname{Suff}_{\mathcal H}(X,A)=\prod_i\mathbb I[X\models_{\mathcal H}a_i].
\]

A reviewer may use only the visible package, explicit relations, and ordinary linguistic knowledge—not external legal knowledge, filenames, hidden metadata, or a previously seen richer package. Randomize package order and blind reviewers to richer conditions.

For each atom,

\[
\mu_i=\min_{\preceq}\{X\in\mathcal X:\operatorname{Suff}_{\mathcal H}(X,\{a_i\})=1\},
\qquad \mu(x)=\bigvee_i\mu_i,
\]

where \(\vee\) is the least upper bound on \(T\preceq TL\preceq TLV\). Thus \(T\) is text-recoverable control, \(TL\) layout-dependent, and \(TLV\) pixel-dependent beyond text+layout. If Full is insufficient, reject or explicitly label unanswerable/invalid.

## 4. Generation stages

1. **Register source:** PDF hash, source family, one-based PDF page, license status, parser/OCR versions.
2. **Parse independently:** text spans, layout objects/relations, original pixels/crops. OCR is not visual evidence.
3. **Cross-modal linking:** typed nodes/edges with direction, confidence, polygon, and provenance.
4. **Mine motifs:** header-cell, label-value, checkbox state, parent-child/path, arrow direction, curve intersection, axis projection, diagram+prose, table+footnote, cross-region join.
5. **Instantiate program:** restricted operators such as `SELECT`, `FILTER`, `TRAVERSE`, `JOIN`, `COMPARE`, `READ_STATE`, `RETURN`.
6. **Execute before wording:** \(A=\mathrm{Exec}(z,G_m)\), \(\Gamma=\mathrm{Trace}(z,G_m)\). Reject empty, out-of-slice, or ungrounded executions.
7. **Controlled realization:** LLM may verbalize \(q\), but cannot change \(A,z,\Gamma\), invent evidence, expose hidden IDs, or leak the answer.
8. **Counterfactual audit:** review identical \((q,A)\) under \(T,TL,TLV\), plus caption-only leakage control. Never delete naturally available text merely to manufacture visual dependence.
9. **Independent annotation:** two reviewers lock decisions before comparison; a third adjudicates answerability, atom support, region, and minimum modality.

## 5. Acceptance and negative controls

Use explicit gates for source validity, executable program, grounding, linguistic validity, full-condition sufficiency, counterfactual necessity, and adjudication:

\[
\mathrm{Acc}(x)=\prod_j \mathbb I[C_j(x)=1].
\]

A page containing a chart/diagram is not a positive example by itself. If \(\mu=T\), retain it only as a **text-recoverable negative control**. Positive multimodal items require \(\mu=TL\) or \(TLV\) with localized evidence.

Lexical answer-token coverage is only a warning. The decisive leakage question is semantic: does text or caption already assert the queried relation?

## 6. Evaluation for a generation paper

Compare against:

- OCR -> LLM;
- page image -> VLM;
- OCR + image free generation;
- image -> caption -> LLM.

Ablate evidence graph, executable program, counterfactual filter, leakage audit, and human modality adjudication. Keep source pages and generation budget matched.

Primary metrics:

- **Yield:** accepted/generated;
- **GAR:** grounded atoms/all atoms;
- **MNP:** adjudicated true multimodal/claimed multimodal;
- **TLR:** text-solvable/claimed multimodal;
- **ERR:** resolvable document-page-region citations/all citations;
- **FAR:** full-answerable/accepted.

Downstream answering under fixed answerer/prompt on \(T,TL,TLV\) is only a validation instrument. Report gains separately on independently adjudicated \(TL\)- and \(TLV\)-dependent subsets.

### Pre-adjudication diagnostic discipline

If sources and frozen packages exist but human annotation is pending, run each item-condition pair in an independent request with one fixed answerer, model/settings, and prompt version; hide reference answers and prevent cross-condition memory. Preserve raw JSONL outputs and generate a machine-readable summary that reports completion, answerability, answer, evidence references, confidence, and exact-match behavior.

Treat this run as a **pipeline/failure-mode diagnostic**, never as semantic modality adjudication or effectiveness evidence. In particular:

- a correct text-only answer can be an unsupported guess from aggregates or priors;
- a model may return `answerable=true` while its rationale admits the evidence is insufficient;
- model failure or success cannot define \(\mu\);
- validator logic must accept a completed abstention (`answerable=false`, `answer=null`) and reject only incomplete/error rows or `answerable=true` without an answer;
- keep positive counts, GAR/MNP/TLR/ERR/FAR, agreement, and multimodal-gain claims blocked until two independent annotations are locked and adjudicated.

The manuscript may report only verified request counts and qualitative failure patterns, explicitly captioned as pre-adjudication diagnostics rather than effectiveness results.

## 7. Short-paper writing and figure rules

For a 2--4 page IEEE method paper:

- Focus only on multimodal TQA generation; keep online QA/RAG outside the contribution unless indispensable.
- Prefer equations and one architecture figure over prose duplication.
- Main figure should be two-column width and follow five large stages: `PARSE -> LINK -> PLAN/REALIZE -> VERIFY -> CLASSIFY/ADJUDICATE`.
- The visual narrative must expose `Evidence motif -> Program -> Answer atoms -> Question -> Counterfactual audit` at page scale.
- Use short box labels, large fonts, a single main spine, and isolated whitespace corridors for cross-stage, reject, and feedback edges.
- Pin every cross-stage connector to perimeter ports (`exitX/exitY`, `entryX/entryY`), add perimeter spacing, and use explicit orthogonal waypoints. Automatic center-to-center routing is not acceptable when it crosses a block or text.
- Prefer putting branch meaning inside destination blocks (`T-control`, `TL+`, `TLV+`, `reject`) rather than placing labels on connector lines. Edge labels that overlap lines or blocks are a hard failure.
- Show nested evidence conditions explicitly, e.g. \(X_T\subset X_{TL}\subset X_{TLV}\), then a decision for the minimum sufficient condition. Include all outcomes: text control, layout/pixel positive, Full-insufficient reject/unanswerable, and failed-adjudication feedback.
- Keep notation and output schema identical across manuscript, figure, README, and artifacts. Do not alternate between \(G=(N,E)\) and \(G=(N,E,P)\), between \(m\) and \(G_m\), or between output tuples.
- The acceptance expression must match the prose gates exactly.
- Define TQA at first use; narrow novelty explicitly (not a new encoder) and position against visual QG, grounded VQA, programmatic VQA, and counterfactual/prior-leakage work.
- Do not present prospective metrics as measured results. Never keep an effectiveness table filled with `--`; replace it with verified source-audit evidence or remove it until real results exist.
- If only provenance/source readiness exists, call the manuscript a method and evaluation design, not an empirical superiority paper. A `Results` section that only promises future results is weaker than an honest `Current Evidence / Claim Boundary` section.

### Production export gate for paper figures

- Prefer vector PDF/SVG only if font audit confirms no venue-problematic fonts. Draw.io math/Unicode glyphs can become Type 3 even when `math=0`; disabling math alone is not a sufficient fix.
- Audit the **final manuscript PDF** with `pdffonts`, not only the standalone figure. Require zero unembedded fonts; for strict IEEE/PDF eXpress workflows, require zero Type 3 fonts.
- If outlining text is unavailable and Draw.io PDF still contains Type 3, use a clean high-resolution PNG in the paper (about 2400 px full-width, roughly 300--350 dpi), while retaining editable `.drawio` and vector PDF as source artifacts.
- Export/rebuild until: correct page size/count and PDF version; zero undefined citations/references; zero overfull/underfull boxes; zero Type 3 and unembedded fonts; and no foreign-project metrics or empty-result placeholders.
- Build success does not prove arrow/text readability. Run deterministic geometry/routing checks and a successful final-size human/vision inspection when available; if vision fails technically, report deterministic PASS and visual status separately.

## 8. Artifact and QA gate

Before claiming a complete draft:

- back up the prior manuscript;
- search the main manuscript, captions, figure labels, README, and release notes for foreign corpus IDs/metrics;
- build until references settle;
- require no undefined references/citations, overfull boxes, or underfull boxes in the final log;
- verify page count, page size, PDF version, embedded fonts, Type 3 count, and rendered pages;
- keep editable Draw.io plus clean PNG/PDF exports;
- distinguish three statuses explicitly: **method-complete**, **source/provenance-verified**, and **experiment-complete**;
- never call the submission empirically ready without adjudicated positive \(TL/TLV\) items, baseline comparison, at least one load-bearing ablation, agreement, and matched \(T/TL/TLV\) evaluation;
- if vision audit fails technically, do not call it a visual pass: use deterministic geometry/log/text extraction and report vision status separately.

Placeholders for authors, affiliations, annotations, model runs, rights, and empirical results remain explicit blockers to camera-ready or experiment-complete status. Do not pad a page limit with unsupported prose or fabricated/empty result tables; use formalization, operator semantics, pseudocode, positioning, and verified source-audit evidence only when they add real information.
