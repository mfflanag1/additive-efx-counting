#!/usr/bin/env python3
"""Audit charity retargeting at the current-wall backward terminal."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/CURRENT_WALL_CHARITY_RETARGET_OR_UNANIMOUS_CAPTURE_LEMMA_20260813.md"
OUTPUT = ROOT / "results/current_wall_charity_retarget_unanimous_capture_audit.json"


def unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    if status != z3.unsat:
        raise AssertionError(f"expected UNSAT, got {status}")
    return "unsat"


def run(output: Path = OUTPUT):
    fd, fr, w_d, incoming_d, h_d, p_d, h_r, p_r, base_r = z3.Reals(
        "fd fr w_d incoming_d h_d p_d h_r p_r base_r"
    )
    common = (
        fd > 0,
        fr > 0,
        w_d >= 0,
        incoming_d >= h_d,
        h_d >= 0,
        p_d > 0,
        h_r >= 0,
        p_r > 0,
        base_r >= 0,
        w_d + incoming_d > fd,
        base_r + h_r >= fr,
        w_d + incoming_d - h_d + p_d < fd,
        base_r + p_r < fr,
    )
    d_polarity = unsat(*common, h_d <= p_d)
    r_polarity = unsat(*common, h_r <= p_r)

    # Independent packet conservation and edge-count check on abstract atoms.
    atoms = {"W", "D-H", "H", "P", "B"}
    before = {
        "d": {"W", "D-H", "P"},
        "r": {"B", "H"},
    }
    after = {
        "d": {"W", "D-H", "H"},
        "r": {"B", "P"},
    }
    if set().union(*before.values()) != atoms or set().union(*after.values()) != atoms:
        raise AssertionError("packet conservation failed")
    if any(left & right for left, right in itertools.combinations(before.values(), 2)):
        raise AssertionError("before bundles overlap")
    if any(left & right for left, right in itertools.combinations(after.values(), 2)):
        raise AssertionError("after bundles overlap")
    before_edges = {("r", "d"), ("charity", "d")}
    after_edges = {("r", "d"), ("charity", "r")}
    edge_count_preserved = len(before_edges) == len(after_edges) == 2
    if not edge_count_preserved:
        raise AssertionError("edge count changed")

    result = {
        "schema": "current-wall-charity-retarget-unanimous-capture-audit-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "checks": {
            "exact_packet_conservation": True,
            "root_owner_failure_forces_H_above_P": r_polarity,
            "sacrificed_owner_failure_forces_H_above_P": d_polarity,
            "two_active_edge_slots_preserved": edge_count_preserved,
        },
        "claim_boundary": (
            "Cap-free payment retarget/polarity lemma. It does not prove "
            "observer safety, generalized PI, or complete EFX."
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
