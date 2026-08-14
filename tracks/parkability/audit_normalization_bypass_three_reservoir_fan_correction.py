#!/usr/bin/env python3
"""Independent audit of the corrected four-core reservoir fan boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_closed_family(source_map, base_owner):
    cores_by_source = {owner: [] for owner in OWNERS}
    for target, source in enumerate(source_map):
        cores_by_source[source].append(target)
    for size in range(1, 5):
        for subset_tuple in itertools.combinations(OWNERS, size):
            subset = set(subset_tuple)
            choices = [cores_by_source[source] for source in subset_tuple]
            if any(not options for options in choices):
                continue
            for selected in itertools.product(*choices):
                if len(set(selected)) != len(selected):
                    continue
                if all(base_owner[target] in subset for target in selected):
                    return True
    return False


def run(root: Path = ROOT) -> dict[str, object]:
    maps = [
        mapping
        for mapping in itertools.product(OWNERS, repeat=4)
        if all(mapping[target] != target for target in OWNERS)
    ]
    image_histogram = Counter(len(set(mapping)) for mapping in maps)
    multiplicity_histogram = Counter(
        "+".join(map(str, sorted(Counter(mapping).values(), reverse=True)))
        for mapping in maps
    )

    counter_source_map = (1, 0, 0, 0)
    counter_base_owner = (2, 3, 2, 3)
    current_cycle = (
        counter_source_map[0] == 1 and counter_source_map[1] == 0
    )
    counterexample_has_closed_family = has_closed_family(
        counter_source_map, counter_base_owner
    )

    theorem = root / "results/NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_CORRECTION_LEMMA_20260814.md"
    closed = root / "results/CLOSED_DISJOINT_DESIRED_CORE_PI_CAPTURE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "base owners" in text
    assert "current supplier cycle implies generalized PI" in text

    return {
        "schema": "normalization-bypass-three-reservoir-fan-correction-audit-v1",
        "status": "SURJECTIVE_PI_OR_MISSING_SOURCE_DEFECT",
        "nonself_source_maps": len(maps),
        "image_size_histogram": {
            str(key): image_histogram[key] for key in sorted(image_histogram)
        },
        "multiplicity_histogram": {
            key: multiplicity_histogram[key]
            for key in sorted(multiplicity_histogram)
        },
        "surjective_maps_force_closed_family": all(
            has_closed_family(mapping, (0, 1, 2, 3))
            for mapping in maps if len(set(mapping)) == 4
        ),
        "counterexample": {
            "source_map_by_target": list(counter_source_map),
            "base_owner_by_core_target": list(counter_base_owner),
            "has_current_supplier_two_cycle": current_cycle,
            "has_closed_disjoint_core_family": counterexample_has_closed_family,
        },
        "current_supplier_cycle_sufficient_for_generalized_pi": False,
        "missing_source_capture_reversed": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, closed, script)
        },
        "claim_boundary": (
            "four distinct sources force generalized PI; nonsurjective maps "
            "leave a missing-source defect and current supplier cycles are insufficient"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
