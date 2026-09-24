# IEEE/IEEE Access Author and Template Handling

Use this note when the user asks to change author blocks, affiliations, or journal templates for IEEE-family manuscripts.

## Author Block Pattern From June 2026 Session

Preferred author list for bài bandwidth-scheduling/bài probe-transmit-style papers:

- Xuan Van Mai\n- Duc Minh Phuong Le\n- Tri Nguyen Dang\n- Khanh Duy Truong\n- Hoang Son Nguyen\n- Tuong Tri Nguyen

Affiliations:

- `a` the university of Education, the university, Hue, Viet Nam
- `b` Gia Dinh University, Department of Information Technology, Ho Chi Minh, Viet Nam
- `c` Institute of Open Education and Information Technology -- the university, Hue, Viet Nam

Notes:

- `1` marks equal contribution for Xuan Van Mai and Duc Minh Phuong Le.
- `*` marks Tuong Tri Nguyen as corresponding author.
- Use `Viet Nam` spelling when matching this author block.
- Do not include academic titles.

## IEEE Journal / IEEE Access Pitfalls

- IEEE Access author requirements emphasize full names, affiliations, corresponding author indication, and any equal contribution note; put these in the author note/footnote if the class supports it.
- For IEEEtran-based drafts, use `\thanks{...}` blocks for affiliations, equal contribution, and corresponding author.
- For custom non-IEEE article drafts (e.g., hội nghị C1-style bài bandwidth-scheduling), use a centered author block with superscripts and a compact affiliation block.
- Do not claim a manuscript is fully converted to official IEEE Access format unless `ieeeaccess.cls` or the official template files are present and the PDF builds with that class. If the official class is missing, say it is IEEE/IEEE-Access-ready in author metadata but not yet built with the official Access class.
- If downloading official IEEE templates fails due access restrictions, keep the buildable source stable and tell the user the exact remaining step: obtain the official IEEE Access LaTeX template/`ieeeaccess.cls`, then port the content.

## Verification

After author/template changes:

1. Build the PDF after the final edit.
2. Check undefined refs/citations.
3. Check overfull hboxes.
4. Refresh the submission package so source and PDF match.
5. Inspect the first page visually if title/author layout is the main requested change.
