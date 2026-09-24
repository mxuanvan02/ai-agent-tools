# Bibtex output-directory trap + Crossref API source verification

## Bibtex + output-directory resolution bug

### Symptom
- `bibtex build/main` reports "Done." with 0 warnings
- But bbl has fewer entries than expected (e.g. 75 instead of 89)
- New `\citation{}` lines exist in `build/Chapter/*.aux` but are ignored
- PDF shows `[?]` for new citations despite bib file being syntactically correct

### Root cause
bibtex resolves `\@input{Chapter/foo.aux}` relative to CWD, not relative to the
aux file's directory. When CWD is project root and aux files are in `build/`,
bibtex looks for `./Chapter/foo.aux` (doesn't exist) instead of
`./build/Chapter/foo.aux`.

bibtex DOES read the `\@input` and even logs "A level-1 auxiliary file:
Chapter/noidung_chap4.aux" — but silently fails to open it (no error/warning).

### Fix (in build.sh)
```bash
# bibtex must run FROM $OUTDIR so \@input{Chapter/...} resolves correctly
(cd "$OUTDIR" && BIBINPUTS="..:$BIBINPUTS" BSTINPUTS="..:$BSTINPUTS" bibtex main) || true
```

### Diagnostic recipe
```bash
# 1. Confirm bib parses correctly in isolation
cat > /tmp/test_bib.aux << 'EOF'
\relax
\bibstyle{IEEEtran}
\bibdata{/full/path/to/references}
\citation{newkey1}
\citation{newkey2}
EOF
cd /tmp && bibtex test_bib
# If this produces entries → problem is subaux resolution, not bib syntax

# 2. Confirm citations ARE in subaux
grep '\\citation' build/Chapter/noidung_chap4.aux

# 3. Force-inject citations into main.aux before \bibdata line (workaround)
sed -i '/^\\bibdata/i \\citation{newkey1}' build/main.aux
bibtex build/main  # now produces entries → confirms the bug

# 4. Proper fix: run bibtex from build/ with BIBINPUTS
(cd build && BIBINPUTS=".." bibtex main)
```

## Crossref API for source verification

When adding citations to support region-specific claims (not part of PRISMA
corpus), verify each DOI via Crossref API before inserting into bib:

```bash
curl -sS "https://api.crossref.org/works/10.3390/su13126603" | python3 -c "
import json,sys
d=json.load(sys.stdin)['message']
print('TITLE:', d.get('title',['?'])[0])
print('YEAR:', d.get('issued',{}).get('date-parts',[['?']])[0][0])
print('AUTHORS:', '; '.join(a.get('family','?') for a in d.get('author',[])))
print('VENUE:', d.get('container-title',['?'])[0])
print('DOI:', d.get('DOI'))
"
```

### Search pattern for Vietnam-specific sources
```bash
# Search Crossref by keyword
curl -sS "https://api.crossref.org/works?query=LoRaWAN+Vietnam+agriculture&rows=5&select=title,author,issued,container-title,DOI"
```

### Key lessons from Jun 2026 session
1. Google/Bing bot-blocked for Vietnamese queries; Crossref API works reliably
2. Gov VN sites (lamdong.gov.vn, thuvienphapluat.vn) block automated access
3. Wikipedia vi API (`/api/rest_v1/page/summary/`) works for basic region facts
4. For Discussion/Recommendations section: citations outside PRISMA corpus are
   allowed as "nền cảnh" (context) — declare this explicitly in the opening
   paragraph of the section so reviewer knows they're not corpus entries
5. Always mark bib entries with a comment block separating PRISMA corpus from
   region-evidence entries
