# Journal Q1 Selection Notes

Use this reference when người dùng asks for journal targeting, especially when the requirement is both fit and Q1 category.

## Workflow

1. Clarify which ranking source the institution requires: Scopus/SCImago SJR quartile, Clarivate/JCR quartile, or an institution/NAFOSTED approved journal list. Do not treat them as interchangeable.
2. Check the journal's current subject categories, not only its `Best Quartile`. A journal can be Q1 overall while the category closest to the manuscript is Q2.
3. If người dùng provides an official approved-journal document, extract/search the document before recommending. A journal that is Q1 elsewhere may still be unusable if it is absent from that list.
4. Rank venues by: approved-list presence -> category fit -> quartile in that category -> review/publication speed -> prestige/risk -> APC/fit constraints.
5. For fast-publication claims, prefer official journal pages over third-party ranking pages.
6. Before sending a topic/section/submission link, open it or otherwise verify the exact slug; if a checked link 404s, say so and replace it with a working page.
7. Report the recommendation as a shortlist with a clear first choice and backup path, not a long undifferentiated list.
8. Do not invent official `topics`, `sections`, or `special issues` from manuscript keywords. First check the journal submission/site taxonomy; if a journal only has broad scope plus keywords/classifications, say so explicitly and label suggested terms as `keywords/positioning`, not official topics.
9. When giving section/topic links, verify the exact URL slug. For MDPI Sensors, the Sensor Networks section slug observed in June 2026 was `sensornetworks`, not `Sensor_Networks`.

## bài probe-transmit / IoT Scheduling Precedent

For a manuscript like bài probe-transmit / bài AoI-greenhouse (pull-based IoT sensing, threshold-aware scheduling, safety-critical sensor monitoring):

- `Internet of Things (Elsevier / Netherlands)`: strongest Q1 category fit in Scopus-style sources. Relevant Q1 categories include Artificial Intelligence, Computer Science Applications, Computer Science (miscellaneous), Engineering (miscellaneous), Hardware and Architecture, Information Systems, Management of Technology and Innovation, and Software. Good first choice when the goal is Q1 + topic fit.
- `IEEE Sensors Journal`: Q1 in Electrical and Electronic Engineering and Instrumentation. Good IEEE/sensor route, but frame the paper as wireless sensor-network scheduling, pull-based sensing, and safety-critical sensor monitoring rather than generic IoT algorithms.
- `IEEE Access`: Q1 in broad categories such as Computer Science (miscellaneous) and Engineering (miscellaneous) in checked sources; official IEEE Access page states a 4--6 week submission-to-publication target. Good fast Q1 backup but less targeted/prestigious than domain journals.
- `Sensors (MDPI)`: `Best Quartile` Q1, with Q1 categories such as Instrumentation, but categories closer to IoT algorithms (e.g., Electrical and Electronic Engineering, Information Systems) may be Q2. Fast option, but be explicit about category mismatch if the institution requires the closest category to be Q1.
- `IEEE Internet of Things Journal`: very strong Q1 fit and prestige, but not a fast route; expect higher novelty burden and slower review.

## NAFOSTED / QTUT 2025 Approved-List Precedent

When người dùng asks for journals "thuộc danh mục" and provides `Danh muc tap chi QTUT trong KHTNKT 2025.docx`, verify against that document before recommending. In the June 2026 bài probe-transmit session, the following entries were found in the list and fit IoT/sensor-network scheduling:

- `IEEE Sensors Journal` — TT 3159, ISSN `1530-437X`, E-ISSN `1558-1748`. Best practical replacement for MDPI Sensors when the paper is framed as sensor-network scheduling and safety-critical sensing.
- `IEEE Internet of Things Journal` — TT 3132, ISSN `2327-4662`. Highest-prestige IoT fit, but harder/slower.
- `Internet of Things` (Elsevier) — TT 3728, ISSN `2543-1536`, E-ISSN `2542-6605`. Good fit and less controversial than MDPI.
- `ACM Transactions on Sensor Networks` — TT 44, ISSN `1550-4859`, E-ISSN `1550-4867`. Very strong scope fit but high novelty burden.
- `Ad Hoc Networks` — TT 164, ISSN `1570-8705`, E-ISSN `1570-8713`. Good wireless/sensor-network scheduling fit.
- `Computer Networks` — TT 1786, ISSN `1389-1286`, E-ISSN `1872-7069`. Broader network-resource-allocation option.
- `IEEE Access` — TT 3107, ISSN `2169-3536`. Practical faster fallback that is in the list. Official home page verified in June 2026 at `https://ieeeaccess.ieee.org/`; it states quality/rapid peer review and a 4--6 week submission-to-publication target. Submit link observed on the site was `https://ieee.atyponrex.com/journal/ieee-access`. Use subject areas/keywords such as Internet of Things, Sensor Networks, Wireless Communications, Resource Allocation, and Edge Computing.

Topic/section pitfalls from the same session:
- `Internet of Things` (Elsevier) has a journal scope page and author keywords/classifications, but no official topic/section choice comparable to MDPI sections. Do not present inferred terms such as resource allocation, IoT communications, or sensor scheduling as official Elsevier topics; call them keywords/cover-letter positioning.
- `IEEE Access` has a verified Sections page at `https://ieeeaccess.ieee.org/sections/` and Society Sections at `https://ieeeaccess.ieee.org/sections/ieee-society-sections/`. Do not use the old `/about-ieee-access/scope/` path; it 404ed in June 2026. For bài probe-transmit, there is no exact IoT/Sensor Networks IEEE Access section among the 11 Society Sections. If forced to choose, `IEEE Systems, Man and Cybernetics Society Section` (`https://ieeeaccess.ieee.org/society-sections/ieee-systems-man-and-cybernetics-society-section/`) is the closest system/control/safety-monitoring fit; otherwise choose regular/non-section submission. `IEEE Vehicular Technology Society Section` is only a secondary option for mobile/wireless-radio framing. The Special Sections page (`https://ieeeaccess.ieee.org/sections/special-sections/`) said no Special Sections were open for submissions in June 2026.
- `Sensors` (MDPI, ISSN `1424-8220`) may be Q-indexed elsewhere, but it was not found in this approved-list extraction. Do not recommend it when the hard constraint is "must be in this list" unless re-verification finds the exact journal entry. If discussing MDPI Sensors anyway, the correct Sensor Networks section URL pattern is `https://www.mdpi.com/journal/sensors/sections/sensornetworks`.

## Getting journal data when search engines / Scimago block headless browsers

In the June 2026 bài AoI-greenhouse journal-selection session, `scimagojr.com` returned a Cloudflare
"Just a moment...", `sciencedirect.com` returned "There was a problem providing the content"
(bot block), and both `google.com/search` and `bing.com` redirected to a sorry/captcha
page from the headless browser. DuckDuckGo HTML (`html.duckduckgo.com/html/?q=`) returned
empty. Subagent literature scout (`delegate_task` toolsets `[web]`) exited "completed" with
0 API calls — it could not actually run tools. So do NOT rely on browser search or a web
subagent for this; go straight to the source with `curl`:

- **Official journal homepages carry the exact stats.** `curl -sL -A "<desktop UA>"` the
  journal's own site, strip tags, grep for the numbers. The IEEE IoTJ homepage
  (`https://ieee-iotj.org/`) exposed verbatim: `Submission-to-FirstDecision = 6.9 weeks
  (average)`, `Submission-to-ePublication = 14.5 weeks (average)`, `Impact Factor (JCR'24)
  8.2`, and a dedicated **Expanded Conference Papers** track page
  (`/expanded-conference-papers/`) — IoTJ explicitly welcomes archival expansions of
  conference papers (note the typical ≥30% new-material expectation in cover letter).
- IEEE Sensors Journal page (`https://ieee-sensors.org/sensors-journal/`) gave
  `Submission-to-ePublication = 8.8 weeks (median)` and IF 4.5 — faster to e-pub but scope
  leans to physical sensing/instrumentation, so it is "fast" not "best fit" for a
  scheduling/bandit-theory paper.
- Use a real desktop User-Agent string; the default headless UA gets blocked more often.
- Pipe `curl | python3` to strip `<script>/<style>` then `<[^>]+>`, collapse whitespace,
  then `grep -oiE` for `Submission-to|weeks|Impact Factor|first decision|expanded conference`.
  This `curl | python3` pattern triggers a HIGH security-scan approval prompt (pipe-to-
  interpreter) — expected, let người dùng approve.
- resurchify.com is curl-accessible as an SJR/quartile fallback when Scimago is blocked.

## bài AoI-greenhouse / IoTJ recommendation precedent (June 2026)

For bài AoI-greenhouse (channel-aware Value-of-Update sensor scheduler, RMAB theory + multi-trace
experiments), the recommended first choice was **IEEE Internet of Things Journal**: Q1, IF
8.2, first-decision ~6.9 weeks, and it has the right community (co-sponsored by Sensors
Council + ComSoc + Computer Society + Signal Processing Society) plus an official Expanded
Conference Papers track. IEEE Sensors Journal e-pubs faster (8.8 wk median) but is the
wrong "home" for an algorithm/theory contribution. Always ask người dùng whether the
submission is a standalone journal paper or an extended conference paper before finalizing,
because the Expanded Conference Papers track needs an explicit declaration of the prior
paper and the added material.

### IoT-J submission packaging facts (verified from author guide, June 2026)

When người dùng says "xúc tiến bản nộp IoTJ ... lấy đúng template về" for a paper already
in `\documentclass[journal]{IEEEtran}`: that IS the IoT-J template — no template swap
needed. Confirm/extract the real submission rules from the official author guide page
(`https://ieee-iotj.org/guidelines-for-authors/`; the homepage and many other slugs 404):
- **Template:** double-column IEEEtran (`kpsewhich IEEEtran.cls` confirms it ships).
- **Page charges:** 8 published pages FREE, then **$175/page mandatory over-length** on
  the published version — there is NO hard page cap and a long paper is NOT rejected for
  length. A 15-page paper is allowed; it just incurs ~7×$175. Tell người dùng the cost and
  offer to condense to the typical 11–14 pages, but don't force it.
- **Abstract:** 150–250 words, single paragraph, NO citations or displayed equations.
  Verify word count programmatically before declaring compliant.
- **ORCID:** mandatory for all authors, entered in ScholarOne at submission (not in the
  .tex file) — mention it as a manual step.
Package the submission zip with `main.tex` + `references.bib` + `main.bbl` + `sections/`
+ all `\input`/`\includegraphics` figure assets, EXCLUDING `_backups*`/`_review_artifacts*`
/aux/log. Verify by extracting the zip into a CLEAN `/tmp` dir and running the full chain
from scratch (`pdflatex → bibtex → pdflatex → pdflatex`); require 0 `??` and the expected
page count before handoff. Name it `<Project>_IoTJ_submission.zip` + `<Project>_IoTJ_main.pdf`.

## Response Template

When answering, say:

- `If the requirement is Q1 in a category close to the paper, my first choice is ...`
- Include the checked Q1 categories that match the manuscript.
- Separate `fastest` from `best fit`; do not imply the fastest venue is automatically the best Q1 category fit.
- Add a fallback path: first submit to best-fit Q1; if speed/risk dominates, move to IEEE Access or Sensors with adjusted framing.
