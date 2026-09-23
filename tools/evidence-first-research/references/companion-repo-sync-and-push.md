# Companion-repo sync + clean push to GitHub

Tiếp nối §Stage 9 "Companion-repo submission-readiness gate". Gate đó AUDIT một repo
ĐÃ push. Reference này là bước tiếp: khi người dùng nói **"đồng bộ code hết chưa đã?
Dữ liệu chuẩn chưa? Up repo sạch lên github rồi chạy lại xem"** — tức EXECUTE sync
working code → GitHub, chứng minh tái lập, push sạch.

## Bối cảnh thư mục (quan trọng — dễ nhầm)

- Thư mục manuscript (`bài probe-transmit_IoTJ_clean/`, `bài bandwidth-scheduling_STAIS_clean/manuscript/`)
  thường **KHÔNG phải git repo** — chỉ chứa `.tex`.
- Code working THẬT sinh ra số trong bài nằm ở `SAS/Research/_repos/<repo>/`, và
  thư mục NÀY **chính là** git repo nối GitHub (`git remote -v` → origin GitHub).
- Bản `gh repo clone` (vd `~/gh_check/PT`) chỉ là ảnh chụp của remote để audit, KHÔNG
  phải nơi code mới nằm.

Quy trình bắt đầu: `cd _repos/<repo>`, `git status -s`, `git log -1 --format="%ci %s"`.
Triệu chứng điển hình: **remote push cũ (vd 17/06) nhưng `git status` đầy file
modified + CSV sửa chiều nay (21/06) chưa commit** → số trong bài mới hơn số trên
GitHub. Đây chính là cái "chưa đồng bộ".

## Bước 1 — Re-run để chứng minh tái lập (TRƯỚC khi push)

Đúng thứ tự khoa học: verify trước, push số đã verify.

1. Backup CSV hiện tại: `cp docs/<gen>.csv /tmp/<gen>_before_rerun.csv`.
2. Kiểm venv + deps: `.venv/bin/python -c "import numpy,scipy,pandas,matplotlib"`.
3. Chạy lại script sinh số chính (timeout rộng): `.venv/bin/python scripts/<gen>.py`.
4. **Diff CSV BỎ QUA cột runtime/wall-clock.** Đây là chìa khóa: sim seeded là
   deterministic ở các cột KHOA HỌC (loss/rmse/missed_vio) nhưng runtime wall-clock
   LUÔN đổi theo máy. `diff -q` thô sẽ báo "KHÁC NHAU" gây hoảng. Đúng cách: parse
   CSV, so cell-by-cell chỉ các cột khoa học theo khóa `(window_id, policy)`:

   ```python
   def keycols(f):
       import csv
       return {(r['window_id'],r['policy']):(r['loss'],r['rmse'],r['missed_vio'])
               for r in csv.DictReader(open(f))}
   ko, kn = keycols(before), keycols(after)
   diffs = [k for k in ko if ko[k] != kn[k]]   # kỳ vọng: 0
   ```
   Kết quả mong đợi: **0/N ô lệch** → số trong bài reproducible từ code. (Phiên thật:
   0/420 ô lệch, chỉ runtime đổi.) Đồng thời recompute mean per-policy và đối chiếu
   headline bài (bài AoI-greenhouse loss 0.0028 / missed 0.044% / rmse 0.126 — khớp tuyệt đối).

Nếu cột khoa học LỆCH sau re-run → KHÔNG deterministic (seed/version drift), phải
điều tra trước khi push, đừng push số không ổn định.

## Bước 1b — Verify TOÀN BỘ bảng, không chỉ headline (khi người dùng hỏi "kết quả có vấn đề gì nữa không?")

Re-run script chính + diff CSV (Bước 1) chỉ chứng minh MỘT bảng (vd SOTA). Khi người dùng
người dùng hỏi rộng "kết quả có vấn đề gì nữa không / code+repo sạch chưa", phải đối chiếu
**MỌI** bảng/hình trong bài ↔ CSV+code, không sót. Liệt kê hết bảng (Performance,
Whittle, SOTA, debt ablation, danger-term ablation, sensitivity ×3, scalability,
cross-dataset robustness) rồi recompute mean từng cái bằng execute_code, đối chiếu
số bài. Pitfall lộ ra đúng nhờ làm đủ:
- **Bảng KHÔNG có CSV nguồn trong `docs/`:** danger-term ablation có số trong bài
  (0.00414, 0.01578...) nhưng KHÔNG file CSV nào chứa — vì nó chỉ sinh từ
  `spike_*.py` (xem Bước 2). Nếu chỉ verify các bảng có sẵn CSV, sẽ bỏ sót bảng này
  và vô tình gitignore mất script sinh nó. Quy tắc: bảng nào không truy được về CSV
  → grep keyword/số khắp repo (`--include=*.py`) tìm script sinh, CHẠY nó để xác minh.
- **Cột phân loại không phải tên hiển nhiên:** debt ablation phân loại bằng cột
  `debt_mode` (bounded/accumulating), không phải `policy`; "no-debt" trong bài =
  `VoU` baseline. Đọc header CSV thật trước khi group, đừng đoán tên cột.
- **`robustness_summary.json` có path nội bộ trong field `csv`** nhưng file này nằm
  trong `docs/` đã gỡ khỏi repo nên không lộ — vẫn nên biết để không vô tình ship.
Kết quả phiên thật: 8/8 bảng khớp tuyệt đối sau khi chạy đủ generator (kể cả
danger-term sau khi chạy đúng 30-win). "Không còn vấn đề về số" chỉ được kết luận
SAU khi đã trace hết, không phải sau khi verify mỗi bảng đầu.

## Bước 2 — Phân loại clean-vs-junk TRƯỚC `git add`

`git status -s` sau re-run thường có cả file CẦN lẫn RÁC. Phân loại:

**RÁC — KHÔNG push (thêm vào `.gitignore`, không chỉ skip):**
- `_backups/`, `docs/_backup_<ts>/` — backup nội bộ.
- `*_OLD_*.csv` — bản cũ giữ lại khi re-run.
- `scripts/spike_*.py` — throwaway experiments (phiên thật có ~12 cái). Spike là để
  bắt bug/đóng hướng, phần lớn KHÔNG thuộc bộ code công bố. **NHƯNG ĐỪNG gitignore
  cả nhóm `spike_*` một cách mù quáng — TRƯỚC khi chặn, kiểm xem mỗi spike có sinh
  ra MỘT bảng/hình ĐANG NẰM TRONG BÀI không.** Bug thật phiên bài AoI-greenhouse: định xếp 12
  spike vào rác, nhưng `spike_evcost_vou.py` + `spike_severity_vou.py` chính là thứ
  duy nhất sinh **bảng danger-term ablation** (Classic/ev-cost/severity) trong
  manuscript. Gitignore chúng = người đọc KHÔNG tái lập được một bảng đã công bố =
  vỡ reproducibility. Cách bắt: với mỗi bảng/hình trong bài chưa rõ nguồn, grep số
  hoặc keyword đặc trưng (`grep -rln "0.00414\|ev-cost\|severity\|Phibar" --include=*.py`)
  để truy script sinh ra nó; nếu script đó là `spike_*`, nó KHÔNG còn là throwaway —
  ĐỔI TÊN bỏ tiền tố `spike_` (vd `ablation_danger_term.py`) để không bị `.gitignore`
  chặn, và sửa default param cho khớp bài (xem dưới), rồi mới push. Chỉ những spike
  thực sự không sinh artifact nào trong bài (vd `spike_autoencoder_aoi`,
  `spike_learned_predictor`) mới là rác thật.
- **Spike-default ≠ paper-scale (pitfall đi kèm):** spike thường để default
  `n_windows` nhỏ (vd 8) và/hoặc seed base khác (80260 vs 50260 của các bảng chuẩn)
  để chạy nhanh khi thử. Caption bài lại ghi \"30 matched windows\". Chạy spike ở
  default 8-win cho số LỆCH bài (Classic 0.00506 vs bài 0.00414); chạy đúng 30-win
  thì KHỚP TUYỆT ĐỐI (0.00414/0.0651% = bài 0.00414/0.065%). Khi promote spike thành
  reproducibility script: set default `n_windows`/seed khớp bài, và verify số sinh ra
  trùng bảng TRƯỚC khi push.
- `data/processed/`, `outputs/` — sinh lại được từ raw + script.
- `__pycache__/`, `.venv/`, `*.log`, `.env` — chuẩn.

**CẦN — push:**
- File policy/baseline mới mà bài có dùng (vd `policies/dt_aoi_baseline.py`,
  `policies/sota_recent_baselines.py`).
- Script sinh số/theory mới (`scripts/dt_aoi_comparison.py`,
  `compute_effective_rank.py`, `theory_mdp_lp.py`, `theory_meanfield.py`,
  `verify_vou_lemma.py`).
- `.tex` src/policies đã sửa.
- Data NGUỒN nhỏ cần để script chạy end-to-end (processed sensor panels `.npy`,
  calibration `.csv` trong `data/source/` hoặc `data/raw/`).

### ⭐ PREFERENCE người dùng: repo = CODE + DATA NGUỒN, KHÔNG ship kết quả

**Đây là correction mạnh, override mặc định.** Phiên thật người dùng nói: *"draft và
kết quả các thứ cũng cất đi, chỉ để code cho người đọc vào tái lập, chạy lại kết
quả để kiểm chứng và đọc code để kiểm chứng thôi."* Tức repo công khai chỉ mang
**code + dữ liệu nguồn**; người đọc CHẠY LẠI để sinh kết quả rồi tự đối chiếu với
bài. Hệ quả — các thứ sau phải CẤT (gitignore + `git rm --cached`, giữ trên đĩa):
- **Kết quả tính sẵn:** mọi CSV/JSON kết quả (`docs/*.csv`, `reports/*.json`),
  hình PNG/PDF sinh từ script (`figures/`, `outputs/`). KHÔNG commit dù chúng khớp
  bài — người đọc regenerate. (Mặc định cũ của reference này — "push 11 CSV" — đã
  bị người dùng override; chỉ push CSV/JSON nếu người dùng nói rõ muốn giữ.)
- **Draft/note nội bộ:** `docs/negative_result_*.md`, `docs/*_derivation.md`,
  `docs/theory_*_draft.md`, `*_AUDIT.md` — cất hết, không phải bộ công bố.
- **File manuscript `.tex` lọt vào repo CODE:** repo code không nên chứa manuscript.
  Phiên thật bài bandwidth-scheduling repo tracking `bài bandwidth-scheduling_HueJournal_main.tex` → `git rm --cached` +
  thêm `*.tex` vào `.gitignore`.

Cách thực hiện: viết `.gitignore` phủ `docs/ reports/ figures/ outputs/
data/processed/ *.tex *_draft*.md negative_result_*.md *_derivation.md *_plan.md
<AUDIT>.md` (vẫn whitelist `!data/raw/.../*.npy` cho data nguồn nhỏ), rồi
`git rm -r --cached docs/ reports/ figures/` để gỡ các file kết quả ĐANG tracked
khỏi GitHub (vẫn còn local). Verify `git ls-files` cuối chỉ còn code + data nguồn.

## Bước 2b — Path/secret scrub trên CHÍNH code sắp push

Trước khi commit, quét code (không chỉ repo đã push) cho 2 thứ:

1. **Hardcoded absolute path nội bộ** — lỗi thật phiên này: `make_tradeoff_plot.py`
   có `MAN_FIG = Path("/home/<user>/SAS/Research/bài bandwidth-scheduling_STAIS_clean/...")`. Push lên
   public là lộ cây thư mục máy người dùng + script chạy hỏng trên máy người khác.
   `grep -rniE "/home/|/Users/|openclaw|/opt/hermes|NINEROUTER" <code dirs>`.
   Fix: đổi sang đường dẫn repo-relative + cho override qua env var:
   ```python
   ROOT = Path(__file__).resolve().parents[1]
   import os
   OUT = Path(os.environ.get("<PROJ>_FIG_DIR", ROOT / "figures"))
   OUT.mkdir(parents=True, exist_ok=True)
   ```
   Sau sửa: `git show :<file>` (staged blob) grep lại path = 0 để chắc bản staged sạch.
2. **Secret** — như §Stage 9, đọc từng match để loại false-positive
   (`font-weight`, `risk-weights`, chữ "secrets" trong md).

## Bước 3 — README reproduce (khớp policy code-only)

Kiểm `README.md`: nếu chỉ có 1 dòng tiêu đề (vd bài bandwidth-scheduling) = sơ sài. Viết lại để khớp
policy "code + data nguồn, kết quả tự sinh": (a) layout chỉ liệt kê `code|src/`,
`data/source|raw/`; (b) nói rõ "results/figures NOT shipped — regenerate by running
the scripts, then check against the manuscript"; (c) requirements (vd bài bandwidth-scheduling core là
stdlib-only, chỉ plotting cần pandas/matplotlib); (d) các BƯỚC chạy đánh số đúng thứ
tự + script nào đọc/ghi gì. Verify mọi script tên trong README tồn tại thật
(`for s in ...; do [ -f code/$s.py ]`). Nếu README cũ trỏ tới `docs/`/`figures/` vừa
gỡ → sửa luôn để không link gãy.

## Bước 3 — README reproduce

Kiểm `README.md`: nếu chỉ có 1 dòng tiêu đề (vd bài bandwidth-scheduling) = sơ sài. Bổ sung "How to
reproduce": lệnh chạy, thứ tự script, output mong đợi. Reviewer tải repo về cần biết
chạy gì ra bảng nào.

## Bước 4 — Push (GATED on người dùng approval)

Push lên `main` public là thao tác **khó thu hồi history** → KHÔNG tự push. Trình người dùng:
classification (cần/rác/cân nhắc) + 2 câu hỏi chốt: (a) docs negative-results/draft
push công khai hay giữ nội bộ? (b) OK push thẳng `main` chứ? Sau khi duyệt:
1. Thêm rác vào `.gitignore` (`spike_*`, `_backups/`, `*_OLD_*`, `data/processed/`, `outputs/`).
2. `git add` đúng nhóm cần (add tường minh, KHÔNG `git add -A` để khỏi kéo rác).
3. Commit mô tả rõ ("sync 30-window results + recent SOTA/DT baselines + theory").
4. `git push origin main`.

### Pitfall: `git push` HTTPS fail "could not read Username" dù `gh auth` OK

Remote thường để URL HTTPS (`https://github.com/owner/repo`) nhưng máy không có git
credential helper → `git push` chết với `fatal: could not read Username for
'https://github.com': No such device or address`. `gh auth setup-git` cũng KHÔNG
cứu nếu gh đang ở chế độ SSH. Chẩn đoán + fix (phiên thật đã chạy):
- `gh auth status` → xem dòng "Git operations protocol: ssh" và có SSH key local
  không (`ls ~/.ssh/*.pub`); test `ssh -T git@github.com` → "Hi <user>! You've
  successfully authenticated".
- Nếu SSH OK, ĐỔI remote sang SSH rồi push:
  ```bash
  git remote set-url origin git@github.com:<owner>/<repo>.git
  git push origin main
  ```
  Đây là thay đổi cấu hình repo-local nhẹ, đảo lại được; không cần nhúng token vào URL.

### Verify sau push = CLONE-AND-RUN (không phải recompute-từ-CSV-remote)

Vì repo giờ là CODE-ONLY (Bước 2b — không ship CSV/figure), KHÔNG còn CSV trên remote
để recompute mean. Verify ĐÚNG = chứng minh người đọc tái lập được từ con số 0:
1. `gh repo view --json pushedAt` + clone SẠCH từ GitHub vào thư mục trắng GHI ĐƯỢC
   (`~/gh_verify`, KHÔNG `/tmp` vì hay permission-denied): `git clone git@github.com:...`.
2. Kiểm cấu trúc đúng policy: `find` đếm file; xác nhận `docs/ figures/ reports/`
   = 0 file (đã cất), `spike_*` = 0 (đã chặn), nhưng script-tái-lập-đã-đổi-tên
   (vd `ablation_danger_*.py`) CÓ mặt; repo code không còn `.tex`.
3. Secret/path scan trên bản clone (lần cuối, trên đúng cái public): `grep -rniE
   "/home/|openclaw|gho_|ghp_|sk-[A-Za-z0-9]{20}"` = 0.
4. **Tạo venv mới từ bản clone + chạy MỘT script tái lập** (chọn script nhẹ nhất
   sinh một bảng), đối chiếu output với số bài. Phiên thật: clone trắng → venv →
   `ablation_danger_severity.py` → ra đúng Classic 0.00414 / severity ρ6 0.00431 +
   sanity-check pass = bằng chứng end-to-end reviewer tái lập được, không cần file
   nào của người dùng. Script 30-win nặng (~10-13 phút) → chạy background + wait.
5. Dọn thư mục clone tạm (`~/gh_check`, `~/gh_verify`) hoặc hỏi người dùng giữ lại.

## Checklist nhanh

- [ ] `_repos/<repo>` là git remote; `git status` có afternoon changes chưa commit?
- [ ] Re-run script → diff CSV bỏ cột runtime → 0 ô khoa học lệch?
- [ ] **TRACE MỌI bảng trong bài → CSV/script, không chỉ headline; bảng không có CSV nguồn thì grep tìm script (có thể là `spike_*`) và chạy xác minh?**
- [ ] Mean recompute khớp headline bài?
- [ ] **Trước khi gitignore `spike_*`: mỗi spike có sinh bảng/hình ĐANG trong bài không? Có thì đổi tên (bỏ `spike_`) + set default param khớp bài, KHÔNG chặn?**
- [ ] Scrub: `grep` path nội bộ (`/home/`, `/Users/`...) + secret trong code sắp push = 0?
- [ ] Repo chỉ còn CODE + DATA NGUỒN? (gitignore + `git rm --cached` mọi kết quả/draft/`.tex`)
- [ ] README viết lại theo policy code-only, mọi script tên trong README tồn tại thật?
- [ ] `git add` tường minh (KHÔNG `-A`)?
- [ ] Trình classification + xin duyệt TRƯỚC khi push public main?
- [ ] Push fail HTTPS "could not read Username"? → `git remote set-url origin git@github.com:...` (SSH) rồi push lại.
- [ ] Verify sau push = CLONE SẠCH từ GitHub + tạo venv + CHẠY 1 script tái lập ra đúng số bài (KHÔNG recompute-từ-CSV-remote vì repo code-only không còn CSV)?
