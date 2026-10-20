# Bản đồ thời kỳ và tác phẩm kinh điển (period and canon map)

Orientation only. This map exists so a topic can be placed in time in one read,
and so the researcher knows which works to expect as the field's coordinates.
**It is not a citation source.** Every date below carries the evidence that
supports it, and the distinction between four different kinds of date is the
single most useful thing on this page.

## The four dates, and why conflating them corrupts a paper

Measured during the build of this skill: extracting every 4-digit year from a
Vietnamese wiki page about a work returns a pile of numbers that are each true
and mostly irrelevant — the author's birth and death years, the year of a
surviving manuscript, the year of a woodblock reprint, the year of a modern
edition, and the year the events happened. A regex cannot tell them apart, and
neither can a reader who has not been warned.

| Date kind | Example | Ask before using |
|---|---|---|
| **Composition** | `Bình Ngô đại cáo` 1428 | The one a literary-history claim usually needs |
| **Author lifespan** | Nguyễn Trãi 1380–1442 | Bounds composition; never equals it |
| **Surviving manuscript/edition** | `Thượng kinh ký sự` khắc in 1885; `Vũ trung tùy bút` bản chép 1906 | What you can actually hold or cite |
| **Setting / events** | `Hoàng Lê nhất thống chí` covers 1767–1802 | Not the date of writing |

Rule: **name the kind every time you give a date.** "Truyện Kiều, 1820" and
"Truyện Kiều, bản in 1902" are different claims and both are correct.

A second measured failure, worth recording because it looks authoritative: a
regex over infoboxes returned `nhà Lý 1054-1072` (a reign title range),
`nhà Hồ 1400-1427` (Hồ is 1400–1407), `nhà Mạc 1594-1677` (the Cao Bằng
remnant, not the dynasty's 1527–1592). Do not machine-extract dynasty ranges.

## Periodisation

The period covered by this skill runs from independence in the 10th century to
the turn of the 20th, and is conventionally divided by dynasty. Dates below are
the ones that appeared consistently in the fetched corpus; where the corpus was
silent, the range is marked **unverified** rather than filled in from memory.

| Period | Range | Corpus evidence | Literary character |
|---|---|---|---|
| Ngô–Đinh–Tiền Lê | 10th c. | — | Almost nothing survives; chữ Hán becomes the official script |
| Lý | 1009–1225 | `nhà Lý` with Lý Thái Tổ 1009–1028 | Buddhist-inflected; thiền poetry begins |
| Trần | 1225–1400 | `Đại Việt 1010-1400`, `nhà Trần năm 1377`, `nhà Trần năm 1400` | Zen literature at its peak; Hán poetry mature; **chữ Nôm appears** |
| Hồ / thuộc Minh | 1400–1427 | `nhà Hồ (1400–1427)` — this range spans the occupation, treat with care | Rupture; Ming destruction of books |
| Lê sơ | 1428–1527 | `nhà Lê sơ (1428-1527)` twice in corpus | Hán literature institutionalised; Nôm poetry established |
| Mạc | 1527–1592 | `nhà Mạc … 1527 … 1592`; `nhà Mạc ở Cao Bằng … 1594-1677` | Fragmentation; Nguyễn Bỉnh Khiêm |
| Lê trung hưng (Lê–Trịnh) | 1533–1789 | `Lê trung hưng (1533) cho tới tận trước…`; `Lê-Trịnh (1592)` | Trịnh–Nguyễn split; the great Nôm century |
| Đàng Trong / Đàng Ngoài | 17th–18th c. | dedicated pages fetched | Two literary centres, different conditions |
| Tây Sơn | 1778–1802 | `nhà Tây Sơn 1778-1802` (Đàng Trong page) | Brief; unifies the country |
| Nguyễn | 1802–1945 | `nhà Nguyễn (1802–1945)` | Classical forms perfected then displaced by quốc ngữ |

For literary work, the century matters more than the dynasty. Use
`thế kỷ XV`, `thế kỷ XVI`, `thế kỷ XVIII` in searches: Vietnamese scholarship
periodises that way, and the phrase retrieves survey articles that a dynasty
name does not.

## Canonical works, with the date each claim rests on

Dates marked ✓ were read inline in `en.wikipedia: Vietnamese literature`, which
dates works in a single continuous list — the most reliable single dating source
found in this session. Dates marked ◐ come from the work's own page and are
composition dates stated there. Everything else is marked with what it actually
is.

### 10th–14th century — foundations

| Work | 漢字 | Date | Note |
|---|---|---|---|
| Nam quốc sơn hà | `南國山河` | 1077 ✓ | Attributed to Lý Thường Kiệt; attribution is traditional, not documentary |
| Đại Việt sử ký | `大越史記` | 1272 ✓ | Lê Văn Hưu; the earliest surviving national history |
| Dụ chư tì tướng hịch văn ("Hịch tướng sĩ") | `諭諸裨將檄文` | 1284 ✓ | Trần Quốc Tuấn |
| Cư trần lạc đạo phú | `居塵樂道賦` | Trần Nhân Tông (1258–1308) ◐ | Earliest substantial Nôm text; survives inside `禪宗本行` (1745 woodblock) |
| Đắc thú lâm tuyền thành đạo ca | `得趣林泉成道歌` | Trần Nhân Tông ◐ | Same transmission history |
| Vịnh Hoa Yên tự phú | `詠花煙寺賦` | Huyền Quang 玄光 (1254–1334) | Full title 安子山竹林第三祖玄光尊者詠花烟寺賦; 八言賦, 98 lines |
| An Nam chí lược | — | 1335 ✓ | Written in China by a defector; a different perspective from domestic sources |
| Lĩnh Nam chích quái | `嶺南摭怪` | 14th c. ✓, edited by Vũ Quỳnh (1452–1516) | **Layered text**: accreted and edited over centuries. Never cite one date |
| Đại Việt sử lược | `大越史略` | 1377 ✓ | Anonymous |

### 15th century — the Hán classical peak

| Work | 漢字 | Date | Note |
|---|---|---|---|
| Việt điện u linh tập | `越甸幽靈集` | 1400 ✓ | Lý Tế Xuyên |
| Bình Ngô đại cáo | `平吳大誥` | 1428 ✓ | Nguyễn Trãi; 1,330 chữ ◐; văn biền ngẫu, thể cáo |
| Quốc âm thi tập | `國音詩集` | 15th c., attributed ◐ | Nguyễn Trãi; the earliest Nôm poetry collection; **attribution and poem counts are contested** |
| Gia huấn ca | `家訓歌` | 1420s ✓, attributed | 976 lines; attribution to Nguyễn Trãi is traditional |
| Đại Việt sử ký toàn thư | `大越史記全書` | 1479 ✓ | Ngô Sĩ Liên; the surviving standard edition is the **Nội các quan bản 1697** |
| Hồng Đức quốc âm thi tập | `洪德國音詩集` | 15th c. ◐ | Lê Thánh Tông and the Tao đàn circle; multi-author |
| Thiên Nam dư hạ tập | `天南餘暇集` | 1483 ◐ | 100 quyển; compiled by named court scholars on royal order; shelfmark A.334/1-10 |
| Bạch Đằng giang phú | `白藤江賦` | Trương Hán Siêu | Corpus gives 1455/1419 — **these are not composition dates**; leave undated unless a source is found |

### 16th century — the turn inward

| Work | 漢字 | Date | Note |
|---|---|---|---|
| Truyền kỳ mạn lục | `傳奇漫錄` | 16th c. ◐ (tựa 1547; before 1527 per one reading) | Nguyễn Dữ 阮嶼; 20 truyện in 4 quyển ◐; Hán, mixed with biền văn and poetry; each story ends with a lời bình |
| Tản Viên từ phán sự lục | `傘圓祠判事錄` | inside the above, quyển 2 | The story taught in the grade-10 textbook |
| Nam Xương nữ tử truyện | `南昌女子傳` | inside the above | Note the Han writes 南昌, the Vietnamese reads "Nam Xương" |
| Bạch Vân am thi tập | `白雲庵詩集` | Nguyễn Bỉnh Khiêm 阮秉謙 (1491–1585), 16th c. ◐ | 626 bài in one recorded edition ◐; **Nôm poems attributed to him are heavily contested and overlap with Nguyễn Trãi's** |

### 18th century — the Nôm century

| Work | 漢字 | Date | Note |
|---|---|---|---|
| Đại Việt thông sử | `大越通史` | 1749 ✓ | Lê Quý Đôn |
| Vân đài loại ngữ | `芸臺類語` | 1773 ✓ | Lê Quý Đôn; encyclopaedic |
| Phủ biên tạp lục | `撫邊雜錄` | 1776 ✓ | Lê Quý Đôn; the southern frontier |
| Kiến văn tiểu lục | `見聞小錄` | Lê Quý Đôn | Undated in corpus; find a source before dating |
| Lịch triều hiến chương loại chí | `歷朝憲章類誌` | Phan Huy Chú, early 19th c. | 49 quyển; the standard institutional-history reference |
| Chinh phụ ngâm (Hán original) | `征婦吟` | Đặng Trần Côn (d. 1745) ✓ | The Nôm rendering `征婦吟曲` is by Đoàn Thị Điểm or Phan Huy Ích — **disputed** |
| Cung oán ngâm | `宮怨吟` | 1798 ✓ | Nguyễn Gia Thiều |
| Thiên Nam ngữ lục | `天南語錄` | 17th c.; corpus shows 1682/1709 | 4,068 câu lục bát ◐ = 8,136 lines; the longest lục bát work |
| Thượng kinh ký sự | `上京記事` | written 1782–1783 ◐; khắc in 1885 | Lê Hữu Trác; shelfmark VHv.2225 |
| Vũ trung tùy bút | `雨中隨筆` | late Lê – early Nguyễn ◐; bản chép 1906 | Phạm Đình Hổ 范廷琥; 90 bài ◐; R.1609 / NLVNPF-0300 |
| Hoàng Lê nhất thống chí | `皇黎一統志` | late 18th–early 19th c. ◐ | Ngô gia văn phái; multi-author, chapter-form |

### 19th century — perfection and displacement

| Work | 漢字 | Date | Note |
|---|---|---|---|
| Đoạn trường tân thanh (Truyện Kiều) | `斷腸新聲` | 1820 ◐ | Nguyễn Du 阮攸; 3,254 câu lục bát ◐; based on a Chinese novel by 青心才人 |
| Kim Vân Kiều tân truyện | `金雲翹新傳` | the Chinese source | 1902 and 1906 are **edition** years ◐, not composition |
| Lục Vân Tiên truyện | `蓼雲仙傳` | Nguyễn Đình Chiểu (1822–1888) | Mid-19th c.; the corpus's 1886/1888 are print years |
| Nhị độ mai tân truyện | `二度梅` | 18th–19th c. | Anonymous; from the Chinese 忠孝節義二度梅; 2,826 câu lục bát ◐ |

## Compilations and reference works (not primary literature)

These are what you cite *about* the corpus. All verified as existing records:

| Work | 漢字 | Holding / edition |
|---|---|---|
| Hoàng Việt văn tuyển | `皇越文選` | NLVNPF-0171 / R.601; Tồn Am gia tàng: 裴輝璧; Hi Văn Đường 希文堂; Minh Mệnh 6 (1825); 78 pp; 26×16 cm; woodblock |
| Toàn Việt thi lục | `全越詩錄` | Lê Quý Đôn; **among the 25 volumes reported lost from the Hán Nôm Institute** |
| Khâm định Việt sử thông giám cương mục | `欽定越史通鑑綱目` | Nguyễn dynasty official history; quotes `天南餘暇集` in its commentary |
| Thiền tông bản hạnh | `禪宗本行` | 1745 woodblock; the vehicle that preserves the early Nôm Buddhist texts |
| Tìm hiểu kho sách Hán Nôm | — | Trần Văn Giáp 陳文玾; the standard descriptive bibliography |

## Verse forms, Nôm side

Recorded because they are query terms in their own right:

- `lục bát` (6–8) — the national metre; Truyện Kiều, Thiên Nam ngữ lục, Lục Vân Tiên
- `song thất lục bát` (7–7–6–8) — the ngâm khúc metre; Chinh phụ ngâm, Cung oán ngâm, Thiên Nam minh giám
- `hát nói` — a late form, closer to performance than to the classical tradition
- `ngâm khúc` (laments), `truyện thơ Nôm` (verse narratives) — the two dominant
  Nôm long forms; searching by these genre words retrieves survey scholarship
  that searching by title does not
- Hán side: `律詩` regulated verse, `絕句` quatrain, `賦` rhapsody, `駢文`/`駢偶`
  parallel prose — see `genre-and-poetics.md`

## How to use this map

1. Place the topic in a century, not a dynasty — then search with that century.
2. Pick the canonical works of that century; they are the field's shared
   coordinates and any direction that ignores them will read as uninformed.
3. For each work you will rely on, fix **which** date you mean and find its
   source. Undated is honest; wrongly dated is not.
4. Check the caveats file before making any authorship or attribution claim —
   several entries above are contested, and that is marked here on purpose.

See `textual-criticism-caveats.md` for the disputes, `genre-and-poetics.md` for
form, `source-corpus-verified.md` for where to look.
