#!/usr/bin/env python3
"""Tests for consistency_audit.py.

Every check is exercised in both directions: a fixture that must produce the
finding and one that must not. A gate without a negative test is a gate that
fires on clean prose, and a noisy gate gets ignored — which is worse than no
gate, because it trains the author to skip the report.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import consistency_audit as ca  # noqa: E402

DIRTY = r"""
\begin{abstract}
\textbf{Tóm tắt.} Bộ dữ liệu có 4.668 câu, đạt 54.5\% độ chính xác.
\end{abstract}
\begin{abstract}
\textbf{Abstract.} The dataset contains 4,668 items with 93,8\% coverage.
\end{abstract}
\section{Mở đầu}
Có bảy phép chẩn đoán dưới đây. Kết quả ở Mục~3 và Bảng~2.
Chỉ số KTC dùng ngay, rồi dùng lại. Về sau mới nói khoảng tin cậy (KTC).
\begin{table}[h]
\caption{Bảng chẩn đoán}
\begin{tabular}{lr}
\toprule
Phép đo & Kết quả \\
\midrule
A & 1 \\
B & 2 \\
C & 3 \\
D & 4 \\
E & 5 \\
F & 6 \\
\bottomrule
\end{tabular}
\end{table}
\textbf{Từ khóa:} một; hai; ba.
\textbf{Keywords:} one; two; three; four.
"""

CLEAN = r"""
\begin{abstract}
\textbf{Tóm tắt.} Bộ dữ liệu có 4.668 câu, đạt 54,5\% độ chính xác.
\end{abstract}
\begin{abstract}
\textbf{Abstract.} The dataset contains 4,668 items with 93.8\% coverage.
\end{abstract}
\section{Mở đầu}
Có sáu phép chẩn đoán dưới đây. Kết quả ở Mục~\ref{sec:m} và Bảng~\ref{tab:d}.
Khoảng tin cậy (KTC) được định nghĩa ngay; về sau chỉ dùng KTC.
\begin{table}[h]
\caption{Bảng chẩn đoán trên tập kiểm tra.}
\begin{tabular}{lr}
\toprule
Phép đo & Kết quả \\
\midrule
A & 1 \\
B & 2 \\
C & 3 \\
D & 4 \\
E & 5 \\
F & 6 \\
\bottomrule
\end{tabular}
\label{tab:d}
\end{table}
\textbf{Từ khóa:} một; hai; ba.
\textbf{Keywords:} one; two; three.
"""


def classes(result: dict) -> list[str]:
    return [f["class"] for f in result["findings"]]


def test_dirty_produces_every_class():
    got = classes(ca.scan(DIRTY))
    for expected in (
        "FORMAT_ZONE", "SELF_COUNT", "CROSSREF_HARDCODE",
        "ABBREV_LATE", "KEYWORD_PARITY", "CAPTION_TERMINAL",
    ):
        assert expected in got, f"{expected} not detected; got {got}"


def test_dirty_counts():
    r = ca.scan(DIRTY)
    assert r["counts"]["FORMAT_ZONE"] == 2, r["counts"]
    assert r["counts"]["CROSSREF_HARDCODE"] == 2, r["counts"]
    assert r["counts"]["SELF_COUNT"] == 1, r["counts"]
    assert r["counts"]["ABBREV_LATE"] == 1, r["counts"]
    assert r["exit_code"] == 2


def test_clean_is_silent():
    r = ca.scan(CLEAN)
    assert r["findings"] == [], [f["detail"] for f in r["findings"]]
    assert r["exit_code"] == 0


def test_format_zone_direction():
    """Comma in the English zone and point in the Vietnamese zone, both caught."""
    r = ca.scan(DIRTY)
    details = " ".join(f["detail"] for f in r["findings"] if f["class"] == "FORMAT_ZONE")
    assert "Vietnamese zone uses a decimal point" in details
    assert "English zone uses a decimal comma" in details


def test_self_count_ignores_unrelated_table():
    """'five steps' above a six-row results table is not a count claim."""
    src = r"""
\section{M}
Có năm bước xử lý dữ liệu, mô tả như sau.
\begin{table}[h]
\caption{Độ chính xác theo mô hình}
\begin{tabular}{lr}
\toprule
Mô hình & Acc \\
\midrule
A & 1 \\ B & 2 \\ C & 3 \\ D & 4 \\ E & 5 \\ F & 6 \\
\bottomrule
\end{tabular}
\end{table}
"""
    assert ca.check_self_count(src) == []


def test_self_count_fires_when_noun_matches_caption():
    src = r"""
\section{M}
Có bảy phép đo trong bảng này.
\begin{table}[h]
\caption{Bảng các phép đo}
\begin{tabular}{lr}
\toprule
Phép đo & Kết quả \\
\midrule
A & 1 \\ B & 2 \\ C & 3 \\ D & 4 \\ E & 5 \\ F & 6 \\
\bottomrule
\end{tabular}
\end{table}
"""
    got = ca.check_self_count(src)
    assert len(got) == 1, got
    assert "6 data rows" in got[0]["detail"]


def test_abbrev_ignores_names_and_units():
    """NVIDIA, EMNLP, GB are names/units; no definition exists, so no finding."""
    src = (
        "Chạy trên GPU NVIDIA L4 24 GB. Hội nghị EMNLP và ACL. "
        "Nhắc lại NVIDIA, EMNLP, GB, 24 GB lần nữa."
    )
    assert ca.check_abbrev(src) == []


def test_abbrev_requires_definition_to_exist():
    """Use before definition is a defect; use with no definition anywhere is not."""
    late = "Dùng KTC ngay ở đây. Rồi dùng KTC lần nữa. Sau đó nói khoảng tin cậy (KTC)."
    got = ca.check_abbrev(late)
    assert len(got) == 1 and got[0]["class"] == "ABBREV_LATE", got

    never = "Dùng KTC ngay ở đây. Rồi dùng KTC lần nữa, không định nghĩa."
    assert ca.check_abbrev(never) == []


def test_crossref_accepts_generated_refs():
    src = r"Xem Mục~\ref{sec:a} và Bảng~\ref{tab:b}, Hình~\ref{fig:c}."
    assert ca.check_crossrefs(src) == []


def test_caption_terminal():
    src = r"\caption{Không có dấu chấm}"
    assert len(ca.check_captions(src)) == 1
    assert ca.check_captions(r"\caption{Có dấu chấm.}") == []


def test_referent_collision_reports_quantities():
    src = (
        "Tập đánh giá có 14.210 bản ghi sau lọc. "
        "Sau đó tập đánh giá gồm 688 câu dùng để chấm điểm."
    )
    got = ca.check_referent_collision(src, ["tập đánh giá"])
    assert len(got) == 1, got
    assert "14.210" in got[0]["detail"] and "688" in got[0]["detail"]


def test_referent_collision_silent_for_one_quantity():
    src = "Tập kiểm tra có 688 câu. Tập kiểm tra được dùng cho mọi bảng."
    assert ca.check_referent_collision(src, ["tập kiểm tra"]) == []


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_") or not callable(fn):
            continue
        try:
            fn()
            print(f"PASS {name}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL {name}: {exc}")
    print(f"\n{'OK' if not failures else str(failures) + ' failure(s)'}")
    raise SystemExit(1 if failures else 0)
