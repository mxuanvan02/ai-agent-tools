# Bẫy khi viết script dựng deck bằng python-pptx

Áp dụng khi dựng lại deck theo lối `rebuild_baiNN.py` kế thừa từ bài trước. Mọi lỗi dưới đây đều đã xảy ra thật và tốn ít nhất một vòng dựng lại.

## 1. Tách helper dùng chung, tham số hoá định danh

Copy nguyên script bài trước rồi sửa tay dẫn tới sót định danh ở footer, header, notes và tên tệp sản phẩm. Cách bền hơn:

- Đưa toàn bộ hàm vẽ vào một module dùng chung (ví dụ `qa_tools/deck_helper.py`).
- Module giữ hai biến định danh ở cấp module: `MUC` (mục KHBD) và `HEADER` (chuỗi header trang).
- Script từng bài `import deck_helper as H`, **gán `H.MUC` và `H.HEADER` TRƯỚC khi import các hàm vẽ và trước mọi lệnh vẽ**, rồi mới `from deck_helper import (...)`.

Gán sau khi vẽ thì header/footer mang định danh của bài cũ mà QA cấu trúc vẫn báo đạt.

## 2. Không hardcode số slide khi nhân bản

Sai:

```python
for _ in items: clone_slide(prs, 1)
for idx in range(len(items), 0, -1): delete_slide(prs, idx)   # SAI
```

Vòng xoá đang lấy `len(items)` làm số slide thân bài của deck **nguồn**. Khi số mục thay đổi (thêm slide ghi vở, bung chuỗi khoanh dòng) thì lệch, gây `IndexError: slide index out of range`.

Đúng:

```python
n_goc = len(prs.slides)          # PHAI doc truoc khi nhan ban
for _ in plan: clone_slide(prs, 1)
for idx in range(n_goc - 1, 0, -1): delete_slide(prs, idx)   # giu lai slide bia
assert len(prs.slides) == total, 'so slide: %d, ky vong %d' % (len(prs.slides), total)
```

`assert` này bắt lỗi ngay tại lúc dựng thay vì để lộ ra ở QA.

## 3. Toạ độ trong vòng lặp phải cộng theo chỉ số

Lỗi thật đã lọt qua QA và ra tới Drive ở ba bài liền: trong `note_slide`, vòng tròn số chạy theo `y = 3.03 + j*0.9` nhưng icon số lại ghim cứng `y = 3.115`. Kết quả: số 2 và số 3 đè lên số 1, hai vòng tròn dưới rỗng.

Quy tắc: mỗi phần tử con của một hàng lặp phải dùng **cùng một biểu thức `y`**. Kiểm tra bằng cách đọc toạ độ shape sau khi dựng:

```python
ovals = [(round(sh.left/914400,3), round(sh.top/914400,3)) for sh in s.shapes
         if sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and sh.width == sh.height]
pics  = [(round(sh.left/914400,3), round(sh.top/914400,3)) for sh in s.shapes
         if sh.shape_type == MSO_SHAPE_TYPE.PICTURE]
assert len(set(pics)) == len(pics), 'ICON TRUNG TOA DO'
```

Cùng lúc đó: đừng dùng `[BLUE, ORANGE, GREEN][j]` để chọn màu — sẽ `IndexError` ngay khi có dòng thứ tư. Dùng chỉ số vòng: `PALETTE[j % len(PALETTE)]`.

## 4. Tên tham số không được che tên hàm toàn cục

`def card(..., icon=None, ...)` che mất hàm `icon()` toàn cục dùng để nhúng icon → crash khi `card` gọi `icon(...)`. Đổi tên hàm thành `put_icon()` và giữ tham số `icon` cho ký hiệu chữ. Trước khi dựng, quét lại các chỗ gọi để chắc không còn tên cũ.

Cùng loại lỗi: **đừng đặt tên tệp trùng module stdlib**. Đặt `inspect.py` trong thư mục làm việc làm `lxml`/`python-pptx` gãy với `ImportError: cannot import name 'Presentation' ... circular import`. Đổi tên tệp là hết.

## 5. Khung nội dung phải tự co để không cấn vùng footer

Chiều cao dòng cố định làm khung code dài (9 dòng lệnh) tràn xuống vùng header/footer (`y >= 6.88 in`), sinh lỗi cắt chữ ở đúng thẻ footer. Tính chiều cao dòng theo số dòng:

```python
BOTTOM_MAX = 6.86                     # KHONG duoc cham vung footer
out_h = 0.52 if output is not None else 0.0
lh = min(0.46, (BOTTOM_MAX - top - 0.62 - out_h) / max(1, len(lines)))
csize = 13.5 if lh >= 0.42 else (12.5 if lh >= 0.36 else 11.5)
```

## 6. Patch script bằng chèn dòng: luôn compile lại ngay

Hai lần liên tiếp (hai bài khác nhau), script patch chèn các dòng của `notes = {...}` vào giữa khối `elif kind == ...` đang vẽ, tạo `SyntaxError: illegal target for annotation`. Nguyên nhân: bộ dò mốc chèn khớp sai vì `items = [` có thể thụt lề và dấu `]` nằm cùng dòng cuối.

Quy tắc:

1. Sau **mỗi** lần patch script, chạy `python3 -m py_compile <script>` trước khi dựng.
2. Khi `SyntaxError` chỉ vào một dòng của dict, đọc lại vùng ±20 dòng quanh đó — gần như chắc là dòng dict đã lọt vào khối vẽ.
3. Không dùng regex `^items=\[` để tìm mốc; đọc file bằng Python và so `line.strip().startswith('items')`.
4. Patch có nested triple-quote thì ghi ra tệp `.py` riêng rồi chạy, đừng nhúng trong chuỗi của `execute_code`.

## 7. Khi công cụ đọc tệp trả về thiếu nội dung

Với tệp tạo bằng script (quyền `0600`), `read_file` có thể trả về dict không có khoá `content` → `KeyError`. Đọc thẳng bằng Python và tự in kèm số dòng:

```python
src = open(path, encoding='utf-8').read().splitlines()
for i, l in enumerate(src, 1):
    print('%4d| %s' % (i, l[:160]))
```

Cách này cũng tránh việc `read_file` trả kèm số dòng làm lệch mọi phép so chuỗi khi định vị mốc patch.
