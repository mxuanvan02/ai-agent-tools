# Identity gate and final-artifact gate (2026-07-30)

Use this reference whenever a research session contains multiple projects, old summaries, ZIP/PDF artifacts, or proxy-model review.

## Project identity gate — before any mutation

1. Require direct evidence tying the task to the requested manuscript: user-stated title or supplied file, actual working directory, and corresponding `main.tex`/PDF.
2. Never infer the target project from a stale summary, an old path, or the last file opened.
3. If title/path conflict: report `BLOCKED`, say no changes were made, then locate or ask for the correct artifact.
4. For externally supplied ZIPs, inspect safely and extract to a separate working copy. Keep the original untouched.
5. Back up the exact files to be edited under `_backups/` and record SHA-256 before edits.

## OmniProxy/GPT review discipline

- Verify a model call with a small text completion first; use the correct endpoint/payload evidenced by that probe.
- Never change router configuration unless the user explicitly directs it.
- A timeout or repeated proxy failure is not a manuscript finding. Diagnose once; then continue with local evidence and state model cross-review is `BLOCKED`.
- Model feedback is a candidate critique only. Check every claim against manuscript text, tables, logs, and source artifacts.

## Completion gate for a reviewed manuscript

Do not call a manuscript “final” merely because compilation succeeds. Require evidence for:

1. requested scope is the correct manuscript;
2. every approved edit is in the intended working copy;
3. LaTeX build succeeds;
4. citations and cross-references are resolved;
5. log is checked for overfull boxes/errors; if overfull occurs, use PDF text coordinates or rendered page inspection to establish whether content escapes the page;
6. final PDF checksum is recorded;
7. if sending a ZIP, test archive integrity and include/record its checksum;
8. only say “sent” after a successful `send_message` result with its message handle.

## Reporting pattern

After **every** tool call, report the actual result immediately. Do not describe tools not yet called or work not yet completed. Split findings into: (a) definite source/build/citation defects, (b) evidence-based reviewer risks, and (c) unverified items. “Non-empty model output” is not correctness, sufficiency, or effectiveness evidence.
