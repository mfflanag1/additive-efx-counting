#!/usr/bin/env python3
"""Independent topology/algebra audit for the liquidated-root frontier."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
NONROOT = ("q", "d", "s")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def active_edges(edges):
    return {(source, target) for source, target, active in edges if active and source != target}


def run(root: Path = ROOT) -> dict[str, object]:
    records = []
    maximum = 0
    for q, k, h, source, target in itertools.product(
        NONROOT, NONROOT, NONROOT, NONROOT, ("r", *NONROOT)
    ):
        if h == source or target == source:
            continue
        if target == "r":
            for proper_anchor_residual in (False, True):
                edges = active_edges(
                    (
                        (q, "r", proper_anchor_residual),
                        (q, source, True),
                        ("charity", "r", True),
                    )
                )
                case = "root_target"
                maximum = max(maximum, len(edges))
                records.append((case, len(edges)))
        elif target == k:
            for original_cell_hit in (False, True):
                edges = active_edges(
                    (
                        (q, "r", True),
                        ("r", source, True),
                        (k, source, original_cell_hit),
                        ("charity", h, True),
                    )
                )
                case = "mixed_residual_holder_target"
                maximum = max(maximum, len(edges))
                records.append((case, len(edges)))
        else:
            edges = active_edges(
                (
                    (q, "r", True),
                    ("r", k, True),
                    (target, source, True),
                    ("charity", h, True),
                )
            )
            case = "ordinary_nonroot_target"
            maximum = max(maximum, len(edges))
            records.append((case, len(edges)))

    x, anchor, residual, charity, response = z3.Reals(
        "x anchor residual charity response"
    )
    delta = residual + anchor - x
    payment_solver = z3.SolverFor("QF_LRA")
    payment_solver.add(x > 0, anchor > x, residual > 0, charity > 0, response > 0)
    final_root = anchor - response + residual + charity
    payment_solver.add(z3.Xor(final_root > x, response < delta + charity))
    root_payment_equivalence = payment_solver.check() == z3.unsat

    theorem = root / "results/FIXED_U_LIQUIDATED_ROOT_THREE_PLACEMENT_RESPONSE_FRONTIER_LEMMA_20260814.md"
    transport = root / "results/PERMANENT_ANCHOR_NONROOT_THREE_PLACEMENT_RESPONSE_TRANSFER_LEMMA_20260814.md"
    liquidation = root / "results/FIXED_U_ROOT_RESIDUAL_NONEMPTY_LIQUIDATION_REDUCTION_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "all** of `Y_r`" in text
    assert "controlled floor reset" in text
    assert "does not" in text

    counts = {}
    for case, edge_count in records:
        counts.setdefault(case, {})
        counts[case][str(edge_count)] = counts[case].get(str(edge_count), 0) + 1

    return {
        "schema": "fixed-u-liquidated-root-three-placement-response-frontier-audit-v1",
        "status": "DISJOINT_RESPONSE_FOUR_EDGE_OR_P_AUGMENTED_ROOT_CAPTURE",
        "enumerated_role_cases": len(records),
        "maximum_edge_count": maximum,
        "edge_count_histogram_by_case": counts,
        "root_payment_equivalence": root_payment_equivalence,
        "controlled_floor_reset_used": False,
        "packet_size_bound_used": False,
        "root_capture_eliminated": False,
        "decorated_recurrence_closed": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, transport, liquidation, script)
        },
        "claim_boundary": (
            "all singleton-disjoint responses execute within four edges unless "
            "a root target captures delta_r+v_r(p); recurrence remains open"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
