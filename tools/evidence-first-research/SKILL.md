---
name: evidence-first-research
description: "Evidence-first applied research workflow: divergent ideation, live literature gap-scan, claim-to-source gates, and reviewer-standard manuscript integrity."
metadata:
  version: "2.0.0"
  license: "MIT"
  source_reference: "Distilled from production research sessions; upstream inspiration https://github.com/imbad0202/academic-research-skills (inspected 2026-06-17)"
  references: "research-execution-communication-gate.md"
  status: active
---

# Evidence-First Research Workflow
> For paid-run reconciliation through clean manuscript release, see `references/paid-run-to-clean-manuscript-release.md`.

## Khi nào dùng

Revise bản thảo theo peer review: `references/peer-review-revision-round.md`.
Trước thao tác có tác động: `references/project-identity-gate.md`. Review manuscript/dữ liệu phân tán: identity, artifact, protocol, experiment alignment; bài TQA-generation: `references/ecm-tqag-data-first-pilot.md`. SaaS đóng: `references/closed-saas-evidence-reconstruction.md`. Kiểm định thang đo: `references/instrument-validation-design.md`. Nguồn câu hỏi công khai: `references/public-assessment-item-sourcing.md`. Thiếu ý tưởng mới / cần brainstorm đề tài: `references/divergent-ideation-protocol.md` (phát tán TRƯỚC, cấm chấm sớm). Đối chiếu claim↔bằng chứng bằng System-One (Jev qua MCP jevbridge) + gate trước hành động nguy hiểm: `references/jev-systemone-claim-gate.md`.

Sửa sớm, chạy lại, xác minh; wording không phải evidence.

---

## Rà soát / làm sạch file references.bib (đối chiếu CSDL)

Khi người dùng yêu cầu "rà references", "đối chiếu CSDL", "sửa .bib": xem
`references/bibtex-reference-audit.md` cho quy trình đầy đủ. Lõi:
1. **Pass 0 cục bộ** — parse tất cả entry, bắt lỗi CHẮC CHẮN trước (trùng key →
   BibTeX fail, entry rác `\hl{}`, trùng title khác key, thiếu `author`). Sửa ngay.
2. **Pass 1 Crossref** (`scripts/bibcheck.py`) — đối chiếu year/vol/num/pages, lấy DOI.
3. **Pass 2 LỌC false positive** (`scripts/bibrecheck.py`) — BẮT BUỘC. Pass 1 cho
   ~70% "diff" là NHIỄU (Crossref match nhầm reprint/erratum, hoặc trả năm
   online-first vs năm số in). Chỉ sửa khi Jaccard(title)≥0.85 + khớp họ tác giả.
   **TUYỆT ĐỐI không sửa mù theo Crossref** — sẽ phá hỏng entry kinh điển vốn đúng
   (Breiman2001, Vaswani2017, Rumelhart1986...).
4. Verify bằng `bibtex` thật (exit 0, 0 warning). Backup `_backups/` trước khi sửa.
5. Cặp trùng-nội-dung-khác-key: KHÔNG tự xóa nếu chưa biết manuscript cite key nào
   (xóa nhầm gãy `\cite`) — hỏi người dùng.

## Rà soát toàn diện manuscript IEEE (số/bảng/hình/caption)

Khi người dùng yêu cầu "rà soát toàn diện" hoặc "đồng bộ bảng số liệu", dùng **2 subagent song song**:
- Agent 1: số trong prose ↔ bảng (cross-check mọi con số claim trong text với giá trị bảng tương ứng)
- Agent 2: in đậm trong bảng ↔ caption (kiểm mỗi `\mathbf{}` có caption giải thích quy ước không)
- Agent chính: hình orphan (file PNG/tikz trong `figures/` không được `\includegraphics` trong bất kỳ .tex nào)

### Các lỗi phổ biến cần kiểm

**Số/prose:**
- p-value prose dùng dạng thập phân nhưng bảng dùng ×10⁻ⁿ → thống nhất về một dạng
- Ratio X× tính từ bảng nhưng prose làm tròn sai hướng (ví dụ 0.0233/0.0037=6.30× nhưng prose ghi 6.2×)
- Cùng metric (ví dụ Missed Vio) xuất hiện ở 2 bảng khác nhau với giá trị không nhất quán (0.04 vs 0.044)
- Runtime cùng policy nhưng report khác nhau ở 2 bảng (tab:whittle vs tab:sota)
- Số chỉ có trong prose, không có bảng backup (sensitivity figure sweep) — ghi chú là "figure-backed only"

**Caption/bold:**
- Mọi bảng có `\mathbf{}` đều phải có câu giải thích quy ước trong caption
  - Best per column: *"Best per column in **bold** (↓: lower is better)"*
  - Chosen method: *"**Bold** marks the [method] adopted by [proposed]"*
  - Không bao giờ để bold im lặng trong bảng

**Figure orphan:**
- Chạy: `ls figures/*.png figures/*.tex | grep -v -f <(grep -roh 'figures/[^}]*' sections/ main.tex)`
- Xóa file không dùng trước khi đóng gói zip để tránh gây nhầm lẫn

### Overfull hbox trong equation (IEEE 2-cột)

- Equation một dòng dạng `A \Rightarrow B \Rightarrow C` dễ tràn cột (~3.5 inch)
- Fix: đổi `equation` → `align`, tách tại `\Rightarrow` với `&\;\Rightarrow\;` và `\notag\\`
- `\qquad` trong equation display → `\quad` nếu còn tràn nhẹ
- Ngưỡng chấp nhận: **0 Overfull** trước khi đóng gói; hbox ≥ 4pt cần sửa

### Quy trình đóng gói zip sạch

1. Build từ thư mục canonical (không phải staging)
2. Kiểm log: 0 Overfull, 0 undefined reference, 0 error
3. Tạo staging dir với whitelist (chỉ .tex, .bib, .cls, .bst, figures/ dùng thật, main.pdf)
4. Xóa orphan PNG trước bước này
5. Zip staging → verify `zip -T` → gửi người dùng cả PDF + ZIP

Reviewer pass "nối liền công thức" (chèn bước trung gian =/⟺/⟹ để không làm mù người đọc):
xem `references/derivation-continuity-reviewer-pass.md`.
Khi người dùng GỬI zip/file và bảo sửa "bản này" — luôn kiểm bản canonical trên đĩa mới hơn TRƯỚC
khi sửa: xem `references/canonical-vs-sent-copy-gate.md`.

Soạn slide báo cáo từ manuscript, rà mạch công thức, hoặc đóng gói .zip sạch: xem
`references/manuscript-to-beamer-and-math-audit.md` (pattern fresh-eyes read-only
audit subagent, Beamer build pitfalls double-subscript + overfull-vbox compaction
ladder, xử lý khi unified re-run làm đảo luận điểm, đóng gói zip sạch).

Khi yêu cầu là "rà soát toàn diện / đồng bộ manuscript ↔ thí nghiệm / đồng nhất tham số chạy lại
toàn bộ / sửa method-results làm lệch narrative", xem `references/manuscript-experiment-sync-audit.md`
(quy trình RLM 3-wave: map bề mặt → audit fresh-eyes read-only 3 subagent song song → vá tuần tự
có verify; + quy tắc DỪNG-khi-narrative-đảo, hai-nền-tách-bạch, verify-số-từ-CSV, bẫy file mồ côi).

## Nguyên tắc nền

1. Human-in-the-loop: AI là trợ lý nghiên cứu, không thay nhà nghiên cứu ra quyết định học thuật.
2. Evidence-first: claim quan trọng phải có nguồn, vị trí, metric, citation hoặc log/file tương ứng.
3. Không tự gọi "novel" nếu chưa so với prior work gần nhất.
4. Không gọi "ready" nếu chưa có evidence build/render/test/package/validator.
5. Tách rõ: Fact / Hypothesis / Inference / Recommendation.
6. Chống knowledge leakage: khi viết từ tài liệu đã ingest, ưu tiên source đã cung cấp; thiếu thì ghi `[MATERIAL GAP]`, không tự bịa.
7. Consent boundary: không gửi manuscript/chưa công bố/sensitive corpus cho provider ngoài nếu chưa nói rõ provider, model, loại nội dung gửi và được người dùng đồng ý.

## Kernel trả lời cho việc khó

Dùng cấu trúc sau cho research/review/architecture/debug nặng:

1. Question: câu hỏi cần quyết định.
2. Known facts: dữ kiện đã có từ file, paper, log, data, citation.
3. Method: cách kiểm tra/suy luận.
4. Inference: kết luận kèm độ tự tin.
5. Limitations: điểm chưa chắc, thiếu dữ liệu, nguy cơ sai.
6. Next action: bước nhỏ nhất củng cố kết luận.

## Pipeline nghiên cứu 10 giai đoạn

### Stage 0 - Intake và phân loại

Mục tiêu: xác định request thuộc loại nào.
- ANSWER: giải thích/định hướng, không đổi file.
- EXECUTE: có artifact/file/tool, phải inspect -> change -> verify.
- CLARIFY: chỉ hỏi đúng 1 quyết định nếu thiếu thông tin gây rủi ro.

Output tối thiểu:
- Mục tiêu quan sát được.
- Artifact đích nếu có.
- Rủi ro an toàn hoặc privacy nếu có.

### Stage 1 - Research Question Brief

Mục tiêu: biến ý tưởng mơ hồ thành câu hỏi nghiên cứu kiểm được.

Deliverable: `RQ Brief`
- Research Question: 1 câu hỏi chính, dạng interrogative.
- Sub-Questions: 2-5 câu hỏi phụ.
- Scope: in-scope, out-of-scope, domain, timeframe, geography, population.
- FINER scores: Feasible, Interesting, Novel, Ethical, Relevant, mỗi mục 1-10.
- Keywords: 5-10 cụm từ tìm kiếm.
- Ethical flags nếu có.

Quy tắc: nếu ý tưởng còn mơ hồ, dùng Socratic mode: hỏi từng câu để người dùng tự chốt gap/value/feasibility, không tự áp đặt đề tài. Nếu người dùng chê "thiếu sáng tạo/ít ý tưởng mới": chạy vòng phân kỳ `references/divergent-ideation-protocol.md` (≥10 hướng thô từ ≥3 kỹ thuật, subagent chống neo, CẤM chấm novelty ở bước này) TRƯỚC khi viết RQ Brief — hệ đo thật: Jev xếp hướng an toàn 0.59 vs hướng cross-domain 0.19 nên System-One chỉ được dùng ở bước lọc claim, không dùng xếp hạng ý tưởng.

### Stage 2 - Methodology Blueprint

Mục tiêu: phương pháp phải đi từ câu hỏi, không chọn phương pháp theo thói quen.

Deliverable: `Methodology Blueprint`
- Paradigm: ontology/epistemology nếu phù hợp.
- Methodology type: qualitative / quantitative / mixed / design science / experimental / systematic review.
- Data strategy: nguồn dữ liệu, sampling, collection, inclusion/exclusion.
- Analysis strategy: statistical, thematic, benchmark, ablation, qualitative coding, etc.
- Validity criteria: internal/external/construct/conclusion validity hoặc trustworthiness.
- Limitations by design.

Decision tree nhanh:
- "What is happening?" -> descriptive/survey/case/content analysis.
- "How compare?" -> comparative case/cross-sectional/benchmark.
- "Is X related to Y?" -> correlational/regression/meta-analysis.
- "Does X cause Y?" -> experiment/quasi-experiment/causal inference.
- "How/why experience?" -> qualitative interview/case study/thematic analysis.
- "Can artifact solve problem?" -> design science/engineering evaluation.

### Stage 3 - Literature Search và Verification

Khi cần verify hoặc discover citations programmatically (đặc biệt cho region-context citations ngoài PRISMA corpus), dùng `references/crossref-api-citation-verification.md` — có recipe batch Crossref API, pitfalls (gov VN portals block bot, search engines block headless), và bảng 14 nguồn VN-region đã verify session 2026-06-24.

Mục tiêu: tạo corpus có thể kiểm chứng, không chỉ liệt kê paper.

Deliverable: `Literature Corpus`
- Search strings/databases/date searched.
- Inclusion/exclusion criteria.
- Citation metadata: title, authors, year, venue, DOI/URL.
- Evidence relevance: paper trả lời sub-question nào.
- Quality signal: venue, design, sample, metrics, threat.
- Verification status: verified / uncertain / excluded.

Quy tắc:
- Literature trước gap.
- Với systematic/scoping review: dùng PRISMA mindset, ghi rõ query và flow.
- Citation đáng ngờ phải kiểm tra DOI/venue/metadata; không dùng citation hallucinated.
- Claim rút từ mỗi paper phải đối chiếu được với source verbatim; rà nhanh bằng 1 call `jev_decide` noul (claim↔source, ngưỡng 3 dải ≥0.8 pass / ≤0.2 block / giữa → escalate) — `references/jev-systemone-claim-gate.md`.

### Stage 4 - Synthesis và Gap Analysis

Mục tiêu: tổng hợp xuyên nguồn, không tóm tắt từng paper rời rạc.

Deliverable: `Synthesis Report`
- Themes/patterns across studies.
- Contradictions and explanations.
- Evidence weight: nguồn nào mạnh/yếu, vì sao.
- Gap map: empirical gap, methodological gap, theoretical gap, contextual gap.
- Claim table: claim -> evidence -> limitation -> confidence.

Anti-patterns:
- Paper-by-paper summary kéo dài.
- Chọn citation ủng hộ rồi bỏ qua evidence trái chiều.
- Gọi gap là novelty khi chưa so với prior work mới nhất.
- Chấm/phê phán ý tưởng ngay khi vừa sinh (giết con mới lạ trước khi kịp phát triển) → tách phát tán khỏi hội tụ: `references/divergent-ideation-protocol.md`.

#### Đánh giá hàm lượng khoa học (contribution depth) cho Q1

Khi người dùng hỏi "đóng góp có đủ hàm lượng Q1 không / thuật toán có quá đơn giản không", trả lời thẳng, không tô hồng:
- Bóc method đề xuất thành các primitive components, đối chiếu từng cái với prior art. Nếu method = tổ hợp tuyến tính của các số hạng đã biết + top-k/greedy, thì đó là **incremental combination** — phải nói rõ, reviewer Q1 sẽ gọi đúng tên.
- Phân biệt ba loại đóng góp: (a) formulation mới, (b) algorithm có cấu trúc + guarantee không tầm thường, (c) empirical study mạnh. "Formulation hay + empirical tốt + thuật toán đơn giản" thường rơi vào **Q1 yếu / Q2 mạnh**; muốn Q1 vững cần thêm (b).
- Lỗ hổng lý thuyết hay gặp: theorem chỉ chứng minh cho **analysis variant lý tưởng** chứ không phải **deployed variant**; bound là kết quả kinh điển (deficit/round-robin) được phát biểu lại. Nêu rõ "lý thuyết không khớp cái đang chạy" là điểm reviewer bắt đầu tiên.
- Để nâng hàm lượng, dùng literature 2024–2026 tìm một guarantee gắn ĐÚNG cái đang chạy (submodular (1-1/e), regret, asymptotic optimality, indexability). Fan-out subagent quét song song nhiều nhánh (semantic/AoII scheduling; submodular sensing; RMAB indexability) rồi tổng hợp gap.
- Trước khi sửa method vào manuscript, làm SPIKE kiểm chứng trên dữ liệu thật: implement biến thể mới sau một flag opt-in (không ghi đè deployed path), backup file gốc, chạy 3-window smoke rồi mới full. Xem `references/method-enhancement-spike.md`.
- KHI NÂNG HÀM LƯỢNG BẰNG BIẾN THỂ TAIL-RISK / CVaR (risk-aware, "ghìm đuôi thay vì kỳ vọng", chạy trên dữ liệu khó/thực tế VN): dùng `references/tail-risk-cvar-fold-in.md`. Có recipe Rockafellar–Uryasev (derive trước, hằng số dẫn xuất được) + 4 pitfall đã bị: (1) tail variable zero-inflated làm CVaR thoái hóa thành mean-constraint — phải đặt CVaR trên LOSS liên tục, chẩn đoán tail health (violation%+burst run-length) trước khi chạy; (2) "thắng" có thể chỉ là "tốn băng thông hơn" — phải matched operating point + baseline mean-variance công bằng (nằm giữa, không straw-man); (3) không in đậm cột operating-point matched; (4) ĐỔI DATASET (không phải N) có thể ĐẢO narrative chính (Fixed-B3 thắng khi violation nhiều) — STOP báo số, đừng fudge trọng số, người dùng nghiêng giữ HAI dataset tách bạch (dataset gốc cho SoTA/baseline, dữ liệu khó là case-study riêng cho biến thể mới), report lợi ích tăng-theo-độ-nặng-đuôi trung thực. Kèm: Open-Meteo ERA5 cho dữ liệu khí hậu VN thật tải được; scipy ở venv `_repos/<proj>/.venv` không ở execute_code sandbox.
- KHI NGƯỜI DÙNG MUỐN FOLD MỘT BIẾN THỂ RISK-AWARE/CVaR/tail-risk + "chạy trên dữ liệu khó/thực tế như bài AoI-greenhouse, ưu tiên dữ liệu Việt Nam" + "đề xuất bổ sung nếu chưa đủ tốt": dùng `references/tail-risk-variant-and-real-data-validation.md`. Bài học cốt lõi: (1) nguồn dữ liệu VN thật, tải được, kiểm chứng được = Open-Meteo ERA5 Historical Archive (lat/lon, hourly cả năm, no-auth) — Zenodo query hay rỗng/tràn 20000-char JSON, file VN cũ trên đĩa thường là synthetic (đọc README provenance); (2) ràng buộc CVaR_α SUY BIẾN trên tín hiệu zero-inflated (α-quantile≈0 ⟹ thoái hóa về mean, biến thể chỉ tốn thêm tài nguyên) — đổi sang biến tail LIÊN TỤC (control-loss, không zero-inflated) và in tail-structure (violation%, burst count, run-length) TRƯỚC khi claim non-degenerate; (3) chống confound "thắng nhờ tốn tài nguyên" = bind resource-constraint HARD trên CẢ HAI policy (matched operating point), sweep binding-strength, thêm baseline classical (mean–variance) — nếu nó nằm GIỮA baseline và method thì chứng minh không straw-man; (4) DERIVE-then-spike trên clone (`<repo>_branchB_clone/`, importlib + repoint `M.SRC`), báo negative trước positive; (5) khi fold: objective biến thể phải DERIVE từ objective gốc bằng phép thay-số-hạng (viết thành equation), mọi symbol trong objective/Algorithm có eq định nghĩa (bắt `p^bad` dùng-mà-thiếu-eq), neo hằng số derivable, orphan-label check (range-ref `\eqref{a}--\eqref{b}` = false positive), tie biến thể vào Algorithm theo số dòng, method-name coherence (abstract+intro contribution+keywords); (6) page-budget: giữ toán, đừng hy sinh nội dung để ép trang — hỏi trước khi đẩy proof/bảng phụ sang appendix; cột bandwidth matched-operating-point KHÔNG bold (là control, không phải metric thắng).
- KHI NGƯỜI DÙNG MUỐN FOLD BIẾN THỂ RISK-AWARE/CVaR/tail-risk + "chạy trên dữ liệu khó/thực tế, ưu tiên VIỆT NAM" + "đề xuất bổ sung nếu chưa đủ tốt" (kiểu bài AoI-greenhouse): dùng `references/tail-risk-cvar-enhancement-and-real-data.md` (recipe chính) và `references/real-data-sourcing-and-tail-risk-spike.md`. Lõi: (1) chẩn đoán zero-inflation/cấu trúc đuôi TRƯỚC khi chạy full (CVaR thoái hóa thành mean-constraint nếu tín hiệu sparse); (2) dữ liệu VN thật = Open-Meteo ERA5 archive, khai báo semi-real; (3) khử confound "thắng nhờ tốn tài nguyên" bằng matched operating point (ghim resource-dual như nhau, sweep mức siết) + baseline mean–variance công bằng nằm GIỮA; (4) ξ-tracker RU đừng double-divide cho (1−α); (5) fold page-limited: gộp bảng, không bold cột matched, trình người dùng quyết trade-off trang. BÀI HỌC RIÊNG (không nằm trong 2 ref): một guarantee chỉ đáng claim nếu objective đảm bảo ĐÚNG metric mình quan tâm — objective provably-submodular (information gain) có thể tệ hơn nhiều vì bỏ mất safety term; verify bằng spike, đừng giả định reformulation "đẹp lý thuyết" cải thiện metric đích.
- SỐ CỬA SỐ SMOKE KHÔNG PHẢI BẰNG CHỨNG: 3-window smoke chỉ để bắt bug; kết quả có thể ĐẢO CHIỀU hoàn toàn ở full N. Luôn chạy đủ N (vd 30 windows) + paired Wilcoxon trên per-window delta (báo wins/losses/p) trước khi nói một thành phần "thắng"/"đáng cứu". Nhúng Wilcoxon vào chính spike script. Khi spike đóng một hướng (không biến thể nào thắng deployed có ý nghĩa), nói thẳng và pivot sang hướng lý thuyết, đừng ép một cải thiện cận-biên vào bài.
- KHI MỘT SPIKE ĐÃ ĐÓNG NHƯNG NGƯỜI DÙNG MUỐN "THỬ THÊM TRÊN DỮ LIỆU KHÓ/THỰC TẾ" (đặc biệt biến thể risk-aware / CVaR / tail-risk), dùng `references/risk-aware-spike-revival-and-real-data-sourcing.md`. Bài học cốt lõi: (1) "spike đóng" CÓ ĐIỀU KIỆN theo REGIME dữ liệu — CVaR vô dụng khi tín hiệu rủi ro zero-inflated (đa số khe = 0, phân vị α≈0 ⟹ thoái hóa về ràng buộc kỳ vọng); fix bằng đổi BIẾN đuôi sang đại lượng liên tục (control-loss thay miss-rate) VÀ tìm dataset đuôi không suy biến, in go/no-go tail-diagnostic (viol%/burst/run-length) TRƯỚC khi chạy full; (2) so sánh airtight = ép ràng buộc tài nguyên (băng thông) BẰNG NHAU qua cùng dual + sweep step-size 2–3 mức, chỉ khi đó mới là "phân bổ khôn hơn" không phải "tốn hơn"; thêm baseline mean–variance công bằng (nằm GIỮA = không straw-man); (3) dữ liệu VN thật verify-được: Open-Meteo ERA5 reanalysis (lat/lon ĐBSCL, hourly, cả năm), khai báo "semi-real" trung thực; (4) FOLD vào bài = liên kết công thức bằng phép suy ra tường minh (objective mới = objective cũ THAY một số hạng; chain constraint→RU identity→J^CVaR→2 update; mọi symbol trong Algorithm phải có eq định nghĩa — bắt p^bad thiếu eq; orphan-label audit; sync contribution+keyword+abstract); (5) thêm toán thật làm phình trang thì nén prose không cứu được — trình trade-off cho người dùng quyết, đừng siết layout quá độ.
- HỒI SINH MỘT SPIKE ĐÃ FOLD (người dùng nói "thử thêm" / "chạy trên tập dữ liệu khó, thực tế như bài AoI-greenhouse" / "ưu tiên dữ liệu Việt Nam"): dùng `references/reviving-folded-spike-real-data-and-nondegenerate-target.md`. Bài học cốt lõi: (1) spike CVaR/tail-risk fold thường do REGIME suy biến (tín hiệu bị ràng buộc bị zero-inflated ⇒ quantile-90 ≈ 0 ⇒ CVaR thoái hóa thành ~ràng buộc kỳ vọng) — chẩn đoán regime, KHÔNG vặn step-size; hai fix trực giao: đổi BIẾN MỤC TIÊU sang đại lượng liên tục không zero-inflated (vd miss-rate sparse → per-slot control-loss), và đổi sang DATASET KHÓ THẬT có event-rate hai chữ số + cấu trúc chùm; luôn in diagnostic tail-structure (violation% + burst count + mean run-length) làm go/no-go TRƯỚC khi so sánh. (2) Dữ liệu VN thật, kiểm chứng được = Open-Meteo Historical Archive (ERA5 reanalysis) `archive-api.open-meteo.com/v1/archive` cho toạ độ ĐBSCL (Cần Thơ/Sóc Trăng/Cà Mau), hourly temp+RH, 8784 điểm/năm/trạm — semi-real (control mô phỏng TRÊN trace thật), khai báo đúng như dataset khí hậu VN, không gọi "field-measured". (3) Khử confound "thắng nhờ tốn tài nguyên": ghim resource-dual là binding constraint cho MỌI policy cùng step, expose `BW_STEP` qua env và SWEEP 2-3 mức mạnh dần — nếu variant vẫn thắng khi realized budget khớp baseline trong ~1-2% thì win mới airtight (bài bandwidth-scheduling: CVaR-loss giữ p<1e-46 qua mọi mức; CVaR-miss bị loại vì win cưỡi trên +0.19 bandwidth).
- KHI NGƯỜI DÙNG MUỐN ĐỔI QUY MÔ N CỦA SIMULATOR (vd "N=3 nhưng bài ghi N=30 — làm N=30 thật"): dùng `references/simulator-scale-generalization.md`. Bài học cốt lõi: (1) đọc data TRƯỚC — nếu chỉ có K trace thật thì N>K là semi-synthetic, PHẢI khai báo, trình người dùng 3 lựa chọn (giữ N=K honest / mở rộng semi-synthetic / đổi thesis) chứ không tự bootstrap rồi gọi là real; (2) pitfall cốt lõi: hằng-số phạt-per-budget (vd `0.04*B`) mis-scale theo N — lợi ích/sensor ~1/N co lại còn chi phí giữ nguyên, làm Oracle/lower-bound đảo thành tệ hơn heuristic; fix bằng `BW_SCALE=K/N` nhân mọi term phạt-per-B (=1 tại N=K), chẩn đoán từ triệu chứng (oracle đảo, age-based trội) chứ KHÔNG fudge hằng số; (3) smoke gợi ý có thể bị full N + Wilcoxon ĐẢO (phiên này: smoke hint thua → full n=320 xác nhận thua p<1e-50 do regime đổi), luôn full N trước khi để scale viết lại thesis, báo kết quả trung thực; (4) backup code+CSV trước re-run, generalize base sim rồi patch sibling scripts (`importlib`) hardcode `range(K)`/`/K`, monkeypatch `M.channel` cho drift variant, và `random.Random()` không nhận tuple seed (dùng int hash).\n- KHI NÂNG HÀM LƯỢNG TOÁN Ở PHẦN PREDICTOR / VALUE FUNCTION (đổi confirm→predict, thử ML/DL, first-passage, trend model): dùng `references/predictor-enhancement-evaluation.md`. Bài học cốt lõi: (1) đo chất lượng dự đoán TÁCH KHỎI scheduler trước bằng held-out AUC/AP/Brier; (2) chẩn đoán model-mismatch từ THAM SỐ ĐÃ FIT (vd α̂≈1 ⟹ near-random-walk, không phải mean-reverting), đừng đoán; (3) tính Bayes-optimal predictor làm TRẦN — nếu chính nó cũng không cải thiện loss thì không predictor nào làm được (bằng chứng mạnh nhất); (4) calibration tốt (Brier thấp) KHÔNG kéo theo loss scheduler tốt — hệ xếp hạng cần discrimination/spread, first-passage \"anytime\" nén dải urgency làm ranking xấu; (5) chuỗi negative result nhất quán là đòn bẩy Q1 (\"đã thử cái phức tạp, chứng minh closed-form near-sufficient\"), gói thành Proposition + ghi `docs/negative_result_*.md`.\n- KHI NGƯỜI DÙNG HỎI "VÌ SAO DẠNG ĐƠN GIẢN/CLOSED-FORM/POINT-IN-TIME LẠI TỐT — DO DỮ LIỆU HẢ?" hoặc "vì sao dự đoán tương lai không tốt hơn?", và yêu cầu "chứng minh đầy đủ, có toán, từ ngữ đơn giản": dùng `references/defending-closed-form-design.md` + chạy `scripts/measure_regime_properties.py`. Đây là GIẢI THÍCH (không sửa code). Bài học cốt lõi: (1) trả lời thẳng "đúng, do regime dữ liệu" rồi chứng minh bằng ε-expansion: closed-form là số hạng bậc 0 (d_0) của danger Bayes-tối-ưu, correction chỉ ở O(ε), suppression lemma ES/Φ̄→σ·ε, verify số bằng script; (2) mỗi claim phải có MỘT con số đo thật (α̂+half-life, σ/RANGE, z-to-bound, forecast-skill ratio RMSE(AR1)/RMSE(naive)≈1 ⟹ no trend); (3) dự đoán tương lai hỏng vì hai tầng — không có trend (α≈1) VÀ first-passage bão hòa {0,1} nén dải, mất ranking discrimination (scheduler top-B cần ORDER không cần calibration; predictor Brier thấp hơn vẫn loss tệ hơn); (4) nêu rõ điều kiện ĐẢO NGƯỢC (ε lớn = field volatile/sát ngưỡng) làm giới hạn áp dụng + future work; (5) bật biến thể "đẹp lý thuyết" (ev_cost/severity) phải SPIKE đo số thật trước — số thật cho thấy ev_cost thua 2-3× do cùng cơ chế nén dải.\n- KHI EMPIRICAL LEVER ĐÃ ĐÓNG, PIVOT SANG LÝ THUYẾT (proof-layer, không phải kiến trúc mới): chứng minh chính cái rule đang chạy là asymptotic near-optimal. Xem `references/theory-elevation-asymptotic-optimality.md`. Hai bài học cốt lõi: (1) phải nói RÕ với người dùng rằng đây là lớp chứng minh thêm cho artifact cũ, KHÔNG phải bài mới (người dùng hay hỏi thẳng "khác hoàn toàn ... cũ hả?"); (2) trước khi viết theorem, đọc CODE SIMULATOR để kiểm từng assumption của paper — đặc biệt arm-independence (channel dùng chung phá RMAB), bounded vs accumulating state, UGAP (chỉ assume được, support bằng empirical), và heuristic index ≠ exact gain index. Khi assumption buộc đổi mô hình, trình rõ trade-off + chi phí re-run trước khi làm, đừng tự đổi. Khi người dùng đã duyệt đổi mô hình: GATE lần re-run đắt bằng một SPIKE quyết định (full N + Wilcoxon) chứng minh model change cải thiện metric đích trước khi chạy full; gom mọi quyết định thiết kế còn treo (vd VoU redesign) để job nặng chỉ chạy MỘT lần. Reference này cũng có recipe refactor shared-scalar → per-arm-vector (grep mọi call-site, thêm `_vec` cạnh scalar, broadcast `p_succ*vou`, index `p_succ[j]` trong loop, vectorize cả baseline, coi chừng dead code).

### Stage 5 - Draft Architecture

Mục tiêu: dựng cấu trúc bài trước khi viết dài.

Deliverable: `Paper Skeleton`
- Title candidates.
- Abstract bullet outline.
- Introduction move structure: context -> problem -> gap -> contribution -> structure.
- Related work themes.
- Method section structure.
- Results/evaluation plan.
- Discussion: implications, limitations, future work.
- Figure/table plan.

Quy tắc: section nào thiếu evidence thì đánh dấu `[MATERIAL GAP]`.

### Stage 6 - Manuscript Writing

Mục tiêu: viết dựa trên synthesis và source, giữ giọng học thuật của người dùng.

Deliverable: manuscript draft.
- Mỗi claim trọng yếu có citation/evidence.
- Không dùng AI-typical throat-clearing, không nói quá.
- Abstract 150-250 từ nếu theo APA/standard journal, hoặc theo template venue; khi người dùng yêu cầu "ngắn lại", vẫn giữ ngưỡng tối thiểu của venue (ví dụ IEEE IoTJ cần 150--250 words) và kiểm word count sau khi sửa.
- Introduction phải chốt được: problem, gap, contribution, significance; nếu người dùng yêu cầu "bổ sung Introduction nhiều hơn", mở rộng bằng bối cảnh deployment, kiến trúc hệ thống, failure mode của baseline, và rationale của method trước contribution, không kéo dài contribution list.
- Khi người dùng yêu cầu CÔ ĐỌNG / RÚT GỌN bản thảo vì page-limit/page-charge ("viết ngắn hơn được không", "tạp chí giới hạn N trang", "agent triển khai đi"), dùng `references/manuscript-condensation-page-limits.md`. Bài học cốt lõi: (1) xác minh chính sách trang THẬT bằng nguồn live trước khi cắt — IEEE IoTJ 8 trang là NGƯỠNG MIỄN PHÍ ($175/trang vượt), KHÔNG phải giới hạn cứng, regular paper thực tế 11–14 trang; (2) ĐO cái gì chiếm chỗ trước (đếm bảng/hình/word) — cắt prose có thể chỉ rút 1 trang nếu bài dài do 12 bảng, phải gộp bảng/đẩy bảng phụ vào appendix mới giảm trang thật; (3) đẩy proof dài vào appendix (proof sketch trong thân), coi chừng multiply-defined label khi copy block có `\label`; (4) TRƯỚC khi gộp bảng so sánh, kiểm provenance: nếu hàng method-chuẩn lệch số giữa các bảng → chúng từ batch khác nhau, gộp ẩu = bịa bảng đồng nhất, phải chạy lại MỘT batch thống nhất (Cách A) hoặc xin người dùng chọn A/B; (5) người dùng chạy agent SONG SONG trên repo — gặp cảnh báo sibling-modified file thì đọc lại file trước mỗi patch và DỪNG hỏi, đừng để lost-update.

Khi người dùng nhận ra phần đang làm "gần với <paradigm hot>" (Digital Twin, semantic/goal-oriented comm, edge-AI...) và muốn ĐỊNH VỊ bài bắt trend mà không đổi method ("chỗ này gần X rồi agent nhỉ" → "làm hướng nhẹ đi nhé"), dùng `references/positioning-paper-trending-paradigm.md`. Bài học cốt lõi: (1) luôn nêu rõ Hướng A light-positioning (1 câu intro + 1 đoạn related work + 2-3 ref, không đổi toán) vs Hướng B đào sâu (bài riêng) để người dùng chọn; (2) verify ref THẬT qua arXiv API HTTPS, không bịa, chọn paper khớp đúng cơ chế bài; (3) chống overclaim bằng cách tự định danh "lightweight/first-order/per-sensor twin" + nêu ≥2 điểm KHÁC với paradigm đầy đủ; (4) build gate full chain + xác nhận số trang không phình; (5) đề nghị (hỏi trước) phản ánh 1 cụm lên Abstract. Khi người dùng nói "thử chạy xem bài ta có ngon hơn paradigm đó không" → Hướng A+: implement chính policy của paradigm (vd DT+AoI) làm baseline TRUNG THỰC (mạnh nhất nhưng thiếu đúng thành phần đặc trưng của method mình), chạy head-to-head cùng seed/channel/B, báo cả metric THUA (vd DT+AoI thắng RMSE nhưng thua safety) — negative-on-one-metric lại củng cố định vị; xem §Hướng A+ trong reference.

Quality check:
- Câu/đoạn có độ dài biến thiên tự nhiên.
- Không lạm dụng từ chung chung như robust, comprehensive, significant nếu không có metric.
- Claim causal chỉ dùng khi design cho phép causal inference.

#### Ghép toán đã derive + số đã verify vào manuscript (build-gated)

Khi người dùng nói "viết cho nó 'toán' vào" / "agent sửa đi" sau khi đã có derivation
trong `docs/*_derivation.md` và số liệu trong CSV, đây là EXECUTE: ghép thẳng vào
`sections/*.tex`, không chỉ để ở docs. Quy trình đã chạy thật, có build sạch:

1. **Backup trước (thói quen người dùng):** `cp sections/05_theory.tex sections/04_evaluation.tex _backups/manuscript_<ts>/` rồi sửa TẠI CHỖ, không tạo `_v2`.
2. **Kiểm preamble TRƯỚC khi viết math mới.** grep `newtheorem` + `newcommand`/`DeclareMathOperator` trong `main.tex`. Theorem environments (lemma/proposition/corollary) thường có sẵn; nhưng macro toán mới (`\Smin`, `\Smax`, `\Phibar`, `\E`) thường CHƯA — thêm vào preamble bằng `\newcommand`/`\providecommand{\E}{\mathbb{E}}` NGAY, nếu không build vỡ "Undefined control sequence".
3. **Số trong bảng PHẢI lấy programmatically từ CSV gốc** (execute_code đọc CSV → mean ± 1.96·sd/√n), KHÔNG retype từ log/trí nhớ — sai một chữ số là lỗi liêm chính. p-value lấy từ log Wilcoxon đã chạy.
4. **Citation mới: fetch metadata LIVE** từ arXiv `id_list` query (title/authors/year), không bịa. Thêm `@article` vào `references.bib`. Cảnh giác năm: ID 2024 ≠ năm publish luôn (vd Online-Whittle thực ra 2026).
5. **Build gate = FULL chain, không tin latexmk một lần.** Chạy `pdflatex → bibtex → pdflatex → pdflatex`, rồi grep pass CUỐI cho `Citation.*undefined` (phải = 0) và `??` (undefined ref = 0). latexmk một pass hay warn citation cũ vì bibtex chưa chạy đủ — không phải lỗi thật. Xác nhận PDF mới + `pdftotext` grep thấy section/bảng mới có trong PDF.
6. Báo người dùng bằng chứng build THẬT (exit 0, 0 undefined, số trang, backup path), không tự nhận "đã xong".

#### Cross-section notation + consistency audit (sau khi thêm/sửa equation)

Khi thêm phương trình mới vào một section (vd belief-filter vào System Model) hoặc
khi người dùng nói "rà lại đi" / "cái gì cũng phải tường minh", PHẢI audit nhất quán
xuyên section, không chỉ build sạch là xong:
- **Symbol clash:** ký hiệu mới (vd `c_i(t)` = channel mode trong §2) có thể TRÙNG
  ký hiệu cũ ở section khác (vd `c_i(t)` = instantaneous cost trong §3). Reviewer
  bắt ngay. grep ký hiệu xuyên `sections/*.tex`; đổi một bên (vd cost → `ℓ_i(t)`).
- **Notation sync:** scalar cũ (`p_succ`) phải đổi sang dạng mới đã định nghĩa
  (`p_i(t)` per-arm) ở MỌI nơi dùng (probe index, payload index, impl equation),
  và `\eqref` về phương trình định nghĩa.
- **Model coherence:** nếu theorem/§5 dựa trên một giả định (vd per-arm independent
  channel), thì §2 System Model PHẢI khai báo đúng giả định đó — đừng để §2 tả
  "shared channel" trong khi §5 chứng minh trên "per-arm". Mâu thuẫn này làm theorem
  "treo", reviewer bắt.
- **Equation khớp code:** trước khi viết eq (belief predict/update, likelihood),
  ĐỌC hàm thật trong code (`channel.py::update_bad_belief_vec`) và viết khớp 1-1
  (predict qua kernel G-E rồi Bayes update chỉ cho served arm), KHÔNG bịa hệ số.
- **Tường minh hóa term bị chê:** nếu người dùng chê một term "thiếu toán" (vd TrackGap
  chỉ gọi tên), thêm eq định nghĩa tường minh + một đoạn neo nó về object lý thuyết
  (leading-order của Bayes VoU), không chỉ viết công thức trần.
- **Method-name coherence audit:** mọi claim trong TÊN method phải xuất hiện ở mọi
  nơi chính. Vd method "bài AoI-greenhouse" = **C**hannel-**A**ware nhưng abstract/intro
  contributions/figure pipeline ban đầu KHÔNG hề nhắc channel — chữ "C" vô hình.
  Khi đã thêm một trụ (per-arm channel) vào method/theory, grep abstract + §1
  contribution list + figure: nếu thiếu, bổ sung (1-2 câu mô tả cơ chế + 1 dòng
  contribution). Theorem mới (vd O(1/√N)) cũng phải vào contribution list, không để
  trụ lý thuyết lớn mà phần đóng góp không kể.
- **Internal numeric consistency:** mọi con số dẫn xuất (vd ε=σ/(u−μ), suppression
  factor, bội số ×) phải verify PROGRAMMATICALLY và đồng bộ xuyên section. Bug thật
  gặp: §5 viết "z≈8 ⟹ ε≈5×10⁻³" — SAI, vì ε=1/z≈0.12; 5×10⁻³ là nhầm với hệ số
  suppression ES/P̄=v/(u−μ). Lẫn lộn ε với suppression-factor là lỗi điển hình. Tính
  lại bằng execute_code, rồi sync mọi section dùng cùng con số (§3 viết ε≈0.06 trong
  khi §5 ε≈0.12 cho cùng sensor → phải khớp). Bội số (34× vs 39×) verify bằng
  loss_baseline/loss_method, grep mọi lần lặp con số đó trong text + tail/abstract.
- **Complexity-table vs measured-runtime pitfall:** khi bảng độ phức tạp ghi MỌI policy cùng bậc (vd tất cả $O(N\log N)$) nhưng runtime đo thực tế chênh nhau nhiều lần (vd 1.3ms vs 97ms vs 434ms), người dùng sẽ bắt ngay (\"toàn bộ là O(N) thì sao thời gian chạy khác nhau?\"). Đây là lỗi trình bày thật, không phải nghịch lý. Sửa: (1) tách rõ trong text \"cùng asymptotic order\" vs \"khác per-node constant\" — runtime do thao tác MỖI NODE chi phối (vd bài AoI-greenhouse mỗi node phải AR(1) forecast + empirical-residual bootstrap [nặng nhất] + channel-belief update; baseline chỉ đọc age) chứ không phải bậc tiệm cận; (2) thêm cột \"Dominant per-node op\" vào bảng để cột bậc giống nhau không còn đọc như mâu thuẫn; (3) policy thực sự ở bậc CAO HƠN (vd exact belief-MDP $O(KN|S|^3)$) thêm thành một hàng riêng để tách \"cùng order khác hằng số\" với \"khác order\". Quy tắc tổng quát: bảng big-O mà mọi hàng giống nhau + runtime khác nhau LUÔN cần cột giải thích hằng số/thao tác chi phối.\n- **Parameter-table phải gom nhóm + verify từng giá trị với code:** khi người dùng nói \"đồng bộ và rõ ràng 2 bảng này\" (params + reproducibility) hoặc gửi ảnh bảng Simulation Parameters, nâng bảng phẳng thành bảng gom nhóm (Network / Scheduler / Channel / Protocol) và thêm tham số còn THIẾU nhưng phần lý thuyết có dùng (vd kênh G–E: $P_{gg},P_{bb},p_{ok}^G,p_{ok}^B$; seed schema). MỌI giá trị phải đối chiếu trực tiếp với hằng số trong code thật (vd `channel.py` `severe_burst: p_gb=0.12 → P_gg=0.88`; `benchmark_*.py` `lambda_safety=6.0, w_debt=0.05, horizon=240`), KHÔNG retype từ trí nhớ — sai số trong bảng params là lỗi liêm chính giống bảng kết quả. Caption trỏ về Section method/theory để người đọc thấy ký hiệu nhất quán.\n- **Table-bold-correctness (lỗi liêm chính, không phải thẩm mỹ):** caption ghi \"best per row in bold\" / \"lower is better\" thì ô in đậm PHẢI là ô tốt nhất thật (min hoặc max đúng theo hướng). Bug thật phiên bài bandwidth-scheduling: hàng CV in đậm CẢ 0.2 (bài bandwidth-scheduling-L, nhỏ nhất) LẪN 0.3 (bài bandwidth-scheduling-PD), khiến người đọc tưởng bài bandwidth-scheduling-PD ổn định nhất trong khi bài bandwidth-scheduling-L mới nhỏ nhất — bold sai gây HIỂU NHẦM về method nào thắng, nặng hơn lỗi trình bày. Người dùng bắt ngay (\"best per row mà sao lại vậy\"). Khi rà bảng: với MỖI hàng, tự xác định ô tốt nhất theo hướng caption rồi đối chiếu `\\textbf{}` đang đặt ở đâu; chỉ đậm đúng một ô tốt nhất (hoặc nhiều ô nếu thật sự bằng nhau). Cẩn thận hàng tóm tắt (CV/mean/std) có hướng-tốt khác hàng dữ liệu.
- **Context-only column KHÔNG được in đậm (biến thể của bold-correctness):** nếu caption ghi một cột là "reported for context only" / "not a comparison metric" (vd Runtime/wall-clock), thì TUYỆT ĐỐI không `\textbf{}` ô nào trong cột đó — kể cả ô có giá trị min. Bold ở cột chỉ-để-tham-khảo khiến người đọc tưởng đó là tiêu chí thắng/thua. Bug thật phiên bài AoI-greenhouse IoT-J: cột Runtime ghi "for context only" nhưng baseline có runtime 0.5ms lại được in đậm (vừa sai logic vừa sai số vì hàng khác có 0.4ms nhỏ hơn). Người dùng bắt ngay. Fix: bỏ mọi `\textbf{}` trong cột context-only + thêm vào caption "...and is not marked". Quy tắc: chỉ in đậm các cột mà caption thật sự tuyên bố "best per column/row"; cột phụ trợ (runtime, kích thước, tham số cấu hình) để thường.
- **KHÔNG để tên-biến-code / magic-number rò vào prose hay bảng tham số (preference mạnh của người dùng):** identifier kiểu `select_starts`, `severe_burst`, hằng số seed `50260+17w`, tên cờ/hàm code — bọc `\texttt{}` hay không — đều KHÔNG được xuất hiện trong văn xuôi/caption/bảng params. Người dùng coi đây là "không ổn" (lộ ruột code, mất tính hàn lâm). Thay bằng mô tả tự nhiên: `\texttt{severe\_burst}` → "severe-burst channel" (chữ thường, chạy dòng); `select_starts` → "identical window starts"; seed `50260+17w` trong bảng params → "fixed, reproducible" / "paired seeds" (vẫn truyền được tính tái lập mà không khoe hằng số). Cách rà: `grep -rn "texttt|_starts|_burst|<magic-number>|verb|lstinline" sections/ main.tex`, mục tiêu 0 match trong thân bài. Tên kênh/biến chuẩn được phép giữ ở dạng toán (vd $N{=}30$, $B{=}4$, G–E $P_{gg}$) — chỉ identifier-thuần-code mới phải dịch.
- **Ngoặc mô tả cấu hình lặp lại = cắt bớt:** khi nhiều câu/ngoặc nhồi lại cùng một bộ tham số đã khai ở §Setup + bảng params (vd "(identical select_starts, seeds ..., severe_burst channel, N=30, B=4, single batch)"), người dùng thấy "không cần lắm". Nén còn mô tả tối thiểu cần cho tính tái lập ("same matched windows, paired seeds") và bỏ phần trùng; đừng lặp full config ở mỗi subsection.
- **Symbol-used-in-algorithm-without-defining-equation + wrong-attribution (verify với CODE):** nếu Algorithm/objective dùng một đại lượng (vd system risk $R_{t^-}$ trong $-c_R R_{t^-}b$) thì đại lượng đó PHẢI có phương trình định nghĩa tường minh ở đâu đó — đừng để nó xuất hiện trong pseudocode mà không bao giờ được viết ra (vi phạm \"tường minh\" của người dùng). Bug thật phiên bài bandwidth-scheduling: $R_{t^-}$ dùng trong Algorithm 1 nhưng KHÔNG có equation; tệ hơn, một câu prose lại gán nhầm tổ hợp-5-cue cho $p^{\\mathrm{vio}}$ (vốn là CDF Gauss đơn lẻ, Eq khác). Đọc CODE để biết tổ hợp 5-cue thực ra thuộc về symbol NÀO (`risk_score()` = `0.45*maxp+0.20*meanp+...` chính là $R$, không phải $p^{\\mathrm{vio}}$), rồi: (1) thêm equation định nghĩa $R$ khớp code 1-1; (2) sửa mọi câu prose gán nhầm; (3) phân biệt proxy lệch dự đoán $e_{i,t^-}$ (`proxy_error()`) với deviation $\\Delta$ ở per-sensor score nếu là hai đại lượng khác nhau. Quy tắc tổng quát: grep mọi symbol xuất hiện trong Algorithm/objective, mỗi cái phải truy được về một `\\label{eq:}` định nghĩa; mỗi \"tổ hợp N thành phần\" phải gán đúng symbol mà code thật aggregate.
- **Theorem-vs-discussion coherence:** khi thêm theorem (vd asymptotic optimality),
  rà Discussion/Limitations — câu cũ kiểu "not justified by optimality relative to a
  restless-bandit benchmark" giờ MÂU THUẪN với theorem mới. Viết lại cho khớp + giải
  mọi lời hứa "revisit in §discussion" mà section đó chưa có đoạn tương ứng.
- **Dataset-claim audit:** khi người dùng hỏi "chạy mấy dataset" / "experiments setup
  viết đủ chưa", verify dataset THẬT trong repo (`find data -name '*.npy'` + grep
  script load path + đọc CSV kết quả tồn tại) TRƯỚC khi khẳng định. Bắt mâu thuẫn
  "All experiments use Intel" trong khi có bảng robustness Beijing/KETI — viết lại
  setup nêu rõ primary vs robustness.
- Sau mọi sửa: full build chain + grep undefined = 0, rồi `pdftotext` xác nhận eq
  mới render trong PDF; báo bảng nhất quán (section nào dùng model nào, ✓/✗).

#### Nâng cấp figure pipeline để "thể hiện chiều sâu thuật toán"

Khi người dùng nói figure "còn đơn giản quá, chưa thể hiện chuyên sâu về thuật toán"
(hay xin vẽ giống bài NCS/UAV-EAV sensor), đây là EXECUTE vẽ lại TikZ — xem
`references/manuscript-figure-algorithmic-depth.md`. Bài học cốt lõi: (1) backup
figure cũ vào `_backups/`; (2) figure phải hiện cơ chế mà TÊN method ngụ ý nhưng
sơ đồ khối cũ bỏ sót (vd per-arm channel block + belief filter predict→update +
mũi tên p_i(t) feed cả hai stage + vòng phản hồi delivery outcome o_i → cập nhật
belief = thể hiện restless/POMDP); (3) thêm công thức index tường minh mỗi stage;
(4) công thức dài hay TRÀN/ĐÈ tiêu đề stage — đặt xuống dòng riêng, cỡ scriptsize,
khoảng trống giữa hàng hộp; (5) VERIFY bằng cách render trang đó ra PNG
(`pdftoppm -png -r 150 -f <page> -l <page> main.pdf /tmp/fig`) rồi vision-check
chữ có bị cắt/đè/tràn lề không — build sạch KHÔNG đủ để biết layout figure đúng.
Khi người dùng đòi figure thể hiện cả LUỒNG DỮ LIỆU (uplink nhận gì / downlink gửi
gì / mỗi phase truyền cái gì từ đâu đến đâu): gắn nhãn DL/UL trên TỪNG mũi tên
truyền, thêm khối "wireless medium + N sensors" làm nơi mọi DL/UL cắm vào, và đóng
ĐỦ các vòng (đặc biệt vòng payload-uplink X_i,o_i → cập nhật belief hay bị thiếu);
chi tiết trong `references/explaining-pipeline-and-mechanism-math.md`.

#### Giải thích pipeline bằng lời + đưa toán cơ chế vào System Model

Khi người dùng yêu cầu thuyết minh pipeline/figure BẰNG LỜI (giải nghĩa từng ký tự),
làm rõ ý nghĩa công thức (bộ lọc Bayes, xác suất truyền tính kiểu gì), hỏi một câu
cơ chế sâu lộ ra hiểu nhầm khi đọc ngang, hoặc bảo "đưa toàn bộ vào System Model
với công thức + giải thích tường minh" — dùng
`references/explaining-pipeline-and-mechanism-math.md`. Bài học cốt lõi: (1) đọc
file figure thật trước, trả lời theo cấu trúc tổng-quan → BẢNG glossary từng ký
hiệu → thuyết minh luồng đánh số → tóm mạch → map challenge; (2) bắt & đính chính
HIỂU NHẦM của người dùng ngay đầu phản hồi (✓/❌); (3) chứng minh cơ chế động bằng SỐ
THẬT reproduce thẳng từ code (vd belief self-healing hội tụ về π^B sau ~10 vòng),
không hand-wave; (4) khi đưa vào §2: backup, đọc §2 hiện có tránh trùng, thêm 3
khối (state estimator theo tuổi, ma trận G-E + stationary, self-healing hội tụ hình
học), mỗi `\eqref` phải có `\label`, khớp code 1-1, build chain + render + vision.

### Stage 7 - Multi-perspective Review

Mục tiêu: review như hội đồng phản biện, không chỉ sửa văn phong.

Reviewer roles:
- Editor-in-Chief: fit, contribution, decision.
- Methodology reviewer: design, data, metrics, validity.
- Domain reviewer: prior work, theory, domain accuracy.
- Cross-disciplinary reviewer: clarity, transferability, missing assumptions.
- Devil's Advocate: phản biện core argument, counter-claims, logic fallacies.

Trước khi chốt verdict: chạy claim-check tự động cho các câu khẳng định có trích nguồn (jev_decide noul claim↔source; đo thật trên jev-1.13.0: ca "nói quá" bị bắt ở noul 0.03–0.04, ~300–400ms/call, claim paraphrase-đúng-nhưng-thêm-inference rơi dải giữa 0.58 → escalate) — `references/jev-systemone-claim-gate.md`.

- Khi người dùng nói "agent tự làm reviewer đọc sâu từng mục, đánh giá nghiêm khắc" + "sửa liền" (EXECUTE review, không chỉ liệt kê comment), dùng `references/reviewer-deep-read-theory-code-consistency.md`. Bài học cốt lõi: bug nghiêm trọng nhất là THEORY GIẢ ĐỊNH X NHƯNG CODE CHẠY Y (vd §5 chứng minh trên Gaussian Φ nhưng code dùng empirical bootstrap) — đọc code thật xác định deployed path, quantify data property (kurtosis/tail-mass) để biết được phép claim gì, reconcile bằng cách tách "chọn functional nào" khỏi "ước lượng thế nào", sửa ở MỌI nơi nhắc tới (abstract+§method+§eval bảng+§theory, grep symbol). Kèm: số abstract phải recompute từ CSV deployed-variant hiện tại (tên baseline phải khớp batch); bắt ký hiệu kép cùng đại lượng (μ_i vs X̂_i, p_succ vs p_i(t), "Kalman posterior" mà không có measurement-noise = thực ra AR(1) forecast thuần); fix rẻ khi có sibling agent = thêm câu cầu nối buộc hai ký hiệu thay vì viết lại; verdict mở đầu + bảng severity tách ĐÃ-SỬA vs GHI-NHẬN, giữ góc người đọc tích cực ở cuối. Reference này cũng có: (a) bug hằng-số TỰ-KHỚP-NỘI-BỘ nhưng SAI ~2.5× so dữ liệu thật (manh mối duy nhất là VÊNH giữa hai section cho cùng đại lượng); (b) khi người dùng duyệt nâng số-window sweep (12/8→30): propagate prose+bảng+TÁI-TẠO-figure-PNG+câu-metadata, narrative có thể ĐẢO (đỉnh gap đổi B=6→B=4, severity hết \"identical\"); (c) AUDIT ACRONYM first-use (đầy đủ ở lần đầu THÂN bài, abstract không tính, bắt acronym-lần-đầu-trong-bảng + tên-method-chưa-viết-đầy-đủ); (d) GIẢI NGHĨA từng Lemma/Theorem bằng lời (nhóm theo mạch chứng minh, ⭐ định lý chính, ⚠️ kết quả trung thực về giới hạn, hỏi trước khi nhúng intuition vào bài).\n- Khi người dùng hỏi "đã so sánh với SoTA mới nhất/tốt nhất chưa?" hoặc thêm baseline gần đây vào bảng so sánh, dùng `references/sota-baseline-comparison-integrity.md`. Bài học cốt lõi: (1) audit baseline hiện có — họ kinh điển tự cài (Whittle/MaxWeight/AoII/VoI) KHÔNG phải "SoTA mới", reviewer Q1 sẽ đòi method có tên 2024-2025; (2) STRAW-MAN DETECTION: nếu baseline công bố gần đây thua method mình quá đậm (25-90×) VÀ thua cả baseline kinh điển → gần chắc mình cài KHÔNG công bằng (metric mismatch / thiếu safety-gating), KHÔNG đưa số vào bảng, dừng hỏi người dùng chọn framing (fair-tune vs as-published+honest); (3) verify citation LIVE qua HTTPS arXiv API (`http` trả 0 byte; gọi từ execute_code timeout → dùng terminal curl 25s), không bao giờ cite từ trí nhớ, subagent literature nền hay fail im lặng thì tự verify inline.\n- Với IEEE Internet of Things Journal, dùng thêm `references/ieee-iotj-manuscript-review.md`. Với precedent bài probe-transmit/bài AoI-greenhouse, xem `references/probe-transmit-iotj-revision.md` để nhớ cách bỏ nhánh yếu khỏi narrative, đối chiếu số liệu repo, và tạo highlighted PDF. Với bài bandwidth-scheduling/hội nghị C1 hoặc bài adaptive-bandwidth greenhouse IoT, xem `references/rabs-stais-revision.md` để nhớ narrative composite safety--bandwidth, metric pitfalls, và cách làm rõ toán bài bandwidth-scheduling-PD. Nếu bài bandwidth-scheduling có mâu thuẫn giữa text/algorithm/setup và code hoặc người dùng muốn đổi N/scale simulation, dùng thêm `references/rabs-code-vs-manuscript-integrity.md`: code+CSV là source of truth, deployed bài bandwidth-scheduling-PD là 3-dual, dataset thật là N=3 measured zones, và N=30 semi-synthetic có thể đảo thesis nên phải full-run trước khi pivot. Khi bài gần submit-ready nhưng còn cảnh báo layout LaTeX/IEEE, dùng `references/latex-ieee-layout-polish.md`. Khi người dùng hỏi chọn tạp chí Q1/category/fast publication, dùng `references/journal-q1-selection.md` để kiểm tra category-fit thay vì chỉ nhìn Best Quartile. Reference này cũng có recipe lấy review-speed/IF/section THẬT bằng `curl` trang chính thức khi Scimago/Google/ScienceDirect chặn headless browser (đừng tin web-subagent — nó exit "completed" với 0 tool calls), kèm số đã verify cho IEEE IoTJ (first-decision 6.9 tuần, ePub 14.5 tuần, có track Expanded Conference Papers) và IEEE Sensors J (ePub 8.8 tuần median).

Deliverable:
- Major issues: severity, location, evidence, fix.
- Minor issues.
- Editorial decision: accept/minor/major/reject-style recommendation.
- Revision roadmap: prioritized actions.

### Stage 8 - Revision và Re-review

Mục tiêu: sửa theo ma trận, không sửa cảm tính.

Deliverable:
- Response matrix: comment -> action -> file/section -> evidence -> status.
- Revised manuscript.
- Re-review report: comment nào đã giải quyết, comment nào còn blocker.

Khi người dùng yêu cầu chỉnh manuscript sau review:
- Ưu tiên câu chữ ngắn, trực tiếp, ít marketing/overclaim; rút văn phong trước khi thêm nội dung.
- Với phần toán học, làm rõ bằng định nghĩa biến, assumption, statement, rồi proof theo cấu trúc khoa học thường dùng: statement -> set/fix variables -> displayed equality/inequality chain -> implication -> conclusion (`\square`). Ít chữ, nhiều biến đổi rõ; tránh tutorial prose dài và không nhảy bước bằng câu "it is clear".
- Nếu proof chưa đủ chắc, hạ claim thay vì cố giữ theorem mạnh: đổi matching/tight/global-convergence thành sufficient bound, lower-bound example, remark, hoặc empirical validation.
- Luôn tách deployed implementation khỏi analysis variant. Nếu guarantee chỉ đúng cho variant lý tưởng, title/abstract/contribution phải nói rõ.
- Khi có lựa chọn triển khai, chốt một deployed variant rồi đồng bộ title/abstract/method/table/narrative theo variant đó; optional variant chỉ để ablation/extension.
- **Missing-citation handling (KHÔNG tự bịa bib entry):** khi review/audit/RLM bắt một claim THIẾU `\cite` và `.bib` không có entry verify-được phù hợp, default là **gỡ hook cụ thể** (năm chính xác, con số kỹ thuật, threshold, tên công cụ riêng) để câu trở thành phát biểu chung tự đứng, KHÔNG tự thêm `@article` chưa verify. Ví dụ thật phiên LVTN: \"Tassiulas và Ephremides (1992) áp dụng...\" → gỡ \"(1992)\"; \"5G NR... độ trễ thấp (\\textless 10ms)\" → gỡ \"(\\textless 10ms)\"; \"các công cụ chuẩn (như Cochrane RoB)\" → \"các công cụ đánh giá rủi ro thiên lệch chuẩn\"; \"đều nhấn mạnh\" (tuyệt đối) → \"có nhấn mạnh\". Chỉ thêm bib entry mới khi người dùng duyệt VÀ metadata được fetch live từ Crossref/arXiv API trước (xem `references/crossref-api-citation-verification.md`). Lý do: người dùng cấm bịa cite; reviewer Q1 mở DOI là thấy ngay; gỡ hook bảo toàn ý chính mà không tạo nợ liêm chính.
- Nếu người dùng loại một thành phần khỏi câu chuyện chính vì làm bài xấu/không có tác dụng, xóa sạch thành phần đó khỏi title, abstract, contribution, method, related work, evaluation, discussion, conclusion, figure comments/colors, và artifact text; không để lại nhánh “optional” hoặc tên đối lập kiểu `debt-only` nếu thành phần đối lập đã bị loại.
- Khi số liệu/claim có repo công khai đi kèm, clone/pull repo chuẩn vào `SAS/Research/_repos/<repo>/`, đối chiếu CSV/JSON/script output trước khi cập nhật số chính, và đưa đúng link repo vào Data and Code Availability.

Quy tắc: tối đa 2 vòng revision lớn trước khi cần hỏi lại chiến lược.

### Stage 9 - Integrity, Reproducibility, Compliance

Mục tiêu: trước khi gọi artifact tốt/ready, kiểm tra gate.

Checklist:
- Citation integrity: DOI/metadata/ref consistency.
- **Thesis PRISMA/corpus-count consistency + figure audit:** Khi người dùng hỏi các số kiểu ban đầu bao nhiêu rồi giảm dần tới tập lõi đã đủ trong phụ lục chưa, hoặc yêu cầu “quán triệt toàn bộ nội dung/kể cả hình ảnh”, dùng `references/thesis-prisma-consistency-and-figure-audit.md`. Bài học cốt lõi: phụ lục/audit trail là nguồn truth, main text phải theo một flow PRISMA duy nhất (vd 627→424→187→64); nếu corpus count đổi thì đồng bộ số đếm, phần trăm, phụ lục, caption, kết luận và package; kiểm `pdftotext` trên PDF hình vì hình tự chứa `n=120/81/68` có thể mâu thuẫn dù caption đã sửa; tái tạo hình từ corpus cuối hoặc chuyển hình cũ vào `_backups` và exclude khỏi zip; Việt hóa form PRISMA chính, không để `Eligibility/Included/candidate/title-abstract screening` trong bảng/caption chính trừ khi là raw audit-status. Khi chỉnh PHỤ LỤC PRISMA, dùng thêm `references/thesis-prisma-appendix-presentation.md`: phụ lục phải ngắn, ưu tiên bảng/flow + danh mục công trình lõi kiểu tài liệu tham khảo; không in tên file, tên code, biến, raw IDs, query IDs hoặc bảng bằng chứng nội bộ dài — phần trình bày diễn giải nằm ở chương chính.\n- **Figure-generation-script integrity (hình sinh từ script có thể dùng SỐ BỊA hoặc DỮ LIỆU SAI).** Khi vision-audit phát hiện hình mâu thuẫn caption/thân bài (vd caption ghi n=64 nhưng chart vẽ n=120/81/148), ĐỪNG vá ảnh — truy SCRIPT sinh hình. Ba lỗi thật phiên LVTN: (1) script hardcode `N_TOTAL=120` / fallback `=81` + tỉ lệ tay → số trên hình không khớp corpus thật; fix = viết lại script đọc CSV mã hóa per-paper (`open()` thuần), đếm thật, `assert N==<đúng>`, regen, vision-verify. (2) script sinh hình thống kê có comment tự thú `\"data giả lập\"` (energy/IAE bịa \"bám kết luận\") — thay bằng số mô phỏng THẬT từ benchmark CSV. (3) hình minh họa giáo khoa có BUG VẬT LÝ: ETC ra NHIỀU gói hơn periodic (ngược bản chất) vì ngưỡng sự kiện (0.05) sát dải nhiễu đo (std 0.02) → chattering; mô hình lại chỉ có phân rã, không setpoint/nhiễu để \"bám\". Fix = mô hình hóa đúng (setpoint bậc thang + nhiễu, ngưỡng ETC ≫ dải nhiễu) cho ETC < periodic, rồi vision-verify số. (4) matplotlib figure để nhãn/title/legend TIẾNG NGƯỜI DÙNG trong luận văn tiếng Việt — Việt hóa trong script, GIỮ tên method/ký hiệu (TT-MPC, RMSE, °C, LoRa); coi chừng đơn vị lẫn lộn (trục mJ nhưng legend J) + `np.trapz` bỏ ở numpy 2.x (dùng `getattr(np,'trapezoid',np.trapz)`). Quy tắc: con số trên hình phải truy được về CSV/dữ liệu thật y như số trong bảng; build sạch KHÔNG chứng minh hình đúng — phải render trang ra PNG + vision-check.
- **Thesis LaTeX finishing (longtable/float ordering) + review false-positives:** Khi convert `table`→`longtable` để chữa `Float too large`, hoặc khi review-subagent báo lỗi cần VERIFY trước khi sửa, dùng `references/thesis-latex-finishing-and-review-false-positives.md`. Bài học cốt lõi: (1) longtable KHÔNG phải float nên ghim tại chỗ, các float cùng nhóm định nghĩa trước có thể drift xuống dưới → số hiệu (theo source) lệch thứ tự in (theo trang); fix bằng `\clearpage` ngay trước `\begin{longtable}`, rồi kiểm lại `.lot` order; (2) số trang trong `.aux`/`.lot` là trang LOGIC, `pdftoppm` cần trang VẬT LÝ (lệch do front matter) — resolve physical page trước khi render vision-check; (3) false-positive review hay gặp: cite-key≠author là bình thường (verify `.bib` author field), vision đọc nhầm dấu hỏi/sắc trên hình raster (verify `.tex` source), locked section (Mở đầu=đề cương) override quy tắc neutral-tone; (4) `Float too large by ~12pt` residual chỉ là mỹ thuật, không chặn nộp — chỉ overflow hàng trăm pt mới cần fix cấu trúc.\n- **Thesis formatting (trường ĐH) + defense slides + companion repo:** Khi người dùng nói rà ĐỊNH DẠNG luận văn theo chuẩn Trường (bố cục front matter, indent, giãn dòng), giảm độ dày, dựng SLIDE BẢO VỆ, hoặc tạo/đẩy companion repo cho LVTN, dùng `references/thesis-formatting-defense-and-companion-repo.md`. Bài học cốt lõi: (1) **stale-PDF/multi-output trap** — `build.sh` có `cp build/main.pdf ./main.pdf` đẻ nhiều bản PDF, đọc nhầm bản cũ → báo SAI số trang nhiều lần; gỡ dòng cp + `find -name main.pdf` trước khi tin page count; (2) front matter order chuẩn = Bìa→Bìa phụ→Cam đoan→Cảm ơn→Mục lục→**Viết tắt** (ngay sau mục lục, KHÔNG để cuối)→Hình→Bảng→Thuật toán; cam đoan/cảm ơn phải nằm SAU `\frontmatter` để được số La Mã; giãn dòng trường ĐH = 1.5 (đổi từ 1.15 làm tăng trang — báo rõ là đúng chuẩn không phải phình nội dung); GIỮ `\part{}`; (3) front-matter có thể là TEMPLATE STALE của đề tài khác — lấy biến bìa thật từ `Libs/settings.tex`, không đoán; (4) giảm trang bằng đẩy `longtable` thô (627/424 nguồn) ra CSV `bib_audit/`, grep `\ref{label}` trước khi xóa; (5) push repo khi SSH bị chặn = token file tạm + tokenized HTTPS inline (không lưu config), verify LIVE bằng `gh api`; secret-scan đọc từng match (prefix `hf_`/path nội bộ là false-positive); (6) quy chế Trường KHÔNG ở Thông tư Bộ — site trường ASP.NET postback headless không lách được, search engine chặn bot, nói thẳng không bịa; (7) slide defense map theo mạch Đặt vấn đề→Phương pháp→Cơ sở lý thuyết→Kết quả tổng quan→Kiểm chứng→Kết luận, số lấy từ CSV thật.\n- **Thesis chapter structure/style editing:** Khi người dùng nói “tiếp tục đối với chương X của LVTN, rà cấu trúc/văn phong”, hoặc sửa lại rằng không chỉ sửa câu chữ mà phải rà mạch đọc/nội dung có quan hệ/không lan man, dùng `references/thesis-chapter-structure-style-editing.md`. Bài học cốt lõi: chỉnh trực tiếp file `.tex` đang active, backup có kiểm soát, rà cấu trúc trước văn phong, gộp đoạn/tiểu mục lặp nhưng giữ `\label` cũ, giữ một luồng PRISMA/corpus-count duy nhất, thêm câu dẫn trước và kết luận ngắn sau từng bảng/hình chính để người đọc định hình vai trò của artifact, nêu các bước triển khai bằng lời ngắn đúng trọng tâm, build bằng đúng engine (`-xelatex` nếu có `fontspec`), và báo rõ cảnh báo build nào là pre-existing/unrelated. Nếu người dùng nhắc “check các hình ảnh cho kĩ rồi mới rà tiếp chương sau”, phải dừng rà chương sau cho tới khi render các trang chứa hình/bảng ra ảnh, vision-check layout/caption/độ đọc, sửa figure TikZ/caption nếu cần, build lại sạch rồi mới chuyển chương.
- **Ready-submit polish (multi-lens review + layout + code-leakage sweep + packaging):** Khi người dùng nói "rà soát kỹ luận văn, đủ ready-submit chưa", dùng `references/thesis-ready-submit-polish-and-code-leakage.md`. Bài học cốt lõi: (1) PLAN-FIRST rồi RUNNING PROGRESS (người dùng ngắt nếu nhảy vào sửa ngay hoặc im lặng quá lâu); 3 subagent READ-ONLY chia theo FILE, parent là nơi duy nhất ghi + verify mọi finding số liệu từ CSV trước khi patch; (2) longtable fix cho "float too large" + `\clearpage` để chữa thứ tự số hiệu bảng đảo (longtable ghim chỗ vs float trôi xa), verify bằng `.lot` + render trang VẬT LÝ; (3) code-identifier leakage sweep — tên file/đường dẫn/script trong THÂN BÀI phải bỏ (thay bằng mô tả + trỏ phụ lục), GIỮ raw trong phụ lục audit/query Boolean/link repo; (4) packaging: dual-PDF stale trap (md5 cả hai), exclude venv/pycache/backup/aux, liệt kê trước khi xóa rác.
- Claim-faithfulness: claim trong text có đúng với source không.
- Figure/table trace: dữ liệu vẽ từ source/script, không sửa tay số liệu.
- Variant-consistency audit: khi có companion repo, recompute mean/CI của TỪNG bảng từ CSV gốc và xác nhận tất cả bảng (results, SoTA, tail, ablation, sensitivity) cùng sinh ra từ ĐÚNG MỘT deployed variant. Lỗi nguy hiểm hay gặp: headline number lấy từ ablation variant A, nhưng các bảng so sánh + bội số (39×, 43×...) lại sinh từ variant B cũ -> mâu thuẫn nội tại, reviewer/reproduce bắt ngay. Đọc thẳng script sinh số (vd `*_30windows.py`, `tail_metrics.py`) để xem chúng khởi tạo method bằng variant nào, đừng tin nhãn cột. Kiểm bội số bằng tay (loss_baseline/loss_method) phải khớp giá trị headline, không khớp giá trị variant cũ.
- Claim-vs-implementation mismatch: nếu manuscript mô tả method A (vd debt-only) nhưng code sinh thực nghiệm chạy method B (vd corr+debt, do `use_correlation_credit=True` mặc định), đây là lỗi liêm chính nghiêm trọng — phải re-run đúng deployed variant rồi cập nhật mọi bảng, hoặc đổi mô tả cho khớp. Cảnh báo người dùng trước khi chạy job nặng và xin duyệt.\n- **Unverifiable derived-statistic pitfall (effective rank, condition number, mixing time, eff. sample size...).** Một con số dẫn-xuất trong manuscript có thể KHÔNG có code tính kèm — chỉ nằm trong docstring/comment hoặc trí nhớ. Phiên bài AoI-greenhouse: \"effective rank 1.7/7.3\" cho Beijing/KETI chỉ ở docstring `robustness_multidataset.py`, không có hàm tính. Khi người dùng chỉ vào bảng và hỏi/yêu cầu verify (hoặc \"chạy lại\"): (1) tìm script sinh số gốc; nếu KHÔNG có, con số đó không reproducible → không được giữ. (2) Hiểu rằng các metric kiểu \"effective rank\" có NHIỀU định nghĩa cho giá trị rất khác nhau trên cùng dữ liệu — participation ratio, entropy-based (Roy–Vetterli), stable rank (trace/λmax) ra 3 số khác hẳn (vd KETI: 5.1 / 9.96 / 2.6). Số cũ có thể tình cờ khớp một định nghĩa cho dataset này (Beijing 1.78≈1.7 entropy) nhưng không định nghĩa nào ra 7.3 cho dataset kia → bằng chứng số gốc dùng tham số/định nghĩa không ai biết. (3) Fix đúng: chọn MỘT định nghĩa có trích dẫn, viết script reusable tính cho TẤT CẢ dataset bằng cùng pipeline (khớp tiền xử lý gốc — vd shrinkage 0.1 trên train split `min(2000,0.6T)`), chạy thật, rồi thay đồng bộ MỌI chỗ trong manuscript (bảng repro + itemize + bảng robustness header + đoạn diễn giải) — grep `1\\.7|7\\.3` để không sót. (4) Verify luôn cả số neo khác cùng họ (T = số dòng panel `.npy` thật qua `np.load(...).shape`, không retype) vì nếu một số dẫn-xuất sai thì các số khác đáng ngờ theo. Khi không tái hiện được số gốc, nói thẳng với người dùng (người dùng dặn không bịa) và đề xuất dùng số verify-được + ghi rõ định nghĩa, đừng giữ số treo.\n- **Scale-up simulation lên N lớn hơn (claim/code mismatch về quy mô).** Khi manuscript ghi một quy mô (vd N=30) nhưng code chạy quy mô khác (vd 3 sensors) và người dùng chọn nâng code lên đúng quy mô bài, dùng `references/scaling-simulation-N-regime-flip.md`. Bài học cốt lõi: (1) scale-up có thể ĐẢO CHIỀU regime và VỠ luận điểm chính (B/N đổi bậc → under-observation → age-based bỗng thắng risk-aware, tín hiệu rủi ro bão hòa mất discrimination) — phải cảnh báo TRƯỚC và SMOKE-test trước full run; (2) KHÔNG fudge hằng số phạt để ép method thắng lại = bịa số, gặp regime-flip thì DỪNG + trình A/B/C trung thực cho người dùng quyết (khuyến nghị quay về N nhỏ giữ kết quả đã verify); (3) materialize sensor ảo từ ít trace thật phải trung thực (time-offset replay + per-arm G-E, giữ nguyên giá trị đo thật, khai báo bán tổng hợp, layout deterministic giữ paired-comparison); (4) mis-scaling hằng số theo N (chi phí B tuyệt đối vs lợi ích 1/N) làm Oracle hóa tệ nhất — fix N-invariant bằng `BW_SCALE=K/N` nhân mọi hệ số phạt-theo-B + `AOI_NORM`, đây là rescale CÓ NGUYÊN TẮC (khác fudge); (5) refactor `range(K)`→`range(NSENS)`: tham số hóa, vector hóa kênh `bad[i]`, `random.Random` không nhận tuple seed.\n- **Stale-tables / full-pipeline re-run.** Khi MỘT số li ti sai làm người dùng nghi ngờ toàn bộ (\\\"vẫn còn nhiều sạn\\\", \\\"rà chỗ nội dung cũ chưa đụng vào\\\", \\\"xoá hết kết quả rồi chạy lại một lượt cho đồng bộ\\\"), đừng chỉ sửa một ô — RE-RUN cả pipeline. Dùng `references/stale-numbers-full-pipeline-rerun.md`. Bài học cốt lõi: (1) bảng số trong manuscript có thể được dán từ NHIỀU lần chạy ở thời điểm khác nhau → một số bảng reproduce 100% (chạy gần nhất) trong khi Table-I/Whittle/ablation/robustness STALE (sinh từ code cũ); manh mối là CROSS-TABLE INCONSISTENCY cho cùng method (Table I ghi 0.0024, SOTA ghi 0.0028) — số \\\"fresh\\\" là cái xuất hiện nhất quán ở nhiều script. (2) Recipe: map script→CSV, backup docs cũ, smoke test, chạy lại lần lượt (script nặng background+wait), so old-vs-new bằng script, trích MỌI số bằng một script tổng (mean±1.96·sd/√n + claim phái sinh), thay đồng bộ vào .tex, grep số cũ để không sót, build+verify render. (3) Pitfalls: runtime phụ-thuộc-máy phải HỎI giữ-gốc-hay-thay; narrative có thể ĐẢO khi số đổi (Whittle-exact hết \\\"rẻ hơn về loss\\\"; ablation 5×→8×) nên viết lại đoạn diễn giải + p-value chứ không chỉ thay số; map đúng CSV→bảng (DT+AoI, debt-ablation, no-debt-vs-debt mỗi cái một CSV khác); verify số neo cùng họ (T qua `.npy.shape`, α/σ/kurtosis tính trực tiếp từ data).
- **Derivative papers become thesis branches + thesis simulation rerun.** When using, bắt buộc xem chi tiết cập nhật trong `references/thesis-paper-integration-and-simulation-rerun.md`: không đụng Mở đầu/đề cương nếu người dùng cấm; bài AoI-greenhouse có thể là nhánh nối trực tiếp từ mô phỏng, bài bandwidth-scheduling là nhánh sản phẩm liên quan/bổ trợ; RLM readiness phải kiểm corpus unique-count, figure corpus mismatch, stale narrative, refs/cites, build + zip sạch. Khi người dùng nói các bài như bài bandwidth-scheduling và bài AoI-greenhouse/bài probe-transmit là MỘT PHẦN của luận văn và yêu cầu điều chỉnh, đặc biệt \"simulation trong luận văn agent làm lại luôn\", dùng `references/thesis-paper-integration-and-simulation-rerun.md`. Bài học cốt lõi: (1) đây là EXECUTE: inspect thesis includes + backup + sửa prose + rerun code + build PDF; (2) nếu người dùng dặn **không đụng phần Mở đầu/đề cương** thì giữ `modau.tex` nguyên baseline, chỉ nối logic ở chương nội dung, kết luận và phụ lục; (3) định vị paper như nhánh chuyên sâu của cùng bài toán đồng thiết kế control--communication, không như phụ lục rời — thường bài AoI-greenhouse là nhánh nối trực tiếp với simulation, bài bandwidth-scheduling là sản phẩm/nhánh liên quan về resource allocation; (4) sửa simulation theo pipeline thật, patch path hardcode thành project-relative nếu cần, chạy tests/pipeline, lấy số từ CSV fresh rồi thay narrative cũ; (5) kiểm tra file publication có thật sự được `main.tex` include không — nếu không, thêm PDFs vào appendix đang được include; (6) build bằng engine đúng của project (xelatex nếu dùng fontspec), clean aux/toc stale khi đổi engine, rồi verify PDF text có bài bandwidth-scheduling/bài AoI-greenhouse/số mới. Khi người dùng hỏi liệu chương mô phỏng \"làm như bài CAW\" và kết quả có \"lấy từ đó\" không, xem thêm `references/thesis-simulation-caw-vou-integration.md`: phân biệt kết quả từ pipeline mô phỏng nền/CSV (`q1_benchmark_summary.csv`) với kết quả trực tiếp trong paper bài AoI-greenhouse; chỉ claim direct paper provenance khi đã đối chiếu được bảng/hình/source paper.
- **Companion-repo submission-readiness gate (người dùng coi repo công khai là MỘT phần của bộ nộp — hỏi \"code đẩy lên github đã ổn và sạch chưa?\").** Khi người dùng hỏi repo đã sạch/sẵn-sàng chưa, audit repo THẬT trên GitHub, không chỉ thư mục local (thư mục manuscript thường KHÔNG phải git repo): (1) `gh auth status` + `gh repo view <owner>/<repo> --json visibility,pushedAt,isEmpty,diskUsage` cho từng repo bài trỏ tới (URL trong \"Data and Code Availability\"); (2) clone về thư mục GHI ĐƯỢC (`/tmp` có thể bị permission-denied → dùng `~/gh_check`), `git clone --depth 1`; (3) **secret scan với cảnh giác false-positive:** `grep -rniE 'api[_-]?key|secret|password|token|gho_|ghp_|sk-|AKIA|private[_-]?key|bearer'` rồi ĐỌC TỪNG dòng match — phần lớn là false-positive (\"secrets\" trong audit md, \"font-**weight**\", \"risk **weight**s\", \"**token**izer\"), chỉ báo secret thật khi là giá trị credential; (4) junk scan: `find` cho `*.aux *.log *.pyc .DS_Store __pycache__ venv .env *.bak`, đối chiếu `.gitignore`; (5) **QUAN TRỌNG NHẤT — repo↔paper number sync:** so `pushedAt` của repo với ngày sửa số liệu bài; nếu repo cũ hơn, số CSV trong repo có thể LỆCH số trong bảng. Recompute mean từ CSV repo bằng execute_code (vd `sota_comparison_30windows.csv` → loss_mean per policy) và đối chiếu headline bài (bug thật phiên này: repo bài AoI-greenhouse loss 0.0024/missed 0.0367% vs bài 0.0028/0.044% — lệch vì repo push 17/06, bài sửa tới 21/06). Reviewer tải repo về sẽ thấy số không trùng bảng → mất điểm reproducibility. (6) Báo người dùng: repo nào sạch kỹ-thuật, repo nào số lệch (liệt kê cặp old↔new), và đề xuất hoặc cập-nhật-bài-theo-CSV hoặc chạy-lại-push-CSV-mới (người dùng nghiêng về push CSV mới khi bài đã qua nhiều vòng rà). Cũng kiểm README có \"How to reproduce\" không (bài bandwidth-scheduling README chỉ có 1 dòng tiêu đề = sơ sài, nên bổ sung lệnh chạy + thứ tự script). **Khi người dùng chuyển từ AUDIT sang EXECUTE sync (\"đồng bộ code hết chưa, dữ liệu chuẩn chưa, up repo sạch lên github rồi chạy lại xem\"), dùng `references/companion-repo-sync-and-push.md`:** code working THẬT nằm ở `_repos/<repo>/` (chính là git remote, KHÁC thư mục manuscript), thường có afternoon re-run chưa commit; verify tái lập bằng cách re-run rồi diff CSV BỎ QUA cột runtime/wall-clock (0 ô khoa học lệch = reproducible, runtime đổi theo máy là bình thường); phân loại clean-vs-junk (spike_*/`_backups`/`_OLD`/`data/processed`/`outputs` = rác vào `.gitignore`) + `git add` tường minh KHÔNG `-A`; push public main là thao tác khó thu hồi nên GATE trên approval của người dùng.
- AI disclosure: nếu dùng AI trong paper, khai báo đúng stage/tool/version khi venue yêu cầu.
- Reproducibility note: model/tool/version, data/code path, stochasticity caveat nếu có.
- Privacy/ethics: dữ liệu nhạy cảm, consent, IRB nếu phù hợp.

### Stage 10 - Final Packaging

Mục tiêu: artifact nộp được về mặt kỹ thuật, không chỉ có nội dung.

Gate manuscript/LaTeX:\n- PDF freshness: PDF build sau lần sửa cuối.\n- Build log không có lỗi nghiêm trọng.\n- References compile đúng.\n- **XeLaTeX magic-comment (preference người dùng):** project nào build bằng xelatex (có `fontspec`/tiếng Việt) thì thêm `% !TEX program = xelatex` làm DÒNG ĐẦU TIÊN của `main.tex`. Người dùng yêu cầu rõ điều này để editor/Overleaf/collaborator chọn đúng engine, không phải đoán. Thêm vào bản gốc local LẪN bản trong mọi bundle gửi đi.\n- **⚠️ BUNDLE PHẢI BUILD-FROM-BUNDLE, không chỉ ship PDF prebuilt + đừng prune folder mà LaTeX include.** Bug thật phiên LVTN: dọn bundle \\\"sạch\\\" tôi xoá `fig_publication/` vì tưởng là rác → `main.pdf` prebuilt vẫn 227 trang OK, NHƯNG source trong zip KHÔNG rebuild được vì `phuluc.tex` có `\\includepdf{fig_publication/*.pdf}` (2 PDF công trình đính kèm) → `pdfpages Error: Cannot find file`. Người dùng build thử mới phát hiện. Quy tắc cứng cho mọi handoff zip: (1) TRƯỚC khi prune folder lạ (`build/ notes/ tools/ scripts/ simulation/ fig_publication/...`), grep `\\\\includepdf|\\\\input{|\\\\includegraphics|\\\\bibliography` xuyên `.tex` xem folder đó có bị reference không — folder được include là ASSET, KHÔNG phải rác; (2) sau khi đóng bundle, copy ra `/tmp` và CHẠY full build chain TỪ CHÍNH BUNDLE (xelatex→bibtex→xelatex×2), verify trang + 0 undefined + 0 lỗi pdfpages — \\\"PDF prebuilt mở được\\\" KHÔNG chứng minh source reproducible; (3) chỉ gọi bundle \\\"sạch/ready\\\" sau khi source rebuild thành công từ trong bundle.
- **⚠️ \"N trang, 0 lỗi\" KHÔNG đủ để kết luận bibliography đúng — bbl có thể RỖNG mà build vẫn sạch.** Bug thật phiên bài AoI-greenhouse IoT-J: bibtex sinh `main.bbl` với 41 `\bibitem` THÂN TRỐNG (chỉ có key, không có author/title/year) → PDF in `[1]...[41]` không nội dung, NHƯNG `pdflatex` vẫn exit 0, 14 trang, 0 \"undefined\". Người dùng phát hiện qua ảnh chụp (refs trống), không phải qua build log. Gate bắt buộc trước khi gọi submit-ready: (1) đọc `main.bbl`, đếm bibitem có thân: `awk '/\\bibitem/{getline x; if(x!="")c++} END{print c}'` phải = số ref kỳ vọng; (2) đọc `.blg` tìm `"missing a field name"` / `"I'm skipping whatever remains of this entry"` (phải = 0) — đây là dấu hiệu bibtex bỏ qua entry; (3) lưu ý `"(Error may have been on previous line)"` trong .blg là dòng CHÚ THÍCH của bibtex, không phải lỗi đếm được — đừng hoảng vì nó, nhưng PHẢI truy dòng `"missing a field name"` thật ở trên; (4) verify ≥1 ref render trong PDF bằng cách grep từng MẢNH (author + year) — refs 2-cột bị `pdftotext` xáo dòng nên grep cả-câu hay trượt, đừng kết luận \"thiếu\" chỉ vì grep cả câu fail.
- **⚠️ KHÔNG ghi đè `.bib`/`.tex`/file nguồn bằng output của `read_file` (qua execute_code).** `read_file` của hermes_tools trả content KÈM số dòng `N|` ở đầu mỗi dòng. Bug thật phiên này: dùng `execute_code` đọc `references.bib` bằng `read_file()` rồi `write_file()` lại để thay tên tạp chí hàng loạt → MỌI dòng nhiễm tiền tố `1|@article{...}`, `2|  author...` → `@article` thành `1|@article` → bibtex parse fail toàn bộ → bbl rỗng (xem pitfall trên). Quy tắc: để thay text hàng loạt trong file nguồn, dùng `patch(replace_all=True)` hoặc đọc file bằng **`open(path).read()` thuần Python** (KHÔNG dùng `hermes_tools.read_file`) trước khi `write_file`. Nếu lỡ nhiễm: strip bằng regex `re.sub(r'(?m)^\d+\|', '', raw)` sau khi backup bản hỏng vào `_backups/`, rồi rebuild + verify bbl đầy thân. **⚠️⚠️ Lỗi đi kèm NGUY HIỂM HƠN — TRUNCATION ngầm:** `hermes_tools.read_file` mặc định chỉ trả 500 dòng đầu. Đọc file >500 dòng rồi `write_file` ghi đè → file bị CẮT CỤT còn 500 dòng, mất sạch phần sau (build vẫn có thể chạy, chỉ thiếu nội dung). Bug thật phiên LVTN: script sửa 10 caption hàng loạt đọc `noidung_chap1.tex` (1199 dòng) + `chap2.tex` (666 dòng) không set `limit` → cả hai cắt còn 500 dòng + nhiễm tiền tố. Quy tắc cứng: KHÔNG read-rồi-write-toàn-file cho .tex/.bib dài; chỉ dùng `patch` sửa tại chỗ. Buộc đọc trọn trong Python thì dùng `open(path).read()` (trọn, không prefix, không limit). Sau sửa hàng loạt file nguồn dài: `wc -l` đối chiếu trước/sau — sụt mạnh = đã cắt cụt. RECOVERY SPLICE khi đã cắt cụt: (1) PDF build TRƯỚC lúc hỏng còn nguyên nội dung, không mất vĩnh viễn; (2) tìm backup đủ dòng (`find -name` + `wc -l`); (3) phần đầu file hiện tại (dòng 1..cut) thường còn session-edit sống sót — giữ; (4) splice = head-sống-sót + tail-từ-backup, ghép tại một anchor line trùng khớp tuyệt đối giữa hai bản (vd dòng TikZ `draw (net)--(ctrl)`) để không gãy/trùng; (5) tail backup là bản PRE-session nên edit ở vùng tail có thể bị revert — báo người dùng rõ; (6) build full chain + đủ trang + 0 undefined sau splice.
- **⚠️ BIBTEX + OUTPUT-DIRECTORY SUBAUX RESOLUTION BUG (confirmed TeX Live 2023).** Khi dùng `xelatex -output-directory=build main.tex`, LaTeX ghi `\@input{Chapter/noidung_chap4.aux}` vào `build/main.aux`. Khi chạy `bibtex build/main` từ project root, bibtex resolves `\@input{Chapter/...}` relative to CWD (project root → tìm `./Chapter/noidung_chap4.aux` thay vì `./build/Chapter/noidung_chap4.aux`). Hệ quả: bibtex KHÔNG đọc `\citation` từ chapter subaux → bbl thiếu entries mới → "Citation undefined" dai dẳng dù bib file parse OK. Triệu chứng: bibtex báo "Done" không warning, nhưng số bibitem trong bbl không tăng dù đã thêm entry + cite. **Fix đúng:** chạy bibtex TỪ TRONG output-directory: `(cd "$OUTDIR" && BIBINPUTS="..:$BIBINPUTS" BSTINPUTS="..:$BSTINPUTS" bibtex main) || true`. Khi đó `\@input{Chapter/...}` resolve thành `./Chapter/...` đúng (= `build/Chapter/...`). Kiểm chứng: grep `bibitem` trong bbl phải = tổng unique citation keys từ tất cả subaux.
- **⚠️ BIBTEX + OUTPUT-DIRECTORY TRAP (confirmed Jun 2026 on LVTN; see `references/bibtex-output-directory-and-crossref-verification.md` for diagnostic recipe).** When LaTeX uses `-output-directory=build`, bibtex resolves `\@input{Chapter/foo.aux}` relative to CWD, NOT relative to `main.aux` location. Running `bibtex build/main` from the project root means bibtex looks for `./Chapter/foo.aux` (doesn't exist) instead of `./build/Chapter/foo.aux`. Result: bibtex silently ignores all `\citation{}` lines in subaux files — produces a bbl with ONLY the entries cited in main.aux directly, no errors/warnings at all. Fix in `build.sh`: `(cd "$OUTDIR" && BIBINPUTS="..:$BIBINPUTS" BSTINPUTS="..:$BSTINPUTS" bibtex main)`. Symptom: bibtex reports "Done." with fewer entries than expected + new citations show as `[?]` in PDF despite bib file parsing correctly in isolation. Diagnostic: test with `cat > /tmp/test.aux` containing `\citation{newkey}` + `\bibdata{path/to/bib}` + `\bibstyle{IEEEtran}` — if bibtex finds the entry there, the problem is subaux resolution, not bib syntax.
- **⚠️ EXAMPLE/ILLUSTRATION TABLE INTEGRITY — cite-keys must match real papers.** When a table caption claims "trích xuất từ N nghiên cứu đại diện" but cite-keys don't match actual authors/year/domain in the bib (e.g. key `caceres2023mpc` actually points to Morcego et al. on greenhouse, not "Caceres" on irrigation), this is a liêm chính bug reviewer will catch by opening the DOI. Fix: either (a) verify each row against paper abstract via Crossref API, or (b) convert to "Cấu hình A/B/C minh họa" with caption declaring illustrative values + pointer to appendix for real data. Option (b) is safer when source papers haven't been read in detail.
- **⚠️ STALE-PDF / MULTI-OUTPUT TRAP — verify số trang & nội dung trên ĐÚNG file PDF bạn vừa build.** Bug thật phiên LVTN: `build.sh` kết thúc bằng `cp "$OUTDIR/main.pdf" ./main.pdf`, sinh ra 2-3 bản `main.pdf` ở các thư mục khác nhau (`build/`, root, `_build/latex/`). Các lần build sau ghi ra một path, nhưng `pdftotext`/đếm trang lại đọc bản CŨ ở path khác → báo \"vẫn 219 trang\" nhiều lần dù đã bỏ ~1081 dòng bảng (thực tế đã 173 trang). Quy tắc: (1) `find . -name 'main.pdf' -printf '%p %t\\n'` để lộ MỌI bản và mtime; xác định canonical bằng mtime mới nhất; (2) build THẲNG vào một `-output-directory` duy nhất và đọc số trang/nội dung trên CHÍNH file đó, đừng tin lệnh build \"up-to-date\" của latexmk khi PDF đích cũ; (3) gỡ dòng `cp ... ./main.pdf` (hoặc bất kỳ bước nhân bản) khỏi script build để chấm dứt nguồn nhầm; (4) sau `latexmk -C`/clean wipe, `.bbl` bị xóa → citation \"undefined\" tới khi chạy lại full chain (xelatex→bibtex→xelatex×2), đừng hoảng vì undefined ngay sau clean — chạy đủ chain rồi mới grep undefined.\n- Với IEEE/LaTeX trước khi gọi submit-ready, kiểm tra và xử lý `Overfull \\\\\\\\hbox`; xem `references/latex-ieee-layout-polish.md` cho quy trình polish.
- **GOTCHA `\paragraph{}` mồ côi trong IEEEtran:** IEEEtran render `\paragraph{Foo}` thành nhãn liệt kê "a) Foo". Nếu chỉ có MỘT `\paragraph` lẻ trong một mục (không có b), c)...) → nhãn "a)" mồ côi, nhìn rất kỳ; người dùng bắt ngay ("có a) mà không có b) thì cũng không được"). Quy tắc: chỉ dùng `\paragraph{}` khi có ≥2 mục thành nhóm (a),b),c)...). Mục lẻ thì thay bằng câu dẫn in nghiêng chạy dòng: `\smallskip\noindent\textit{Foo---mô tả.}\;`. grep `paragraph{` xuyên `sections/*.tex`, đếm số `\paragraph` liền nhau trong mỗi subsection: nhóm thì giữ, lẻ thì đổi. (Cũng dọn lỗi dấu câu thừa kiểu "permanently.:" khi đổi.)
- Figures không clip/overlap/mất glyph tiếng Việt.
- Author metadata, affiliation, funding, conflict statements. Khi người dùng hỏi về funding/acknowledgment/AI-disclosure/Article-Type/biography, các BƯỚC TRONG CỔNG NỘP ScholarOne (7 cam kết tick, câu hỏi Code Ocean, chọn keyword từ taxonomy), footnote dual-affiliation, hoặc "bổ sung toàn diện các mục template gốc", dùng `references/ieee-frontmatter-funding-ack-ai-disclosure.md` (funding ĐẶT ở first footnote `\thanks` KHÔNG ở Acknowledgment; IEEE bắt buộc khai AI-generated content — kể cả computer-code do AI viết — trong Acknowledgment + nêu tool, nhưng language-editing thường miễn, và KHÔNG dán nhãn "data AI-generated" cho số mô phỏng deterministic; bio chỉ cần lúc accepted; Code Ocean chọn Yes nhưng hoãn upload tới accepted; keyword IoT-J là menu taxonomy chọn sẵn; dual-aff = nhiều `\IEEEauthorrefmark` đúng nhưng dòng `\thanks` hay thiếu tên — rà từng ref-mark; link IEEE Author Center cũ hay 404 — verify URL live trước khi gửi; verify text 2-cột trong PDF bằng grep từng MẢNH không grep cả câu). Khi đổi authors/template IEEE/IEEE Access, xem `references/ieee-author-template-handling.md` để giữ đúng equal-contribution/corresponding-author notes và không claim official Access conversion nếu thiếu `ieeeaccess.cls`. Khi chuyển manuscript sang template tạp chí hoặc tư vấn topic/section/submit link, dùng `references/journal-template-conversion.md`: mở link kiểm chứng trước, phân biệt official section với keyword suy luận, ghi rõ page-limit/graphical-abstract requirements, và test package từ zip sạch.
- Khi người dùng đưa link hội nghị (EasyChair) hoặc nói "nộp cho đúng / bám sát thông tin hội nghị", dùng `references/conference-submission-format-compliance.md`. Bài học cốt lõi: metadata nội bộ ("hội nghị C1 conference style") KHÔNG phải spec — verify format thật qua EasyChair CFP công khai (`easychair.org/cfp/<conf>`, conf thường lowercase) và tải template Google-Doc bằng `export?format=docx` rồi `read_file` (web search hay bị chặn, đừng retry); trích checklist (1-cột/font/heading-không-số/abstract<=200/**page limit 6--8**); convert LaTeX khớp spec (title Arial14, `secnumdepth=0` rồi grep `\ref{sec:` vì sẽ thành `??`); ép page-limit bằng float/display spacing + `\footnotesize` bib + shrink figure + gộp proposition + dedup prose + (đòn cuối nếu vẫn dư 1 trang) `\linespread{0.96}\selectfont` ở preamble (vô hình ở Times-12, claw lại ~1 trang) + bib `\scriptsize` 2-cột qua `multicol` (đo `pdftotext` từng trang trước, KHÔNG cắt nội dung khoa học, KHÔNG cắt `\input{table}` mà giữ prose `\ref{tab:X}` — sẽ in `??`); và HỎI người dùng nếu template là `.docx` mandatory vs nhận PDF-từ-LaTeX trước khi chốt. **Khi người dùng đòi kèm bản .docx ("song song cho thêm bản docx luôn", "chuẩn template")**, dùng `references/latex-to-docx-pandoc-conversion.md`: strip `\resizebox` khỏi mọi bảng, render TikZ→PNG standalone (200dpi), parse `.bbl` IEEEtran thành `\begin{enumerate}` thuần (KHÔNG inline `.bbl` thô — pandoc lỗi `expecting \end{document}`), dùng template venue làm `--reference-doc` để thừa hưởng style, verify bằng XML count `<w:tbl>`/`<w:drawing>`/`<m:oMath>` (python-docx có thể fail nếu template embed font — không phải docx hỏng). Khi chuẩn bị bản Sensors/MDPI, dùng `references/sensors-mdpi-manuscript-prep.md` để thêm đúng front/back matter và đổi section mapping sang Materials and Methods/Results/Discussion/Conclusions.
- ZIP/package đúng yêu cầu venue nếu cần. Khi build local pass nhưng Prism/Overleaf-like compiler fail, hoặc khi chuẩn bị zip để upload lên Prism, dùng `references/prism-overleaf-latex-packaging.md`: test từ zip sạch trong `/tmp`, kiểm tra control characters/delimiter errors, và làm package self-contained theo thư mục chứa `main.tex`. **Khi người dùng nói \"tải template về, đưa nội dung qua, không thiếu file nào trong bộ template\"**: reference này có recipe BUNDLE `.cls`/`.bst` chính thức từ CTAN (diff với bản hệ thống trước, copy vào repo, build-from-scratch trong thư mục trắng rồi grep log `(./IEEEtran.cls` để chứng minh dùng file LOCAL) + PRUNE figure mồ côi (grep `includegraphics`/`input{figures` vs `ls figures/`, xóa phần thừa, verify zip bằng `unzip -l`) để bộ nộp tự chứa với MỌI compiler.

Nếu có validator trong project, chạy validator trước khi báo hoàn tất.

#### Final package handoff + naming scrub for bài AoI-greenhouse-style papers

Khi người dùng nói lặp lại/nhấn mạnh "gửi file zip final hiện tại, kèm file pdf" hoặc sửa ngay trước khi gửi (vd "bài bài AoI-greenhouse làm gì còn corr nữa" / "VoU naming coi kỹ lại và thống nhất"), đây là Stage 10 EXECUTE, không phải chỉ trả lời:
- Trước khi zip, grep source chính (loại `_backups/`, `_review_artifacts*`, artifact cũ) cho term bị loại như `corr|correlation|correlated|corrGreen|correlation-credit`; nếu chỉ còn trong BibTeX title/reference thì không tính là narrative chính, nhưng với handoff final nên cân nhắc dọn cả BibTeX entry không còn được cite để audit sạch tuyệt đối.
- Audit acronym/naming ở title, abstract, intro, figure, slide subtitle: chốt MỘT expansion duy nhất (vd `bài AoI-greenhouse = Channel-Aware Value of Update`) rồi grep các biến thể `Value-of-Update`, `Value of Urgency`, `Value-of-Urgency`, subtitle slide, keywords. Không tự đổi thành `Threshold- & Channel-Aware...`; threshold-aware là đặc tính nội dung, không nhất thiết là chữ trong acronym. Nếu người dùng hỏi `U` là Urgency hay Update: chốt theo bản chất toán `Value of Update` (giá trị của việc cập nhật node bây giờ); dùng `urgency` chỉ như mô tả score/priority, không phải expansion chính thức.
- Khi người dùng nói nội dung so sánh baseline nghe như "tấn công" hoặc dư (vd figure AoI/AoII vs VoU), chuyển giọng từ đối đầu sang kế thừa/định vị: AoI/AoII là lineage/reference operating points; bài AoI-greenhouse chuyên biệt hóa cho threshold-critical monitoring. Loại bỏ figure/đoạn conceptual chỉ để chứng minh baseline "blind/not aware" nếu không cần cho method; giữ so sánh định lượng ở Evaluation. Trong bảng/slide, đổi cột/phrase kiểu `Missing vs.`, `blind`, `not competitive`, `worse`, `trail`, `vì sao thua`, `kết quả phủ định` thành `Primary signal`, `reference operating point`, `higher loss under threshold-weighted objective`, `định vị phạm vi áp dụng`, `diễn giải kết quả`. Nếu người dùng nhấn thêm "phần ở giữa" / "chỉ tập trung đúng trọng tâm" / "hạn chế nhiều chữ", rà Methodology + Evaluation + Theory để rút đoạn diễn giải dài, bỏ subsection tail/worst-case hoặc narrative phụ nếu không cần cho đóng góp chính, và sau mỗi bảng chỉ giữ 1 đoạn trung tính về operating trade-off. Xem `references/neutral-manuscript-polish-caw-vou.md`. Mục tiêu: tập trung trình bày method, không hạ thấp prior work.
- Nếu người dùng nhấn mạnh lại “coi kỹ/rà kỹ/chốt lại” sau khi đã gửi file, chạy vòng audit thứ hai nghiêm hơn: source chính + `figures/*.tex` + `references.bib` + slide, sau đó audit CHÍNH ZIP bằng `unzip -l ... | grep -Ei 'corr|correlation|review_artifacts|backups'`. Lỗi thật đã gặp: `rsync --exclude='_review_artifacts*'` không loại thư mục như mong muốn; dùng pattern có dấu `/` rõ ràng (`--exclude='_review_artifacts/' --exclude='_review_artifacts*/' --exclude='*/_backups*/'`) hoặc kiểm bằng `unzip -l` rồi rebuild zip nếu còn artifact cũ.
- Build lại PDF SAU sửa cuối cùng (`latexmk`/full chain tùy project) cho cả manuscript và slide nếu slide có sửa; không gửi PDF stale. Nếu build nhiều project, chạy trong đúng `workdir` của từng project, đừng nối hai `latexmk` khác thư mục trong một lệnh.
- Tạo zip sạch ở `/tmp` hoặc thư mục handoff, exclude `_backups`, `_review_artifacts*`, aux/log/fls/fdb/toc/nav/snm, nhưng include source, figures, `.bib`, PDF chính. Test tên file rõ: `<Project>_final_current.zip`, `<Project>_manuscript_final.pdf`, `<Project>_slides_final.pdf` nếu có deck.
- Final reply cực ngắn bằng tiếng Việt, đính kèm `MEDIA:` zip và PDF(s), kèm 1-2 dòng nói đã scrub naming/term bị loại và build lại. Không giải thích dài.

#### Soạn slide Beamer trình bày từ manuscript (dùng template viện/trường)

Khi người dùng gửi template `.tex` Beamer và nói "soạn slide trình bày nội dung
manuscript, ngắn gọn, ít chữ nhiều hình, có toán + giải thích, sắp đúng thứ tự",
dùng `references/manuscript-to-beamer-slides.md`. Bài học cốt lõi: (1) giải nén +
đọc template TRƯỚC, giữ nguyên theme/màu/headline/recurring-TOC; logo asset hay
THIẾU trong zip → dùng logo-fallback `\IfFileExists` để build không vỡ; (2) thứ tự
slide cho BÁO CÁO manuscript: Bài toán+3 thách thức → Mô hình (toán) → Phương pháp
(pipeline + chỉ số, tách số hạng map 1-1 về 3 thách thức) → Lý thuyết (lemma/theorem
kèm block "Kết luận") → Thực nghiệm (slide SETUP riêng "cố định tham số trước" + kết
quả + SoTA + regime) → Kết luận; (3) PREFERENCE người dùng: ít chữ, mỗi slide toán có
1 dòng "Đọc công thức" diễn giải bằng lời, tô màu số hạng theo challenge; (4) tái
dùng TikZ 2-cột bằng `\resizebox{0.98\textwidth}{!}{\input{...}}` + định nghĩa lại
palette màu trong preamble deck; (5) VERIFY = build chain ≥2 lần + render slide rủi\nro (pipeline) ra PNG rồi vision-check (build sạch KHÔNG đủ; recurring TOC đẩy số\ntrang nên đừng đoán). Đặt deck trong `SAS/Research/<project>_Slides/`. Khi người dùng\nxin \"trình bày THÊM cách chứng minh, nói đơn giản, đưa toán giải thích trực quan\":\nthêm slide proof-sketch riêng (4.1b/4.2b) cấu trúc 3-bước B1/B2/B3 + boxed result +\nblock \"Trực giác hình học\" (ẩn dụ đời thường) — xem §5f của reference, và nhớ đồng\nbộ số stale trong deck từ CSV batch hiện tại trước khi thêm.

**PREFERENCE Việt hóa + hàn lâm hóa slide:** người dùng yêu cầu "hạn chế text nội bộ
(English), câu chữ tự nhiên hơn, hàn lâm hơn". Khi rà slide: grep các từ English
lẫn trong prose (primary, robustness, Method, Policy, ours, error bar, freshness,
novelty, recon, regime, leading-order, negative result, starvation, fade, blacklist,
seed, round-robin, bridge, SoTA) → Việt hóa (bộ chính, kiểm bền vững, Phương pháp,
Chính sách, đề xuất, thanh sai số, độ tươi, độ mới lạ, tái tạo, chế độ, xấp xỉ bậc
thấp, kết quả phủ định, chống bỏ đói, nghẽn, không bị loại vĩnh viễn, hạt giống,
luân phiên đều, sai khác, phương pháp tiên tiến gần đây). NHƯNG **giữ nguyên thuật
ngữ chuẩn không nên dịch**: bài AoI-greenhouse, AR(1), Gilbert–Elliott, per-arm, VoU, AoI,
RMSE, Wilcoxon, $O(1/\sqrt N)$ — dịch ra sẽ kỳ. Đổi tiêu đề block "Đọc bằng lời" /
"Đọc công thức" → "Diễn giải" cho trang trọng, thống nhất. Sau sửa: build chain +
render slide có chữ dài (vd 2.1 có nhiều block) ra PNG, vision-check không tràn đáy/
đè footer; rút câu nếu Overfull vbox > vài pt (1pt bỏ qua được).

## Handoff schema rút gọn

Khi chia sub-agent, mỗi handoff phải có:
- Task boundary: agent chỉ làm phase nào.
- Inputs allowed: file/data nào được đọc.
- Outputs required: tên artifact và schema ngắn.
- Non-goals: không viết sang phase sau, không tự simulate persona khác.
- Evidence requirement: citation/path/line/page/metric.
- Blocker rule: thiếu dữ liệu thì báo blocker, không tự bịa.

## Fan-out sub-agent khuyến nghị

Dùng khi workload nặng và có thể song song:
- Literature scout: tìm và xác minh paper.
- Methodologist: kiểm tra coherence câu hỏi-phương pháp.
- Synthesis critic: phát hiện mâu thuẫn/gap.
- Reviewer personas: EIC, methodology, domain, devil's advocate.
- Reproducibility checker: build, data trace, citation consistency.

Không fan-out khi:
- Task cần quyết định học thuật của người dùng.
- Dữ liệu private chưa được phép gửi sang agent/provider khác.
- Subtask không có output kiểm chứng được.

### Pattern: RLM (Recursive Language Model) — decomposition đệ quy cho audit toàn diện

Khi người dùng nói \"dùng RLM\" / \"rà soát toàn diện, nhiều hướng, nhiều góc nhìn cho khỏi sót\" / \"quét cả N chương + reference + phụ lục\", đây KHÔNG phải skill đã cài sẵn — RLM là **methodology**: chẻ bài toán audit lớn thành các nhánh độc lập theo trục (file/loại lỗi/lăng kính), quét song song bằng `delegate_task`, rồi gộp lên. Người dùng dùng \"RLM\" như từ khóa kích hoạt pattern này — đừng đi tìm skill `rlm`, hãy áp dụng ngay.

Recipe phiên LVTN 4 chương + refs + phụ lục:
1. **Định vị state THẬT trước khi phân nhánh:** đọc `main.tex` để biết structure, `wc -l` từng chapter, đếm bib entries, list CSV evidence. Không phân nhánh khi chưa biết phạm vi thật.
2. **Phân rã theo TRỤC FILE (không theo loại lỗi):** mỗi subagent ôm một cụm file gần nhau về ngữ cảnh (vd Nhánh A = mở đầu+Ch1+Ch2 mạch lập luận; Nhánh B = Ch3+Ch4+kết luận; Nhánh C = phụ lục + đối chiếu CSV evidence; Nhánh D = refs/bib parent tự làm vì cần script chính xác). Mỗi nhánh chỉ-đọc, trả về findings có evidence `file:dòng` + mức độ.
3. **Một số nhánh PARENT TỰ LÀM, không delegate:** việc cần script chính xác (đối chiếu `\cite` xuyên file vs `.bib`, normalize tiêu đề so CSV) parent làm bằng `execute_code` vì subagent dễ báo sai count (vd phiên này `read_file` qua wrapper trả KeyError với file lớn → subagent đếm thiếu 30/87 cite). Quy tắc: nếu cần `re.findall` xuyên nhiều file lớn → parent tự, không delegate.
4. **VERIFY chéo trước khi báo:** xem §Pitfall \"subagent review-finding có TỶ LỆ BÁO NHẦM CAO\". Phiên này 4/8 finding CAO của subagent là báo oan; ghi rõ trong báo cáo cuối những finding nào đã bị hạ cấp và vì sao.
5. **Báo cáo cuối có 3 vùng:** (a) CAO đã verify thật, (b) BÁO NHẦM đã hạ cấp (người dùng trọng minh bạch — nếu im lặng người dùng sẽ tưởng có lỗi mà không thấy fix), (c) còn lại cần người dùng quyết hướng (xoá/cô đọng/sửa).

Khi người dùng confirm \"sửa hết\" sau khi đọc báo cáo RLM: chuyển sang Stage 8 (revision) — SỬA TUẦN TỰ, build chain sau MỖI cụm, không gom 10 patch rồi build một lần (sai một chỗ khó cô lập).

### Pattern: multi-lens review song song READ-ONLY → parent verify → fix serially

Khi người dùng nói \"review qua nhiều lượt ở nhiều góc nhìn khác nhau rồi sửa cho
ready-submit\", đây là pattern đã chạy thật end-to-end cho cả bài AoI-greenhouse lẫn bài bandwidth-scheduling trong
một phiên:
1. **Phóng 3 subagent review SONG SONG, mỗi agent một LĂNG KÍNH, toolsets `[terminal, file]`, nhiệm vụ READ-ONLY (cấm sửa file):**
   - Lăng kính A — **số liệu & nhất quán:** đối chiếu MỌI con số trong .tex với CSV/output gốc; bắt số stale, mâu thuẫn liên-section.
   - Lăng kính B — **tham chiếu chéo & cấu trúc:** build + đọc log/.aux tìm undef ref/cite, label mồ côi, figure/table không ref, multiply-defined, bib entry trùng/thừa, overfull>60pt.
   - Lăng kính C — **notation + ngôn ngữ + overclaim:** ký hiệu kép/không đồng bộ, acronym first-use, câu khẳng định quá mạnh (\"optimal/guarantee/self-tuning\" khi thực ra heuristic), grammar/typo, lặp ý.
   Mỗi agent trả về BẢNG `loại | file:dòng | hiện tại | đúng | đề xuất`, ưu tiên vấn đề thật, trả lời tiếng Việt.
2. **Vì sao READ-ONLY:** người dùng hay chạy nhiều agent song song trên cùng repo →
   nếu để subagent ghi sẽ lost-update/ghi đè chéo. Tách hẳn: subagent CHỈ đọc & báo
   cáo, PARENT là nơi duy nhất ghi file.
3. **Parent VERIFY trước khi sửa — không tin subagent mù quáng.** Subagent có thể
   báo nhầm (vd báo 2 CSV khác nhau, hoặc OCR vision đọc nhầm 2 dòng số gần nhau).
   Với mỗi finding số liệu, parent tự reproduce con số đúng từ CSV gốc bằng
   execute_code TRƯỚC khi patch. Bug nặng nhất phiên này lộ ra đúng nhờ verify:
   3 bảng bài AoI-greenhouse in nhầm biến thể (xem dưới).
   **Locked-section precedence:** nếu người dùng đã KHÓA một phần (vd \"phần Mở đầu = 100%% đề cương gốc, không sửa\"), thì finding của lăng kính ngôn ngữ/tông giọng nằm TRONG phần đó phải BỎ QUA — ràng buộc khóa của người dùng ưu tiên hơn quy tắc tông trung lập. Verify bằng cách grep cụm bị flag (\"ưu việt\", \"ưu thế vượt trội\"...) trong file đề cương gốc (PDF→pdftotext, normalize whitespace vì PDF hay ngắt dòng giữa cụm gây false-negative); nếu cụm có nguyên văn trong baseline khóa → giữ nguyên, báo người dùng rõ là CỐ Ý không sửa và vì sao.
4. **Sửa TUẦN TỰ, đọc lại file trước mỗi patch** (cảnh báo sibling-modified là
   marker review-agent đã xong, vô hại — nhưng vẫn đọc lại để chắc). Build chain
   đầy đủ sau mỗi cụm sửa, không gộp 10 patch rồi mới build.
5. Cuối: full build chain + grep undef=0 + overfull>60pt=0 + đếm trang, rồi báo
   người dùng evidence thật + những điểm cần người dùng quyết (bib thừa giữ/dọn, nhãn cột...).

### Pitfall: subagent review-finding có TỶ LỆ BÁO NHẦM CAO ở mức \"CAO/critical\"

Bằng chứng định lượng phiên LVTN review toàn diện 4 chương: 8 finding mức CAO từ
3 subagent đọc song song, sau khi parent verify chỉ còn 4 là thật. 4/8 = 50% false
positive ở mức nghiêm trọng nhất. Các kiểu báo nhầm điển hình cần soi kỹ:
- **\"Tên tác giả không khớp bibkey\" → bibkey chỉ là string đặt tên xấu.** Phải mở
  `.bib` đọc trường `author = {...}` thật. Vd `nawaz2024aiot` thực ra có author
  `Sangeetha et al.` (khớp text), key đặt tên cẩu thả nhưng KHÔNG phải lỗi liêm
  chính. Verify nhanh: `grep -A 4 \"@.*{<key>,\" references.bib`.
- **\"Công thức/đại lượng X không tồn tại trong chương Y\" → thường nằm ở chương Z khác.**
  Subagent quét hạn theo phạm vi file được giao, không thấy ở chương yêu cầu sẽ
  kết luận \"không có\" — trong khi định nghĩa ở chương khác. Vd phiên này: subagent
  Ch3+Ch4 báo \"$\\Delta_{IAE}$/PRR/12 biến PNCE không có hậu thuẫn\" nhưng cả ba định
  nghĩa rõ ở Ch2 (eq:iae_improvement dòng 536, eq:prr_formula dòng 551, bảng
  pnce_extraction dòng 445). Verify: grep label/symbol XUYÊN toàn bộ chương, không
  chỉ trong phạm vi subagent được giao.
- **\"Số trên hình mâu thuẫn caption\" → đôi khi caption đúng, hình mới sai (sinh từ
  script bịa số);** ngược lại nhiều khi hình raster bị OCR/vision đọc nhầm chữ
  thường thành chữ in (vd dấu hỏi/dấu sắc lệch). Verify cả hai chiều: render trang
  ra PNG xem mắt thường + đọc script sinh hình.

Quy tắc cứng: TRƯỚC khi báo cáo finding \"CAO\" cho người dùng hay patch file, parent
phải tự verify từng cáo buộc bằng MỘT thao tác cụ thể (`grep`/`read_file`/đọc thẳng
`.bib`). Nếu verify trái với báo cáo subagent → HẠ CẤP hoặc BỎ finding, ghi rõ
trong báo cáo cuối cùng để người dùng biết subagent đã báo oan ở chỗ nào (người dùng
trọng minh bạch — \"sửa lại báo cáo trước, finding nào nhầm thì nói rõ\").

### Pitfall: \"chốt số X, xoá cái sai\" — phải INVESTIGATE delta là dedup hay drop

Khi người dùng nói \"chốt N (số nhỏ), xoá những thứ không khớp\" cho dataset/PRISMA/bib
audit: delta có hai nghĩa rất khác nhau, chọn sai phá liêm chính khoa học:

- **Cách A — Drop entities (irreversible scientific decision):** giảm corpus M→N
  bằng cách bỏ M−N công trình thật. Đây là quyết định khoa học của người dùng, AI
  KHÔNG được tự ý chọn bỏ paper nào.
- **Cách B — Dedup duplicate rows (mechanical cleanup):** số manuscript ghi N là
  đúng, CSV bị nhân đôi (M−N) dòng do quá trình audit. Xoá dòng trùng → khớp, không
  mất nội dung khoa học. An toàn AI làm được.

Đừng đoán — verify bằng cách: (1) đọc cấu trúc \"đầu mục lõi\" từ phụ lục
manuscript (vd `\\begin{enumerate}...C1...CN`), normalize tiêu đề (lowercase, strip
punctuation/dấu \"&\" vs \"and\"), so với CSV rows; (2) đếm CSV-row-per-core-entry —
nếu mỗi core có ≥1 CSV match và TỔNG = M, có core khớp nhiều CSV → đó là CASE B
(dedup). Nếu có CSV row không match core nào → CASE A (drop entity). Phiên LVTN
delta 68→64: title-normalize cho ra **4 core khớp 2 CSV mỗi cái** (cùng DOI/year),
0 CSV mồ côi → CASE B, an toàn xoá 4 dòng trùng. Verify cuối: 4 cặp phải
byte-identical (cùng DOI + title + year) trước khi delete.

Khi áp dụng dedup: ưu tiên giữ row có nhiều metadata hơn (cite key, replacement
trail) thay vì id thấp hơn. ID gaps trong file provenance/audit là OK và TRUNG
THỰC (\"duplicates removed\"); đừng đánh số lại trừ khi manuscript tham chiếu S-id
(grep `S\\d{2}` xuyên `.tex` để biết).

### Pitfall: bảng in nhầm BIẾN THỂ của method (self-consistent nhưng sai headline)

Lỗi liêm chính nguy hiểm, khó thấy: nhiều bảng (results/ablation/whittle) in cùng
một con số cho method-chính, nhưng đó là số của một BIẾN THỂ khác chứ không phải
deployed variant. Phiên bài AoI-greenhouse: 3 bảng in `+debt -corr` (tắt channel-correlation)
= 0.0027/0.041 thay vì `Full (corr+debt)` = 0.0024/0.0367. Các dòng baseline khác
lại đúng batch → bảng \"trông\" nhất quán nội bộ. Manh mối: số method-chính KHÔNG
khớp CSV nào ở batch chuẩn; abstract (78%/96%) chỉ khớp khi dùng Full variant. Cách
bắt: recompute từng dòng từ CSV gốc, đọc thẳng script sinh bảng xem nó khởi tạo
method bằng cờ nào (`use_correlation_credit`), đừng tin nhãn cột. Sửa về Full rồi
sync bội số (34×→39×, v.v.) ở mọi nơi.

### Pitfall: nhầm ε với độ-lệch-chuẩn-dự-báo s (biến thể thứ 3 của ε-confusion)

Ngoài \"ε vs suppression-factor\" đã ghi ở §Stage 6, phiên này gặp biến thể thứ ba:
ε (= s/(u−μ), innovation-to-distance ratio, ≈0.3 cho sensor sát ngưỡng) bị gọi nhầm
thành s (predictive std 4-bước ≈0.16) ở methodology/eval/discussion, trong khi
theory viết đúng 0.3. Quy tắc: grep mọi lần xuất hiện ký hiệu/giá trị ε xuyên
section, xác định MỘT định nghĩa chuẩn (thường ở §theory), rồi sync tất cả về đó;
verify giá trị bằng execute_code (ε = s/(u−μ)), đừng để mỗi section một con số.

## Cross-paper carry-forward

Nếu dùng paper trước của người dùng:
- Re-feed Material Passport/reference list như input khai báo, không tin tự động.
- Đưa limitations/reviewer comments cũ vào Socratic input.
- Re-verify citation dưới policy hiện tại.
- Không dựa vào memory mơ hồ để sinh gap mới.

## Workspace hygiene và file-version discipline

Áp dụng cho mọi artifact nghiên cứu/paper/report/figure trong workspace của người dùng:
- Mặc định đặt project nghiên cứu trong `SAS/Research/<project-name>/`; không để project nằm trực tiếp dưới `SAS/` nếu đã xác định nhóm công việc.
- Nếu nhóm khác phù hợp hơn, tạo thư mục nhóm rõ nghĩa dưới `SAS/` trước, ví dụ `SAS/Teaching/`, `SAS/Business/`, `SAS/Software/`; hỏi người dùng nếu phân loại mơ hồ.
- Giữ thư mục làm việc gọn; không tạo nhiều file `v1`, `v2`, `final`, `final2`, `new`, `copy` nếu không có lý do kiểm chứng rõ.
- Ưu tiên sửa trực tiếp vào file chính; dùng diff/log/manifest để theo dõi thay đổi thay vì nhân bản artifact.
- Nếu cần backup trước khi sửa file quan trọng, tạo backup có kiểm soát trong `_backups/<timestamp>/`, không để bản sao rải trong thư mục làm việc.
- Với tái cấu trúc thư mục: chỉ di chuyển, không xóa dữ liệu; tạo manifest đường đi cũ -> mới; bảo vệ các thư mục/project được người dùng nêu rõ.
- Khi cần nhiều biến thể học thuật thật sự, đặt trong thư mục con có mục đích rõ như `drafts/`, `experiments/`, `figures/variants/`, hoặc `_review_artifacts/`, kèm README/manifest ngắn.

## Highlighted revision PDF workflow

Khi người dùng yêu cầu PDF có highlight các chỉnh sửa:
- Lấy bản baseline từ nguồn gốc kiểm chứng được: zip ban đầu, clean checkout, hoặc `_backups/<timestamp>/`.
- Dùng thư mục phụ có mục đích rõ, ví dụ `_review_artifacts/original_zip/` và `_review_artifacts/highlight_diff/`; không rải file diff ở root ngoài bản PDF cần gửi.
- Với LaTeX nhiều `\input`, dùng `latexpand main.tex` cho cả baseline và revised trước khi chạy `latexdiff`, để section-level edits được bắt đầy đủ.
- `soul`/`\hl` dễ lỗi với math và align; ưu tiên `latexdiff --type=CFONT --math-markup=off`, rồi override `\DIFadd` bằng `\colorbox{revYellow}{...}` nếu cần nền vàng. Nếu compile lỗi vì markup trong math, tắt math markup hoặc không highlight bên trong equations.
- Compile diff PDF trong thư mục `_review_artifacts/highlight_diff/`, copy bản gửi ra root project với tên rõ như `<Project>_highlighted_changes.pdf`, rồi báo đường dẫn/`MEDIA:` cho người dùng.
- Luôn compile lại bản clean `main.pdf` riêng nếu đã di chuyển workspace hoặc sửa sau lần build trước.

## Output mặc định cho người dùng

- Mở đầu trả lời thẳng quyết định/kết quả trong 1-3 câu.
- Phần sau mới nêu evidence, quy trình, caveat.
- Với review: findings trước, theo severity, kèm file/page/line nếu có.
- Với execute: báo đã đổi gì, verify gì, blocker gì.
- Với uncertainty: nói rõ confidence và dữ liệu còn thiếu.
- **Định dạng nhẹ trên kênh chat (Telegram):** người dùng khó chịu khi câu trả lời \"bị md các thứ\" — tức bảng Markdown nhiều cột, nhiều ký hiệu `|`/`#`/`**` dồn dập render rối trên điện thoại. Mặc định dùng prose ngắn + danh sách gạch đầu dòng đơn giản; CHỈ dùng bảng khi người dùng xin so sánh dạng bảng hoặc dữ liệu thật sự dạng ma trận. Khi bị nhắc về định dạng, lặp lại gọn bằng câu thường, không dựng bảng.
- **Báo cáo tiến trình giữa chừng cho tác vụ dài:** khi một phiên EXECUTE kéo dài nhiều bước (rà soát, sửa hàng loạt, phục hồi), người dùng cần biết \"ở giữa đã làm gì\" — không chỉ kết quả cuối. Sau mỗi cụm thao tác (hoặc khi người dùng hỏi \"xong chưa/đã làm gì rồi\"), tóm tắt NGẮN theo dạng: đã đụng FILE nào, sửa ĐIỂM gì, còn lại gì. Liệt kê file-đã-sửa vs file-chỉ-đọc rõ ràng. Đừng để người dùng phải hỏi lại mới biết phạm vi thay đổi.
