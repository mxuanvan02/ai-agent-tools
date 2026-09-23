# Phát hiện & sửa reference bịa (LM hallucination) trong manuscript LaTeX

Dùng khi người dùng nói "nhiều bibtex hallucination", "rà kĩ hơn", "references sạch chưa",
hoặc khi file .bib có dấu hiệu sinh bằng LM. Đây là bước SÂU hơn dedup/cú pháp thông thường.
Bài có tên người dùng ⇒ một reference bịa lọt qua = mất uy tín với reviewer, nên làm rất chặt.

## Nguyên tắc cốt lõi
- **DOI lookup là nguồn chân lý**, KHÔNG phải title-search ranking. Crossref `query.bibliographic`
  hay xếp nhầm "Faculty Opinions recommendation", bài review, supplement, hoặc bài mới hơn lên đầu.
- **Chỉ verify key được CITE thật** (đọc từ `.aux`: `grep '\\citation' *.aux` hoặc `\bibcite`).
  Bib thường chứa nhiều entry thừa không cite — BibTeX chỉ render cái được `\cite`, nên ưu tiên
  62→0 entry thừa sau, verify entry hiển thị trước.
- **KHÔNG sửa mù theo máy chấm.** Phần lớn "diff" tự động là dương tính giả. Chỉ sửa khi có
  bằng chứng DOI chính tắc. Sửa ẩu trên bài có tên tác giả là tệ hơn không sửa.

## Các kiểu hallucination thực tế đã gặp (4 + 3)
**Nhóm sai metadata (bài CÓ THẬT, DOI đúng nhưng trường bịa):**
- Bịa tác giả đầu: bib ghi "Ding, H." → DOI thật cho tác giả "Liu Songbo et al." (Front Microbiol).
- Bịa tác giả: "Taha, Kamal" → thật "Ibrahim A.H. et al." (PLOS ONE).
- Sai vị trí tác giả: "Cong, Qian and others" → Cong là tác giả CUỐI (Zhang, Durham, Cong).
- Gắn nhầm tiêu đề: title "The organizing principles..." nhưng DOI thật là
  "Prediction of physical protein–protein interactions" (cùng tác giả/journal/năm).

**Nhóm bịa hẳn (không tồn tại ở Crossref/S2/arXiv):**
- Key giả + tên method giả (vd "KG-PPI / Xu Bin, TCBB 2024" không tồn tại) → thay bằng bài thật
  gần nhất cùng journal/năm/chủ đề (Yang et al., KG-fused GNN, TCBB 2024;21(6):2518–2530).
- Title bịa → thay bằng bài thật đúng ngữ cảnh câu đang cite.

**Misattribution tên baseline trong PROSE (không nằm ở .bib):** bib entry đúng (RAPPPID,
AWD-LSTM twin networks) nhưng prose gọi sai tên "RAFT-PPI" + mô tả kỹ thuật sai
"residue-attention fusion" ở 8 chỗ (prose + bảng). grep tên method, đối chiếu key cite với
metadata thật, sửa đồng loạt tên + câu mô tả kỹ thuật.

## Báo động giả điển hình — KHÔNG đụng
- Lệch năm online-first vs in-print: Crossref trả năm online, bib ghi năm số/volume in.
  Nếu volume/issue khớp thì bib ĐÚNG theo quy ước trích dẫn. (huang2009, chou2005, oughtred2019,
  kumar2022/2024, chatr2017, hu2022, blohm2014, vig2020, elnaggar2021...)
- Crossref match nhầm reprint/erratum/Faculty Opinions: bài kinh điển (Random Forests 2001,
  Attention 2017, SHAP NeurIPS 2017, Doshi-Velez arXiv) bib đúng, Crossref xếp hạng kém.

## Quy trình
1. `git`/cp backup .bib vào `_backups/<ts>/` trước khi đụng.
2. Lấy cited keys từ `.aux`. Parse .bib bằng Python (KHÔNG ripgrep — vướng `{}`, lỗi
   "Unmatched \\{" / "Invalid content of \\{\\}"; dùng brace-depth scan trong execute_code).
3. Đối chiếu 2 nguồn: Crossref `query.bibliographic` + Semantic Scholar
   `graph/v1/paper/search`. LƯU Ý S2 hay 429 (rate-limit) ⇒ retry backoff 3*(t+1)s; khi S2 chết
   thì thực chất chỉ còn Crossref, phải tự đọc bằng mắt.
4. Với entry nghi vấn: fetch THẲNG metadata theo DOI (`api.crossref.org/works/{doi}`) — nguồn
   không nói dối — để lấy tác giả/title/volume/pages chuẩn.
5. Phân loại: lỗi metadata (bài thật) → vá đúng trường; bịa hẳn → thay bài thật verify DOI;
   báo động giả → giữ nguyên. BÁO NGƯỜI DÙNG danh sách + cho người dùng chọn nhóm "nghi bịa" (thay/xóa).
6. **Viết lại prose**: khi tên/title bị bịa, câu đang cite có thể mô tả nội dung bài BỊA.
   Sau khi thay bằng bài thật, đọc câu `\cite{key}` và sửa cho khớp bài thật (vd KG-fused GNN
   thay vì "logical relations", AWD-LSTM twin thay vì "residue-attention fusion").
7. Khi đổi title một entry, kiểm câu đang cite nó còn hợp ngữ cảnh không; nếu lệch, chuyển cite
   sang câu phù hợp hoặc thay bằng review đúng chủ đề (vd self-cite, de2010protein cho vai trò
   sinh học) — verify DOI trước khi đưa bài mới vào.
8. Self-citation: bài cùng nhóm/cùng chủ đề (vd truong2025predicting có tên người dùng) cite được
   và có lợi; chèn vào cụm đúng ngữ cảnh (early-ML/handcrafted feature) rồi đưa lại entry vào bib.
9. Rebuild đầy đủ: pdflatex → bibtex → pdflatex ×2. Verify: 0 undefined citation/reference,
   0 BibTeX warning (`warning$ -- 0` trong .blg), đếm bbl ref = số cite, render đúng tên mới.
10. Prune entry không cite cuối cùng (giữ đúng N cite). Backup trước, verify cited-but-missing=[].

## RLM duyệt cuối (người dùng hay yêu cầu "dùng RLM chốt")
Spawn 3 subagent song song, mỗi cái một mặt độc lập, chỉ-đọc:
(1) số liệu prose↔bảng + quy ước in đậm theo caption;
(2) toàn vẹn tham chiếu (cite/ref/label/figure orphan, undefined, build log);
(3) chất lượng học thuật/ngôn ngữ (ngữ pháp, thuật ngữ nhất quán, lộ chi tiết triển khai,
    misattribution baseline, claim mạnh thiếu bằng chứng).
Subagent (3) là cái hay bắt được hallucination tên baseline + lộ implementation.

## Lộ chi tiết triển khai nội bộ (người dùng CẤM để lọt bản công bố)
Quét và xóa: "CSV result table", "feature-engineering code", "local benchmark package",
"evaluation files", tên file/biến/pipeline nội bộ. Thay bằng ngôn ngữ học thuật
("As reported in these tables", "Each protein is represented by", "evaluation splits and protocol").
