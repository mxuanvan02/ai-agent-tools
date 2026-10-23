---
name: code-review-gates
description: "Use when reviewing agent-written changes at volume: risk tier decides how many humans, findings need voter-confirmed evidence, review rounds are capped, and noise is measured — not guessed."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Code-Review, Gates, Risk-Tiers, Evidence, Convergence, Agent-Written-Code]
    related_skills: [github-pr-workflow, evidence-verified-auditing, system-one-work-loop, software-quality-workflows]
---

# code-review-gates

Review machinery for changes produced faster than a human can read them. Every rule here comes
from a measured failure, not from a preference: the four scripts and two templates in this tool
implement the parts of a machine-first review pipeline that can be made deterministic.

The premise, stated by the team that had to solve it: asking *"did a human read the code?"* is an
imprecise proxy for *"what could go wrong with this change, and which check — automated or human —
is the right one to catch it?"*

## What this tool does NOT claim

- It does not review code. It decides **how much human attention a change gets**, records what a
  reviewer found and what the author did about it, and blocks a change whose findings are
  unanswered. The finding itself still comes from a model or a person.
- It does not make an agent's approval count as a human's. Nothing in this tool can promote a bot
  review into a required human slot.
- It does not replace reading evidence. A tier of `low` is a statement about blast radius, not
  permission to merge blind.

## When to use

- Agents open most of the pull requests, and per-line human review has stopped being possible.
- You want a written, reviewable rule for *which* changes need zero, one, or two people, so the
  answer does not depend on who is asking or how tired the reviewer is.
- Review keeps going in circles: the same area is flagged every round, rounds never terminate.
- You need a number for reviewer noise so you can tell whether the reviewer is getting better.

## When NOT to use

- Solo repository, few changes a day: read the diff. The overhead is not repaid.
- The change cannot be reverted cheaply. Every rule below assumes rollback is minutes, not days;
  without that, the correct answer is more people, not fewer.
- You are about to use the tier as a way to skip the human on a change whose failure mode is
  financial, irreversible, or public. Those paths belong in `always_human` and stay there.

## The four mechanisms, each with a script

| Mechanism | Script | What it decides |
|---|---|---|
| **Risk tier from the change, not the author** | `scripts/risk_tier.py` | tier (low/medium/high) → required human approvals (0/1/2), per-file reasons, fail-closed on unknown paths |
| **Findings need evidence and a response** | `scripts/review_ledger.py` | every finding carries `file:line` + severity class, is answered (fixed/rejected/intentional/ignored), duplicates rejected |
| **Review must converge** | `scripts/review_ledger.py gate` | unanswered findings block; rounds capped (default 3); noise rate reported |
| **Incidents become the eval** | `references/incident-to-eval.md` | each confirmed incident becomes a permanent case the reviewer is rescored against |

## Workflow

1. **Before opening the change** — the author produces evidence, not a claim: tests/build/lint
   output, and a fresh-context review of the diff. Anthropic's own estimate is that giving the
   model something it can run makes the final result two to three times better; a second agent
   reviewing the diff in a *fresh context* is what stops the author from talking itself into a pass.
2. **Classify** — `python3 scripts/risk_tier.py --config risk-tiers.json --numstat <(git diff --numstat origin/main...)`.
   Never classify by hand and never let the author pick the tier. Unmatched paths are `high`.
3. **Record findings** — `review_ledger.py add` for each finding a reviewer posts, with severity
   `important | nit | pre-existing`. Style-only, diagnostics-only and cleanup findings are dropped
   before recording (see `references/finding-verification.md`).
4. **Answer every finding** — `review_ledger.py respond --action fixed|rejected|intentional|ignored
   --note "..."`. Silence is not an answer; a rejected finding needs a reason.
5. **Gate** — `review_ledger.py gate --max-rounds 3`. Non-zero exit blocks the merge.
6. **After the merge** — if it breaks, the change is reverted first and the incident is written
   into the eval set (`references/incident-to-eval.md`). "You land it, you own it" only works
   because changes are small, reversible, and the review looks at the system, not the person.

## The tier table (copy this into your own policy)

| Tier | Examples | Human approvals |
|---|---|---|
| low | docs, copy, internal-only features, additive changes behind a flag | 0, once automated review and security checks are green |
| medium | ordinary product changes, and sensitive-but-bounded areas (caching, auto-updater, prompt text) | 1 |
| high | highest-risk code, plus paths that always need two people | 2 |

Rules that must survive translation into your repo:

- **The change sets the tier, not the author.** A second pass asks whether *this* change needs a
  person even when its tier says it does not.
- **Some paths always need a person**: CI workflow files, auth, billing, migrations, installers,
  anything an owner marked sensitive.
- **A bot's approval never fills a human slot.** Automated review can clear a low-risk change; it
  cannot be the one person that medium requires.
- **The person who prompted the agent is on the hook.** On an agent-written change they count as
  one of the required reviewers, exactly as if they had typed it.
- **Approval binds to one commit.** New commits that the system cannot vouch for — an agent push, a
  hand-resolved merge — invalidate the approval and it has to be given again.

## Convergence rules (the part everyone skips)

The failure is not "the reviewer missed bugs"; it is that author and reviewer keep each other busy.
Measured on one team's own pull requests: a single change went through **more than fifty rounds**
of review and fixes overnight before its author stopped it, and when they ran `git blame` on what
the reviewer kept flagging, about **59%** was code that had been there since the reviewer's first
pass. The reviewer was rarely finding new bugs; it was finding a few more old ones each round, and
the team had trained itself to run many rounds by default.

Four changes fixed it, and this tool enforces all four:

1. **Round cap** — after three rounds the reviewer stops and asks the author to reconsider the
   approach, instead of producing round four.
2. **Diff-only re-review** after the first few passes.
3. **Flag the class of bug**, so the author fixes every instance instead of one line.
4. **No repeats** of findings already posted — `review_ledger.py add` rejects a duplicate
   `(file, line, class)` outright.

After those changes: changes passing in one review round went from 65% to 78%; changes needing five
or more rounds went from 8.9% to 1.5%; mean reviews to pass went from 2.08 to 1.32.

## Noise is measured from what authors do

It is easy to catch more bugs if you do not mind flagging non-bugs, so the reviewer needs a
counterweight. Sort every comment the reviewer left by how the author on that change responded —
**fixed it, said it was wrong, said the behavior was intentional, decided it did not matter** — and
run the reviewer on known-clean changes to count how often it reports something that would have led
someone to make a harmful change. `review_ledger.py stats` computes the first part directly.

Noise costs more when the author is an agent: a person waves off a nit in seconds, an agent fixes it,
which means another commit and another round of review. The stated priority, in this order, is
**catch real bugs first, cut review rounds second**.

## Files

- `scripts/risk_tier.py` — deterministic tier + approval count from a diff and a rules file.
- `scripts/review_ledger.py` — append-only finding ledger: `add`, `respond`, `round`, `stats`, `gate`.
- `templates/risk-tiers.json` — rules file with a fail-closed default, ready to edit.
- `templates/REVIEW.md` — code-owner contract for one repository area.
- `references/risk-tiers.md` — how to write the rules so they stay honest.
- `references/finding-verification.md` — parallel finders, verifier votes, what to drop, severity labels.
- `references/review-md-contract.md` — what a good REVIEW.md says, and what makes one useless.
- `references/incident-to-eval.md` — turning reverts into a permanent eval set.
- `tests/` — unit tests; they include mutants that prove each gate can fail.

## Known limits (measured, not guessed)

- A path-based tier is a proxy. It cannot see that a one-line change to a config default reroutes
  production traffic. Keep such paths in `always_human` and accept the false positives.
- The ledger records decisions, not understanding. It cannot detect a reviewer who read nothing and
  answered every finding with `ignored`; `stats` will show the noise rate, and a human has to look.
- Round capping hides a real signal when the underlying change is genuinely bad. That is why the cap
  escalates to "reconsider the approach", not to "merge anyway".
- Nothing here checks that CI actually ran. Pair it with required checks; a green gate over red CI
  is the one failure mode this tool cannot see.
