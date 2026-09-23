# Rà manuscript bằng GPT qua OmniProxy

Dùng khi người dùng yêu cầu rà hoặc hoàn thiện bài báo bằng model GPT qua OmniProxy.

## Nguyên tắc

1. Chỉ gọi model GPT đã được kiểm chứng bằng một yêu cầu chữ ngắn qua đúng `POST /v1/chat/completions`; đừng tin riêng danh sách `/v1/models`.
2. Không tự sửa cấu hình router, không để router âm thầm đổi sang Claude. Nếu phản hồi trả model/tuyến khác với model yêu cầu, coi là `BLOCKED` và báo rõ.
3. Tách hai bước: model chỉ rà và liệt kê claim/mâu thuẫn trước; con người/agent đối chiếu số liệu nguồn rồi mới sửa tối thiểu.
4. Không để model bịa số liệu, kiểm định thống kê, nhãn người, hoặc nguyên nhân cơ chế. Sao lưu nguồn và checksum trước khi vá.
5. Khi sửa claim, rà theo nghĩa ở mọi nơi: abstract, introduction, results, conclusion, caption, bảng/hình và limitations.

## Ghi nhận thực tế

- `gpt-5.4-mini` đã trả `HTTP 200`, `returned_model=gpt-5.4-mini` qua OmniProxy trong lần rà manuscript này.
- Danh sách model hoặc HTTP 200 ở health endpoint không đủ chứng minh model chạy được.
- Chênh lệch phần trăm không đồng nghĩa “có ý nghĩa thống kê”; chỉ dùng từ đó khi có kiểm định/khoảng tin cậy phù hợp.
