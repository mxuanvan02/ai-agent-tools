# Peer-Review Revision Round (revise bản thảo của chính mình theo review)

Dùng khi: người dùng gửi manuscript + peer review (PDF/DOCX/text) và yêu cầu "revise theo peer review". Đã áp dụng thành công cho bài bandwidth-scheduling hội nghị C1 (submission 40, 2026-09): 6 điểm review, 4 thí nghiệm mới, clean PDF đúng 8 trang, repo public sync.

## 0. Định vị review — KHÔNG BAO GIỜ ĐOÁN

1. Quét `~/.hermes/cache/documents/` (file mới nhất), `/home/<user>/reviews/`, `.hermes/artifacts/`, và annotations trong PDF manuscript (`page.annots()`).
2. Cẩn thận file review của BÀI KHÁC trong cache (VD: bài của người phản biện khác = bài LegalQA người dùng đi review hộ, không phải bài của người dùng).
3. Không tìm thấy → hỏi người dùng; thiếu bằng chứng = BLOCKED, không suy diễn nội dung review để "sửa bừa".

## 1. Reproduce TRƯỚC, viết SAU

- Clone repo public của bài → chạy pipeline → diff từng bảng với bản nộp (byte-for-byte hoặc dung sai 4 chữ số). Khớp = pipeline đúng; lệch = tìm pipeline thật (VD: bài bandwidth-scheduling có 2 pipeline, bản nộp dùng pipeline ERA5 chứ không phải pipeline greenhouse cũ).
- Mọi con số trả lời reviewer phải đo lại từ code (có CI, có test ghép cặp). Không trích từ trí nhớ model.
- Cross-check cứng: script sinh bảng phải **abort nếu drift** khỏi số đã nộp. Nhân tiện sẽ phát hiện bug cũ (VD: hàng no_dev/no_aoi tính trên basis VoU trong khi caption nói deployed basis) → sửa và khai báo minh bạch trong letter.

## 2. Phân loại từng điểm review

(a) Lỗi trình bày — sửa + verify programmatic. (b) Trả lời được bằng số liệu đã có — trích đúng CI/p-value. (c) Cần thí nghiệm mới — chạy ngay (deterministic, seeded), ĐẶC BIỆT khi reviewer chất vấn thành phần lõi:
- **Ablate TẤT CẢ kênh liên quan**, không chỉ kênh reviewer gọi tên (bài bandwidth-scheduling: reviewer hỏi risk trong ranking → đo cả risk trong budget rule và miss surrogate).
- **Thêm regime khắc nghiệt hơn** — thứ tự reviewer giả định có thể ĐẢO (extreme burst: full polling hóa ra kém an toàn hơn adaptive vì phơi nhiều packet vào loss). Thí nghiệm mới có thể là đòn phản biện mạnh nhất.

## 3. Negative result — không phòng thủ

Khi reviewer ĐÚNG (component không giúp): (1) thừa nhận thẳng trong letter + manuscript; (2) tìm **lý do cấu trúc** (VD: replay deterministic μ=x nên p và δ mã hóa cùng tín hiệu → risk channel redundant); (3) chỉ rõ gain thật đến từ đâu (PD adaptation + dev/AoI vẫn thắng mọi baseline kể cả bỏ hết risk); (4) reframe thành *design hypothesis* cho điều kiện field, không claim là kết quả; (5) đồng bộ abstract/conclusion/limitations. Reviewer tôn trọng điều này hơn ngụy biện.

## 4. Tracked changes LaTeX (2 bản, cùng sections/)

- `main.tex` = clean (mọi marker là no-op), `main_review.tex` = markup visible. Cùng `\input{sections/...}`.
- Marker theo vòng: `revblock` (mdframed vàng, vòng 1), `revblockb` (`\begingroup\color{blue}...\endgroup`, vòng 2 — PHẢI là color group chứ không phải box vì dùng được CẢ inline lẫn block), `\revdel` (`\textcolor{red}{\st{#1}}`, text bị xóa).
- **CẤM nest** `revblock` trong `revblock` (mdframed vỡ). Khi patch thay nội dung đoạn đã wrap, thay CẢ cặp begin/end.
- Conclusion/decklarations nằm trong main*.tex (không qua sections/) → sau khi sửa main.tex phải **sync sang main_review.tex** (extract `\section{Conclusion}`...`\section*{Data...}` và replace).
- Verify render bằng PDF span-color scan: đếm từ xanh (round mới), từ đỏ gạch (revdel), box vàng (round cũ) — không tin "chắc là được".

## 5. Page limit — phương án C (người dùng đã duyệt thành chuẩn)

Manuscript chỉ giữ **số liệu then chốt** (~5 câu/điểm); lập luận đầy đủ chuyển sang `RESPONSE_TO_REVIEWERS.md` (không giới hạn trang). Quy trình: nén từng vòng → build → đo trang SAU MỖI vòng (không nén mù). Đòn cuối hợp lệ: bibliography `\footnotesize`→`\scriptsize`, figure width −0.05. **Vẫn tràn → hỏi người dùng, KHÔNG tự cắt nội dung khoa học.** (Bản tracked-changes dài hơn clean là bình thường — không phải bản nộp.)

## 6. Figure fix — verify bằng bbox, không bằng mắt

- Sửa layout (leader lines, dời label) trong script generator, số liệu vẫn đọc từ CSV (không hardcode).
- Verify: PyMuPDF extract text spans size ≤ 7.9 → pairwise bbox intersection > 0.5px² = collision. Báo cáo "N collisions → 0". Cách này chạy được cả khi vision API down và chính xác hơn nhìn.

## 7. Response letter

- Cấu trúc: quote comment → Response → bảng số → "Summary of changes" đánh số theo manuscript.
- **Mọi số trong letter phải verify trước khi gửi** (suýt viết "3 collisions" khi đo thật là 4).
- Nếu letter hứa "released with the revision" → PHẢI push thật trước khi bàn giao.

## 8. Sync repo public

- Chạy thử generator mới: output phải giống hệt file trong manuscript (diff).
- `reproduce.sh`: script sinh bảng MỚI phải chạy SAU script legacy (nếu không bị ghi đè lại bảng cũ). `bash -n` trước khi commit.
- Push: HTTPS có thể fail khi secret-masking bóp méo `$(gh auth token)` trong lệnh → dùng SSH `git@github.com:...`. Verify sau push: SHA local=remote, `gh api` tree đủ file, curl raw.githubusercontent grep nội dung mới.

## 9. Bàn giao qua Discord

Gửi TỪNG file với `MEDIA:<abs_path>`, target `discord:<chat_id>:<thread_id>`, chỉ coi là xong khi `success=true` + `message_id`. Bộ chuẩn: clean PDF, tracked-changes PDF, response letter (MD), package zip (source + PDF + letter + script/CSV mới).
