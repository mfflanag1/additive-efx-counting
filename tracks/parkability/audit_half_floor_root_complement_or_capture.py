#!/usr/bin/env python3
"""Independent audit of the half-floor root complement/capture fork."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/HALF_FLOOR_ROOT_COMPLEMENT_OR_CAPTURE_LEMMA_20260813.md"
OUTPUT = ROOT / "results/half_floor_root_complement_or_capture_audit.json"


def unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    if status != z3.unsat:
        raise AssertionError(f"expected UNSAT, got {status}")
    return "unsat"


def run(output: Path = OUTPUT):
    floor, w, a, c, remainder = z3.Reals("floor w a c remainder")
    common = (
        floor > 0,
        2 * w > floor,
        a > w,
        c >= 0,
        remainder >= 0,
        a == c + remainder,
        w + remainder < floor,
    )
    capture = unsat(*common, c <= a + w - floor)
    positive_slack = unsat(*common, c <= 2 * w - floor)

    observer_floor, a_i, removed_i, remainder_i = z3.Reals(
        "observer_floor a_i removed_i remainder_i"
    )
    safety = unsat(
        observer_floor > 0,
        removed_i >= 0,
        remainder_i <= a_i - removed_i,
        a_i - removed_i <= observer_floor,
        remainder_i > observer_floor,
    )

    result = {
        "schema": "half-floor-root-complement-or-capture-audit-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "checks": {
            "failed_complement_payment_forces_exact_capture": capture,
            "capture_strictly_exceeds_positive_half_floor_slack": positive_slack,
            "proper_root_complement_is_full_value_base_safe": safety,
        },
        "claim_boundary": (
            "Cap-free exact split/capture fork. It does not compress two root "
            "recipient edges into the four-edge endpoint, prove safety of the "
            "enlarged W+R target, or finish complete EFX."
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
