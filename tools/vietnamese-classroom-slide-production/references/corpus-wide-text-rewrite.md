# Sửa chữ HÀNG LOẠT trên cả kho deck: 7 luật đã trả giá

Phạm vi: áp một thay đổi CHỮ lên hàng chục deck (ví dụ bỏ kiểu "chép vào vở / nộp tệp /
ghi phiếu" trên 34 deck = 923 chỗ). Khác việc dựng một deck mới: ở đây rủi ro là phá
hàng loạt thứ đã được duyệt, và lỗi dễ ẩn vì số lượng.

## 1. Tách LUẬT ra module dùng chung — dry-run và bản ghi thật phải import cùng một file

Đã trả giá: v1→v4 em vá luật trực tiếp vào file dry-run, nên mỗi lần "dry-run đạt" là
đạt trên một bộ luật khác với bộ luật sẽ ghi thật → kết quả verify vô nghĩa. Sửa:
`rewrite_rules.py` là nguồn luật duy nhất, cả `dryrun_v5.py` lẫn
`apply_corpus_rewrite.py` đều `import` từ đó.

## 2. Số chuỗi KHÁC NHAU quyết định cách làm, không phải số chỗ

Đo ra 941 chỗ nhưng **383 chuỗi khác nhau**. Bảng tra thủ công (như đã làm cho một deck
30 chỗ) là bất khả thi và chắc chắn sót. Cách đúng: tách TIỀN TỐ thời gian
(`6 phút · `, `90 phút · hai tiết · `) ra, áp luật cho PHẦN THÂN, câu nào không có luật
thì ABORT. Kết quả: 300 thân câu duy nhất phủ hết 939 chỗ.

## 3. THỨ TỰ luật là quy tắc — cụm dài/cụ thể trước, luật chung sau

Sai thứ tự sinh câu hỏng, đã gặp hai ca:
- `[Nn]ộp tệp Bx_NhomXX` phải đi TRƯỚC `NhomXX`, nếu không ra `Nộp Kết quả của nhóm`
  (còn đúng chữ "Nộp" là thứ cần bỏ).
- `ghi vào phiếu` → `ghi lại` phải đi TRƯỚC luật xoá `\svào phiếu`, nếu không ra
  `Cách còn lại ghi, kèm…` — động từ lơ lửng.

## 4. Luật phải bật `re.I`; thay thế phải theo HOÁ của chỗ khớp

Câu trong deck là `**C**ó phần em chép vào vở` mà luật viết `có phần (em )?chép vào vở`
không có `re.I` → không khớp → rơi xuống luật chung → ra câu dài hơn. Đồng thời phải
có hàm `match_case(src, rep)`: nếu không thì `CHÉP VÀO VỞ · 1. BA KHÁI NIỆM` thành
`ba phần NỘI DUNG CHÍNH` (hoa sai giữa câu thường).

## 5. Regex phải phủ BIẾN THỂ CÓ THẬT trong corpus — đếm biến thể trước khi viết luật

Đã gặp: corpus có câu kết thúc `…B2_NhomXX nộp cuối` **KHÔNG có chữ "giờ"**, nên phần
tuỳ chọn `(nộp cuối giờ)?` không khớp, để sót `nộp cuối` rồi bị luật chung biến thành
`hoàn thành cuối` (vừa dài vừa vô nghĩa). Cách phòng: đếm biến thể bằng lệnh
(`27× 'nộp cuối giờ'`, `1× 'nộp cuối'`) rồi viết luật phủ cả hai.

## 6. CỔNG phải SO SAI PHÂN, và phải tự kiểm chứng trước khi tin số của nó

Em đã hai lần viết detector hỏng trong cùng một phiên:
- Cổng `\s·` (bắt "dấu · dính khoảng trắng") báo **525/939 câu vi phạm** — nhưng câu
  GỐC cũng là `90 phút · hai tiết`, tức đó là định dạng đúng sẵn có của deck. Âm giả.
- Bộ dò "caption đè footer" báo **1083 vi phạm trên 34 deck đã phát hành** vì bắt trúng
  chính hộp chữ footer (cũng >60 ký tự, cao 0.26in, luôn có ảnh phía trên).

Sửa: chia cổng làm hai loại —
- `BANNED_ABSOLUTE`: đúng thứ cần loại (nộp/vở/phiếu/NhomXX). Cấm tuyệt đối ở câu mới.
- `DIFFERENTIAL`: lỗi định dạng (cách đôi, lặp từ, hoa sai, dài ra). Chỉ tính khi
  **có ở câu mới mà KHÔNG có ở câu cũ** → miễn nhiễm với định dạng sẵn có.

Dấu hiệu nhận ra âm giả: (a) số lỗi == số slide, (b) mọi vi phạm cùng một geometry,
(c) câu gốc cũng có đặc điểm đó. **Nghi tool trước, nghi deck sau.**

## 7. So bản local vs bản Drive: CHUẨN HOÁ CẢ HAI PHÍA, rồi mới kết luận

Ba bước đã trả giá:
1. Chỉ đọc `has_text_frame` cấp ngoài → mọi shape là GROUP → báo "0 hộp cần sửa"
   (FAIL-OPEN). Phải đệ quy vào GROUP.
2. Lọc `is_scaffold` ở cả hai phía rồi so thứ tự → local có câu CŨ (bị loại), Drive có
   câu MỚI (được giữ) → dãy lệch đúng MỘT Ô → báo "213 vị trí lệch" oan và kết luận
   "local có nội dung riêng" SAI. Bằng chứng nó sai: các vị trí lệch liên tiếp dịch
   đúng một ô (`local[34]='Hoạt động'` vs `Drive[34]='Kết quả'`).
3. Sửa đúng: `normalize()` cả hai phía bằng CÙNG bộ luật rồi mới so, và so bằng cả
   THỨ TỰ (list) lẫn MULTISET (Counter) — so set bỏ sót khác biệt số lần xuất hiện.

Sau khi chuẩn hoá, khác biệt thật của BAI_30 chỉ còn **11 vị trí** (không phải 213), và
chúng không cùng một hướng:
- Drive hơn local: đã bỏ ký tự `• ` gõ thừa (`fix_double_bullet_all.py`, mtime trùng
  mtime bản Drive) + đã sửa chữ kiểu nộp tệp.
- Local hơn Drive: tiêu đề ĐẦY ĐỦ (`…tính ƯCLN`, 49 ký tự) trong khi Drive bị cắt cụt
  (`…chương trình…`, 40 ký tự) — defect có sẵn từ lúc build (đo: 298 đoạn có dấu `…`
  trên 24/34 deck, số này KHÔNG ĐỔI trước/sau khi sửa chữ nên không phải do việc sửa).

→ Không bản nào là superset. KHÔNG ghi đè mù theo hướng nào; báo số cho người dùng
quyết. Luật: khi hai bản phân kỳ hai chiều, tìm BẰNG CHỨNG của lần sửa (mtime script so
với mtime file) thay vì đoán bản nào mới hơn theo cảm giác.

## Checklist tối thiểu cho một đợt sửa chữ hàng loạt

1. Kiểm kê bằng lệnh: số chỗ, số chuỗi khác nhau, số deck, biến thể đuôi.
2. Tách luật ra module; dry-run import module đó; in TOÀN BỘ thân câu duy nhất để soát
   bằng mắt (không soát mẫu 15 câu).
3. Cổng so sai phân; chạy cổng trên mẫu đã biết sạch VÀ mẫu đã biết lỗi trước khi tin số.
4. Chạy thử MỘT deck nhỏ nhất → render → vision xem ≥2 slide đại diện (câu dài nhất,
   câu ngắn nhất, bảng nhiều cột).
5. Backup từng deck, gate từng deck (ABORT nếu có câu không sinh được), verify bằng cách
   ĐỌC LẠI file sau ghi.
6. So md5 local vs Drive: chỉ ghi đè local khi chứng minh được local là bản cũ.
7. Upload rồi verify từ phía server (`rclone check`, so size, mtime) — không tin log của
   job nền đã kết thúc mà mình chưa đọc được output.
