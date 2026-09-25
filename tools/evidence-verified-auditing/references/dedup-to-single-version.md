# Reducing a project tree to one copy of each file

Triggered by "no `v2`/`v3`/`_final` clutter, keep only the newest/best version of each
file, delete what is redundant". The instinct is to grep for version-shaped names and
delete the older ones. That destroys provenance in a tree that is not under version
control. This is the procedure that does it safely.

---

## 1. Survey before deciding anything

Four measurements, all cheap, all needed before a single removal:

```python
# a) size and file count per top-level directory -- where the mass is
# b) every file whose NAME looks versioned
PAT = re.compile(r'(_v\d+|[-_.]v\d+|_final|_copy|_old|_new|_bak|_backup|_orig'
                 r'|\bR\d+_|_revised|_edit)', re.I)
# c) every group of files with an identical sha256 -- the real duplicates
# d) an import/reference graph: for each candidate, which files mention its name
```

(c) is the only list that proves redundancy. (b) is a list of *names*, and a
version-shaped name is frequently not a version at all (see §2). Never delete from (b).

Then classify every duplicate group before acting:

| group shape | verdict |
| --- | --- |
| one copy in a backup/archive dir, one live | keep live; the backup is a rollback point by design |
| build output ≡ hash-pinned deliverable | **keep both** — see §3 |
| same plan/config inside two sealed run directories | keep both — per-run self-containment |
| a log re-run whose files differ in content | keep both — the difference is reproducibility evidence |
| a log re-run that is byte-identical and adds nothing | archive one |
| bytecode / cache / toolchain intermediates | delete, regenerable |

## 2. A version-shaped name may be a protocol version locked by hash

Before renaming or "merging" anything named `foo_v2.py` / `foo_v3.py`:

```bash
grep -rn 'foo_v2\(\.py\)\?' --include='*.json' --include='*.py' .   # sealed records + hardcoded paths
grep -rn 'sha256' --include='*.json' records/ | head               # is the filename+hash pinned?
```

Three things make a rename break provenance, and any one is sufficient:

1. a **sealed record** stores the filename and its sha256 (a pre-registration or protocol
   JSON). Renaming leaves the record pointing at a file that does not exist.
2. a **path constant** is hardcoded elsewhere: `SEALED_GATES_PATH = parents[1]/"dir"/"foo_v2.py"`.
3. the file **self-verifies** against a declared hash, so a rename silently detaches it
   from the thing it claims to be a version of.

When `v2` and `v3` are *different protocol generations* (one frozen and hash-pinned, one
the candidate under test), they are not two versions of a file and there is nothing to
deduplicate. Report that instead of renaming, and re-verify the pinned hash afterwards:

```bash
python3 -c "import hashlib,pathlib;print(hashlib.sha256(pathlib.Path('dir/foo_v2.py').read_bytes()).hexdigest()[:16])"
```

## 3. Byte-identical is not the same as redundant

This is the inverse of the "hash differs but content is identical" trap. Two copies that
match exactly can be *load-bearing*: a build tree's output and a hash-pinned deliverable
that agree prove the shipped artifact equals what the current sources build. Deleting
either loses the proof or breaks the pin.

So measure reproducibility before assuming one copy is spare:

```bash
T=/tmp/rebuild_test; rm -rf $T; mkdir -p $T; cp -r manuscript/* $T/; cd $T
OLD=$(sha256sum main.pdf | cut -d' ' -f1); rm -f main.*; latexmk -pdf -interaction=nonstopmode main.tex
NEW=$(sha256sum main.pdf | cut -d' ' -f1); [ "$OLD" = "$NEW" ] && echo REPRODUCIBLE || echo "DIFFERS"
```

A LaTeX/PDF rebuild typically yields the **same byte size and a different hash**, because
`CreationDate` is embedded. That means the matching pair is *not* regenerable-and-therefore-
spare; it is the only evidence tying deliverable to sources. Check `/CreationDate` and
`/ModDate` before concluding "just a timestamp, delete one".

Do the rebuild in a scratch copy, never in the live tree, and verify the live file's hash
is unchanged afterwards.

## 4. Archive, never delete, when there is no undo

```bash
git -C . rev-parse --git-dir 2>&1 | grep -q fatal && echo "NOT A GIT REPO -- no undo"
```

In a non-git tree, every removal is permanent. Use three classes and refuse to act on
anything unclassified:

- **DELETE-DUP** — sha256 byte-identical to a file that is being KEPT. Find the twin by
  hash *at delete time* and refuse if none exists; the twin's name goes in the manifest.
- **DELETE-REGEN** — an explicit, enumerated list of toolchain intermediates. Never infer
  this from a pattern: `.aux/.blg/.fls/.fdb_latexmk` regenerate, `.bbl` is often needed for
  submission and `.log` is input to a build-diagnostics check.
- **ARCHIVE** — unique content that is superseded. `shutil.move` to a durable volume,
  verify the destination hash, and record it.

Verify the mount is real before starting, or "archive" silently becomes "delete":

```bash
df -h /media/<vol> | tail -1     # must show a mounted filesystem
```

## 5. The manifest must survive a second run

A cleanup script that writes its manifest with `open(path, 'w')` **destroys the previous
run's evidence**: the second run moves nothing, so it records nothing, and writes an empty
file over the real record. The archived files survive; the reason they are there does not.

```python
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
run_manifest = ARCHIVE / f'DEDUP_MANIFEST_{stamp}.tsv'      # every run writes its own
main = ARCHIVE / 'DEDUP_MANIFEST.tsv'
existing = [x for x in main.read_text().splitlines()[1:] if x.strip()] if main.exists() else []
if existing and not this_run_rows:
    pass                    # refuse to clobber a non-empty manifest with an empty one
elif not existing:
    write(main, this_run_rows)
```

Every manifest row should carry **how it was established**, because the rows are not
equally strong:

| evidence class | meaning |
| --- | --- |
| `archived_in_sas` | file is in the archive now; hash recomputed from it |
| `recomputed_from_twin` | deleted as a byte-identical duplicate; the kept twin still exists and was verified identical at delete time, so this *is* the deleted file's hash |
| `not_recoverable` | deleted regenerable intermediate; gone, and a rebuild would not reproduce the same bytes. Stated as such — never left blank, never invented |

## 6. Idempotency and non-regression are both proved by running again

```bash
sha_before=$(sha256sum <key sources> | sha256sum | cut -c1-16)
python3 dedup.py; echo "run1=$?"
sha_mid=$(sha256sum <key sources> | sha256sum | cut -c1-16)
python3 dedup.py; echo "run2=$?"          # must report "removed 0 files"
sha_after=$(sha256sum <key sources> | sha256sum | cut -c1-16)
[ "$sha_mid" = "$sha_after" ] && echo IDEMPOTENT
python3 make_validation_report.py          # full suite, must still be all green
```

Run 2 is where the manifest bug in §5 shows up, which is why it is part of the procedure
rather than an optional extra.

## 7. Two false-positive classes in "this file is orphaned"

Import-graph scans (`who mentions this filename?`) flag live files:

1. **Entry points.** A tool invoked by a report generator, a shell command, a cron entry,
   or a human is imported by nobody. Check whether a generator/runner names it, and whether
   it appears in any status report, before calling it dead.
2. **Files that import *from* the tree.** A script that measures an external dataset but
   `import`s a module from this repo cannot be relocated to the project it superficially
   belongs to — moving it breaks the import. It stays, and the README should say why, so
   the next scan does not re-flag it.

Conversely, a file whose *only* consumer is a volatile location needs rescuing, not
keeping: if a patch in the repo was already applied to a target under `/tmp`, copy the
applied target into the durable archive beside the patch, with a note saying the patch is
the authoritative description of the change.

## 8. Status reports about the tree must be generated, not written

A hand-written validation report goes stale silently — it cannot notice that the suite grew,
that the PDF was rebuilt, or that a page-count claim stopped being true. Write a generator
that runs every check and reads each number from that command's output:

- one list of `(label, argv, cwd, pattern)`; run each, quote the regex capture, record exit;
- a regex that finds nothing is a **failure**, not a silent blank — otherwise a renamed
  output line turns a check into a no-op that still reads as green;
- the tool prints `len(CHECKS)` itself. A count quoted by hand from memory was wrong twice
  in one session while the list sat right there;
- include the things that are cheap to get wrong and expensive to fake: build-log error
  counts, page count **and where the body ends** (a total page count alone does not say
  whether a venue limit is met — find the page `References` starts on and subtract),
  declared-hash verification of the deliverable, and the pinned hash of any sealed module.

Regenerate after any cleanup, so the report describes the tree that exists.
