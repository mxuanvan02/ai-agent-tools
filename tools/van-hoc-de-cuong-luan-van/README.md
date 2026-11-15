# van-hoc-de-cuong-luan-van

Khung đề cương luận văn / luận án ngành **Văn học**.

## Mục đích

Khi soạn, rà hoặc bảo vệ một đề cương luận văn ThS / luận án TS thuộc các ngành văn học (Văn học
Việt Nam, Văn học nước ngoài, Lý luận văn học, Văn học so sánh), skill này cung cấp:

- **chín mục** theo đúng thứ tự hội đồng đọc;
- **thiết kế câu hỏi nghiên cứu** dạng diễn giải (không phải giả thuyết kiểm chứng);
- **ba loại khoảng trống nghiên cứu** xếp theo độ mạnh, kèm cách viết an toàn;
- **tách mục đích khỏi nhiệm vụ** và các phép kiểm đi kèm;
- **danh mục phương pháp** với thao tác cụ thể và cảnh báo khái niệm mượn ngành;
- **khung kỹ thuật để đối chiếu** — để thấy rõ hai khung khác nhau ở đâu, không để trộn.

## Ranh giới quan trọng nhất

Skill này là một bộ khung **hình thức và phương pháp luận**, không phải bộ mẫu điền sẵn cho một đề
tài cụ thể. Nó cố ý không nêu tên tác phẩm, tác giả hay lĩnh vực hẹp nào: một khung bị gắn với một đề
tài sẽ bị đọc như đề cương của đề tài đó, và mọi chỗ khác dùng lại đều sai. Kiến thức nền theo lĩnh
vực hẹp nằm ở skill chuyên ngành tương ứng.

## Cấu trúc

| File | Nội dung |
|---|---|
| `SKILL.md` | Điểm vào: nguyên tắc nền, chín mục, quy tắc, sáu lỗi, validation |
| `references/proposal-skeleton.md` | Chín mục chi tiết, yêu cầu cốt lõi, lỗi thường gặp từng mục |
| `references/research-question-design.md` | Câu hỏi chính/phụ, bảng dạng sai–dạng đúng, phép thử |
| `references/gap-and-contribution.md` | Ba loại khoảng trống, công thức viết, kiểm tra khớp đóng góp |
| `references/methods-catalogue.md` | Danh mục phương pháp, thao tác, cảnh báo khái niệm mượn ngành |
| `references/engineering-contrast.md` | Khung kỹ thuật để đối chiếu, bảng dịch thuật ngữ |

## Validation

```bash
python3 tools/van-hoc-de-cuong-luan-van/scripts/public_hygiene_check.py
python3 -m py_compile tools/van-hoc-de-cuong-luan-van/scripts/*.py tools/van-hoc-de-cuong-luan-van/tests/*.py
python3 -m unittest discover -s tools/van-hoc-de-cuong-luan-van/tests -v
```

## Phân loại lĩnh vực

Đây là một tool thuộc lĩnh vực **văn học** (`metadata.hermes.category: van-hoc`), nằm cạnh các công
cụ kỹ thuật trong monorepo. Phân loại này đi theo skill để trình cài đặt tôn trọng nó có thể nhóm
riêng theo lĩnh vực.