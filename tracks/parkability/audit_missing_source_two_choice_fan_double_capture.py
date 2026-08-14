#!/usr/bin/env python3
"""Independent audit of the rank-three fan double-capture lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path = ROOT) -> dict[str, object]:
    image_three = []
    topology = Counter()
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        image = set(mapping)
        if len(image) != 3:
            continue
        missing = next(owner for owner in OWNERS if owner not in image)
        multiplicities = Counter(mapping)
        duplicate = next(source for source, count in multiplicities.items() if count == 2)
        duplicate_targets = {
            target for target, source in enumerate(mapping) if source == duplicate
        }
        missing_supplies_duplicate_core = missing in duplicate_targets
        topology[
            "missing_is_duplicate_core_supplier"
            if missing_supplies_duplicate_core
            else "both_duplicate_cores_foreign_to_missing"
        ] += 1
        image_three.append(mapping)

    mu, h, p1, p2 = z3.Reals("mu h p1 p2")
    assumptions = [mu > 0, h >= 0, p1 >= 0, p2 >= 0, h + p1 >= mu, h + p2 >= mu]
    double_capture = z3.SolverFor("QF_LRA")
    double_capture.add(*assumptions, h < mu)
    eta = mu - h
    double_capture.add(z3.Or(p1 < eta, p2 < eta))

    theorem = root / "results/MISSING_SOURCE_TWO_CHOICE_FAN_DOUBLE_CAPTURE_LEMMA_20260814.md"
    correction = root / "results/NORMALIZATION_BYPASS_THREE_RESERVOIR_FAN_CORRECTION_LEMMA_20260814.md"
    closed = root / "results/CLOSED_DISJOINT_DESIRED_CORE_PI_CAPTURE_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "double-capture certificate" in text
    assert "24/24 topology split" in text

    return {
        "schema": "missing-source-two-choice-fan-double-capture-audit-v1",
        "status": "COMMON_CAPTURE_OR_TWO_DISJOINT_RESIDUAL_CAPTURES",
        "image_size_three_maps": len(image_three),
        "topology_split": {
            key: topology[key] for key in sorted(topology)
        },
        "double_capture_implication": double_capture.check() == z3.unsat,
        "packet_size_bound_used": False,
        "capture_reversal_proved": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, correction, closed, script)
        },
        "claim_boundary": (
            "PI-freeness forces common full capture or two disjoint residual "
            "captures; the foreign-supplier reversal remains open"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
