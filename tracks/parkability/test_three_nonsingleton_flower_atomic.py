#!/usr/bin/env python3
"""Regression checks for the additive and true-tail flower frontiers."""

from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_additive_low_wall import run as run_additive
    from .decide_three_nonsingleton_flower_atomic_low_wall import run as run_atomic
    from .analyze_three_nonsingleton_flower_atomic_witness import run as run_witness
except ImportError:
    from decide_three_nonsingleton_flower_additive_low_wall import run as run_additive
    from decide_three_nonsingleton_flower_atomic_low_wall import run as run_atomic
    from analyze_three_nonsingleton_flower_atomic_witness import run as run_witness


ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    additive = run_additive()
    assert additive["status"] == "COMPLETE"
    assert additive["counts"] == {"IMPOSSIBLE": 148, "sat": 284, "unknown": 0}

    atomic = run_atomic()
    assert atomic["status"] == "COMPLETE"
    assert atomic["counts"] == {"IMPOSSIBLE": 316, "sat": 116, "unknown": 0}
    witnesses = [record for record in atomic["records"] if "component_values" in record]
    assert len(witnesses) == 1
    assert witnesses[0]["status"] == "sat"

    witness_path = ROOT / "results" / "three_nonsingleton_flower_atomic_low_wall_audit.json"
    analysis = run_witness(witness_path)
    assert analysis["nearest_partial_improvement"]["status"] == "SAT"
    assert analysis["nearest_partial_improvement"]["minimum_moved_goods"] == 2
    assert analysis["nearest_complete_improvement"]["status"] == "SAT"
    assert analysis["nearest_complete_improvement"]["minimum_moved_goods"] == 3
    print("three-nonsingleton flower atomic tests passed")


if __name__ == "__main__":
    main()
