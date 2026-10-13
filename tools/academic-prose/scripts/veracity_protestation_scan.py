#!/usr/bin/env python3
"""Flag veracity-protestation padding in any generated artifact; report only, never rewrite.

The failure this gate catches: a generated slide, document, demo page or report
spends words asserting that its own evidence is real -- "ảnh chụp thật",
"thao tác thật", "số đo được, không ước lượng", "real output, not simulated".
The assertion adds no information: the evidence either stands on its own or the
adjective does not save it. Worse, protestation is the signature of fabricated
content -- real artifacts rarely need to claim they are real.

Principle enforced (see references/veracity-protestation-gate.md):
  Evidence presents itself. If authenticity genuinely matters, replace the
  adjective with a checkable pointer (URL, hash, timestamp, command line),
  never with emphasis.

A lexical hit is a candidate, never a verdict, same as vi_ai_pattern_scan.py.
Licensed constructions are suppressed automatically:
  * mathematics: số thực / phần thực / giá trị thực / real analysis
  * a stated contrast against synthetic or simulated data inside one sentence
    ("dữ liệu thật, khác với bộ tổng hợp ...") -- that is a methods statement
  * quotations and cited speech

Input: .tex .md .txt .docx .pptx (single file or directory; office files are
read through ooxml_text like the sibling scanners). Comments are stripped for
tex/md before scanning so this file and the fixture corpus do not flag themselves.

Exit: 0 no candidate, 2 candidates present, 3 input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:  # office support is optional at runtime; sibling scanners require it
    from ooxml_text import read_text as read_ooxml_text
except Exception:  # pragma: no cover
    read_ooxml_text = None

# --- patterns ----------------------------------------------------------------

# Verdict: delete (the sentence loses nothing but the protest)
PROTESTATION = [
    # Vietnamese -- authenticity of a shown artifact
    r"ảnh\s+chụp\s+(?:màn\s+hình\s+)?thật",
    r"(?:hình\s+ảnh|screenshot|ảnh)\s+thật",
    r"thao\s+tác\s+thật",
    r"chạy\s+thật",
    r"kết\s+quả\s+(?:lệnh\s+)?thật",
    r"lệnh\s+chạy\s+thật",
    r"output\s+thật",
    r"(?:drive|dữ\s+liệu|thư\s+mục|hệ\s+thống|máy\s+chủ|tài\s+khoản)\s+thật",
    r"trên\s+(?:môi\s+trường\s+)?thật\b",
    r"người\s+thật\s+việc\s+thật\s+100",
    r"hoàn\s+toàn\s+thật",
    r"100\s*%\s*(?:là\s+)?thật",
    # Vietnamese -- denial of fakery (still protestation)
    r"không\s+phải\s+(?:ảnh\s+vẽ|ảnh\s+giả|ảnh\s+dựng|mô\s+phỏng|giả\s+lập|diễn|dàn\s+dựng|làm\s+giả|số\s+liệu\s+bịa|mockup)",
    r"không\s+(?:phải\s+)?(?:là\s+)?(?:ước\s+lượng|ước\s+tính|phỏng\s+đoán|con\s+số\s+ áng)",
    r"không\s+dùng\s+(?:mock|fake|dữ\s+liệu\s+giả)",
    r"đo\s+được(?:,|\s)\s+không\s+ước",
    r"(?:số|kích\s+thước|dung\s+lượng|thời\s+gian)\s+đo\s+(?:được\s+)?(?:từ\s+)?(?:hệ\s+thống\s+)?thực\s+tế",
    r"xác\s+thực\s+(?:100\s*%|tuyệt\s+đối)",
    r"đã\s+(?:được\s+)?kiểm\s+chứng\s+thực\s+tế",
    r"minh\s+chứng\s+sống",
    r"bằng\s+chứng\s+sống",
    # English counterparts
    r"\breal\s+screenshot\b|\bactual\s+screenshot\b|\bgenuine\s+screenshot\b",
    r"\breal\s+execution\b|\bactually\s+executed\b|\blive\s+output\b|\breal\s+output\b",
    r"\bnot\s+simulated\b|\bnot\s+mocked?\b|\bnot\s+a\s+mockup\b|\bnot\s+staged\b",
    r"\breal[- ]world\s+run\b|\breal\s+terminal\b",
    r"\btrue\s+to\s+life\b|\bauthentic\s+capture\b",
]

# Verdict: replace_with_pointer (authenticity matters -> give a checkable handle)
NEEDS_POINTER = [
    r"ảnh\s+(?:này\s+)?(?:được\s+)?chụp\s+(?:trực\s+tiếp\s+)?(?:từ|trên)\s+(?:máy|màn\s+hình|hệ\s+thống)",
    r"(?:số\s+liệu|biểu\s+đồ|dữ\s+liệu|kết\s+quả|hình\s+ảnh)?\s*(?:được\s+)?(?:đo|lấy|trích|thu)\s+(?:trực\s+tiếp\s+)?(?:từ|trên)\s+(?:hệ\s+thống|máy|drive|thực\s+địa|môi\s+trường)",
    r"kết\s+quả\s+(?:được\s+)?trả\s+về\s+(?:trực\s+tiếp\s+)?từ\s+lệnh",
    r"\bdirect(?:ly)?\s+from\s+the\s+(?:system|machine|terminal)\b",
    r"\bcaptured\s+(?:directly\s+)?(?:from|on)\s+the\s+(?:live\s+)?(?:system|machine)\b",
]

# --- licensing ---------------------------------------------------------------

MATH_LICENSE = re.compile(
    r"số\s+thực|phần\s+thực|giá\s+trị\s+thực|biến\s+thực|hàm\s+thực|"
    r"real\s+analysis|real\s+numbers?|\bRe\b|\breal\s+part\b", re.I)
CONTRAST_LICENSE = re.compile(
    r"(?:khác\s+với|so\s+với|thay\s+vì|không\s+dùng|phân\s+biệt|"
    r"unlike|compared\s+(?:to|with)|instead\s+of|versus|\bvs\b|"
    r"synthetic|tổng\s+hợp|mô\s+phỏng|giả\s+lập|dummy|fake)", re.I)
QUOTE_LICENSE = re.compile(r'“[^”]*”|"[^"]*"|\\(?:enquote|textquote|blockquote)\{[^}]*\}|`[^`]*`')

TEXT_EXTS = {".tex", ".md", ".txt", ".html", ".rst"}
OFFICE_EXTS = {".docx", ".pptx"}

COMMENT_TEX = re.compile(r"(?<!\\)%[^\n]*")
COMMENT_MD = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"(?s)```.*?```")


def read_pptx(path: Path) -> str:
    """Extract slide text and speaker notes from a .pptx zip natively.

    ooxml_text.read_text only special-cases .docx and falls back to a raw
    utf-8 read, which raises on .pptx bytes -- measured on three real decks
    (2026-10-13). Parse slideN.xml + notesSlideN.xml ourselves instead.
    """
    import zipfile
    from xml.etree import ElementTree as XET
    out = []
    with zipfile.ZipFile(path) as z:
        names = sorted(z.namelist())
        xmls = [n for n in names
                if n.startswith("ppt/slides/slide")
                or n.startswith("ppt/notesSlides/notesSlide")]
        for n in xmls:
            try:
                root = XET.fromstring(z.read(n))
            except XET.ParseError:
                continue
            texts = [t.text for t in root.iter(
                "{http://schemas.openxmlformats.org/drawingml/2006/main}t")
                if t.text]
            if texts:
                out.append(" ".join(texts))
    return "\n\n".join(out)


def read_input(path: Path) -> str:
    if path.suffix.lower() == ".pptx":
        return read_pptx(path)
    if path.suffix.lower() in OFFICE_EXTS:
        if read_ooxml_text is None:
            raise ValueError(f"ooxml_text unavailable, cannot read {path}")
        return read_ooxml_text(path)
    if path.suffix.lower() in TEXT_EXTS:
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix.lower() == ".tex":
            text = COMMENT_TEX.sub(" ", text)
        elif path.suffix.lower() in {".md", ".html", ".rst"}:
            text = COMMENT_MD.sub(" ", text)
        return text
    raise ValueError(f"unsupported input type: {path}")


def split_sentences(text: str) -> list[str]:
    text = FENCE.sub(" <CODE> ", text)
    text = QUOTE_LICENSE.sub(" <QUOTE> ", text)
    parts = re.split(r"(?<=[.!?:;\n])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def scan(text: str, source: str = "<stdin>") -> dict:
    findings = []
    for i, sent in enumerate(split_sentences(text), start=1):
        licensed = bool(MATH_LICENSE.search(sent))
        for pat in PROTESTATION:
            m = re.search(pat, sent, re.I)
            if not m:
                continue
            # a stated contrast against synthetic/simulated data is a methods
            # statement, not protestation -- but only when the hit word itself
            # is the contrastive one (dữ liệu thật vs dữ liệu tổng hợp)
            if not licensed and CONTRAST_LICENSE.search(sent) and re.search(
                    r"(?:thật|thực\s+tế|real|actual|live)", m.group(0), re.I):
                licensed = True
            if licensed:
                continue
            findings.append({
                "id": f"V{len(findings)+1}",
                "class": "veracity_protestation",
                "verdict": "delete",
                "sentence_no": i,
                "span": m.group(0),
                "sentence": sent[:200],
                "source": source,
            })
            break  # one finding per sentence is enough signal
        if any(f["sentence_no"] == i for f in findings):
            continue
        for pat in NEEDS_POINTER:
            m = re.search(pat, sent, re.I)
            if not m:
                continue
            findings.append({
                "id": f"V{len(findings)+1}",
                "class": "authenticity_claim_without_pointer",
                "verdict": "replace_with_pointer",
                "sentence_no": i,
                "span": m.group(0),
                "sentence": sent[:200],
                "source": source,
            })
            break
    return {"source": source, "findings": findings,
            "verdict": "fail" if findings else "pass"}


def render_report(result: dict) -> str:
    out = [f"== veracity-protestation gate: {result['source']} =="]
    if not result["findings"]:
        out.append("PASS: không có câu nào tự chứng thực.")
        return "\n".join(out)
    for f in result["findings"]:
        out.append(f"[{f['id']}] {f['class']} -> {f['verdict']}")
        out.append(f"    span: \"{f['span']}\"")
        out.append(f"    câu : \"{f['sentence']}\"")
    out.append(f"TỔNG: {len(result['findings'])} ứng viên. "
               "Ứng viên không phải kết luận: đọc lại câu và xoá phần tự chứng "
               "thực, hoặc thay bằng pointer kiểm tra được (link/hash/lệnh).")
    return "\n".join(out)


def iter_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            files.extend(sorted(
                f for f in p.rglob("*")
                if f.suffix.lower() in TEXT_EXTS | OFFICE_EXTS))
        else:
            files.append(p)
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Flag veracity-protestation padding; report only, never rewrite.")
    ap.add_argument("inputs", nargs="+", help="file or directory")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    results = []
    for p in iter_files([Path(x) for x in args.inputs]):
        try:
            text = read_input(p)
        except Exception as e:
            print(f"input error: {p}: {e}", file=sys.stderr)
            return 3
        results.append(scan(text, str(p)))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(render_report(r))
            print()
    return 2 if any(r["findings"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
