#!/usr/bin/env python3
"""Differential tests for the exact parkability workbench."""

from __future__ import annotations

import contextlib
import hashlib
import io
import itertools
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from . import (
        core,
        audit_matching_augmentation,
        audit_aggregate_min_selector,
        audit_row_min_selector,
        audit_bottom_pattern_conversion_orbits,
        augment_partition_pool_by_shape,
        build_anchored49_pool,
        fast_count,
        independent,
        integer_partition_master,
        lra_master,
        master,
        normalize_smt2_for_cvc5,
        run_adaptive_priority_cegar,
        run_cegar,
        run_efx_lra_cegar,
        run_distinct_half_full_cell_cegar,
        run_distinct_half_full_cell_cpsat_cegar,
        run_bottom_pair_pattern_selector_cegar,
        run_two_pair_bottom_cross_cegar,
        decide_bottom_pattern_conversion_selector,
        decide_two_pair_bottom_cross_conversion,
        decide_distinct_half_terminal_exchange,
        run_generic_partition_cegar,
        run_integer_partition_cegar,
        run_lexmax_partial_cegar,
        run_lra_cegar,
    )
except ImportError:
    import core
    import audit_matching_augmentation
    import audit_aggregate_min_selector
    import audit_row_min_selector
    import audit_bottom_pattern_conversion_orbits
    import augment_partition_pool_by_shape
    import build_anchored49_pool
    import fast_count
    import independent
    import integer_partition_master
    import lra_master
    import master
    import normalize_smt2_for_cvc5
    import run_adaptive_priority_cegar
    import run_cegar
    import run_efx_lra_cegar
    import run_distinct_half_full_cell_cegar
    import run_distinct_half_full_cell_cpsat_cegar
    import run_bottom_pair_pattern_selector_cegar
    import run_two_pair_bottom_cross_cegar
    import decide_bottom_pattern_conversion_selector
    import decide_two_pair_bottom_cross_conversion
    import decide_distinct_half_terminal_exchange
    import run_generic_partition_cegar
    import run_integer_partition_cegar
    import run_lexmax_partial_cegar
    import run_lra_cegar


ROOT = Path(__file__).resolve().parents[2]


def triple_key(triple: core.Triple) -> independent.Triple:
    return triple.floater, tuple(triple.base_owner), triple.host


def compare_enumerators(values: list[list[int]], label: str) -> int:
    base_first = independent.enumerate_base_first(values)
    completion_first = independent.enumerate_completion_first(values)
    if base_first != completion_first:
        raise AssertionError(f"{label}: independent enumeration orders disagree")

    optimized = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    repeated = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    if optimized != repeated:
        raise AssertionError(f"{label}: optimized enumeration is nondeterministic")
    if optimized != base_first:
        raise AssertionError(f"{label}: optimized and literal triple sets disagree")
    optimized_count = core.count_efx0_allocations(values)
    literal_count = independent.count_complete_efx0(values)
    if optimized_count != literal_count:
        raise AssertionError(f"{label}: optimized and literal complete counts disagree")

    for floater, owner, host in optimized:
        triple = core.Triple(floater, owner, host)
        if not core.triple_is_parkable(values, triple):
            raise AssertionError(f"{label}: enumerated triple failed core predicate")
        if not independent.is_parkable_triple(values, floater, owner, host):
            raise AssertionError(f"{label}: enumerated triple failed literal predicate")
    return len(optimized)


def test_literal_zero_semantics() -> None:
    values = [[0, 0], [1, 0]]
    if independent.is_complete_efx0(values, [0, 0]):
        raise AssertionError("zero-valued removed goods were not checked")
    base = (0, None)
    if not independent.is_removed_good_efx0(values, base, 1):
        raise AssertionError("controlled one-good base is not EFX0")
    triple = core.Triple(1, base, 0)
    if independent.is_parkable_triple(values, 1, base, 0):
        raise AssertionError("literal predicate accepted zero-sensitive parking")
    if core.triple_is_parkable(values, triple):
        raise AssertionError("core predicate accepted zero-sensitive parking")


def test_small_differential() -> tuple[int, int]:
    cases = [
        ("single_good", [[1], [0]]),
        ("zero_sensitive", [[0, 0], [1, 0]]),
        ("all_ones", [[1, 1, 1], [1, 1, 1]]),
    ]
    rng = random.Random(20260726)
    for n, m, repetitions in ((2, 2, 5), (2, 3, 5), (3, 3, 5), (3, 4, 5)):
        for index in range(repetitions):
            values = [[rng.randrange(5) for _ in range(m)] for _ in range(n)]
            cases.append((f"random_{n}_{m}_{index}", values))

    triple_total = 0
    for label, values in cases:
        triple_total += compare_enumerators(values, label)
    return len(cases), triple_total


def test_basin1_regression() -> None:
    instance = json.loads((ROOT / "results" / "tb4.json").read_text())
    values = instance["values"]
    expected = [(3, (1, 1, 0, None, 3, 2, 2, 2), host) for host in range(4)] + [
        (5, (1, 1, 0, 2, 3, None, 2, 2), 2),
        (7, (1, 1, 0, 2, 3, 2, 2, None), 2),
    ]
    expected = sorted(expected)

    independent_base = independent.enumerate_base_first(values)
    independent_completion = independent.enumerate_completion_first(values)
    optimized = [triple_key(triple) for triple in core.iter_parkable_triples(values)]
    if independent_base != expected:
        raise AssertionError("basin-1 literal base-first regression changed")
    if independent_completion != expected:
        raise AssertionError("basin-1 literal completion-first regression changed")
    if optimized != expected:
        raise AssertionError("basin-1 optimized regression changed")

    limited = [
        triple_key(triple) for triple in core.iter_parkable_triples(values, limit=3)
    ]
    if limited != expected[:3]:
        raise AssertionError("triple enumeration limit is not a stable prefix")

    recorded_base = expected[0][1]
    base_detail = core.classify_base(values, 3, recorded_base)
    certificates = json.loads(
        (ROOT / "artifacts" / "generalized_parking" / "certificates.json").read_text()
    )
    certificate = next(
        record for record in certificates["witnesses"] if record["id"] == "n4_m8_basin1"
    )
    if base_detail["base_min_efx_slack"] != 3:
        raise AssertionError("basin-1 base EFX slack changed")
    if base_detail["parking_slack_matrix"] != certificate["parking_slack_matrix"]:
        raise AssertionError("basin-1 parking slack matrix changed")
    if base_detail["parkable_hosts"] != [0, 1, 2, 3]:
        raise AssertionError("basin-1 recorded base lost a parking")

    report = core.landscape(values, sample_limit=10)
    if not report["exhaustive"]:
        raise AssertionError("basin-1 landscape unexpectedly stopped early")
    if report["deletion_allocations_checked"] != 8 * 4**7:
        raise AssertionError("basin-1 deletion universe was not exhausted")
    if report["parkable_triple_count"] != 6:
        raise AssertionError("basin-1 parkable triple count changed")
    if report["complete_efx0_count"] != 4:
        raise AssertionError("basin-1 complete EFX0 count changed")
    if independent.count_complete_efx0(values) != 4:
        raise AssertionError("basin-1 literal complete EFX0 count changed")
    if (
        list(independent.count_removed_good_efx0_bases(values))
        != report["efx0_base_count_by_floater"]
    ):
        raise AssertionError("basin-1 literal deletion-base counts changed")
    if [
        core.validate_triple(raw, 4, 8).to_dict() for raw in report["triple_sample"]
    ] != [core.Triple(*triple).to_dict() for triple in expected]:
        raise AssertionError("basin-1 landscape sample changed")

    completions = {
        tuple(
            host if good == floater else owner for good, owner in enumerate(base_owner)
        )
        for floater, base_owner, host in expected
    }
    if len(completions) != 4:
        raise AssertionError("six basin-1 triples no longer encode four completions")

    invalid = core.Triple(0, (None, 0, 0, 0, 0, 0, 0, 0), 0)
    if core.triple_is_parkable(values, invalid):
        raise AssertionError("invalid basin-1 control passed the core predicate")
    if independent.is_parkable_triple(
        values, invalid.floater, invalid.base_owner, invalid.host
    ):
        raise AssertionError("invalid basin-1 control passed the literal predicate")


def test_master_cuts() -> int:
    values = json.loads((ROOT / "results" / "tb4.json").read_text())["values"]
    triples = [
        core.Triple(3, (1, 1, 0, None, 3, 2, 2, 2), host) for host in range(4)
    ] + [
        core.Triple(5, (1, 1, 0, 2, 3, None, 2, 2), 2),
        core.Triple(7, (1, 1, 0, 2, 3, 2, 2, None), 2),
    ]
    for triple in triples:
        fixed = master.ParkabilityMaster(4, 8, 1, 60, fixed_values=values)
        if not fixed.add_triple(triple):
            raise AssertionError("fresh valid triple was treated as a duplicate")
        if fixed.add_triple(triple) or fixed.pool_size != 1:
            raise AssertionError("master triple deduplication failed")
        result = fixed.solve(time_limit_s=10)
        if result.status != "UNSAT":
            raise AssertionError(f"valid fixed triple cut returned {result.status}")

    invalid = core.Triple(0, (None, 0, 0, 0, 0, 0, 0, 0), 0)
    fixed = master.ParkabilityMaster(4, 8, 1, 60, fixed_values=values)
    fixed.add_triple(invalid)
    result = fixed.solve(time_limit_s=10)
    if result.status != "SAT":
        raise AssertionError(f"invalid fixed triple cut returned {result.status}")
    if result.values != tuple(tuple(row) for row in values):
        raise AssertionError("fixed-value master decoded a different matrix")

    tiny = master.ParkabilityMaster(2, 1, 1, 1)
    if tiny.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("empty tiny K=1 master is not SAT")
    only_matrix_triple = core.Triple(0, (None,), 0)
    if not independent.is_parkable_triple(
        [[1], [1]],
        only_matrix_triple.floater,
        only_matrix_triple.base_owner,
        only_matrix_triple.host,
    ):
        raise AssertionError("tiny K=1 control triple is not parkable")
    tiny.add_triple(only_matrix_triple)
    if tiny.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("tiny K=1 valid cut did not close the master")

    exhaustive = 0
    for flat in itertools.product((1, 2), repeat=4):
        small_values = [list(flat[:2]), list(flat[2:])]
        for floater in range(2):
            other = 1 - floater
            for owner in range(2):
                base_owner: list[int | None] = [None, None]
                base_owner[other] = owner
                for host in range(2):
                    triple = core.Triple(floater, tuple(base_owner), host)
                    expected_valid = independent.is_parkable_triple(
                        small_values,
                        floater,
                        base_owner,
                        host,
                    )
                    fixed = master.ParkabilityMaster(
                        2,
                        2,
                        1,
                        2,
                        fixed_values=small_values,
                    )
                    fixed.add_triple(triple)
                    encoded_valid = fixed.solve(time_limit_s=10).status == "UNSAT"
                    if encoded_valid != expected_valid:
                        raise AssertionError(
                            (
                                "fixed triple cut mismatch",
                                small_values,
                                triple,
                                expected_valid,
                            )
                        )
                    exhaustive += 1
    return len(triples) + 2 + exhaustive


def test_lra_master() -> int:
    values = json.loads((ROOT / "results" / "tb4.json").read_text())["values"]
    valid = core.Triple(3, (1, 1, 0, None, 3, 2, 2, 2), 0)
    invalid = core.Triple(0, (None, 0, 0, 0, 0, 0, 0, 0), 0)

    integer = lra_master.ParkabilityLRAMaster(
        2,
        2,
        integer_upper=3,
        fixed_values=[[3, 1], [1, 3]],
    )
    integer_overflow = lra_master.ParkabilityLRAMaster(
        2,
        2,
        integer_upper=2,
        fixed_values=[[3, 1], [1, 3]],
    )
    if (
        integer.solve(time_limit_s=10).values != ((3, 1), (1, 3))
        or integer_overflow.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("bounded-integer arithmetic domain is inconsistent")

    fixed = lra_master.ParkabilityLRAMaster(4, 8, fixed_values=values)
    fixed.add_triple(valid)
    if fixed.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("valid triple did not exclude its fixed rational matrix")

    fixed = lra_master.ParkabilityLRAMaster(4, 8, fixed_values=values)
    fixed.add_triple(invalid)
    solved = fixed.solve(time_limit_s=10)
    if solved.status != "SAT" or solved.values != tuple(map(tuple, values)):
        raise AssertionError("invalid LRA triple excluded or changed its fixed matrix")

    valid_completion = tuple(
        valid.host if good == valid.floater else owner
        for good, owner in enumerate(valid.base_owner)
    )
    fixed = lra_master.ParkabilityLRAMaster(4, 8, fixed_values=values)
    fixed.add_complete_allocation(valid_completion)
    if fixed.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("valid complete allocation did not exclude its matrix")

    invalid_completion = (0,) * 8
    if independent.is_complete_efx0(values, invalid_completion):
        raise AssertionError("LRA invalid-completion control unexpectedly became EFX0")
    fixed = lra_master.ParkabilityLRAMaster(4, 8, fixed_values=values)
    fixed.add_complete_allocation(invalid_completion)
    solved = fixed.solve(time_limit_s=10)
    if solved.status != "SAT" or solved.values != tuple(map(tuple, values)):
        raise AssertionError("invalid complete allocation excluded its fixed matrix")

    universal = lra_master.ParkabilityLRAMaster(
        2,
        2,
        exclude_universal_min=True,
        fixed_values=[[1, 1], [1, 2]],
    )
    if universal.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("universal-minimum LRA case cut was not enforced")

    nonuniversal = lra_master.ParkabilityLRAMaster(
        2,
        2,
        exclude_universal_min=True,
        fixed_values=[[1, 2], [2, 1]],
    )
    solved = nonuniversal.solve(time_limit_s=10)
    if solved.status != "SAT" or solved.values != ((1, 2), (2, 1)):
        raise AssertionError("no-universal-minimum matrix was lost or decoded incorrectly")

    peelable = lra_master.ParkabilityLRAMaster(
        4,
        8,
        exclude_peelable=True,
        fixed_values=[[100, 1, 1, 1, 1, 1, 1, 1]] * 4,
    )
    if peelable.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("peelable-good LRA case cut was not enforced")

    nonpeelable_values = json.loads((ROOT / "results" / "tb4.json").read_text())[
        "values"
    ]
    nonpeelable = lra_master.ParkabilityLRAMaster(
        4,
        8,
        exclude_peelable=True,
        fixed_values=nonpeelable_values,
    )
    if nonpeelable.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("nonpeelable matrix was lost by the LRA case cut")

    repeated = lra_master.ParkabilityLRAMaster(
        4,
        8,
        require_pairwise_distinct_rows=True,
        fixed_values=[nonpeelable_values[0]] * 4,
    )
    if repeated.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("repeated normalized rows survived the distinct-row cut")

    distinct = lra_master.ParkabilityLRAMaster(
        4,
        8,
        require_pairwise_distinct_rows=True,
        fixed_values=nonpeelable_values,
    )
    if distinct.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("pairwise-distinct normalized rows were lost")

    tied_items = lra_master.ParkabilityLRAMaster(
        2,
        3,
        require_distinct_item_values=True,
        fixed_values=[[1, 1, 2], [1, 2, 3]],
    )
    if tied_items.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("tied item values survived the generic-position cut")

    distinct_items = lra_master.ParkabilityLRAMaster(
        2,
        3,
        require_distinct_item_values=True,
        fixed_values=[[1, 2, 3], [3, 2, 1]],
    )
    if distinct_items.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("distinct item values were lost")

    favorite_match = lra_master.ParkabilityLRAMaster(
        4,
        8,
        require_favorite_hall_deficiency=True,
        fixed_values=[
            [9, 1, 1, 1, 1, 1, 1, 1],
            [1, 9, 1, 1, 1, 1, 1, 1],
            [1, 1, 9, 1, 1, 1, 1, 1],
            [1, 1, 1, 9, 1, 1, 1, 1],
        ],
    )
    if favorite_match.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("favorite-good matching survived the Hall cut")

    favorite_deficient = lra_master.ParkabilityLRAMaster(
        4,
        8,
        require_favorite_hall_deficiency=True,
        fixed_values=nonpeelable_values,
    )
    if favorite_deficient.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("favorite-Hall-deficient matrix was lost")

    boxed = lra_master.ParkabilityLRAMaster(2, 2)
    boxed.add_normalized_box([[1, 3], [3, 1]], Fraction(1, 100))
    solved = boxed.solve(time_limit_s=10)
    if solved.status != "SAT" or solved.values is None:
        raise AssertionError("nonempty normalized LRA box was lost")
    for row, center in zip(solved.values, ((1, 3), (3, 1))):
        for value, midpoint in zip(row, center):
            if abs(Fraction(value, sum(row)) - Fraction(midpoint, 4)) > Fraction(
                1, 100
            ):
                raise AssertionError("decoded LRA box model lies outside its bounds")

    ordered = lra_master.ParkabilityLRAMaster(
        2, 2, symmetry="double_lex", fixed_values=[[2, 1], [1, 2]]
    )
    reversed_rows = lra_master.ParkabilityLRAMaster(
        2, 2, symmetry="double_lex", fixed_values=[[1, 2], [2, 1]]
    )
    if (
        ordered.solve(time_limit_s=10).status != "SAT"
        or reversed_rows.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("exact-real DoubleLex ordering is inconsistent")

    covered = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[1, 2, 3], [2, 1, 3]]
    )
    covered.add_minimum_cover([0, 1])
    uncovered = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[3, 1, 2], [3, 2, 1]]
    )
    uncovered.add_minimum_cover([0])
    if (
        covered.solve(time_limit_s=10).status != "SAT"
        or uncovered.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("minimum-cover LRA constraint is inconsistent")

    patterned = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[1, 2, 3], [2, 1, 3]]
    )
    patterned.add_minimum_pattern([0, 1])
    wrong_pattern = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[1, 2, 3], [2, 1, 3]]
    )
    wrong_pattern.add_minimum_pattern([1, 0])
    if (
        patterned.solve(time_limit_s=10).status != "SAT"
        or wrong_pattern.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("minimum-pattern LRA constraint is inconsistent")

    favorite_patterned = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[3, 2, 1], [1, 3, 2]]
    )
    favorite_patterned.add_strict_favorite_pattern([0, 1])
    wrong_favorite_pattern = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[3, 2, 1], [1, 3, 2]]
    )
    wrong_favorite_pattern.add_strict_favorite_pattern([1, 0])
    if (
        favorite_patterned.solve(time_limit_s=10).status != "SAT"
        or wrong_favorite_pattern.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("strict-favorite LRA pattern is inconsistent")

    stabilized = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[3, 2, 1], [3, 1, 2]]
    )
    stabilized.add_strict_favorite_pattern([0, 0])
    stabilized.add_favorite_pattern_stabilizer([0, 0])
    unstabilized_order = lra_master.ParkabilityLRAMaster(
        2, 3, fixed_values=[[3, 1, 2], [3, 2, 1]]
    )
    unstabilized_order.add_strict_favorite_pattern([0, 0])
    unstabilized_order.add_favorite_pattern_stabilizer([0, 0])
    if (
        stabilized.solve(time_limit_s=10).status != "SAT"
        or unstabilized_order.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("favorite-pattern stabilizer is inconsistent")

    ranked = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[4, 3, 2, 1], [4, 1, 3, 2]]
    )
    ranked.add_strict_ranking_prefixes([(0, 1), (0, 2)])
    wrong_ranking = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[4, 3, 2, 1], [4, 1, 3, 2]]
    )
    wrong_ranking.add_strict_ranking_prefixes([(0, 2), (0, 1)])
    if (
        ranked.solve(time_limit_s=10).status != "SAT"
        or wrong_ranking.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("strict ranking-prefix constraints are inconsistent")

    rank_stabilized = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[4, 3, 2, 1], [4, 3, 1, 2]]
    )
    rank_stabilized.add_strict_ranking_prefixes([(0, 1), (0, 1)])
    rank_stabilized.add_ranking_prefix_stabilizer([(0, 1), (0, 1)])
    wrong_rank_order = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[4, 3, 1, 2], [4, 3, 2, 1]]
    )
    wrong_rank_order.add_strict_ranking_prefixes([(0, 1), (0, 1)])
    wrong_rank_order.add_ranking_prefix_stabilizer([(0, 1), (0, 1)])
    if (
        rank_stabilized.solve(time_limit_s=10).status != "SAT"
        or wrong_rank_order.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("ranking-prefix stabilizer is inconsistent")

    bottom = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[1, 2, 3, 4], [2, 1, 4, 3]]
    )
    bottom.add_bottom_set([0, 1])
    wrong_bottom = lra_master.ParkabilityLRAMaster(
        2, 4, fixed_values=[[1, 3, 2, 4], [2, 1, 4, 3]]
    )
    wrong_bottom.add_bottom_set([0, 1])
    if (
        bottom.solve(time_limit_s=10).status != "SAT"
        or wrong_bottom.solve(time_limit_s=10).status != "UNSAT"
    ):
        raise AssertionError("bottom-set LRA constraint is inconsistent")

    efx_partition = ((0, 1), (2, 3), (4,), (5, 6, 7))
    partitioned = lra_master.ParkabilityLRAMaster(
        4,
        8,
        fixed_values=values,
    )
    partitioned.add_partition_obstruction(efx_partition)
    if partitioned.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("EFX-admitting partition was not excluded")

    activated = lra_master.ParkabilityLRAMaster(
        4,
        8,
        fixed_values=values,
    )
    partition_activation = lra_master.z3.Bool("partition_activation_control")
    activated.add_partition_obstruction(
        efx_partition,
        activation=partition_activation,
    )
    if (
        activated.solver.check() != lra_master.z3.sat
        or activated.solver.check(partition_activation) != lra_master.z3.unsat
    ):
        raise AssertionError("partition activation literal is not exact")

    no_efx_partition = ((0, 1), (2, 3), (4, 5), (6, 7))
    partitioned = lra_master.ParkabilityLRAMaster(
        4,
        8,
        fixed_values=values,
    )
    partitioned.add_partition_obstruction(no_efx_partition)
    if partitioned.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("Hall-deficient partition obstruction was lost")
    return 37


def test_integer_partition_master() -> int:
    partitions = list(core.iter_unlabeled_nonempty_partitions(2, 3))
    checked = 0
    for flat in itertools.product((1, 2), repeat=6):
        values = (flat[:3], flat[3:])
        for partition in partitions:
            expected = (
                "SAT"
                if audit_matching_augmentation.matching_rank(
                    audit_matching_augmentation.feasible_graph(values, partition)
                )
                < 2
                else "UNSAT"
            )
            for encoding in ("matching_clauses", "hall_selectors"):
                encoded = integer_partition_master.IntegerPartitionMaster(
                    2,
                    3,
                    2,
                    fixed_values=values,
                )
                encoded.add_partition_obstruction(
                    partition,
                    encoding=encoding,
                )
                if encoded.solve(time_limit_s=5).status != expected:
                    raise AssertionError(
                        ("integer partition encoding mismatch", values, partition)
                    )
            checked += 1

    upper_missing = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        3,
        require_upper_used=True,
        fixed_values=((1, 2, 1), (2, 1, 2)),
    )
    upper_present = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        3,
        require_upper_used=True,
        fixed_values=((1, 3, 1), (2, 1, 2)),
    )
    if (
        upper_missing.solve(time_limit_s=5).status != "UNSAT"
        or upper_present.solve(time_limit_s=5).status != "SAT"
    ):
        raise AssertionError("upper-used cap-ladder cut is inconsistent")

    ranked = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        3,
        fixed_values=((3, 2, 1), (3, 1, 2)),
    )
    ranked.add_strict_ranking_prefixes(((0, 1), (0, 2)))
    wrong_ranked = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        3,
        fixed_values=((3, 1, 2), (3, 2, 1)),
    )
    wrong_ranked.add_strict_ranking_prefixes(((0, 1), (0, 2)))
    stabilized = integer_partition_master.IntegerPartitionMaster(2, 3, 3)
    stabilized.add_strict_ranking_prefixes(((0, 1), (0, 1)))
    stabilized.add_ranking_prefix_stabilizer(((0, 1), (0, 1)))
    if (
        ranked.solve(time_limit_s=5).status != "SAT"
        or wrong_ranked.solve(time_limit_s=5).status != "UNSAT"
        or stabilized.solve(time_limit_s=5).status != "SAT"
    ):
        raise AssertionError("integer ranking-prefix constraints are inconsistent")

    half_represented = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        5,
        fixed_values=((5, 3, 1), (5, 1, 3)),
    )
    half_represented.add_half_favorite_representatives((0, 0), (1, 2))
    wrong_half_represented = integer_partition_master.IntegerPartitionMaster(
        2,
        3,
        5,
        fixed_values=((5, 2, 1), (5, 1, 2)),
    )
    wrong_half_represented.add_half_favorite_representatives((0, 0), (1, 2))
    stabilized_half_represented = (
        integer_partition_master.IntegerPartitionMaster(2, 4, 5)
    )
    stabilized_half_represented.add_half_favorite_representatives(
        (0, 0),
        (1, 2),
    )
    stabilized_half_represented.add_half_favorite_representative_stabilizer(
        (0, 0),
        (1, 2),
    )
    if (
        half_represented.solve(time_limit_s=5).status != "SAT"
        or wrong_half_represented.solve(time_limit_s=5).status != "UNSAT"
        or stabilized_half_represented.solve(time_limit_s=5).status != "SAT"
    ):
        raise AssertionError("half-favorite representatives are inconsistent")

    threshold_passes = integer_partition_master.IntegerPartitionMaster(
        3,
        4,
        3,
        fixed_values=((3, 1, 1, 1),) * 3,
    )
    threshold_fails = integer_partition_master.IntegerPartitionMaster(
        3,
        4,
        3,
        fixed_values=((1, 3, 3, 3),) * 3,
    )
    residual_partitions = tuple(core.iter_unlabeled_nonempty_partitions(2, 3))
    for observer in range(3):
        for residual_partition in residual_partitions:
            mapped = tuple(
                tuple(good + 1 for good in bundle)
                for bundle in residual_partition
            )
            threshold_passes.add_owner_threshold_obstruction(
                observer,
                0,
                mapped,
            )
            threshold_fails.add_owner_threshold_obstruction(
                observer,
                0,
                mapped,
            )
    if (
        threshold_passes.solve(time_limit_s=5).status != "UNSAT"
        or threshold_fails.solve(time_limit_s=5).status != "SAT"
        or threshold_fails.owner_threshold_clauses != 9
    ):
        raise AssertionError("owner-threshold obstruction is inconsistent")

    envelope_fails = integer_partition_master.IntegerPartitionMaster(
        4,
        9,
        10,
        fixed_values=((10, 9, 8, 7, 6, 5, 4, 3, 2),) * 4,
    )
    envelope_passes = integer_partition_master.IntegerPartitionMaster(
        4,
        9,
        10,
        fixed_values=((10, 1, 1, 1, 1, 1, 1, 1, 1),) * 4,
    )
    for observer in range(4):
        envelope_fails.add_owner_threshold_shape_envelope(observer, 0)
        envelope_passes.add_owner_threshold_shape_envelope(observer, 0)
    if (
        envelope_fails.solve(time_limit_s=5).status != "SAT"
        or envelope_passes.solve(time_limit_s=5).status != "UNSAT"
        or envelope_fails.owner_threshold_envelope_rows != 4
    ):
        raise AssertionError("owner-threshold shape envelope is inconsistent")

    with tempfile.TemporaryDirectory(prefix="integer-partition-test-") as directory:
        root = Path(directory)
        with contextlib.redirect_stdout(io.StringIO()):
            result = run_integer_partition_cegar.run(
                n=2,
                m=3,
                upper=5,
                pool_path=root / "pool.json",
                result_path=root / "result.json",
                proto_path=root / "model.pb",
                partition_shape=(2, 1),
                max_iterations=5,
                time_limit_s=10,
                workers=1,
            )
        if (
            result["status"] != "UNSAT_BOUNDED_CELL_CANDIDATE"
            or result["partition_shape"] != [2, 1]
            or result["partition_universe_size"] != 3
        ):
            raise AssertionError("shape-restricted integer CEGAR failed")
        with contextlib.redirect_stdout(io.StringIO()):
            union_result = run_integer_partition_cegar.run(
                n=3,
                m=5,
                upper=1,
                pool_path=root / "union-pool.json",
                result_path=root / "union-result.json",
                proto_path=root / "union-model.pb",
                partition_shape=(3, 1, 1),
                partition_singleton_good=0,
                add_per_iteration=13,
                max_iterations=2,
                time_limit_s=10,
                workers=1,
            )
        if (
            union_result["status"] != "UNSAT_BOUNDED_CELL_CANDIDATE"
            or union_result["partition_shape"] != [3, 1, 1]
            or union_result["partition_shapes"] != [[3, 1, 1]]
            or union_result["partition_singleton_good"] != 0
            or union_result["partition_singleton_goods"] != [0]
            or union_result["partition_universe_size"] != 13
        ):
            raise AssertionError("shape-or-singleton integer CEGAR failed")
        with contextlib.redirect_stdout(io.StringIO()):
            shape_union_result = run_integer_partition_cegar.run(
                n=3,
                m=5,
                upper=1,
                pool_path=root / "shape-union-pool.json",
                result_path=root / "shape-union-result.json",
                proto_path=root / "shape-union-model.pb",
                partition_shapes=((3, 1, 1), (2, 2, 1)),
                add_per_iteration=25,
                max_iterations=2,
                time_limit_s=10,
                workers=1,
            )
        if (
            shape_union_result["status"] != "UNSAT_BOUNDED_CELL_CANDIDATE"
            or shape_union_result["partition_shape"] is not None
            or shape_union_result["partition_shapes"]
            != [[3, 1, 1], [2, 2, 1]]
            or shape_union_result["partition_universe_size"] != 25
        ):
            raise AssertionError("multi-shape integer CEGAR failed")
    return checked + 17


def test_fast_count() -> int:
    evaluator = fast_count.FastParkability()
    instances = [json.loads((ROOT / "results" / "tb4.json").read_text())["values"]]
    rng = random.Random(20260729)
    instances.extend(
        [[rng.randrange(1, 8) for _ in range(8)] for _ in range(4)]
        for _ in range(3)
    )
    for values in instances:
        fast = evaluator.landscape(values)
        exact = core.landscape(values, sample_limit=0, include_complete_count=False)
        if fast["parkable_triple_count"] != exact["parkable_triple_count"]:
            raise AssertionError("vectorized and core parkability counts disagree")
        if [
            sum(row)
            for row in fast["parkable_triple_count_by_floater_host"]
        ] != exact["parkable_triple_count_by_floater"]:
            raise AssertionError("vectorized floater counts disagree")
        if [
            sum(fast["parkable_triple_count_by_floater_host"][floater][host]
                for floater in range(8))
            for host in range(4)
        ] != exact["parkable_triple_count_by_host"]:
            raise AssertionError("vectorized host counts disagree")
        complete = evaluator.complete_efx0_landscape(values)
        literal_complete = independent.count_complete_efx0(values)
        if complete["complete_efx0_count"] != literal_complete:
            raise AssertionError("vectorized and literal complete-EFX counts disagree")
        if sum(complete["complete_efx0_count_by_shape"].values()) != literal_complete:
            raise AssertionError("vectorized complete-EFX shape counts disagree")
        family = evaluator.complete_efx0_family_landscape(
            values,
            shape_codes=(3221,),
            singleton_goods=(0,),
        )
        exact_family = sum(
            "".join(
                map(
                    str,
                    sorted(
                        (
                            assignment.count(agent)
                            for agent in range(4)
                        ),
                        reverse=True,
                    ),
                )
            )
            == "3221"
            or assignment.count(assignment[0]) == 1
            for assignment in core.iter_efx0_assignments(values)
        )
        if family["complete_efx0_family_count"] != exact_family:
            raise AssertionError("vectorized complete-EFX family count disagrees")

    small_values = [[4, 2, 1], [1, 3, 2]]
    small = fast_count.FastParkability(2, 3)
    lexmax = small.lexmax_one_unallocated_landscape(small_values)
    eligible = []
    for floater in range(3):
        for base in core.iter_efx_bases(small_values, floater):
            if all(
                base["own_values"][observer] >= small_values[observer][floater]
                for observer in range(2)
            ):
                eligible.append(base)
    best_key = max(tuple(base["own_values"]) for base in eligible)
    best = [
        base for base in eligible
        if tuple(base["own_values"]) == best_key
    ]
    if (
        lexmax["eligible_base_count"] != len(eligible)
        or lexmax["lexmax_utility_key"] != list(best_key)
        or lexmax["lexmax_base_count"] != len(best)
        or lexmax["lexmax_insertable_count"]
        != sum(bool(base["parkable_hosts"]) for base in best)
    ):
        raise AssertionError("vectorized lex-max partial-EFX audit disagrees")
    all_orders = small.lexmax_all_agent_orders_landscape(small_values)
    individual_orders = [
        small.lexmax_one_unallocated_landscape(
            small_values,
            agent_order=order,
        )
        for order in itertools.permutations(range(2))
    ]
    if (
        all_orders["eligible_base_count"] != len(eligible)
        or all_orders["agent_order_count"] != 2
        or all_orders["insertable_agent_order_count"]
        != sum(
            result["lexmax_insertable_count"] > 0
            for result in individual_orders
        )
        or [
            record["lexmax_utility_key"]
            for record in all_orders["order_records"]
        ]
        != [
            result["lexmax_utility_key"]
            for result in individual_orders
        ]
        or any(
            record["lexmax_base_count"] != result["lexmax_base_count"]
            or record["lexmax_insertable_count"]
            != result["lexmax_insertable_count"]
            or abs(
                record["best_lexmax_host_normalized_margin"]
                - result["best_lexmax_host_normalized_margin"]
            )
            > 1e-12
            for record, result in zip(
                all_orders["order_records"],
                individual_orders,
            )
        )
    ):
        raise AssertionError("shared all-order lex-max audit disagrees")
    try:
        small.lexmax_one_unallocated_landscape(
            small_values,
            agent_order=(0, 0),
        )
    except ValueError:
        pass
    else:
        raise AssertionError("invalid lex-max agent order was accepted")
    return len(instances) + 2


def test_lexmax_partial_encoding() -> int:
    values = (
        (2, 1, 9),
        (5, 3, 4),
    )
    candidate = (1, (0, None, 1))
    order = (0, 1)
    rivals, audit = run_lexmax_partial_cegar.lex_rivals(
        values,
        candidate,
        order,
    )
    if (
        audit["eligible_base_count"] != 2
        or audit["nonlower_rival_count"] != 1
        or len(rivals) != 1
    ):
        raise AssertionError("small lex-max rival census changed")
    candidate_only = lra_master.ParkabilityLRAMaster(
        2,
        3,
        fixed_values=values,
    )
    utilities = run_lexmax_partial_cegar.add_candidate(
        candidate_only,
        *candidate,
    )
    if candidate_only.solver.check() != lra_master.z3.sat:
        raise AssertionError("strict blocked candidate encoding rejected its model")
    run_lexmax_partial_cegar.add_rival_blocker(
        candidate_only,
        utilities,
        candidate[1],
        rivals[0],
        order,
        "exact",
    )
    if candidate_only.solver.check() != lra_master.z3.unsat:
        raise AssertionError("lexicographically nonlower rival was not blocked")
    nondegenerate = lra_master.ParkabilityLRAMaster(
        2,
        3,
        fixed_values=values,
    )
    utilities = run_lexmax_partial_cegar.add_candidate(
        nondegenerate,
        *candidate,
    )
    run_lexmax_partial_cegar.add_rival_blocker(
        nondegenerate,
        utilities,
        candidate[1],
        rivals[0],
        order,
        "bundle_nondegenerate",
    )
    if nondegenerate.solver.check() != lra_master.z3.unsat:
        raise AssertionError("nondegenerate lex rival was not blocked")
    return 3


def test_adaptive_priority_helpers() -> int:
    values = (
        (2, 1, 9),
        (5, 3, 4),
    )
    expected = [
        ((0, 1), (1, (1, None, 0))),
        ((1, 0), (1, (1, None, 0))),
    ]
    cells = run_adaptive_priority_cegar.derive_unique_seed_cells(values)
    if cells != expected:
        raise AssertionError(("adaptive-priority seed cells changed", cells))
    rivals = {order: [] for order, _ in cells}
    with tempfile.TemporaryDirectory(
        prefix="adaptive-priority-pool-"
    ) as directory:
        path = Path(directory) / "pool.json"
        path.write_text(
            json.dumps(
                run_adaptive_priority_cegar.pool_document(
                    2,
                    3,
                    cells,
                    rivals,
                )
            )
        )
        loaded = run_adaptive_priority_cegar.load_pool(
            path,
            2,
            3,
            cells,
        )
        if loaded != rivals:
            raise AssertionError("adaptive-priority pool round trip changed")
    try:
        run_adaptive_priority_cegar.derive_unique_seed_cells(
            (
                (1, 1, 1),
                (1, 1, 1),
            )
        )
    except ValueError:
        pass
    else:
        raise AssertionError("tied adaptive-priority seed was accepted")
    return 3


def test_one_nonsingleton_certificates() -> tuple[int, int]:
    small = list(core.iter_one_nonsingleton_triples(2, 3))
    if len(small) != 12 or len(set(small)) != 12:
        raise AssertionError("small one-nonsingleton certificate count changed")
    for triple in small:
        if not independent.is_parkable_triple(
            [[1, 1, 1], [1, 1, 1]],
            triple.floater,
            triple.base_owner,
            triple.host,
        ):
            raise AssertionError("one-nonsingleton control certificate is invalid")
    target = list(core.iter_one_nonsingleton_triples(4, 8))
    if len(target) != 6_720 or len(set(target)) != 6_720:
        raise AssertionError("shape-5111 certificate count changed")
    return len(small), len(target)


def test_source_census() -> int:
    no_two_source = [
        [18, 1, 11, 52, 6, 7],
        [16, 19, 18, 21, 16, 5],
        [13, 10, 14, 20, 13, 17],
        [18, 10, 11, 19, 14, 10],
    ]
    census = core.complete_efx0_source_census(no_two_source)
    if census != (6, 52, 0, 0, 0):
        raise AssertionError(("two-source obstruction census changed", census))
    if sum(census) != independent.count_complete_efx0(no_two_source):
        raise AssertionError("source census and literal EFX count disagree")
    no_equalization_kernel = [
        [31, 18, 26, 31, 31, 45],
        [41, 7, 32, 36, 13, 42],
        [46, 41, 27, 30, 21, 50],
        [44, 29, 31, 9, 28, 45],
    ]
    second_census = core.complete_efx0_source_census(no_equalization_kernel)
    if second_census != (20, 72, 0, 0, 0):
        raise AssertionError(
            ("source-equalization obstruction census changed", second_census)
        )
    no_equalization = [
        [14, 31, 18, 26, 31, 10, 31, 45],
        [3, 41, 7, 32, 36, 1, 13, 42],
        [18, 46, 41, 27, 30, 10, 21, 50],
        [2, 44, 29, 31, 9, 8, 28, 45],
    ]
    kernel = core.bottom_pair_kernel_census(no_equalization, [0, 5])
    if kernel != {
        "efx0_count": 92,
        "source_count_census": (20, 72, 0, 0, 0),
        "two_source_allocation_count": 0,
        "source_equalization_count": 0,
    }:
        raise AssertionError(("bottom-pair kernel census changed", kernel))
    return 3


def test_threshold_cycle_normal_form() -> tuple[int, int]:
    matrix_count = 0
    allocation_count = 0
    for flat in itertools.product((1, 2), repeat=6):
        values = [flat[:3], flat[3:]]
        matrix_count += 1
        for assignment in itertools.product(range(2), repeat=3):
            if not independent.is_complete_efx0(values, assignment):
                continue
            allocation_count += 1
            result = core.threshold_cycle_normal_form(values, assignment)
            if not independent.is_complete_efx0(values, result.assignment):
                raise AssertionError("threshold-cycle endpoint is not literally EFX0")
            if any(
                right <= left
                for left, right in zip(
                    result.threshold_potential_trace,
                    result.threshold_potential_trace[1:],
                )
            ):
                raise AssertionError("threshold-cycle potential trace did not increase")
            for host, good in result.removable_pairs:
                base = list(result.assignment)
                base[good] = None
                if not independent.is_parkable_triple(values, good, base, host):
                    raise AssertionError(
                        "threshold-cycle removable pair failed literal verification"
                    )
    rotation_values = [
        [14, 13, 9, 9, 2, 1, 2, 11],
        [10, 14, 7, 7, 10, 5, 6, 12],
        [13, 2, 7, 8, 6, 2, 7, 6],
        [12, 10, 10, 14, 6, 1, 2, 3],
    ]
    rotation_start = (0, 3, 1, 2, 3, 1, 1, 2)
    rotated = core.threshold_cycle_normal_form(rotation_values, rotation_start)
    if (
        rotated.assignment != (0, 1, 2, 3, 1, 2, 2, 3)
        or rotated.rotations != ((3, 2, 1),)
        or rotated.threshold_potential_trace != (31, 42)
    ):
        raise AssertionError(("threshold-cycle directed regression changed", rotated))
    allocation_count += 1
    return matrix_count, allocation_count


def test_favorite_pair_construction() -> int:
    cases = 0
    for flat in itertools.product((1, 2), repeat=8):
        values = [flat[:4], flat[4:]]
        assignment = core.favorite_pair_allocation(values)
        favorite_sets = [
            {good for good, value in enumerate(row) if value == max(row)}
            for row in values
        ]
        matching_exists = any(
            pair[0] in favorite_sets[0] and pair[1] in favorite_sets[1]
            for pair in itertools.permutations(range(4), 2)
        )
        if (assignment is not None) != matching_exists:
            raise AssertionError("favorite-pair matching detection changed")
        if assignment is not None and not independent.is_complete_efx0(
            values, assignment
        ):
            raise AssertionError("favorite-pair construction is not EFX0")
        cases += 1
    if core.favorite_pair_allocation(
        [
            [9, 1, 1, 1, 1, 1, 1, 1],
            [1, 9, 1, 1, 1, 1, 1, 1],
            [1, 1, 9, 1, 1, 1, 1, 1],
            [1, 1, 1, 9, 1, 1, 1, 1],
        ]
    ) is None:
        raise AssertionError("four-agent favorite-pair control lost its matching")
    tb4 = json.loads((ROOT / "results" / "tb4.json").read_text())["values"]
    if core.favorite_pair_allocation(tb4) is not None:
        raise AssertionError("favorite-Hall-deficient basin unexpectedly matched")
    return cases + 2


def test_complementary_wall() -> int:
    values = [
        [3, 5492, 2694, 22602, 31736, 4, 21010, 34539],
        [348, 28272, 16010, 84861, 36138, 18, 10058, 60455],
        [372, 110006, 23178, 206395, 86612, 12994, 206519, 180484],
        [12, 36021, 17067, 145590, 48350, 2707, 148982, 73591],
    ]
    primary = {
        (host, 2, 0, 1, 2, 2, 3, 0)
        for host in range(4)
    }
    dual = {
        (0, 0, 1, 3, 0, 1, 2, 1),
        (0, 0, 1, 2, 0, 1, 3, 1),
        (0, 0, 2, 1, 0, 2, 3, 2),
        (0, 0, 3, 1, 0, 3, 2, 3),
    }
    expected_counts = (4, 4, 8, 7)
    for delta, expected_count in enumerate(expected_counts):
        perturbed = [row[:] for row in values]
        perturbed[0][1] += delta
        perturbed[0][5] -= delta
        allocations = set(core.iter_efx0_assignments(perturbed))
        if len(allocations) != expected_count:
            raise AssertionError(("complementary-wall count changed", delta))
        if delta <= 2 and not primary <= allocations:
            raise AssertionError(("primary wall family disappeared too early", delta))
        if delta >= 2 and not dual <= allocations:
            raise AssertionError(("dual wall family appeared too late", delta))

    shape_switch_base = [
        [3, 95, 100, 6, 64, 20, 23, 9],
        [28, 75, 77, 20, 74, 9, 21, 2],
        [9, 94, 4, 13, 93, 63, 3, 5],
        [21, 58, 31, 19, 96, 34, 20, 10],
    ]
    shape_switch_counts = (
        (4, Counter({"4211": 3, "5111": 1})),
        (7, Counter({"4211": 2, "5111": 5})),
        (7, Counter({"4211": 2, "5111": 5})),
        (9, Counter({"4211": 2, "5111": 7})),
        (9, Counter({"4211": 1, "5111": 8})),
        (8, Counter({"5111": 8})),
    )
    for delta, (expected_count, expected_shapes) in enumerate(
        shape_switch_counts
    ):
        shape_switch = [row[:] for row in shape_switch_base]
        shape_switch[1][0] -= delta
        shape_switch[1][2] += delta
        switched_allocations = list(core.iter_efx0_assignments(shape_switch))
        switched_shapes = Counter(
            "".join(
                map(
                    str,
                    sorted(
                        (
                            assignment.count(agent)
                            for agent in range(4)
                        ),
                        reverse=True,
                    ),
                )
            )
            for assignment in switched_allocations
        )
        if (
            len(switched_allocations) != expected_count
            or switched_shapes != expected_shapes
        ):
            raise AssertionError(("shape-switch certificate changed", delta))
    shape_switch = [row[:] for row in shape_switch_base]
    shape_switch[1][0] -= 5
    shape_switch[1][2] += 5
    if (
        run_lra_cegar.has_universal_min(shape_switch)
        or run_efx_lra_cegar.has_peelable_good(shape_switch)
        or run_efx_lra_cegar.has_repeated_normalized_rows(shape_switch)
    ):
        raise AssertionError("shape-switch certificate left the residual case")
    return len(expected_counts) + len(shape_switch_counts)


def test_partition_reduction() -> tuple[int, int]:
    partitions = list(core.iter_unlabeled_nonempty_partitions(4, 8))
    shape_counts = Counter(
        tuple(sorted(map(len, partition), reverse=True))
        for partition in partitions
    )
    expected = Counter(
        {
            (5, 1, 1, 1): 56,
            (4, 2, 1, 1): 420,
            (3, 3, 1, 1): 280,
            (3, 2, 2, 1): 840,
            (2, 2, 2, 2): 105,
        }
    )
    if shape_counts != expected or len(set(partitions)) != 1701:
        raise AssertionError(("unlabeled partition universe changed", shape_counts))

    encoded_cases = 0
    small_partitions = list(core.iter_unlabeled_nonempty_partitions(2, 3))
    for flat in itertools.product((1, 2), repeat=6):
        values = [flat[:3], flat[3:]]
        for partition in small_partitions:
            admits_efx = False
            for matching in itertools.permutations(range(2)):
                assignment = [0] * 3
                for agent, bundle in enumerate(matching):
                    for good in partition[bundle]:
                        assignment[good] = agent
                admits_efx |= independent.is_complete_efx0(values, assignment)
            for encoding in (
                "matching_clauses",
                "inline_matching_clauses",
                "hall_selectors",
            ):
                fixed = lra_master.ParkabilityLRAMaster(
                    2,
                    3,
                    fixed_values=values,
                )
                fixed.add_partition_obstruction(
                    partition,
                    encoding=encoding,
                )
                encoded = fixed.solve(time_limit_s=10).status == "UNSAT"
                if encoded != admits_efx:
                    raise AssertionError(
                        (
                            "partition-matching encoding mismatch",
                            encoding,
                            values,
                            partition,
                        )
                    )
                encoded_cases += 1
    return len(partitions), encoded_cases


def test_anchored49_family() -> int:
    partitions = list(core.iter_unlabeled_nonempty_partitions(4, 9))
    singleton = {
        partition
        for partition in partitions
        if build_anchored49_pool.singleton_anchor(partition)
    }
    balanced = {
        partition
        for partition in partitions
        if build_anchored49_pool.balanced_boundary(partition)
    }
    if (
        len(partitions) != 7770
        or len(singleton) != 473
        or len(balanced) != 480
        or singleton & balanced
    ):
        raise AssertionError("anchored 4x9 family census changed")
    return len(singleton | balanced)


def test_ranking_cell_stabilizer_guard() -> int:
    try:
        run_generic_partition_cegar.run(
            n=2,
            m=3,
            seed_paths=[],
            pool_path=Path("unused-pool.json"),
            result_path=Path("unused-result.json"),
            smt2_path=Path("unused-formula.smt2"),
            add_per_iteration=1,
            max_iterations=1,
            time_limit_s=1,
            symmetry="none",
            exclude_universal_min=False,
            exclude_peelable=False,
            require_pairwise_distinct_rows=False,
            require_distinct_item_values=False,
            obstruction_encoding="matching_clauses",
            favorite_pattern=(0, 0),
            favorite_pattern_stabilizer=True,
            second_favorite_pattern=(1, 2),
            ranking_prefix_stabilizer=True,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("unsafe real favorite-only stabilizer was accepted")
    try:
        run_integer_partition_cegar.run(
            n=2,
            m=3,
            upper=3,
            pool_path=Path("unused-integer-pool.json"),
            result_path=Path("unused-integer-result.json"),
            proto_path=Path("unused-integer-model.pb"),
            favorite_pattern=(0, 0),
            favorite_pattern_stabilizer=True,
            second_favorite_pattern=(1, 2),
            ranking_prefix_stabilizer=True,
        )
    except ValueError:
        return 2
    raise AssertionError("unsafe integer favorite-only stabilizer was accepted")


def test_generic_partition_scope() -> int:
    with tempfile.TemporaryDirectory(prefix="generic-partition-scope-") as directory:
        root = Path(directory)
        with contextlib.redirect_stdout(io.StringIO()):
            result = run_generic_partition_cegar.run(
                n=3,
                m=5,
                seed_paths=[],
                pool_path=root / "pool.json",
                result_path=root / "result.json",
                smt2_path=root / "formula.smt2",
                add_per_iteration=13,
                max_iterations=2,
                time_limit_s=10,
                symmetry="none",
                exclude_universal_min=False,
                exclude_peelable=False,
                require_pairwise_distinct_rows=False,
                require_distinct_item_values=False,
                obstruction_encoding="matching_clauses",
                favorite_pattern=None,
                favorite_pattern_stabilizer=False,
                second_favorite_pattern=None,
                ranking_prefix_stabilizer=False,
                integer_upper=1,
                partition_shape=(3, 1, 1),
                partition_singleton_goods=(0,),
            )
        if (
            result["status"] != "UNSAT_CANDIDATE"
            or result["partition_universe_size"] != 13
            or result["partition_shape"] != [3, 1, 1]
            or result["partition_singleton_goods"] != [0]
        ):
            raise AssertionError("shape-or-singleton LRA scope failed")
        with contextlib.redirect_stdout(io.StringIO()):
            shape_union = run_generic_partition_cegar.run(
                n=3,
                m=5,
                seed_paths=[],
                pool_path=root / "shape-union-pool.json",
                result_path=root / "shape-union-result.json",
                smt2_path=root / "shape-union-formula.smt2",
                add_per_iteration=25,
                max_iterations=2,
                time_limit_s=10,
                symmetry="none",
                exclude_universal_min=False,
                exclude_peelable=False,
                require_pairwise_distinct_rows=False,
                require_distinct_item_values=False,
                obstruction_encoding="matching_clauses",
                favorite_pattern=None,
                favorite_pattern_stabilizer=False,
                second_favorite_pattern=None,
                ranking_prefix_stabilizer=False,
                integer_upper=1,
                partition_shape=(3, 1, 1),
                additional_partition_shapes=((2, 2, 1),),
            )
        if (
            shape_union["status"] != "UNSAT_CANDIDATE"
            or shape_union["partition_universe_size"] != 25
            or shape_union["partition_shape"] != [3, 1, 1]
            or shape_union["additional_partition_shapes"] != [[2, 2, 1]]
        ):
            raise AssertionError("multi-shape LRA scope failed")
    balanced = tuple(
        partition
        for partition in core.iter_unlabeled_nonempty_partitions(4, 9)
        if augment_partition_pool_by_shape.eligible_partition(
            partition,
            {"3222"},
            set(),
            {0: 2},
        )
    )
    if len(balanced) != 840:
        raise AssertionError("favorite-pair balanced filter changed")
    return 3


def test_standard_hall_smt2() -> int:
    nonstandard = (
        "(declare-fun a () Bool)\n"
        "(assert ((_ at-most 1) a))\n"
        "(check-sat)\n"
    )
    try:
        normalize_smt2_for_cvc5.normalize(nonstandard)
    except ValueError:
        pass
    else:
        raise AssertionError("nonstandard cardinality operator was accepted")
    partition = next(core.iter_unlabeled_nonempty_partitions(2, 3))
    master_instance = lra_master.ParkabilityLRAMaster(2, 3)
    master_instance.add_partition_obstruction(
        partition,
        encoding="hall_selectors",
    )
    source = master_instance.to_smt2()
    if "(_ at-most" in source or "(_ at-least" in source:
        raise AssertionError("Hall encoding emitted a nonstandard operator")
    normalized, _ = normalize_smt2_for_cvc5.normalize(source)
    if "(set-logic QF_LRA)" not in normalized:
        raise AssertionError("standard Hall formula was not normalized")
    integer_source = source.replace("() Real)", "() Int)")
    integer_normalized, _ = normalize_smt2_for_cvc5.normalize(integer_source)
    if "(set-logic QF_LIA)" not in integer_normalized:
        raise AssertionError("integer Hall formula received the wrong logic")
    return 3


def test_aggregate_minimum_selector_helpers() -> int:
    values = ((1, 2, 3), (3, 2, 1))
    scores = audit_aggregate_min_selector.normalized_aggregate_scores(values)
    if scores != (Fraction(2, 3), Fraction(2, 3), Fraction(2, 3)):
        raise AssertionError("normalized aggregate scores changed")
    if audit_aggregate_min_selector.aggregate_minimum_goods(values) != (0, 1, 2):
        raise AssertionError("aggregate-minimum tie handling changed")

    for strict in (False, True):
        encoded = lra_master.ParkabilityLRAMaster(2, 3, fixed_values=values)
        encoded.add_aggregate_minimum_good(0, strict=strict)
        expected = not strict
        if (encoded.solve(time_limit_s=10).status == "SAT") != expected:
            raise AssertionError("aggregate-minimum LRA encoding changed")

    unique = ((1, 3, 4), (1, 4, 3))
    encoded = lra_master.ParkabilityLRAMaster(2, 3, fixed_values=unique)
    encoded.add_aggregate_minimum_good(0, strict=True)
    if encoded.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("strict aggregate-minimum encoding rejected control")

    row_min_values = ((1, 3, 4), (4, 2, 3))
    if audit_row_min_selector.row_minimum_goods(row_min_values) != (0, 1):
        raise AssertionError("row-minimum selector changed")
    strict_minimum = lra_master.ParkabilityLRAMaster(
        2,
        3,
        fixed_values=row_min_values,
    )
    strict_minimum.add_strict_minimum_pattern((0, 1))
    if strict_minimum.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("strict row-minimum encoding rejected control")
    strict_minimum_wrong = lra_master.ParkabilityLRAMaster(
        2,
        3,
        fixed_values=row_min_values,
    )
    strict_minimum_wrong.add_strict_minimum_pattern((1, 0))
    if strict_minimum_wrong.solve(time_limit_s=10).status != "UNSAT":
        raise AssertionError("strict row-minimum encoding accepted wrong pattern")
    return 7


def test_complete_efx_lra_pool() -> int:
    values = json.loads((ROOT / "results" / "tb4.json").read_text())["values"]
    if run_efx_lra_cegar.has_peelable_good(values):
        raise AssertionError("nonpeelable direct-EFX control changed")
    if not run_efx_lra_cegar.has_peelable_good(
        [[100, 1, 1, 1, 1, 1, 1, 1]] * 4
    ):
        raise AssertionError("peelable direct-EFX control was not detected")
    if run_efx_lra_cegar.has_repeated_normalized_rows(values):
        raise AssertionError("distinct direct-EFX control rows became proportional")
    if not run_efx_lra_cegar.has_repeated_normalized_rows([values[0]] * 4):
        raise AssertionError("repeated normalized rows were not detected")
    triple = core.Triple(3, (1, 1, 0, None, 3, 2, 2, 2), 0)
    if run_efx_lra_cegar.completion_of_triple(triple) != (
        1,
        1,
        0,
        0,
        3,
        2,
        2,
        2,
    ):
        raise AssertionError("parkable triple was imported as the wrong completion")
    selected, total, counts = run_efx_lra_cegar.select_diverse_allocations(
        values,
        10,
        set(),
    )
    if total != 4 or len(selected) != 4 or sum(counts.values()) != 4:
        raise AssertionError("complete-EFX LRA selector lost basin-1 allocations")
    if any(not independent.is_complete_efx0(values, item) for item in selected):
        raise AssertionError("complete-EFX LRA selector emitted an invalid allocation")
    with tempfile.TemporaryDirectory(prefix="complete-efx-pool-test-") as directory:
        pool_path = Path(directory) / "pool.json"
        raw_path = Path(directory) / "raw.json"
        pool_path.write_text(json.dumps(run_efx_lra_cegar.pool_document(selected)))
        if run_efx_lra_cegar.load_pool(pool_path) != selected:
            raise AssertionError("complete-EFX LRA pool did not round-trip")
        raw_path.write_text(json.dumps([list(item) for item in selected]))
        if run_efx_lra_cegar.load_allocation_import(raw_path) != selected:
            raise AssertionError("raw allocation import did not round-trip")
    return 10


def is_double_lex(values: list[list[int]]) -> bool:
    rows = [tuple(row) for row in values]
    columns = [
        tuple(values[observer][good] for observer in range(len(values)))
        for good in range(len(values[0]))
    ]
    return all(
        rows[index] >= rows[index + 1] for index in range(len(rows) - 1)
    ) and all(columns[index] >= columns[index + 1] for index in range(len(columns) - 1))


def test_double_lex() -> tuple[int, int]:
    encoded_cases = 0
    for flat in itertools.product((1, 2), repeat=4):
        values = [list(flat[:2]), list(flat[2:])]
        fixed = master.ParkabilityMaster(
            2, 2, 1, 2, symmetry="double_lex", fixed_values=values
        )
        encoded = fixed.solve(time_limit_s=10).status == "SAT"
        if encoded != is_double_lex(values):
            raise AssertionError(("DoubleLex encoding mismatch", values))
        encoded_cases += 1

    orbit_cases = 0
    for flat in itertools.product((1, 2), repeat=6):
        values = [list(flat[:3]), list(flat[3:])]
        representative = False
        for rows in itertools.permutations(range(2)):
            for columns in itertools.permutations(range(3)):
                permuted = [[values[row][good] for good in columns] for row in rows]
                if is_double_lex(permuted):
                    representative = True
                    break
            if representative:
                break
        if not representative:
            raise AssertionError(("DoubleLex orbit uncovered", values))
        orbit_cases += 1
    return encoded_cases, orbit_cases


def test_pool_and_runner() -> int:
    with tempfile.TemporaryDirectory(prefix="parkability-test-") as directory:
        root = Path(directory)
        pool_path = root / "pool.json"
        trace_path = root / "trace.jsonl"
        result_path = root / "result.json"
        with contextlib.redirect_stdout(io.StringIO()):
            result = run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=result_path,
                trace_path=trace_path,
            )
        if result["status"] != "UNSAT_CANDIDATE":
            raise AssertionError("K=1 runner smoke did not close")
        if result["iterations"] != 2 or result["pool_size"] != 4:
            raise AssertionError("K=1 runner smoke changed")
        pool_bytes = pool_path.read_bytes()
        if result["pool_sha256"] != hashlib.sha256(pool_bytes).hexdigest():
            raise AssertionError("result does not bind the pool bytes")
        if (
            result["trace_sha256"]
            != hashlib.sha256(trace_path.read_bytes()).hexdigest()
        ):
            raise AssertionError("result does not bind the trace bytes")
        triples = run_cegar.load_pool(pool_path, 1, "none")
        if len(triples) != 4:
            raise AssertionError("saved K=1 pool did not replay")
        try:
            run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=root / "stale-trace-result.json",
                trace_path=trace_path,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("existing session trace was accepted")

        resumed_path = root / "resumed.json"
        with contextlib.redirect_stdout(io.StringIO()):
            resumed = run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=resumed_path,
                trace_path=None,
            )
        if (
            resumed["status"] != "UNSAT_CANDIDATE"
            or resumed["iterations"] != 1
            or resumed["pool_sha256"] != result["pool_sha256"]
        ):
            raise AssertionError("K=1 resumed terminal result changed")

        duplicate_path = root / "duplicate.json"
        duplicate = run_cegar.pool_document(triples, 1, "none")
        duplicate["triples"].append(duplicate["triples"][0])
        duplicate_path.write_text(json.dumps(duplicate))
        try:
            run_cegar.load_pool(duplicate_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("duplicate pool triple was accepted")

        wrong_box_path = root / "wrong-box.json"
        wrong_box = run_cegar.pool_document(triples, 1, "none")
        wrong_box["upper"] = 2
        wrong_box_path.write_text(json.dumps(wrong_box))
        try:
            run_cegar.load_pool(wrong_box_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("pool from a different box was accepted")

        extra_field_path = root / "extra-field.json"
        extra_field = run_cegar.pool_document(triples, 1, "none")
        extra_field["note"] = "not part of the schema"
        extra_field_path.write_text(json.dumps(extra_field))
        try:
            run_cegar.load_pool(extra_field_path, 1, "none")
        except ValueError:
            pass
        else:
            raise AssertionError("extra pool field was accepted")

        try:
            run_cegar.run(
                upper=1,
                add_per_iteration=4,
                time_limit_s=10,
                workers=1,
                random_seed=1,
                symmetry="none",
                max_iterations=0,
                pool_path=pool_path,
                result_path=pool_path,
                trace_path=None,
            )
        except ValueError:
            pass
        else:
            raise AssertionError("aliased pool and result paths were accepted")
    return 6


def test_evaluator_cli() -> int:
    with tempfile.TemporaryDirectory(prefix="parkability-evaluate-") as directory:
        output = Path(directory) / "landscape.json"
        details = Path(directory) / "bases.jsonl"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tracks" / "parkability" / "evaluate.py"),
                str(ROOT / "results" / "tb4.json"),
                "--output",
                str(output),
                "--details",
                str(details),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(output.read_text())
        detail_bytes = details.read_bytes()
        if result["details"]["records"] != 167:
            raise AssertionError("evaluator detail record count changed")
        if result["details"]["sha256"] != hashlib.sha256(detail_bytes).hexdigest():
            raise AssertionError("evaluator output does not bind details")
        if detail_bytes.count(b"\n") != result["efx0_base_count"]:
            raise AssertionError("evaluator details are incomplete")
    return 3


def test_full_cell_cpsat_pool_initialization() -> int:
    universe = ("a", "b", "c")
    supported = {"a"}
    select = run_distinct_half_full_cell_cpsat_cegar.initial_seeded_partitions
    if select(universe, supported, "union", True) != {"a"}:
        raise AssertionError("seed-union initialization changed")
    if select(universe, supported, "complement", True) != {"b", "c"}:
        raise AssertionError("seed-complement initialization changed")
    if select(universe, supported, "complement", False):
        raise AssertionError("pool-only initialization imported the full universe")
    expected_family_sizes = {
        "all": 840,
        "six_orbit": 624,
        "eight_orbit": 780,
        "common_uu_fan": 54,
    }
    for family, expected_size in expected_family_sizes.items():
        if (
            len(run_distinct_half_full_cell_cegar.favorite_pair_universe(family))
            != expected_size
        ):
            raise AssertionError("favorite-pair partition family census changed")
    return 7


def test_bottom_pair_support_encoding() -> int:
    three_agents = (
        (20, 10, 9, 8, 7, 6, 5, 2, 1),
        (20, 9, 10, 8, 7, 6, 5, 2, 1),
        (20, 9, 8, 10, 7, 6, 5, 2, 1),
        (20, 10, 9, 8, 7, 2, 1, 6, 5),
    )
    at_most_two = (
        *three_agents[:2],
        (20, 10, 9, 8, 7, 2, 1, 6, 5),
        (20, 10, 9, 8, 7, 2, 1, 5, 6),
    )
    for values, expected_status in (
        (three_agents, "UNSAT"),
        (at_most_two, "SAT"),
    ):
        has_three = bool(
            run_distinct_half_full_cell_cegar.three_agent_bottom_pairs(values)
        )
        if has_three != (expected_status == "UNSAT"):
            raise AssertionError("three-agent bottom-pair census changed")
        exact = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=values)
        exact_metadata = (
            run_distinct_half_full_cell_cegar.add_no_three_agent_bottom_pair(
                exact
            )
        )
        if exact_metadata != {
            "candidate_bottom_pairs": 28,
            "candidate_agent_triples_per_pair": 4,
            "strict_nonbottom_terms_per_agent_triple": 36,
        }:
            raise AssertionError("exact three-agent bottom encoding size changed")
        if exact.solve(time_limit_s=10).status != expected_status:
            raise AssertionError("exact three-agent bottom semantics changed")

        model = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpModel()
        cap = max(max(row) for row in values)
        variables = tuple(
            tuple(
                model.NewIntVar(1, cap, f"bottom_test_{agent}_{good}")
                for good in range(9)
            )
            for agent in range(4)
        )
        for agent, row in enumerate(values):
            for good, value in enumerate(row):
                model.Add(variables[agent][good] == value)
        cp_metadata = (
            run_distinct_half_full_cell_cpsat_cegar.add_no_three_agent_bottom_pair(
                model, variables
            )
        )
        if cp_metadata != {
            "candidate_bottom_pairs": 28,
            "bottom_support_literals": 112,
            "strict_nonbottom_witness_literals": 1344,
            "maximum_agents_per_bottom_pair": 2,
        }:
            raise AssertionError("CP three-agent bottom encoding size changed")
        cp_status = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpSolver().Solve(
            model
        )
        expected_cp = (
            run_distinct_half_full_cell_cpsat_cegar.cp_model.INFEASIBLE
            if expected_status == "UNSAT"
            else run_distinct_half_full_cell_cpsat_cegar.cp_model.OPTIMAL
        )
        if cp_status != expected_cp:
            raise AssertionError("CP three-agent bottom semantics changed")
    return 4


def test_two_pair_bottom_matching_orbits() -> int:
    disjoint = (
        decide_two_pair_bottom_cross_conversion.disjoint_matching_orbits()
    )
    overlap = (
        decide_two_pair_bottom_cross_conversion.overlap_matching_orbits()
    )
    if len(disjoint) != 9:
        raise AssertionError("disjoint bottom-pair orbit census changed")
    if len(overlap) != 4:
        raise AssertionError("overlap bottom-pair orbit census changed")
    if len(
        run_two_pair_bottom_cross_cegar.target_universe(
            "overlap", (6, 8), "shared_low_triple"
        )
    ) != 315:
        raise AssertionError("shared-low-triple family census changed")
    if len(
        run_two_pair_bottom_cross_cegar.target_universe(
            "overlap", (6, 8), "shared_low_active"
        )
    ) != 420:
        raise AssertionError("shared-low-active family census changed")
    resume = json.loads(
        (
            ROOT
            / "results"
            / "efx49_two_pair_bottom_cross_overlap_orbit1_"
            "shared_active_cegar_session1.json"
        ).read_text()
    )
    first_matching, second_lows, _, second_matching, _ = (
        decide_two_pair_bottom_cross_conversion.cells("overlap", 1)
    )
    active_universe = (
        run_two_pair_bottom_cross_cegar.target_universe(
            "overlap", second_lows, "shared_low_active"
        )
    )
    active_set = set(active_universe)
    initial_pool = tuple(
        partition
        for partition in dict.fromkeys(
            (
                *decide_two_pair_bottom_cross_conversion.conversions(
                    decide_two_pair_bottom_cross_conversion.FIRST_LOWS,
                    first_matching,
                ),
                *decide_two_pair_bottom_cross_conversion.conversions(
                    second_lows,
                    second_matching,
                ),
            )
        )
        if partition in active_set
    )
    if len(
        run_two_pair_bottom_cross_cegar.reconstruct_trace_pool(
            resume, active_universe, initial_pool
        )
    ) != 107:
        raise AssertionError("cross-pair resume pool changed")
    for pattern, orbits in (("disjoint", disjoint), ("overlap", overlap)):
        for orbit_index, expected in enumerate(orbits):
            first, _, _, second, orbit_count = (
                decide_two_pair_bottom_cross_conversion.cells(
                    pattern, orbit_index
                )
            )
            if (first, second) != expected or orbit_count != len(orbits):
                raise AssertionError("bottom-pair orbit lookup changed")
    return len(disjoint) + len(overlap) + 3


def test_bottom_pair_pattern_census() -> int:
    patterns = run_bottom_pair_pattern_selector_cegar.CANONICAL_PATTERNS
    if len(patterns) != 20:
        raise AssertionError("bottom-pair pattern census changed")

    def canonical(pattern):
        vertices = sorted({vertex for edge in pattern for vertex in edge})
        signatures = []
        for image in itertools.permutations(range(len(vertices))):
            mapping = dict(zip(vertices, image))
            signatures.append(
                tuple(
                    sorted(
                        tuple(sorted((mapping[left], mapping[right])))
                        for left, right in pattern
                    )
                )
            )
        return min(signatures)

    signatures = [canonical(pattern) for pattern in patterns]
    if len(set(signatures)) != len(patterns):
        raise AssertionError("bottom-pair patterns are not pairwise distinct")

    for pattern_index, expected, group_size, orbit_count, expected_source_count in (
        (0, 165, 240, 4, 30),
        (1, 228, 48, 16, 45),
        (2, 225, 240, 5, 45),
        (3, 240, 48, 13, 45),
        (4, 240, 24, 26, 45),
        (5, 255, 12, 41, 45),
        (6, 180, 192, 4, 30),
        (7, 255, 24, 24, 45),
        (8, 270, 32, 20, 45),
        (14, 300, 192, 5, 60),
        (19, 360, 384, 4, 60),
    ):
        pattern = run_bottom_pair_pattern_selector_cegar.goods_pattern(
            pattern_index
        )
        selected_pairs = tuple(dict.fromkeys(pattern))
        closure, source_count = (
            decide_bottom_pattern_conversion_selector.conversion_closure(
                selected_pairs
            )
        )
        if len(closure) != expected or source_count != expected_source_count:
            raise AssertionError("bottom-pair conversion census changed")
        group = audit_bottom_pattern_conversion_orbits.automorphisms(pattern)
        orbits = audit_bottom_pattern_conversion_orbits.partition_orbits(
            closure, group
        )
        if len(group) != group_size or len(orbits) != orbit_count:
            raise AssertionError("bottom-pair conversion orbits changed")
        if pattern_index == 0 and tuple(
            map(
                len,
                decide_bottom_pattern_conversion_selector.overlap_conversion_orbits(
                    closure
                ),
            )
        ) != (15, 60, 30, 60):
            raise AssertionError("overlap selector orbit census changed")
        selector_orbits = (
            decide_bottom_pattern_conversion_selector.pattern_conversion_orbits(
                pattern, closure
            )
        )
        if tuple(map(len, selector_orbits)) != tuple(
            len(orbit) for _, orbit in orbits
        ):
            raise AssertionError("generic selector orbit census changed")
    multiplicities = Counter(
        run_bottom_pair_pattern_selector_cegar.multiplicity_signature(pattern)
        for pattern in patterns
    )
    if multiplicities != Counter(
        {(1, 1, 1, 1): 11, (2, 1, 1): 7, (2, 2): 2}
    ):
        raise AssertionError("bottom-pair multiplicity census changed")
    if run_bottom_pair_pattern_selector_cegar.select_obstructions(
        tuple(range(10)), 4, "spread"
    ) != (0, 3, 6, 9):
        raise AssertionError("spread obstruction selection changed")

    canonical_overlap = (
        (100, 3, 20, 23, 68, 67, 66, 63, 58),
        (100, 1, 17, 27, 68, 70, 69, 60, 60),
        (100, 4, 86, 8, 60, 74, 57, 52, 54),
        (100, 5, 78, 14, 67, 63, 61, 55, 58),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_overlap
    )
    symmetry = (
        decide_bottom_pattern_conversion_selector.add_overlap_pattern_symmetry(
            symmetry_master
        )
    )
    if symmetry["group_size"] != 960:
        raise AssertionError("overlap-pattern symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical overlap profile violates symmetry cuts")

    canonical_star = (
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 10, 1, 10, 15, 14, 13, 12),
        (100, 1, 10, 10, 1, 15, 14, 13, 12),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_star
    )
    symmetry = (
        decide_bottom_pattern_conversion_selector.add_star_repeated_pattern_symmetry(
            symmetry_master
        )
    )
    if symmetry["group_size"] != 96:
        raise AssertionError("star-repeated symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical star profile violates symmetry cuts")

    canonical_path = (
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 10, 1, 10, 15, 14, 13, 12),
        (100, 10, 1, 10, 1, 15, 14, 13, 12),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_path
    )
    symmetry = (
        decide_bottom_pattern_conversion_selector.add_path_repeated_pattern_symmetry(
            symmetry_master
        )
    )
    if symmetry["group_size"] != 96:
        raise AssertionError("path-repeated symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical path profile violates symmetry cuts")

    canonical_end_path = (
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 1, 9, 9, 20, 19, 18, 17),
        (100, 1, 10, 1, 10, 15, 14, 13, 12),
        (100, 10, 10, 1, 1, 15, 14, 13, 12),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_end_path
    )
    symmetry = (
        decide_bottom_pattern_conversion_selector.add_end_repeated_path_pattern_symmetry(
            symmetry_master
        )
    )
    if symmetry["group_size"] != 48:
        raise AssertionError("end-repeated-path symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical end-path profile violates symmetry cuts")

    canonical_detached = (
        (100, 1, 1, 9, 9, 9, 20, 19, 18),
        (100, 1, 1, 9, 9, 9, 20, 19, 18),
        (100, 1, 10, 1, 10, 10, 15, 14, 13),
        (100, 10, 10, 10, 1, 1, 15, 14, 13),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_detached
    )
    symmetry = decide_bottom_pattern_conversion_selector.add_detached_edge_repeated_pattern_symmetry(
        symmetry_master
    )
    if symmetry["group_size"] != 24:
        raise AssertionError("detached-edge symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical detached-edge profile violates symmetry cuts")

    canonical_disconnected_fork = (
        (100, 1, 1, 9, 9, 9, 20, 19, 18),
        (100, 1, 1, 9, 9, 9, 20, 19, 18),
        (100, 10, 10, 1, 1, 10, 15, 14, 13),
        (100, 10, 10, 1, 10, 1, 15, 14, 13),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_disconnected_fork
    )
    symmetry = decide_bottom_pattern_conversion_selector.add_disconnected_fork_repeated_pattern_symmetry(
        symmetry_master
    )
    if symmetry["group_size"] != 48:
        raise AssertionError("disconnected-fork symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical disconnected-fork profile violates symmetry cuts")

    canonical_three_edges = (
        (100, 1, 1, 9, 9, 9, 9, 20, 19),
        (100, 1, 1, 9, 9, 9, 9, 20, 19),
        (100, 10, 10, 1, 1, 10, 10, 15, 14),
        (100, 10, 10, 10, 10, 1, 1, 15, 14),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_three_edges
    )
    symmetry = decide_bottom_pattern_conversion_selector.add_three_disconnected_edges_pattern_symmetry(
        symmetry_master
    )
    if symmetry["group_size"] != 64:
        raise AssertionError("three-disconnected-edges symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical three-edge profile violates symmetry cuts")

    canonical_four_edges = (
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_four_edges
    )
    symmetry = decide_bottom_pattern_conversion_selector.add_four_disconnected_edges_pattern_symmetry(
        symmetry_master
    )
    if symmetry["group_size"] != 384:
        raise AssertionError("four-disconnected-edges symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical four-edge profile violates symmetry cuts")

    canonical_four_cycle = (
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
        (100, 1, 1, 1, 1, 1, 1, 1, 1),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_four_cycle
    )
    symmetry = decide_bottom_pattern_conversion_selector.add_four_cycle_pattern_symmetry(
        symmetry_master
    )
    if symmetry["group_size"] != 192:
        raise AssertionError("four-cycle symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical four-cycle profile violates symmetry cuts")

    expected_distinct_groups = {
        9: 144,
        10: 48,
        11: 12,
        12: 24,
        13: 72,
        14: 192,
        15: 12,
        16: 8,
        17: 16,
        18: 16,
        19: 384,
    }
    for pattern_index, expected_group in expected_distinct_groups.items():
        symmetry_master = lra_master.ParkabilityLRAMaster(
            4, 9, fixed_values=canonical_four_edges
        )
        symmetry = decide_bottom_pattern_conversion_selector.add_pattern_symmetry(
            symmetry_master, pattern_index, "all_distinct_canonical"
        )
        if (
            symmetry["group_size"] != expected_group
            or symmetry["goods_automorphism_count"] != expected_group
        ):
            raise AssertionError("generic all-distinct symmetry group changed")
        if symmetry_master.solve(time_limit_s=5).status != "SAT":
            raise AssertionError("generic all-distinct profile violates symmetry cuts")

    canonical_triangle = (
        (100, 1, 1, 9, 20, 19, 18, 17, 16),
        (100, 1, 1, 9, 20, 19, 18, 17, 16),
        (100, 1, 10, 1, 15, 14, 13, 12, 11),
        (100, 10, 1, 1, 15, 14, 13, 12, 11),
    )
    symmetry_master = lra_master.ParkabilityLRAMaster(
        4, 9, fixed_values=canonical_triangle
    )
    symmetry = (
        decide_bottom_pattern_conversion_selector.add_triangle_repeated_pattern_symmetry(
            symmetry_master
        )
    )
    if symmetry["group_size"] != 480:
        raise AssertionError("triangle-repeated symmetry group changed")
    if symmetry_master.solve(time_limit_s=5).status != "SAT":
        raise AssertionError("canonical triangle profile violates symmetry cuts")
    return len(patterns) + 21


def test_full_cell_singleton_encoding() -> int:
    all_cells = (
        (16, 10, 10, 10, 10, 7, 5, 5, 4),
        (9, 5, 5, 5, 5, 5, 3, 2, 1),
        (9, 5, 5, 5, 5, 5, 3, 2, 1),
        (7, 4, 4, 4, 4, 4, 2, 2, 2),
    )
    one_missing = (
        (21016, 10532, 15702, 18479, 15894, 18671, 5266, 18239, 2537),
        (945, 4, 571, 581, 370, 362, 931, 744, 756),
        (31588, 10508, 13183, 18405, 28977, 23755, 23627, 7961, 10444),
        (3914, 683, 48, 1366, 2636, 3239, 3906, 1969, 3295),
    )
    cases = 0
    for values, expected_cells, expected_status in (
        (all_cells, 28, "SAT"),
        (one_missing, 27, "UNSAT"),
    ):
        cells = run_distinct_half_full_cell_cegar.singleton_failure_cells(values)
        if len(cells) != expected_cells:
            raise AssertionError("singleton Hall-cell census changed")
        candidate = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=values)
        metadata = (
            run_distinct_half_full_cell_cegar.add_all_cells_singleton_failure(
                candidate
            )
        )
        if metadata != {
            "low_pair_cells": 28,
            "candidate_singleton_witness_edges": 420,
        }:
            raise AssertionError("singleton Hall-cell encoding size changed")
        if candidate.solve(time_limit_s=10).status != expected_status:
            raise AssertionError("singleton Hall-cell encoding changed semantics")
        model = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpModel()
        cap = max(max(row) for row in values)
        variables = tuple(
            tuple(
                model.NewIntVar(1, cap, f"singleton_test_{agent}_{good}")
                for good in range(9)
            )
            for agent in range(4)
        )
        for agent, row in enumerate(values):
            for good, value in enumerate(row):
                model.Add(variables[agent][good] == value)
        cp_metadata = (
            run_distinct_half_full_cell_cpsat_cegar.add_all_cells_singleton_failures(
                model, variables, cap
            )
        )
        if cp_metadata != metadata:
            raise AssertionError("CP singleton Hall-cell encoding size changed")
        cp_status = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpSolver().Solve(
            model
        )
        expected_cp_status = (
            run_distinct_half_full_cell_cpsat_cegar.cp_model.OPTIMAL
            if expected_status == "SAT"
            else run_distinct_half_full_cell_cpsat_cegar.cp_model.INFEASIBLE
        )
        if cp_status != expected_cp_status:
            raise AssertionError("CP singleton Hall-cell encoding changed semantics")
        cases += 2
    rr_cells = tuple(itertools.combinations(range(1, 5), 2))
    for values, constraint, expected_status in (
        (
            all_cells,
            lambda candidate: (
                run_distinct_half_full_cell_cegar.add_singleton_failure_cells(
                    candidate, rr_cells
                )
            ),
            "SAT",
        ),
        (
            one_missing,
            lambda candidate: (
                run_distinct_half_full_cell_cegar.add_singleton_failure_cells(
                    candidate, rr_cells
                )
            ),
            "UNSAT",
        ),
        (
            all_cells,
            lambda candidate: (
                run_distinct_half_full_cell_cegar.add_no_singleton_failure_cell(
                    candidate, (1, 2)
                )
            ),
            "UNSAT",
        ),
        (
            one_missing,
            lambda candidate: (
                run_distinct_half_full_cell_cegar.add_no_singleton_failure_cell(
                    candidate, (1, 2)
                )
            ),
            "SAT",
        ),
    ):
        candidate = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=values)
        constraint(candidate)
        if candidate.solve(time_limit_s=10).status != expected_status:
            raise AssertionError("RR Hall-cell split changed semantics")
        cases += 1
    for values, expected_status in (
        (all_cells, "SAT"),
        (one_missing, "UNSAT"),
    ):
        semantic = (
            run_distinct_half_full_cell_cegar.common_rr_uu_singleton_witness(
                values
            )
        )
        if semantic != (expected_status == "SAT"):
            raise AssertionError("common UU witness semantic check changed")
        candidate = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=values)
        metadata = (
            run_distinct_half_full_cell_cegar.add_common_rr_uu_singleton_witness(
                candidate
            )
        )
        if metadata != {
            "edge": [5, 6],
            "rr_low_pair_cells": 6,
            "rejection_constraints": 24,
        }:
            raise AssertionError("common UU witness encoding size changed")
        if candidate.solve(time_limit_s=10).status != expected_status:
            raise AssertionError("common UU witness encoding changed semantics")
        cp = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpModel()
        cap = max(max(row) for row in values)
        variables = tuple(
            tuple(
                cp.NewIntVar(1, cap, f"common_uu_{agent}_{good}")
                for good in range(9)
            )
            for agent in range(4)
        )
        for agent, row in enumerate(values):
            for good, value in enumerate(row):
                cp.Add(variables[agent][good] == value)
        cp_metadata = (
            run_distinct_half_full_cell_cpsat_cegar.add_common_rr_uu_singleton_witness(
                cp, variables, cap
            )
        )
        if cp_metadata != metadata:
            raise AssertionError("CP common UU witness encoding size changed")
        cp_status = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpSolver().Solve(
            cp
        )
        if (cp_status == run_distinct_half_full_cell_cpsat_cegar.cp_model.OPTIMAL) != (
            expected_status == "SAT"
        ):
            raise AssertionError("CP common UU witness encoding changed semantics")
        cases += 1
    mapped = (1, 1, 1, 1)
    if not (
        run_distinct_half_full_cell_cegar.second_smallest_representative_map_holds(
            all_cells, mapped
        )
    ):
        raise AssertionError("second-smallest map semantic check changed")
    candidate = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=all_cells)
    mapped_metadata = (
        run_distinct_half_full_cell_cegar.add_common_rr_uu_singleton_witness(
            candidate, mapping=mapped
        )
    )
    if mapped_metadata != {
        "edge": [5, 6],
        "rr_low_pair_cells": 6,
        "rejection_constraints": 4,
        "second_smallest_map_encoding": {
            "representative_map": [1, 1, 1, 1],
            "order_constraints": 16,
        },
    }:
        raise AssertionError("second-smallest map encoding size changed")
    if candidate.solve(time_limit_s=10).status != "SAT":
        raise AssertionError("second-smallest map encoding changed semantics")
    cases += 1
    for values, expected_status in (
        (all_cells, "UNSAT"),
        (one_missing, "SAT"),
    ):
        semantic = not (
            run_distinct_half_full_cell_cegar.common_rr_uu_singleton_witnesses(
                values
            )
        )
        if semantic != (expected_status == "SAT"):
            raise AssertionError("no-common-UU semantic check changed")
        candidate = lra_master.ParkabilityLRAMaster(4, 9, fixed_values=values)
        metadata = (
            run_distinct_half_full_cell_cegar.add_no_common_rr_uu_singleton_witness(
                candidate
            )
        )
        if metadata != {
            "unmatched_edges": 6,
            "nonwitness_constraints": 6,
        }:
            raise AssertionError("no-common-UU encoding size changed")
        if candidate.solve(time_limit_s=10).status != expected_status:
            raise AssertionError("no-common-UU encoding changed semantics")
        cp = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpModel()
        cap = max(max(row) for row in values)
        variables = tuple(
            tuple(
                cp.NewIntVar(1, cap, f"no_common_uu_{agent}_{good}")
                for good in range(9)
            )
            for agent in range(4)
        )
        for agent, row in enumerate(values):
            for good, value in enumerate(row):
                cp.Add(variables[agent][good] == value)
        cp_metadata = (
            run_distinct_half_full_cell_cpsat_cegar.add_no_common_rr_uu_singleton_witness(
                cp, variables
            )
        )
        if cp_metadata != {
            "unmatched_edges": 6,
            "nonwitness_constraints": 6,
            "witness_literals": 144,
        }:
            raise AssertionError("CP no-common-UU encoding size changed")
        cp_status = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpSolver().Solve(
            cp
        )
        if (cp_status == run_distinct_half_full_cell_cpsat_cegar.cp_model.OPTIMAL) != (
            expected_status == "SAT"
        ):
            raise AssertionError("CP no-common-UU encoding changed semantics")
        cases += 1
    selected = lra_master.ParkabilityLRAMaster(4, 9)
    selected_metadata = run_distinct_half_full_cell_cegar.add_no_full_hall_cell(
        selected, [(1, 2)]
    )
    if selected_metadata != {
        "low_pair_cells": 1,
        "accept_literals": 60,
        "pairing_failure_terms": 15,
        "hall_failure_templates_per_pairing": 21,
    }:
        raise AssertionError("selected exact Hall-cell encoding size changed")
    selected_cp = run_distinct_half_full_cell_cpsat_cegar.cp_model.CpModel()
    selected_values = tuple(
        tuple(
            selected_cp.NewIntVar(1, 20, f"selected_cell_{agent}_{good}")
            for good in range(9)
        )
        for agent in range(4)
    )
    selected_cp_metadata = (
        run_distinct_half_full_cell_cpsat_cegar.add_no_full_hall_cells(
            selected_cp, selected_values, 20, low_pairs=[(1, 2)]
        )
    )
    if (
        selected_cp_metadata["low_pair_cells"] != 1
        or selected_cp_metadata["accept_literals"] != 60
        or selected_cp_metadata["hall_witness_literals"] != 315
    ):
        raise AssertionError("selected CP Hall-cell encoding size changed")
    cases += 2
    return cases


def test_terminal_matching_orbits() -> int:
    if decide_distinct_half_terminal_exchange.parse_low_pair("1,2") != (1, 2):
        raise AssertionError("terminal low-pair parser changed")
    all_matchings = set(itertools.permutations(range(4)))

    def act(matching, agent_permutation, bundle_permutation):
        transformed = [None] * 4
        for agent in range(4):
            transformed[agent_permutation[agent]] = bundle_permutation[
                matching[agent]
            ]
        return tuple(transformed)

    covered_r = set()
    for representative in (
        decide_distinct_half_terminal_exchange.TERMINAL_MATCHING_REPRESENTATIVES[
            "R"
        ]
    ):
        for residual_agents in itertools.permutations((1, 2, 3)):
            for residual_pairs in ((0, 1, 2, 3), (0, 1, 3, 2)):
                covered_r.add(
                    act(representative, (0,) + residual_agents, residual_pairs)
                )
    covered_u = set()
    for representative in (
        decide_distinct_half_terminal_exchange.TERMINAL_MATCHING_REPRESENTATIVES[
            "U"
        ]
    ):
        for triple_agents in itertools.permutations((0, 1, 2)):
            covered_u.add(
                act(representative, triple_agents + (3,), (0, 1, 2, 3))
            )
    if covered_r != all_matchings or covered_u != all_matchings:
        raise AssertionError("terminal matching orbit census changed")
    expected_stabilizer_census = {
        "R": ((8, 28), (8, 28), (4, 54)),
        "U": ((2, 87), (2, 87), (2, 87), (2, 87)),
    }
    terminal_exchange = decide_distinct_half_terminal_exchange
    for case, representatives in (
        terminal_exchange.TERMINAL_MATCHING_REPRESENTATIVES.items()
    ):
        for orbit_position, matching in enumerate(representatives):
            good_permutations = terminal_exchange.terminal_stabilizer_good_permutations(
                case, matching
            )
            target_orbits = terminal_exchange.target_partition_orbits(
                case, matching, "radius2"
            )
            expected_group, expected_orbits = expected_stabilizer_census[case][
                orbit_position
            ]
            if (
                len(good_permutations) != expected_group
                or len(target_orbits) != expected_orbits
                or sum(map(len, target_orbits)) != 138
            ):
                raise AssertionError("terminal stabilizer census changed")
    for case, partition in (
        decide_distinct_half_terminal_exchange.TERMINAL_PARTITIONS.items()
    ):
        if len(
            decide_distinct_half_terminal_exchange.exchange_neighbors(partition)
        ) != 12:
            raise AssertionError("terminal exchange-neighbor census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "eight_orbit", partition
            )
        ) != 780:
            raise AssertionError("terminal target family census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "radius2", partition
            )
        ) != 138:
            raise AssertionError("terminal radius-two family census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "radius2_same_favorite", partition
            )
        ) != {"R": 66, "U": 57}[case]:
            raise AssertionError("same-favorite radius-two census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "radius2_new_favorite_partner", partition
            )
        ) != {"R": 72, "U": 81}[case]:
            raise AssertionError("new-partner radius-two census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "radius2_triple_partner", partition
            )
        ) != {"R": 36, "U": 42}[case]:
            raise AssertionError("triple-partner radius-two census changed")
        if len(
            decide_distinct_half_terminal_exchange.target_partitions(
                "same_favorite", partition
            )
        ) != {"R": 102, "U": 93}[case]:
            raise AssertionError("same-favorite target census changed")
    return 4


def main() -> None:
    test_literal_zero_semantics()
    cases, triples = test_small_differential()
    test_basin1_regression()
    master_cases = test_master_cuts()
    lra_cases = test_lra_master()
    integer_partition_cases = test_integer_partition_master()
    fast_cases = test_fast_count()
    lexmax_partial_cases = test_lexmax_partial_encoding()
    adaptive_priority_cases = test_adaptive_priority_helpers()
    small_static, target_static = test_one_nonsingleton_certificates()
    source_census_cases = test_source_census()
    normal_form_matrices, normal_form_allocations = (
        test_threshold_cycle_normal_form()
    )
    favorite_pair_cases = test_favorite_pair_construction()
    complementary_wall_cases = test_complementary_wall()
    partition_count, partition_encoding_cases = test_partition_reduction()
    anchored49_count = test_anchored49_family()
    stabilizer_guard_cases = test_ranking_cell_stabilizer_guard()
    generic_scope_cases = test_generic_partition_scope()
    standard_hall_cases = test_standard_hall_smt2()
    aggregate_selector_cases = test_aggregate_minimum_selector_helpers()
    complete_efx_pool_cases = test_complete_efx_lra_pool()
    double_lex_cases, orbit_cases = test_double_lex()
    runner_cases = test_pool_and_runner()
    pool_initialization_cases = test_full_cell_cpsat_pool_initialization()
    bottom_pair_cases = test_bottom_pair_support_encoding()
    bottom_pair_orbits = test_two_pair_bottom_matching_orbits()
    bottom_pair_patterns = test_bottom_pair_pattern_census()
    singleton_cell_cases = test_full_cell_singleton_encoding()
    terminal_matching_cases = test_terminal_matching_orbits()
    evaluator_cases = test_evaluator_cli()
    print(
        f"PASS parkability differential: {cases} small matrices, "
        f"{triples} small triples, basin-1 exact regression, "
        f"{master_cases} master cases, {double_lex_cases} DoubleLex encodings, "
        f"{lra_cases} LRA cases, "
        f"{integer_partition_cases} integer-partition cases, "
        f"{fast_cases} vectorized counts, "
        f"{lexmax_partial_cases} lex-max partial-EFX checks, "
        f"{adaptive_priority_cases} adaptive-priority helper checks, "
        f"{small_static}+{target_static} static shape certificates, "
        f"{source_census_cases} source-census obstruction, "
        f"{normal_form_allocations} threshold-normal forms on "
        f"{normal_form_matrices} matrices, "
        f"{favorite_pair_cases} favorite-pair constructions, "
        f"{complementary_wall_cases} complementary-wall points, "
        f"{partition_count} unlabeled partitions, "
        f"{partition_encoding_cases} partition encodings, "
        f"{anchored49_count} anchored 4x9 partitions, "
        f"{stabilizer_guard_cases} ranking-cell stabilizer guard, "
        f"{generic_scope_cases} generic partition-scope check, "
        f"{standard_hall_cases} standard Hall-SMT checks, "
        f"{aggregate_selector_cases} aggregate-selector helpers, "
        f"{complete_efx_pool_cases} direct-EFX pool records, "
        f"{orbit_cases} DoubleLex orbits, {runner_cases} runner cases, "
        f"{pool_initialization_cases} pool-initialization cases, "
        f"{bottom_pair_cases} bottom-pair support cases, "
        f"{bottom_pair_orbits} two-pair matching orbits, "
        f"{bottom_pair_patterns} bottom-pair patterns, "
        f"{singleton_cell_cases} singleton-cell cases, "
        f"{terminal_matching_cases} terminal-matching cases, "
        f"{evaluator_cases} evaluator cases"
    )


if __name__ == "__main__":
    main()
