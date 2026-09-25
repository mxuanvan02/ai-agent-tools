# Authoring a prose quality gate (scanner + policy + fixtures + tests)

Extends the "a scan produces candidates, not findings" rule in `SKILL.md` to the
case where **you are building the scanner**, not consuming someone else's. The
deliverable is a control that a future session can trust; the risk is shipping
something that reads like a control and stops nothing.

Applies to any lexical gate over text: register/voice checks, chronology and
logic checks, terminology enforcement, claim-denial density, placeholder residue.

---

## 1. A documented gate is a *proposed* control

Four artifacts commonly get reported as "the gate is available":

```
references/<gate>.md          policy prose        -> proposed
scripts/<gate>_scan.py        pattern list        -> proposed
scripts/test_<gate>_scan.py   passing tests       -> proposed
validator lists the files     existence check     -> STILL proposed
```

The last one is the trap. A repository validator that only asserts
`Path(f).is_file()` for the new scanner and its fixtures will pass while the
tests never execute. Measured directly:

```bash
grep -n 'test_<gate>_scan' scripts/validate_skill.py   # appears in REQUIRED list
grep -n 'subprocess.run' scripts/validate_skill.py     # ...but no run() for it
```

Wire the tests into the validator as a subprocess with a non-zero-exit check, and
add the same step to CI. Until then the validator is proving the files exist, not
that the gate works.

## 2. Prove stopping power by mutation, and measure the mutation honestly

Delete one load-bearing branch, assert red, restore, assert green:

```bash
cp scripts/<gate>_scan.py /tmp/pristine.py
python3 - <<'PY'
import pathlib
p = pathlib.Path("scripts/<gate>_scan.py"); s = p.read_text()
target = '|(?:assembled|formed|built)\\s+(?:beforehand|earlier)\\b'   # English branch
assert target in s, "MUTATION DID NOT APPLY"      # <- do not skip this
p.write_text(s.replace(target, ""))
PY
python3 scripts/test_<gate>_scan.py ; echo "tests exit=$?"      # must be non-zero
python3 scripts/validate_skill.py  ; echo "validate exit=$?"    # must be non-zero
cp /tmp/pristine.py scripts/<gate>_scan.py
python3 scripts/validate_skill.py  ; echo "restored exit=$?"    # must be 0
```

Two honesty traps, both hit in practice:

- **The mutation silently did not apply.** A first attempt printed
  `mutated: False` alongside `validate exit=1`, and that was reported as proof of
  stopping power. It proved nothing: the validator was red for an unrelated
  reason. Assert the mutation landed before interpreting the exit code.
- **A pipe swallows the exit code.** `python3 validate.py | tail -5; echo $?`
  reports `tail`'s status. One run printed `missing required files: ...` next to
  `exit=0`. Run the command bare and read its own status.

Delete a **fixture** as a second mutation: the validator must fail with
`missing required files`, which proves the fixture is load-bearing rather than
decorative.

## 3. The scanner's output contract: candidate, verdict, no auto-rewrite

A gate that edits text is a rewriter, and a rewriter cannot be trusted with
meaning. Return findings with a *named verdict to apply*, never an applied edit:

| field | purpose |
| --- | --- |
| `class` | which defect class matched |
| `span` | the sentence, truncated, so a human can read it |
| `verdict` | the repair operation the policy licenses for that class |
| `why` | the criterion that failed, in one clause |
| `exit_code` | `0` none, `2` candidates, `1` blocking class, `3` input error |

Two disclaimers belong in the returned payload and in the CLI `--help`, not only
in the policy document:

- *a lexical hit is a candidate, never a verdict* — the human applies the ordered
  tests and records the outcome;
- *absence of hits is a partial verification only* — paraphrases of the
  paraphrasable classes have no lexical signature, so a clean scan does not
  discharge the manual pass.

Enumerate the licensed verdicts and **exclude the seductive one**. For a register
or logic gate the forbidden operation is *soften*: hedging an internal or
underspecified sentence leaves it internal and now also vague.

## 4. Calibrate on the real corpus; every false positive becomes a test

Fixtures written by the gate's author measure the author's imagination. Run
against real documents before reporting the pattern list as done:

```
first run  on a real thesis : 11 candidates
after calibration           :  5 candidates across 3 genuinely defective sentences
```

The six that disappeared were the pattern's fault, and each is now a test:

- the role of a later step was stated **in the next sentence** — widen the window
  to the following sentence before declaring the role unstated;
- a negative role (`không tạo thêm nguồn mới`, `did not add`) is a stated role;
- an adjective was mistaken for an ordering marker (`bổ sung` = *supplementary*,
  not *next*), so it must not count as a sequence cue on its own;
- the sentence already named the anchor (`trước khi chạy truy vấn`), which is the
  repaired form the gate is supposed to accept;
- diagram/notation zones and a LaTeX preamble are not prose — strip to
  `\begin{document}`, drop math, `\cite/\ref/\label` arguments, verbatim, and
  comments before matching;
- ordinary temporal language about the *object of study* (`nhiệt độ giảm trước
  khi bơm bật`) is not a process-chronology defect.

## 5. Bilingual symmetry is part of the gate

A class inventory built from one language silently passes the other. Measured on
an English text carrying every defect: **7 of 10 classes detected**, threshold
table clean, nothing in the output announcing that three classes had no English
markers at all.

Every class needs markers in both languages, a fixture in both languages, and a
test asserting the same class set on both. Two recurring near-misses: person
agreement (`does not prove` without `do not prove` under-counts a real stack) and
intensifier exclusion (`not only … but also` must be excluded exactly as
`không chỉ … mà còn` is).

When a marker does not fire, print the matcher's per-sentence output before
editing the regex. Guessing at the pattern cost two revisions; one diagnostic
print located the cause immediately.

## 6. Report shape after running a gate you built

State the two numbers separately — hits the scanner found, sites the manual pass
found — and label a scan-only clean report as partial. Distinguish licensed hits
from actionable ones: a policy that permits one roadmap passage per document will
legitimately leave findings at `exit=0`, and reporting those as defects is the
same error as missing them.

Restrict the scan to source files under version control. Sweeping a tree that
contains `_backups/<timestamp>/` inflates the count with historical copies of
already-repaired text — one run reported 109 findings, of which 107 were backups.
