# SoTA baseline comparison integrity (Q1 review-proofing)

When người dùng asks "đã so sánh với SoTA mới nhất/tốt nhất chưa?" or you add recent
baselines to a comparison table. Lesson distilled from bài probe-transmit/bài AoI-greenhouse.

## 1. Audit what the current baselines actually ARE before answering

Read the comparison script (e.g. `sota_comparison_*windows.py`) and list each
baseline's true provenance. Classic families you implemented yourself (Whittle
1988, MaxWeight/Tassiulas 1992, AoII/Maatouk 2020, VoI-greedy) are *foundational
families*, NOT "recent SoTA methods". A Q1 reviewer (IoTJ/TMC/TON) will ask
"how do you compare to [named 2024-2025 method]?". If every baseline is ≥pre-2023
and unnamed, that is the single biggest comparison gap — say so directly.

## 2. STRAW-MAN DETECTION — the load-bearing pitfall

After implementing a recent published baseline, smoke-test it (1 window) BEFORE
any full run. Sanity gate on the numbers:

- If your method beats the new baseline by an enormous margin (saw ~25-90×), AND
- the new (published, 2023-2026) baseline is ALSO worse than your basic
  foundational baselines (AoII-greedy etc.),

then it is almost certainly an UNFAIR implementation on your side, NOT a weak
method. A peer-reviewed recent method that loses to vanilla AoII-greedy is a red
flag. Do NOT put those numbers in any table — a reviewer instantly calls
"straw-man baseline" and it damages credibility more than having no baseline.

Common root causes of accidental straw-manning (all seen this session):
- The baseline optimizes a DIFFERENT objective than your headline metric. E.g. a
  Gauss-Markov remote-estimation Whittle index minimizes estimation error, not
  safety-violation; scored on a safety-loss metric it looks terrible. That's a
  metric mismatch, not a bad method.
- Missing the safety-gating / near-threshold focus that your method has, so the
  baseline spreads budget uniformly instead of concentrating on at-risk arms.
- Mismatched index scale between probe and payload stages → noisy ranking.

## 3. Resolution — present each baseline at its STRONGEST

When numbers look like straw-man, STOP and ask người dùng which framing (don't
self-decide, it's an integrity call):

- (A) **Fair-tune**: give each baseline the same safety-aware machinery your
  method has (near-threshold gate, matched scale), so it loses *reasonably*
  (≈1.5-5×) rather than collapsing. Honest + persuasive: "we gave each SoTA its
  best safety-aware form; ours still wins."
- (B) **As-published + honest framing**: keep the baseline faithful to its paper
  (optimizing its own objective) and state explicitly that it underperforms on
  the safety metric *because it was not designed for safety* — this motivates
  your contribution. Valid, but MUST be spelled out or it reads as straw-man.
- Ideal: report BOTH (as-published and safety-tuned variant).

Always also report runtime/step (Q1 reviewers compare compute).

## 4. Honesty labels for reimplemented baselines

Each adapter is "OUR implementation of the published index rule," stated as such
in the module docstring and paper. Do NOT claim to reproduce the authors' exact
numbers or setup. Run them apples-to-apples: same channel, same budgets, same
windows, same metrics as your method. Keep them as pure index rules (no training)
where possible so they're runnable in-harness; flag learned baselines (NeurWIN /
ContextWIN, DRL index networks) to người dùng as heavy — faithful reimpl is a
project in itself; option is cite + a clearly-labelled light proxy, or omit with
justification.

### Adapting a pull/query-based baseline when YOUR problem has no explicit query

Pull-based AoI methods (QAoI-Whittle 2411.02108, QVAoI 2407.08587) assume freshness
only matters WHEN a query arrives. If your problem has no literal query, model the
per-slot query probability as the **task-relevance proxy** — for safety monitoring,
`q_i = danger(μ_i)` ∈ [0,1] (a sensor near a bound is implicitly "queried" more).
Then QAoI index = `age_i · q_i`, QVAoI index = `version_lag_i · q_i` where
`version_lag = |μ−xh|/σ`. State the analog explicitly in the docstring + paper so
it's an honest adaptation, not a misrepresentation. Result this session (dual-metric,
as-published): semantic/query-aware 2024 baselines (RiskAwareAoII, QAoI-Whittle) land
at a FAIR 2.8-3.1× vs bài AoI-greenhouse, while pure Whittle-MSE (OnlineWhittle, MultiChan, QVAoI)
collapse at 10-11× AND show high RMSE — exactly the separation that proves the table
isn't straw-man: methods near your design philosophy compete; estimation-only methods
lose on safety because they optimize MSE (and the RMSE column shows where they'd win).

## 5. Live citation verification (do NOT cite from memory)

Before any arXiv ID enters a plan or manuscript, verify it live. Background
literature subagents have failed silently here (returned after 5-7s with 1 API
call and no real search) — when that happens, do NOT re-dispatch endlessly;
verify inline yourself and never fabricate citations.

arXiv API quirk (confirmed this session):
- `http://export.arxiv.org/api/query` returns HTTP 400 / **0 bytes** — useless.
- `https://export.arxiv.org/api/query?search_query=...` works (HTTPS only).
- Calling it from `execute_code` (Python) timed out at 300s; a direct
  `terminal` curl with a 25s timeout returned cleanly. Prefer terminal curl.

Recipe (one query, parse ID + date + title):
```bash
timeout 25 curl -s "https://export.arxiv.org/api/query?search_query=all:%22Age+of+Incorrect+Information%22+AND+all:threshold&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending" -o r.xml
grep -oE "abs/[0-9]+\.[0-9]+" r.xml
grep -oE "<title>[^<]+" r.xml   # first <title> is the feed title — skip it
grep -oE "<published>[^<]+" r.xml
```
Record verified IDs + dates + quoted titles in `docs/sota_baselines_plan.md`
with the verification date, and state plainly which IDs are still from memory and
unverified.

**ID-vs-title misattribution trap (cost a wrong implementation this session).** A
batch `search_query` returns MULTIPLE results; the `abs/ID`, `<published>`, and
`<title>` lists are parsed in parallel and are EASY to misalign — you can grab the
ID from result #1 and the title from result #2. Two concrete failures seen:
2510.22288 was logged as "AoI-at-Query Whittle" but is actually "Correlated Wiener
Processes / MAF scheduler"; 2511.18378 was logged as "QVAoI" but is a text-to-image
RL paper (completely unrelated). ALWAYS re-fetch each candidate by exact ID with
`?id_list=ID` and read its OWN `<title>` + `<summary>` before trusting the pairing
or implementing its index rule. The real IDs were QVAoI=2407.08587 and
QAoI-Whittle=2411.02108 (both 2024, not 2025-2026 — also re-check the year you
claimed). One bad pairing → you implement the wrong algorithm.

## 6. Public-code availability check (người dùng asks "bài đó có public code không?")

Order of checks, and the traps:
- arXiv abstract page shows a **"Code, Data"** tab on EVERY paper — it is a
  default UI label, NOT proof of an author repo. Don't report it as "has code".
  The integration links it lists (alphaxiv, semanticscholar, core.ac.uk,
  dagshub, huggingface, paperswithcode) are auto-injected on every abstract too.
- Papers-with-Code API (`https://paperswithcode.com/api/v1/papers/?arxiv_id=ID`)
  and Semantic Scholar Graph API often return 0 bytes / HTTP 429 without a key —
  rate-limited, not "no code". GitHub search API returns empty without auth.
- Honest conclusion when tools are blocked: "not found with available tools" ≠
  "confirmed no code". Say which sources you checked and which were blocked.
  Practical prior: 2026 papers are usually too new to have released code; a 2023
  paper is more likely to. To confirm definitively you'd need an S2 API key,
  Google Scholar by hand, or the paper PDF's "Code availability" section.
- Implication for the table: NO public author code is the community-accepted
  green light to reimplement the published *index rule* yourself (label it "our
  implementation"). But it also means the fairness burden is entirely on you —
  so §2 straw-man detection and §3 fair presentation become mandatory, not
  optional.

## 7. Diagnostic: a flat tuning sweep means the lever is WRONG, not weak

When fair-tuning a baseline (§3-A), sweep the safety-awareness strength (e.g. a
multiplicative danger reweight `idx * (floor + (1-floor)*danger)**gamma`,
gamma ∈ {0, 0.5, 1, 2, 3}). If the best gamma barely moves loss (saw 0.0425 →
0.0393, ~8%) and it's still ~10× your method, STOP patching — that is positive
evidence the safety-gate is NOT the bottleneck. Root cause this session: the
base index ranks by *estimation uncertainty* (predictive std / error-variance
reduction), while your method's danger term is *additive and dominant* (e.g.
VoU = TrackGap + λ·P_vio with λ=6) keyed on the forecast mean crossing the
threshold. A multiplicative reweight can't fix a base index dominated by the
wrong quantity. The honest read: the baseline optimizes a different objective
(MSE), so report dual-metric (RMSE where it competes + safety-loss where it
loses) rather than forcing it to look good — and note that making it additive-
dominant like yours would turn it into a near-clone of your method, defeating
the purpose of an independent baseline. This is exactly why người dùng's choice
"làm đúng như bài báo gốc" (as-published, gamma=0) + dual-metric is the correct
integrity stance.
