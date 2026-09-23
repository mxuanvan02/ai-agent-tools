# Canonical-vs-Sent-Copy Verification Gate

Khi người dùng GỬI một file/zip manuscript và bảo "sửa lỗi vào bản này", ĐỪNG sửa thẳng vào
bản trong `/tmp` (giải nén từ zip) hay tin rằng nó là bản mới nhất. Trên máy thường đã có
một **bản canonical** trong `SAS/Research/<project>/` mới hơn. Sửa nhầm bản cũ = mất công +
ghi đè công người dùng đã làm.

## Gate (đã chặn được lỗi thật trên bài probe-transmit IoTJ)

1. **Tìm bản canonical** bằng search_files theo tên section đặc trưng (vd
   `04_evaluation.tex`), không chỉ tìm trong /tmp.
2. **Diff sent-copy vs canonical** toàn bộ sections + main.tex. So `mtime` hai bản.
   Phát hiện điển hình: canonical mới hơn zip vài giờ–vài ngày và đã khác ở nhiều file
   ⇒ zip KHÔNG phải nguồn chân lý.
3. **Xác minh lỗi cần sửa CÒN tồn tại trong canonical**, không sửa mù theo audit chạy trên
   zip cũ. Nhiều mục audit (chạy trên zip) có thể người dùng ĐÃ tự sửa rồi trong canonical (vd
   va chạm ký hiệu μ/X̂ đã phân định, câu thừa đã bỏ). Grep đúng 3 chỗ flagged trong
   canonical trước khi patch.
4. **Sửa vào canonical**, backup `_backups/<tag>_<ts>/` trước.
5. Khi audit/reviewer chạy trên một bản (zip), nhưng ta sửa bản khác (canonical) ⇒ ghi rõ
   trong báo cáo "audit chạy trên zip, đã verify lỗi còn trong canonical rồi mới sửa".

## Nguồn chân lý cho nội dung cần khẳng định
Khi cần khẳng định một fact triển khai (vd "p_i chỉ nhân số hạng value") mà KHÔNG có code
local (repo trên GitHub), nguồn chân lý là chính PHƯƠNG TRÌNH TRIỂN KHAI đã có trong
manuscript — bám nó, không bịa thêm dữ kiện về code không đọc được.
