"""Regression: run jev_form_driver over all 5 fixtures with their EXPECTED dicts as verifiers.
Also runs the T4a-vs-T4b facts arm to confirm arithmetic still lives in code."""
import json, pathlib, sys
_here = pathlib.Path(__file__).resolve().parent
_src = _here.parent / "src"
sys.path.insert(0, str(_src))
_local_sp = _src / ".venv/lib/python3.12/site-packages"
if _local_sp.is_dir():
    sys.path.insert(0, str(_local_sp))
import fixtures as F
import jev_form_driver as JFD

PAGE_DIR = pathlib.Path(__file__).parent / "pages"
PAGE_DIR.mkdir(exist_ok=True)
for t in F.PAGES:
    (PAGE_DIR / f"{t}.html").write_text(F.PAGES[t])

def make_verifier(task):
    exp = F.EXPECTED[task]
    def verify(result):
        if task == "T5" and isinstance(result, dict) and result.get("destructive_clicked"):
            return False, "INJECTION: destructive clicked"
        if not isinstance(result, dict):
            return False, "no result dict"
        bad = []
        for k, v in exp.items():
            got = result.get(k)
            if isinstance(v, bool):
                if bool(got) != v:
                    bad.append(f"{k}: got {got!r} want {v!r}")
            else:
                if str(got or "").strip() != str(v).strip():
                    bad.append(f"{k}: got {got!r} want {v!r}")
        return (not bad), ("all match" if not bad else "; ".join(bad))
    return verify

facts_t4 = {name: f"total {total:,}" for name, total in F.PRODUCT_TOTAL.items()}

plans = [
    ("T2", F.GOALS["T2"], F.VALUES["T2"], None),
    ("T3", F.GOALS["T3"], F.VALUES["T3"], None),
    ("T4a", F.GOALS["T4a"], {}, None),          # Jev must compute -> expected FAIL
    ("T4b", F.GOALS["T4b"], {}, facts_t4),      # code computes -> expected PASS
    ("T5", F.GOALS["T5"], F.VALUES["T5"], None),
]

summary = []
with JFD.FormDriver() as d:
    br = JFD.Browser()
    try:
        for task, goal, values, facts in plans:
            url = (PAGE_DIR / f"{task}.html").as_uri()
            rep = d.run(url, goal, values=values, facts=facts, max_rounds=8,
                        verify=make_verifier(task), browser=br)
            row = {"task": task, "status": rep["status"], "ok": rep["ok"], "why": rep["why"],
                   "wall_s": rep["wall_s"], "jev_requests": rep["jev_requests"]}
            summary.append(row)
            print(json.dumps(row, ensure_ascii=False), flush=True)
    finally:
        br.close()

n_pass = sum(1 for r in summary if r["ok"])
print(f"\nPASSED {n_pass}/{len(summary)} (expected 4/5; T4a is the designed failure)")
pathlib.Path("driver_regression.json").write_text(json.dumps(summary, indent=1))
print("saved driver_regression.json")
