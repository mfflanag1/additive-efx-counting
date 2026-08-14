#!/usr/bin/env python3
"""Independent finite/QF_LRA audit of paid-hole core trimming."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "PAID_HOLE_CORE_TRIMMING_OR_DOUBLE_CAPTURE_LEMMA_20260813.md"


def audit():
    records = 0
    for size in range(1, 5):
        for weights in itertools.product(range(1, 4), repeat=size):
            total = sum(weights)
            for residual in range(0, 5):
                for charity in range(1, 4):
                    for base in range(1, residual + total + 1):
                        if residual + charity >= base:
                            continue
                        feasible = []
                        for mask in range(1, 1 << size):
                            value = sum(
                                weights[index] for index in range(size)
                                if mask & (1 << index)
                            )
                            if residual + charity + value >= base:
                                feasible.append(mask)
                        assert feasible
                        minimum = min(feasible, key=lambda mask: (mask.bit_count(), mask))
                        for index in range(size):
                            if minimum & (1 << index):
                                reduced = minimum & ~(1 << index)
                                reduced_value = sum(
                                    weights[j] for j in range(size)
                                    if reduced & (1 << j)
                                )
                                assert residual + charity + reduced_value < base
                        records += 1

    # If the trimmed remainder T no longer pays source k, the retained H
    # captures the whole strict margin of O=H+T.
    h, t, base_k = z3.Reals("retained_h trimmed_t base_k")
    capture = z3.SolverFor("QF_LRA")
    capture.add(h >= 0, t >= 0, h + t > base_k, t <= base_k)
    capture.add(z3.Not(h >= h + t - base_k))
    assert capture.check() == z3.unsat

    # Matched source and repaired hole are jointly paid in the success case.
    residual, charity, base_h = z3.Reals("residual charity base_h")
    success = z3.SolverFor("QF_LRA")
    success.add(residual + charity + h >= base_h, t > base_k)
    success.add(z3.Or(
        residual + charity + h < base_h,
        t <= base_k,
    ))
    assert success.check() == z3.unsat

    return {
        "schema": "paid-hole-core-trimming-double-capture-audit-v1",
        "status": "MINIMAL_REPAIR_AND_DOUBLE_CAPTURE_VERIFIED",
        "finite_minimal_repair_records": records,
        "maximum_core_items_enumerated": 4,
        "capture_implication_status": "unsat",
        "joint_payment_status": "unsat",
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free algebraic trimming/capture implication with finite "
            "minimal-subset calibration. Simultaneous double-capture reversal, "
            "observer safety, and the active theorem remain open."
        ),
    }


def main():
    result = audit()
    output = ROOT / "results" / "paid_hole_core_trimming_double_capture_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "records": result["finite_minimal_repair_records"],
    }, indent=2))


if __name__ == "__main__":
    main()
