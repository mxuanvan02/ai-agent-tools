# REVIEW.md — contract between code owner and reviewer

Copy this file into the area of the repository you own. Keep it short; a long REVIEW.md is one
nobody reads, and the reviewer will fall back to guessing.

## What failure looks like here

> One sentence. For docs: "it lies." For config: "it misroutes." For code: "the test passes
> but the behavior is wrong." This is the single most important line in the file.

## What to look for

- The three things that, if broken, would actually matter in this area.
- Not style. Not formatting. Not "could be cleaner." Those belong in a linter.

## What to skip

- Paths the reviewer should never touch.
- Findings that are already handled by CI (lint, types, build).

## Evidence, not names

- Every finding must cite a file and a line.
- Every finding must explain what would break if it were ignored.
- A finding that is a guess about a name is not a finding.

## Summary format

- Start with a count: "3 findings: 1 important, 2 nit."
- If there is nothing to fix, say so plainly: "no findings."
- Do not pad the summary with praise or caveats.
