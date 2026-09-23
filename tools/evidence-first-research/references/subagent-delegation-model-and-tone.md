# Điều phối subagent cho manuscript/research (model override + văn phong)

## Ép model cho `delegate_task`
- `delegation.model` / `delegation.provider` trong `config.yaml` set qua `hermes config set` **không áp dụng ngay cho subagent đang chạy trong session hiện tại** — nó chỉ có hiệu lực từ session/turn mới (giống mọi thay đổi config Hermes khác). Set xong trong session cũ rồi gọi `delegate_task` ngay trong session đó vẫn có thể ra model cũ.
- LUÔN verify bằng field `model` trong kết quả trả về của `delegate_task` (`results[].model`), đừng giả định set config = đã đổi. Nếu field đó vẫn là model cũ, báo thật với người dùng là override chưa ăn, đừng báo "đã set" như đã xong.
- Nếu cần đổi model NGAY trong lượt hiện tại mà set config không ăn, cân nhắc: (a) báo người dùng cần 1 lượt/session mới để override có hiệu lực, hoặc (b) dùng `model` param trực tiếp trong lời gọi nếu tool hỗ trợ per-call override (kiểm tra schema `delegate_task` — nếu không có param model per-task thì chỉ còn cách (a)).

## người dùng phong khi điều phối subagent cho người dùng (research/manuscript)
Người dùng không muốn giọng "nói chuyện" lặp mỗi lượt khi agent chỉ đóng vai điều phối (dispatch subagent, không tự code). Cụ thể:
- Tránh: "agent sẽ...", "nhé", "gửi người dùng xem", các câu mở đầu kiểu tường thuật ý định.
- Thay bằng: log điều phối ngắn — dispatch cho ai/model gì, đã verify gì (build log, số liệu, exit code), bước kế tiếp là gì. Đọc như status update của một pipeline, không phải hội thoại.
- Vẫn PHẢI giữ yêu cầu báo tool/skill/MCP ngay câu đầu (tên + mục đích) — hai yêu cầu này không mâu thuẫn: câu đầu báo tool ngắn gọn, phần thân là log kết quả, không chèn filler xuyên suốt.
