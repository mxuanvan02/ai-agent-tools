# Thesis Architecture — Canonical Model

Canonical reference: a completed institutional research report (4 chapters,
~90 pages of Vietnamese prose, LaTeX source built with `book` 12pt, XeLaTeX +
polyglossia). Every structural claim below is read off that source, not off a
genre description.

A thesis is not a long paper. A paper compresses one claim into the fewest pages a
reviewer will accept; a thesis must **carry** that claim across chapters a
multi-disciplinary committee reads in order. The diagnostic is one sentence per
chapter — if either line is unwritable, the chapter is not load-bearing:

- *what chapter n takes from chapter n−1*
- *what chapter n hands to chapter n+1*

## Verified skeleton

Front matter, in the order `main.tex` actually includes it:

1. `Covers/cover` — bìa, khung viền kép vẽ bằng TikZ (1.5pt ngoài, 1pt trong)
2. `Covers/inner_cover_project` — bìa phụ, có xác nhận cơ quan chủ trì + chủ nhiệm
3. `Covers/team_members` — danh sách thành viên tham gia
4. `Covers/camdoan` — lời cam đoan
5. `\frontmatter`: Mục lục → Danh mục bảng, biểu → Danh mục hình ảnh → **Danh mục thuật toán**
6. `Chapter/information_VN` — THÔNG TIN KẾT QUẢ NGHIÊN CỨU, 6 mục đánh số
7. `Chapter/information_EN` — cùng 6 mục, bản tiếng Anh

Body:

8. `\part{Mở đầu}` → `Chapter/modau` — **6 section**, xem dưới
9. `\part{Nội dung}` → `noidung_chap1..4` (chương 4 có trong source nhưng bị
   comment ở `main.tex`; bật lại bằng cách bỏ `%`)
10. `\part{Kết luận}` → `Chapter/ketluan`
11. `\bibliographystyle{IEEEtran}` + `\bibliography{references}`
12. `\appendix` → `\part{Phụ lục}` → `Chapter/publication` (3 chương: Thuyết minh
    đề tài, Sản phẩm khoa học, Sản phẩm đào tạo)

Two features of this skeleton are easy to omit and both are load-bearing. The
**Danh mục thuật toán** exists because the report carries pseudocode; a thesis with
algorithms but no list of them fails a format check. The **information_VN/EN block**
is an institutional reporting requirement, not a decorative abstract — it must state mã số, chủ
nhiệm, thời gian, mục tiêu, tính mới, kết quả, sản phẩm, và khả năng ứng dụng, and
the two language versions must agree item by item.

## Mở đầu: the six sections, in order

1. `Tổng quan tình hình nghiên cứu` — with `Trên thế giới` and `Trong nước` as
   subsections. Not a bibliography read aloud: each source gets its **advantage and
   its limitation**, and the limitation is what the next section needs.
2. `Tính cấp thiết của đề tài`
3. `Mục tiêu nghiên cứu` — `Mục tiêu tổng thể` (one sentence) + `Các mục tiêu cụ
   thể` (itemized, each one testable)
4. `Đối tượng và phạm vi nghiên cứu` — `Đối tượng` + `Phạm vi`
5. `Nội dung nghiên cứu`
6. `Cách tiếp cận và phương pháp nghiên cứu` — `Cách tiếp cận`, `Phương pháp
   nghiên cứu`, `Các bộ dữ liệu thực nghiệm`, `Các tiêu chí đánh giá hiệu suất`

The order is not arbitrary and must not be reordered. Tổng quan establishes what is
known; Tính cấp thiết converts that into what is missing; Mục tiêu states what will
be done about it; Đối tượng/Phạm vi bounds the claim before any method is named;
Nội dung lists the work; Cách tiếp cận explains how. A draft that opens with Tính
cấp thiết has no evidence for its own necessity.

`Tính cấp thiết` is the weakest section in most Vietnamese theses because it argues
importance instead of necessity. It needs four links: a practical problem with
evidence; the scientific problem that creates; what remains unresolved in existing
work; which part this study settles and which it explicitly does not.

## Chapter pattern

Every content chapter in the canonical source closes with a numbered section
`Tiểu kết chương N`. That section is not a summary of topics — it states what the
chapter **settled** and what it now **forces** the next chapter to do. A Tiểu kết
that repeats the section headings is duplication; one that states the settled result
and the resulting obligation is integration.

Two chapter shapes appear in the source, and both are legitimate:

- **Theory chapter** (`noidung_chap1`): `Protein` → `Dự đoán tương tác protein` →
  `Tiểu kết chương 1`. Background, then the problem class, then the hand-off.
- **Contribution chapter** (`noidung_chap2..4`): `Mở đầu` → `Phương pháp đề xuất` →
  `Kết quả` (or `Kết quả và Thảo luận`) → `Tiểu kết chương N`. Each contribution
  chapter is a self-contained study with its own opening, so a committee member can
  read chapter 3 without chapter 2.

Note the second shape: a contribution chapter **reopens** with its own `Mở đầu`
rather than relying on the thesis-level Mở đầu. That is what makes multi-paper
theses readable, and it is why chapter numbering restarts cleanly after
`\part{Nội dung}` with `\setcounter{chapter}{0}`.

## Kết luận: two unnumbered sections

`ketluan.tex` uses `\section*`, so the two parts carry no numbers and no TOC
entries:

- `Đánh giá kết quả nghiên cứu` — the answers, in the order Mục tiêu stated them
- `Một số tồn tại và hướng nghiên cứu tiếp theo` — itemized limitations, each with
  the consequence attached, then the next steps

Using `\section*` is deliberate: numbered conclusion sections would appear as
chapter-level items in the TOC and read as a fifth chapter. Do not "fix" it.

## Paper to thesis, by function

| Function | Paper | Thesis |
|---|---|---|
| Prior work | one Related Work section, competing studies only | a full section with Thế giới / Trong nước split, each source ending at a limitation |
| Method | enough to reproduce | enough to reproduce **and** why this design over the rejected alternatives |
| Results | the subset answering the question | the fuller set, including the runs the committee will ask about |
| Discussion | comparison with cited literature | that plus practical implication and warranted recommendation |
| Claim | narrow, defensible | equally narrow, and must also cover the parts not published as papers |

Expanding a paper by adding words to each section raises length without raising
function. A Methods section stretched to thirty pages fails the same way an annotated
bibliography does.

## Prose gates specific to this genre

**Chapter opening.** One short paragraph on the chapter's function. Not
`Chương này gồm ba phần: ...` — that is the TOC read aloud.

**Cross-chapter terminology.** One term per construct for the whole document. A
construct renamed between chương 1 and chương 3 reads as two constructs, and the
committee will ask which one the results support.

**Vietnamese third person.** `nghiên cứu được tiến hành`, not `tôi`/`chúng tôi`.
The canonical source states this rule explicitly and enforces it in prose.

**No new claim in Kết luận.** A conclusion that introduces an implication absent
from the results has widened the thesis after the evidence stopped.
