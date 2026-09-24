# Reviewer-driven revision loop (critique → new experiments → manuscript)

Khi người dùng đưa một bản review (Claude-CLI feedback hoặc reviewer thật) và bảo "giải quyết toàn bộ", đây là quy trình đã chạy thành công cho bài bandwidth-scheduling_STAIS.

## 0. Định vị code + data TRƯỚC khi sửa chữ
- Manuscript dir (`*_submission_ready`) thường CHỈ có `.tex` + `outputs/` đã render — KHÔNG có code sinh số. Code thật hay nằm trên GitHub (`gh api repos/<user>/<repo>/git/trees/HEAD?recursive=1`). Clone về workspace riêng (`rabs_repro_<ts>/`), KHÔNG sửa trong manuscript dir.
- Đọc script thực nghiệm chính để biết: N/tham số hardcode ở đâu, dataset đến từ đâu, bảng manuscript map sang script nào (tên file thường KHÁC nhau — manuscript có bảng format thủ công tiếng Anh, script sinh bảng tiếng Việt đầy đủ policy → cần 1 generator riêng sinh đúng format manuscript từ CSV).
- Backup manuscript vào `_backups/<ts>/` trước khi đụng.

## 1. Biến từng điểm review thành thí nghiệm, không viết chay
- "N quá nhỏ" → viết script scaling parameterize N, chạy N∈{3,8,12,20} THẬT. (bài bandwidth-scheduling: lợi thế PD tăng theo N → biến điểm yếu thành điểm mạnh.)
- "thiếu ablation" → tắt từng term, chạy thật.
- "objective chưa định nghĩa" → thêm equation KHỚP đúng công thức trong code (đọc `eval_step`/objective trong script, không bịa).

## 2. Nâng heuristic thành đại lượng có nền lý thuyết (đúng gu Q1 của người dùng)
- Nếu reviewer chê "thin heuristic": thay term bằng dạng derivable. Ví dụ bài bandwidth-scheduling: urgency `w·p_vio` (raw prob) → **VoU `g(p)=4p(1-p)`** = decision-uncertainty, leading-order value-of-information cho quyết định nhị phân, cực đại ở biên p=0.5, =0 khi đã chắc chắn. Raw prob vừa lãng phí poll khi outcome đã chắc, vừa double-count ngưỡng detector.
- DERIVE trước (giải thích vì sao dạng mới đúng) → rồi mới chạy verify. Sửa ĐÚNG 1 chỗ trong code (nhánh urgency của policy đề xuất), giữ nguyên baseline.

## 3. Khi enhancement THẤT BẠI — kỷ luật kết quả âm (CỐT LÕI)
- Nếu một cơ chế được thử ≥3–6 lần trên ≥1 dataset thật mà không thắng metric của chính nó → **ĐÓ LÀ KẾT QUẢ, không phải bug để vá mãi**. bài bandwidth-scheduling-CVaR: 6 lần thất bại (greenhouse đuôi-nhẹ + ERA5 VN đuôi-nặng) → CVaR thua PD có ý nghĩa trên chính CVaR-loss.
- KHÔNG gắn nhãn "Proposed" cho phương pháp thua sạch metric của nó. Reviewer chạy lại code (mục Code Availability) sẽ thấy → sập uy tín cả các đóng góp thật.
- Báo người dùng thẳng với BẢNG số + p-value, nêu 2–3 hướng (giữ làm knob / negative-result có kiểm soát / bỏ về Future Work). Người dùng thường chọn: **nếu thất bại thì BỎ, tập trung proposed mạnh nhất.** Đừng cố nhồi.
- Occam là thông điệp mạnh: "VoU + primal-dual đã hút hết lợi ích khả thi; thêm tail-machinery chỉ tăng chi phí" = phát hiện sạch, không phải thất bại.

## 4. SIGN-CHECK thống kê paired (đã sai 1 lần, phải cẩn thận)
- `delta = mean(A) - mean(B)`. Với metric "thấp=tốt": delta ÂM nghĩa là A tốt hơn B. p-value chỉ nói CÓ Ý NGHĨA, KHÔNG nói CHIỀU. Luôn in kèm `-> X better` và đối chiếu mắt trước khi viết "cải thiện". Đừng đọc |delta| lớn + p nhỏ = "thắng".
- scipy Wilcoxon cần venv (uv: `uv venv && uv pip install numpy scipy`); PEP668 nên không cài global được.

## 5. Đồng bộ + markup
- Text MỚI thêm vào manuscript = bọc `\hlnew{...}` (macro nền vàng, khai báo trong main.tex với `\usepackage{soul}`), để người dùng review; strip bằng `\renewcommand{\hlnew}[1]{#1}` trước nộp.
- Đổi phương pháp (VoU) → regen TẤT CẢ số phụ thuộc (Wilcoxon, sensitivity, nonstationary, tradeoff). Script phụ import module chính thì tự thừa hưởng; script tự-định-nghĩa urgency phải sửa theo. XOÁ outputs cũ trước khi chạy lại kẻo lẫn số (người dùng nhắc: "xoá số cũ kẻo nhầm").
- Data "mất" có thể chỉ là chưa push: đọc `fetch_*.py` — nếu là API công khai (vd Open-Meteo ERA5 archive) thì fetch lại được, đó là data thật tái lập.
- Push code+data GitHub = hành động ngoài → CHỜ người dùng duyệt.
