# Khôi phục niềm tin khi người dùng nói "sửa lui sửa tới, không tin được kết quả nào là thật"

## Tín hiệu kích hoạt
Người dùng mất niềm tin vào kết quả vì phương pháp bị đổi tới đổi lui: một kỹ thuật/đề xuất được **thêm rồi bỏ rồi lại cân nhắc**, nhiều biến thể cùng tên (kiểu bài bandwidth-scheduling-PD / bài bandwidth-scheduling-CVaR / bài bandwidth-scheduling-MV…), hoặc nhiều bản thảo song song. Câu nói mẫu: *"Cứ sửa lui sửa tới… khiến người dùng rất khó tin tưởng được kết quả nào là thật"*, *"lúc thì đề xuất thêm X rồi lại bảo nó không phù hợp"*.

**QUAN TRỌNG:** đây KHÔNG phải lời mời sửa tiếp. Sửa thêm một lần nữa chỉ làm sâu thêm mất niềm tin. Đây là lỗi **quy trình**, chữa bằng cách thiết lập lại nguồn sự thật + kiểm chứng, KHÔNG bằng cách chỉnh nội dung.

## Quy trình đúng (theo thứ tự — DỪNG sửa nội dung trước đã)

1. **Kéo lại bối cảnh** bằng `session_search` trước khi đụng gì. Đừng lặp lại đúng cái vòng đã gây lộn xộn.

2. **Định vị mọi bản trùng** trên đĩa (`search_files`). Đếm rõ có bao nhiêu bản `.tex`/thư mục song song, bao nhiêu `.zip` rải rác. Nêu con số này ra — chính sự phân mảnh (không phải số liệu) mới là gốc mất niềm tin.

3. **Tìm nguồn có git.** Repo git (có `.git`) đáng tin hơn mọi thư mục rời + zip, vì nó có lịch sử và (thường) pipeline tái lập. Chốt nó là **canonical**.

4. **KIỂM CHỨNG TÁI LẬP = phép thử niềm tin.** Đây là bước quyết định, làm THẬT chứ không hứa:
   - Xoá bảng/artifact cũ trong thư mục **tạm**, chạy lại toàn bộ pipeline từ dữ liệu gốc.
   - `diff` từng file (`.tex`, `*_summary.csv`) mới sinh vs bản đã commit.
   - **KHỚP tuyệt đối** ⇒ số liệu tất định, sinh từ script + data thật, KHÔNG gõ tay ⇒ người dùng tin được. Báo bảng KHỚP/LỆCH rõ ràng.
   - **LỆCH** ⇒ chỉ mặt đúng file/số nào "ảo", đó mới là thứ cần sửa.
   - Kiểm tra dữ liệu có thật không (ví dụ ERA5 thật vs mô phỏng calibration).

5. **Dựng lại lịch sử quyết định từ `git log --stat`.** Đọc thẳng cái vòng thêm→bỏ→legacy cho người dùng thấy, ví dụ:
   `Add VoU urgency channel` → `drop VoU… switch to real ERA5` → `move VoU/CVaR to legacy/`.
   Kết luận thẳng: kỹ thuật nào **đã bị bỏ** (không còn là đề xuất), kỹ thuật nào **còn sống**. Dùng `grep`/đếm nhãn để liệt kê các biến thể (bài bandwidth-scheduling-PD sống, bài bandwidth-scheduling-CVaR đã vào legacy, "bài bandwidth-scheduling-to" chỉ là mảnh regex…).

6. **Cô lập legacy, KHÔNG xoá.** Đưa bản `.tex` thừa + zip thừa vào `_backups/<ts>/` để chỉ còn 1 bản làm việc. Mất niềm tin thường do legacy chưa cắt khỏi tầm mắt, nên mở ra vẫn thấy cả VoU/CVaR và tưởng chúng vẫn đang tranh cãi.

## Sau khi kiểm chứng — hỏi đúng MỘT quyết định chặn
Đừng tự ý thêm/bỏ kỹ thuật nữa (chính điều đó gây mất niềm tin). Trình bày rõ "quyết định đã chốt là gì" theo git, rồi hỏi người dùng xác nhận: *giữ nguyên hướng đã chốt* hay *muốn cân nhắc lại kỹ thuật đã bỏ* (nếu cân nhắc lại thì phân tích ưu/nhược để người dùng quyết, không tự quyết).

## Pitfalls
- Đừng kể lịch sử theo trí nhớ — moi từ `git log`/code thật rồi mới nói.
- Đừng gọi kết quả "khớp/tái lập được" nếu chưa chạy diff thật (memory: cấm gọi artifact "ready" không có bằng chứng chạy).
- Nhiều bản song song = tự nó là bug quy trình; nhắc người dùng nguyên tắc "edit main in place, no versioned copies, backup vào _backups/".
