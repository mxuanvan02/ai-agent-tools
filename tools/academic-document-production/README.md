# Academic Document Production

Agent Skill quản lý **phần artifact** của văn bản học thuật: bao nhiêu từ và bao nhiêu
trang thì vừa, template nào là template thật, một file DOCX được cấu trúc và sửa thế
nào, phải kiểm gì trước khi nộp, cách dựng lại danh mục tài liệu, và công cụ dịch trả
văn bản về ra sao.

> `academic-prose` quyết định câu văn khẳng định điều gì. Skill này quyết định file
> mang câu văn đó có đúng quy cách, đầy đủ và kiểm chứng được hay không.

## Phân chia với `academic-prose`

Hai skill hỏng độc lập nhau. Một bản thảo có thể lập luận rất chắc mà vẫn dài hơn
giới hạn 400 từ, hoặc đúng số từ mà phần đánh số trang sai.

| Việc | Skill |
| --- | --- |
| Tuyên bố, lập trường, hedging, thuật ngữ, cú pháp sao phỏng tiếng Anh, move tu từ | `academic-prose` |
| Giới hạn từ/trang đo trên file đã render, template, DOCX, LaTeX, bibliography, kiểm tra trước khi nộp | skill này |

Khi cả hai cùng áp dụng, ranh giới là: nội dung câu thuộc `academic-prose`; tính hợp
quy cách của file chứa câu đó thuộc skill này.

## Nội dung

- **Ngân sách từ và trang** — đo trên artifact đã render, không đo trên source; quy
  đổi trang sang từ theo template thật của tạp chí.
- **Thẩm quyền quy cách** — chuỗi Bộ → đại học → đơn vị đào tạo; không gán một con số
  font/lề cho văn bản không quy định nó.
- **DOCX** — accepted view, sửa hàng loạt có kiểm soát, gate rà bản sửa.
- **LaTeX** — preflight trước khi nộp, caption và bảng, số hiệu chú thích.
- **Bibliography** — dựng lại danh mục từ dữ liệu có thể kiểm.
- **Tích hợp dịch PDF** — nhận văn bản dịch về đúng vị trí, giữ định dạng.

## Cài đặt

```bash
pip install -r tools/academic-document-production/requirements.txt
```

Tích hợp thủ công: đặt thư mục này ở vị trí môi trường khám phá được và đăng ký
`SKILL.md` làm hợp đồng định tuyến chính.

## Cách sử dụng

```text
Bản thảo này vượt giới hạn 6000 từ của tạp chí. Đo trên file DOCX đã render, chỉ ra
chỗ cắt được mà không mất tuyên bố nào, rồi cắt và đo lại.
```

```text
Trích xuất accepted text của file DOCX này, đối chiếu với bản tôi đã sửa, và liệt kê
mọi thay đổi chưa được chấp nhận.
```

## Kiểm tra

```bash
python3 scripts/public_hygiene_check.py     # không lộ thông tin nội bộ khi phát hành
python3 -m py_compile scripts/*.py
python3 scripts/verify_journal_docx.py --help
```

## Giấy phép

MIT. Xem `LICENSE`.
