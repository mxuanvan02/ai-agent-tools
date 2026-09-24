# Criteria templates by domain — bộ tiêu chí theo ngữ cảnh

> Chất lượng loop bị chặn trên bởi chất lượng bộ tiêu chí. Đừng soạn từ trang trắng:
> chọn khung sườn theo ngữ cảnh dưới đây rồi điền. Template là KHỞI ĐẦU, không phải
> danh sách đóng — gặp ngữ cảnh mới thì đúc template mới bổ sung vào file này.

## Tư duy tổng quát — 4 góc nhìn BẤT BIẾN

Mọi bộ tiêu chí, bất kể lĩnh vực, đều là tổ hợp của 4 góc nhìn cố định. Tên vai trò
đổi theo ngữ cảnh (PM/dev/tester, tác giả/phản biện, tổ trưởng/GV...), nhưng bản
chất 4 góc thì không đổi:

| Góc | Vai trong phần mềm | Hỏi gì | Rủi ro nếu thiếu góc này |
|---|---|---|---|
| **Requester** (người ra yêu cầu) | PM / Product Owner / khách | Đúng ý chưa? Đủ scope chưa? Có vượt scope không? | Loop xây đúng thứ không ai đặt hàng |
| **Builder** (người làm) | Developer / author / GV soạn | Chất lượng kỹ thuật? Chuẩn nội bộ? | Code/bài chạy được nhưng rác, không bảo trì nổi |
| **Verifier** (người kiểm ĐỘC LẬP) | Tester / QA / reviewer | Xác nhận độc lập; chủ động tìm cách phá | Agent tự khen tự dừng (failure mode #2) |
| **Operator** (người chịu hậu quả) | DevOps / người dùng cuối | Vận hành được? An toàn? Đảo ngược được? | "Xong" trên máy agent, chết khi chạy thật |

**Luật phủ góc:** bộ tiêu chí thiếu bất kỳ góc nào trong 4 = chưa đủ, chưa cho loop chạy.
Với task một người đóng cả 4 vai (nghiên cứu cá nhân), vẫn phải TÁCH 4 checklist —
vai Verifier không được dùng chung não với vai Builder.

## Giải phẫu một bộ tiêu chí — 6 thành phần (ngữ cảnh nào cũng phải có)

1. **Done-criteria máy-chấm-được** — mỗi tiêu chí map về MỘT lệnh/phép kiểm yes-no.
2. **Boundaries** — điều KHÔNG được làm, kể cả khi làm vậy giúp "pass" (anti-Goodhart).
3. **Reconciliation anchors** — neo vào sự thật bên ngoài (nguồn gốc, tổng số độc lập, golden sample), không tự khai.
4. **Role lenses** — bảng theo 4 góc ở trên, ai nghiệm thu góc nào.
5. **Undecidable declarations** — khai báo phần KHÔNG máy-chấm-được (gu thẩm mỹ, tính sư phạm, "hay") → route lên người dùng làm điểm escalate, KHÔNG để agent tự chấm.
6. **Stuck law** — retry cap (mặc định 3), mơ hồ → escalate, không đoán giữa chừng.

Self-check cuối: đưa bộ tiêu chí cho người ngoài ngành — họ chạy ĐÚNG MỘT LỆNH và
nói được "xong chưa?". Không → viết lại trước khi chạy loop.

---

## TEMPLATE A — Phần mềm / website (bảng theo vai)

| Vai | Nhìn gì (done-criteria) | Chấm bằng | Không máy-chấm-được → escalate |
|---|---|---|---|
| PM/Requester | Mọi requirement trace được về code+test; không scope creep; đủ trang/tính năng theo danh sách chốt | checklist requirement × trace-id; `grep` route; đếm trang so mapping nguồn | "flow hợp lý chưa", "đúng gu khách" |
| Dev/Builder | Build sạch; lint+typecheck pass; coverage ≥ ngưỡng; không hardcode secret; không đụng deployed path | `npm run build`; `npm run lint`; `pytest --cov`; secret-scan; `git diff --name-only` so whitelist | Kiến trúc "đẹp" khi chưa có ADR |
| Tester/Verifier | Test xanh VÀ không bị sửa để xanh; feature mới có test mới; regression còn nguyên | `git diff` trên test files (boundary); chạy full suite; mutation spot-check | "test này có thực sự có nghĩa không" |
| Ops/Operator | Deploy được; reversible; có health endpoint; log/monitoring; preview URL sống | `curl -sS <preview>/health`; IaC validate; check log stream | Quyết định production, mua domain |

**Boundaries chuẩn của ngữ cảnh này:** không xóa/nới test để pass; không giảm coverage;
không sửa tiêu chí nghiệm thu; không force-push; không deploy production / mua gì tốn
tiền (→ LUÔN confirm); không đụng dữ liệu nguồn (Notion/DB gốc).

**Reconciliation anchors:** mapping nguồn→output (vd mỗi Notion page = 1 route, diff nội
dung = 0 thiếu); tổng số bản ghi khớp back-office; link-checker chạy thật (0 dead link).

## TEMPLATE B — Nghiên cứu / bản thảo học thuật

ĐÃ CÓ đầy đủ trong skill research (evidence-first-research):
claim-gate 3 dải, citation verify live, straw-man detection, số truy về CSV, hình từ
script, build-from-bundle. Ở đây chỉ map 4 góc:

| Vai | Là ai | Tiêu chí neo |
|---|---|---|
| Requester | Tác giả chính (người dùng) | RQ Brief đã duyệt; scope không phình |
| Builder | Agent viết/sửa | Mọi claim có nguồn; số = từ CSV deployed; ký hiệu nhất quán |
| Verifier | Claim-gate (Jev/laya) + reviewer độc lập subagent | noul 3 dải; đối chiếu claim↔source verbatim |
| Operator | Venue/compliance | Format đúng template; page limit; citation DOI thật; liêm chính số liệu |

**Undecidable:** "đóng góp có đủ hàm lượng Q1 không", novelty framing → người dùng quyết.

## TEMPLATE C — Nội dung / hành chính / giảng dạy (kế hoạch bài dạy, công văn, slide)

| Vai | Nhìn gì | Chấm bằng | Không máy-chấm-được → escalate |
|---|---|---|---|
| Requester | Bám văn bản gốc (thông tư/CV/mẫu của trường); đủ mục theo quy định | checklist mục × trace về điều khoản mẫu | "đúng tinh thần chỉ đạo" |
| Builder | Đúng cấu trúc/bố cục; ngôn ngữ phù hợp đối tượng; đủ tiết/phần | script check cấu trúc; đếm trang/tiết; validate bảng biểu | Văn phong "hay" |
| Verifier | Số liệu/trích dẫn khớp nguồn; không mục nào trống; nhất quán thuật ngữ | diff với nguồn quy định; scan placeholder rỗng | Tính sư phạm của hoạt động |
| Operator | In/nộp được (PDF đúng định dạng); mở được trên máy trường; nộp đúng hạn | build PDF + mở thật; check font tiếng Việt | Ký duyệt — LUÔN của người |

**Boundaries:** không bịa trích dẫn điều khoản; không tự ký/tự nộp; không đổi nội dung
văn bản gốc; template trường ≠ tự sáng tác layout.

## TEMPLATE D — Dữ liệu / pipeline ETL

| Vai | Nhìn gì | Chấm bằng | Không máy-chấm-được → escalate |
|---|---|---|---|
| Requester | Đúng schema contract; đủ trường cần cho báo cáo | schema validation (pydantic/jsonschema) | "số này có nghĩa kinh doanh gì" |
| Builder | Idempotent, re-runnable; không mất dòng; có log từng bước | chạy 2 lần so kết quả (hash); đếm dòng in/out | Thiết kế model khi chưa có spec |
| Verifier | Tổng reconcile với nguồn ĐỘC LẬP (back-office, sổ gốc); sample kiểm tay | sum/count diff = 0; spot-check 5 bản ghi | Chọn mẫu "đại diện" |
| Operator | Chạy đúng lịch; cảnh báo khi fail; output có documentation | cron/CI status; alert test | Dừng pipeline production |

**Boundaries:** không ghi đè dữ liệu nguồn; không im lặng nuốt exception; không đổi
contract một phía.

## TEMPLATE E — Website/nội dung DỒN từ nguồn có sẵn (Notion/Drive/CMS) — ca hay gặp

1. **Content reconciliation (anchor mạnh nhất):** mapping 1-1 nguồn→trang; mọi page có
   route; diff nội dung = 0 thiếu; ảnh/media đủ (đếm asset nguồn vs asset site).
2. **Build/Dev:** build pass; link-checker 0 dead link; responsive check (script/headless).
3. **UX/thẩm mỹ:** KHAI BÁO undecidable — agent chụp screenshot/preview URL đưa người
   dùng phán, KHÔNG tự chấm "đẹp".
4. **Deploy:** preview URL sống (health check); production = confirm.

---

## Quy trình điền (gắn vào Bước 0 của loop)

1. Nhận task → phân loại ngữ cảnh → chọn template A–E (hoặc tổ hợp nhiều cái).
2. Điền đủ 6 thành phần; thành phần nào KHÔNG điền được = flag ngay, đó là câu hỏi front-load cho người dùng.
3. Self-check "người ngoài ngành + 1 lệnh".
4. **Trình người dùng DUYỆT bộ tiêu chí trước khi loop chạy** — đây là sản phẩm của tầng phán xét.
5. Trong loop: build KHÔNG được sửa tiêu chí (luật sắt 3); muốn sửa → confirm người dùng, ghi lý do.
6. Sau mỗi task thật: tiêu chí nào bị chứng tỏ thiếu/sai → vá lại template trong file này (bài học vào template, không vào trí nhớ phiên).

## Bẫy khi soạn tiêu chí (mỗi bẫy là một failure mode đã đặt tên)

- **Tiêu chí đếm được nhưng đếm sai thứ:** "số lượng trang = 10" pass dù 3 trang rỗng → thêm anchor nội dung (diff nguồn = 0 thiếu).
- **Gộp phần không-chấm-được vào phần chấm được:** "trang web đúng và đẹp" → tách "đúng" (máy chấm) khỏi "đẹp" (escalate), không để agent chấm hộ cả cụm.
- **Boundary viết sau khi build bắt đầu:** luôn viết boundary TRƯỚC, cùng lúc với done-criteria; viết sau = đã cho phép ăn gian.
- **Nhiều tiêu chí mâu thuẫn nhau:** (vd "deploy nhanh" vs "mọi thay đổi qua review") → người dùng xếp hạng ưu tiên ở front-load, không để agent tự trade-off giữa chừng.
- **Verifier dùng chung công cụ với Builder:** test do chính code-gen viết có thể cùng sai một giả định → thêm 1 anchor ngoài (reconciliation, golden sample) độc lập với cả hai.
