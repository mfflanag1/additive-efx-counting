#!/usr/bin/env python3
"""Independent exact audit of the half-floor current-wall lift."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/HALF_FLOOR_CURRENT_WALL_LIFT_LEMMA_20260813.md"
OUTPUT = ROOT / "results/half_floor_current_wall_lift_audit.json"


def prove_unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    verdict = solver.check()
    if verdict != z3.unsat:
        raise AssertionError(f"expected UNSAT, obtained {verdict}")
    return "unsat"


def run(output: Path = OUTPUT):
    # A least positive good in a bundle of cardinality at least two has value
    # at most half of the bundle total.  q_min is the least-good value and
    # q_rest is the value of the remaining nonempty packet.
    floor, q_min, q_rest, w, root_tail = z3.Reals(
        "floor q_min q_rest w root_tail"
    )
    common = (
        floor > 0,
        q_min > 0,
        q_rest > 0,
        q_min <= q_rest,
        q_min + q_rest > floor,
        w >= q_rest,
        root_tail > w,
    )
    half_floor = prove_unsat(*common, 2 * w <= floor)
    base_payment = prove_unsat(*common, w + root_tail <= floor)

    # Cross-observer packet safety.  g is the d-least root good, while
    # observer_min is the potentially different least good in observer i's
    # row.  Since every actual good is at least observer_min, deleting g gives
    # no more value than deleting observer_min.
    observer_floor, root_total, observer_min, g_value = z3.Reals(
        "observer_floor root_total observer_min g_value"
    )
    observer_safety = prove_unsat(
        observer_floor > 0,
        observer_min >= 0,
        g_value >= observer_min,
        root_total - observer_min <= observer_floor,
        root_total - g_value > observer_floor,
    )

    result = {
        "schema": "half-floor-current-wall-lift-audit-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "checks": {
            "nonsingleton_tail_forces_w_above_half_floor": half_floor,
            "retained_w_plus_root_tail_strictly_base_pays_d": base_payment,
            "d_least_deletion_is_full_value_base_safe_for_every_observer": observer_safety,
        },
        "claim_boundary": (
            "Cap-free exact payment and packet-safety lemma. It does not prove "
            "observer safety of the enlarged W+(A-g) target, disjointness of "
            "the singleton-Q branch, complete EFX, or the universal theorem."
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
