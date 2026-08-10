#!/usr/bin/env python3
"""Regression checks for the two-nonsingleton composition dependency map."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    dependencies = {
        "length_two": "TRAPPED_SOURCE_RETURN_LENGTH_TWO_CLOSURE_THEOREM.md",
        "length_three": "LENGTH_THREE_RESERVOIR_ORDER_ESCAPE_THEOREM.md",
        "adjacent": "ADJACENT_LARGE_GLOBAL_LEX_TARGET_20260809.md",
        "alternating": "ALTERNATING_GLOBAL_LEX_CAPFREE_THEOREM.md",
    }
    for filename in dependencies.values():
        assert (ROOT / "results" / filename).is_file(), filename

    adjacent = (ROOT / "results" / dependencies["adjacent"]).read_text()
    alternating = (ROOT / "results" / dependencies["alternating"]).read_text()
    length_two = (ROOT / "results" / dependencies["length_two"]).read_text()
    length_three = (ROOT / "results" / dependencies["length_three"]).read_text()
    assert "all twenty-four priority orders" in adjacent
    assert "There are 24 priority orders" in alternating
    assert "cannot have length two" in length_two
    assert "twenty-four aggregate allocation implications" in length_three

    composition = (
        ROOT / "results" / "TWO_NONSINGLETON_COMPOSITION_THEOREM_20260809.md"
    ).read_text()
    assert "four-agent EFX state cannot have exactly two nonsingleton bundles" in composition
    assert "conditional on item 2" not in composition

    classes = set()
    for length in (2, 3, 4):
        for second_target in range(1, length):
            if length == 2:
                classes.add("length_two")
            elif length == 3:
                classes.add("length_three")
            elif second_target in (1, 3):
                classes.add("adjacent")
            else:
                classes.add("alternating")
    assert classes == set(dependencies)
    print("two-nonsingleton composition dependency audit passed")


if __name__ == "__main__":
    main()
