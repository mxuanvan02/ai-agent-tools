# Finding verification — how to drop noise before it reaches a human

## The problem

It is easy to catch more bugs if you do not mind flagging non-bugs. A reviewer that reports
everything will have a high recall and a low precision, and the author will stop reading.

## The filter

Before a finding is recorded in the ledger, it must pass three checks:

1. **Not style-only.** If the finding is about formatting, naming, or readability, it belongs
   in a linter, not a review. A linter can be fixed in one commit; a review finding requires
   a conversation.

2. **Not diagnostics-only.** If the finding is "this function is long" or "this module has
   many dependencies," it is a smell, not a bug. Smells are worth discussing in a design
   review, not a code review.

3. **Not cleanup-only.** If the finding is "this comment is stale" or "this import is unused,"
   it is a chore, not a bug. Chores are worth fixing, but they do not block a merge.

## Parallel finders, verifier votes

The Anthropic team runs several agents in parallel, each looking for bugs. A separate group
of agents votes on each finding, and only findings that get enough votes are posted. This is
what stops a single over-eager reviewer from flooding the ledger.

## Severity labels

Every finding must be labeled:

- **important** — a bug that would break something if ignored.
- **nit** — a small issue that is worth fixing but does not block.
- **pre-existing** — a bug the PR did not introduce. Labeled so the author is not blamed
  for code they did not write.

## What to drop

- Findings about style, diagnostics, or cleanup.
- Findings that are only about code the PR did not touch.
- Findings that the reviewer cannot cite with a file and a line.

## What to keep

- Findings that explain what would break if ignored.
- Findings that cite a file and a line.
- Findings that are about code the PR actually changed.
