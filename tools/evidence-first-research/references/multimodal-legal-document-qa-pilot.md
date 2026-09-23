# Multimodal legal/document QA: evidence-first pilot protocol

Dùng khi phát triển benchmark hoặc phương pháp QA trên PDF giáo trình, tài liệu pháp lý, tài liệu nhiều trang có text–image–layout và metadata nguồn.

## 1. Gate trước khi gọi dữ liệu là multimodal

Không suy ra “multimodal” chỉ vì PDF được rasterize thành ảnh hoặc có vài trang chứa sơ đồ. Audit ở cấp item:

- representation thực tế: native text, OCR, page pixels, table, figure, layout;
- evidence có định vị được tới document checksum → PDF page/printed page → bbox/polygon không;
- câu hỏi có thật sự cần pixels hoặc quan hệ 2-D không;
- text/OCR-only có còn đủ answer atoms không.

Nhãn khuyến nghị: `text_sufficient`, `layout_helpful`, `visual_required`, `multimodal_required`. Với item cần vision/layout, bắt buộc có `visual_necessity_rationale` và kiểm tra che/thay vùng visual. Nếu caption/OCR thay pixel mà hiệu năng tương đương, framing đúng là textualized/document QA, chưa phải visual reasoning.

## 2. Metadata là biến nghiên cứu, không phải phần trang trí

Tách entity tối thiểu:

- **Document:** opaque ID, SHA-256, title, author/publisher, edition, publication date, course, legal domain, jurisdiction, license, source family, page offset, ingestion version.
- **Legal time/version:** `law_as_of`, `effective_from/to`, supersedes/amends/repeals; không suy “luật hiện hành” từ năm xuất bản giáo trình.
- **Asset/evidence:** representation, page PDF/trang in, bbox/polygon, exact span/crop, OCR lineage, parent asset, image hash.
- **QA item:** answer atoms, evidence refs, required modalities, metadata relevance, source-family split, answerability, counterfactual group, creation provenance.
- **Annotation:** nhãn độc lập, qualification, evidence/modality/legal-validity decision, confidence, adjudication và change history.

Metadata đưa vào query/retrieval không được chứa answer, evidence ID hay split label. Luôn log candidate pool trước và sau metadata filtering.

## 3. Pilot có khả năng bác bỏ claim

Trước khi xử lý toàn corpus, dựng pilot có contrast thật:

- nhiều source families, ít nhất vài loại visual element;
- visual-dependent items đã adjudicate;
- metadata-conflict/counterfactual pairs có đáp án hoặc evidence thay đổi theo edition, legal time, course hoặc jurisdiction;
- matched text-only controls;
- split theo source family, deduplicate trước khi split;
- hai annotator độc lập và legal adjudication.

Không chuyển corpus QA text hiện có thành benchmark multimodal bằng cách thêm trường modality hậu nghiệm nếu chưa có page/region evidence và necessity test.

## 4. Ma trận causal ablation

Giữ answer model, prompt budget, candidate count và corpus cố định; thay một yếu tố mỗi lần:

1. sparse text, không metadata;
2. dense text, không metadata;
3. text + metadata đúng;
4. text + metadata random;
5. text + metadata sai nhưng hợp lý;
6. text + original page pixels, không metadata;
7. full multimodal + metadata đúng;
8. full system + metadata random/sai;
9. oracle text evidence;
10. oracle pixels với text layer được mask theo protocol;
11. caption/OCR thay pixels;
12. bỏ layout coordinates.

Báo riêng retrieval, answering, citation, legal validity, abstention, calibration, latency/cost và kết quả theo modality/source family/domain.

## 5. Claim gates

- **Vision:** full visual system phải hơn strong text baseline trên adjudicated visual subset với clustered CI không chứa 0; caption/OCR substitution phải kém rõ ràng.
- **Metadata:** metadata đúng phải hơn cả absent/random/wrong metadata trên counterfactual pairs; field completeness và disagreement phải được báo cáo.
- **Citation:** evidence ID phải resolve được tới checksum, page và region; “có citation string” không phải citation correctness.
- **Benchmark readiness:** không source-family leakage, có license/reproducible access, expert gold, frozen manifests, prompts/models/seeds và clean reproduction.

Nếu gate thất bại, bỏ hoặc thu hẹp claim trong title/abstract; không tune lại test để cứu claim.

## 6. Mốc Q1/Q2 và bibliography hygiene

- Quartile mô tả **venue**, không bảo chứng chất lượng manuscript.
- Ghi rõ database (`SJR/SCImago` hoặc `JCR`), category, year, quartile, URL và access date; không trộn SJR với JCR.
- Conference benchmark là technical anchor/baseline, không phải bằng chứng “journal Q1/Q2”.
- Xác minh DOI/title/journal bằng Crossref hoặc publisher trước; title gần giống có thể dẫn tới DOI của bài khác.
- Nếu không truy cập được record quartile chính thức, đánh dấu `quartile_pending_verification`, không gán theo danh tiếng.

## 8. Fusion phải phục vụ đúng contribution trung tâm

Nếu contribution trung tâm là **sinh genuinely multimodal TQA**, đọc thêm `references/evidence-first-multimodal-tqa-generation.md`. Khóa paper vào trục:

`evidence motif → executable program → answer atoms → question realization → counterfactual modality audit`.

Trong trường hợp này, online answering/RAG chỉ là downstream check, không được chiếm trục phương pháp; metric generation phải ưu tiên grounding, modality-necessity precision và text-leakage rate. Không dùng retrieval diagnostic của corpus/bài khác để thay thế kết quả multimodal.

Khi đề tài rộng hơn là **xây dựng/sinh TQA và trả lời**, không được vẽ kiến trúc như thể multimodal fusion chỉ đứng trước Answerer. Phải tách hai pipeline dùng chung một **typed evidence representation/fusion interface**:

### Offline TQA generation

`PDF + provenance → text/OCR + page pixels/crops + layout graph → cross-modal linking → fused evidence graph → question blueprint → joint question/answer/evidence generation → necessity/quality gates → audited TQA item`.

Question Generator phải nhận ngữ cảnh đã liên kết giữa các modality, không sinh câu hỏi từ OCR rồi gắn hình sau. Mỗi blueprint ghi rõ operation, answer form và required modalities, ví dụ `follow diagram branch → link same entity to table row → retrieve deadline`. Output tối thiểu gồm question, answer atoms, reasoning operations, evidence refs, page/region, required modalities và necessity rationale.

### Online TQA answering

`Question + optional metadata → parallel text/visual/layout retrieval → metadata filter/rerank → query-conditioned fusion → evidence pack → grounded answer + citation/abstention`.

Không nói hai nhánh dùng “cùng toàn bộ fused context” nếu offline thấy full graph còn online chỉ thấy top-k evidence. Cách nói đúng là: **dùng chung typed evidence representation và fusion interface; online có thêm retrieval và evidence budget**.

### Ví dụ kiểm tra tính multimodal

Nếu flowchart cho biết nhánh `Thiếu → Yêu cầu bổ sung`, còn bảng ghi `Yêu cầu bổ sung → 05 ngày`, item phù hợp là: “Nếu hồ sơ thiếu, bước tiếp theo là gì và thời hạn bao lâu?”. Bỏ flowchart thì mất bước tiếp theo; bỏ bảng thì mất thời hạn. Câu chỉ hỏi “Thời hạn yêu cầu bổ sung?” là table/text QA, không phải multimodal mạnh.

## 9. Formalization tối thiểu cho evidence graph

Để tránh evidence graph chỉ là tên mới của document graph/RAG index:

- node: stable ID, type, document/page ID, normalized polygon, modality, extraction confidence, provenance pointer;
- edge: typed relation, direction, confidence, provenance pointer;
- lineage: PDF hash → rendered page → crop/span/layout object → citation;
- output: `(answer, evidence regions, confidence, answer atoms/claims, answerability)`;
- mỗi answer atom phải resolve về document–page–region, nếu không thì abstain;
- metadata chỉ là filter/rerank feature; chạy metadata-only control để phát hiện leakage.

Visual-necessity label phải được gán **trước model evaluation** bởi annotator độc lập trên frozen evidence conditions. Nên phân biệt `text_recoverable`, `layout_dependent`, `pixel_dependent`, `cross_modal`, `unanswerable`; caption-only không đủ để tách layout dependence khỏi pixel dependence.

## 10. Short IEEE architecture/protocol paper gate

Khi dữ liệu chưa đủ benchmark hoặc chưa có kết quả, frame là **architecture and evaluation protocol**, không phải performance paper. Trong bài 2–4 trang:

1. Nêu failure case thực tế trước công nghệ.
2. Khẳng định rõ contribution không phải encoder mới, mà là tổ hợp testable: evidence schema, joint TQA generation/answering interface, metadata/version controls, necessity validation, citation và abstention.
3. Công khai corpus status và source-family count; blank/sample cùng template không phải nguồn độc lập.
4. Không dùng “preregistered”, “audited”, “reproducible”, “ready” nếu chưa có artifact/record tương ứng; dùng “prospectively specified”, “proposed”, hoặc “design target”.
5. Có ablation tối thiểu: text, text+layout, text+pixels, full, no-metadata, no-cross-modal-links; split theo family.
6. Build sạch nhiều vòng; kiểm tra page limit, undefined citations/references, overfull boxes, embedded fonts, từng trang render và hình ở kích thước xuất bản.
7. Author/affiliation placeholder là blocker camera-ready. Không gọi “submission-ready” trước khi thay và xác minh.
8. Sau producer review, phải có critic độc lập; sửa claim/logic/formalization rồi rebuild và kiểm tra ZIP integrity + manifest/checksum.

Khi một tool phụ trợ lỗi do setup, tiếp tục bằng workflow học thuật chính và báo blocker ngắn gọn; không để phản hồi người dùng trống sau tool calls.

## 11. Cô lập corpus và kết quả giữa các bài

Khi nhiều bài cùng dùng TQA, cùng workspace hoặc cùng nguồn PDF, phải lập provenance trước khi đưa số liệu vào manuscript:

`claim/result → run artifact → dataset/corpus → paper/project owner`.

Chỉ dùng corpus, baseline, bảng số liệu và metric khi cả bốn mắt xích thuộc đúng bài đang viết. Không được nhập kết quả từ bài text-centric vào bài multimodal chỉ vì cùng chủ đề hoặc cùng thư mục. Nếu attribution chưa chắc chắn, giữ ngoài manuscript và đánh dấu `PENDING_PROJECT_ATTRIBUTION`.

Với bài multimodal, kết quả cốt lõi phải trực tiếp kiểm tra modality dưới điều kiện đối chứng phù hợp, tối thiểu `Text-only`, `Text+Layout`, và `Full Text+Layout+Pixels`; retrieval diagnostic của một corpus text khác không thay thế được multimodal evidence.

Khi người dùng sửa attribution:

1. Thừa nhận lỗi ngắn gọn, không biện hộ.
2. Sao lưu manuscript/artifact hiện tại.
3. Tìm và loại kết quả nhiễm khỏi toàn bộ abstract, results, table, discussion, conclusion và artifact mô tả liên quan.
4. Định vị lại contribution, RQ, hypothesis và experiment theo đúng mục tiêu của bài.
5. Build lại; kiểm tra page count, citation/reference, log và PDF render trước khi báo hoàn tất.
6. Ghi ranh giới dự án vào memory để tránh tái nhiễm ở phiên sau.

Ví dụ ranh giới đã xác lập: ICTC MetaLegalTQA là bài multimodal; corpus 5.741/2.371 và BM25 Recall/MRR của bài AAG không phải kết quả ICTC và không được dùng để chứng minh multimodal gain.

## 12. Artifact tối thiểu

- `documents.jsonl`, `assets.jsonl`, `items.jsonl`, `annotations.jsonl`;
- JSON Schemas và integrity validator;
- frozen split manifest + duplicate report;
- experiment configs và raw run artifacts;
- architecture source có thể chỉnh sửa + SVG/PDF vector;
- benchmark card, annotation handbook, claim checklist và limitation/licensing statement.

Sơ đồ bài báo phải tách rõ offline ingestion/indexing, online retrieve–answer–verify, và evaluation. Đặt feedback/control flow ở corridor riêng; kiểm tra render thật để tránh chữ nhỏ và arrow overlap.