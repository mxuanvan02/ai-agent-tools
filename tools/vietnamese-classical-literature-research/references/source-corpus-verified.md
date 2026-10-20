# Nguồn tư liệu đã kiểm chứng khả năng truy cập

Generated file. Do not edit by hand — edit `assets/verified_terms.json` and run
`python3 scripts/build_glossary.py`. `tests/test_skill_integrity.py` fails on drift.

Every row was measured with `curl` (HTTP status) and `getent hosts` (DNS) during the
session that built this file. Reachability is a property of a network and a moment in
time, so re-probe with `python3 scripts/probe_sources.py --live` before relying on a
`dns-dead` verdict, and before concluding that a `browser-only` source is unusable.

## Reachability classes

| Class | Meaning | Consequence |
|---|---|---|
| `curl-ok` | Plain HTTP fetch returns a usable status | Scriptable; safe to fetch in bulk |
| `browser-only` | Host resolves, but returns 000/403 to non-browser clients | **Not dead.** Use a browser session. Never conclude the source is gone from a curl failure |
| `dns-dead` | Domain does not resolve | Do not put this URL in a deliverable. Find the same content elsewhere |

The distinction between the last two classes is the expensive lesson here: three domains
that are commonly cited in this field were measured DNS-dead, while four important
catalogues merely block `curl`. A source list assembled from memory gets both wrong, in
opposite directions.

## Layer 1 — Primary / manuscript

### Kho tàng thư tịch cổ Hán Nôm (Thư viện Quốc gia Việt Nam)

- URL: http://hannom.nlv.gov.vn/
- Reachability: **curl OK** (`curl-ok`)
- Catalogue of digitised Han-Nom holdings with shelfmark (Mã kho R.xxx), digitisation code (nlvnpf-xxxx), page count, dimensions, print type, and a Vietnamese abstract that often quotes the original Han title. The single most useful layer-1 entry point. NOTE: the deep path /hannom/ returns 404 to curl while the host root returns 200 — cite record URLs, not the app root.

### Nom Foundation digital library

- URL: https://lib.nomfoundation.org/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- Mirrors the national-library records in a clean bilingual (Viet/English) layout with NLVNPF-xxxx identifiers. curl returns 000 from this network but the host resolves and the records are indexed by search engines, so it is bot-blocking, NOT dead. Use a browser session or reach the same record via hannom.nlv.gov.vn.

### Vietnamese National Library

- URL: http://www.nlv.gov.vn/
- Reachability: **curl OK** (`curl-ok`)
- Institutional home of the R-series shelfmarks quoted in every catalogue record.

### data.nlv.gov.vn

- URL: https://data.nlv.gov.vn/
- Reachability: **DNS DEAD — do not cite** (`dns-dead`)
- DNS FAIL measured this session. Open-data endpoint does not resolve; use hannom.nlv.gov.vn for catalogue data.

## Layer 2 — Peer-reviewed scholarship

### Tạp chí Hán Nôm articles via Viện Nghiên cứu Hán Nôm citations

- URL: https://khoavanhoc-ngonngu.edu.vn/
- Reachability: **curl OK** (`curl-ok`)
- University faculty site (literature and linguistics) hosting full-text scholarly articles in Vietnamese, including detailed textual-criticism studies with shelfmarks and edition collations. Verified reachable; used in this session for the Chỉ nam ngọc âm giải nghĩa dating debate.

### Trung tâm Nghiên cứu Quốc học / journal articles (secondary)

- URL: https://lib.hpu.edu.vn/
- Reachability: **curl OK** (`curl-ok`)
- University repository holding records and abstracts for classical works; useful for confirming an edition or a translator when the primary catalogue is silent.

### 中華佛學研究所 CHIBS bulletin (Chinese-language Buddhist scholarship)

- URL: https://www.chibs.edu.tw/ch_html/chbs/21/chbs2107.pdf
- Reachability: **curl OK** (`curl-ok`)
- Full-text peer-reviewed PDF. Verified in this session as the source confirming 禪宗本行 and the full title of 詠花煙寺賦 with its 八言賦 98-line form. Chinese-language Buddhist-studies venues are a strong layer-2 source for the Thiền Trúc Lâm corpus.

### Vietnam Studies / Journal of Vietnamese Studies (JSTOR)

- URL: https://www.jstor.org/journal/jvietstud
- Reachability: **curl OK** (`curl-ok`)
- Landing page resolves; article PDFs are paywalled. Use for English-language scholarship discovery, then obtain through a library.

### Journal of Vietnamese Studies (publisher site)

- URL: https://online.ucpress.edu/jvs
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 403. Publisher platform blocks non-browser clients; works in a browser.

### Viện Nghiên cứu Hán Nôm (institute site)

- URL: https://www.hannom.org.vn/
- Reachability: **DNS DEAD — do not cite** (`dns-dead`)
- curl 000 (0.3s, connection refused/failed) while DNS resolves; http://hannom.org.vn returns 301. Measured unusable from this network in this session. The institute's catalogue content survives via hannom.nlv.gov.vn and lib.nomfoundation.org, so cite those instead. Re-probe before relying on it.

### Viện Văn học / ncvanhoc.org.vn

- URL: https://ncvanhoc.org.vn/
- Reachability: **DNS DEAD — do not cite** (`dns-dead`)
- DNS FAIL measured this session. Do not put this URL in a deliverable.

### tapchinghiencuuvanhoc.vn

- URL: https://tapchinghiencuuvanhoc.vn/
- Reachability: **DNS DEAD — do not cite** (`dns-dead`)
- DNS FAIL measured this session. Search for the journal's articles through a university repository or a database instead of linking the domain.

### academia.edu

- URL: https://www.academia.edu/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 403. Hosts many relevant dissertations; needs a browser and often a login. Never cite an aggregator page — cite the dissertation itself.

## Layer 3 — Reference works (bibliographies, dictionaries)

### Nom Foundation (main site, dictionaries and tools)

- URL: https://nomfoundation.org/
- Reachability: **curl OK** (`curl-ok`)
- Hosts the Tu dien chu Nom dan giai sources pages, which give per-work Han titles, script (Han vs Nom), verse form, shelfmark and holding institution. Verified in this session as the source of the 天南明鑑 record (HNv.006).

### Từ điển Hán Nôm (hvdic.thivien.net)

- URL: https://hvdic.thivien.net/
- Reachability: **curl OK** (`curl-ok`)
- Han-Nom dictionary with per-entry Han form and, for book titles, a short definition citing Từ điển Nguyễn Quốc Hùng. Fast way to confirm a Han title. Verified this session for 天南餘暇集.

### Thi Viện (thivien.net)

- URL: https://www.thivien.net/
- Reachability: **curl OK** (`curl-ok`)
- Large poet-and-poem database with Han author names (e.g. 阮秉謙) and long scholarly introductions quoting Vũ Khâm Lân, Phan Huy Chú, Lê Quý Đôn, Trần Văn Giáp on text history. Valuable for the transmission history of a poet's collected works; it is a secondary compilation, so cite the underlying scholar it quotes, not the site.

### Tự điển chữ Nôm trích dẫn (bibliography of Nom texts)

- URL: http://nguyendu.com.free.fr/nom/ThuMuc_Bia_1.htm
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- Static bibliography listing 51 Nom works with Han title, author, source edition and date. Verified this session as the source for 詠花煙寺賦 / Huyền Quang. Personal-hosted mirror of a printed reference work: check against a library edition before citing in formal work.

### 中國哲學書電子化計劃 (ctext.org)

- URL: https://ctext.org/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- The standard full-text corpus of received Chinese classics. curl returns 000 from this network but the host resolves and the site is heavily mirrored; treat as bot-blocking. Needed for the Chinese side of any comparative genre or thought question (志怪, 傳奇, 理學, 四書五經).

### Kanripo 漢籍リポジトリ

- URL: https://kanripo.org/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 403. Open repository of Chinese-language texts, useful for edition images.

### Gallica (BnF)

- URL: https://gallica.bnf.fr/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 403. Holds EFEO-era Vietnamese manuscripts and early printed quốc ngữ editions; relevant for transmission history of Nom works.

### Yale Southeast Asia Collection research guide

- URL: https://guides.library.yale.edu/SoutheastAsiaCollection
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 000, DNS resolves. Library research guide listing Han-Nom studies resources; useful orientation, open in a browser.

## Layer 4 — Open corpora (verify spelling, do not cite as scholarship)

### Wikisource tiếng Việt

- URL: https://vi.wikisource.org/
- Reachability: **curl OK** (`curl-ok`)
- Vietnamese-language public-domain texts, including full translations of works such as Thượng kinh ký sự and Vũ trung tùy bút with translator named. Good for reading a text fast and for confirming a Han title form; not a citable edition.

### 維基文庫 (zh.wikisource.org)

- URL: https://zh.wikisource.org/
- Reachability: **curl OK** (`curl-ok`)
- Classical Chinese texts, including Vietnamese-authored Han works such as 平吳大誥. Use to read the Han original; confirm against a manuscript or printed edition before quoting.

### 識典古籍 (shidianguji.com)

- URL: https://www.shidianguji.com/
- Reachability: **curl OK** (`curl-ok`)
- Full-text classical Chinese corpus. Verified this session as holding the complete text of 傳奇漫錄 卷之二 opening with 傘圓祠判事錄, which is how the Han title of that story was confirmed at character level. Strong for reading a work end to end; still layer 4 for citation purposes.

### 漢喃数字圖書館 (chunom.net)

- URL: https://www.chunom.net/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 000 but resolvable and indexed; mirrors national-library catalogue records with the same identifiers. Handy cross-check when hannom.nlv.gov.vn is slow.

### Việt Sử Đồ (vietsudo.org)

- URL: https://vietsudo.org/
- Reachability: **curl OK** (`curl-ok`)
- Knowledge graph of Vietnamese history that quotes primary sources with the Han original inline. Verified this session as the source of the 大越史記全 thư 1697 Inner Cabinet edition quotation naming 天南餘暇集. Excellent for locating a Han phrase inside a named primary source.

### Wikipedia (vi / zh / en)

- URL: https://vi.wikipedia.org/
- Reachability: **curl OK** (`curl-ok`)
- Used in this session as a Han-character verification corpus via the MediaWiki API (142 pages fetched). Appropriate for confirming a character or a title form and for finding which named scholar or catalogue to cite. NOT a citable authority for a scholarly claim.

### vietnamvanhien.org

- URL: https://www.vietnamvanhien.org/
- Reachability: **DNS DEAD — do not cite** (`dns-dead`)
- DNS FAIL measured this session. Frequently cited in older reference lists; treat any citation to it as needing a replacement source.

### hannom-rcv.org (Nom-language wiki)

- URL: http://hannom-rcv.org/wi/
- Reachability: **browser only (blocks non-browser clients)** (`browser-only`)
- curl 403. Content written IN chữ Nôm with quốc ngữ gloss; of interest for Nom orthography, not a scholarship source.

## Search order that follows from the layering

1. **Settle a textual fact** (title characters, author, shelfmark, edition year, page
   count) at layer 1. `hannom.nlv.gov.vn` gives the record with `Mã kho R.xxx` and
   `nlvnpf-xxxx`; `lib.nomfoundation.org` gives the same record bilingually.
2. **Find the scholarly conversation** at layer 2. Vietnamese textual criticism
   (văn bản học) lives in university faculty sites and journals; the Chinese-language
   side of Buddhist and genre questions lives in venues like the CHIBS bulletin.
3. **Confirm a reading or a definition** at layer 3 (dictionaries, bibliographies).
4. **Read fast, verify spelling** at layer 4 — then go back up a layer before citing.
   `識典古籍` gives a complete 傳奇漫錄 text; that is enough to confirm 傘圓祠判事錄
   character by character, and still not a citable edition.
5. **Never ship a `dns-dead` URL.** If a claim depends on such a source, the claim needs
   a different source, not a different link.

