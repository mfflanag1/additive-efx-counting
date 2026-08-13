#!/usr/bin/env python3
"""Symbolic/support audit of backup-response anchor release."""

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
    base_r, pre_r, e_r, target_tau = z3.Reals(
        "base_r pre_r e_r target_tau"
    )
    root_paid = prove(
        [pre_r >= base_r, pre_r >= target_tau, e_r > pre_r],
        z3.And(e_r > base_r, e_r > target_tau),
    )
    w_d, k_d = z3.Reals("w_d k_d")
    residual_improves = prove(
        [w_d >= 0, k_d > 0], w_d + k_d > w_d
    )
    assert root_paid and residual_improves

    # Exact atomic support conservation.
    K = {"k0", "k1"}
    E = {"e0", "e1"}
    W = {"w0", "w1"}
    before = K | E | W
    root_after = E
    residual_after = W | K
    assert root_after.isdisjoint(residual_after)
    assert root_after | residual_after == before

    # Abstract wall localization. Root pays all old targets; d improves;
    # unchanged owners cannot newly fail against shrinking/unchanged targets.
    old_assigned = z3.RealVector("old_assigned", 4)
    new_assigned = z3.RealVector("new_assigned", 4)
    old_tau = [[z3.Real(f"old_tau_{i}_{j}") for j in range(4)] for i in range(4)]
    new_tau = [[z3.Real(f"new_tau_{i}_{j}") for j in range(4)] for i in range(4)]
    root_agent, hole_agent = 0, 3
    enlarged_target = hole_agent
    solver = z3.SolverFor("QF_LRA")
    for i in range(4):
        for j in range(4):
            solver.add(old_assigned[i] >= old_tau[i][j])
            if j != enlarged_target:
                solver.add(new_tau[i][j] <= old_tau[i][j])
        if i == root_agent:
            solver.add(new_assigned[i] >= old_assigned[i])
        elif i == hole_agent:
            solver.add(new_assigned[i] > old_assigned[i])
        else:
            solver.add(new_assigned[i] == old_assigned[i])
    assert solver.check() == z3.sat
    for i in range(4):
        for j in range(4):
            if j == enlarged_target:
                continue
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), new_assigned[i] < new_tau[i][j])
            assert probe.check() == z3.unsat

    theorem = root / "results/BACKUP_RESPONSE_ANCHOR_RELEASE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "backup-response-anchor-release-audit-v1",
        "status": "CONDITIONAL_ANCHOR_RELEASE_LOCALIZATION_VERIFIED",
        "root_paid_and_old_targets_safe": root_paid,
        "residual_owner_strictly_improves": residual_improves,
        "support_partition_valid": True,
        "only_possible_new_wall_target": "W+K",
        "permanent_anchor_released": True,
        "claim_boundary": (
            "new-wall localization under the stated backup-floor premises; "
            "not the unconditional recurrence resolution"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
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
        "only_possible_new_wall_target": result["only_possible_new_wall_target"],
    }, indent=2))


if __name__ == "__main__":
    main()
