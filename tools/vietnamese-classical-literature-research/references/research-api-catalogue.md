# Kho/API nghiên cứu đã xác minh (cập nhật 2026-10-22)

Đây là bản đồ **truy cập có cấu trúc**, không phải danh sách link tham khảo chung. Mỗi endpoint
bên dưới đã được gọi thật; `HTTP 200` chỉ chứng minh endpoint phục vụ dữ liệu, không tự động chứng
minh dữ liệu phù hợp cho mọi câu hỏi.

## 1. Kho Việt Nam — ưu tiên dùng trước

### HCMUSSH DSpace 7 — kho thư viện số Khoa học Xã hội và Nhân văn

- Trang: `https://elib.hcmussh.edu.vn/`
- REST discover:

```
https://elib.hcmussh.edu.vn/server/api/discover/search/objects?query=H%C3%A1n%20N%C3%B4m&size=20
```

- Đã đo: HTTP 200, JSON HAL. Query `Hán Nôm` cho **1.620** kết quả trong lần khảo sát.
- Mẫu thật: `Cơ sở ngữ văn Hán Nôm. T.4` — Lê Trí Viễn, 1987, 340 tr.;
  `Khảo sát hệ thống văn bản truyện thơ Nôm Kinh trong kho sách của Viện Nghiên cứu Hán Nôm` —
  2025.
- Có metadata: tên, tác giả, năm, chủ đề, số trang, handle, UUID, URI.
- Lưu ý: `/server/api/core/items` trả 401; dùng `discover/search/objects`, không đoán endpoint
  core. DSpace 7 đặt item ở `_embedded.searchResult._embedded.objects[]._embedded.indexableObject`.

### VNU-CRIS — kho nghiên cứu ĐHQGHN

- Trang: `https://scholar.vnu.edu.vn/`
- REST discover:

```
https://scholar.vnu.edu.vn/server/api/discover/search/objects?query=h%C3%A1n%20n%C3%B4m&size=20
```

- Đã đo: HTTP 200, JSON HAL.
- Mẫu thật: bài về địa danh gốc Hán ở Việt Nam; bài trên **Tạp chí Hán Nôm** về địa danh và
  ngữ nghĩa.
- Lưu ý: `/server/api/core/items` trả 401; `/oai/request` không phải OAI-PMH hoạt động.

## 2. Tạp chí OAI-PMH — dùng để harvest metadata

### VNU Journal of Science — SSH

```
https://js.vnu.edu.vn/SSH/oai?verb=Identify
https://js.vnu.edu.vn/SSH/oai?verb=ListRecords&metadataPrefix=oai_dc
```

- Identify và ListRecords: HTTP 200, XML OAI-PMH.
- **Giới hạn quan trọng:** `from=2024-01-01` trả `noRecordsMatch`; bỏ `from` thì có khoảng
  84 KB bản ghi, nhưng mẫu đầu chủ yếu `status="deleted"`, datestamp 2016. Không coi HTTP 200
  là kho bài đang harvest tốt; dùng VNU-CRIS để tìm bài cụ thể.

### Tạp chí khoa học của một đại học — OAI-PMH SSH

- Một tạp chí khoa học dùng OJS có OAI-PMH mở, đã đo HTTP 200 với `oai_dc`, có set SSH và
  metadata song ngữ.
- Host của tạp chí nằm trong **registry cục bộ** (không ship trong repo công khai vì gate
  hygiene chặn định danh cơ quan/venue):

```
~/.hermes/data/van-hoc-kho/endpoints.local.json
```

- Dùng qua tên corpus `local:<key>`:

```bash
python3 scripts/research_api.py local:hujos-ssh --from-date 2024-01-01 --limit 20
```

- Dùng để lấy danh mục bài mới, sau đó mở trang bài để đọc toàn văn.

### Tạp chí Khoa học Đại học Đà Lạt

```
https://tckh.dlu.edu.vn/index.php/tckhdhdl/oai?verb=Identify
https://tckh.dlu.edu.vn/index.php/tckhdhdl/oai?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01
```

- Đã đo: HTTP 200, XML OAI-PMH; response khoảng 359 KB, có record sống.
- Dùng `oai_dc` để lọc title, creator, subject, date; không cần đăng nhập.

## 3. Thủ bản/ảnh số quốc tế

### Columbia University — Hán-Nôm Sino-Vietnamese Textual Library

- Collection: `https://dlc.library.columbia.edu/npf_vietnamese`
- IIIF Presentation 3:

```
https://dlc.library.columbia.edu/iiif/3/presentation/10.7916/d8-rzke-ja79/manifest
```

- Đã đo: HTTP 200, manifest có **68 canvas**, nhãn `Kim Vân Kiều`.
- IIIF Image API mẫu:

```
https://triclops.library.columbia.edu/iiif/2/standard/cul:zgmsbcc5rq/info.json
```

- Đã đo: HTTP 200, trả kích thước ảnh và profile IIIF.
- MODS:

```
https://dlc.library.columbia.edu/catalog/cul:2jm63xsm89/mods
```

- Đã đo: HTTP 200, XML MODS. Mẫu là *Kim Vân Kiều*, mã R.274, 68 trang.
- OAI bị PoW chặn; dùng manifest + MODS + Image API. Đây là nguồn phù hợp nhất để đối chiếu
  văn bản Nôm bằng ảnh trang, không dùng OCR thay cho đọc ảnh.

### EFEO / Calames

- Mục lục EFEO fonds VIET:

```
https://calames.abes.fr/pub/ms/Calames-202141415248109875
```

- Đã đo: HTTP 200, trang mục lục HTML.
- Trang giới thiệu bộ sưu tập:
  `https://www.efeo.fr/collection/manuscrits-et-imprimes-en-han-nom/` — HTTP 200.
- Mẫu fonds: *Lão bạng sinh châu diễn truyện* (kịch Nôm); *Phật thuyết tạo tượng lượng độ kinh*.
- `archives.efeo.fr` tồn tại nhưng browser-only/cert lỗi từ môi trường này; OAI không mở.

### Internet Archive

- Tìm sách:

```
https://archive.org/advancedsearch.php?q=title%3A%28%22Truy%E1%BB%81n+k%C3%AC+m%E1%BA%A1n+l%E1%BB%A5c%22%29&fl%5B%5D=identifier&fl%5B%5D=title&fl%5B%5D=creator&fl%5B%5D=year&rows=20&output=json
```

- Đã đo: HTTP 200; tìm được `ARC.HOANG.120` và `ARC.HOANG.121`, người tạo Nguyễn Dữ,
  năm 1930.
- Metadata/files:
  `https://archive.org/metadata/ARC.HOANG.46` — HTTP 200; dùng để tìm PDF/JPEG/OCR.
- OCR mẫu `_djvu.txt` có HTTP 200 nhưng chữ Hán/Nôm nhiễu mạnh. Phải tải PDF/JP2 và đọc ảnh.

## 4. API đối chiếu văn bản và sách

### OpenAlex

```
https://api.openalex.org/works?filter=title_and_abstract.search:%22v%C4%83n%20h%E1%BB%8Dc%20trung%20%C4%91%E1%BA%A1i%22,type:article&per-page=20
```

- Đã đo: HTTP 200.
- Cú pháp cần dùng: `title_and_abstract.search`, giữ dấu tiếng Việt. Tham số `search=` quá rộng,
  có thể trả bài y tế khi tìm tên người Việt.
- Mẫu thật: bài về *Truyền kì mạn lục*, chữ Nôm, văn học trung đại Việt Nam.
- `abstract_inverted_index` có thể vắng; không tự suy ra abstract khi trường không có.

### CORE

```
https://api.core.ac.uk/v3/search/works?q=Vietnamese%20literature
```

- Đã đo: HTTP 200 JSON, nhưng phải kiểm tra quota/key nếu harvest lớn. Kết quả trả metadata
  học thuật; không nhầm HTTP 200 với quyền tải toàn văn.

### HAL

```
https://api.archives-ouvertes.fr/search/?q=litt%C3%A9rature%20vietnamienne&fl=title_s,producedDate_s,uri_s&rows=20&wt=json
```

- Đã đo: HTTP 200 JSON; lần khảo sát trả 87 kết quả.
- Hữu ích cho bài tiếng Pháp, luận văn và metadata liên quan Đông Dương/Việt Nam.

### Open Library

```
https://openlibrary.org/search.json?q=Truyen+ki+man+luc&limit=20
```

- Đã đo: HTTP 200 JSON; query trả 3 kết quả trong lần khảo sát.
- Dùng để xác nhận edition/ISBN/bibliographic lead, không mặc nhiên coi bản ghi là bản số hóa.

### Wikisource tiếng Trung

```
https://zh.wikisource.org/w/api.php?action=query&list=search&srsearch=%E8%B6%8A%E5%8D%97&format=json
```

- Đã đo: HTTP 200 JSON, tìm được 4.325 hit cho `越南` trong lần khảo sát.
- Dùng đối chiếu chữ Hán và tìm văn bản; không dùng làm nguồn học thuật cuối cùng.

### Kanripo raw GitHub

```
https://raw.githubusercontent.com/kanripo/KR1a0001/master/KR1a0001_001.txt
```

- Đã đo: HTTP 200 text/plain.
- Dùng đọc nhanh văn bản Hán cổ; sau đó quay về bản in/bản chụp để xác định dị bản.

## 5. Không nên mất thời gian tự động ở lượt này

- **BASE:** endpoint trả `Access denied` theo IP/user-agent hiện tại.
- **DOAJ:** trả 502 từ môi trường hiện tại; cần retry/browser trước khi kết luận.
- **Persée:** request API timeout trong lần đo.
- **OpenEdition RSS path đã thử:** 404; không dùng path đoán này làm API.
- **Gallica, LoC API, SOAS Digital sâu:** bị WAF/PoW hoặc browser-only; dùng browser khi cần.
- **VNU OAI:** endpoint sống nhưng dữ liệu hiện ra chủ yếu đã deleted; ưu tiên VNU-CRIS.

## 6. Lệnh dùng nhanh

```bash
# Danh sách connector
python3 scripts/research_api.py --list

# Kiểm tra endpoint
python3 scripts/research_api.py --probe

# DSpace luận văn/sách Hán-Nôm
python3 scripts/research_api.py dspace-hcmussh "Hán Nôm" --limit 20
python3 scripts/research_api.py dspace-vnu "truyện thơ Nôm" --limit 20

# OAI bài báo
python3 scripts/research_api.py local:hujos-ssh --from-date 2024-01-01 --limit 20
python3 scripts/research_api.py oai-dlu --from-date 2024-01-01 --limit 20

# Ảnh thủ bản IIIF
python3 scripts/research_api.py columbia-iiif

# Sách số hóa
python3 scripts/research_api.py archive "Truyền kì mạn lục" --limit 20
python3 scripts/research_api.py archive-metadata ARC.HOANG.46
```
