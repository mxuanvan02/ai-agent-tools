# bài TQA-generation manuscript review: durable lessons

## Project identity before any manuscript action
- A conversation can contain several papers and paths. Before reading, editing, building, sending, or submitting, ask/verify the exact title plus source artifact/repository.
- Treat a prior compacted summary, a nearby LaTeX project, and a previously built PDF as candidates only. Never infer the active manuscript from them.
- For a ZIP submission package, inventory it and verify source/PDF checksums before edits. Work in a separate audit directory; preserve the supplied archive unchanged.

## Evidence-bounded protocol/artifact papers
- Classify the paper before review: method/protocol, artifact, or efficacy/benchmark. Do not let a protocol paper borrow the rhetoric or figures of an efficacy paper.
- A test that schemas, hashes, reconstruction, or package binding work demonstrates implementation-contract behavior only. It does not demonstrate semantic correctness, grounding, necessity of pixels, question quality, or comparative utility.
- If outputs, retained-run numbers, inaccessible source-derived examples, or internal receipts cannot be independently audited, remove them from the manuscript rather than retaining them with disclaimers.
- Do not retain a figure/table whose visual message conflicts with a disclaimer in the prose. A six-cell diagnostic output table is still perceived as an experiment even if its caption says it is not.
- Put scientific limits in `Limitations`; put the source-code URL alone in `Code Availability`. Do not use limitations as an artifact inventory or a defence of omitted data.

## Final package gate
- Build after each substantive cut, then search source for obsolete terminology, figures, references, and claims.
- Repackage from an allow-list of files actually used by the manuscript. Do not carry removed figures, logs, cached PDFs, receipts, or “just in case” files.
- Verify: LaTeX errors, undefined citations/references, overfull boxes, PDF page boundaries, ZIP integrity, and checksums for every packaged file.
- Never say “ready to submit” merely because a PDF builds. State the paper class and any evidence limits plainly.
