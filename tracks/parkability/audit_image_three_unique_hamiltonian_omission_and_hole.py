#!/usr/bin/env python3
"""Audit the unique Hamiltonian omission in every image-three source map."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OWNERS = tuple(range(4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_order(mapping, omitted):
    adjacency = {owner: set() for owner in OWNERS}
    edge_count = 0
    for target, source in enumerate(mapping):
        if target == omitted:
            continue
        adjacency[target].add(source)
        adjacency[source].add(target)
        edge_count += 1
    if edge_count != 3 or sorted(map(len, adjacency.values())) != [1, 1, 2, 2]:
        return None
    endpoints = sorted(owner for owner, neighbors in adjacency.items() if len(neighbors) == 1)
    order = [endpoints[0]]
    previous = None
    while len(order) < 4:
        candidates = adjacency[order[-1]] - ({previous} if previous is not None else set())
        if not candidates:
            return None
        previous, current = order[-1], min(candidates)
        order.append(current)
    if set(order) != set(OWNERS):
        return None
    return order


def run(root: Path = ROOT) -> dict[str, object]:
    records = []
    valid_choice_histogram = Counter()
    missing_is_omitted_histogram = Counter()
    for mapping in itertools.product(OWNERS, repeat=4):
        if any(mapping[target] == target for target in OWNERS):
            continue
        if len(set(mapping)) != 3:
            continue
        missing = next(owner for owner in OWNERS if owner not in mapping)
        duplicate = next(owner for owner in OWNERS if mapping.count(owner) == 2)
        duplicate_targets = [target for target in OWNERS if mapping[target] == duplicate]
        choices = []
        for omitted in duplicate_targets:
            order = path_order(mapping, omitted)
            if order is None:
                continue
            if order[-1] != omitted:
                order.reverse()
            assert order[0] == missing
            assert order[-1] == omitted
            assert all(mapping[order[index]] == order[index + 1] for index in range(3))
            choices.append((omitted, order))
        valid_choice_histogram[len(choices)] += 1
        assert len(choices) == 1
        omitted, order = choices[0]
        missing_is_omitted_histogram[missing in duplicate_targets] += 1
        records.append({
            "mapping": list(mapping),
            "missing_source": missing,
            "duplicated_source": duplicate,
            "duplicated_targets": duplicate_targets,
            "hamiltonian_omission": omitted,
            "oriented_path": order,
            "missing_target_is_duplicate_supplier": missing in duplicate_targets,
        })

    theorem = root / "results/IMAGE_THREE_UNIQUE_HAMILTONIAN_OMISSION_AND_HOLE_LEMMA_20260814.md"
    connected = root / "results/IMAGE_THREE_FULL_OWNER_CONNECTED_RANK_DEFECT_LEMMA_20260814.md"
    payment = root / "results/MISSING_SUPPLIER_DUPLICATE_OMISSION_FOUR_EDGE_PAYMENT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    text = theorem.read_text()
    assert "Exactly one" in text
    assert "single missing-owner hole" in text

    return {
        "schema": "image-three-unique-hamiltonian-omission-hole-audit-v1",
        "status": "ALL_48_MAPS_HAVE_ONE_CANONICAL_PATH_OMISSION",
        "map_count": len(records),
        "valid_hamiltonian_choice_histogram": {
            str(count): frequency
            for count, frequency in sorted(valid_choice_histogram.items())
        },
        "missing_target_duplicate_class_histogram": {
            "missing_supplies_duplicate": missing_is_omitted_histogram[True],
            "foreign_duplicate": missing_is_omitted_histogram[False],
        },
        "all_paths_start_at_missing_source": all(
            record["oriented_path"][0] == record["missing_source"] for record in records
        ),
        "all_paths_end_at_omitted_target": all(
            record["oriented_path"][-1] == record["hamiltonian_omission"]
            for record in records
        ),
        "represented_sources_paid_by_desire": True,
        "only_missing_owner_can_be_unpaid": True,
        "frozen_supplier_edge_bound_proved": False,
        "missing_owner_payment_proved": False,
        "fixed_u_theorem_proved": False,
        "canonical_examples_by_missing_source": {
            str(owner): next(
                record for record in records if record["missing_source"] == owner
            )
            for owner in OWNERS
        },
        "provenance": {
            str(path.relative_to(root)): sha256(path)
            for path in (theorem, connected, payment, script)
        },
        "claim_boundary": (
            "every image-three map has a unique current-holder Hamiltonian "
            "path omission; missing-owner payment and frozen-supplier compression remain"
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
