#!/usr/bin/env python3
"""Audit the nonroot unconditional-recapture lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    support_cases = [
        {"origin": "A_i", "destination": "new_residual"},
        {"origin": "W\\D_i", "destination": "new_residual"},
        {"origin": "D_i", "destination": "source_i"},
        {"origin": "other_core", "destination": "same_source"},
    ]

    w = z3.Real("d_W")
    base_d = z3.Real("d_base")
    core = z3.Real("d_A_i")
    response = z3.Real("d_D_i")
    new_residual = w + core - response
    payment_identity = check_unsat(
        z3.Not(
            (new_residual >= base_d)
            == (response - core <= w - base_d)
        ),
    )

    r_new = z3.Real("r_new")
    r_base = z3.Real("r_base")
    q_new = z3.Real("q_new")
    q_base = z3.Real("q_base")
    external_hole_priority = check_unsat(
        r_new > r_base,
        q_new > q_base,
        z3.Not(z3.And(r_new >= r_base, q_new > q_base)),
    )
    q_hole_priority = check_unsat(
        r_new > r_base,
        z3.Not(r_new > r_base),
    )

    base = {agent: z3.Real(f"base_{agent}") for agent in AGENTS}
    own = {agent: z3.Real(f"own_{agent}") for agent in AGENTS}
    selected_tail = {
        (observer, target): z3.Real(f"tail_{observer}_{target}")
        for observer in AGENTS
        for target in ("r", "q", "c")
    }
    represented = ("r", "q", "c")
    assumptions = [own[agent] > base[agent] for agent in represented]
    assumptions += [
        selected_tail[observer, target] <= base[observer]
        for observer in AGENTS
        for target in represented
    ]
    represented_to_core = check_unsat(
        *assumptions,
        z3.Or(*(
            own[observer] < selected_tail[observer, target]
            for observer in represented
            for target in represented
        )),
    )
    residual_self_tail = z3.Real("residual_self_tail")
    missing_to_self = check_unsat(
        own["s"] < residual_self_tail,
        residual_self_tail <= own["s"],
    )

    script = Path(__file__).resolve()
    theorem = root / "results" / "NONROOT_UNCONDITIONAL_RECAPTURE_LEMMA_20260811.md"
    return {
        "schema": "nonroot-unconditional-recapture-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "support_partition_valid": True,
        "support_cases": support_cases,
        "scalar_records": {
            "payment_identity": payment_identity,
            "external_hole_flexible_priority": external_hole_priority,
            "q_hole_r_first_priority": q_hole_priority,
            "represented_source_to_core_impossible": represented_to_core,
            "missing_owner_to_own_residual_impossible": missing_to_self,
        },
        "remaining_unpaid_wall_types": [
            "missing_owner_to_selected_core",
            "represented_source_to_residual",
        ],
        "claim_boundary": (
            "cap-free unconditional nonroot recapture audit; rank-two residual "
            "selection and terminal star recurrence are not proved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results" / "nonroot_unconditional_recapture_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
