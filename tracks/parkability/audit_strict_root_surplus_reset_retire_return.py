#!/usr/bin/env python3
"""Independent audit of the strict-root surplus reset/retire/return lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/STRICT_ROOT_SURPLUS_RESET_RETIRE_RETURN_CLOSURE_THEOREM_20260814.md"
COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"


def _allocation_audit():
    current = {
        "r": {"A", "H"},
        "q": {"Q"},
        "d": {"W"},
        "s": {"E"},
        "charity": {"P"},
    }
    c_d = {
        "r": {"A"},
        "q": {"Q"},
        "d": {"W", "H", "P"},
        "s": {"E"},
        "charity": set(),
    }
    c_r = {
        "r": {"A", "H"},
        "q": {"Q"},
        "d": {"W", "P"},
        "s": {"E"},
        "charity": set(),
    }

    goods = set().union(*current.values())
    for allocation in (current, c_d, c_r):
        assert set().union(*allocation.values()) == goods
        assert sum(map(len, allocation.values())) == len(goods)

    def edges(source, target):
        holder = {good: owner for owner, bundle in source.items() for good in bundle}
        return sorted(
            (holder[good], owner, good)
            for owner, bundle in target.items()
            for good in bundle
            if holder[good] != owner
        )

    assert edges(current, c_d) == [("charity", "d", "P"), ("r", "d", "H")]
    assert edges(current, c_r) == [("charity", "d", "P")]
    assert edges(c_d, c_r) == [("d", "r", "H")]
    assert c_d["r"] & c_r["r"] == {"A"}
    return current, c_d, c_r


def _linear_audit():
    x, a, h = z3.Reals("x a h")
    root = z3.SolverFor("QF_LRA")
    root.add(x >= 0, a > x, h > 0, z3.Or(a <= x, a + h <= x))
    root_status = str(root.check())
    assert root_status == "unsat"

    w_d, p_d, h_d, floor_d, returned_d = z3.Reals(
        "w_d p_d h_d floor_d returned_d"
    )
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        w_d > 0,
        h_d > 0,
        p_d >= 0,
        floor_d == w_d + h_d + p_d,
        returned_d == w_d + p_d,
        z3.Or(
            returned_d >= floor_d,
            floor_d - returned_d != h_d,
            floor_d - returned_d <= 0,
        ),
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"
    return root_status, capture_status


def run(output: Path):
    _allocation_audit()
    root_status, capture_status = _linear_audit()
    result = {
        "schema": "strict-root-surplus-reset-retire-return-audit-v1",
        "status": "CONDITIONAL_AUDIT_PASSED",
        "physical_conservation": True,
        "current_to_first_probe_edges": [["charity", "d"], ["r", "d"]],
        "current_to_second_probe_edges": [["charity", "d"]],
        "first_to_second_probe_edge": [["d", "r"]],
        "maximum_endpoint_edge_count": 2,
        "canonical_cancellation_restores_first_probe": True,
        "permanent_anchor_support": "A",
        "strict_root_negation_status": root_status,
        "reset_floor_capture_negation_status": capture_status,
        "retired_packet_nonempty": True,
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Checks the exact allocation, edge, strict-root, reset-payment, "
            "deficit-capture, and cancellation identities. It does not prove "
            "that every fixed-U state has detachable strict-root surplus, "
            "independently certify floor-reset admission, or reprove the "
            "imported collision theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
