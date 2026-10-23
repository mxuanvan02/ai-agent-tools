# The REVIEW.md contract

## What a good REVIEW.md says

- **What failure looks like here.** One sentence. For docs: "it lies." For config: "it
  misroutes." For code: "the test passes but the behavior is wrong." This is the single
  most important line in the file.

- **What to look for.** The three things that, if broken, would actually matter. Not style,
  not formatting, not "could be cleaner." Those belong in a linter.

- **What to skip.** Paths the reviewer should never touch. Findings already handled by CI.

- **Evidence, not names.** Every finding must cite a file and a line, and explain what would
  break if ignored. A finding that is a guess about a name is not a finding.

- **Summary format.** Start with a count: "3 findings: 1 important, 2 nit." If there is
  nothing to fix, say so plainly. Do not pad with praise or caveats.

## What makes a REVIEW.md useless

- **Too long.** A long REVIEW.md is one nobody reads. Keep it to one page.

- **Too vague.** "Make sure the code is good" is not a contract. "The test must pass and the
  behavior must match the spec" is.

- **Too prescriptive.** "Use this naming convention" belongs in a linter, not a review.

- **Stale.** A REVIEW.md that lists paths that no longer exist is worse than no REVIEW.md,
  because the reviewer will trust it and miss real findings.

## Who writes it

The code owner. Not the reviewer, not the author of the PR. The person who is responsible
for the area writes the contract, and the reviewer follows it.

## How often to update it

Every time a finding is rejected because the REVIEW.md did not cover it, the REVIEW.md must
be updated. Every time a path is renamed or removed, the REVIEW.md must be updated. A stale
REVIEW.md is a bug.
