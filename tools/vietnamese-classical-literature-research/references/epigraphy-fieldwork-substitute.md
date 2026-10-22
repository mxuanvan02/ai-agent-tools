# Thay thế khảo sát thực địa bằng dữ liệu số (epigraphy & stele corpora)

Dùng khi đề tài cần tư liệu **tại chỗ** — bia đá, văn khắc, lăng tẩm, đình chùa, sắc phong,
gia phả, khoán ước — mà người nghiên cứu **không thể đi thực địa** (không có điều kiện đi,
bia đã mất, di tích đã giải tỏa, kinh phí, thời gian).

Nguyên tắc: **không có gì thay thế được việc nhìn bia thật**, nhưng ba lớp dưới đây thay thế
được **phần lớn** công việc mà chuyến đi thực địa phục vụ — xác định bia có tồn tại không,
ở đâu, khắc năm nào, ai soạn, nội dung gì, chữ ra sao.

## Ba lớp thay thế

### Lớp A — Ảnh thác bản (bản rập) — quan trọng nhất

**Vietnamica** (Viện Nghiên cứu Hán Nôm × EFEO), `https://gallery.vietnamica.online/`

Đây là bộ sưu tập **20.980 thác bản văn bia** do Viện Viễn Đông Bác Cổ Pháp rập tại Việt Nam
từ 1910 đến 1944. Thác bản là bản rập giấy ướt lên mặt bia — tức là **bản sao 1:1 của bia ở
thời điểm rập**. Với bia đã mất hoặc đã mòn sau 1944, thác bản là **bản ghi duy nhất còn lại**.

Mỗi bản ghi mang:

| Trường | Nội dung | Dùng để |
|---|---|---|
| `RefNumber` | Mã số thác bản | Trích dẫn chuẩn (vd `00001`) |
| `Original_Title` | Tiêu đề **Hán tự** | Đối chiếu chữ, tránh sai dị thể tự |
| `Vietnamese_Title` | Tiêu đề Quốc ngữ | Tra cứu bằng tiếng Việt |
| `CalendarYear` / `Full_Date` | Niên đại dương lịch + niên hiệu | Định niên (vd `Cảnh Hưng thứ 37 (1776)`) |
| `TinhVN` / `HuyenVN` / `XaVN` | Tỉnh/huyện/xã **hiện tại** | Định vị |
| `Full_Location_(origin)` | Địa danh **thời kỳ khắc bia** | Truy nguyên hành chính cổ |
| `Number_Faces` / `Number_Columns` / `Number_Characters` | Số mặt/cột/ký tự | Ước lượng quy mô văn bản |
| `Dimension` | Kích thước (vd `35 x62 cm`) | Mô tả hiện vật |
| `Content` | Tóm tắt nội dung bằng tiếng Việt | Sàng lọc trước khi đọc bản rập |
| `Composer1_Name` / `Writer1_Name` / `Engraver1_Name` | Người soạn / người viết / thợ khắc | Truy tác giả, kèm học vị chức vị |
| `Picture_Link` | URL ảnh JPEG độ phân giải cao | Đọc chữ Hán trực tiếp |

Đo thực tế trên hệ thống: 10.759 bản ghi trả về qua API, phủ niên đại **1074–1944**
(451 năm có dữ liệu), tập trung nhất 1650–1850, địa bàn mạnh nhất là đồng bằng sông Hồng
(Hà Đông, Bắc Ninh, Hải Dương, Vĩnh Yên, Hà Nội). Ảnh thực tế **3840 × 5778 px**, ~2.9 MB/ảnh.

### Lớp B — Bản đồ định vị theo địa giới cổ

`https://carto.vietnamica.online/`

Bản đồ dựng lại địa giới hành chính đồng bằng sông Hồng **đúng thời kỳ rập bản (1910–1944)**,
bốn cấp Tỉnh / Huyện / Tổng / Xã. Mỗi bia là một điểm đỏ kèm mã số thác bản; bấm vào ra toàn bộ
trường dữ liệu và link ảnh.

Giá trị phương pháp: địa danh trong bia là địa danh **thời khắc bia**, không phải địa danh sau
các cuộc đổi đơn vị hành chính. Muốn tìm bia theo tên làng cũ, phải dùng bản đồ này chứ không
dùng bản đồ hiện hành. Đây chính là việc mà trước kia phải đi thực địa hỏi già làng mới làm được.

### Lớp C — Mục lục để tra chéo

| Nguồn | Quy mô đo được | Vai trò |
|---|---|---|
| `chonthieng.com/van-bia/` | 12.025 bản ghi (mã VB000200–VB12287) | Mục lục tổng hợp, tra chéo, lớp 4 — không cite |
| `lib.nomfoundation.org/collection/2/subject/9` | mã `tnvnpf-vb-xxx`, Hán + Quốc ngữ | Đối chiếu song ngữ |
| `hannom.nlv.gov.vn` (a=cl&cl=CL1) | 1.778 tựa sách Hán-Nôm | Bản rập là bia, còn đây là **sách** — bổ trợ cho nhau |
| CiNii `BA8546792X` | Thư mục thác bản EFEO, NXB VHTT 2007 | Mốc tham chiếu bản in |

## Quy trình 5 bước

1. **Khoanh vùng bằng mục lục, không bằng trí nhớ.** Chạy `scripts/harvest_epigraphy.py`
   để lấy danh mục đầy đủ, rồi lọc theo địa danh / niên đại / từ khoá. Không đoán mã thác bản.

2. **Sàng lọc bằng `Content` trước khi tải ảnh.** Mỗi ảnh ~3 MB; đọc tóm tắt tiếng Việt trước
   để loại 90% bản ghi không liên quan.

3. **Xác định địa danh cổ bằng bản đồ** khi bia ghi địa danh không còn tồn tại.

4. **Đọc bản rập ở độ phân giải gốc.** Ảnh 3840×5778 đủ đọc chữ Hán cỡ nhỏ. Đây là bước duy nhất
   thay thế được việc đứng trước bia — mọi suy luận về chữ phải dựa trên ảnh này, không dựa trên
   tiêu đề Quốc ngữ (Quốc ngữ là **phiên âm của người biên mục**, có thể sai hoặc theo cách đọc khác).

5. **Ghi ledger theo mẫu**, kèm mã thác bản:

```
claim | RefNumber + ảnh thác bản | Hán tự (đọc từ ảnh) | Quốc ngữ biên mục | verified?
```

## Cạm bẫy đo được

- **Token Vietnamica gắn với PHP session.** Gọi `api/search.php` với token đúng nhưng không có
  cookie `PHPSESSID` trả `{"error":"Access denied. No token"}` — đúng ra là
  `Invalid or missing token` khi token cũ. Phải tải trang chủ để lấy **cùng lúc** meta
  `name="api-token"` và cookie, rồi gọi API với header `X-API-Token`. Token tự đổi mỗi session.
- **`Content` là tóm tắt của biên mục, không phải nguyên văn.** Trích nguyên văn phải đọc ảnh.
- **`No Info` là giá trị thật trong dữ liệu**, không phải null. Đừng đếm nó là "có tác giả".
  Đo thực tế: 5.476 bản ghi có `Composer1_Name`, nhưng 2.684 trong đó là chuỗi `không ghi.`
- **Địa danh trong `TinhVN` là đơn vị hành chính cũ**, không phải tỉnh hiện nay (Hà Đông, Vĩnh Yên,
  Kiến An, Phúc Yên đã sáp nhập). Đừng đưa thẳng vào bản thảo như địa chỉ hiện hành.
- **Số bản ghi ≠ số bia.** Một bia có thể có nhiều thác bản (rập nhiều lần), và `Picture_Link`
  có thể chứa **nhiều URL phân cách bằng dấu phẩy** — tách ra trước khi tải.
- **Đừng kết luận "không có tư liệu" từ một truy vấn rỗng.** Tập này chỉ phủ đồng bằng sông Hồng
  và giai đoạn 1910–1944. Bia ở miền Trung, miền Nam, hoặc bia dựng sau 1944 **không nằm trong**
  bộ này — vắng mặt ở đây không có nghĩa là vắng mặt trên thực địa.

## Giới hạn phải nói thẳng khi viết bài

Thác bản không thay thế được: quan sát chất liệu (đá gì, còn nguyên hay vá), bối cảnh không gian
(bia đặt ở đâu trong chùa, hướng nào), các mặt bia không được rập, và bia dựng sau 1944. Nếu
kết luận phụ thuộc vào mấy yếu tố đó, phải khai là hạn chế của phương pháp — không được lặng lẽ
trình bày dữ liệu số như thể đã khảo sát thực địa.
