# Thesis Section Layouts — Measured

Every number here is counted from a completed institutional research report's LaTeX
source, words of running prose with markup excluded. Use them as budgets, not quotas —
but treat a section at 3× or 1/5× these numbers as a signal, because the canonical
report is internally consistent.

## The abstract is a form, not prose

The canonical report has **two** things that could be called an abstract, and only one
is active. This is the most misleading thing about the genre.

**`Chapter/tomtat.tex` — 296 words, ONE paragraph, 10 sentences, no citations — is
commented out** in `main.tex` (`% \include{Chapter/tomtat}`). Do not treat it as the
model. Its defect is visible on reading: sentences 1–6 describe the research field in
general (`Phương pháp này sử dụng học máy để dự đoán…`, `Các kỹ thuật mã hóa phổ
biến…`), not what this study found. No result with a quantity, no method specific to
the work, no bounded claim. It is a topic summary, and it is disabled for a reason.

**`Chapter/information_VN.tex` + `information_EN.tex` — the active front matter.**
A numbered form, ~300 words, no citations, no tables, six items in fixed order:

1. `Thông tin chung` — 1.1 Tên đề tài, 1.2 Mã số, 1.3 Chủ nhiệm, 1.4 Cơ quan chủ trì,
   1.5 Thời gian thực hiện
2. `Mục tiêu nghiên cứu` — one sentence, copied verbatim from Mục tiêu tổng thể
3. `Tính mới và sáng tạo` — two labelled lines: `Tính mới:` and `Tính sáng tạo:`
4. `Các kết quả nghiên cứu thu được` — prose, with the parenthetical instruction
   `(nêu vắn tắt các kết quả chính ứng với các nội dung nghiên cứu, gồm thông tin,
   số liệu và đánh giá)`
5. `Các sản phẩm của đề tài` — 5.1 Sản phẩm khoa học, 5.2 Sản phẩm đào tạo,
   5.3 Sản phẩm ứng dụng, 5.4 Sản phẩm khác. Counts are written
   `01 / (01 theo thuyết minh đề tài)`, i.e. delivered / committed
6. `Các đóng góp, khả năng ứng dụng và phương thức chuyển giao` — begins
   `Khả năng ứng dụng: Tốt`

Two rules follow. VN and EN must agree **item by item**, not merely in tone. And the
product counts are a claim against the proposal, so delivered-vs-committed mismatch is
visible to a reviewer without any prose analysis.

A journal-style prose abstract inside a thesis still uses the six-move order in
[The opening sentence gate](abstract-opening-sentence-gate.md) — but that is a
different artifact from this form, and a thesis usually needs both.

## Mở đầu: measured budget, six sections

| Section | Paragraphs | Words | Shape |
|---|---|---|---|
| Tổng quan — Trên thế giới | 2 | 1 339 | one source per cluster: method → advantage → limitation |
| Tổng quan — Trong nước | 6 | 824 | grouped by direction, opens `Trong khuôn khổ của đề tài này, chúng tôi quan tâm…` |
| Tính cấp thiết | 4 | 403 | field → what feature extraction is → why it is the bottleneck |
| Mục tiêu tổng thể | 1 | 23 | exactly one sentence |
| Các mục tiêu cụ thể | 1 | 102 | `itemize`, 3 items, each testable |
| Đối tượng nghiên cứu | 1 | 40 | one sentence, `bao gồm:` + list |
| Phạm vi nghiên cứu | 1 | 80 | two sentences: covered, excluded |
| Nội dung nghiên cứu | 1 | 206 | one paragraph, comma-separated work items |
| Cách tiếp cận | 1 | 88 | one sentence plus elaboration |
| Phương pháp nghiên cứu | 1 | 565 | `itemize` of named methods, each glossed |
| Các bộ dữ liệu thực nghiệm | 4 | 241 | count first (`10 bộ dữ liệu`), then provenance |
| Các tiêu chí đánh giá | 7 | 177 | one metric per paragraph, formula inline |

Total ≈ 4 000 words. Three ratios matter: Tổng quan is **half** the whole Mở đầu;
Mục tiêu tổng thể is **one sentence**; every subsection under Đối tượng and Mục tiêu
is a single paragraph, never an essay.

Each section's opening sentence names its own object immediately — `Đối tượng nghiên
cứu của đề tài bao gồm:`, `Để huấn luyện và kiểm chứng các mô hình, đề tài sử dụng 10
bộ dữ liệu…`. None opens with `Trong chương này…` or with a definition of the field.

## Contribution chapter: measured internal layout

| Part | Ch.2 (DeepCF-PPI) | Ch.3 (embedding) | Ch.4 (Hilbert) |
|---|---|---|---|
| Mở đầu | 2 ¶, 124 w | 3 ¶, 1 130 w | 5 ¶, 677 w |
| Phương pháp đề xuất | 4 subsections, 3 280 w | 2 subsections, 1 912 w | 3 subsections, 1 320 w |
| Kết quả (và Thảo luận) | 6 subsections, 3 669 w | 5 subsections, 2 340 w | 3 subsections, 1 384 w |
| Tiểu kết chương N | 1 ¶, 265 w | 1 ¶, 282 w | 1 ¶, 164 w |

Method outweighs results in ch.2 and ch.4, roughly equal in ch.3 — the normal shape
when the contribution **is** the method. If results outweigh method by more than 2:1,
either the method section is under-specified or the results chapter is carrying
discussion that belongs elsewhere.

Floats are distributed, not pooled: ch.2 has 8 figures, 6 tables, 7 equations, 0
algorithms; ch.3 has 4 figures, 2 tables, 7 equations, 4 algorithms; ch.4 has 2
figures, 3 tables, 2 equations, 0 algorithms. Ch.3's four algorithms are why the
report ships a `Danh mục thuật toán` — a chapter with pseudocode and no algorithm
list fails the front-matter check.

## Tiểu kết chương: measured

One paragraph, 164–282 words in the contribution chapters. Chapter 1's is longer
(589 w, 4 paragraphs) because a theory chapter closes by consolidating several
constructs.

The move is fixed: *what this chapter established* → *what that now forces*. It never
lists section titles back. A Tiểu kết that reads as a table of contents in prose is
duplication; the test is whether the last sentence states an obligation the next
chapter must meet.

## Kết luận: two unnumbered sections

| Section | Paragraphs | Words | Shape |
|---|---|---|---|
| Đánh giá kết quả nghiên cứu | 3 | 537 | answer → generalization claim → the specific technique and its limit |
| Một số tồn tại và hướng nghiên cứu tiếp theo | 1 + `itemize` | 339 | `Mặc dù…vẫn còn một số tồn tại` → 3 items → next steps as `(1)…(2)…` |

Both use `\section*`, so neither appears numbered in the TOC. Paragraph 1 of Đánh giá
opens on the field (`Các phương pháp dựa trên học máy…đã được phát triển rộng rãi`),
then narrows to `Trong nghiên cứu này, …chúng tôi đã đề xuất`. Copy that two-beat
opening: field state, then this work's position. Opening directly on `chúng tôi đã đề
xuất` reads as if the field were empty.

Each limitation carries its consequence — `hiệu suất của mô hình vẫn phụ thuộc lớn vào
chất lượng và sự đa dạng của dữ liệu huấn luyện` is followed by what that prevents
concluding. A bare `dữ liệu còn hạn chế` is not a limitation.

## Checks before writing

1. Is the front matter the **form** (information_VN/EN), a prose abstract, or both?
   An institutional research report needs the form; a degree thesis usually needs both.
2. Does Mục tiêu tổng thể fit one sentence, and does each item under Các mục tiêu cụ
   thể map to one chapter?
3. Is Tổng quan roughly half of Mở đầu, with each source ending at a limitation?
4. Does every contribution chapter reopen with its own Mở đầu?
5. Does every chapter close with a Tiểu kết stating an obligation, not a summary?
6. Does Kết luận answer the objectives in the order stated, with no new claim?
