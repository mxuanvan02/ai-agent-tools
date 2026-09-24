# Conference-review-to-revision workflow

Use this reference when reviewing a manuscript as a conference reviewer and the user expects the review to continue into an actionable revision plan.

## Core sequence

1. **Read the complete evidence set**
   - Manuscript source/PDF, figures and captions.
   - README, artifact/reproducibility notes, acceptance matrices, and experiment outputs when available.
   - Distinguish manuscript claims from private readiness notes and future-work plans.

2. **Reconstruct the paper before judging it**
   - Problem and intended contribution.
   - Method pipeline and formal objects.
   - What was actually implemented.
   - What was actually measured.
   - Explicit non-claims and limitations.

3. **Review from multiple independent perspectives**
   - Method/novelty reviewer: validity, circularity, relation to prior work, technical guarantees.
   - Experimental reviewer: sampling, labels, baselines, ablations, metrics, uncertainty, reproducibility.
   - Positioning/presentation reviewer: title, contribution type, claim–evidence fit, venue/track fit, terminology.

4. **Produce a meta-review**
   - Separate strengths from decision-dominating weaknesses.
   - State the likely verdict and confidence.
   - Identify which weaknesses are fatal for the target track versus repairable by prose.
   - Do not treat cautious disclaimers as a substitute for validation.

5. **Continue into revision, not merely criticism**
   - P0: changes required before submission.
   - P1: changes that materially improve acceptance odds.
   - P2: ideal extended evaluation.
   - Give concrete replacement text for title, abstract, contributions, experiment section, limitations, and conclusion when requested or useful.
   - End with a predicted verdict under at least two scenarios: framing-only revision and revision with new evidence.

## Claim–evidence ladder

Keep these levels distinct:

1. **Protocol specification:** the paper defines a sequence, representation, checks, or schema.
2. **Implementation evidence:** code executes, records validate, hashes bind, reconstruction passes.
3. **Descriptive diagnostic:** a fixed system produced specified outputs under specified conditions.
4. **Semantic validation:** independent evidence establishes correctness, grounding, or label accuracy.
5. **Comparative effectiveness:** baselines/ablations establish added value.
6. **Generalization:** sampling and uncertainty support broader conclusions.

Never promote evidence from one level to a higher level through wording alone.

## Small diagnostic studies

For output/no-output tables or a handful of examples:

- Treat them as implementation diagnostics or worked examples, not effectiveness evaluation.
- Output presence does not establish correctness, grounding, sufficiency, or modality necessity.
- Abstention can reflect model capability, prompting, calibration, representation, or policy.
- “First observed output” is not “minimum sufficient package.”
- A minimum viable empirical upgrade is usually:
  - a prespecified sample rather than hand-picked successes;
  - matched conditions on every candidate;
  - independent correctness/grounding/answerability labels;
  - agreement/adjudication;
  - one fair baseline;
  - one ablation targeting the central mechanism;
  - coverage plus valid yield and confidence intervals.

## Positioning when empirical evidence is limited

Prefer precise contribution nouns:

- `protocol` over `framework` when benefits are not validated;
- `recording provisional model-relative judgments` over `assigning labels`;
- `implementation diagnostic` over `evaluation`;
- `retention under the protocol` over `admission` or `certification`;
- `matched evidence-package withholding` over causal `ablation` when no causal intervention is established.

Keep limitations explicit but avoid repeating the same disclaimer in every section. Place the full boundary in the abstract, diagnostic/evaluation section, and limitations; elsewhere use stable terminology.

## Comprehensive revision execution gate

When the user authorizes a **comprehensive** revision, move from review prose to verified artifact edits in the same workflow:

1. **Inspect evidence availability before promising an empirical upgrade.** Search retained runs, public fixtures, annotations, baselines, ablations, prompts, and distributable source evidence. Classify each as real evaluation evidence, implementation-only evidence, or future-work material.
2. **Never manufacture the missing layer.** If only synthetic transport fixtures or a tiny retained diagnostic exist, do not invent sample counts, human labels, agreement, baselines, ablations, or effectiveness numbers. Improve positioning and explicitly report the empirical ceiling.
3. **Edit all claim-bearing sites together.** Propagate the new contribution type and terminology through title, abstract, keywords, introduction/contributions, section headings, figure captions, diagnostic/evaluation prose, limitations, and conclusion. Search for stale terms after editing.
4. **Prefer evidence-shaped terminology.** For example, use `protocol`, `implementation diagnostic`, and `provisional model-relative judgment` when the evidence supports specification and execution but not semantic validation.
5. **Build and verify before reporting success.** For LaTeX, require a clean multi-pass build and inspect page count, unresolved references/citations, overfull boxes, extracted PDF text, embedded fonts, and figure inclusion. Distinguish harmless typography warnings from submission blockers, and recommend the venue's official PDF checker when relevant.
6. **Report two verdicts.** State the reviewer verdict after the artifact-only revision and the likely verdict after the minimum viable empirical upgrade. This prevents prose improvements from being mistaken for scientific validation.
7. **Never return an empty response after tool calls.** Tool completion is not user delivery. Always synthesize what changed, verification evidence, remaining blockers, and exact artifact paths in the same turn.

## Interaction rule learned from review sessions

When the user says to proceed with the review/revision work, execute the next substantive stage in that turn. Do not stop after announcing what will be done next. If a long process is split, clearly mark completed work, current work, and the next deliverable; otherwise a premature conclusion reads as abandonment. After tools finish, always provide the promised synthesis rather than ending on raw tool output or an empty message.
