#!/usr/bin/env python3
"""QUÉT ĐỘ PHỦ PIN — bản tổng quát để publish, không chứa nội dung bản thảo cụ thể.

Nguồn gốc: /tmp/sweep_pin_coverage2.py (đã đo 82 cặp trên một bản thảo HUJOS, đóng 13 điểm mù).
Bản này: tham số hoá 4 đường dẫn, giữ nguyên logic, để người khác áp dụng cho gate của họ.

CÁCH DÙNG:
  python sweep_pin_coverage.py --project /path/to/project --gate referee_verify.py \\
                               --manuscript manuscript.md --output /tmp/pin_coverage.jsonl

  Gate phải:
    - có dòng `H = Path('...')` gán đường dẫn thư mục dự án
    - in `=== RESULT: PASS ===` hoặc `=== RESULT: FAIL N ===` ở cuối
    - in `FAILED: ...` cho mỗi check hỏng

  Script sẽ:
    1. Chạy gate trên nguồn, đòi PASS (nếu không thì dừng — baseline đỏ vô hiệu hoá mọi kết luận)
    2. Dựng bản sao, thay đường dẫn trong gate trỏ về bản sao
    3. Liệt kê mọi số trong thân bài, phân loại DATA (đơn vị đo) / CITE (pháp lý, cấu trúc)
    4. Với mỗi (token, lần xuất hiện thứ j): thay đúng 1 chỗ, chạy gate, phân loại:
       - CAUGHT: gate đỏ và có dòng FAILED
       - CRASH: gate đỏ nhưng không có FAILED (nổ traceback — phép thử hỏng, không tính là bắt)
       - BLIND: gate xanh (sửa sai mà không bị phát hiện — điểm mù)
    5. Khôi phục bản thảo bằng sha256, báo cáo độ phủ

ĐIỀU KIỆN TIÊN QUYẾT: baseline phải xanh. Nếu không, mọi kết luận sau đó vô hiệu.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path


def run_gate(cwd, gate_file, py, timeout=600):
    """Chạy gate, trả (rc, result, failed_lines, crash_tail, n_lines)."""
    p = subprocess.run([py, gate_file], cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    failed = [l.strip()[:150] for l in p.stdout.splitlines() if l.strip().startswith("FAILED:")]
    m = re.search(r"=== RESULT: (\w+ ?\d*) ===", p.stdout)
    result = m.group(1) if m else "KHÔNG-CÓ-RESULT"
    crash_tail = ""
    if p.returncode != 0 and not failed:
        lines = (p.stderr.strip().splitlines() or p.stdout.strip().splitlines()
                 or ["(cả stdout và stderr đều rỗng)"])
        crash_tail = "\n".join("      " + l[:180] for l in lines[-16:])
    return p.returncode, result, failed, crash_tail, len(p.stdout.splitlines())


def bump(tok):
    """Tăng 1 đơn vị, giữ định dạng locale VN (chấm nghìn, phẩy thập phân)."""
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", tok):
        s = str(int(tok.replace(".", "")) + 1)
        parts = []
        while len(s) > 3:
            parts.insert(0, s[-3:])
            s = s[:-3]
        parts.insert(0, s)
        return ".".join(parts)
    if "," in tok:
        ip, dp = tok.split(",")
        return str(int(ip) + 1) + "," + dp
    return str(int(tok) + 1)


def main():
    ap = argparse.ArgumentParser(description="Quét độ phủ pin bằng mutation testing")
    ap.add_argument("--project", required=True, help="Thư mục dự án chứa gate và bản thảo")
    ap.add_argument("--gate", default="referee_verify.py", help="File gate (mặc định: referee_verify.py)")
    ap.add_argument("--manuscript", default="manuscript.md", help="File bản thảo (mặc định: manuscript.md)")
    ap.add_argument("--output", default="/tmp/pin_coverage.jsonl", help="File output JSONL")
    ap.add_argument("--py", default=sys.executable, help="Đường dẫn Python interpreter")
    ap.add_argument("--max-occ", type=int, default=6, help="Cap số lần xuất hiện mỗi token (mặc định: 6)")
    ap.add_argument("--max-runs", type=int, default=130, help="Cap tổng số cặp (mặc định: 130)")
    args = ap.parse_args()

    H = Path(args.project).resolve()
    GATE = H / args.gate
    MSF = H / args.manuscript
    PY = args.py
    OUT = Path(args.output)
    MAX_OCC = args.max_occ
    MAX_RUNS = args.max_runs

    if not GATE.exists():
        print("!! không thấy gate: %s" % GATE, file=sys.stderr)
        sys.exit(2)
    if not MSF.exists():
        print("!! không thấy bản thảo: %s" % MSF, file=sys.stderr)
        sys.exit(2)

    # ---------- 0. điều kiện tiên quyết ----------
    print("=" * 92)
    print("0. ĐIỀU KIỆN TIÊN QUYẾT — gate trên nguồn phải PASS")
    print("=" * 92, flush=True)
    rc, res, failed, crash, nl = run_gate(H, GATE.name, PY)
    print("  exit=%d | RESULT=%s | %d dòng stdout | %d dòng FAILED" % (rc, res, nl, len(failed)),
          flush=True)
    if rc != 0 or res != "PASS":
        print("\n  DỪNG. Baseline đỏ -> đo tiếp vô hiệu.")
        for l in failed[:10]:
            print("   ", l)
        if crash:
            print("  traceback:\n" + crash)
        sys.exit(4)
    print("  -> nguồn XANH, an toàn để dựng bản sao.", flush=True)

    # ---------- 1. dựng bản sao ----------
    print("\n" + "=" * 92)
    print("1. DỰNG BẢN SAO")
    print("=" * 92, flush=True)
    MUT = Path(tempfile.mkdtemp(prefix="mut_sweep_"))
    shutil.rmtree(MUT, ignore_errors=True)
    shutil.copytree(H, MUT, dirs_exist_ok=True)
    rv = GATE.read_text(encoding="utf-8")
    # tìm dòng gán đường dẫn dự án
    m = re.search(r"^H\s*=\s*Path\(['\"]([^'\"]+)['\"]\)", rv, re.M)
    if not m:
        print("!! gate không có dòng `H = Path('...')` -> không đổi được đường dẫn bản sao", file=sys.stderr)
        sys.exit(3)
    old_path = m.group(1)
    (MUT / GATE.name).write_text(rv.replace("H = Path('%s')" % old_path, "H = Path('%s')" % MUT)
                                    .replace('H = Path("%s")' % old_path, 'H = Path("%s")' % MUT),
                                 encoding="utf-8")
    MSF_MUT = MUT / MSF.name
    ORIG = MSF_MUT.read_text(encoding="utf-8")
    SHA_ORIG = hashlib.sha256(ORIG.encode()).hexdigest()
    print("  bản sao %s (%d mục) | sha256 bản thảo: %s…" % (MUT, len(list(MUT.iterdir())), SHA_ORIG[:16]),
          flush=True)

    rc0, res0, f0, crash0, nl0 = run_gate(MUT, GATE.name, PY)
    print("  baseline bản sao: exit=%d | RESULT=%s | %d dòng FAILED" % (rc0, res0, len(f0)), flush=True)
    if crash0:
        print("  traceback (bản 1 nuốt đoạn này):\n" + crash0, flush=True)
    if rc0 != 0 or res0 != "PASS":
        print("\n  DỪNG: bản sao ĐỎ trong khi bản thật XANH -> cơ chế bản sao có vấn đề.", flush=True)
        for l in f0[:10]:
            print("   ", l)
        sys.exit(3)

    # ---------- 2. liệt kê token, phân loại DATA/CITE ----------
    MS = unicodedata.normalize("NFC", ORIG)
    cut = MS.find("# TÀI LIỆU THAM KHẢO")
    BODY = MS if cut < 0 else MS[:cut]

    NUM = re.compile(r"(?<![\w/])(?<!\d\.)(\d{1,3}(?:[.,]\d{3})+(?:,\d+)?|\d+(?:,\d+)?)"
                     r"(?![\w])(?!\.\d)")
    # chỉ giữ định vị pháp lý / cấu trúc; đơn vị đo (từ, trang, câu, mục) là DATA
    LAW_BEFORE = re.compile(r"(Điều|Khoản|khoản|điều|Thông tư|Nghị định|Nghị quyết|Luật|Bộ luật|"
                            r"Quyết định|Văn bản hợp nhất|QĐ|VBHN|Phụ lục|Bảng|Hình|Mục|Chương|"
                            r"mục|bảng|hình|năm|tháng|ngày)\s*$")
    LAW_AFTER = re.compile(r"^\s*(Điều|Khoản|khoản|điều|Thông tư|Nghị định|Nghị quyết|Luật|Bộ luật|"
                           r"QĐ|VBHN|Phụ lục|Bảng|Hình|Mục|Chương|mục|bảng|hình)")

    print("\n" + "=" * 92)
    print("2. LIỆT KÊ TOKEN SỐ TRONG THÂN BÀI")
    print("=" * 92, flush=True)
    print("  thân bài %d ký tự (toàn bài %d)" % (len(BODY), len(MS)), flush=True)
    occ = {}
    for m in NUM.finditer(BODY):
        occ.setdefault(m.group(1), []).append(m.start())
    uniq = list(occ.keys())
    print("  token duy nhất: %d | tổng số lần xuất hiện: %d" % (len(uniq), sum(len(v) for v in occ.values())),
          flush=True)

    items = []
    for tok in uniq:
        positions = occ[tok]
        ctx_before = " ".join(BODY[max(0, positions[0] - 48):positions[0]].split())[-40:]
        after = BODY[positions[0] + len(tok): positions[0] + len(tok) + 26]
        ctx_after = " ".join(after.split())[:22]
        if re.fullmatch(r"(19|20)\d{2}", tok):
            cls = "CITE"
        elif LAW_BEFORE.search(ctx_before) or LAW_AFTER.search(ctx_after):
            cls = "CITE"
        else:
            cls = "DATA"
        items.append({"tok": tok, "cls": cls, "n_occ": len(positions),
                      "ctx_before": ctx_before, "ctx_after": ctx_after})

    n_data = sum(1 for it in items if it["cls"] == "DATA")
    print("  DATA = %d | CITE = %d" % (n_data, len(items) - n_data), flush=True)

    # ---------- 3. dựng danh sách cặp ----------
    todo = [it for it in items if it["cls"] == "DATA"]
    pairs_a = [(it, 0) for it in todo]
    pairs_b = []
    for it in todo:
        ncap = min(it["n_occ"], MAX_OCC)
        for j in range(1, ncap):
            pairs_b.append((it, j))
        if it["n_occ"] > MAX_OCC:
            it["capped_from"] = it["n_occ"]

    pairs = pairs_a + pairs_b
    if len(pairs) > MAX_RUNS:
        keep_b = max(0, MAX_RUNS - len(pairs_a))
        pairs = pairs_a + pairs_b[:keep_b]
        print("  cặp cần đo %d > cap %d -> giữ TRỌN đợt A (%d token) + %d cặp đợt B; "
              % (len(pairs_a) + len(pairs_b), MAX_RUNS, len(pairs_a), keep_b), flush=True)
    else:
        print("  cặp (token, vị trí) cần đo: %d  [đợt A %d token + đợt B %d lần lặp]"
              % (len(pairs), len(pairs_a), len(pairs_b)), flush=True)
    print("  ước lượng thời gian: %d × ~9 s ≈ %.0f phút" % (len(pairs), len(pairs) * 9 / 60),
          flush=True)

    # ---------- 4. đo ----------
    print("\n" + "=" * 92)
    print("3. QUÉT — mỗi cặp là MỘT lần thay đúng 1 chỗ")
    print("=" * 92, flush=True)
    OUT.write_text("", encoding="utf-8")
    res = []
    n_caught = n_crash = n_blind = 0
    for i, (it, j) in enumerate(pairs, 1):
        tok = it["tok"]
        new = bump(tok)
        if new == tok:
            continue
        pat = re.compile(r"(?<![\w/.])" + re.escape(tok) + r"(?![\w.])")
        hits = list(pat.finditer(ORIG))
        if j >= len(hits):
            continue
        m = hits[j]
        mutated = ORIG[:m.start()] + new + ORIG[m.end():]
        if mutated == ORIG:
            continue
        MSF_MUT.write_text(mutated, encoding="utf-8")
        try:
            rc, result, failed, crash, _ = run_gate(MUT, GATE.name, PY)
        except subprocess.TimeoutExpired:
            rc, result, failed, crash = -1, "TIMEOUT", ["FAILED: TIMEOUT"], ""
        MSF_MUT.write_text(ORIG, encoding="utf-8")
        if rc == 0:
            kind = "BLIND"
            n_blind += 1
        elif failed:
            kind = "CAUGHT"
            n_caught += 1
        else:
            kind = "CRASH"
            n_crash += 1
        rec = dict(it)
        rec.update({"i": i, "occ_index": j, "new": new, "kind": kind, "rc": rc,
                    "result": result, "n_failed": len(failed), "failed_sample": failed[:2],
                    "crash_tail": crash[:600]})
        res.append(rec)
        with OUT.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("  %3d/%3d %-10s@%-2d -> %-10s %-6s %s%s"
              % (i, len(pairs), tok, j + 1, new, it["cls"], kind,
                 ("  <- " + failed[0][:88]) if (kind == "CAUGHT" and failed) else ""), flush=True)
        if kind == "CRASH" and crash:
            print(crash, flush=True)

    MSF_MUT.write_text(ORIG, encoding="utf-8")
    sha_after = hashlib.sha256(MSF_MUT.read_text(encoding="utf-8").encode()).hexdigest()

    # ---------- 5. tổng hợp ----------
    print("\n" + "=" * 92)
    print("KẾT QUẢ ĐỘ PHỦ PIN")
    print("=" * 92, flush=True)
    print("  bản thảo khôi phục: %s (%s…)" % ("ĐÚNG" if sha_after == SHA_ORIG else "SAI", sha_after[:16]))
    print("  đã đo %d cặp | CAUGHT %d | CRASH %d | BLIND %d" % (len(res), n_caught, n_crash, n_blind))
    for cls in ("DATA", "CITE"):
        grp = [r for r in res if r["cls"] == cls]
        if not grp:
            continue
        c = sum(1 for r in grp if r["kind"] == "CAUGHT")
        x = sum(1 for r in grp if r["kind"] == "CRASH")
        b = sum(1 for r in grp if r["kind"] == "BLIND")
        valid = len(grp) - x
        print("\n  nhóm %-5s: %d cặp -> CAUGHT %d | CRASH %d | BLIND %d" % (cls, len(grp), c, x, b))
        if valid:
            print("     độ phủ (loại CRASH khỏi mẫu): %d/%d = %.1f%%" % (c, valid, c / valid * 100))
        if cls == "DATA" and b:
            blind_toks = sorted({r["tok"] for r in grp if r["kind"] == "BLIND"})
            print("     ĐIỂM MÙ (sửa sai mà gate vẫn PASS): %s" % ", ".join(blind_toks))
        if x:
            print("     ca CRASH (phép thử hỏng, KHÔNG tính là bắt): %s"
                  % ", ".join(sorted({r["tok"] for r in grp if r["kind"] == "CRASH"})))
    print("\n  chi tiết: %s" % OUT)


if __name__ == "__main__":
    main()
