#!/usr/bin/env python3
"""Focused regression test for the frozen threshold--Hall checkpoint."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

try:
    from .fast_count import FastParkability
except ImportError:
    from fast_count import FastParkability


ROOT = Path(__file__).resolve().parents[2]


def test_threshold_hall_checkpoint() -> None:
    landscape = FastParkability(2, 3).partial_linear_potential_landscape(
        [[4, 2, 1], [1, 3, 2]],
        potential="normalized_threshold",
    )
    assert landscape["eligible_base_count"] == 1
    assert landscape["maximizer_count"] == 1
    assert landscape["hall_insertable_maximizer_count"] == 1
    assert landscape["maximizers"] == [
        {
            "floater": 2,
            "base_index": 2,
            "utilities": [4, 3],
            "best_host_normalized_margin": 2 / 7,
            "insertable": True,
            "best_hall_normalized_margin": 2 / 7,
            "hall_insertable": True,
        }
    ]

    results = ROOT / "results"
    existential = json.loads(
        (results / "partial_hall_threshold_existential_full_corpus_scan.json")
        .read_text()
    )
    minimum_path = results / "partial_hall_threshold_minimum_full_corpus_scan.json"
    minimum = json.loads(minimum_path.read_text())
    plateau = json.loads(
        (results / "partial_hall_threshold_plateau_completion_analysis.json")
        .read_text()
    )

    assert existential["distinct_profile_count"] == 237
    assert existential["direct_hall_failure_count"] == 0
    assert minimum["distinct_profile_count"] == 237
    assert minimum["direct_hall_failure_count"] == 46
    assert plateau["profile_count"] == 46
    assert plateau["blocked_selected_state_count"] == 4_847
    assert plateau["ownerwise_threshold_preserving_count"] == 4_847
    assert plateau["minimum_slot_cycle_count"] == 4_843
    assert plateau["strict_hall_margin_swap_reachable_count"] == 4_847
    assert plateau["maximum_strict_hall_margin_swap_path_length"] == 2
    assert plateau["source_sha256"] == hashlib.sha256(
        minimum_path.read_bytes()
    ).hexdigest()
