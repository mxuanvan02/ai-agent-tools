# Bảng tra từ khoá Hán – Nôm đã kiểm chứng

Generated file. Do not edit by hand — edit `assets/verified_terms.json` and run
`python3 scripts/build_glossary.py`. `tests/test_skill_integrity.py` fails on drift.

## Contract for every row

Each row below carries a Han string that was **matched byte-for-byte in a fetched
source during the verification session that built this file** (`status` column). No
character in this table was recalled from memory. Evidence is named in
`assets/verified_terms.json` (`evidence[].where`).

Status values:

- `CONFIRMED-INDEPENDENT` — matched in a layer-1/2/3 named source: a library catalogue
  record with shelfmark, a full-text edition, a dictionary entry, or a peer-reviewed
  paper. Strongest. Safe to print in a deliverable.
- `CONFIRMED+GLOSS` — the Han string and its Vietnamese gloss co-occur in the same
  window of a fetched page. Strong for search terms; for a citation, upgrade to a
  named source first.
- `CONFIRMED` — the Han string occurs in a fetched page but not adjacent to the gloss
  (common for generic vocabulary such as 科舉, 平仄). Usable as a query term.

## How to use a row

A row is a **query term**, not a citation. Searching `傳奇漫錄` retrieves Chinese-language
scholarship and digitised editions that `Truyền kỳ mạn lục` cannot reach. But before the
characters appear in a paper, confirm them against a layer-1/2 source and record that
source in the evidence ledger.

Rules that cost nothing to follow and prevent the common failures:

1. **Query the genre term separately from the title.** `傳奇` (genre) retrieves
   comparative studies of the form; `傳奇漫錄` retrieves one book. They answer
   different questions and both are usually needed.
2. **Query the author's courtesy name too.** Catalogues index by both: Nguyễn Trãi and
   `Ức Trai` `抑齋`; Nguyễn Bỉnh Khiêm and `Bạch Vân am` `白雲庵`, `程國公`.
3. **Include Vietnamese spelling variants.** `kí`/`ký`, `tùy`/`tuỳ`, `kỳ`/`kì`,
   `Truyện`/`Chuyện`. Reputable sources differ and one form loses hits.
4. **Never emit a character that is not in this table without labelling it
   unverified.** An unverified character is a hypothesis, not a search term — and a
   wrong one returns zero results, which reads as "no sources exist".
5. **When this table lacks a term, verify it; do not fill it in.** Run
   `scripts/verify_han_terms.py` against fetched pages, or find a layer-1/2 source
   that prints the title, and add the row with its evidence.

## Tác phẩm (works)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| An Nam chí lược | `安南志略` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Bình Ngô đại cáo | `平吳大誥` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Bạch Vân am thi tập | `白雲庵詩集` | CONFIRMED+GLOSS | wiki corpus: vi_byat |
| Bạch Đằng giang phú | `白藤江賦` | CONFIRMED+GLOSS | wiki corpus: vi_bdgp |
| Chinh phụ ngâm khúc | `征婦吟曲` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Chỉ nam ngọc âm giải nghĩa | `指南玉音解義` | CONFIRMED | wiki corpus: en_chunom |
| Cung oán ngâm | `宮怨吟` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Cư trần lạc đạo phú | `居塵樂道賦` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Dư địa chí | `輿地誌` | CONFIRMED+GLOSS | wiki corpus: vi_nt |
| Dụ chư tì tướng hịch văn | `諭諸裨將檄文` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Gia huấn ca | `家訓歌` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Hoàng Lê nhất thống chí | `皇黎一統志` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Hoàng Việt văn tuyển | `皇越文選` | CONFIRMED-INDEPENDENT | Nom Foundation lib.nomfoundation.org/collection/1/volume/241 — NLVNPF- |
| Hồng Đức quốc âm thi tập | `洪德國音詩集` | CONFIRMED+GLOSS | wiki corpus: vi_hđqa |
| Khâm định Việt sử thông giám cương mục | `欽定越史通鑑綱目` | CONFIRMED+GLOSS | wiki corpus: vi_vsttgc |
| Kim Vân Kiều tân truyện | `金雲翹新傳` | CONFIRMED+GLOSS | wiki corpus: vi_tk |
| Kiến văn tiểu lục | `見聞小錄` | CONFIRMED-INDEPENDENT | vi.wikipedia article titled 見聞小錄 quoting 'cuốn Kiến văn tiểu lục (見聞小錄 |
| Lĩnh Nam chích quái | `嶺南摭怪` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Lịch triều hiến chương loại chí | `歷朝憲章類誌` | CONFIRMED+GLOSS | wiki corpus: vi_lthclc |
| Lục Vân Tiên truyện | `蓼雲仙傳` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Nam Xương nữ tử truyện | `南昌女子傳` | CONFIRMED+GLOSS | wiki corpus: vi_tkml |
| Nam quốc sơn hà | `南國山河` | CONFIRMED+GLOSS | wiki corpus: en_hannom |
| Nhị độ mai tân truyện | `二度梅` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Nhị độ mai' |
| Phủ biên tạp lục | `撫邊雜錄` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Quốc âm thi tập | `國音詩集` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Thiên Nam dư hạ tập | `天南餘暇集` | CONFIRMED-INDEPENDENT | vietsudo.org quoting Đại Việt sử ký toàn thư |
| Thiên Nam ngữ lục | `天南語錄` | CONFIRMED+GLOSS | wiki corpus: vi_tnng |
| Thiền tông bản hạnh | `禪宗本行` | CONFIRMED-INDEPENDENT | chibs.edu.tw/ch_html/chbs/21/chbs2107.pdf |
| Thượng kinh ký sự | `上京記事` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Thượng kinh ký sự' |
| Toàn Việt thi lục | `全越詩錄` | CONFIRMED+GLOSS | wiki corpus: vi_hannom |
| Truyền kỳ mạn lục | `傳奇漫錄` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Tản Viên từ phán sự lục | `傘圓祠判事錄` | CONFIRMED-INDEPENDENT | en.wikipedia 'The Tale of the Judge of Tản Viên Temple' |
| Việt điện u linh tập | `越甸幽靈集` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Vân đài loại ngữ | `芸臺類語` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Vũ trung tùy bút | `雨中隨筆` | CONFIRMED-INDEPENDENT | hannom.nlv.gov.vn |
| Vịnh Hoa Yên tự phú | `詠花煙寺賦` | CONFIRMED-INDEPENDENT | Tự điển chữ Nôm trích dẫn (nguyendu.com.free.fr) entry 3 |
| Đoạn trường tân thanh | `斷腸新聲` | CONFIRMED+GLOSS | wiki corpus: vi_tk |
| Đại Việt sử ký | `大越史記` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Đại Việt sử ký toàn thư | `大越史記全書` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Đại Việt sử lược | `大越史略` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Đại Việt thông sử | `大越通史` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Đắc thú lâm tuyền thành đạo ca | `得趣林泉成道歌` | CONFIRMED+GLOSS | wiki corpus: vi_chunom |
| Ức Trai di tập | `抑齋遺集` | CONFIRMED+GLOSS | wiki corpus: vi_nt |

## Tác giả, tự, hiệu (authors, courtesy names, pen names)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Bạch Vân am | `白雲庵` | CONFIRMED+GLOSS | wiki corpus: vi_byat |
| Chu Văn An | `朱文安` | CONFIRMED+GLOSS | wiki corpus: vi_cva |
| Huyền Quang | `玄光` | CONFIRMED+GLOSS | wiki corpus: vi_hq |
| Hải Thượng Lãn Ông | `海上懶翁` | CONFIRMED+GLOSS | wiki corpus: vi_lht |
| Hồ Xuân Hương | `胡春香` | CONFIRMED+GLOSS | wiki corpus: vi_hxh |
| Lê Hữu Trác | `黎有晫` | CONFIRMED+GLOSS | wiki corpus: vi_lht |
| Lê Quý Đôn | `黎貴惇` | CONFIRMED+GLOSS | wiki corpus: vi_ldt |
| Lê Thánh Tông | `黎聖宗` | CONFIRMED+GLOSS | wiki corpus: vi_ltt |
| Lê Văn Hưu | `黎文休` | CONFIRMED+GLOSS | wiki corpus: vi_lvh |
| Lý Tế Xuyên | `李濟川` | CONFIRMED+GLOSS | wiki corpus: vi_ltc |
| Mạc Đĩnh Chi | `莫挺之` | CONFIRMED+GLOSS | wiki corpus: vi_mdc |
| Nguyễn Bỉnh Khiêm | `阮秉謙` | CONFIRMED+GLOSS | wiki corpus: vi_byat |
| Nguyễn Cư Trinh | `阮居貞` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Nguyễn Cư Trinh' |
| Nguyễn Du | `阮攸` | CONFIRMED+GLOSS | wiki corpus: vi_nd2 |
| Nguyễn Dữ | `阮嶼` | CONFIRMED+GLOSS | wiki corpus: vi_ndu |
| Nguyễn Huy Tự | `阮輝嗣` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Nguyễn Huy Tự' |
| Nguyễn Khuyến | `阮勸` | CONFIRMED+GLOSS | wiki corpus: vi_nk2 |
| Nguyễn Trung Ngạn | `阮忠彥` | CONFIRMED+GLOSS | wiki corpus: vi_ntn2 |
| Nguyễn Trãi | `阮廌` | CONFIRMED+GLOSS | wiki corpus: vi_nt |
| Nguyễn Đình Chiểu | `阮廷炤` | CONFIRMED+GLOSS | wiki corpus: vi_ndc |
| Ngô Sĩ Liên | `吳士連` | CONFIRMED+GLOSS | wiki corpus: vi_dvsktt |
| Phan Huy Chú | `潘輝注` | CONFIRMED+GLOSS | wiki corpus: vi_pnc |
| Pháp Loa | `法螺` | CONFIRMED+GLOSS | wiki corpus: vi_pl |
| Phạm Sư Mạnh | `范師孟` | CONFIRMED+GLOSS | wiki corpus: vi_psm |
| Phạm Đình Hổ | `范廷琥` | CONFIRMED+GLOSS | wiki corpus: vi_pdh |
| Thanh Tâm Tài Nhân | `青心才人` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Thanh Tâm Tài Nhân' |
| Trình quốc công | `程國公` | CONFIRMED+GLOSS | wiki corpus: vi_byat |
| Trúc Lâm Tam Tổ | `竹林三祖` | CONFIRMED-INDEPENDENT | zh.wikipedia 竹林禪派 |
| Trương Hán Siêu | `張漢超` | CONFIRMED+GLOSS | wiki corpus: vi_ths |
| Trần Nhân Tông | `陳仁宗` | CONFIRMED+GLOSS | wiki corpus: vi_tdv |
| Trần Quốc Tuấn | `陳國峻` | CONFIRMED+GLOSS | wiki corpus: vi_tqd |
| Trần Tế Xương | `陳濟昌` | CONFIRMED+GLOSS | wiki corpus: vi_tx |
| Trần Văn Giáp | `陳文玾` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Trần Văn Giáp' |
| Đoàn Thị Điểm | `段氏點` | CONFIRMED+GLOSS | wiki corpus: vi_dtd |
| Đào Duy Từ | `陶維慈` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Đào Duy Từ' |
| Đặng Trần Côn | `鄧陳琨` | CONFIRMED | wiki corpus: vi_dtc |
| Ức Trai (hiệu) | `抑齋` | CONFIRMED+GLOSS | wiki corpus: vi_nt |

## Thể loại (genres)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Biền ngẫu | `駢偶` | CONFIRMED | wiki corpus: zh_pianwen |
| Biền văn | `駢文` | CONFIRMED | wiki corpus: zh_cifu |
| Biểu | `表` | CONFIRMED+GLOSS | wiki corpus: en_sino |
| Bát cú | `八句` | CONFIRMED | wiki corpus: zh_qyls |
| Bát cổ văn | `八股文` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Bình điểm | `評點` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Bút ký tiểu thuyết | `筆記小說` | CONFIRMED+GLOSS | wiki corpus: zh_chuanqi |
| Chiếu | `詔` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Chí quái | `志怪` | CONFIRMED | wiki corpus: zh_chuanqi |
| Chương hồi tiểu thuyết | `章回小說` | CONFIRMED+GLOSS | wiki corpus: zh_zhanghui |
| Cáo | `誥` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Cổ văn | `古文` | CONFIRMED+GLOSS | wiki corpus: en_classiccn |
| Hịch | `檄` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Ký | `記` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Luật thi | `律詩` | CONFIRMED | wiki corpus: zh_chuanqi |
| Lời bình | `評` | CONFIRMED | wiki corpus: zh_bagu |
| Minh | `銘` | CONFIRMED | wiki corpus: zh_chuanqi |
| Ngũ ngôn | `五言` | CONFIRMED | wiki corpus: zh_jueju |
| Nhạc phủ | `樂府` | CONFIRMED | wiki corpus: zh_chuanqi |
| Phú | `賦` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Thất ngôn luật thi | `七言律詩` | CONFIRMED | wiki corpus: zh_qyls |
| Thất ngôn tứ tuyệt | `七言絕句` | CONFIRMED | wiki corpus: zh_duizhang |
| Truyền kỳ (thể loại) | `傳奇` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Tuyệt cú | `絕句` | CONFIRMED | wiki corpus: zh_duizhang |
| Tống từ | `宋詞` | CONFIRMED+GLOSS | wiki corpus: zh_duizhang |
| Từ phú | `辭賦` | CONFIRMED+GLOSS | wiki corpus: zh_cifu |
| Tự bạt | `序跋` | CONFIRMED+GLOSS | wiki corpus: zh_guwen |
| Văn ngôn | `文言` | CONFIRMED | wiki corpus: en_classiccn |
| Đường thi | `唐詩` | CONFIRMED+GLOSS | wiki corpus: vi_thodt |

## Niêm luật, thi pháp (versification and poetics)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Bình trắc | `平仄` | CONFIRMED+GLOSS | wiki corpus: zh_duizhang |
| Dụng điển | `用典` | CONFIRMED+GLOSS | wiki corpus: zh_pianwen |
| Áp vận | `押韻` | CONFIRMED+GLOSS | wiki corpus: zh_cifu |
| Điển cố | `典故` | CONFIRMED+GLOSS | wiki corpus: zh_pianwen |
| Đối trượng | `對仗` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |

## Văn tự, ngôn ngữ (scripts and language)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Chữ Hán | `漢字` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Chữ Nôm | `喃` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Chữ quốc ngữ | `國語` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Hán Nôm | `漢喃` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Hán Việt | `漢越` | CONFIRMED+GLOSS | wiki corpus: en_hannom |
| Khải thư | `楷書` | CONFIRMED | wiki corpus: zh_hanzi |

## Tư tưởng (thought vocabulary)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Hiếu | `孝` | CONFIRMED+GLOSS | wiki corpus: en_sino |
| Kinh học | `經學` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Lý học | `理學` | CONFIRMED | wiki corpus: zh_chuanqi |
| Ngũ hành | `五行` | CONFIRMED | wiki corpus: zh_daojia |
| Nho giáo | `儒教` | CONFIRMED+GLOSS | wiki corpus: vi_nhohoc |
| Nhân nghĩa | `仁義` | CONFIRMED | wiki corpus: zh_wuxing |
| Phật | `佛` | CONFIRMED+GLOSS | wiki corpus: en_chunom |
| Phật giáo | `佛教` | CONFIRMED | wiki corpus: zh_chuanqi |
| Tam cương ngũ thường | `三綱五常` | CONFIRMED+GLOSS | wiki corpus: zh_wuxing |
| Tam giáo | `三教` | CONFIRMED | wiki corpus: zh_daojia |
| Thi ngôn chí | `詩言志` | CONFIRMED-INDEPENDENT | zh.wikipedia 夔 (乐官) |
| Thiên nhân hợp nhất | `天人合一` | CONFIRMED+GLOSS | wiki corpus: zh_tianren |
| Thiền | `禪` | CONFIRMED | wiki corpus: zh_daojia |
| Tiên | `仙` | CONFIRMED+GLOSS | wiki corpus: en_vietlit |
| Tiết nghĩa | `節義` | CONFIRMED-INDEPENDENT | vi.wikipedia 'Nhị độ mai' |
| Trung quân | `忠君` | CONFIRMED | wiki corpus: zh_duizhang |
| Tâm học | `心學` | CONFIRMED | wiki corpus: zh_lixue |
| Tứ thư ngũ kinh | `四書五經` | CONFIRMED+GLOSS | wiki corpus: zh_hanzi |
| Văn dĩ tải đạo | `文以載道` | CONFIRMED | wiki corpus: zh_chuanqi |
| Âm dương | `陰陽` | CONFIRMED | wiki corpus: zh_wuxing |
| Đạo giáo | `道教` | CONFIRMED | wiki corpus: zh_chuanqi |
| Đạo học | `道學` | CONFIRMED+GLOSS | wiki corpus: zh_lixue |
| Ẩn dật | `隱逸` | CONFIRMED | wiki corpus: zh_tangshi |

## Khoa cử, quan chế (examination system)

| Thuật ngữ | 漢字 | Status | Evidence anchor |
|---|---|---|---|
| Bảng nhãn | `榜眼` | CONFIRMED+GLOSS | wiki corpus: zh_dianshi |
| Hàn lâm viện | `翰林院` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Hương thí | `鄉試` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Hội thí | `會試` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Khoa bảng | `科榜` | CONFIRMED+GLOSS | wiki corpus: vi_khoa_bang |
| Khoa cử | `科舉` | CONFIRMED+GLOSS | wiki corpus: vi_khoa_bang |
| Quốc Tử Giám | `國子監` | CONFIRMED+GLOSS | wiki corpus: vi_vmqtg |
| Thám hoa | `探花` | CONFIRMED+GLOSS | wiki corpus: zh_dianshi |
| Tiến sĩ | `進士` | CONFIRMED+GLOSS | wiki corpus: en_sino |
| Trạng nguyên | `狀元` | CONFIRMED+GLOSS | wiki corpus: zh_bagu |
| Văn Miếu | `文廟` | CONFIRMED+GLOSS | wiki corpus: vi_vmqtg |
| Điện thí | `殿試` | CONFIRMED+GLOSS | wiki corpus: zh_dianshi |

## Corrections discovered during verification

These are recorded because they are exactly the errors a recall-based glossary makes:
the recalled character is plausible, and a search using it silently returns nothing.

| Term | Recalled (wrong) | Verified | Verified from |
|---|---|---|---|
| Nguyễn Huy Tự | 阮輝似 | `阮輝嗣` | vi.wikipedia page for the author |
| Trần Văn Giáp | 陳文甲 | `陳文玾` | vi.wikipedia page for the author (8 occurrences) |
| Thượng kinh ký sự | 上京紀事 | `上京記事` | vi.wikipedia + vi.wikisource title line |
| Vịnh Hoa Yên tự phú | 花煙寺賦 (missing 詠) | `詠花煙寺賦` | Tự điển chữ Nôm trích dẫn; CHIBS paper full title |

## Notes from the verification session

- [
- "
- V
- i
- e
- t
- n
- a
- m
- e
- s
- e
-  
- s
- o
- u
- r
- c
- e
- s
-  
- w
- r
- i
- t
- e
-  
- b
- o
- t
- h
-  
- '
- T
- r
- ú
- c
-  
- L
- â
- m
-  
- T
- a
- m
-  
- T
- ổ
- '
-  
- a
- n
- d
-  
- '
- T
- a
- m
-  
- t
- ổ
-  
- T
- r
- ú
- c
-  
- L
- â
- m
- '
- ;
-  
- t
- h
- e
-  
- H
- a
- n
-  
- f
- o
- r
- m
-  
- 竹
- 林
- 三
- 祖
-  
- i
- s
-  
- c
- o
- n
- f
- i
- r
- m
- e
- d
-  
- i
- n
-  
- z
- h
- .
- w
- i
- k
- i
- p
- e
- d
- i
- a
-  
- a
- n
- d
-  
- i
- n
-  
- a
-  
- C
- H
- I
- B
- S
-  
- p
- a
- p
- e
- r
-  
- t
- i
- t
- l
- e
-  
- (
- 釋
- 清
- 慈
- 《
- 竹
- 林
- 三
- 祖
- 講
- 解
- 》
- )
- .
-  
- Q
- u
- e
- r
- y
-  
- b
- o
- t
- h
-  
- w
- o
- r
- d
-  
- o
- r
- d
- e
- r
- s
- .
- "
- ,
-  
- "
- 花
- 煙
- 寺
-  
- v
- s
-  
- H
- o
- a
-  
- Y
- ê
- n
-  
- t
- ự
- :
-  
- t
- h
- e
-  
- H
- a
- n
-  
- s
- o
- u
- r
- c
- e
- s
-  
- w
- r
- i
- t
- e
-  
- 煙
-  
- (
- y
- ê
- n
- ,
-  
- '
- s
- m
- o
- k
- e
- /
- m
- i
- s
- t
- '
- )
-  
- w
- h
- i
- l
- e
-  
- t
- h
- e
-  
- V
- i
- e
- t
- n
- a
- m
- e
- s
- e
-  
- r
- e
- a
- d
- i
- n
- g
-  
- i
- s
-  
- '
- Y
- ê
- n
- '
- .
-  
- T
- h
- e
-  
- f
- u
- l
- l
-  
- t
- i
- t
- l
- e
-  
- i
- n
-  
- t
- h
- e
-  
- C
- H
- I
- B
- S
-  
- p
- a
- p
- e
- r
-  
- i
- s
-  
- 安
- 子
- 山
- 竹
- 林
- 第
- 三
- 祖
- 玄
- 光
- 尊
- 者
- 詠
- 花
- 烟
- 寺
- 賦
- ,
-  
- w
- i
- t
- h
-  
- t
- h
- e
-  
- s
- i
- m
- p
- l
- i
- f
- i
- e
- d
-  
- 烟
- .
-  
- Q
- u
- e
- r
- y
-  
- 花
- 煙
- 寺
- 賦
- ,
-  
- 詠
- 花
- 煙
- 寺
- 賦
-  
- a
- n
- d
-  
- 花
- 烟
- 寺
- 賦
- .
- "
- ,
-  
- '
- 上
- 京
- 記
- 事
-  
- n
- o
- t
-  
- 上
- 京
- 紀
- 事
- :
-  
- v
- i
- .
- w
- i
- k
- i
- p
- e
- d
- i
- a
-  
- a
- n
- d
-  
- v
- i
- .
- w
- i
- k
- i
- s
- o
- u
- r
- c
- e
-  
- b
- o
- t
- h
-  
- g
- i
- v
- e
-  
- 記
- 事
-  
- f
- o
- r
-  
- T
- h
- ư
- ợ
- n
- g
-  
- k
- i
- n
- h
-  
- k
- ý
-  
- s
- ự
- .
-  
- A
-  
- r
- e
- c
- a
- l
- l
- e
- d
-  
- 紀
- 事
-  
- i
- s
-  
- a
-  
- p
- l
- a
- u
- s
- i
- b
- l
- e
- -
- l
- o
- o
- k
- i
- n
- g
-  
- e
- r
- r
- o
- r
- ;
-  
- t
- h
- e
-  
- v
- e
- r
- i
- f
- i
- e
- d
-  
- f
- o
- r
- m
-  
- s
- h
- i
- p
- s
-  
- i
- n
-  
- t
- h
- i
- s
-  
- t
- a
- b
- l
- e
- .
- '
- ]
-  
- |
-  
- d
- e
- e
- p
- _
- w
- e
- b
- _
- e
- p
- i
- g
- r
- a
- p
- h
- y
- :
-  
- N
- g
- u
- ồ
- n
-  
- t
- h
- a
- y
-  
- t
- h
- ế
-  
- c
- h
- o
-  
- k
- h
- ả
- o
-  
- s
- á
- t
-  
- t
- h
- ự
- c
-  
- đ
- ị
- a
- :
-  
- V
- i
- e
- t
- n
- a
- m
- i
- c
- a
-  
- (
- 2
- 0
- .
- 9
- 8
- 0
-  
- t
- h
- á
- c
-  
- b
- ả
- n
-  
- v
- ă
- n
-  
- b
- i
- a
- )
-  
- +
-  
- b
- ả
- n
-  
- đ
- ồ
-  
- đ
- ị
- n
- h
-  
- v
- ị
-  
- C
- S
- D
- L
-  
- +
-  
- N
- L
- V
-  
- c
- a
- t
- a
- l
- o
- g
- u
- e
-  
- 1
- .
- 7
- 7
- 8
-  
- t
- ự
- a
-  
- H
- á
- n
- -
- N
- ô
- m
-  
- +
-  
- m
- ụ
- c
-  
- l
- ụ
- c
-  
- c
- h
- o
- n
- t
- h
- i
- e
- n
- g
-  
- 1
- 2
- .
- 0
- 2
- 5
-  
- b
- ả
- n
-  
- g
- h
- i
- .
-  
- T
- ấ
- t
-  
- c
- ả
-  
- đ
- o
-  
- t
- h
- ự
- c
-  
- t
- ế
- ,
-  
- k
- h
- ô
- n
- g
-  
- s
- u
- y
-  
- t
- ừ
-  
- t
- r
- í
-  
- n
- h
- ớ
- .

## Why the "most frequent Han run near the gloss" heuristic is rejected

A cheap way to fill a glossary is: find the Vietnamese gloss in a page, then take the
most frequent Han string nearby. Measured on this corpus it produced **5 wrong answers
out of 12 attempts**, each wrong in a way that looks correct:

| Term asked for | Heuristic returned | Why it is wrong |
|---|---|---|
| Hoàng Việt văn tuyển | `皇越文選` | discovery returned 平吳大誥 (the work mentioned INSIDE the sentence) |
| Kiến văn tiểu lục | `見聞小錄` | discovery returned 撫邊雜錄 (sibling title in the same caption) |
| Vịnh Hoa Yên tự phú | `詠花煙寺賦` | discovery returned 大聖陳朝竹林頭陀靜慧覺皇調御祖佛 (author posthumous title on the same page) |
| Vũ trung tùy bút | `雨中隨筆` | discovery returned 范廷琥 (the author's name, not the title) |
| Hoa tiên ký | `花箋記` | discovery returned 石生新傳 (unrelated neighbouring entry) |

The failure mode is structural: Han strings adjacent to a title belong to whatever
else that sentence is about — the author, a sibling work, a shelfmark, a filename.
Frequency is not evidence. **Only an exact-string match of the candidate inside a
source that actually names the work counts.** That is what
`scripts/verify_han_terms.py` implements, and why `DISCOVERED` output is printed for
human judgement instead of being accepted automatically.

