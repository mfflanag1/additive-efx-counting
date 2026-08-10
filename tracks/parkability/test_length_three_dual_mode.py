#!/usr/bin/env python3
"""Regression checks for the length-three dual-mode reductions and probes."""

from __future__ import annotations

import itertools
import json
import tempfile
from pathlib import Path

try:
    from .decide_length_three_dual_mode_atom import run as run_atom
    from .decide_length_three_dual_mode_split import (
        find_alternative_dual_mode,
        make_cell,
        payment_owner,
        subset_tables,
    )
    from .analyze_length_three_lex_tail_profiles import run as run_lex_tail
    from .analyze_length_three_tail_extremal_profiles import run as run_tail_extremal
    from .analyze_length_three_hybrid_extremal_profiles import run as run_hybrid_extremal
    from .decide_length_three_hybrid_atom import run as run_hybrid_atom
    from .decide_length_three_ap_suffix_atom import run as run_ap_suffix_atom
    from .decide_length_three_canonical_packet import run as run_canonical_packet
    from .decide_length_three_parallel_pivot import run as run_parallel_pivot
    from .decide_length_three_augmented_payment import run as run_augmented_payment
    from .run_alternating_global_lex_cegar import bundles
except ImportError:
    from decide_length_three_dual_mode_atom import run as run_atom
    from decide_length_three_dual_mode_split import (
        find_alternative_dual_mode,
        make_cell,
        payment_owner,
        subset_tables,
    )
    from analyze_length_three_lex_tail_profiles import run as run_lex_tail
    from analyze_length_three_tail_extremal_profiles import run as run_tail_extremal
    from analyze_length_three_hybrid_extremal_profiles import run as run_hybrid_extremal
    from decide_length_three_hybrid_atom import run as run_hybrid_atom
    from decide_length_three_ap_suffix_atom import run as run_ap_suffix_atom
    from decide_length_three_canonical_packet import run as run_canonical_packet
    from decide_length_three_parallel_pivot import run as run_parallel_pivot
    from decide_length_three_augmented_payment import run as run_augmented_payment
    from run_alternating_global_lex_cegar import bundles


ROOT = Path(__file__).resolve().parents[2]


def numeric_efx(totals, tails, owner):
    assigned = bundles(owner)
    masks = tuple(sum(1 << good for good in bundle) for bundle in assigned)
    return all(
        totals[observer][masks[observer]] >= tails[observer][masks[target]]
        for observer in range(4)
        for target in range(4)
    )


def test_adversarial_audit():
    result = json.loads((ROOT / "results/length_three_dual_mode_adversarial_audit.json").read_text())
    assert result["profile_count"] == 26
    assert result["direct_escape_profile_count"] == 25
    failures = [record for record in result["profiles"] if record["direct_dual_mode_escape"] is None]
    assert [record["label"] for record in failures] == ["pareto_maximal_vstar"]
    assert not failures[0]["mode_feasible_pair_counts"]["r"]
    assert not failures[0]["mode_feasible_pair_counts"]["s"]
    assert all(
        record["canonical_pair"]["escape"] is not None
        for record in result["profiles"]
        if record["label"] != "pareto_maximal_vstar"
    )


def test_lex_tail_adversarial_audit():
    frozen = ROOT / "results/length_three_lex_tail_adversarial_audit.json"
    result = json.loads(frozen.read_text())
    assert result["profile_count"] == 26
    assert result["p_first_escape_count"] == 26
    assert result["s_then_p_escape_count"] == 26
    with tempfile.TemporaryDirectory() as directory:
        replay = Path(directory) / frozen.name
        run_lex_tail(replay)
        assert replay.read_bytes() == frozen.read_bytes()


def test_extremal_adversarial_audits():
    cases = (
        (
            "length_three_tail_extremal_adversarial_audit.json",
            run_tail_extremal,
            {"profile_count": 28, "pareto_pair_count": 57, "pareto_pair_failure_count": 9},
        ),
        (
            "length_three_hybrid_extremal_adversarial_audit.json",
            run_hybrid_extremal,
            {
                "profile_count": 28,
                "pareto_pair_count": 54,
                "pareto_pair_failure_count": 0,
                "canonical_anchor_failure_count": 0,
                "two_way_anchor_failure_count": 0,
                "fixed_p_qmax_failure_count": 0,
            },
        ),
    )
    with tempfile.TemporaryDirectory() as directory:
        for name, replay_function, expected in cases:
            frozen = ROOT / "results" / name
            result = json.loads(frozen.read_text())
            for key, value in expected.items():
                assert result[key] == value
            replay = Path(directory) / name
            replay_function(replay)
            assert replay.read_bytes() == frozen.read_bytes()


def test_atomic_decisions():
    assert run_atom("exact")["status"] == "FIXED_ROOT_DUAL_MODE_FORCED"
    assert run_atom("selected")["status"] == "SAT"
    hybrid = run_hybrid_atom(120)
    assert hybrid["status"] == "ALL_SOURCE_ATOM_FORCED"
    assert hybrid["candidate_count"] == 16384
    assert [record["status"] for record in hybrid["records"]] == ["FORCED"] * 3
    suffix = run_ap_suffix_atom(120)
    assert suffix["status"] == "SUFFIX_FORCED"
    assert suffix["case_count"] == 14
    canonical = run_canonical_packet()
    assert canonical["status"] == "ALL_FORCED"
    assert len(canonical["records"]) == 16
    pivot = run_parallel_pivot()
    assert pivot["status"] == "ALL_FORCED"
    assert len(pivot["records"]) == 4
    payment = run_augmented_payment()
    assert payment["status"] == "ALL_FORCED"
    assert len(payment["records"]) == 5


def test_split_refutation():
    result = json.loads((ROOT / "results/length_three_dual_mode_split_refutation.json").read_text())
    assert result["status"] == "FIXED_ROOT_DUAL_MODE_REFUTED"
    cell = make_cell(tuple(result["packet_sizes"]))
    values = tuple(tuple(row) for row in result["values"])
    totals, tails = subset_tables(values, cell["m"])
    base_masks = tuple(
        sum(1 << good for good in bundle) for bundle in cell["base_bundles"]
    )
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    _tr, br, tq, bq = cell["packets"]
    residual = br + tq + bq
    for size in range(1, len(residual) + 1):
        for payment in itertools.combinations(residual, size):
            for mode, recipient in (("r", 1), ("s", 3)):
                owner = payment_owner(cell, payment, mode)
                payment_value = sum(values[recipient][good] for good in payment)
                assert payment_value < base[recipient] or not numeric_efx(totals, tails, owner)

    minimum = find_alternative_dual_mode(values, cell)
    assert minimum == result["minimum_alternative_dual_mode_escape"]
    assert minimum["changed_good_count"] == 3


if __name__ == "__main__":
    test_adversarial_audit()
    test_lex_tail_adversarial_audit()
    test_extremal_adversarial_audits()
    test_atomic_decisions()
    test_split_refutation()
    print("length-three dual-mode tests passed")
