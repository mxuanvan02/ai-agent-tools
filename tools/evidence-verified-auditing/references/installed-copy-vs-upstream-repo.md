# Promoting edits from an installed runtime copy to its upstream repo

Extends the "claim a side effect only from its own confirmation" rule in
`SKILL.md` to a side effect that is easy to believe and easy to get wrong: an
improvement you made to something *installed*, which you then report as an
upgrade to the *project*.

---

## 1. The failure mode

Runtime library directories (skills, plugins, prompt packs, dotfile configs,
site-packages) are working copies with **no version history**. Editing them in
place is legitimate and takes effect immediately, so every local signal is green:

```
packaged validator  -> passed, exit=0
package unit tests  -> all OK
manager discovery   -> enabled
```

None of those touch git. In one session four separate improvements accumulated in
an installed package across several turns while the upstream `HEAD` never moved;
each turn's report said the capability now existed. It existed on one machine,
until the next reinstall from the repo silently reverted all of it.

The trap is structural, not careless: the thing you tested and the thing that
persists are two different trees.

## 2. Detect drift before reporting the upgrade

Run this as soon as you edit anything under a runtime library, and again before
any claim that the capability "is now available":

```bash
INSTALL_DIR=~/.hermes/skills/<pkg>       # or plugin/config install root
CLONE_DIR=/path/to/<pkg>-clone

diff -rq "$INSTALL_DIR" "$CLONE_DIR" | grep -v '\.git'
#   "Files ... differ"          -> modified file not in the repo
#   "Only in $INSTALL_DIR ..."  -> whole new file not in the repo

git -C "$CLONE_DIR" log --oneline -1
git -C "$CLONE_DIR" status --porcelain
git -C "$CLONE_DIR" ls-remote origin 'refs/heads/*'
```

If `ls-remote` shows the same SHA it showed before your work, nothing you did is
saved anywhere but this filesystem. Say that explicitly rather than describing
the feature as delivered.

## 3. Promotion sequence

Order matters: the tree you validate must be the tree you commit.

1. **Copy per file, then prove the copy.** Compare a hash per path, not directory
   size or timestamps:

   ```bash
   for f in SKILL.md references/a.md references/b.md; do
     a=$(sha256sum "$INSTALL_DIR/$f" | cut -c1-16)
     b=$(sha256sum "$CLONE_DIR/$f"   | cut -c1-16)
     [ "$a" = "$b" ] && echo "OK   $f" || echo "DIFF $f  $a  $b"
   done
   ```

2. **Run the package's own validator inside the clone**, not the installed copy.
   Validating the install and committing the clone proves nothing about what
   landed.
3. **Branch, never the default branch.** Stage only the promoted paths — `git add
   -A` in a clone that also holds build output or local experiments commits them
   too.
4. **Commit with `-F <file>`.** See the shell-quoting trap in `SKILL.md`.
5. **Push, then verify against the remote**, asserting both that your branch
   appeared *and* that the base branch SHA is unchanged.
6. **State which side is now authoritative**, and whether a reinstall would keep
   or lose the change.

## 4. Three git traps that print success while nothing landed

- **No commit identity in this repo.** Fails with `unable to auto-detect email
  address`; a `cmd; echo "exit=$?"` wrapper then reports `exit=0` from the `echo`,
  not from git. Set identity **locally** (never `--global`), reusing the values
  another repo on the same machine already uses for consistency, and confirm by
  finding the new SHA in `ls-remote`.
- **Fetch URL is not push URL.** With a read-scoped token, HTTPS push returns
  `403 Permission ... denied` even for the repo owner. Change only the push side —
  `git remote set-url --push origin git@host:owner/repo.git` — and confirm with
  `git remote -v` that the two lines now differ.
- **Cannot open the PR.** If the credential lacks write scope, branch push over
  SSH works but PR creation does not. Push the branch, hand the user the
  `.../pull/new/<branch>` URL, and do not report the PR as opened.

## 5. Companion rule: verify sources before they enter a reference bank

Writing a knowledge file (a genre blueprint, an API note, a domain corpus) into a
skill is authoring a citation list. Same discipline as any other identity check:

- Resolve **every** entry against an authoritative registry by stable ID before
  it goes in the file — Crossref by DOI, DataCite for `10.48550/*` preprints,
  package registries by name+version. Keep the pass count and state it in the
  file itself (`19/19 verified`), so a future reader knows the bank was checked
  rather than recalled.
- When the user supplies material whose own reference list does not cover its
  central claims, **do not supply the missing attributions from memory**. Say
  which parts are unsourced, look the candidates up, and keep only what the
  registry confirms. Filling the gap with plausible author names is fabrication
  even when the names turn out to exist.
- Record a short `Verification Status` section at the end of the reference file:
  what was registry-verified, what came from the user unverified, and what was
  dropped for lack of confirmation.
