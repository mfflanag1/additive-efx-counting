#!/usr/bin/env python3
"""Audit the representative-pair Hall split proof-mining boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .run_distinct_half_conversion_dichotomy_cegar import load_values
    from .run_distinct_half_full_cell_cegar import (
        common_rr_uu_singleton_witnesses,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from audit_matching_augmentation import feasible_graph, matching_rank
    from run_distinct_half_conversion_dichotomy_cegar import load_values
    from run_distinct_half_full_cell_cegar import (
        common_rr_uu_singleton_witnesses,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-rr-hall-split-gate-audit-v1"
CEGAR_SCHEMA = "distinct-half-full-cell-cegar-v1"
CENSUS_SCHEMA = "distinct-half-full-cell-hall-witness-census-v2"
OPTIMIZER_SCHEMA = "distinct-half-eight-orbit-cpsat-optimization-v1"
FULL_CELL_ENCODING = {
    "accept_literals": 1680,
    "hall_failure_templates_per_pairing": 21,
    "low_pair_cells": 28,
    "pairing_failure_terms": 420,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_seed_union(payload, universe):
    supported = set()
    sources = []
    for source in payload["seed_sources"]:
        path = Path(source["path"])
        if source.get("sha256") != sha256(path):
            raise AssertionError(f"seed hash changed: {path}")
        supported.update(supported_partitions(load_values(path), list(universe)))
        sources.append({"path": str(path), "sha256": source["sha256"]})
    if (
        len(supported) != payload.get("seed_supported_union_size")
        or len(supported) != payload.get("pool_size")
    ):
        raise AssertionError("seed-union replay changed")
    return sources


def audit_unknown_boundary(
    path: Path,
    *,
    pool_size: int,
    time_limit: float,
    common: bool = False,
    forbid_common: bool = False,
    second_smallest_map=None,
):
    payload = json.loads(path.read_text())
    universe = favorite_pair_universe("eight_orbit")
    formula_path = Path(payload["smt2_path"])
    expected_common = [5, 6] if common else None
    expected_map = list(second_smallest_map) if second_smallest_map else None
    if (
        payload.get("schema") != CEGAR_SCHEMA
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "unknown"
        or payload.get("reason_unknown") != "timeout"
        or payload.get("partition_family") != "eight_orbit"
        or payload.get("favorite_pair_partition_count") != len(universe)
        or payload.get("seed_mode") != "union"
        or payload.get("pool_size") != pool_size
        or payload.get("time_limit_seconds") != time_limit
        or payload.get("max_iterations") != 1
        or payload.get("iterations") != 1
        or payload.get("trace")
        or payload.get("values") is not None
        or payload.get("literal_complete_efx_count") is not None
        or payload.get("full_hall_cell_forbidden") is not True
        or payload.get("full_cell_encoding") != FULL_CELL_ENCODING
        or payload.get("common_rr_uu_singleton_witness") != expected_common
        or payload.get("common_rr_uu_singleton_witness_forbidden")
        is not forbid_common
        or payload.get("second_smallest_representative_map") != expected_map
        or payload.get("rank_disjunct_branch") is not None
        or payload.get("smt2_sha256") != sha256(formula_path)
    ):
        raise AssertionError(f"exact-real boundary changed: {path}")
    common_encoding = payload.get("common_rr_uu_singleton_witness_encoding")
    no_common_encoding = payload.get("no_common_rr_uu_singleton_witness_encoding")
    if common:
        expected_rejections = 4 if second_smallest_map else 24
        if (
            common_encoding.get("edge") != [5, 6]
            or common_encoding.get("rr_low_pair_cells") != 6
            or common_encoding.get("rejection_constraints")
            != expected_rejections
            or no_common_encoding is not None
        ):
            raise AssertionError(f"common-UU encoding changed: {path}")
    elif common_encoding is not None:
        raise AssertionError(f"unexpected common-UU encoding: {path}")
    if forbid_common:
        if no_common_encoding != {
            "nonwitness_constraints": 6,
            "unmatched_edges": 6,
        }:
            raise AssertionError("no-common-UU encoding changed")
    elif no_common_encoding is not None:
        raise AssertionError(f"unexpected no-common-UU encoding: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload["smt2_sha256"],
        "seed_sources": audit_seed_union(payload, universe),
        "pool_size": pool_size,
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_optimizer(path: Path):
    payload = json.loads(path.read_text())
    values = tuple(tuple(row) for row in payload["values"])
    targets = favorite_pair_universe("eight_orbit")
    all_partitions = favorite_pair_universe("all")
    audit_branch(values)
    target_repairs = tuple(
        partition
        for partition in targets
        if matching_rank(feasible_graph(values, partition)) == 4
    )
    all_repairs = tuple(supported_partitions(values, list(all_partitions)))
    histogram = Counter(
        favorite_pair_orbit_signature(partition) for partition in all_repairs
    )
    partner_histogram = Counter(
        next(
            good
            for bundle in partition
            if 0 in bundle
            for good in bundle
            if good != 0
        )
        for partition in all_repairs
    )
    expected_histogram = {
        ("U", 0, ("RR", "RR")): 6,
        ("U", 1, ("RR", "RU")): 24,
    }
    literal_count = independent.count_complete_efx0(values)
    proto_path = Path(payload["proto_path"])
    if (
        payload.get("schema") != OPTIMIZER_SCHEMA
        or payload.get("status") != "OPTIMIZATION_CHECKPOINT"
        or payload.get("solver_status") != "FEASIBLE"
        or payload.get("cap") != 20
        or payload.get("target_partition_count") != len(targets)
        or payload.get("obstruction_objective") != 750.0
        or payload.get("obstruction_objective_bound") != 780.0
        or payload.get("semantic_obstruction_count") != 750
        or payload.get("target_repair_count") != 30
        or len(target_repairs) != 30
        or payload.get("favorite_pair_efx_partition_count") != 30
        or len(all_repairs) != 30
        or histogram != expected_histogram
        or partner_histogram != Counter({7: 15, 8: 15})
        or payload.get("literal_complete_efx_count") != 684
        or literal_count != 684
        or payload.get("full_hall_cells") != []
        or full_hall_cells(values)
        or len(common_rr_uu_singleton_witnesses(values)) != 6
        or payload.get("proto_sha256") != sha256(proto_path)
    ):
        raise AssertionError("cap-20 eight-orbit optimization replay changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula_sha256": payload["proto_sha256"],
        "values": [list(row) for row in values],
        "eight_orbit_repair_count": len(target_repairs),
        "favorite_pair_repair_count": len(all_repairs),
        "repair_orbit_histogram": {
            repr(signature): count
            for signature, count in sorted(
                histogram.items(), key=lambda item: repr(item[0])
            )
        },
        "favorite_partner_histogram": {
            str(good): count for good, count in sorted(partner_histogram.items())
        },
        "literal_complete_efx_count": literal_count,
        "common_unrepresented_witness_edges": [
            list(edge) for edge in common_rr_uu_singleton_witnesses(values)
        ],
        "full_hall_cells": [],
    }


def run(census_path: Path, output: Path):
    census = json.loads(census_path.read_text())
    structure = census.get("rr_singleton_structure", {})
    if (
        census.get("schema") != CENSUS_SCHEMA
        or census.get("profile_count") != 21
        or census.get("cell_minimum_witness_size_counts")
        != {"1": 572, "2": 9, "3": 7}
        or structure.get("minimum_cell_cover_size_histogram")
        != {"1": 17, "2": 1, "3": 3}
        or structure.get(
            "profiles_with_one_unrepresented_edge_witnessing_all_six_cells"
        )
        != 17
        or structure.get("second_smallest_representative_map_orbit_count")
        != 19
        or structure.get("common_uu_unobserved_second_smallest_orbits")
        != [[1, 2, 3, 4]]
    ):
        raise AssertionError("RR Hall-witness census changed")
    result = {
        "schema": SCHEMA,
        "status": "PROOF_MINING_BOUNDARIES_AUDITED",
        "not_claimed": (
            "No eight-orbit selector, full-cell dichotomy, or general EFX theorem."
        ),
        "census": {
            "source": str(census_path),
            "source_sha256": sha256(census_path),
            "common_uu_profile_count": 17,
            "minimum_edge_cover_size_histogram": {"1": 17, "2": 1, "3": 3},
            "second_smallest_map_orbit_count": 19,
            "unobserved_map_orbits": [[1, 2, 3, 4]],
        },
        "exact_real_boundaries": {
            "global": audit_unknown_boundary(
                Path("results/efx49_distinct_half_eight_orbit_cegar_session5.json"),
                pool_size=708,
                time_limit=600.0,
            ),
            "common_uu": audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_eight_orbit_"
                    "common_uu_cegar_session1.json"
                ),
                pool_size=708,
                time_limit=300.0,
                common=True,
            ),
            "no_common_uu": audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_eight_orbit_"
                    "no_common_uu_cegar_session1.json"
                ),
                pool_size=708,
                time_limit=300.0,
                forbid_common=True,
            ),
            "common_uu_map_1112": audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_eight_orbit_"
                    "common_uu_map1112_cegar_session1.json"
                ),
                pool_size=316,
                time_limit=60.0,
                common=True,
                second_smallest_map=(1, 1, 1, 2),
            ),
            "common_uu_map_1234": audit_unknown_boundary(
                Path(
                    "results/efx49_distinct_half_eight_orbit_"
                    "common_uu_map1234_cegar_session1.json"
                ),
                pool_size=708,
                time_limit=300.0,
                common=True,
                second_smallest_map=(1, 2, 3, 4),
            ),
        },
        "cap20_optimization_checkpoint": audit_optimizer(
            Path(
                "results/efx49_distinct_half_eight_orbit_"
                "cpsat_cap20_optimize_session1.json"
            )
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--census",
        type=Path,
        default=Path(
            "results/efx49_distinct_half_full_cell_cap6_hall_witness_census.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "results/efx49_distinct_half_rr_hall_split_gate_audit.json"
        ),
    )
    args = parser.parse_args()
    result = run(args.census, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
