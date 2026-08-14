#!/usr/bin/env python3
"""Audit the allocations and scalar admission in the R2 H-return relay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"


def edge_set(initial, final):
    holder = {good: owner for owner, goods in initial.items() for good in goods}
    destination = {good: owner for owner, goods in final.items() for good in goods}
    return sorted({
        (holder[good], destination[good])
        for good in holder if holder[good] != destination[good]
    })


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def run(root):
    support = {
        "r": {"a", "h"}, "q": {"q"}, "d": {"w"},
        "s": {"e"}, "charity": {"p"},
    }
    c_d = {
        "r": {"a"}, "q": {"q"}, "d": {"w", "h"},
        "s": {"e", "p"}, "charity": set(),
    }
    c_r = {
        "r": {"a", "h"}, "q": {"q"}, "d": {"w"},
        "s": {"e", "p"}, "charity": set(),
    }
    all_goods = set().union(*support.values())
    assert set().union(*c_d.values()) == all_goods
    assert set().union(*c_r.values()) == all_goods
    assert sum(map(len, c_d.values())) == len(all_goods)
    assert sum(map(len, c_r.values())) == len(all_goods)
    c_d_edges = edge_set(support, c_d)
    c_r_edges = edge_set(support, c_r)
    relay_edges = edge_set(c_d, c_r)
    assert c_d_edges == [("charity", "s"), ("r", "d")]
    assert c_r_edges == [("charity", "s")]
    assert relay_edges == [("d", "r")]

    cd_d, cr_d, base_d, h = z3.Reals("cd_d cr_d base_d h")
    capture = prove(
        [cd_d >= base_d, cr_d < base_d, h == cd_d - cr_d],
        h > cd_d - base_d,
    )
    root_before, root_after, root_h = z3.Reals(
        "root_before root_after root_h"
    )
    root_strict = prove(
        [root_h > 0, root_after == root_before + root_h],
        root_after > root_before,
    )
    assert capture and root_strict

    theorem = root / "results/R2_TWO_PROBE_H_RETURN_CLOSURE_THEOREM_20260814.md"
    payment = root / "results/ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "r2-two-probe-h-return-closure-audit-v1",
        "status": "CONDITIONAL_R2_H_RETURN_COMPOSITION_AUDIT_PASSED",
        "c_d_edges": [list(edge) for edge in c_d_edges],
        "c_r_edges": [list(edge) for edge in c_r_edges],
        "relay_from_c_d_to_c_r": {"packet": "H", "edge": "d->r"},
        "canonical_cancellation_of_relay_equals": "C_d",
        "checks": {
            "both_probes_complete_partitions": True,
            "c_d_uses_two_edges": True,
            "c_r_uses_one_edge": True,
            "only_incremental_change_is_whole_H_return": True,
            "unpaid_d_forces_strict_H_deficit_capture": capture,
            "root_strictly_improves_on_H_return": root_strict,
        },
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "dependencies": {
            str(theorem.relative_to(root)): hashlib.sha256(theorem.read_bytes()).hexdigest(),
            str(payment.relative_to(root)): hashlib.sha256(payment.read_bytes()).hexdigest(),
        },
        "source_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Checks exact allocations, edges, cancellation, and payment-capture "
            "algebra. It imports the proper-residual payment theorem and does "
            "not independently validate T_Ltimes or universal provenance."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(Path(__file__).resolve().parents[2])
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
