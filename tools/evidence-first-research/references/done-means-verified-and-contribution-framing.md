# "Xong" nghĩa là đã tự dò-lặp đến 0 lỗi + khung contribution đúng

Hai bài học đắt từ phiên làm bài bài bandwidth-scheduling/hội nghị C1 với người dùng. Cả hai đều là **correction lặp lại** — người dùng đã phải nhắc, nên phải nội hoá.

## 1. "Xong" = trạng thái sau khi TỰ ĐỘNG dò-lặp đến 0 lỗi — build-pass ≠ xong

**Sai lầm đã mắc:** báo "xong" ngay khi `latexmk` EXIT 0 + đủ trang. Người dùng phản ứng: *"khi nhắc dò lại thì agent mới dò và phát hiện lỗi sai, thì làm sao người dùng yên tâm được?"* và *"agent khi làm xong thì TỰ ĐỘNG DÒ LẠI, lặp lại lặp lại đến lúc production-ready/submit-ready thì mới gọi là xong."*

**Vì sao build-pass là "xong giả":** trình biên dịch LaTeX KHÔNG đọc nghĩa. Cả một lớp lỗi *ngữ nghĩa* lọt qua build sạch:
- Hàm mục tiêu phát biểu ở System Model (`min M̂_t`) mâu thuẫn với selector/code thật (`min L̂_t`).
- Abstract nói "about half the bandwidth", Conclusion nói "one third" — cùng tả một tỉ số 1.37/3.00.
- Số trong văn xuôi lệch số trong bảng/CSV.
- Thuật ngữ sai bản chất dữ liệu ("measured" cho ERA5 reanalysis).

**Quy trình đúng — cổng tự động chạy lại được (không dựa mắt người):** dựng `verify.py` chạy nhiều lần, lặp sửa đến khi cả 3 gate xanh + exit 0:
1. **Build gate** — `latexmk` EXIT 0, đúng số trang, 0 undefined ref, 0 overfull box.
2. **Semantic gate** — số văn xuôi ↔ bảng/CSV; abstract ↔ conclusion nhất quán; mọi `\ref`/`\label` khớp; mọi `\cite` có entry + không entry rác.
3. **Hallucination gate** — mọi reference resolve tới nguồn thật (Crossref DOI + arXiv API), tiêu đề khớp.

Bài học phụ: **chính cái verifier cũng phải tự dò** — lần đầu `verify.py` gọi một hàm đã đổi tên (`dump_refs()` cũ) và tự crash. Chạy verifier trên chính nó, sửa, chạy lại đến exit 0 mới tin.

Chỉ khi cả 3 gate xanh, ĐỒNG THỜI, một lần chạy, mới được nói "xong". Không tách "build lần này, verify lần khác".

## 2. Contribution = thứ mình ĐỀ XUẤT trong Methodology — KHÔNG phải reproducibility, KHÔNG phải empirical finding

**Sai lầm đã mắc:** viết bullet contribution thứ 3 là *"fully reproducible replay evidence..."*. Người dùng: *"Contribution là cái gì mình đóng góp cơ mà? Còn reproducible là cái buộc phải có để minh chứng."* Rồi agent thử sửa thành "empirical finding" — người dùng lại chỉnh tiếp: *"contribute là mấy cái được trình bày trong methodology ấy."*

**Phân loại đúng (đừng lẫn phương tiện với đóng góp):**

| Loại | Bản chất | Đặt ở đâu | Có phải contribution? |
|---|---|---|---|
| **Cơ chế** mình xây | urgency score, luật bài bandwidth-scheduling-PD | Methodology | ✅ CÓ |
| **Lý thuyết** mình chứng minh | dẫn xuất primal-dual, bound O(1/T) | Methodology | ✅ CÓ |
| **Phát hiện thực nghiệm** | saving tăng theo scale, raw-p > VoU | **Evaluation** | ❌ KHÔNG (là kết quả) |
| **Reproducibility** | mọi số tái lập từ code | 1 câu "We validate..." | ❌ KHÔNG (là nghĩa vụ minh chứng) |

**Quy tắc:** danh sách "The contributions are:" chỉ liệt kê **cái mình làm ra / chứng minh, nằm trong phần phương pháp**. Reproducibility hạ xuống một câu khẳng định riêng sau danh sách ("We validate X on Y; every reported number is regenerated end-to-end from public data by the released code"). Kết quả/phát hiện để ở Evaluation, không nhồi vào contribution.

## 3. Đóng gói bản sạch + bản review từ MỘT nguồn nội dung

Khi người dùng muốn "1 bản main.tex sạch + 1 bản highlight để đọc": KHÔNG nhân đôi nội dung (sẽ lệch nhau). Dùng chung một bộ `sections/`, chỉ khác preamble:
- `main_review.tex`: `revblock` = hộp vàng (mdframed), `\rev` = `\hl` (soul).
- `main.tex` (nộp): `revblock` = môi trường no-op (`\newenvironment{revblock}{}{}`), `\rev{#1}` = `#1`. Không nạp soul/mdframed.

Sửa nội dung ở `sections/` thì cả hai bản tự đồng bộ. Verify bản sạch bằng **đếm pixel vàng thật trong PDF render = 0** (grep chữ "revblock"/"yellow" trong .tex sẽ khớp nhầm comment + dòng định nghĩa no-op → false positive; phải render + đếm pixel).

Soul pitfall: `\hl` vỡ với `\cite`/`\ref`/display-math (`\soulregister{\ref}` gây đệ quy vô hạn → TeX capacity exceeded). Dùng môi trường block-level `mdframed` (revblock) cho đoạn có cite/ref/math, chỉ để `\hl` cho text thuần.

## 4. Method thử-và-THUA ⇒ ablation, KHÔNG Future Work

Khi một hướng (VoU/CVaR) đã thử và thua trong ablation: KHÔNG gắn "Proposed", cũng KHÔNG đưa vào Future Work — vì "đã thử thua rồi lại bảo tương lai sẽ làm" là tự mâu thuẫn (người dùng chỉ ra). Giữ nó làm **điểm so sánh trong ablation** (bằng chứng "đã cân nhắc và loại"), và chỉ để lại cite của người khác ở Related Work nếu có. Đây là điểm mạnh về tính trung thực, không phải điểm yếu.
