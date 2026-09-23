# bài TQA-generation and Telegram Communication Addendum

## Telegram format

- Reply in Vietnamese by default and address the user as người dùng.
- For Telegram messages, render mathematical notation as readable rich text rather than raw LaTeX: use Unicode symbols and superscript/subscript characters, with Telegram-compatible Markdown/HTML where helpful.
- Send raw LaTeX only when the user explicitly requests source code.
- When explaining a manuscript, state the scientific role first, then introduce notation; do not let formulas obscure the method's meaning.

## bài TQA-generation method interpretation

- Separate the construction layer from the evidence-packaging/evaluation layer.
- The construction layer creates **one** TQA item from aligned evidence, derives the answer and provenance, and freezes them before question realization.
- T/TL/TLV are not three independent inputs that generate three questions. They are matched evidence conditions for the same item: T = text, TL = text + layout, TLV = text + layout + visual.
- Keep item identity, question, choices, answer, rationale, and provenance fixed across the matched packages; only the evidence/modality exposed to the downstream evaluator or answering model changes.
- Do not infer modality necessity from package existence or structural PASS. A modality-necessity claim requires a separate controlled answering or human evaluation.
- In experiment review, distinguish construction consistency, model-family evaluator agreement, baseline/SOTA comparison, ablation, and modality-necessity evaluation. GPT/Claude evaluator agreement is not a baseline comparison.
