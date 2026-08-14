"""Regression test for the exact liquidated-root physical-edge census."""

import itertools
import json
from collections import Counter
from pathlib import Path

from .audit_liquidated_root_three_source_physical_compression import run


ROOT = Path(__file__).resolve().parents[2]


def independent_census():
    """Second encoding: integer edge masks, with no call to minimum_edges."""
    owners = range(4)
    edge_bit = {
        (supplier, destination): 1 << index
        for index, (supplier, destination) in enumerate(
            (pair for pair in itertools.product(owners, repeat=2) if pair[0] != pair[1])
        )
    }
    charity_bit = {owner: 1 << (12 + owner) for owner in owners}
    histograms = {}
    survivors = {}
    for anchor in (1, 2, 3):
        histogram = Counter()
        five = []
        for mapping in itertools.product(owners, repeat=4):
            if any(mapping[target] == target for target in owners):
                continue
            sources = set(mapping)
            if len(sources) != 3:
                continue
            missing = ({0, 1, 2, 3} - sources).pop()
            duplicate = next(source for source in sources if mapping.count(source) == 2)
            repeated_targets = [target for target in owners if mapping[target] == duplicate]
            omissions = [missing] if missing in repeated_targets else repeated_targets
            candidates = []
            for omitted in omissions:
                for residual_destination in owners:
                    mask = charity_bit[missing]
                    for target in owners:
                        supplier = anchor if target == 0 else target
                        destination = target if target == omitted else mapping[target]
                        if supplier != destination:
                            mask |= edge_bit[(supplier, destination)]
                    if residual_destination != 0:
                        mask |= edge_bit[(0, residual_destination)]
                    candidates.append(mask.bit_count())
            minimum = min(candidates)
            histogram[minimum] += 1
            if minimum == 5:
                five.append(list(mapping))
        histograms[str(anchor)] = dict(sorted(histogram.items()))
        survivors[str(anchor)] = five
    return histograms, survivors


def test_liquidated_root_three_source_physical_compression_replays():
    result = run()
    expected = json.loads(
        (ROOT / "results/liquidated_root_three_source_physical_compression_audit.json").read_text()
    )
    assert result == expected
    assert result["maps_per_anchor_supplier"] == {"1": 48, "2": 48, "3": 48}
    assert result["minimum_edge_histogram_all_anchor_suppliers"] == {
        "3": 42,
        "4": 84,
        "5": 18,
    }
    assert result["at_most_four_per_anchor_supplier"] == 42
    assert result["five_edge_per_anchor_supplier"] == 6
    expected_survivors = [
        [1, 2, 3, 1],
        [1, 3, 1, 2],
        [2, 2, 3, 1],
        [2, 3, 1, 2],
        [3, 2, 3, 1],
        [3, 3, 1, 2],
    ]
    assert result["five_edge_mappings_by_anchor_supplier"] == {
        "1": expected_survivors,
        "2": expected_survivors,
        "3": expected_survivors,
    }
    independent_histograms, independent_survivors = independent_census()
    assert independent_histograms == {
        "1": {3: 14, 4: 28, 5: 6},
        "2": {3: 14, 4: 28, 5: 6},
        "3": {3: 14, 4: 28, 5: 6},
    }
    assert independent_survivors == result["five_edge_mappings_by_anchor_supplier"]
    assert result["minimum_within_declared_normal_form_proved"]
    assert not result["unrestricted_packet_graph_theorem_proved"]
    assert not result["observer_safety_proved"]
    assert not result["fixed_u_theorem_proved"]
