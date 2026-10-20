# Cảnh báo văn bản học (textual criticism caveats)

The disputes and traps that are already known. Read this **before** round 1 of a
search, because most of them will otherwise cost you a round to rediscover, and
because a direction that ignores them will read as uninformed to any Vietnamese
reviewer.

Every entry below is sourced to the corpus fetched while building this skill, or
to a named source recorded in `assets/verified_terms.json`.

## Contested attributions

### Quốc âm thi tập and the Nguyễn Trãi / Nguyễn Bỉnh Khiêm overlap

The Vietnamese corpus records that about **30 Nôm poems appear in both**
`國音詩集` (Nguyễn Trãi) and `白雲庵詩集` (Nguyễn Bỉnh Khiêm), and quotes Bùi Duy
Tân's explanation: both Nôm collections survive only in later copies, and between
Nguyễn Bỉnh Khiêm's death (1585) and the Phúc Khê printing (1868) — some three or
four hundred years — the two collections could easily have become mixed.

Also recorded: multiple modern editions give **different poem counts** (161, 176,
177, 152) because each editor made different decisions about the overlaps.

**Consequences:**
- Never state a poem count for either collection without naming the edition.
- Any stylistic argument that depends on a poem being by one author must address
  the overlap.
- `Quốc âm thi tập` is described in the English corpus as **attributed** to
  Nguyễn Trãi — the attribution is traditional, not documentary.

### Gia huấn ca

Recorded in the English corpus as "attributed to Nguyễn Trãi", 976 lines. Same
status: traditional attribution, no contemporary witness.

### Nam quốc sơn hà

Attributed to Lý Thường Kiệt; the corpus gives 1077. The attribution is
traditional. The poem's own transmission is complicated — one fetched page notes
it is preserved in the *Complete Tang Poems*, which raises the separate question
of how a Chinese anthology came to hold it.

### Chinh phụ ngâm — who rendered it into Nôm

The Hán original `征婦吟` is by Đặng Trần Côn (d. 1745). The Nôm version
`征婦吟曲` is attributed to **Đoàn Thị Điểm or Phan Huy Ích, and this is
disputed**. Both attributions have defenders. Any argument that rests on the
Nôm text's style must state which attribution it assumes and why it matters.

### Lĩnh Nam chích quái is a layered text

The corpus dates it to the 14th century and records it as **edited by Vũ Quỳnh
(1452–1516)**. A work accreted and edited across two centuries has no single
author and no single date. Cite the layer you read.

### Truyền kỳ mạn lục — compilation or creation

The corpus records Bùi Duy Tân's position: on the evidence of the stories'
character, `傳奇漫錄` is **not** a collection of the kind `嶺南摭怪` or
`天南雲錄` are, but a work of literary creation in the full sense — a reworking
that marks an important step in the development of image-based narrative in Hán
literature.

Also recorded: Hà Thiện Hán's preface dated **1547** says Nguyễn Dữ wrote it
while living in seclusion in the mountains of Thanh; one scholar (Nguyễn Phạm
Hùng) dates it to **before 1527**, under the Lê. And Nguyễn Bỉnh Khiêm —
recorded as the author's teacher — is named in one manuscript as having
`hiệu chính` (corrected) the text, while another manuscript's title page reads
`傳奇傳錄` rather than `傳奇漫錄`.

**Consequences:** the dating question is live, the title itself varies between
manuscripts, and the compilation-vs-creation question is a genuine research
problem, not a settled fact.

### Nguyễn Huy Tự — a name, not a work, but worth recording

The verified table corrects his Han name to `阮輝嗣` (the corpus also records
`阮輝似` in a manuscript bibliography). Different sources give different
characters for the same person. When a Han name appears once, treat it as a
hypothesis.

### Trần Văn Giáp

Verified as `陳文玾` — eight occurrences in the fetched page — not the plausible
`陳文甲`. His `Tìm hiểu kho sách Hán Nôm` is the standard descriptive
bibliography, so his name appears in citations often; getting the character wrong
there is visible.

## Lost and missing material

### Toàn Việt thi lục

The Vietnamese corpus records that the Hán Nôm Institute issued a press release
announcing that it had **lost 25 ancient volumes**, including precious material
such as `全越詩錄`, Lê Quý Đôn's poetry anthology.

**Consequence:** claims about this work's contents may rest on secondary
descriptions rather than on a consultable witness. Say so when it matters.

### Works recorded as extant only in other works

`居塵樂道賦` and `得趣林泉成道歌` (Trần Nhân Tông) survive **inside**
`禪宗本行`, a 1745 woodblock. `詠花煙寺賦` (Huyền Quang) likewise. Their earliest
witness is therefore centuries later than their composition, and their text
passed through a compiler's hands.

The Chinese corpus also records that many works attributed to Trần Nhân Tông
(`禪林鐵嘴語錄`, `大香海印詩集`, `僧伽碎事`, `石室寐語`) are **mostly lost**, which
it names as the central difficulty of researching Vietnamese Buddhist literature.

**Consequence:** for the Trần dynasty Buddhist corpus, absence of evidence is
structural, not a gap you can search your way out of. Frame claims accordingly.

## Date traps

Measured while building this skill, all of them plausible-looking and all wrong:

| Trap | Wrong result | Why |
|---|---|---|
| Regex over infoboxes for dynasty ranges | `nhà Lý 1054-1072`, `nhà Hồ 1400-1427`, `nhà Mạc 1594-1677` | Reign-title ranges and remnant-period ranges, not dynasty spans |
| Years on a work's page | `上京記事` → 1885; `雨中隨筆` → 1906; `金雲翹新傳` → 1902/1906 | Those are **print/copy** years; composition is 1782–83, late Lê–early Nguyễn, and the Chinese source respectively |
| "Most frequent Han run near the gloss" | 5 of 12 wrong | Returns the author's name, a sibling work, a filename — whatever else the sentence mentions |

The four date kinds and how to name them: `period-and-canon-map.md`.

## Variant orthography traps

Real variants across reputable sources — search both, and do not silently
normalise in a quotation:

- `kí` / `ký` — `Thượng kinh ký sự`, `Kiến văn tiểu lục`
- `tùy` / `tuỳ` — `Vũ trung tùy bút` appears both ways, including inside the
  same catalogue record
- `kì` / `kỳ` — `truyền kì` / `truyền kỳ`
- `Truyện` / `Chuyện` — the grade-10 textbook title is *Chuyện chức phán sự đền
  Tản Viên* while the scholarly title is *Tản Viên từ phán sự lục*
- `Yên` vs `煙` — the Han writes `花煙寺` while Vietnamese reads "Hoa Yên tự";
  the simplified `花烟寺` also appears. Query all three.
- `阮嶼` vs "Nguyễn Dữ" — the corpus notes the author is also called
  **Nguyễn Dư**; the Han is `阮嶼` in both readings

## What to write down for any textual claim

Six fields. Omitting the first two is how an uncheckable statement enters a paper:

1. **Which witness** — Hán original, Nôm rendering, phiên âm, or translation.
2. **Which edition/record** — shelfmark (`R.xxx`, `nlvnpf-xxxx`, `NLVNPF-xxxx`,
   `A.xxx`, `VHv.xxxx`) or full bibliographic citation.
3. **What the preface says** — `序跋` is where compilers name themselves and date
   the work.
4. **Whether variants exist** — and if so, which ones you are not discussing.
5. **Attribution status** — documentary, traditional, or disputed.
6. **Date kind** — composition / lifespan / surviving witness / setting.

## The one rule

**A specific that you cannot source is worse than a gap you admit.** "Approximately
100 poems survive, though editions differ" is defensible. "The collection contains
107 poems" is a fabrication the moment the number has no edition behind it — and
in this field, where poem counts genuinely differ between editions, the fabricated
number is often *close enough to look right*, which is what makes it dangerous.

See `research-direction-design.md` for turning a known dispute into a feasible
direction, and `deep-research-protocol.md` for round 4 (adversarial search).
