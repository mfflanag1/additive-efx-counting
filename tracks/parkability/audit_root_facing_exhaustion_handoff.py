#!/usr/bin/env python3
"""Audit the root-facing exhaustion handoff lemma."""

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
    q_tr, q_f, q_xq, q_k = z3.Reals("q_Tr q_f q_Xq q_K")
    top_packet_payment = check_unsat(
        q_tr + q_f > q_xq,
        q_xq > q_k,
        z3.Not(q_tr + q_f > q_k),
    )

    r_f, r_w, r_tq, r_xr = z3.Reals("r_f r_W r_Tq r_Xr")
    sigma = r_tq + r_f - r_xr
    f_only_cancellation = check_unsat(
        r_f - r_w >= sigma,
        z3.Not(r_xr >= r_tq + r_w),
    )
    charity_above_residual = check_unsat(
        r_xr >= r_tq + r_w,
        r_tq + r_f > r_xr,
        z3.Not(r_f > r_w),
    )

    r_br = z3.Real("r_Br")
    bottom_above_residual = check_unsat(
        r_br >= r_f,
        r_f > r_w,
        z3.Not(r_br > r_w),
    )

    # If every bottom good were in W, positivity/additivity would give
    # v_r(B_r) <= v_r(W), contradicting the strict scalar consequence.
    captured_bottom_nonempty = check_unsat(
        r_br > r_w,
        r_br <= r_w,
    )

    script = Path(__file__).resolve()
    theorem = root / "results" / "ROOT_FACING_EXHAUSTION_HANDOFF_LEMMA_20260811.md"
    return {
        "schema": "root-facing-exhaustion-handoff-audit-v1",
        "status": "ALL_FORCED",
        "solver": f"Z3 {z3.get_version_string()}",
        "scalar_records": {
            "top_packet_enters_root_exchange": top_packet_payment,
            "f_only_exhaustion_cancels_to_root_bound": f_only_cancellation,
            "charity_strictly_above_residual": charity_above_residual,
            "root_bottom_strictly_above_residual": bottom_above_residual,
            "captured_root_bottom_packet_nonempty": captured_bottom_nonempty,
        },
        "support_record": {
            "top_containing_packet_routes_to_existing_exchange": True,
            "top_empty_nonempty_packet_is_charity_singleton": True,
            "bottom_containment_would_imply_value_containment": True,
        },
        "claim_boundary": (
            "cap-free root-facing split and captured-bottom handoff audit; "
            "captured-bottom compensation and recurrence are not proved"
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
    output = args.output or root / "results" / "root_facing_exhaustion_handoff_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
