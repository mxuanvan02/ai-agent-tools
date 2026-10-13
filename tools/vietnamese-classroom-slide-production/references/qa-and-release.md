# QA và phát hành

## Fingerprint nguồn

Trước khi sửa, ghi lại: đường dẫn/tên file, SHA-256 hoặc kích thước, số slide, tỉ lệ trang, tiêu đề bìa và chuỗi đại diện ở vài slide. Nếu có nhiều file gần tên, không tự chọn theo suy đoán.

## Cổng cấu trúc

Kiểm tra trên file PPTX cuối:

- ZIP/OOXML hợp lệ; đúng tỉ lệ 16:9.
- Số slide đúng bản đồ bài học.
- Notes không rỗng trên mọi slide nội dung.
- Không có shape vượt biên, placeholder, chuỗi `\\n`, chữ rác hoặc nội dung từ bài khác.
- Không có nhãn/cụm bị cấm; dấu hỏi chỉ nằm ở phần bài tập được phép.

## Cổng hình ảnh

1. Xuất PDF từ PPTX cuối và đối chiếu số trang.
2. Render toàn bộ slide thành ảnh; tạo contact sheet.
3. Xem riêng slide dày nhất, ví dụ mới, bảng/biểu đồ và slide có chữ nhỏ.
4. Phân loại: P0 = chồng/cắt/mất chữ; P1 = khó đọc, tương phản thấp, ngắt dòng hoặc phân cấp sai.
5. Sửa nguyên nhân, dựng lại PPTX/PDF và kiểm tra lại. Không phát hành khi còn P0/P1.

## Quy ước tên phát hành

Dùng tên ổn định, không chứa trạng thái nội bộ như `LAM_LAI`, `FINAL`, `NEW`:

- PPTX: `BAI_XX_<TEN_BAI_KHONG_DAU>.pptx`
- PDF đối chiếu: `BAI_XX_<TEN_BAI_KHONG_DAU>.pdf`

Giữ số bài hai chữ số nếu cả thư mục dùng chuẩn đó; nếu thư mục hiện hành có quy ước khác, ưu tiên tính nhất quán của toàn bộ thư mục.

## Cập nhật Drive an toàn

- Liệt kê đúng thư mục và nhận diện file cũ bằng tên, kích thước, thời gian sửa.
- Tải bản mới lên tên tạm hoặc thư mục staging trước khi thay thế nếu backend không hỗ trợ versioning rõ ràng.
- Giữ một bản phục hồi có timestamp hoặc dựa vào Trash/version history; không xóa vĩnh viễn.
- Sau upload, đọc lại metadata/kích thước và so sánh với file local.
- Chỉ báo thành công khi file đích tồn tại và kiểm tra đọc lại đạt yêu cầu.

## Báo cáo theo lô

Với bộ nhiều bài, báo cáo ngắn theo bảng: bài, nguồn, số slide, notes, QA, tên Drive, trạng thái. Không tuyên bố “đã làm hết” khi chỉ mới tạo script hoặc bản dựng trung gian.


## Đo lỗi trình bày: đọc XML, đừng đọc text

- **`python-pptx .text` KHÔNG chứa bullet tự sinh.** Dấu `buChar`/`buAutoNum` nằm ở `pPr`, không nằm trong run, nên tìm chuỗi `"• •"` trong `paragraph.text` luôn ra 0 hit. Đã vì thế mà kết luận SAI một lỗi có thật: 40 đoạn trên 4 deck vừa khai `<a:buChar char="•"/>` vừa có text bắt đầu bằng `•` → PowerPoint vẽ HAI dấu. Muốn biết màn hình vẽ mấy dấu thì đọc XML của `pPr`, và xác nhận lại bằng vision trên ảnh zoom.
- **Sửa bullet lặp: bỏ dấu GÕ THỪA trong text, giữ `buChar`.** `buChar` mang màu/cỡ/font của template (`buClr`/`buSzTx`/`buFontTx`); xoá nó sẽ làm bullet mất style và lệch với các bullet khác trong cùng deck.
- **Lệch bullet trong PDF có thể là artifact của renderer, không phải lỗi deck.** Artifact để dạy là `.pptx` mở bằng PowerPoint, còn ảnh ta đo là PDF do `soffice` render. Tách cho rõ bằng thí nghiệm có đối chứng: dựng pptx tối thiểu với các textbox có `left/marL/indent/buChar` GIỐNG HỆT, chỉ khác độ dài chữ, rồi render và đo toạ độ glyph bằng `fitz`. Nếu bản đối chứng cũng lệch (đã đo: 5.24pt, cùng cỡ 3.36pt trên deck thật) thì đó là cách LibreOffice render hanging indent — **không "sửa" geometry vốn đúng**.

## Guard phải chặn đúng thứ thật, không chặn proxy tự chế

- Guard "số từ mỗi slide không được tăng" từng CHẶN OAN một sửa đổi đúng: slide đó đã vượt ngưỡng sẵn nên thêm 3–5 từ không làm slide nào **mới** vượt. Tiêu chí đúng: **số slide vượt ngưỡng không được tăng**. Còn rủi ro thật (tràn chữ đè ảnh) thì chặn theo từng đoạn ("bản mới không dài hơn bản cũ + 2 kí tự", vì shape có width cố định) và để cổng `ink_clip_check` trên PDF đã render phán xử — cổng đó đo va chạm thật, không phải proxy.
- **Đọc chữ ký hàm trước khi dùng nó làm guard.** `measure_path()` trả `(size, ncols, hits)`; unpack thành `sev, ncols, hits` rồi kiểm `if sev:` là kiểm **size** — tuple luôn truthy nên guard FAIL oan dù `hits=[]` (0 vết cắt). In kèm giá trị thô vào log là cách phát hiện loại lỗi này ngay.
- **Đừng dựng lát cắt từ hiệu hai toạ độ rồi giả định nó khác rỗng.** Cắt dải "khoảng trống giữa hai band" với `start = mốc_trên + cao_band + 2`, `stop = mốc_dưới - 2` cho slice RỖNG khi band cao hơn khoảng cách giữa hai mốc → `np.median([])` trả NaN → `ValueError`. Cách bền: lấy median của pixel **không-mực** trong toàn nội dung, kèm guard kiểm số pixel tối thiểu.
- **Phát hiện vạch chia dọc phải bỏ viền ngoài.** Quét cột xám chạy suốt trên toàn chiều rộng sẽ bắt luôn viền khung (cột 0 và W-1 cũng thoả) → khoảng chia thành rỗng → "0 band". Chỉ quét trong vùng nội dung, gom cụm, loại cụm quá rộng và cụm dính mép, chọn cụm hẹp gần tâm nhất.
- **Thêm guard bảo toàn mực khi dịch/chuyển nội dung ảnh:** tổng số pixel mực trước và sau phải bằng nhau từng pixel (đã dùng: 54343 → 54343). Kèm guard dải định cắt phải 0 pixel mực. Hai guard này bắt được glyph gãy mà mắt thường dễ bỏ qua.

## Cổng kết luận "đã đồng bộ" phải so với server, không so với clone local

- Một script verify so `~/.hermes/skills/...` với `~/ai-agent-tools/...` (clone **local**) và chỉ quét những file có sẵn trong thư mục references sẽ kết luận "KHÔNG cần mở PR" ngay cả khi base branch trên server chưa có nội dung mới. Phép thử quyết định: `git show origin/<base>:<đường dẫn>` có chứa luật mới không, và `git ls-tree origin/<base> <thư mục>` có file mới không.
- **`gh` cài bằng snap bị confine: không đọc được `<data>`.** Chạy `gh pr create` từ worktree trên đĩa đó ra `fatal: error opening '.../.git': Permission denied`. Cách đúng: chạy `gh` từ clone trong `$HOME` và đặt file body PR trong `$HOME` (`/tmp` cũng không đọc được). Nếu vẫn kẹt, fallback `gh api repos/<owner>/<repo>/pulls -X POST -F body=@/home/<user>/file.md` không cần git.
- **Exit code của pipeline là exit code của LỆNH CUỐI.** `gh pr create ... | tail -5; echo $?` trả 0 dù lệnh create fail. Luôn verify bằng một lệnh đọc độc lập: `gh pr list --head <branch> --state all --json number,state,url`.
