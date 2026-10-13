# Hạ tầng chụp ảnh: Open WebUI tự chủ và chẩn đoán vision relay

Hai mục này là **hạ tầng để dựng ảnh**, không phải luật soạn slide, nên nằm ở
đây thay vì SKILL.md (SKILL.md có trần 100.000 char và đã gần đầy).

---

## Ảnh thao tác AI web: dựng Open WebUI tự chủ khi mọi trang công cộng bị chặn

Khi bài học cần ảnh chụp "dùng AI trên web" mà các trang công cộng đều chặn máy
tự động hoá (đã đo 10/10/2026: Copilot bắt đăng nhập, Qwen đòi xác nhận tuổi,
Duck.ai/HuggingChat/Perplexity dính CAPTCHA/403/Cloudflare, LM Arena/Blackbox
không phải bản chat miễn phí), đừng dựng ảnh giả giao diện. Dựng **Open WebUI
tự chủ** (Docker) trỏ vào endpoint AI nội bộ — giao diện web thật + AI thật nên
ảnh chụp là ảnh thao tác thật, không cần tài khoản của người dùng.

Chuỗi lỗi đã trả giá (mỗi cái là một vòng ~5 phút vì model sinh chữ chậm):

1. **Danh sách `/v1/models` của relay KHÔNG đầy đủ.** Nó chỉ liệt kê vài model
   (ở đây claude-sonnet-5, claude-opus-5 — đều hết quota), còn model cần dùng
   gọi trực tiếp vẫn HTTP 200 nhưng không có trong danh sách. Kết luận sai đã
   mắc: "không endpoint nào còn quota" vì chỉ thử model trong `/models`. Phải
   thử cả model mình thật sự cần. Cách nối: proxy mỏng phơi `/v1/models` chỉ
   chứa model đó rồi chuyển tiếp kèm streaming (Open WebUI cần SSE, không đệm).
2. **Open WebUI gửi model id RỖNG** dù đã set `DEFAULT_MODELS` và UI hiện đúng
   tên model -> relay báo "Model ' ' was not found", không có câu trả lời. Sửa ở
   proxy: ÉP `payload['model']=MODEL` trước khi forward. Proxy là tầng mình kiểm
   soát nên đó là chỗ đúng để ép.
3. **Model "thinking" gọi tool rồi TREO.** qwen3.8-max gọi `get_current_timestamp`
   để tra ngày cho loại lỗi "lỗi thời" và UI treo ở bước thực thi tool (resp kẹt
   129 ký tự 180s, proxy vẫn HTTP 200). Sửa bằng PROMPT: cấp ngữ cảnh thời gian
   ngay trong câu lệnh + ghi rõ "không dùng công cụ tra cứu bên ngoài". Đây cũng
   là bài dạy học trò: đủ ngữ cảnh thì AI không đi lòng vòng.
4. **Chụp ảnh câu trả lời: cuộn container theo % KHÔNG BAO GIỜ trúng.** Câu trả
   lời AI nằm GIỮA (sau tin nhắn người dùng chứa khối dữ liệu dài) nên 0%->phần
   người dùng, 100%->cuối câu trả lời. Phải `scrollIntoView` vào CHÍNH phần tử
   trả lời, chọn phần tử innerText DÀI NHẤT. Và selector `.prose` là KHÔNG ĐỦ —
   Open WebUI bọc trả lời trong `.chat-assistant`; bộ selector rộng
   `.chat-assistant, .prose, [class*="response"], .markdown, article` mới trúng.
5. **Mở lại chat đã lưu KHÔNG lấy được câu trả lời để chụp lại.** Open WebUI
   không commit nội dung stream vào DB ngay (assistant content = 0), nên mở lại
   chỉ render phần người dùng, `.prose` count = 0. Muốn ảnh trả lời thì phải chụp
   NGAY trong phiên đang render; không tiết kiệm quota bằng cách mở lại được.
6. **Scroll ô nhập contenteditable lên đầu bằng `Ctrl+Home`**, không bằng
   `scrollTop=0` (set scrollTop trên contenteditable của Open WebUI không ăn).
   Verify bằng cách đọc ký tự ĐẦU đang hiển thị, không tin đã cuộn.

Kỷ luật verify ảnh: exit 0 của script chụp KHÔNG phải bằng chứng ảnh đúng. Đã 6
lần checker tự động báo sai (so theo MaHS trong khi AI trả lời theo số dòng; ngưỡng
`len>5` trong khi đáp án đúng dài đúng 5 ký tự; OCR mất dấu nên tìm chuỗi có dấu
khớp 0/9). Phải đọc NỘI DUNG THẬT (OCR text hoặc vision) và đối chiếu ground truth,
không tin boolean của checker. Vision hay timeout ở bước này — OCR là phép kiểm
chính, vision để xác nhận thẩm mỹ.

---

## Chẩn đoán vision relay: lỗi account/quota trông giống lỗi model

*(mục này từng mang tiêu đề trùng với mục "Bài học phiên 2026-10-09 — chèn kịch
bản nói vào tài liệu giải thích" ở SKILL.md; hai nội dung khác nhau nhưng cùng một
tiêu đề nên đã đổi tên ở đây)*

Khi `vision_analyze` lúc được lúc không, nguyên nhân thường là **relay bốc ngẫu nhiên giữa các account** chứ không phải model sai. Đo bằng probe 1 lượt/model rồi **phân loại theo lỗi của account**, không phân loại theo model:

| Lỗi trả về | Nghĩa thật |
|---|---|
| `402 insufficient_user_quota` / "chưa kích hoạt subscription" | account hết gói → route này chết |
| `429 insufficient_quota` + ngày reset | account cạn quota tháng |
| `503 No available accounts` | **không có account nào** khai model đó (model chỉ chạy text, không nhận ảnh) |

Hệ quả: một lệnh `vision_analyze` thành công **không chứng minh** vision ổn định — nó chỉ chứng minh lượt đó bốc trúng account còn hạn. Muốn kết luận phải probe lặp ≥8 lần.

**Model sống sót chưa chắc dùng QA được.** `MiniMax-M3` probe ra `VISION_OK` nhưng 3 lần gọi chỉ 1 lần trả nội dung (2 lần trả đúng 1 ký tự `'>'`), và lần trả nội dung thì **đọc sai chữ trên ảnh** (`"màu thuẫn, xem bảng cuối mỗi dấu"` thay vì `"mâu thuẫn, xem bảng cuối phần mở đầu"`). OCR sai chữ = bằng chứng âm, nguy hiểm hơn không có bằng chứng vì nó mời ta kết luận "đạt". Trước khi tin một model làm QA trực quan, bắt nó **đọc nguyên văn một dòng ta biết trước**; đọc sai thì loại.

Khi mọi đường vision đều chết: dùng cổng đo tọa độ (PyMuPDF `span['font']`, `bbox`) để chứng minh *cấu trúc* — in nghiêng, thụt lề, không cắt trang, không tofu — và **ghi rõ trạng thái "chưa xác minh trực quan"** cho phần thẩm mỹ. Không thay bằng lời mô tả suy đoán.
