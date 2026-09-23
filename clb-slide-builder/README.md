# CLB Slide Builder

Script tạo slide PPTX cho Câu lạc bộ Năng lực số và Ứng dụng AI.

## Cách sử dụng

```bash
python3 gen_deck_clb_simple.py /path/to/noi_dung.json
```

## Cấu trúc JSON

File JSON cần có các trường:
- `bai_so`: Số thứ tự bài
- `ten_bai`: Tên bài học
- `tiet`: Số tiết (ví dụ: "1", "2")
- `tuan`: Số tuần
- `khoi_dong`: Phần khởi động
- `muc_tieu`: Mục tiêu bài học
- `phan`: Nội dung chính (3 phần)
- `luyentap`: Luyện tập
- `vandung`: Vận dụng
- `tong_ket`: Tổng kết
- `tom_tat_vo`: Tóm tắt vở
- `ket_thuc`: Kết thúc

## Output

- File PPTX với 9-10 slides
- Tự động upload lên Google Drive
- Verify SHA256
