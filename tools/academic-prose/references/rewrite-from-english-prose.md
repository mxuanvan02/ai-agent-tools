# Rewrite from English: finding and fixing translated prose

When the user says prose "nghe English quá" / "sounds translated", the problem is
structural, not lexical. Swapping individual words does not fix it; rewriting from
meaning does. This file is the procedure.

## The machine-rhythm tell

English-to-Vietnamese translation produces uniform sentence lengths because the
translator maps one English clause to one Vietnamese clause. A human Vietnamese
writer varies: short for emphasis, long for elaboration.

**Measured tell**: three consecutive sentences at 32, 32, 32 words. That is not
a stylistic choice; it is a machine signature. The fix is not swapping words —
it is restructuring so the rhythm varies: [29, 31, 34, 9, 41, 15, 18, 42, 13, 18].

Count sentence lengths before and after rewriting. If the lengths are all within
±3 words of each other, the rewrite has not broken the machine rhythm.

## The calque hunt list

These are structural calques — grammatical but not idiomatic Vietnamese — that
survive word-level editing. Hunt them by pattern, not by individual word:

| Pattern | Signal | Fix |
|---|---|---|
| `Nghiên cứu dựng X` | calque of "we build" | `Chúng tôi xây dựng X` or restructure |
| `cho/để <actor> tối ưu` | calque of "allowing X to optimize" | `mô phỏng <actor> tối ưu` |
| `dời ... mà vẫn làm tăng` | calque of "shifting ... while still increasing" | split into two clauses |
| `Vật lý không kiểm soát được` | calque of "Physics cannot control" | `Mô hình vật lý không ràng buộc được` |
| `Theo thứ tự từ trái sang phải:` | calque of "from left to right:" | `Ba đại lượng này theo thứ tự là` |
| `... có điểm mù:` | colon introducing explanation (English habit) | full stop, then new sentence |
| `định lượng được cái giá của X:` | calque of "we quantify the cost of X:" | `định lượng cái giá của X, đó là` |

## Semantic contradiction detection

Structural gates (word count, calque count, keyword presence) pass text that
contradicts its own argument. The gate that catches this is reading the claim
against its evidence.

**Measured instance**: a limitations section argued that device anchoring has a
blind spot, then wrote "phép neo vẫn phát hiện được vì bản ghi khớp nhau" —
matching records means the anchor does NOT detect anything, which contradicts
the limitation being stated. The fix: "bản ghi khớp nhau nên phép neo không
phát hiện được, dù lượng nước thực tế vào ruộng khác hẳn lượng đã bơm."

**Rule**: after any rewrite, read each paragraph's claim against the sentence
that follows it. If the following sentence's evidence would make the claim
false, the rewrite introduced a contradiction. Fix the contradiction, not the
style.

## The rewrite procedure

1. **Hunt** by pattern: grep for the calque list above, count sentence lengths,
   flag any run of 3+ sentences within ±3 words of each other.
2. **Rewrite from meaning**, not from the English source: state what the sentence
   claims in Vietnamese, then check the claim against the evidence in the same
   paragraph.
3. **Break rhythm**: vary sentence lengths deliberately. Short for emphasis
   (5–15 words), long for elaboration (30–45 words).
4. **Preserve hedges**: if the original says "giả định đúng", the rewrite must
   keep that assumption. Losing a hedge to save words is a stance upgrade.
5. **Verify numbers**: every quantity in the original must appear in the rewrite.
   Grep for each number after the edit.
6. **Verify keywords**: if the venue requires keywords in the abstract, check
   each one appears verbatim in the rewritten text.
7. **Rebuild and count on the PDF**: source-side word counts disagree with
   rendered counts when math mode is present.
