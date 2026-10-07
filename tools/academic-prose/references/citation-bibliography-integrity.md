# Citation–Bibliography Integrity

Measured on a Vietnamese LaTeX manuscript (XeLaTeX + `polyglossia`, `article` class) at a late revision round.

## Failure observed
4 prose gates clean (internal_register 349 sents, process_logic 334, vi_ai 311, academic_discourse 69 paras) yet manuscript had **15 bracket-citation groups** (`[1–5]`, `[6,7]`, `[8,9]`, `[1]..[22]`) and **no §6 Tài liệu tham khảo / References** section. LibreOffice PDF 9 pages rendered without bibliography — submission blocker missed by prose scans.

## Why scans miss it
- `internal_register_scan`, `process_logic_scan`, `vi_ai_pattern_scan`, `academic_discourse_scan` check register/logic/style, not citation resolution.
- `has_TLTK` / `has References` flag must be checked separately.

## Recipe (use docx_accepted_text.py)
1. Dump accepted text: `python3 ~/.hermes/skills/academic-prose/scripts/docx_accepted_text.py --dump <docx> | head -n 200`
2. Extract citations: regex `\[\d+[–\-\d,]*\]` over accepted text; collect unique groups, count total.
3. Check bibliography: search accepted text for headings `Tài liệu tham khảo` / `References` / `Bibliography` (tab-prefixed `\t6\t` form in this template). `has_TLTK == False` is blocker if `cites_total > 0`.
4. Verify coverage: max cited number (here 22) vs entries present. Report `cites_total`, `has_TLTK`, `max_cite`.
5. Office smoke: `libreoffice --headless --convert-to pdf` then `zip_test None` + `paras/tables/media` counts to confirm not corrupt.

## Fix policy
- Never invent bibliography entries to satisfy count. Gate is `submission-integrity` → placeholder or author source required.
- Options offered to author: (a) provide `.bib` / list to insert, (b) insert placeholder `6. Tài liệu tham khảo — [CẦN BỔ SUNG]` with `[n] — cần bổ sung` lines to keep citations resolvable.
- Re-run smoke + cross-copy check after insertion.

## Pitfall to embed
A "clean 4-gate" report is not submission-ready. Always run citation-bibliography check as gate 5 before claiming ready-to-submit, especially for DOCX manuscripts with numeric bracket citations.

## LaTeX variant — the heading can render broken while the source looks fine
Measured on a Vietnamese XeLaTeX build (`polyglossia`, vietnamese default, `article` class): all 17 `\bibitem`s present, citations [1]–[17] resolved, zero build warnings — yet `pdftotext` showed the bibliography heading truncated to `Tài liệu` immediately followed by `[1] Kembhavi…`. The rendered artifact, not the source, carried the defect; both prose scans and a source grep passed.

Rules:
1. Verify the bibliography heading on **pdftotext of the built PDF**, not by grepping the `.tex`: search for the full string `Tài liệu tham khảo` (or `References`) and confirm the first `[1]` entry does not directly abut a partial heading.
2. Fix for `article`: `\renewcommand{\refname}{Tài liệu tham khảo}` immediately before `\begin{thebibliography}`. (`\bibname` applies to `book`/`report` classes.)
3. Rebuild twice, then re-verify heading text **and** full citation range `[1..N]` in the rendered text before calling the build final.

## Prose gates cannot catch a reversed finding — audit claims, not register
Measured on a Vietnamese master's essay: all four prose gates returned clean or licensed-only, yet the draft reversed an empirical result, mischaracterized a legal instrument, and cited a statutory number that had never been verified.

Rules, in the order that catches the most:
1. **Direction of a comparison must come from the paper's own table, never from memory.** Mockus/Fielding/Herbsleb (TOSEM 2002, Table III) reports Apache post-release defect density of 2.64 per KLOCA against 0.1–0.7 for four commercial projects — *worse*, not better — while the pre-system-test figure is 2.64 against 5.7–6.9, i.e. *better*. A result that cuts both ways is the signal you have a real finding; a one-directional paraphrase of a two-directional study is the classic reversal. Fetch the PDF and read the table before writing the sentence.
2. **Name the subject of a legal obligation from the article text, not from the headline.** Regulation (EU) 2024/2847 Art. 3(14) defines the `open-source software steward` as a *legal person* (foundations such as ASF, LF), Art. 2(2) excludes individuals contributing source code outside commercial activity, and Art. 64(10)(b) exempts stewards from administrative fines. "The burden falls on unpaid individuals" is the opposite of what the text says.
3. **Never write a statutory instrument number from memory.** Verify the circular/regulation on an official gazette (Vietnam: `congbao.chinhphu.vn`) and record signer, promulgation date, effective date, gazette issue. Mirror the same rule for CVE IDs (query the NVD API) and DOIs (query Crossref) — a DOI that 404s at Crossref is a fabricated venue or volume.
4. **Delete unsourced superlatives and round quantities.** `hàng triệu ứng dụng`, `phần lớn máy chủ Internet`, `được sử dụng rộng rãi nhất thế giới` read as evidence but carry none. Either attach a citable measurement or recast to the verifiable component list.
5. **Check the bibliography in both directions after every edit round.** Replacing a citation key in prose orphans the bib entry and breaks the other way too; diff `\cite{}` keys against `@type{key}` entries and require both `CITED-NOT-DEFINED` and `DEFINED-NOT-CITED` to be empty.
6. **A lexical gate hit can be a collision — adjudicate, don't blindly rewrite.** `đã biên dịch sẵn` (a prebuilt object file) trips `verification_log_prose`, whose pattern targets first-person process narration. Apply the three tests (admissible semantic subject, work-continues, re-typesetting); if the subject is a world entity and the reader can verify it from the cited source, the verdict is `license` — recast only when an equally exact wording removes the collision without distorting the technical meaning.
7. **Table captions are a licensed exception to the no-colon rule.** `Bảng 1: Tên bảng` is the Vietnamese house convention and appears in the author's own approved theses; `vi_ai_pattern_scan` flags caption colons as candidates by design. Adjudicate them as licensed rather than rewriting.

## Recitals explain, articles bind — never cite a preamble as an obligation
Measured on a Vietnamese master's essay: the draft said the EU Cyber Resilience Act "does not apply to individuals contributing source code", phrased as a binding rule. That sentence lives in **Recital 18**, a non-binding preamble. Article 2 (Scope) contains no such exclusion; the operative threshold is **Article 3(22)**, which defines `making available on the market` as supply `in the course of a commercial activity, whether in return for payment or free of charge`.

Rules:
1. Before attributing any obligation or exclusion to a regulation, locate the sentence and record whether it sits in a **Recital** (numbered `(n)` in the preamble) or an **Article** (binding). Fetch the full text — EUR-Lex HTML is often truncated or JS-gated, so pull it through the Wayback snapshot and grep the plain text.
2. Verify by grepping the article text, not by trusting a summary blog. Blogs routinely state Article numbers that do not exist in the adopted text (one source cited "Article 8" for steward obligations; the adopted text has **Article 24**).
3. Do not put named examples next to a quoted definition unless the instrument itself names them. Grepping the CRA full text for `Apache`, `Linux Foundation`, `Eclipse`, `Python Software Foundation` returned **zero** hits; the regulation only says "certain foundations". Naming ASF/LF right after quoting Art. 3(14) implies the text names them.
4. Cite EU provisions in the form the instrument uses — `Điểm b khoản 10 Điều 64` for Art. 64(10)(b), `Điểm 14 Điều 3` for Art. 3(14). Writing `Điều 3 khoản 14` reverses the hierarchy.

## Verify byline and date from the page, not from memory
The essay credited LWN article 967192 ("How the XZ backdoor works") to Jonathan Corbet. The page's own `FeatureByline` div says **Daroc Alden, April 2, 2024**. Corbet appears zero times. Any web citation must have author and date read off the fetched page; `grep -o 'FeatureByline">(.\{0,160\}\?)</div>'` is enough.

A `curl` HTTP 403/405 does **not** prove a URL is dead. `opensource.org/osd` returned 403 to bare curl but 200 to a browser User-Agent; `arstechnica.com` returns 405/403 to any curl but is live and archived. Test with a browser UA and with the Wayback availability API before reporting a broken reference.

## A reviewer subagent writes its findings into the session DB, not into your file
An independent reviewer was told to append findings to `FINDINGS.md` after each part. It wrote the header once, then stopped updating the file for 40+ minutes while continuing to work — the file looked stale and the run looked hung. The real work product was in `~/.hermes-racer/state.db`, table `messages`, keyed by `session_id`; its tool results contained the verified evidence (CRA article text, Công báo PDF of Thông tư 20/2014, LWN byline, NVD CWE data).

Rules:
1. Before concluding a long reviewer run is stuck, read `state.db` messages for its session — do not judge progress from the mtime of the file it was asked to maintain.
2. `assistant` rows can have empty `content` while `tool` rows carry all the substance; extract tool results too, filtered by keywords from the task.
3. An instruction to "write findings to a file after each part" is not self-enforcing. If the deliverable is the report, require the reviewer to emit it in its final message as well, and treat the file as a bonus.
4. Stop the run when the evidence gathered already covers the brief; a reviewer at 100+ minutes emitting no new claims is spending tokens, not finding defects.

## Pointer in SKILL.md
Section "Evidence-Bound Revision" item 6 now references this file.
