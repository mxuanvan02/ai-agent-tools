# Phát hiện citation "ma" (AI-hallucinated / mis-spliced) trong references.bib

Bệnh thường gặp KHÔNG phải cả bibliography bị bịa, mà là vài entry lẻ bị AI
ghép sai: tên tác giả THẬT + tiêu đề/journal/toạ độ KHÔNG tồn tại. Mục này là
quy trình xác minh và các dấu hiệu nhận diện đã kiểm chứng trên thực tế.

## Quy trình xác minh (đối chiếu 2 CSDL độc lập)

Với mỗi entry nghi vấn, query CẢ Crossref VÀ OpenAlex (đừng tin một nguồn):

1. **Theo tiêu đề** — Crossref `bibliographic` + OpenAlex `search`. Không có
   bản ghi nào khớp tiêu đề ⇒ cờ đỏ mạnh.
2. **Theo tác giả + chủ đề** — xác minh tác giả đó CÓ thực sự viết bài về chủ
   đề này không. Tác giả thật nhưng lĩnh vực lệch (vd Ian Walsh làm protein
   stability/aggregation, KHÔNG làm đánh giá độ chính xác PPI) ⇒ tên bị mượn.
3. **Theo toạ độ tập/số/trang** — query `container-title` + volume + năm trên
   Crossref, kiểm tra đúng pages đó có chứa bài này không. Toạ độ trỏ tới bài
   khác (hoặc trống) ⇒ bịa.

### Snippet API (chạy trong execute_code)

```python
import urllib.request, urllib.parse, json
def crossref_title(q, rows=5):
    u = "https://api.crossref.org/works?" + urllib.parse.urlencode(
        {"query.bibliographic": q, "rows": rows})
    req = urllib.request.Request(u, headers={"User-Agent": "ref-audit/1.0 (mailto:anhvan)"})
    return json.load(urllib.request.urlopen(req, timeout=20))["message"]["items"]
def openalex_title(q, rows=5):
    u = "https://api.openalex.org/works?" + urllib.parse.urlencode(
        {"search": q, "per-page": rows})
    return json.load(urllib.request.urlopen(u, timeout=20))["results"]
```

**Pitfall:** OpenAlex trả JSON lớn → output terminal bị cắt ở mốc ~20k ký tự
("Invalid control character at line 1 column 20001"). GHI kết quả ra file rồi
parse, hoặc chỉ in các field cần (title/author/year/doi), đừng dump raw.

## Dấu hiệu nhận diện entry "ma" (không cần API cũng ngờ được)

- `author = {... and others}` ở bài mà bản gốc có số tác giả xác định, kèm
  metadata thiếu (thiếu `number`, thiếu `pages`).
- Tên tác giả nổi tiếng bị gán vào tiêu đề/journal sai (vd "Richard B.
  Silverman" — tác giả sách Organic Chemistry of Drug Design — bị gán cho một
  review PPI-targeted drug discovery không tồn tại).
- Tiêu đề "đẹp hợp lý" + journal uy tín + toạ độ tròn trịa nhưng không tra ra.
- **Key không khớp nội dung:** key đặt theo tên+năm (vd `srinivasan2007protein`)
  nhưng metadata bên trong là tác giả+năm khác (Park 2009, BMC Bioinformatics
  10:419). Luôn rà cả sự khớp giữa KEY và NỘI DUNG, không chỉ nội dung.

## Thay thế đúng ngữ cảnh

Trước khi đề xuất ref thay, GREP `\cite{<key>}` trong .tex để biết câu văn cần
ref kiểu gì, rồi tìm bài THẬT cùng ngữ cảnh và verify DOI qua Crossref:
- Ngữ cảnh "PPI là đích trị liệu/drug discovery" → vd Lu et al. 2020, Signal
  Transduct. Target. Ther., DOI 10.1038/s41392-020-00315-3.
- Ngữ cảnh "rò rỉ dữ liệu/lỗi đánh giá do tương đồng" → vd Hamp & Rost 2015,
  Bioinformatics, DOI 10.1093/bioinformatics/btu857.

**Pitfall grep:** `\cite` chứa dấu `{` làm regex lỗi "Unmatched \{". Escape
hoặc search literal `cite{` thay vì `\cite{`. Citation có thể nằm rải trong
nhiều lệnh `\cite{a,b,c}` — search theo từng key, không theo cả cụm.

## Báo cáo

Bảng cho mỗi entry: cờ kiểm chứng (title / toạ độ / tác giả-chủ đề) + kết luận
(phantom hay thật), bối cảnh trích dẫn, và 1-2 ứng viên thay thế đã verify DOI.
KHÔNG tự sửa .bib khi chưa được chốt — backup `_backups/<ts>/` trước, hỏi người dùng
người dùng chọn ref thay thế hoặc cho phép áp luôn.
