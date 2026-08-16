#!/usr/bin/env python3
"""Audit the bounded terminal-to-radius-two exchange theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch, build_state_graph
    from .audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from .decide_distinct_half_terminal_exchange import (
        REPRESENTATIVES,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        UNREPRESENTED,
        target_partitions,
    )
    from .decide_distinct_half_terminal_exchange_cpsat import matching_is_efx
    from .run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch, build_state_graph
    from audit_matching_augmentation import (
        canonical_partition,
        feasible_graph,
        matching_rank,
    )
    from decide_distinct_half_terminal_exchange import (
        REPRESENTATIVES,
        TERMINAL_MATCHING_REPRESENTATIVES,
        TERMINAL_PARTITIONS,
        UNREPRESENTED,
        target_partitions,
    )
    from decide_distinct_half_terminal_exchange_cpsat import matching_is_efx
    from run_distinct_half_full_cell_cegar import (
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )


SCHEMA = "distinct-half-terminal-exchange-gate-audit-v2"
RESULT = Path("results/efx49_distinct_half_terminal_exchange_gate_audit.json")
CP_SCHEMA = "distinct-half-terminal-exchange-cpsat-v1"
Z3_SCHEMA = "distinct-half-terminal-exchange-decision-v1"
NONVACUITY_VALUES = (
    (5, 3, 3, 3, 1, 1, 2, 4, 3),
    (5, 3, 3, 3, 4, 4, 1, 2, 1),
    (5, 1, 2, 4, 1, 4, 4, 3, 3),
    (5, 1, 3, 2, 3, 4, 3, 4, 2),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encoded_partition_hash(partitions) -> str:
    encoded = json.dumps(
        [[list(bundle) for bundle in partition] for partition in partitions],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def mapped_partition(partition, agent_permutation, low_permutation):
    good_map = {0: 0}
    good_map.update(
        {
            representative: agent_permutation[representative - 1] + 1
            for representative in REPRESENTATIVES
        }
    )
    good_map.update(
        {
            low: 5 + low_permutation[low - 5]
            for low in UNREPRESENTED
        }
    )
    return canonical_partition(
        tuple(tuple(good_map[good] for good in bundle) for bundle in partition)
    ), good_map


def transformed_matching(
    partition, matching, agent_permutation, low_permutation
):
    transformed_partition, good_map = mapped_partition(
        partition, agent_permutation, low_permutation
    )
    bundle_positions = {
        bundle: position for position, bundle in enumerate(transformed_partition)
    }
    transformed = [None] * 4
    for observer, bundle_position in enumerate(matching):
        mapped_bundle = tuple(
            sorted(good_map[good] for good in partition[bundle_position])
        )
        transformed[agent_permutation[observer]] = bundle_positions[mapped_bundle]
    return tuple(transformed)


def matching_orbit_audit(case):
    partition = TERMINAL_PARTITIONS[case]
    stabilizer = []
    for agent_permutation in itertools.permutations(range(4)):
        for low_permutation in itertools.permutations(range(4)):
            transformed, _ = mapped_partition(
                partition, agent_permutation, low_permutation
            )
            if transformed == partition:
                stabilizer.append((agent_permutation, low_permutation))

    remaining = set(itertools.permutations(range(4)))
    orbits = []
    while remaining:
        seed = min(remaining)
        orbit = {
            transformed_matching(partition, seed, agents, lows)
            for agents, lows in stabilizer
        }
        if not orbit <= remaining:
            raise AssertionError("matching stabilizer orbit overlap changed")
        remaining.difference_update(orbit)
        orbits.append(orbit)

    representatives = TERMINAL_MATCHING_REPRESENTATIVES[case]
    if len(representatives) != len(orbits) or any(
        sum(representative in orbit for orbit in orbits) != 1
        for representative in representatives
    ):
        raise AssertionError(f"{case} matching representatives changed")
    orbit_sizes = sorted(len(orbit) for orbit in orbits)
    expected_sizes = [6, 6, 12] if case == "R" else [6, 6, 6, 6]
    expected_stabilizer = 48 if case == "R" else 12
    if len(stabilizer) != expected_stabilizer or orbit_sizes != expected_sizes:
        raise AssertionError(f"{case} matching orbit census changed")
    return len(stabilizer), orbit_sizes


def audit_cell(case, matching_orbit, targets, target_hash):
    stem = f"efx49_distinct_half_terminal_radius2_{case}_m{matching_orbit}"
    cp_path = Path(f"results/{stem}_cpsat_cap5_nocell_replay.json")
    z3_path = Path(f"results/{stem}_z3_cap5_nocell_replay.json")
    cp = json.loads(cp_path.read_text())
    z3 = json.loads(z3_path.read_text())
    matching = list(TERMINAL_MATCHING_REPRESENTATIVES[case][matching_orbit])
    common = {
        "case": case,
        "target": "radius2",
        "terminal_matching_orbit": matching_orbit,
        "terminal_matching_representative": matching,
        "target_partition_count": len(targets),
        "target_partitions_sha256": target_hash,
        "full_hall_cell_forbidden": False,
        "values": None,
    }
    if any(cp.get(key) != value for key, value in common.items()) or (
        cp.get("schema") != CP_SCHEMA
        or cp.get("status") != "FINITE_CAP_UNSAT_CANDIDATE"
        or cp.get("solver_status") != "INFEASIBLE"
        or cp.get("cap") != 5
        or cp.get("workers") != 1
        or cp.get("full_cell_encoding") is not None
    ):
        raise AssertionError(f"CP-SAT metadata changed for {case}/{matching_orbit}")
    if any(z3.get(key) != value for key, value in common.items()) or (
        z3.get("schema") != Z3_SCHEMA
        or z3.get("status") != "UNSAT_CANDIDATE"
        or z3.get("solver_status") != "unsat"
        or z3.get("integer_cap") != 5
        or z3.get("domain") != "positive integers at most 5"
        or z3.get("full_cell_encoding") is not None
    ):
        raise AssertionError(f"Z3 metadata changed for {case}/{matching_orbit}")

    proto_path = Path(cp["proto_path"])
    smt2_path = Path(z3["smt2_path"])
    if cp.get("proto_sha256") != sha256(proto_path):
        raise AssertionError(f"CP-SAT proto hash changed for {case}/{matching_orbit}")
    if z3.get("smt2_sha256") != sha256(smt2_path):
        raise AssertionError(f"Z3 formula hash changed for {case}/{matching_orbit}")
    return {
        "case": case,
        "matching_orbit": matching_orbit,
        "matching": matching,
        "cp_sat_result": str(cp_path),
        "cp_sat_result_sha256": sha256(cp_path),
        "cp_sat_proto_sha256": cp["proto_sha256"],
        "z3_result": str(z3_path),
        "z3_result_sha256": sha256(z3_path),
        "z3_smt2_sha256": z3["smt2_sha256"],
    }


def audit_nonvacuity():
    values = NONVACUITY_VALUES
    terminal = TERMINAL_PARTITIONS["R"]
    matching = TERMINAL_MATCHING_REPRESENTATIVES["R"][0]
    targets = target_partitions("radius2", terminal)
    audit_branch(values)
    if (
        max(max(row) for row in values) > 5
        or full_hall_cells(values)
        or not matching_is_efx(values, terminal, matching)
    ):
        raise AssertionError("terminal exchange theorem became vacuous")
    target_repairs = tuple(
        partition
        for partition in targets
        if matching_rank(feasible_graph(values, partition)) == 4
    )
    all_repairs = tuple(
        partition
        for partition in favorite_pair_universe("all")
        if matching_rank(feasible_graph(values, partition)) == 4
    )
    if len(target_repairs) != 96 or len(all_repairs) != 592:
        raise AssertionError("nonvacuity witness repair census changed")
    return {
        "case": "R",
        "matching_orbit": 0,
        "values": [list(row) for row in values],
        "radius_two_eight_orbit_repair_count": len(target_repairs),
        "favorite_pair_repair_count": len(all_repairs),
    }


def supporting_count(values, partitions):
    return sum(
        matching_rank(feasible_graph(values, partition)) == 4
        for partition in partitions
    )


def audit_refutation(path, expected_target, expected_cap, expected_counts):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    terminal = TERMINAL_PARTITIONS["R"]
    matching = TERMINAL_MATCHING_REPRESENTATIVES["R"][0]
    audit_branch(values)
    if (
        payload.get("status") != "TERMINAL_SELECTOR_COUNTEREXAMPLE"
        or payload.get("case") != "R"
        or payload.get("terminal_matching_orbit") != 0
        or payload.get("target") != expected_target
        or payload.get("full_hall_cell_forbidden") is not True
        or (expected_cap is not None and max(max(row) for row in values) > expected_cap)
        or full_hall_cells(values)
        or not matching_is_efx(values, terminal, matching)
    ):
        raise AssertionError(f"terminal selector refutation changed: {path}")
    families = {
        target: target_partitions(target, terminal)
        for target in (
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
        )
    }
    counts = {
        target: supporting_count(values, partitions)
        for target, partitions in families.items()
    }
    if counts != expected_counts:
        raise AssertionError(f"terminal selector repair census changed: {path}")
    formula_key = "proto_path" if "cpsat" in path.name else "smt2_path"
    formula_hash_key = (
        "proto_sha256" if formula_key == "proto_path" else "smt2_sha256"
    )
    formula_path = Path(payload[formula_key])
    if payload.get(formula_hash_key) != sha256(formula_path):
        raise AssertionError(f"terminal selector formula hash changed: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload[formula_hash_key],
        "repair_counts": counts,
    }


def audit_unknown_boundary(path, expected_solver, expected_time):
    payload = json.loads(path.read_text())
    if (
        payload.get("case") != "R"
        or payload.get("terminal_matching_orbit") != 0
        or payload.get("target") != "radius2_new_favorite_partner"
        or payload.get("target_partition_count") != 72
        or payload.get("full_hall_cell_forbidden") is not True
        or payload.get("solver_status") != expected_solver
        or payload.get("time_limit_seconds") != expected_time
        or payload.get("values") is not None
    ):
        raise AssertionError(f"new-partner decision boundary changed: {path}")
    formula_key = "proto_path" if "cpsat" in path.name else "smt2_path"
    formula_hash_key = (
        "proto_sha256" if formula_key == "proto_path" else "smt2_sha256"
    )
    formula_path = Path(payload[formula_key])
    if payload.get(formula_hash_key) != sha256(formula_path):
        raise AssertionError(f"new-partner formula hash changed: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload[formula_hash_key],
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_optimization_refutation(path, expected_counts):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    terminal = TERMINAL_PARTITIONS["R"]
    matching = TERMINAL_MATCHING_REPRESENTATIVES["R"][0]
    audit_branch(values)
    if (
        payload.get("status") != "OPTIMIZATION_CHECKPOINT"
        or payload.get("case") != "R"
        or payload.get("terminal_matching_orbit") != 0
        or payload.get("target") != "radius2"
        or payload.get("full_hall_cell_forbidden") is not True
        or max(max(row) for row in values) > 20
        or full_hall_cells(values)
        or not matching_is_efx(values, terminal, matching)
    ):
        raise AssertionError(f"optimization refutation changed: {path}")
    counts = {
        target: supporting_count(values, target_partitions(target, terminal))
        for target in (
            "radius2_same_favorite",
            "radius2_new_favorite_partner",
            "radius2_triple_partner",
        )
    }
    if counts != expected_counts or counts["radius2_new_favorite_partner"]:
        raise AssertionError(f"new-partner repair census changed: {path}")
    proto_path = Path(payload["proto_path"])
    if payload.get("proto_sha256") != sha256(proto_path):
        raise AssertionError(f"optimization formula hash changed: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload["proto_sha256"],
        "repair_counts": counts,
    }


def audit_radius_two_refutation():
    path = Path(
        "results/efx49_distinct_half_terminal_radius2_R_m0_"
        "cpsat_cap20_forbid_cell12_optimize_session1.json"
    )
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    terminal = TERMINAL_PARTITIONS["R"]
    matching = TERMINAL_MATCHING_REPRESENTATIVES["R"][0]
    targets = target_partitions("radius2", terminal)
    all_partitions = favorite_pair_universe("all")
    audit_branch(values)
    target_repairs = supporting_count(values, targets)
    all_repairs = tuple(
        partition
        for partition in all_partitions
        if matching_rank(feasible_graph(values, partition)) == 4
    )
    eight_repairs = tuple(
        partition
        for partition in all_repairs
        if favorite_pair_orbit_signature(partition)[1] < 3
    )
    literal_count = independent.count_complete_efx0(values)
    if (
        payload.get("schema")
        != "distinct-half-terminal-exchange-cpsat-optimization-v1"
        or payload.get("status") != "TERMINAL_SELECTOR_COUNTEREXAMPLE"
        or payload.get("solver_status") != "OPTIMAL"
        or payload.get("case") != "R"
        or payload.get("terminal_matching_orbit") != 0
        or payload.get("terminal_matching_representative") != list(matching)
        or payload.get("target") != "radius2"
        or payload.get("target_partition_count") != len(targets)
        or payload.get("target_partitions_sha256")
        != encoded_partition_hash(targets)
        or payload.get("target_repair_count") != 0
        or payload.get("cap") != 20
        or payload.get("obstruction_objective") != 138.0
        or payload.get("obstruction_objective_bound") != 138.0
        or payload.get("full_hall_cell_forbidden") is not False
        or payload.get("full_hall_cell_forbidden_pairs") != [[1, 2]]
        or payload.get("full_hall_cells") != []
        or max(max(row) for row in values) > 20
        or full_hall_cells(values)
        or not matching_is_efx(values, terminal, matching)
        or target_repairs != 0
        or payload.get("favorite_pair_efx_partition_count") != 336
        or len(all_repairs) != 336
        or len(eight_repairs) != 290
        or payload.get("literal_complete_efx_count") != 1439
        or literal_count != 1439
    ):
        raise AssertionError("full radius-two refutation changed")

    universe, neighbors = build_state_graph()
    positions = {partition: position for position, partition in enumerate(universe)}
    start = positions[terminal]
    distances = {start: 0}
    frontier = [start]
    for position in frontier:
        for neighbor in neighbors[position]:
            if neighbor not in distances:
                distances[neighbor] = distances[position] + 1
                frontier.append(neighbor)
    distance_histogram = Counter(
        distances[positions[partition]] for partition in eight_repairs
    )
    all_distance_histogram = Counter(
        distances[positions[partition]] for partition in all_repairs
    )
    if distance_histogram != Counter({3: 152, 4: 138}):
        raise AssertionError("radius-two refutation distance census changed")
    if all_distance_histogram != Counter({0: 1, 1: 4, 2: 17, 3: 176, 4: 138}):
        raise AssertionError("radius-two refutation full distance census changed")
    proto_path = Path(payload["proto_path"])
    if payload.get("proto_sha256") != sha256(proto_path):
        raise AssertionError("radius-two optimization formula hash changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload["proto_sha256"],
        "values": [list(row) for row in values],
        "radius_two_repair_count": target_repairs,
        "favorite_pair_repair_count": len(all_repairs),
        "eight_orbit_repair_count": len(eight_repairs),
        "terminal_orbit_repair_count": len(all_repairs) - len(eight_repairs),
        "favorite_pair_distance_histogram": {
            str(distance): count
            for distance, count in sorted(all_distance_histogram.items())
        },
        "eight_orbit_distance_histogram": {
            str(distance): count
            for distance, count in sorted(distance_histogram.items())
        },
        "literal_complete_efx_count": literal_count,
        "full_hall_cells": [],
    }


def audit_analytic_extraction():
    same_counts = (
        {
            "radius2_same_favorite": 0,
            "radius2_new_favorite_partner": 27,
            "radius2_triple_partner": 22,
        },
        {
            "radius2_same_favorite": 0,
            "radius2_new_favorite_partner": 25,
            "radius2_triple_partner": 24,
        },
    )
    triple_counts = {
        "radius2_same_favorite": 38,
        "radius2_new_favorite_partner": 16,
        "radius2_triple_partner": 0,
    }, {
        "radius2_same_favorite": 30,
        "radius2_new_favorite_partner": 10,
        "radius2_triple_partner": 0,
    }
    return {
        "same_favorite_refutations": [
            audit_refutation(
                Path(
                    "results/efx49_distinct_half_terminal_same_favorite_"
                    "radius2_R_m0_real_with_no_full_cell_session1.json"
                ),
                "radius2_same_favorite",
                None,
                same_counts[0],
            ),
            audit_refutation(
                Path(
                    "results/efx49_distinct_half_terminal_same_favorite_"
                    "radius2_R_m0_cpsat_cap20_with_no_full_cell_session1.json"
                ),
                "radius2_same_favorite",
                20,
                same_counts[1],
            ),
        ],
        "former_triple_partner_refutations": [
            audit_refutation(
                Path(
                    "results/efx49_distinct_half_terminal_triple_partner_"
                    "radius2_R_m0_z3_cap6_with_no_full_cell_session1.json"
                ),
                "radius2_triple_partner",
                6,
                triple_counts[0],
            ),
            audit_refutation(
                Path(
                    "results/efx49_distinct_half_terminal_triple_partner_"
                    "radius2_R_m0_cpsat_cap6_with_no_full_cell_session1.json"
                ),
                "radius2_triple_partner",
                6,
                triple_counts[1],
            ),
        ],
        "new_partner_refutations": [
            audit_optimization_refutation(
                Path(
                    "results/efx49_distinct_half_terminal_radius2_R_m0_"
                    "cpsat_cap20_no_full_optimize_session1.json"
                ),
                {
                    "radius2_same_favorite": 12,
                    "radius2_new_favorite_partner": 0,
                    "radius2_triple_partner": 0,
                },
            )
        ],
        "direct_new_partner_solver_boundaries": [
            audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_terminal_new_partner_"
                    "radius2_R_m0_real_with_no_full_cell_session1.json"
                ),
                "unknown",
                300.0,
            ),
            audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_terminal_new_partner_"
                    "radius2_R_m0_cpsat_cap20_with_no_full_cell_session1.json"
                ),
                "UNKNOWN",
                180.0,
            ),
        ],
        "radius_two_refutation": audit_radius_two_refutation(),
        "surviving_candidate": (
            "The radius-two terminal selector is retired. The surviving "
            "target is the global eight-orbit-or-full-Hall dichotomy."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=RESULT)
    args = parser.parse_args()
    target_summaries = {}
    cells = []
    symmetry = {}
    for case in TERMINAL_PARTITIONS:
        stabilizer_size, orbit_sizes = matching_orbit_audit(case)
        targets = target_partitions("radius2", TERMINAL_PARTITIONS[case])
        target_hash = encoded_partition_hash(targets)
        if len(targets) != 138 or len(set(targets)) != 138:
            raise AssertionError(f"{case} radius-two target family changed")
        symmetry[case] = {
            "stabilizer_size": stabilizer_size,
            "matching_orbit_sizes": orbit_sizes,
            "matching_orbit_count": len(orbit_sizes),
        }
        target_summaries[case] = {
            "partition_count": len(targets),
            "partitions_sha256": target_hash,
        }
        for matching_orbit in range(
            len(TERMINAL_MATCHING_REPRESENTATIVES[case])
        ):
            cells.append(
                audit_cell(case, matching_orbit, targets, target_hash)
            )

    if Counter(cell["case"] for cell in cells) != Counter({"R": 3, "U": 4}):
        raise AssertionError("terminal cell coverage changed")
    result = {
        "schema": SCHEMA,
        "status": "DUAL_VERIFIED_FINITE_CAP_THEOREM",
        "n": 4,
        "m": 9,
        "cap": 5,
        "scope": {
            "strict_common_favorite": True,
            "universal_owner_threshold_failure": True,
            "four_distinct_half_favorite_representatives": True,
            "full_favorite_triple_hall_cell_condition": "not assumed",
        },
        "theorem": (
            "For positive-integer values at most 5 in the stated structural "
            "branch, if either terminal partition supports EFX, then an "
            "eight-orbit favorite-pair partition within graph distance at "
            "most 2 of that terminal partition supports EFX."
        ),
        "not_claimed": (
            "No cap-free exchange lemma and no proof of general additive EFX."
        ),
        "terminal_symmetry": symmetry,
        "target_families": target_summaries,
        "canonical_cell_count": len(cells),
        "independent_encodings": ["OR-Tools CP-SAT", "Z3 QF_LIA"],
        "nonvacuity_witness": audit_nonvacuity(),
        "analytic_extraction": audit_analytic_extraction(),
        "cells": cells,
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
