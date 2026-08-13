#!/usr/bin/env python3
"""Symbolic/support audit of anchor trim versus whole-target response."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    x, k, e, h, j, kp, ep, d, c = z3.Reals(
        "x k e h j kp ep d c"
    )
    base = [
        x >= 0, h > 0, j > 0,
        k == h + kp, e == j + ep,
        d == h + j, c == kp + ep,
        k > x, e > x,
    ]
    symbolic = {
        "partition_identity": prove(base, k + e == d + c),
        "root_capture_when_complement_fails": prove(
            [*base, c <= x], d > x
        ),
        "old_trim_strict_margin": prove(
            [*base, kp > x], z3.And(kp > x, kp < k)
        ),
        "response_trim_strict_support": prove(
            [*base, ep > x], z3.And(ep > x, ep < e)
        ),
    }
    assert all(symbolic.values())

    # Atomic support audit for every nonempty intersection with each side.
    support_records = []
    K = {"k0", "k1"}
    E = {"e0", "e1"}
    B = K | E
    for h_mask in range(1, 4):
        H = {f"k{i}" for i in range(2) if h_mask >> i & 1}
        for j_mask in range(1, 4):
            J = {f"e{i}" for i in range(2) if j_mask >> i & 1}
            D = H | J
            C = B - D
            assert D.isdisjoint(C)
            assert D | C == B
            support_records.append({
                "H": sorted(H), "J": sorted(J),
                "D": sorted(D), "C": sorted(C),
                "whole_target": D == B,
                "proper_descent": D < B,
            })
    assert len(support_records) == 9
    assert sum(record["whole_target"] for record in support_records) == 1
    assert sum(record["proper_descent"] for record in support_records) == 8

    # A response extracted by global minimum cardinality from an unsafe
    # target is proper: the blocking observer desires a one-good deletion.
    target_size, response_size = z3.Ints("target_size response_size")
    proper = prove(
        [target_size >= 2, response_size <= target_size - 1],
        response_size < target_size,
    )
    assert proper

    theorem = root / "results/ANCHOR_TRIM_OR_WHOLE_TARGET_RESPONSE_LEMMA_20260813.md"
    contract = root / "results/PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "anchor-trim-or-whole-target-response-audit-v1",
        "status": "PROPER_RESPONSE_REDUCTION_VERIFIED_SUPERSEDED_BRANCHING",
        "symbolic_checks": symbolic,
        "support_records": support_records,
        "support_record_count": len(support_records),
        "proper_descent_count": sum(record["proper_descent"] for record in support_records),
        "whole_target_count": sum(record["whole_target"] for record in support_records),
        "wall_derived_response_is_proper": proper,
        "claim_boundary": (
            "properness and scalar partition verified; response-side safety "
            "branch used an unavailable post-handoff premise and is superseded"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "contract": str(contract.relative_to(root)),
            "contract_sha256": sha256(contract),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "proper_descent_count": result["proper_descent_count"],
        "whole_target_count": result["whole_target_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
