# Journal Template Conversion And Venue Compliance

Use this when người dùng asks to move a manuscript into a target journal template or asks for section/topic/submit links.

## Link and scope verification

- Do not send guessed venue URLs. Open each URL first and verify it is not a 404/error page.
- For journal/topic/section advice, distinguish official sections/topics from your inferred keywords or positioning phrases.
- If a journal has no relevant official section, say so plainly and recommend Regular Article / no section rather than forcing a weak section.
- For trusted-journal-list filtering, extract the uploaded DOCX/PDF list and verify the exact journal title, ISSN/E-ISSN, and list index before recommending.

## Template conversion workflow

1. Open the target journal author guide and template page first.
2. Record durable requirements that affect the manuscript: class/template, article type, page limits, graphical abstract, supplementary files, data/code statements, author metadata, funding/conflict statements.
3. Create a clean target directory under `SAS/Research/<project>_<journal>`, copy only necessary source, figures, BibTeX, and generated artifacts.
4. Convert to the official or venue-accepted template; if the exact official class is unavailable, state the fallback clearly and do not claim official conversion.
5. Preserve author/corresponding/equal-contribution metadata from người dùng's preferred author block.
6. Build from scratch and parse logs for LaTeX errors, undefined citations/references, and overfull hboxes.
7. If venue requires a separate graphical abstract, create and build a separate upload artifact.
8. Package a zip and verify by unzipping into `/tmp` and rebuilding from the packaged source.

## IEEE Sensors Journal notes from bài probe-transmit session

- IEEE Sensors Journal author guide says submitted manuscripts should use IEEE double-column style template; `IEEEtran` journal mode is the practical LaTeX template route.
- It states manuscripts normally should not exceed 8 pages; if the converted draft remains longer, report the page count and warn about overlength handling/charges instead of silently calling it fully compliant.
- It states a graphical abstract is mandatory; include a separate `graphical_abstract.tex`/`.pdf` upload artifact.
- Use IEEE-style structure: title, authors/affiliations, abstract, IEEE keywords, numbered sections, appendix, data/code availability if appropriate, IEEEtran bibliography.
