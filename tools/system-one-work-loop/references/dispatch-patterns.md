# Dispatch patterns — cách cho loop "tự chạy" trong Hermes

Ba mức, tăng dần độ tự động. Chọn theo mức tin cậy đã đạt.

## Mức 1 — Loop trong MỘT turn agent (mặc định, an toàn nhất)

Agent nhận task, front-load ở Bước 0, rồi chạy nhiều tool call LIÊN TIẾP trong
cùng một lượt: build → check → gate → build tiếp... cho tới khi gate trả
done/confirm/escalate/abort. Chỉ KẾT THÚC LƯỢT (nhắn người dùng) khi:
- gate=done (xong), hoặc
- gate=confirm/escalate/abort (cần người).

Đây là "tự làm tiếp không cần người nhắn từng bước" đúng nghĩa: agent không dừng
lại sau mỗi bước chờ "làm tiếp", nó tự đi hết chuỗi execute rồi mới báo.

## Mức 2 — Subagent điều phối (task dài, nhiều nhánh độc lập)

Dùng `delegate_task` spawn subagent cho các nhánh song song độc lập; parent giữ
vai plan + judge tổng. Mỗi subagent tự chạy loop Mức 1 cho nhánh của nó, trả
summary có bằng chứng verify được (URL/ID/path/số). Parent VERIFY lại trước khi
báo người dùng — summary của subagent là tự-báo-cáo, không phải sự thật đã kiểm.

## Mức 3 — Cron / background thường trú (full-auto, chỉ khi đã tin)

Treo loop lên cron (`cronjob_manage`) hoặc background process cho việc "phải xảy
ra đúng giờ" (vd: đêm rà bản thảo, sáng báo PR sạch). Kèm laya server thường trú
làm van offline để không phụ thuộc mạng. Vẫn giữ lằn ranh đỏ: mở PR/nháp, KHÔNG
tự merge/publish; escalate về kênh người dùng khi kẹt.

## Skeleton tài liệu-điều-phối (maintenance, tùy chọn)

Với việc "trông coi một thứ đang tồn tại", dùng một doc làm hàng đợi + máy trạng
thái + giao diện người:
- cột "vấn đề" chỉ người ghi; cột "kết quả" chỉ loop ghi; trạng thái tiến MỘT
  CHIỀU, không lùi.
- exit code là tối hậu (script nói exit 1 thì script thắng).
- trạng thái chỉ tiến tới "chờ nghiệm thu"; ô "DONE" do NGƯỜI lật.

## Kiểm trước khi lên Mức 2/3

- Đã chạy TAY 1 lần thành công task đại diện? (buộc rõ judge chấm bằng gì)
- Retry cap + escalate path có thật? Không quay vô hạn?
- Mọi thao tác không-đảo-ngược đều confirm/escalate, không execute tự động?
- Nguồn doc/memory loop dựa vào có tươi không, ai bảo trì?
