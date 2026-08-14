#!/usr/bin/env python3
"""Independent audit of the liquidated-root full-source swap."""

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


def run(root: Path = ROOT) -> dict[str, object]:
    records = []
    maximum = 0
    for q, k, source, anchor_residual, source_cell in itertools.product(
        NONROOT, NONROOT, NONROOT, (False, True), (False, True)
    ):
        edges = {
            (supplier, target)
            for supplier, target, active in (
                (q, "r", anchor_residual),
                (q, source, True),
                (source, "r", source_cell),
                ("charity", "r", True),
            )
            if active and supplier != target
        }
        maximum = max(maximum, len(edges))
        records.append(
            {
                "anchor_source": q,
                "residual_holder": k,
                "response_source": source,
                "anchor_residual": anchor_residual,
                "source_cell_nonempty": source_cell,
                "edge_count": len(edges),
            }
        )

    x, anchor, residual, charity, response, source_cell, q_cell = z3.Reals(
        "x anchor residual charity response source_cell q_cell"
    )
    delta = residual + anchor - x
    assumptions = [
        x > 0,
        anchor > x,
        residual > 0,
        charity > 0,
        response > 0,
        source_cell >= 0,
        q_cell >= 0,
        response <= anchor,
    ]

    equivalence = z3.SolverFor("QF_LRA")
    equivalence.add(*assumptions)
    final_root = anchor - response + residual + source_cell + q_cell + charity
    equivalence.add(
        z3.Xor(
            final_root > x,
            response - source_cell - q_cell < delta + charity,
        )
    )

    separator = z3.SolverFor("QF_LRA")
    separator.add(*assumptions)
    separator.add(response - source_cell - q_cell >= delta + charity)
    separator.add(z3.Not(source_cell + q_cell + charity < x))

    theorem = root / "results/LIQUIDATED_ROOT_RESPONSE_FULL_SOURCE_SWAP_FRONTIER_LEMMA_20260814.md"
    parent = root / "results/FIXED_U_LIQUIDATED_ROOT_THREE_PLACEMENT_RESPONSE_FRONTIER_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "full-source swap" in text.lower()
    assert "direct-safety wall" in text

    histogram = {}
    for record in records:
        key = str(record["edge_count"])
        histogram[key] = histogram.get(key, 0) + 1

    return {
        "schema": "liquidated-root-response-full-source-swap-frontier-audit-v1",
        "status": "FOUR_EDGE_SWAP_OR_STRICT_DIRECT_SAFETY",
        "enumerated_role_cases": len(records),
        "maximum_edge_count": maximum,
        "edge_count_histogram": histogram,
        "root_payment_equivalence": equivalence.check() == z3.unsat,
        "failure_implies_strict_direct_safety": separator.check() == z3.unsat,
        "packet_size_bound_used": False,
        "direct_safety_contradicted": False,
        "decorated_recurrence_closed": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "root capture repairs by a four-edge full-source/anchor-residual "
            "swap or implies v_r(S_i)+v_r(Q_i)+v_r(p)<v_r(X_r); "
            "neither final branch is closed"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
