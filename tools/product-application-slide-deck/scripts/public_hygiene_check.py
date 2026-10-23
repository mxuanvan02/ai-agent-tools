#!/usr/bin/env python3
"""Public hygiene check for product-application-slide-deck skill."""

import sys
import subprocess
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists."""
    if path.exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} NOT FOUND")
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
            print(f"✓ Compiles: {script_path}")
            return True
        else:
            print(f"✗ Syntax error in {script_path}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"✗ Failed to check {script_path}: {e}")
        return False


def main():
    """Run all hygiene checks."""
    skill_dir = Path(__file__).parent.parent
    print(f"Running hygiene checks for: {skill_dir.name}")
    print("=" * 60)

    all_passed = True

    # Check required files exist
    required_files = [
        (skill_dir / "SKILL.md", "Skill documentation"),
        (skill_dir / "README.md", "User documentation"),
        (skill_dir / "scripts" / "validate_deck.py", "Validation script"),
        (skill_dir / "scripts" / "create_product_deck.py", "Template script"),
        (skill_dir / "tests" / "test_validate_deck.py", "Test suite"),
    ]

    print("\n1. Checking required files...")
    for path, description in required_files:
        if not check_file_exists(path, description):
            all_passed = False

    # Check scripts compile
    print("\n2. Checking script compilation...")
    scripts = [
        skill_dir / "scripts" / "validate_deck.py",
        skill_dir / "scripts" / "create_product_deck.py",
        skill_dir / "tests" / "test_validate_deck.py",
    ]

    for script in scripts:
        if script.exists() and not check_script_compiles(script):
            all_passed = False

    # Check SKILL.md has required sections
    print("\n3. Checking SKILL.md structure...")
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()
        required_sections = [
            "## Purpose",
            "## When to Use",
            "## Workflow",
            "## Scripts",
            "## Design Principles",
            "## Honest Boundaries",
        ]
        for section in required_sections:
            if section in content:
                print(f"✓ Found section: {section}")
            else:
                print(f"✗ Missing section: {section}")
                all_passed = False
    else:
        print("✗ SKILL.md not found")
        all_passed = False

    # Check README.md has required sections
    print("\n4. Checking README.md structure...")
    readme_md = skill_dir / "README.md"
    if readme_md.exists():
        content = readme_md.read_text()
        required_sections = [
            "## Quick Start",
            "## Structure",
            "## Scripts",
            "## Design Principles",
            "## Honest Boundaries",
            "## Validation",
        ]
        for section in required_sections:
            if section in content:
                print(f"✓ Found section: {section}")
            else:
                print(f"✗ Missing section: {section}")
                all_passed = False
    else:
        print("✗ README.md not found")
        all_passed = False

    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All hygiene checks passed")
        return 0
    else:
        print("✗ Some hygiene checks failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
