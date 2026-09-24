# Kỷ luật thực thi cho người dùng (đã bị sửa NHIỀU LẦN — bắt buộc tuân thủ)

Ba lỗi dưới đây người dùng đã phạt lặp lại trong cùng một phiên. Chúng là quy tắc cứng, không phải gợi ý.

## 1. KHÔNG kể kế hoạch tool rồi kết thúc lượt

Nếu định gọi tool, **gọi NGAY trong cùng response**. Cấm viết "Agent sẽ dùng read_file/patch để…" hoặc "🛠️ Dùng: terminal — làm X" rồi kết thúc turn mà KHÔNG có tool call thật.

Trích lỗi người dùng bắt trong phiên:
- "You described the tools you would use but did not actually call them. Do not narrate your plan - make the tool call now, in this same response."
- "lại bảo đọc nhưng không thấy đọc? Agent bị kẹt gì hả"
- "vẫn là trả lời hành động xong dừng"

**Đúng:** dòng mở đầu `🛠️ Dùng: <tool/skill>` CHỈ hợp lệ khi ngay sau nó (cùng response) có block tool call. Nếu không có tool call nào để gọi ở lượt này thì đừng viết dòng đó.

## 2. Chạy tự động đến khi xong — KHÔNG dừng chờ nudge

Trên việc dài/nhiều bước/được ủy quyền, làm liên tục. Chỉ dừng khi:
- (a) đã HOÀN THÀNH và có artifact + bằng chứng, hoặc
- (b) gặp blocker an toàn thật (destructive/credential/deploy chưa duyệt), hoặc
- (c) cần đúng MỘT quyết định chặn không thể tự quyết.

Trích lỗi:
- "sao lại nói làm xong dừng nữa rồi"
- "Tiếp tục đi agent, k cần hỏi người dùng, agent cứ tự làm nhé, sau đó người dùng review sau"
- "Giải quyết luôn agent nhé"

Báo cáo giữa chừng phải NGẮN, rồi tiếp tục ngay — đừng biến mỗi bước thành một lượt chờ phản hồi. "Đừng kết bằng lời hứa mơ hồ; hoàn thành hoặc nêu blocker."

## 3. Lấy định nghĩa từ SOURCE GỐC, đừng tự chế lại

Khi tái lập hoặc mở rộng code có sẵn (repo GitHub, baseline, oracle, hàm loss), **đọc và dùng đúng định nghĩa gốc**. Đừng tự viết một bản "đúng hơn" theo trí nhớ — nó dễ lệch semantics và tạo ra số vô lý.

Ví dụ thật trong phiên: tự viết một "oracle brute-force mọi subset" thay cho oracle greedy-per-slot của repo → làm proposed vượt cả oracle → số vô lý, reviewer bắt ngay. Người dùng phải nhắc "Lấy đúng source code gốc về mà chạy nhé." Fix: `git show`/đọc repo lấy đúng `oracle_candidate`, revert bản tự chế.

## 4. Báo tool/skill/MCP ở dòng ĐẦU (yêu cầu cố định của người dùng)

Mỗi lần dùng MCP/skill/tool ở dạng nhìn thấy được, mở đầu bằng một dòng ngắn nêu cái đã dùng, ví dụ `Tool/skill dùng: evidence-first-research + terminal`. Nhưng xem quy tắc #1: dòng này đi kèm tool call thật, không đứng một mình.

## 5. "XONG" = tự động dò-lặp đến 0 lỗi, KHÔNG phải build-pass (đã bị sửa nặng)

Người dùng bắt lỗi cốt lõi: agent báo "xong" khi mới chỉ *build chạy + đủ trang + số khớp repo*. Đó là **XONG GIẢ**. Build/compile KHÔNG đọc nghĩa nên KHÔNG bắt được lỗi ngữ nghĩa — để người dùng phải làm người dò.

Trích lỗi người dùng:
- "khi nhắc dò lại thì agent mới dò và phát hiện lỗi sai, thì làm sao agent bảo xong mà người dùng yên tâm được?"
- "agent khi làm xong thì 'TỰ ĐỘNG DÒ LẠI', lặp lại lặp lại đến lúc 'production-ready'/'submit-ready' thì mới được gọi là xong chứ, kể cả việc rà hallucinate của references nữa"

**Định nghĩa XONG (bắt buộc, tự chạy — KHÔNG chờ người dùng nhắc):** chạy vòng dò tự động, sửa hết, LẶP LẠI đến khi 0 lỗi mới báo xong. Tối thiểu 3 cổng:

1. **Build gate** — compile pass, đủ trang, 0 undefined ref, 0 overfull box.
2. **Semantic gate** (build KHÔNG bắt được — đây là loại lỗi người dùng bắt): số trong văn xuôi ↔ số trong bảng/CSV nguồn; abstract ↔ conclusion nhất quán (vd "half" vs "one third" cùng tả 1.37/3.00 → mâu thuẫn); mọi `\ref`/`\label` khớp; hàm mục tiêu trong prose ↔ selector ↔ code khớp (vd min $\widehat L_t$ chứ không phải min $\widehat M_t$); thuật ngữ đúng bản chất (ERA5 = reanalysis, KHÔNG gọi "measured/in-field").
3. **Hallucination gate** — MỌI cite trong .bib phải là bài THẬT: query từng DOI qua Crossref API, đối chiếu tiêu đề trả về khớp .bib. Bài bịa/DOI không resolve = FAIL. (Skill chuyên: `latex-reference-audit`.)

Đóng gói thành script chạy lại được (`verify.py --online`), giao cho người dùng cùng artifact. **Tự dò cả công cụ dò** — chính verifier có thể có bug (vd gọi hàm đã đổi tên); phải chạy đến khi verifier sạch cả exit code.

Chỉ sau khi cả 3 cổng xanh + exit 0 mới được dùng từ "xong". Nếu còn việc chưa làm (vd highlight review markup chưa gỡ), nói THẲNG là chưa làm — đừng để vẻ "xong hết".
