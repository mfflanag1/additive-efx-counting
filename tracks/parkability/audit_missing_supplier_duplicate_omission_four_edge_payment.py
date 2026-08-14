#!/usr/bin/env python3
"""Audit the duplicate-omission payment construction in every role map."""

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
    covered = []
    foreign = []
    edge_histogram = Counter()
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        image = set(mapping)
        if len(image) != 3:
            continue
        missing = next(owner for owner in OWNERS if owner not in image)
        multiplicities = Counter(mapping)
        duplicate = next(source for source, count in multiplicities.items() if count == 2)
        duplicate_targets = [
            target for target, source in enumerate(mapping) if source == duplicate
        ]
        if missing not in duplicate_targets:
            foreign.append(mapping)
            continue

        selected_targets = []
        for source in sorted(image):
            candidates = [
                target for target, named_source in enumerate(mapping)
                if named_source == source and target != missing
            ]
            assert candidates
            selected_targets.append(candidates[0])
        assert len(selected_targets) == 3
        assert len(set(selected_targets)) == 3
        assert missing not in selected_targets
        assert {mapping[target] for target in selected_targets} == image
        edges = {
            (target, mapping[target]) for target in selected_targets
            if target != mapping[target]
        }
        edges.add(("charity", missing))
        edge_histogram[len(edges)] += 1
        covered.append(mapping)

    old, incoming, residual, charity = z3.Reals(
        "old incoming residual charity"
    )
    payment = z3.SolverFor("QF_LRA")
    payment.add(old >= 0, incoming > old, residual >= 0)
    payment.add(z3.Not(residual + incoming > old))
    missing_payment = z3.SolverFor("QF_LRA")
    missing_payment.add(old >= 0, charity > 0)
    missing_payment.add(z3.Not(old + charity > old))

    theorem = root / "results/MISSING_SUPPLIER_DUPLICATE_OMISSION_FOUR_EDGE_PAYMENT_LEMMA_20260814.md"
    parent = root / "results/MISSING_SOURCE_TWO_CHOICE_FAN_DOUBLE_CAPTURE_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Duplicate omission" in text
    assert "24 complementary" in text

    return {
        "schema": "missing-supplier-duplicate-omission-four-edge-payment-audit-v1",
        "status": "TWENTY_FOUR_MAPS_ALL_OWNER_PAID_SUPPORT_CONDITIONAL",
        "covered_maps": len(covered),
        "foreign_supplier_maps": len(foreign),
        "current_holder_move_count_histogram": {
            str(key): edge_histogram[key] for key in sorted(edge_histogram)
        },
        "represented_source_payment": payment.check() == z3.unsat,
        "missing_source_payment": missing_payment.check() == z3.unsat,
        "packet_size_bound_used": False,
        "original_supplier_edge_bound_proved": False,
        "observer_safety_proved": False,
        "paid_repeat_closed": False,
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, parent, script)
        },
        "claim_boundary": (
            "the 24 maps where the missing owner supplies a duplicate core "
            "have an all-owner-paid three-holder-move-plus-charity candidate; "
            "the original-supplier edge condition and observer closure remain"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
