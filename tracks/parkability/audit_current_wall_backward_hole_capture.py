#!/usr/bin/env python3
"""Independent exact audit of current-wall backward-hole termination."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/CURRENT_WALL_BACKWARD_HOLE_CAPTURE_LEMMA_20260813.md"
OUTPUT = ROOT / "results/current_wall_backward_hole_capture_audit.json"


def unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    if status != z3.unsat:
        raise AssertionError(f"expected UNSAT, got {status}")
    return "unsat"


def run(output: Path = OUTPUT):
    floor, w, incoming, charity, retained = z3.Reals(
        "floor w incoming charity retained"
    )
    common = (
        floor > 0,
        charity >= 0,
        retained >= 0,
        retained <= incoming,
        2 * w > floor,
        incoming > w,
    )
    full_packet_payment = unsat(*common, w + incoming <= floor)
    terminal_capture = unsat(
        *common,
        w + incoming - retained + charity < floor,
        retained <= w + incoming + charity - floor,
    )
    positive_capture = unsat(
        *common,
        w + incoming - retained + charity < floor,
        retained <= charity,
    )

    result = {
        "schema": "current-wall-backward-hole-capture-audit-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "checks": {
            "full_current_wall_packet_with_retained_w_base_pays": full_packet_payment,
            "terminal_failure_forces_exact_retained_packet_capture": terminal_capture,
            "terminal_capture_strictly_exceeds_charity_value": positive_capture,
        },
        "claim_boundary": (
            "Cap-free payment-hole termination for the nonsingleton current "
            "wall. Observer safety, capture uncrossing, and complete EFX remain."
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
