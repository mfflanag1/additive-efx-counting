#!/usr/bin/env python3
"""Audit Hall-menu coverage and reject vacuous fixed-U finite decisions."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_external_hall_star_fork_menu import menu
    from .run_fixed_u_full_packet_terminal_cegar import BASE
    from .run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from .run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )
except ImportError:
    from decide_external_hall_star_fork_menu import menu
    from run_fixed_u_full_packet_terminal_cegar import BASE
    from run_fixed_u_rank_three_relation_cegar import build_rank_three_master
    from run_full_capture_rank_three_cegar import (
        generalized_self_pi_free_constraints, ordinary_pi_free_constraints,
    )


EXPECTED = {
    0: {"star_signatures": 15, "fork_signatures": 78,
        "star_topologies": 13, "fork_topologies": 46, "union_topologies": 53},
    2: {"star_signatures": 15, "fork_signatures": 78,
        "star_topologies": 15, "fork_topologies": 60, "union_topologies": 60},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def legacy_premise_status(form_index: int, include_generalized_self: bool) -> str:
    solver, value = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
        owner_cycle_form_index=form_index,
    )
    solver.add(*ordinary_pi_free_constraints(value, BASE))
    if include_generalized_self:
        solver.add(*generalized_self_pi_free_constraints(value, BASE))
    return str(solver.check())


def run(root: Path) -> dict:
    forms = {}
    for form_index in (0, 2):
        union, star, fork, star_records, fork_records = menu(form_index)
        counts = {
            "star_signatures": len(star_records),
            "fork_signatures": len(fork_records),
            "star_topologies": len(star),
            "fork_topologies": len(fork),
            "union_topologies": len(union),
        }
        assert counts == EXPECTED[form_index]
        assert all(len(topology) <= 4 for topology in union)
        ordinary_status = legacy_premise_status(form_index, False)
        full_status = legacy_premise_status(form_index, True)
        assert ordinary_status == "sat"
        assert full_status == "unsat"
        forms[str(form_index)] = {
            **counts,
            "ordinary_pi_premise_status": ordinary_status,
            "with_generalized_self_pi_premise_status": full_status,
            "menu_theorem_nonvacuous_under_full_pi": False,
        }

    script = Path(__file__).resolve()
    decision = root / "tracks" / "parkability" / "decide_external_hall_star_fork_menu.py"
    theorem = root / "results" / "EXTERNAL_HALL_FINITE_DECISION_NONVACUITY_GATE_20260814.md"
    return {
        "schema": "external-hall-finite-decision-nonvacuity-audit-v1",
        "status": "LEGACY_FULL_PI_MENU_DECISION_VACUOUS",
        "forms": forms,
        "live_analytic_gate": (
            "cap-free alternating external-Hall closure-or-cancellation: every "
            "overflowing mixed core must give new signed support, close a physical "
            "PI family, or reach a star/fork edge-cancelling endpoint"
        ),
        "claim_boundary": (
            "exact menu and legacy-master nonvacuity audit only; it neither decides "
            "the repaired allocated-support cell nor proves the cap-free fixed-U theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "decision_driver": str(decision.relative_to(root)),
            "decision_driver_sha256": sha256(decision),
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
    print(json.dumps({"status": result["status"], "forms": result["forms"]}, indent=2))


if __name__ == "__main__":
    main()
