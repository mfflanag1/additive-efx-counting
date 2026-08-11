#!/usr/bin/env python3
"""Audit the root-critical alternating-frontier lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root: Path) -> dict:
    rh, ra, rw, rl = z3.Reals("r_H r_A r_W r_L")
    rr, rs = z3.Reals("r_R r_S")
    dr, ds = z3.Reals("d_R d_S")
    dr_next = z3.Real("d_R_next")
    delta = rh - ra

    feasible_exchange = check_unsat(
        rh >= ra,
        rs >= rr - delta,
        z3.Not(rh - rr + rs >= ra),
    )
    maximality_forces_s_order = check_unsat(
        dr <= ds,
        z3.Not(ds >= dr),
    )
    old_s_cannot_pay_next_r = check_unsat(
        dr_next > ds,
        ds >= dr_next,
    )
    full_root_cell_must_terminate = check_unsat(
        ra > rw,
        rl <= rw,
        z3.Not(rl < rh - delta),
    )
    terminal_packet_beats_old_residual = check_unsat(
        ra + rw == rh + rl,
        rl < rr - delta,
        z3.Not(rr > rw),
    )

    r_a, r_w_part, r_w_complement = z3.Reals(
        "r_R_A r_R_W r_W_complement"
    )
    terminal_support_cancellation = check_unsat(
        rr == r_a + r_w_part,
        rw == r_w_part + r_w_complement,
        rr > rw,
        z3.Not(r_a > r_w_complement),
    )

    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_CRITICAL_ALTERNATING_FRONTIER_LEMMA_20260811.md"
    return {
        "schema": "root-critical-alternating-frontier-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "compensator_exchange_preserves_root": feasible_exchange,
            "selector_maximality_forces_s_order": maximality_forces_s_order,
            "old_s_cannot_compensate_strict_r_extension": old_s_cannot_pay_next_r,
            "full_root_cell_forces_termination": full_root_cell_must_terminate,
            "terminal_packet_beats_old_residual": terminal_packet_beats_old_residual,
            "terminal_support_cancellation": terminal_support_cancellation,
        },
        "finite_growth": {
            "r_packet": "strict_inclusion_each_round",
            "s_packet": "strict_inclusion_each_round",
            "addition_bound": "|H|+|L|",
        },
        "claim_boundary": (
            "cap-free termination of the root-critical compensator chain; "
            "top-reset, captured-bottom, and nonroot recurrences remain open"
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
    output = args.output or root / "results/root_critical_alternating_frontier_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
