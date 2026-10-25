#!/usr/bin/env python3
"""Structure check for the product-application-slide-deck tool.

This is the tool's OWN housekeeping check: it verifies that the files this skill
needs are present, that the scripts compile, and that the documentation still
carries the sections the workflow depends on.

It is NOT the public-hygiene gate. That gate is repository-wide infrastructure
and ships byte-identically in every tool; it scans for tokens that must never
appear in a public repository. A tool that keeps its own script under the gate's
filename gets a check that means something different from its neighbours', and
"a tool with no gate is a tool CI never inspects" becomes true for a tool that
thinks it is protected.

Exit 0 = clean, exit 1 = findings printed.
"""
import sys
import subprocess
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parents[1]


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    if path.exists():
        print(f"[ok] {description}: {path}")
        return True
    print(f"[FAIL] {description}: {path} NOT FOUND")
    return False


def check_script_compiles(script_path: Path) -> bool:
    """Check if a Python script compiles without syntax errors."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"[ok] Compiles: {script_path}")
            return True
        print(f"[FAIL] Syntax error in {script_path}:")
        print(result.stderr)
        return False
    except Exception as e:
        print(f"[FAIL] Failed to check {script_path}: {e}")
        return False


def check_sections(path: Path, sections: list[str]) -> bool:
    """Check that a documentation file still carries the required sections."""
    if not path.exists():
        print(f"[FAIL] {path.name} not found")
        return False
    content = path.read_text(encoding="utf-8")
    ok = True
    for section in sections:
        if section in content:
            print(f"[ok] Found section in {path.name}: {section}")
        else:
            print(f"[FAIL] Missing section in {path.name}: {section}")
            ok = False
    return ok


def main() -> int:
    """Run all structure checks."""
    print(f"Running structure checks for: {TOOL_DIR.name}")
    print("=" * 60)

    all_passed = True

    print("\n1. Checking required files...")
    required_files = [
        (TOOL_DIR / "SKILL.md", "Skill documentation"),
        (TOOL_DIR / "README.md", "User documentation"),
        (TOOL_DIR / "scripts" / "validate_deck.py", "Validation script"),
        (TOOL_DIR / "scripts" / "create_product_deck.py", "Template script"),
        (TOOL_DIR / "scripts" / "check_structure.py", "Structure check"),
        (TOOL_DIR / "tests" / "test_validate_deck.py", "Test suite"),
    ]
    for path, description in required_files:
        if not check_file_exists(path, description):
            all_passed = False

    print("\n2. Checking script compilation...")
    scripts = [
        TOOL_DIR / "scripts" / "validate_deck.py",
        TOOL_DIR / "scripts" / "create_product_deck.py",
        TOOL_DIR / "scripts" / "check_structure.py",
        TOOL_DIR / "tests" / "test_validate_deck.py",
    ]
    for script in scripts:
        if script.exists() and not check_script_compiles(script):
            all_passed = False

    print("\n3. Checking SKILL.md structure...")
    if not check_sections(TOOL_DIR / "SKILL.md", [
        "## Purpose",
        "## When to Use",
        "## Workflow",
        "## Scripts",
        "## Design Principles",
        "## Honest Boundaries",
    ]):
        all_passed = False

    print("\n4. Checking README.md structure...")
    if not check_sections(TOOL_DIR / "README.md", [
        "## Quick Start",
        "## Structure",
        "## Scripts",
        "## Design Principles",
        "## Honest Boundaries",
        "## Validation",
    ]):
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("[ok] All structure checks passed")
        return 0
    print("[FAIL] Some structure checks failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
