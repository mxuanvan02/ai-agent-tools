#!/usr/bin/env python3
"""Validate product application slide deck structure and bounds."""

import argparse
import sys
from pathlib import Path

try:
    from pptx import Presentation
    from pptx.util import Inches
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False


def validate_slide_count(pptx_path: Path, expected: int = 15) -> bool:
    """Check slide count matches expected."""
    p = Presentation(str(pptx_path))
    actual = len(p.slides)
    if actual != expected:
        print(f"FAIL: Expected {expected} slides, got {actual}")
        return False
    print(f"OK: {actual} slides")
    return True


def validate_bounds(pptx_path: Path) -> bool:
    """Check no elements exceed slide boundaries."""
    p = Presentation(str(pptx_path))
    W, H = p.slide_width, p.slide_height
    violations = []

    for i, slide in enumerate(p.slides, 1):
        for j, shape in enumerate(slide.shapes, 1):
            if shape.left < 0 or shape.top < 0:
                violations.append((i, j, "negative position"))
            if shape.left + shape.width > W:
                violations.append((i, j, "exceeds right edge"))
            if shape.top + shape.height > H:
                violations.append((i, j, "exceeds bottom edge"))

    if violations:
        print(f"FAIL: {len(violations)} bound violations:")
        for slide_idx, shape_idx, reason in violations[:10]:
            print(f"  Slide {slide_idx}, shape {shape_idx}: {reason}")
        return False

    print("OK: No bound violations")
    return True


def validate_aspect_ratios(pptx_path: Path) -> bool:
    """Check images preserve aspect ratios (no stretching)."""
    p = Presentation(str(pptx_path))
    warnings = []

    for i, slide in enumerate(p.slides, 1):
        for j, shape in enumerate(slide.shapes, 1):
            if shape.shape_type == 13:  # Picture
                # Check if image has both width and height set
                if hasattr(shape, 'image') and shape.image:
                    img = shape.image
                    orig_w = img.size[0]
                    orig_h = img.size[1]
                    orig_ratio = orig_w / orig_h

                    shape_w = shape.width / 914400  # EMU to inches
                    shape_h = shape.height / 914400
                    shape_ratio = shape_w / shape_h

                    # Allow 5% tolerance
                    if abs(orig_ratio - shape_ratio) / orig_ratio > 0.05:
                        warnings.append((i, j, f"ratio mismatch: {orig_ratio:.2f} vs {shape_ratio:.2f}"))

    if warnings:
        print(f"WARN: {len(warnings)} images may have distorted aspect ratios:")
        for slide_idx, shape_idx, msg in warnings[:5]:
            print(f"  Slide {slide_idx}, shape {shape_idx}: {msg}")
        # Not a hard failure, just warning
    else:
        print("OK: All images preserve aspect ratios")

    return True


def validate_speaker_notes(pptx_path: Path) -> bool:
    """Check slides have speaker notes."""
    p = Presentation(str(pptx_path))
    slides_without_notes = []

    for i, slide in enumerate(p.slides, 1):
        notes_slide = slide.notes_slide
        notes_text = notes_slide.notes_text_frame.text.strip()
        if not notes_text:
            slides_without_notes.append(i)

    if slides_without_notes:
        print(f"WARN: Slides without speaker notes: {slides_without_notes}")
        return False

    print(f"OK: All {len(p.slides)} slides have speaker notes")
    return True


def main():
    parser = argparse.ArgumentParser(description="Validate product application slide deck")
    parser.add_argument("pptx_path", type=Path, help="Path to PPTX file")
    parser.add_argument("--expected-slides", type=int, default=15, help="Expected slide count")
    parser.add_argument("--bounds", action="store_true", help="Check element bounds")
    parser.add_argument("--aspect-ratios", action="store_true", help="Check image aspect ratios")
    parser.add_argument("--notes", action="store_true", help="Check speaker notes")
    parser.add_argument("--all", action="store_true", help="Run all validations")

    args = parser.parse_args()

    if not HAS_PPTX:
        print("ERROR: python-pptx not installed. Run: pip install python-pptx", file=sys.stderr)
        sys.exit(1)

    if not args.pptx_path.exists():
        print(f"ERROR: File not found: {args.pptx_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Validating: {args.pptx_path}")
    print("-" * 60)

    all_passed = True

    # Always check slide count
    if not validate_slide_count(args.pptx_path, args.expected_slides):
        all_passed = False

    # Check bounds if requested
    if args.bounds or args.all:
        if not validate_bounds(args.pptx_path):
            all_passed = False

    # Check aspect ratios if requested
    if args.aspect_ratios or args.all:
        validate_aspect_ratios(args.pptx_path)  # Warning only

    # Check speaker notes if requested
    if args.notes or args.all:
        if not validate_speaker_notes(args.pptx_path):
            all_passed = False

    print("-" * 60)
    if all_passed:
        print("RESULT: PASS")
        sys.exit(0)
    else:
        print("RESULT: FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
