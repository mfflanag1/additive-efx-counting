#!/usr/bin/env python3
"""Exact arithmetic audit of the mixed-core pure-cell-lift refutation."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    floor = Fraction(10)
    ordinary = Fraction(6)
    residual = Fraction(5)
    desired = ordinary + residual > floor
    no_component_desired = ordinary <= floor and residual <= floor
    source_safe = max(ordinary, residual) <= floor
    observer_rows = [
        {"floor": Fraction(10), "ordinary": Fraction(1 + index), "residual": Fraction(2)}
        for index in range(3)
    ]
    other_observers_safe = all(
        max(row["ordinary"], row["residual"]) <= row["floor"]
        for row in observer_rows
    )

    theorem = root / "results/PURE_CELL_RESPONSE_LIFT_LOCAL_REFUTATION_20260814.md"
    parent = root / "results/LIQUIDATED_ROOT_THREE_SOURCE_PHYSICAL_COMPRESSION_FRONTIER_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "v_i(s)=6" in text
    assert "common-safe" in text

    return {
        "schema": "pure-cell-response-lift-local-refutation-audit-v1",
        "status": "EXACT_POSITIVE_ADDITIVE_LOCAL_COUNTEREXAMPLE",
        "source_floor": str(floor),
        "ordinary_component_value": str(ordinary),
        "root_residual_component_value": str(residual),
        "union_value": str(ordinary + residual),
        "union_strictly_desired": desired,
        "neither_component_desired": no_component_desired,
        "source_row_safe": source_safe,
        "other_observer_rows_safe": other_observers_safe,
        "positive_additive": all(
            value > 0
            for value in (ordinary, residual)
        ) and all(
            row[key] > 0 for row in observer_rows for key in ("ordinary", "residual")
        ),
        "full_fixed_u_countermodel": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "desire and common safety of a mixed core do not imply desire "
            "for either original-supplier component; full saturation remains"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
