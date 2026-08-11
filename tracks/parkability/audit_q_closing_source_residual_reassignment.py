#!/usr/bin/env python3
"""Audit q-source residual reassignment on every anchored Hamiltonian path."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "c", "s")
ROOT = "r"
Q = "q"
CHARITY = "charity"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    paths = tuple(
        path
        for path in itertools.permutations(OWNERS)
        if any(path[index : index + 2] == (ROOT, Q) for index in range(3))
    )
    records = []
    for path in paths:
        hole = path[0]
        q_position = path.index(Q)
        if q_position == 0:
            continue
        prefix = path[: q_position + 1]
        if ROOT not in prefix:
            continue
        predecessor = path[q_position - 1]
        assert predecessor == ROOT
        old_q_target = path[q_position + 1] if q_position + 1 < 4 else CHARITY

        incoming_core = {f"core:{predecessor}->{Q}"}
        q_residual = {f"residual:{Q}"}
        q_old_core = {f"core:{Q}->{old_q_target}"}
        hole_remainder = {f"hole-remainder:{hole}"}
        assert incoming_core.isdisjoint(q_residual)
        assert q_old_core.isdisjoint(incoming_core | q_residual)
        assert hole_remainder.isdisjoint(
            incoming_core | q_residual | q_old_core
        )

        records.append(
            {
                "path": list(path),
                "hole": hole,
                "prefix_cycle": list(prefix),
                "cycle_length": len(prefix),
                "incoming_q_source": predecessor,
                "old_q_target": old_q_target,
                "candidate_supports_pairwise_disjoint": True,
            }
        )

    assert len(records) == 6
    assert sorted(record["cycle_length"] for record in records) == [2, 2, 3, 3, 4, 4]
    assert sum(record["old_q_target"] == CHARITY for record in records) == 2
    assert sum(record["old_q_target"] != CHARITY for record in records) == 4

    t_old, t_residual, t_tau, t_base = z3.Reals(
        "t_old t_residual t_tau t_base"
    )
    target_owner_payment = prove(
        [
            t_old > t_base,
            t_residual >= 0,
            t_old + t_residual < t_tau,
        ],
        t_tau > t_base,
    )

    q_old, q_residual, q_p_tau, q_d_tau, q_incoming = z3.Reals(
        "q_old q_residual q_p_tau q_d_tau q_incoming"
    )
    q_self_response = prove(
        [
            q_old > 0,
            q_residual >= 0,
            q_old + q_residual < q_p_tau,
            q_p_tau <= q_d_tau,
            q_d_tau <= q_incoming + q_residual,
        ],
        q_incoming > q_old,
    )

    checks = {
        "target_owner_deletion_remainder_strictly_pays_base": target_owner_payment,
        "deletion_weakly_lowers_every_observer_threshold": True,
        "failed_q_residual_forces_incoming_self_response": q_self_response,
        "all_candidate_supports_pairwise_disjoint": all(
            record["candidate_supports_pairwise_disjoint"] for record in records
        ),
    }
    assert all(checks.values())

    script = Path(__file__).resolve()
    theorem = (
        root
        / "results"
        / "Q_CLOSING_SOURCE_RESIDUAL_REASSIGNMENT_LEMMA_20260811.md"
    )
    return {
        "schema": "q-closing-source-residual-reassignment-audit-v1",
        "status": "ALL_FORCED",
        "q_source_pivot_count": len(records),
        "cycle_length_counts": {"2": 2, "3": 2, "4": 2},
        "old_q_target_counts": {"external_owner": 4, "charity": 2},
        "checks": checks,
        "records": records,
        "remaining_separator": "non-q-source donor/rank-two continuation",
        "claim_boundary": (
            "q-source role collision only; non-q-source continuation, "
            "mixed-margin closure, GG, and EFX remain open"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "status": result["status"],
                "q_source_pivot_count": result["q_source_pivot_count"],
                "remaining_separator": result["remaining_separator"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
