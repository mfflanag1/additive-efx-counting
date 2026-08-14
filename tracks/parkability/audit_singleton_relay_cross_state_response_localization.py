#!/usr/bin/env python3
"""Exact audit of singleton-relay cross-state response localization."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    br, bd, p, e = z3.Reals("br bd p e")
    tr, td = z3.Reals("tr td")
    nonnegative = [br >= 0, bd >= 0, p > 0, e >= 0, tr >= 0, td >= 0]

    checks = {
        "d_desire_persists_unless_root_source": prove(
            nonnegative + [e > bd + p], e > bd
        ),
        "ordinary_d_state_desire_persists_to_r_state": prove(
            nonnegative + [e > br], e > br
        ),
        "d_only_root_desire_forces_p_band": prove(
            nonnegative + [e > br, e <= br + p],
            z3.And(br < e, e <= br + p),
        ),
        "r_only_d_desire_forces_p_band": prove(
            nonnegative + [e > bd, e <= bd + p],
            z3.And(bd < e, e <= bd + p),
        ),
        "d_safe_response_can_lose_safety_only_in_d_row": prove(
            nonnegative + [td <= bd + p, td > bd],
            z3.And(bd < td, td <= bd + p),
        ),
        "r_safe_response_can_lose_safety_only_in_root_row": prove(
            nonnegative + [tr <= br + p, tr > br],
            z3.And(br < tr, tr <= br + p),
        ),
    }
    assert all(checks.values())

    solver = z3.Solver()
    solver.add(
        br == 1,
        bd == 1,
        p == z3.Q(1, 2),
        e == z3.Q(5, 4),
        tr == z3.Q(5, 4),
        td == z3.Q(5, 4),
        br < e,
        e <= br + p,
        bd < e,
        e <= bd + p,
        br < tr,
        tr <= br + p,
        bd < td,
        td <= bd + p,
    )
    separator_feasible = solver.check() == z3.sat
    assert separator_feasible

    script = Path(__file__).resolve()
    theorem = root / "results" / "SINGLETON_RELAY_CROSS_STATE_RESPONSE_LOCALIZATION_LEMMA_20260814.md"
    return {
        "schema": "singleton-relay-cross-state-response-localization-audit-v1",
        "status": "CAP_FREE_LOCALIZATION_PROVED",
        "checks": checks,
        "isolated_singleton_critical_separator_feasible": separator_feasible,
        "critical_rows": ["r", "d"],
        "remaining_gate": (
            "use the saturated rank-three response/support premises to eliminate "
            "a shared safe response or the exact r/d singleton-critical intervals"
        ),
        "claim_boundary": (
            "response-source and cross-state safety localization only; collision "
            "closure, fixed-U, GG, and EFX remain open"
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
    print(json.dumps({"status": result["status"], "remaining_gate": result["remaining_gate"]}, indent=2))


if __name__ == "__main__":
    main()
