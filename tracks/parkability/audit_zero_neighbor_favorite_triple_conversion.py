#!/usr/bin/env python3
"""Audit the zero-neighbor conversion exposed by the three-repair boundary."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
    )
    from .optimize_distinct_half_eight_orbit_cpsat import canonicalize_hint
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_two_core_cegar import perfect_pairings
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
    )
    from optimize_distinct_half_eight_orbit_cpsat import canonicalize_hint
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_two_core_cegar import perfect_pairings
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "zero-neighbor-favorite-triple-conversion-audit-v1"
N = 4
M = 9
FAVORITE = 0
LOW_PAIR = (7, 8)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_partition(*bundles):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in bundles))


def conversion_holds(values, high, low, edge, other_pairs):
    if any(row[high] < row[low] for row in values):
        return False
    left, right = edge
    for row in values:
        edge_value = row[left] + row[right]
        threshold = max(
            row[FAVORITE],
            edge_value,
            row[low] + max(row[left], row[right]),
        )
        if (
            edge_value >= row[FAVORITE] + row[high]
            or edge_value + row[low] < row[FAVORITE]
            or any(sum(row[good] for good in pair) < threshold for pair in other_pairs)
        ):
            return False
    return True


def zero_neighbor_conversions(values):
    conversions = set()
    for lows in itertools.combinations(range(1, M), 2):
        orientations = []
        if all(row[lows[0]] >= row[lows[1]] for row in values):
            orientations.append(lows)
        if all(row[lows[1]] >= row[lows[0]] for row in values):
            orientations.append(tuple(reversed(lows)))
        residual = tuple(good for good in range(1, M) if good not in lows)
        for high, low in orientations:
            for matching in perfect_pairings(residual):
                for edge in matching:
                    other_pairs = tuple(
                        pair for pair in matching if pair != edge
                    )
                    if conversion_holds(values, high, low, edge, other_pairs):
                        conversions.add(
                            canonical_partition(
                                (FAVORITE, high), (*edge, low), *other_pairs
                            )
                        )
    return tuple(sorted(conversions))


def audit_profile(path: Path):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    if len(values) != N or any(len(row) != M for row in values):
        raise AssertionError("profile dimensions changed")
    audit_branch(values)
    if full_hall_cells(values):
        raise AssertionError("profile gained a full Hall cell")

    six_repairs = supported_partitions(
        values, list(favorite_pair_universe("six_orbit"))
    )
    all_favorite_pair_repairs = tuple(
        supported_partitions(values, list(favorite_pair_universe("all")))
    )
    if six_repairs or len(all_favorite_pair_repairs) != 3:
        raise AssertionError("three-repair boundary changed")

    residual = tuple(good for good in range(1, M) if good not in LOW_PAIR)
    matchings = tuple(perfect_pairings(residual))
    good_matchings = tuple(
        matching
        for matching in matchings
        if pairing_has_hall_matching(values, LOW_PAIR, matching)
    )
    bad_matchings = tuple(
        matching for matching in matchings if matching not in good_matchings
    )
    if len(matchings) != 15 or len(good_matchings) != 12 or len(bad_matchings) != 3:
        raise AssertionError("12+3 Hall-cell boundary changed")

    zero_edges = []
    for matching in bad_matchings:
        candidates = tuple(
            edge
            for edge in matching
            if all(
                sum(row[good] for good in edge)
                < row[FAVORITE] + max(row[good] for good in LOW_PAIR)
                for row in values
            )
        )
        if len(candidates) != 1:
            raise AssertionError("bad matching lost its unique zero-neighbor edge")
        zero_edges.append(candidates[0])
    if len(set(zero_edges)) != 1:
        raise AssertionError("bad pairings no longer share one edge")
    edge = zero_edges[0]

    if all(row[7] > row[8] for row in values):
        high, low = 7, 8
    elif all(row[8] > row[7] for row in values):
        high, low = 8, 7
    else:
        raise AssertionError("low pair lost its common strict orientation")

    conversions = []
    for matching in bad_matchings:
        other_pairs = tuple(pair for pair in matching if pair != edge)
        if not conversion_holds(values, high, low, edge, other_pairs):
            raise AssertionError("zero-neighbor conversion inequalities changed")
        partition = canonical_partition(
            (FAVORITE, high), (*edge, low), *other_pairs
        )
        graph = feasible_graph(values, partition)
        if not all(all(row) for row in graph) or matching_rank(graph) != N:
            raise AssertionError("converted partition is no longer universally EFX")
        conversions.append(partition)
    if set(conversions) != set(all_favorite_pair_repairs):
        raise AssertionError("converted partitions no longer equal all pair repairs")

    all_repairs = []
    balanced_repairs = []
    for partition in core.iter_unlabeled_nonempty_partitions(N, M):
        graph = feasible_graph(values, partition)
        if matching_rank(graph) != N:
            continue
        all_repairs.append(partition)
        if tuple(sorted(map(len, partition), reverse=True)) == (3, 2, 2, 2):
            balanced_repairs.append(partition)
    expected_triples = {
        canonical_partition((FAVORITE, *LOW_PAIR), *matching)
        for matching in good_matchings
    }
    if (
        len(all_repairs) != 15
        or len(balanced_repairs) != 15
        or set(all_repairs) != set(balanced_repairs)
        or set(balanced_repairs) != expected_triples | set(conversions)
        or any(
            not all(all(row) for row in feasible_graph(values, partition))
            for partition in all_repairs
        )
        or independent.count_complete_efx0(values) != 360
    ):
        raise AssertionError("15-partition balanced boundary changed")

    return {
        "path": str(path),
        "sha256": sha256(path),
        "values": [list(row) for row in values],
        "low_pair": list(LOW_PAIR),
        "common_high_low_orientation": [high, low],
        "shared_zero_neighbor_edge": list(edge),
        "hall_valid_pairing_count": len(good_matchings),
        "hall_failed_pairing_count": len(bad_matchings),
        "converted_favorite_pair_count": len(conversions),
        "complete_efx_partition_count": len(all_repairs),
        "balanced_efx_partition_count": len(balanced_repairs),
        "all_feasibility_graphs_complete": True,
        "literal_complete_efx_count": 360,
    }


def audit_negative_control(path: Path):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    audit_branch(values)
    repairs = supported_partitions(
        values, list(favorite_pair_universe("all"))
    )
    if (
        full_hall_cells(values)
        or supported_partitions(
            values, list(favorite_pair_universe("six_orbit"))
        )
        or len(repairs) != 27
        or zero_neighbor_conversions(values)
    ):
        raise AssertionError("zero-neighbor negative control changed")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "favorite_pair_efx_partition_count": len(repairs),
        "zero_neighbor_conversion_count": 0,
        "full_hall_cells": [],
    }


def audit_conditional_optimizer(path: Path):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    hint_path = path.parent / Path(payload["hint_path"]).name
    hint = canonicalize_hint(load_values(hint_path))
    universe = favorite_pair_universe("eight_orbit")
    targets = tuple(supported_partitions(hint, list(universe)))
    target_set = set(targets)
    hard = tuple(partition for partition in universe if partition not in target_set)
    target_repairs = tuple(supported_partitions(values, list(targets)))
    hard_repairs = tuple(supported_partitions(values, list(hard)))
    all_favorite_repairs = tuple(
        supported_partitions(values, list(favorite_pair_universe("all")))
    )
    proto_path = path.parent / Path(payload["proto_path"]).name
    audit_branch(values)
    if (
        payload.get("schema") != "distinct-half-eight-orbit-cpsat-optimization-v1"
        or payload.get("status") != "OPTIMIZATION_CHECKPOINT"
        or payload.get("solver_status") != "FEASIBLE"
        or payload.get("cap") != 100
        or payload.get("hard_partition_family")
        != "hint_eight_orbit_complement"
        or payload.get("hard_partition_count") != 777
        or payload.get("hard_partition_repair_count") != 0
        or payload.get("hint_eight_orbit_repair_count") != 3
        or payload.get("target_partition_count") != 3
        or payload.get("target_repair_count") != 3
        or payload.get("semantic_obstruction_count") != 0
        or payload.get("obstruction_objective") != 0
        or payload.get("obstruction_objective_bound") != 3
        or len(targets) != 3
        or len(target_repairs) != 3
        or len(hard) != 777
        or hard_repairs
        or len(all_favorite_repairs) != 3
        or full_hall_cells(values)
        or independent.count_complete_efx0(values) != 360
        or payload.get("proto_sha256") != sha256(proto_path)
    ):
        raise AssertionError("conditional three-pairing optimizer changed")
    return {
        "path": str(path),
        "sha256": sha256(path),
        "formula_sha256": payload["proto_sha256"],
        "hard_partition_count": len(hard),
        "target_partition_count": len(targets),
        "target_repair_count": len(target_repairs),
        "objective_bound": payload["obstruction_objective_bound"],
        "favorite_pair_efx_partition_count": len(all_favorite_repairs),
        "literal_complete_efx_count": 360,
        "interpretation": (
            "The checkpoint preserves all three targets; its bound still "
            "permits zero repairs and proves no lower bound."
        ),
    }


def symbolic_check(smt2_path: Path):
    names = ("F", "h", "ell", "x", "y", "p1", "p2", "q1", "q2")
    variables = dict(zip(names, z3.Reals(" ".join(names))))
    F = variables["F"]
    h = variables["h"]
    ell = variables["ell"]
    x = variables["x"]
    y = variables["y"]
    pair_p = variables["p1"] + variables["p2"]
    pair_q = variables["q1"] + variables["q2"]
    edge = x + y
    solver = z3.Solver()
    solver.add(*(value > 0 for value in variables.values()))
    solver.add(*(F > variables[name] for name in names if name != "F"))
    solver.add(h >= ell, edge < F + h, edge + ell >= F)
    for pair in (pair_p, pair_q):
        solver.add(pair >= F, pair >= edge, pair >= ell + x, pair >= ell + y)
    bundle_values = (F + h, edge + ell, pair_p, pair_q)
    target_remainders = (
        F,
        h,
        edge,
        ell + x,
        ell + y,
        variables["p1"],
        variables["p2"],
        variables["q1"],
        variables["q2"],
    )
    solver.add(
        z3.Or(
            *(
                own < remainder
                for own in bundle_values
                for remainder in target_remainders
            )
        )
    )
    if solver.check() != z3.unsat:
        raise AssertionError("symbolic zero-neighbor implication is not UNSAT")
    formula = solver.to_smt2()
    smt2_path.parent.mkdir(parents=True, exist_ok=True)
    smt2_path.write_text(formula)
    return {
        "solver": "z3",
        "status": "unsat",
        "smt2_sha256": hashlib.sha256(formula.encode()).hexdigest(),
    }


def run(inputs, negative_controls, conditional_optimizer, output, smt2_path):
    records = [audit_profile(path) for path in inputs]
    negative_records = [
        audit_negative_control(path) for path in negative_controls
    ]
    result = {
        "schema": SCHEMA,
        "status": "ZERO_NEIGHBOR_CONVERSION_BOUNDARIES_AUDITED",
        "profile_count": len(records),
        "profiles": records,
        "negative_control_count": len(negative_records),
        "negative_controls": negative_records,
        "conditional_three_pairing_boundary": audit_conditional_optimizer(
            conditional_optimizer
        ),
        "symbolic_implication": symbolic_check(smt2_path),
        "claim_boundary": (
            "The audit verifies two discovery profiles and the local conversion; "
            "it does not prove that every hard-branch profile contains this motif."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument(
        "--negative-control", type=Path, action="append", default=[]
    )
    parser.add_argument("--conditional-optimizer", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        tuple(args.input),
        tuple(args.negative_control),
        args.conditional_optimizer,
        args.output,
        args.smt2,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
