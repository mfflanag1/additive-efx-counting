#!/usr/bin/env python3
"""Audit the root-monopoly complement escape."""

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
    r_kt, r_kb, r_tr_tail, r_br = z3.Reals(
        "r_KT r_KB r_Tr_tail r_Br"
    )
    root_capture = check_unsat(
        r_kt + r_kb > r_kt + r_tr_tail + r_br,
        r_tr_tail >= 0,
        r_br > 0,
        z3.Not(z3.And(r_kb > r_tr_tail + r_br, r_kb > r_br)),
    )

    r_tr, r_bq, r_base = z3.Reals("r_Tr r_Bq r_base")
    root_target_below_double_base = check_unsat(
        r_tr < r_base,
        r_bq <= r_base,
        z3.Not(r_tr + r_bq < 2 * r_base),
    )

    r_d, r_e, r_u = z3.Reals("r_D r_E r_U")
    repeated_root_source_impossible = check_unsat(
        r_d > r_base,
        r_e > r_base,
        r_u >= r_d + r_e,
        r_u < 2 * r_base,
    )

    q_u, q_o, q_base = z3.Reals("q_U q_O q_base")
    q_d = q_u - q_o
    terminal_q_capture = check_unsat(
        q_u > q_base,
        q_o <= q_base,
        z3.Not(z3.And(q_d >= q_u - q_base, q_d > 0)),
    )

    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_MONOPOLY_COMPLEMENT_ESCAPE_LEMMA_20260811.md"
    return {
        "schema": "root-monopoly-complement-escape-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "root_capture_cancels_selected_top": root_capture,
            "base_efx_bounds_live_target_below_twice_root_base": (
                root_target_below_double_base
            ),
            "two_disjoint_root_desired_cores_are_impossible": (
                repeated_root_source_impossible
            ),
            "terminal_core_captures_q_target_surplus": terminal_q_capture,
        },
        "support_record": {
            "D_and_O_disjoint": True,
            "D_union_O": "T_r+B_q",
            "complement_desired_outcome": "nonroot response source restores rank two",
            "complement_inactive_outcome": "two-row bottom-capture polarity",
        },
        "claim_boundary": (
            "cap-free termination of repeated root monopoly; terminal "
            "two-row bottom-capture compensation is not proved"
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
    output = args.output or root / "results/root_monopoly_complement_escape_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
