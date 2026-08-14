#!/usr/bin/env python3
"""Audit the exact scalar model realizing both d-capture inequalities."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/DUAL_D_CAPTURE_SCALAR_COMPATIBILITY_NO_GO_20260813.md"
OUTPUT = ROOT / "results/dual_d_capture_scalar_compatibility_audit.json"


def run(output: Path = OUTPUT):
    values = {
        "floor": Fraction(1),
        "w": Fraction(3, 5),
        "charity": Fraction(1, 10),
        "q_good_1": Fraction(3, 5),
        "q_good_2": Fraction(3, 5),
        "current_root_core": Fraction(7, 10),
        "retained_root": Fraction(1, 2),
    }
    q = values["q_good_1"] + values["q_good_2"]
    q_tail = q - min(values["q_good_1"], values["q_good_2"])
    q_margin = q - values["floor"]
    retained_q = q
    root_final = (
        values["w"] + values["current_root_core"]
        - values["retained_root"] + values["charity"]
    )
    checks = {
        "q_is_base_desired": q > values["floor"],
        "q_tail_equals_w": q_tail == values["w"],
        "w_above_half_floor": 2 * values["w"] > values["floor"],
        "current_root_core_above_w": values["current_root_core"] > values["w"],
        "base_q_capture": retained_q > q_margin + values["w"] + values["charity"],
        "current_root_terminal_underpaid": root_final < values["floor"],
        "current_root_capture": values["retained_root"] > (
            values["w"] + values["current_root_core"]
            + values["charity"] - values["floor"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    floor, w, charity, q1, q2, current, retained = z3.Reals(
        "floor w charity q1 q2 current retained"
    )
    solver = z3.SolverFor("QF_LRA")
    exact = (floor, w, charity, q1, q2, current, retained)
    fractions = tuple(values[key] for key in (
        "floor", "w", "charity", "q_good_1", "q_good_2",
        "current_root_core", "retained_root",
    ))
    for variable, amount in zip(exact, fractions, strict=True):
        solver.add(variable == z3.RealVal(f"{amount.numerator}/{amount.denominator}"))
    solver.add(
        q1 + q2 > floor,
        w == q1,
        2 * w > floor,
        current > w,
        q1 + q2 > (q1 + q2 - floor) + w + charity,
        w + current - retained + charity < floor,
        retained > w + current + charity - floor,
    )
    status = solver.check()
    if status != z3.sat:
        raise AssertionError(status)

    result = {
        "schema": "dual-d-capture-scalar-compatibility-audit-v1",
        "status": "SAT_EXACT_SCALAR_MODEL",
        "solver": f"Z3 {z3.get_version_string()}",
        "values": {key: str(value) for key, value in values.items()},
        "derived": {
            "q_total": str(q),
            "q_tail": str(q_tail),
            "q_margin": str(q_margin),
            "current_branch_final_d_value": str(root_final),
        },
        "checks": checks,
        "claim_boundary": (
            "Exact one-row scalar compatibility witness only. It is not a "
            "four-owner valuation profile, saturated state, or EFX countermodel."
        ),
        "theorem": str(THEOREM.relative_to(ROOT)),
        "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        "source": str(Path(__file__).resolve().relative_to(ROOT)),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
