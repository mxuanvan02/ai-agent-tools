# Sensors/MDPI Manuscript Preparation Notes

Use when preparing a bài probe-transmit/IoT/sensor-network manuscript for Sensors (MDPI) or another MDPI journal.

## Required/expected front matter
- Article type (usually `Article`).
- Title.
- Full author list without titles/degrees.
- Affiliations with numeric superscripts.
- Corresponding author line: `* Correspondence: Name (email)`.
- Equal-contribution note if applicable, commonly dagger-marked.
- Abstract and Keywords. For Sensors, frame keywords around sensor systems/IoT/monitoring, e.g. `Internet of Things; wireless sensor networks; safety-critical monitoring; probe-then-transmit; scheduling; fairness`.

## Required/expected back matter
Include these sections before the appendix/references when submitting to MDPI/Sensors:
- Author Contributions.
- Funding. For người dùng projects, check whether a grant code exists before leaving `no external funding`; in this session bài probe-transmit used the university grant `DHH2025-19-07`.
- Institutional Review Board Statement (or `Not applicable.`).
- Informed Consent Statement (or `Not applicable.`).
- Data Availability Statement. If raw datasets are public but not redistributed, say the raw datasets are available from their original providers; if processed data/code/scripts are on GitHub for reproducibility, say that explicitly instead of implying the repository is the sole data source.
- Acknowledgments (optional, but include if datasets/software are acknowledged).
- Conflicts of Interest.

## Section mapping from IEEE-style bài probe-transmit to Sensors/MDPI
- `Introduction` remains `Introduction`; for Sensors drafts, add recent task-oriented/semantic-AoI/remote-inference citations where they clarify why application-level risk matters. Verify DOI/metadata through Crossref/Semantic Scholar before adding. Examples used successfully: `10.1109/GLOBECOM54140.2023.10437950`, `10.1109/TNET.2024.3408673`, `10.1109/TWC.2025.3600511`.
- `Related Work` can remain separate if the article benefits from positioning, but keep it connected to the sensor-system framing.
- `System Model` + `Methodology` + `Algorithm` should be grouped under `Materials and Methods` for MDPI readability.
- If the user asks Method headings to follow contributions, rename subsections to contribution-shaped labels such as `Contribution 1: Safety-Critical Probe-Then-Transmit Formulation`, `Contribution 2: Threshold-Aware Value of Urgency`, `Contribution 3: Probe Selection Under Service Debt`, and `Contribution 4: Debt-Aware Payload Allocation`.
- `Performance Evaluation` becomes `Results`.
- Theory/complexity can be `Theoretical Analysis` if substantial; otherwise move selected results into `Materials and Methods` or appendix.
- Discussion/limitations should be `Discussion`.
- `Conclusion` should be `Conclusions`.
- Appendices can follow MDPI back matter or be placed before references depending on the official template. Do not leave an empty-looking `Appendix A`; give it a descriptive title (e.g., `Proof Details for the Debt-Based Service Guarantee`) and a short sentence explaining why the appendix exists.
- For proof appendices, write in conventional mathematical style: statement -> definitions/assumptions -> displayed equalities/inequalities/implications -> `\square`. Keep prose sparse and use phrases like `Fix`, `Set`, `For any`, `Since`, `Thus`, `Hence`; avoid tutorial-style step narration unless needed.

## Framing for Sensors
- Emphasize sensor-system contribution, not only algorithmic scheduling: wireless sensor networks, pull-based sensing, metadata/payload budget, smart monitoring, safety-critical threshold violations.
- If agriculture/greenhouse is present, keep it as an application context; avoid making field deployment claims unless a real deployment exists.
- Keep claims metric-grounded: missed violations, safety-critical loss, bandwidth/runtime, fairness, scalability.

## Template handling pitfall
- Prefer the official MDPI template for Sensors drafts. The MDPI website may block automated downloads; first try the official site, then use a verified template mirror only as a practical fallback and clearly keep the official class files in the package (`Definitions/mdpi.cls`, `Definitions/mdpi.bst`, logos/assets).
- Use the official class invocation for Sensors submissions when available: `\documentclass[sensors,article,submit,pdftex,moreauthors]{Definitions/mdpi}`.
- If the official MDPI `Definitions/mdpi.cls` is unavailable in the environment, do not claim the manuscript has been fully converted to the official class. Create a clean MDPI/Sensors-structured draft with the required sections and note it can be transferred to the official class once downloaded.
- When using a local fallback article class, still preserve all scientific content and MDPI-required statements in a separate package so conversion is mostly macro/formatting work.
- MDPI's official class defines capitalized theorem environments; when converting from IEEE sources that use lowercase `theorem`, `lemma`, `definition`, etc., add compatibility aliases via `\newenvironment{theorem}{\begin{Theorem}}{\end{Theorem}}` rather than redefining counters with `\newtheorem`, which causes duplicate-counter LaTeX errors.

## Verification checklist
- Build PDF after final edits.
- Check citations/references are resolved after BibTeX and reruns; for new references, verify DOI/title/venue/year through Crossref or Semantic Scholar before inserting BibTeX.
- Check section labels still resolve after renaming `Methodology` to `Materials and Methods`.
- Check wide tables in one-column fallback layout; wrap large result tables in `\resizebox{\textwidth}{!}{...}` or use smaller tabular spacing.
- Package the Sensors draft separately from the IEEE/IoTJ draft to avoid confusing submission artifacts.
- Keep the final draft directory clean: remove LaTeX byproducts (`.aux`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.log`, `.out`) and obsolete fallback PDFs/sources after the official MDPI version builds. Keep one source (`main_mdpi_official.tex`), one final PDF, `Definitions/`, `sections/`, `figures/`, `references.bib`, and a short README.