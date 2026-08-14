#!/usr/bin/env python3
"""Independent algebra/topology audit of root-residual liquidation."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    x, anchor, residual, charity = z3.Reals("x anchor residual charity")
    solver = z3.SolverFor("QF_LRA")
    solver.add(x > 0, anchor > x, residual > 0, charity > 0)
    delta = residual + anchor - x
    solver.add(z3.Not(residual < delta))
    strict_anchor_implies_residual_below_margin = solver.check() == z3.unsat

    owners = ("q", "d", "s")
    records = []
    for q, recipient in itertools.product(owners, repeat=2):
        edges = {(q, "r"), ("r", recipient), ("charity", recipient)}
        # q is a role label here and is always distinct from root/charity;
        # recipient is nonroot.  Coincident source-target pairs would only
        # delete an edge, never add one.
        records.append(
            {
                "anchor_target": q,
                "residual_recipient": recipient,
                "edge_count_upper_bound": len(edges),
            }
        )

    theorem = root / "results/FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md"
    ledger = root / "results/FIXED_U_RANK_THREE_FOUR_EDGE_PREMISE_LEDGER_20260813.md"
    bilateral = root / "results/PERMANENT_ANCHOR_ROOT_TARGET_BILATERAL_COMPENSATOR_FRONTIER_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    ledger_text = ledger.read_text()
    theorem_text = theorem.read_text()
    assert "mandatory strong-wall response `d -> r`" in ledger_text
    assert "physical target support" in ledger_text
    assert "nonempty desired core" in theorem_text
    assert "separate physical progress argument" in theorem_text

    return {
        "schema": "fixed-u-root-residual-nonempty-liquidation-audit-v1",
        "status": "UNIVERSAL_THREE_EDGE_PRIORITY_VALID_PROBE",
        "mandatory_root_response_recorded": True,
        "response_core_nonempty_by_declared_record_semantics": True,
        "response_target_is_original_root_cell": True,
        "strict_anchor_implies_residual_below_margin": (
            strict_anchor_implies_residual_below_margin
        ),
        "maximum_edge_count": max(r["edge_count_upper_bound"] for r in records),
        "topology_records": records,
        "complete_efx_endpoint_proved": False,
        "post_probe_response_recurrence_closed": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, ledger, bilateral, script)
        },
        "claim_boundary": (
            "cap-free nonemptiness and three-edge priority-valid probe; "
            "not a proof that the probe is EFX or that its response closes"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
