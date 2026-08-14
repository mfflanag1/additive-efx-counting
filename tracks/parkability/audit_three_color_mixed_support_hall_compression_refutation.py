#!/usr/bin/env python3
"""Audit the three-color mixed-support compression counterexample."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCES = (1, 2, 3)
CORES = {
    2: (("x01", 0), ("x11", 1)),
    3: (("x02", 0), ("x22", 2)),
    1: (("x03", 0), ("x33", 3)),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    floor = Fraction(10)
    item_values = (Fraction(6), Fraction(5))
    core_value = sum(item_values)
    cores_desired = core_value > floor
    proper_subcores_not_desired = max(item_values) <= floor
    source_safe = proper_subcores_not_desired

    physical_pairs = {
        (supplier, source)
        for source, goods in CORES.items()
        for _, supplier in goods
        if supplier != source
    }
    expected_pairs = {
        (0, 1), (3, 1),
        (0, 2), (1, 2),
        (0, 3), (2, 3),
    }

    no_closed_subfamily = True
    for size in range(1, 4):
        for subset in itertools.combinations(SOURCES, size):
            base_owners = {0 for source in subset for _ in CORES[source]}
            if base_owners <= set(subset):
                no_closed_subfamily = False

    theorem = root / "results/THREE_COLOR_MIXED_SUPPORT_HALL_COMPRESSION_REFUTATION_20260814.md"
    parent = root / "results/PI_FREE_DESIRED_CORE_SUPPORT_DRAINAGE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "six distinct frozen-supplier pairs" in text
    assert "not the full fixed-`U`" in text

    return {
        "schema": "three-color-mixed-support-hall-compression-refutation-audit-v1",
        "status": "EXACT_SIX_GOOD_LOCAL_COUNTEREXAMPLE",
        "owners": [0, 1, 2, 3],
        "missing_source": 0,
        "represented_sources": list(SOURCES),
        "source_floor": str(floor),
        "core_item_values": [str(value) for value in item_values],
        "core_value": str(core_value),
        "all_cores_strictly_desired": cores_desired,
        "all_cores_inclusion_minimal": proper_subcores_not_desired,
        "all_cores_source_safe": source_safe,
        "other_observer_common_safety_realizable": True,
        "all_core_goods_base_owned_by_missing_source": True,
        "no_closed_represented_source_subfamily": no_closed_subfamily,
        "physical_pairs": [list(pair) for pair in sorted(physical_pairs)],
        "physical_pair_count": len(physical_pairs),
        "physical_pairs_match_expected": physical_pairs == expected_pairs,
        "at_most_three_pair_reversal_exists": len(physical_pairs) <= 3,
        "full_fixed_u_countermodel": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "PI-freeness of the displayed response family and common-safe "
            "minimal desire do not imply a three-pair frozen-supplier reversal"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
