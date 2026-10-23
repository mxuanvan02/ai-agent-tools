# Incident to eval — turning reverts into a permanent eval set

## The problem

A reviewer that is not rescored against real failures will drift. It will catch the same
bugs it always caught, and miss the new ones. The only way to keep it honest is to feed it
the incidents it missed.

## The loop

1. **An incident happens.** A change is merged, and something breaks. The change is reverted.

2. **The incident is written up.** Not as a blame document, but as a case: what was the
   change, what broke, what should the reviewer have caught.

3. **The case is added to the eval set.** The eval set is a collection of changes that
   caused incidents, with their fix-forwards and reverts. Engineers who know the code
   confirm each bug and where it lived.

4. **The reviewer is rescored.** Every time the reviewer changes — a new prompt, a new tool,
   a new model — it is run against the entire eval set. If the score goes up, the change is
   kept. If not, it is dropped.

## Why this works

- The eval set grows with every incident, so the reviewer is always being tested against
  the kinds of bugs it has actually missed.

- The eval set is reviewed by engineers who know the code, so it is not a collection of
  synthetic cases that no one cares about.

- The reviewer is rescored every time it changes, so drift is caught before it becomes a
  pattern.

## What to include

- The change that caused the incident.
- The revert or fix-forward.
- A description of what the reviewer should have caught, and why it did not.

## What to exclude

- Incidents that were not caused by a code change (e.g., infrastructure failures).
- Incidents that were caused by a change the reviewer could not have caught (e.g., a
  race condition that only manifests under load).

## How to run the eval

The eval is a script that takes the reviewer and the eval set, and returns a score. The
score is the fraction of cases the reviewer caught. The script must be deterministic: the
same reviewer on the same eval set must produce the same score every time.

## When to update the eval set

Every time an incident is resolved, the case is added. The eval set is never pruned: an
old incident is still a valid test of the reviewer's ability to catch that kind of bug.
