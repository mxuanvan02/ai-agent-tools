# Proving a verifier can fail

A checker that reports `checked: 85, mismatches: 0` is only evidence if it is
capable of reporting a mismatch. Verifiers written in a hurry frequently are not:
they parse the wrong key, guard an empty set, or carry an assertion that nothing
computes. This is the procedure for converting "my checker passes" into "my
checker passes and here is proof it can fail".

---

## 1. The four classes of false green

Each of these produces a clean verdict on data that would fail if the checker
worked. All four were found live in one verifier that reported 0 mismatches.

### Vacuous aggregate

```python
"all_have_bbox": all(...) if items else False   # empty subset reports a verdict
```

A subset that is legitimately empty (a unit with no OCR words) still gets a
boolean, so an assertion about coverage fails for a reason unrelated to coverage.
Fix: count the *exceptions* and assert the count is zero.

```python
n_missing = sum(... for item in items)
"all_have_bbox": n_missing == 0
```

Then also report the denominator — `0 of 6671` is a claim about a population,
while `0` alone is not.

### Wrong key

Iterating a dict whose keys are composite (`<id>::<variant>`) and then stripping
only the prefix leaves a suffix that matches nothing downstream. Every item scores
0, every fraction becomes 0.0, and the verifier passes because 0.0 is what the
spec table happens to expect for an unrelated field.

Detect it by asserting the join rate itself:

```python
o["n_items_scored"] = scored
o["n_items_unmatched_to_bundle"] = len(rows) - scored   # pin this to 0
```

A feasibility or coverage fraction with no "how many rows actually joined" beside
it is unverifiable.

### Neutered guard

`if False:` left around an assertion, or a `raise` replaced by `pass`. Compiles,
runs, reports success. Detect it by *scanning the file you are auditing* for dead
branches — this is the mutation a survivor analysis must include, because a
checker cannot be trusted to notice its own guard was removed:

```python
def dead_guards(tree):
    return [n.lineno for n in ast.walk(tree)
            if isinstance(n, (ast.If, ast.While))
            and isinstance(n.test, ast.Constant) and not n.test.value]
```

### Swallowed assertion

```python
try:
    assert_suite_really_ran()
except AssertionError:
    pass          # call site present, "live", failure discarded
```

Counting live call sites does not catch this. Walk up the parent chain from the
call to the enclosing `ast.Try` and inspect each handler:

- a handler catching `AssertionError`/`Exception`/`BaseException`/bare is
  swallowing **unless** it re-raises or returns a non-zero exit code;
- `except AssertionError as exc: print(exc); return 3` is legitimate — turning a
  guard into an exit code is not swallowing. Test the detector against both
  shapes or it will flag correct code.

Self-test the detector on synthetic snippets covering: `pass`, `return 0`, bare
`except`, `except Exception`, tuple of exceptions, re-raise, `return 3`,
unrelated exception type, no `try` at all, and a dead-branch call. If a snippet
class is misclassified, the detector is not ready to guard anything.

---

## 2. The mutation loop

Run it as a single script that restores the original file by hash at the end, so
a crash mid-loop cannot leave a mutated checker on disk.

```python
orig = path.read_text(); h0 = sha256(orig.encode()).hexdigest()
for label, old, new in MUTANTS:
    assert orig.count(old) == 1, label      # ambiguous anchor = bad mutant
    path.write_text(orig.replace(old, new))
    assert new in path.read_text()          # confirm the mutation landed
    rc, problems = run()
    survived += (rc == 0)
    path.write_text(orig)
assert sha256(path.read_text().encode()).hexdigest() == h0   # restored
```

Mutate two kinds of thing, in roughly equal measure:

- **expectations** — change a pinned number (`4` → `29`). Cheap; proves the pin is
  actually read.
- **logic** — flip `>=` to `>`, swap two counting conventions, replace a filter
  with an unfiltered count, invert a subset test. This is the kind that survives
  expectation-only mutation.

Include at least one **boundary** mutant that must stay green: a value one below
a threshold. If the checker goes red there, it has a false positive and every
future clean run is luck.

### Count mutants honestly

A mutant that raises during *setup* never ran its assertion. `continue`-ing past
it and reporting `16/16 killed` is a false claim about your own test — the correct
report is 15 killed plus 1 not-run, then fix the setup and re-run it. Track setup
failures as their own category and print them.

Report survivors rather than hiding them, and classify each:

- **equivalent mutant** — the change cannot alter the output on this data. Do not
  "fix" the code; **pin the premise** that makes it equivalent, so the equivalence
  is stated and goes red when the data changes:

  ```python
  # Pinned because it makes removing the guard equivalent rather than undetected:
  # no unit in this corpus has zero regions, so `if n_regions and ...` cannot
  # change the count. Asserting the premise makes that falsifiable.
  o["n_units_with_zero_regions"] = sum(1 for u in units if not u["n_regions"])
  ```

- **real hole** — fix it, then add the mutant to the standing list so the fix is
  regression-tested.

### Pin returned values, not constants

`"selftest": "passed"` is a string literal; it survives every mutation of the code
that was supposed to earn it. Have the probe **return its numbers** and assert
against those, including the value the wrong algorithm would produce:

```python
o["selftest_pairwise_on_synthetic"] = SELFTEST["pairwise"]        # 1
o["selftest_positional_zip_on_synthetic"] = SELFTEST["zip"]       # 2
o["selftest_algorithms_differ"] = SELFTEST["algorithms_differ"]   # True
```

Choose synthetic inputs where the correct and the buggy algorithm provably
disagree, and assert they do — otherwise the self-test cannot distinguish them and
says nothing.

---

## 3. A guard cannot protect itself: use a separate trust root

Every in-file guard is defeatable by editing that file: neuter the condition,
delete the call, swallow the exception. Three successive hardening rounds each
survived mutation testing for exactly this reason. The fix is structural, not
more assertions.

Put the check in a **separate file** that:

1. **runs** the suite (import the module and call its entry function) rather than
   trusting its output file;
2. **re-derives** what should have happened from the suite's own source AST —
   extract every assertion label literally written in the body, count the dynamic
   ones separately, and require the executed labels to match;
3. reads the suite's real counters after the run, and cross-checks them against
   its own derivation;
4. scans the suite file for dead branches and swallowed guards (§1).

Deriving the expectation from the AST is what closes the last hole: a hand-written
`EXPECTED = 61` can be lowered to `0` to match a gutted body, but a count read from
the source cannot be edited without editing the assertions themselves.

A script-style suite (module-level code, no `test_` functions) cannot be imported
for this if it calls `sys.exit()` at module level — see the pytest pitfall in the
main skill. Wrap the body in a function first; then both the CLI and the trust root
call the same function.

---

## 4. Two implementations must disagree somewhere to be worth having

Cross-checking an independent reimplementation agreed 27/27 while the one field
holding a real bug was absent from the comparison list. The agreement was real and
useless for that field.

- Add a newly computed field to the cross-check **in the same edit** that creates
  it. Prefer deriving the pair list from one implementation's keys over typing it
  by hand.
- Print unmatched entries (`DIFF`) explicitly, and print the agreement count with
  its denominator so a shrunk list is visible.
- A cross-check that only compares aggregates ("both say 60") proves little;
  compare the per-stratum values too.

---

## 5. A documented checker may not exist

Release documentation routinely promises a validator: "the emitted layer is checked
by `audit/verify_x.py`, which fails closed, so a bad release cannot be produced."
Before believing the invariant, **grep the file listing for that filename**. In a
29k-file archive the promised checker had zero matches, meaning the redaction was
performed by the builder and never independently re-checked — the release contained
an unfulfilled promise about itself.

When you find this:

1. Report it as a defect in the release, not as your own tooling gap.
2. Write the checker, enforcing exactly what the documents promise plus the rules
   the sibling artifacts are actually governed by.
3. Verify it against the real release artifact (download it; do not test against a
   fixture you made), and report its receipt: files scanned, strings scanned,
   declared-hash matches, per-layer violations.
4. Mutation-test it to the same standard as any other verifier (§2), including
   boundary cases that must stay green.
5. Keep it **outside** the release tree if it contains non-ASCII test fixtures — a
   checker enforcing "no diacritics in this directory" will flag itself if it is
   placed inside that directory.

Also derive config from the artifact rather than hardcoding it: read the exclusion
list out of the release's own manifest so the checker tracks the release instead of
a copy of it made at authoring time.

---

## 6. Calibrating an attribution matcher

When the checker's job is to decide whether each number in a document is *sourced*
(provenance audit, citation grounding, claim-to-dataset reconciliation), the matcher
itself needs calibrating — a matcher loose enough to accept anything makes "every
number is accounted for" mean nothing.

### Identity: calibration must call the shipped matcher

A private probe copy that hardcodes one of the matcher's inputs (`frac_reason=None`)
rejects every token the real matcher accepts through that input. It reported
`true_positive = 0.9958` for a matcher that was correct, and the two "misses" were
the probe's own rule, not a regression. Route both paths through one function; if a
lookup table is built for the probe, use it in the probe.

### Bounds: derived, declared, and reachable

1. Declare the bound **before** measuring, and say so in a comment.
2. Compute the analytic **coverage ceiling** of the pinned universe — what fraction of
   random numbers in the relevant range genuinely coincide with a real value. A fixed
   2% false-accept bound was unreachable because the ceiling was 3.4% (3dp) / 8.6%
   (1dp). Bound = ceiling + declared slack, printed beside the measurement.
3. **Do not gate on a mutation detection rate.** Corrupting real tokens and requiring
   rejection has a ceiling set by coincidence: a mutant landing on another legitimately
   pinned value cannot be rejected by any correct matcher (measured 39/102 decimal,
   362/450 integer). Gating on 0.90/1.00 failed a correct matcher forever.
4. Gate on **unexplained acceptances = 0**: mutants the matcher accepts that no pinned
   or recorded value can legitimately produce. Decide legitimacy with an independent
   arithmetic re-derivation, never by asking the matcher — that is circular.
5. Report the rejection rate and the coincidence count beside it as *limitations*,
   not as gated quantities.

### Snapshot-gate every structural classifier

A regex rule's **reach** must be pinned to the exact token set it fires on:

```python
EXPECTED_HYPHEN_IDENTIFIER_TOKENS = ["256"]   # the 256 in "SHA-256"
...
if hyphen_ids != hyphen_exp:
    print("VERDICT: the hyphenated-name rule now fires on %s, not the reviewed "
          "snapshot %s" % (hyphen_ids, hyphen_exp))
    return 1
```

Recompute the fired set from the text rather than trusting a flag recorded during
classification, so the snapshot measures what the rule *does*. Widening the rule then
becomes a deliberate, reviewed edit.

### Line-level consistency is a separate question

See core rule 13 in the main skill. Token attribution passing on every token does not
mean the line is true: `42/227 = 18.1%` had three individually sourced tokens and one
false sentence. Add a check that recomputes every printed `a/b = X` at X's own printed
precision, and mutation-test it by corrupting the numerator (`41`→`42`) *and* the
printed ratio (`18.1`→`18.5`) — the two corrupt different tokens and must both go red.

### Wrong statistical function survives as a plausible number

`fisher(b, 0, 0, d)` used for a McNemar test is degenerate: the margins force a single
table, so it returns 1.0 for every arm and silently destroys published p-values. McNemar
conditions on the discordant total and is a two-sided binomial with p=0.5 over
`min(b, d)`:

```python
def mcnemar_exact(b, d):
    n = b + d
    if n == 0:
        return 1.0
    tail = sum(math.comb(n, i) * 0.5 ** n for i in range(min(b, d) + 1))
    return min(1.0, 2 * tail)
```

Only pinning a published p-value (0.0525) caught this; a pin on a count would not have.
When porting a statistic between frames, pin at least one value whose wrong-algorithm
result differs visibly — and check that the discordant difference reproduces the
observed gap (`b - d` must equal the admitted-count difference), which is what exposed
a derivation that had dropped whole pairs from the pairing.
