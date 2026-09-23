# Execution discipline & honest negative results (người dùng)

Two lessons người dùng corrected explicitly during a bài bandwidth-scheduling manuscript-revision session.

## 1. Say-it → do-it in the SAME turn (corrected multiple times)

Người dùng reacted sharply — twice — when a turn announced an action but ended
without the tool actually running:
- "lại bảo đọc nhưng không thấy đọc? Agent bị kẹt gì hả"
- "sao lại nói làm xong dừng nữa rồi"

Rules:
- Never write "để agent đọc…/agent tìm…/agent xem lại…" and then stop. The tool call
  MUST be in the same turn as the sentence that promises it.
- On long / multi-step / delegated work, KEEP GOING autonomously. Do not pause
  for a nudge after each step. Only stop for: (a) task complete, (b) a real
  blocker needing his decision (safety / missing data / direction change),
  (c) a genuine scientific trade-off. Otherwise continue.
- Announce the tool/skill in use on the FIRST line of every task turn, not just
  the opening turn.

## 2. Honest negative results — do NOT patch for pretty numbers

When an ablation or extension shows a component is inert or harmful, and it
repeats consistently on the same data, that is a REAL FINDING, not a bug to
hide. In the bài bandwidth-scheduling session, three separate "risk/tail" mechanisms all proved
useless on a light-tail greenhouse replay:
- raw `p_vio` term in the urgency score (ablation: dropping it improved obj,
  missed%, and CVaR/VaR tail together — it double-counted the detector rule);
- risk-widening budget term `-c_R·R·b` (on/off nearly identical → dual already
  regulated it);
- bài bandwidth-scheduling-CVaR tail pricing (did not beat plain PD, even lost at the extreme tail).

Consistent message: VoU urgency + primal-dual duals already captured the
achievable gain; the tail was too light for extra machinery to help.

How to handle:
- Report it straight, with 2–3 options (move to Limitations/Future work · keep
  as a controlled negative result · request data in the right regime) and a
  recommendation. Let người dùng choose the direction.
- DERIVE-then-verify. The winning fix (VoU `g(p)=4p(1-p)`, decision-uncertainty
  = leading-order value-of-information for a binary safety decision) came from a
  theory argument BEFORE the run, not from a grid search. Never grid-search
  blindly to force a nice number. Occam wins.

## 3. Diagnose root cause after 2 failures, don't keep patching

When the first CVaR run gave bài bandwidth-scheduling-MV ≡ bài bandwidth-scheduling-PD (identical to every digit) and
CVaR worse than PD, the fix was to STOP and read the code for the root cause:
- MV variance was computed on realized loss history (constant across candidate
  budgets → no effect on argmin) instead of predicted per-candidate risk;
- CVaR ξ was drifting to 0 via a bad subgradient, so the term just amplified
  mean loss instead of targeting the tail.
Fix ξ as the empirical α-quantile of a trailing loss window (direct VaR
estimate), price only predicted tail exceedance. Two bugs, one read — not five
blind tweaks.
