# Experiment comparison tables and Telegram reporting

## Give every table one role
Before retaining or writing an experimental table, state its role in one sentence.

- **Main comparative table:** compares ECM–TQAG against named, reproducible baselines under the same inputs, output format, evaluator/rubric, and aggregation rule. Its metrics must be defined for every compared method.
- **Protocol audit table:** verifies that a protocol emitted required fields or provenance records. It may report protocol-specific fields, but it cannot rank methods whose output contracts differ. Place it in an audit subsection or appendix, not as the main evidence that one method is better.
- **Ablation table:** varies one component while holding the rest fixed. Do not call prompt variants or different output schemas a component ablation unless the controlled design supports that interpretation.

## Baseline and SOTA gate
Do not call a method “SOTA” from a generic prompt, a hosted model, or an internal variant. To claim a comparative SOTA baseline, record: paper/repository, exact checkpoint/version, license, preprocessing, prompt or decoding settings, identical evidence packages, run ledger, and the shared evaluation protocol. If a published baseline cannot be run fairly on the task, state that it is unavailable and do not manufacture a comparison. Never upload protected textbook/figure material to an external service without explicit user approval.

## Explain a percentage in everyday Vietnamese
For every number, identify:
1. **Unit:** what one denominator item is (e.g., one chunk-generated MCQ), not “a criterion”.
2. **Denominator and numerator:** e.g., 5 of 8 items, hence 62.5%.
3. **Exact mechanical rule:** which fields are compared and whether it is exact-string, schema, or semantic/expert judgment.
4. **One genuine pass and one genuine non-pass record** from the ledger; do not invent examples.
5. **What it does not establish:** format/trace checks do not prove factual correctness, legal correctness, pedagogical quality, or modality benefit.

If a caption or column label differs from the code that generated it, fix the label and manuscript explanation before presenting the table. In particular, distinguish `answer` from a separately recorded `evidence_excerpt`; do not rename the latter as answer support.

## Telegram delivery for người dùng
Telegram updates are delivery notices, not manuscript sections. Send only 1–3 short lines: result/status, attached file or link, and one key validation fact. Use native rich text—HTML plus Telegram `parse_mode=HTML`—when the transport exposes it; use only supported tags such as `<b>`, `<code>`, and `<a>`. Do not call plain text or Markdown “rich text.” If the active send tool does not expose a formatting mode, keep the message short and honest about the limitation rather than pasting long Markdown tables or logs. Put detailed explanations in a file/PDF, or send them only when explicitly requested.

## Four-page manuscript compaction without weakening claims
When a conference page limit is binding, compress prose before removing methodological meaning or claim-linked citations.

1. Keep a compact distinction in **Measurements**: record audit (schema, exact-string, source-field checks) versus semantic/pedagogical quality (requires a shared blinded expert rubric).
2. Define each audit metric in one plain sentence: fields inspected, pass rule, and scope. Preserve special caveats: text/structure literal matching cannot validate image semantics.
3. Collapse repeated prose across Abstract, Results, Conclusion, and Limitations; retain the result once, then state its interpretation boundary once.
4. Restore citations only where each claim needs them. Before delivery, compile clean and check: page count is within limit; every cited key exists; every bibliography entry is cited; no undefined reference/citation remains.

Do not reduce a paper to fewer pages at the cost of relabelling an audit as a quality comparison or silently dropping citations that support retained claims.