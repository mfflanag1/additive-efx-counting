#!/usr/bin/env python3
"""Audit the symmetry-orbit proof-mining gate extracted from the cap-5 core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .run_distinct_half_full_cell_cegar import (
        SIX_ORBIT_SIGNATURES,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
        perfect_pairings,
    )
    from .run_generic_partition_cegar import supported_partitions
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from run_distinct_half_full_cell_cegar import (
        SIX_ORBIT_SIGNATURES,
        favorite_pair_orbit_signature,
        favorite_pair_universe,
        full_hall_cells,
        pairing_has_hall_matching,
        perfect_pairings,
    )
    from run_generic_partition_cegar import supported_partitions


SCHEMA = "distinct-half-full-cell-orbit-gate-audit-v1"
MINIMAL_CORE_SCHEMA = "distinct-half-full-cell-threshold-cnf-minimal-core-v1"
INTEGER_PROBE_SCHEMA = "distinct-half-full-cell-integer-core-probe-v1"
ANNEAL_SCHEMA = "distinct-half-rank-augmentation-anneal-v1"
CEGAR_SCHEMA = "distinct-half-full-cell-cegar-v1"
ORBIT_POOL_SCHEMA = "distinct-half-full-cell-orbit-pool-v1"
CPSAT_CEGAR_SCHEMA = "distinct-half-full-cell-cpsat-cegar-v1"
FULL_CELL_ENCODING = {
    "accept_literals": 1680,
    "hall_failure_templates_per_pairing": 21,
    "low_pair_cells": 28,
    "pairing_failure_terms": 420,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode_partition(raw):
    return tuple(tuple(bundle) for bundle in raw)


def signature_name(signature) -> str:
    partner, representative_count, pair_types = signature
    return f"{partner}|tripleR={representative_count}|{'+'.join(pair_types)}"


def signature_histogram(partitions) -> dict[str, int]:
    counts = Counter(favorite_pair_orbit_signature(partition) for partition in partitions)
    return {
        signature_name(signature): counts[signature]
        for signature in sorted(counts)
    }


def read_values(payload):
    return core.validate_values(
        payload["values"], expected_n=4, expected_m=9, lower=1
    )


def favorite_triple_cell_counts(values):
    counts = {}
    for lows in itertools.combinations(range(1, 9), 2):
        residual = tuple(good for good in range(1, 9) if good not in lows)
        counts[lows] = sum(
            pairing_has_hall_matching(values, lows, matching)
            for matching in perfect_pairings(residual)
        )
    return counts


def audit_cegar(
    payload,
    seed_path: Path,
    universe,
    partition_family: str,
    expected_resume_path: Path | None = None,
    expected_time_limit: float | None = None,
):
    if (
        payload.get("schema") != CEGAR_SCHEMA
        or payload.get("partition_family") != partition_family
        or payload.get("favorite_pair_partition_count") != len(universe)
        or payload.get("seed_mode") != "union"
        or payload.get("seed_sources")
        != [{"path": str(seed_path), "sha256": sha256(seed_path)}]
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "unknown"
        or payload.get("reason_unknown") not in {"canceled", "timeout"}
        or payload.get("n") != 4
        or payload.get("m") != 9
        or payload.get("fixed_half_favorite_representatives") != [1, 2, 3, 4]
        or payload.get("universal_owner_threshold_failure") is not True
        or payload.get("universal_threshold_encoding") != "cardinal"
        or payload.get("full_hall_cell_forbidden") is not True
        or payload.get("full_cell_encoding") != FULL_CELL_ENCODING
        or payload.get("values") is not None
        or payload.get("literal_complete_efx_count") is not None
        or payload.get("iterations") != len(payload.get("trace", [])) + 1
    ):
        raise AssertionError(f"{partition_family} CEGAR metadata changed")
    if expected_time_limit is not None and (
        payload.get("time_limit_seconds") != expected_time_limit
        or payload.get("elapsed_seconds", 0) < expected_time_limit
        or payload.get("max_iterations") != 4
    ):
        raise AssertionError(f"{partition_family} CEGAR timeout changed")
    if expected_resume_path is not None and (
        payload.get("resume_source") != str(expected_resume_path)
        or payload.get("resume_source_sha256") != sha256(expected_resume_path)
    ):
        raise AssertionError(f"{partition_family} CEGAR resume changed")

    seed = json.loads(seed_path.read_text())
    seed_values = read_values(seed)
    pool = set(supported_partitions(seed_values, list(universe)))
    if len(pool) != payload.get("seed_supported_union_size"):
        raise AssertionError(f"{partition_family} seed pool changed")
    trace_survivors = []
    for position, record in enumerate(payload["trace"], start=1):
        values = core.validate_values(
            record["values"], expected_n=4, expected_m=9, lower=1
        )
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError(
                f"{partition_family} trace acquired a full Hall cell"
            )
        survivors = tuple(
            partition
            for partition in supported_partitions(values, list(universe))
            if partition not in pool
        )
        if (
            record["iteration"] != position
            or record["pool_size_before"] != len(pool)
            or record["favorite_pair_efx_survivors"] != len(survivors)
        ):
            raise AssertionError(f"{partition_family} CEGAR trace changed")
        trace_survivors.append(len(survivors))
        pool.update(survivors[: payload["add_per_iteration"]])
    if len(pool) != payload["pool_size"]:
        raise AssertionError(f"{partition_family} CEGAR pool changed")
    smt2_path = Path(payload["smt2_path"])
    if sha256(smt2_path) != payload["smt2_sha256"]:
        raise AssertionError(f"{partition_family} CEGAR formula hash changed")
    return trace_survivors


def audit_refutation(payload, full_universe):
    if (
        payload.get("schema") != "distinct-half-six-orbit-refutation-v1"
        or payload.get("status") != "SIX_ORBIT_SELECTION_REFUTED"
        or payload.get("cap") != 20
    ):
        raise AssertionError("six-orbit refutation metadata changed")

    values = core.validate_values(
        payload["values"], expected_n=4, expected_m=9, lower=1, upper=20
    )
    audit_branch(values)
    repairs = tuple(supported_partitions(values, list(full_universe)))
    six_orbit_repairs = tuple(
        partition
        for partition in repairs
        if favorite_pair_orbit_signature(partition) in SIX_ORBIT_SIGNATURES
    )
    representative_partner_repairs = tuple(
        partition
        for partition in repairs
        if any(
            0 in bundle
            and any(good in {1, 2, 3, 4} for good in bundle)
            for bundle in partition
        )
    )
    literal_count = independent.count_complete_efx0(values)
    partner_counts = Counter(
        next(good for good in bundle if good != 0)
        for partition in repairs
        for bundle in partition
        if 0 in bundle
    )
    half_eligible_partners = {
        good
        for good in partner_counts
        if any(2 * row[good] > row[0] for row in values)
    }
    if (
        full_hall_cells(values)
        or six_orbit_repairs
        or representative_partner_repairs
        or len(repairs) != 45
        or literal_count != 900
        or partner_counts != Counter({6: 15, 7: 15, 8: 15})
        or half_eligible_partners
    ):
        raise AssertionError("six-orbit refutation replay changed")
    return values, repairs, literal_count, partner_counts


def audit_eight_orbit_boundary(
    pool_path: Path, result_path: Path, cegar_path: Path, seed_path: Path
):
    pool = json.loads(pool_path.read_text())
    result = json.loads(result_path.read_text())
    partitions = tuple(
        decode_partition(partition) for partition in pool["core_partitions"]
    )
    expected = favorite_pair_universe("eight_orbit")
    triple_not_all_representatives = tuple(
        partition
        for partition in favorite_pair_universe("all")
        if favorite_pair_orbit_signature(partition)[1] < 3
    )
    pool_source = result.get("pool_source", {})
    proto_path = Path(result.get("proto_path", ""))
    if not proto_path.is_file():
        proto_path = result_path.parent / proto_path.name
    if (
        pool.get("schema") != ORBIT_POOL_SCHEMA
        or pool.get("status") != "PROOF_MINING_POOL"
        or pool.get("family") != "eight_orbit"
        or pool.get("universe_size") != 840
        or pool.get("core_size") != 780
        or partitions != expected
        or expected != triple_not_all_representatives
        or result.get("schema") != CPSAT_CEGAR_SCHEMA
        or result.get("status") != "CP_SAT_UNKNOWN"
        or result.get("solver_status") != "UNKNOWN"
        or result.get("cap") != 20
        or result.get("seed_mode") != "complement"
        or result.get("seed_sources")
        or result.get("seed_supported_union_size") != 0
        or result.get("pool_size") != 780
        or result.get("trace")
        or result.get("favorite_pair_partition_count") != 840
        or result.get("fixed_half_favorite_representatives") != [1, 2, 3, 4]
        or result.get("full_hall_cell_forbidden") is not True
        or result.get("full_cell_encoding")
        != {
            "accept_literals": 1680,
            "hall_failure_templates_per_pairing": 21,
            "hall_witness_literals": 8820,
            "low_pair_cells": 28,
        }
        or result.get("iterations") != 1
        or result.get("add_per_iteration") != 128
        or result.get("time_limit_seconds") != 600.0
        or result.get("symmetry_breaking")
        != [
            "nonincreasing favorite values by agent",
            "nonincreasing agent-0 values on goods 5..8",
        ]
        or result.get("resume_source") is not None
        or result.get("resume_source_sha256") is not None
        or result.get("values") is not None
        or result.get("literal_complete_efx_count") is not None
        or pool_source.get("path") != str(pool_path)
        or pool_source.get("sha256") != sha256(pool_path)
        or pool_source.get("partition_count") != 780
        or not proto_path.is_file()
        or result.get("proto_sha256") != sha256(proto_path)
    ):
        raise AssertionError("eight-orbit decision boundary changed")
    cegar = json.loads(cegar_path.read_text())
    trace_survivors = audit_cegar(
        cegar,
        seed_path,
        expected,
        "eight_orbit",
        expected_resume_path=Path(
            "results/efx49_distinct_half_eight_orbit_cegar_session1.json"
        ),
        expected_time_limit=300.0,
    )
    return result, cegar, trace_survivors


def run(
    minimal_core_path: Path,
    cap6_escape_path: Path,
    anneal_path: Path,
    cegar_path: Path,
    refutation_path: Path,
    eight_pool_path: Path,
    eight_cpsat_path: Path,
    eight_cegar_path: Path,
    output: Path,
):
    minimal = json.loads(minimal_core_path.read_text())
    cap6 = json.loads(cap6_escape_path.read_text())
    anneal = json.loads(anneal_path.read_text())
    cegar = json.loads(cegar_path.read_text())
    refutation = json.loads(refutation_path.read_text())
    full_universe = favorite_pair_universe("all")
    six_orbit_universe = favorite_pair_universe("six_orbit")
    minimal_partitions = tuple(
        decode_partition(partition) for partition in minimal["core_partitions"]
    )
    if (
        minimal.get("schema") != MINIMAL_CORE_SCHEMA
        or minimal.get("status") != "DELETION_MINIMAL_UNSAT_CORE_VERIFIED"
        or minimal.get("cap") != 5
        or minimal.get("core_size") != 17
        or len(minimal_partitions) != 17
        or len(set(minimal_partitions)) != 17
        or not set(minimal_partitions) <= set(six_orbit_universe)
        or len(full_universe) != 840
        or len(six_orbit_universe) != 624
    ):
        raise AssertionError("minimal-core orbit scope changed")

    boundary_repairs = []
    common_repairs = set(full_universe)
    for position, record in enumerate(minimal["removal_boundaries"]):
        if record["removed_position"] != position:
            raise AssertionError("minimal-core boundary order changed")
        values = core.validate_values(
            record["values"], expected_n=4, expected_m=9, lower=1, upper=5
        )
        audit_branch(values)
        if full_hall_cells(values):
            raise AssertionError("minimal-core boundary acquired a full cell")
        repairs = set(supported_partitions(values, list(full_universe)))
        core_repairs = repairs & set(minimal_partitions)
        if core_repairs != {minimal_partitions[position]}:
            raise AssertionError("minimal-core unique repair changed")
        common_repairs &= repairs
        boundary_repairs.append(len(repairs))

    cap6_values = read_values(cap6)
    audit_branch(cap6_values)
    cap6_repairs = tuple(supported_partitions(cap6_values, list(full_universe)))
    cap6_core_repairs = supported_partitions(cap6_values, list(minimal_partitions))
    if (
        cap6.get("schema") != INTEGER_PROBE_SCHEMA
        or cap6.get("status") != "SAT_CORE_ESCAPE"
        or cap6.get("cap") != 6
        or cap6.get("source_sha256") != sha256(minimal_core_path)
        or cap6.get("core_size") != len(minimal_partitions)
        or full_hall_cells(cap6_values)
        or cap6_core_repairs
        or len(cap6_repairs) != cap6.get("favorite_pair_repair_count")
        or independent.count_complete_efx0(cap6_values)
        != cap6.get("literal_complete_efx_count")
    ):
        raise AssertionError("cap-6 minimal-core escape changed")

    anneal_values = read_values(anneal)
    audit_branch(anneal_values)
    anneal_full_repairs = supported_partitions(anneal_values, list(full_universe))
    anneal_six_repairs = supported_partitions(
        anneal_values, list(six_orbit_universe)
    )
    anneal_cell_counts = favorite_triple_cell_counts(anneal_values)
    anneal_audit = anneal.get("audit", {})
    if (
        anneal.get("schema") != ANNEAL_SCHEMA
        or anneal.get("objective") != "orbit_gate"
        or anneal.get("universe") != "favorite_pair"
        or full_hall_cells(anneal_values)
        or len(anneal_full_repairs)
        != anneal_audit.get("favorite_pair_perfect_partition_count")
        or len(anneal_six_repairs)
        != anneal_audit.get("six_orbit_perfect_partition_count")
        or sum(anneal_cell_counts.values())
        != anneal_audit.get("favorite_triple_perfect_partition_count")
        or max(anneal_cell_counts.values())
        != anneal_audit.get("maximum_favorite_triple_cell_count")
        or sum(count == 15 for count in anneal_cell_counts.values())
        != anneal_audit.get("full_favorite_triple_cell_count")
    ):
        raise AssertionError("six-orbit annealing boundary changed")
    trace_survivors = audit_cegar(
        cegar, anneal_path, six_orbit_universe, "six_orbit"
    )
    (
        refutation_values,
        refutation_repairs,
        literal_count,
        refutation_partner_counts,
    ) = audit_refutation(refutation, full_universe)
    eight_cpsat, eight_cegar, eight_trace_survivors = (
        audit_eight_orbit_boundary(
            eight_pool_path,
            eight_cpsat_path,
            eight_cegar_path,
            refutation_path,
        )
    )

    result = {
        "schema": SCHEMA,
        "status": "SIX_ORBIT_GATE_REFUTED",
        "scope": (
            "strict-common-favorite, universal-owner-threshold-failure, "
            "distinct half-favorite representatives at (4,9)"
        ),
        "partition_orbits": {
            "full_favorite_pair_universe": len(full_universe),
            "orbit_count": 10,
            "universe_histogram": signature_histogram(full_universe),
            "six_orbit_family_count": len(six_orbit_universe),
            "six_orbit_signatures": [
                signature_name(signature)
                for signature in sorted(SIX_ORBIT_SIGNATURES)
            ],
            "minimal_core_histogram": signature_histogram(minimal_partitions),
        },
        "cap5_minimal_core": {
            "source": str(minimal_core_path),
            "source_sha256": sha256(minimal_core_path),
            "core_size": len(minimal_partitions),
            "deletion_boundary_count": len(boundary_repairs),
            "full_universe_repair_count_min": min(boundary_repairs),
            "full_universe_repair_count_max": max(boundary_repairs),
            "common_full_universe_repair_count": len(common_repairs),
            "common_full_universe_repairs": [
                [list(bundle) for bundle in partition]
                for partition in sorted(common_repairs)
            ],
            "common_repair_histogram": signature_histogram(common_repairs),
        },
        "cap6_escape": {
            "source": str(cap6_escape_path),
            "source_sha256": sha256(cap6_escape_path),
            "favorite_pair_repair_count": len(cap6_repairs),
            "six_orbit_repair_count": sum(
                favorite_pair_orbit_signature(partition) in SIX_ORBIT_SIGNATURES
                for partition in cap6_repairs
            ),
            "repair_histogram": signature_histogram(cap6_repairs),
            "literal_complete_efx_count": cap6["literal_complete_efx_count"],
            "interpretation": (
                "The deletion-minimal 17-template core is cap-specific and "
                "cannot itself be promoted to a real-valued lemma."
            ),
        },
        "six_orbit_decision_boundary": {
            "anneal_source": str(anneal_path),
            "anneal_source_sha256": sha256(anneal_path),
            "anneal_six_orbit_repairs": len(anneal_six_repairs),
            "anneal_favorite_pair_repairs": len(anneal_full_repairs),
            "anneal_favorite_triple_repairs": sum(
                anneal_cell_counts.values()
            ),
            "anneal_maximum_favorite_triple_cell_count": max(
                anneal_cell_counts.values()
            ),
            "anneal_full_favorite_triple_cell_count": sum(
                count == 15 for count in anneal_cell_counts.values()
            ),
            "cegar_source": str(cegar_path),
            "cegar_source_sha256": sha256(cegar_path),
            "cegar_status": cegar["status"],
            "cegar_pool_size": cegar["pool_size"],
            "cegar_trace_survivors": trace_survivors,
            "cegar_elapsed_seconds": cegar["elapsed_seconds"],
        },
        "candidate": {
            "statement": (
                "If no favorite-triple full Hall cell exists, some EFX "
                "favorite-pair partition lies in one of the six listed "
                "representative/free-good orbits."
            ),
            "status": "REFUTED by an exact cap-20 profile",
            "warning": (
                "The refuting profile has many complete EFX allocations; "
                "it refutes only the proposed orbit-selection statement."
            ),
        },
        "six_orbit_refutation": {
            "source": str(refutation_path),
            "source_sha256": sha256(refutation_path),
            "cap": 20,
            "values": [list(row) for row in refutation_values],
            "full_favorite_triple_cell_count": 0,
            "favorite_pair_repair_count": len(refutation_repairs),
            "six_orbit_repair_count": 0,
            "representative_partner_repair_count": 0,
            "favorite_partner_histogram": {
                str(good): count
                for good, count in sorted(refutation_partner_counts.items())
            },
            "half_eligible_favorite_partner_count": 0,
            "repair_histogram": signature_histogram(refutation_repairs),
            "literal_complete_efx_count": literal_count,
            "interpretation": (
                "All surviving favorite-pair repairs lie in two orbits "
                "omitted by the six-orbit family. This is a positive EFX "
                "profile, not a counterexample to existence."
            ),
        },
        "eight_orbit_decision_boundary": {
            "candidate_statement": (
                "Some EFX favorite-pair repair has a triple containing "
                "at most two of the four fixed representatives."
            ),
            "candidate_partition_count": 780,
            "omitted_partition_count": 60,
            "omitted_signatures": [
                "R|tripleR=3|UU+UU",
                "U|tripleR=3|RU+UU",
            ],
            "pool_source": str(eight_pool_path),
            "pool_source_sha256": sha256(eight_pool_path),
            "cpsat_source": str(eight_cpsat_path),
            "cpsat_source_sha256": sha256(eight_cpsat_path),
            "cpsat_status": eight_cpsat["status"],
            "elapsed_seconds": eight_cpsat["elapsed_seconds"],
            "conflicts": eight_cpsat["conflicts"],
            "branches": eight_cpsat["branches"],
            "exact_real_source": str(eight_cegar_path),
            "exact_real_source_sha256": sha256(eight_cegar_path),
            "exact_real_status": eight_cegar["status"],
            "exact_real_pool_size": eight_cegar["pool_size"],
            "exact_real_trace_survivors": eight_trace_survivors,
            "exact_real_elapsed_seconds": eight_cegar["elapsed_seconds"],
            "interpretation": (
                "No counterexample or infeasibility proof was obtained at "
                "the cap-20 or exact-real boundaries. The eight-orbit "
                "candidate remains open."
            ),
        },
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--minimal-core", type=Path, required=True)
    parser.add_argument("--cap6-escape", type=Path, required=True)
    parser.add_argument("--anneal", type=Path, required=True)
    parser.add_argument("--cegar", type=Path, required=True)
    parser.add_argument("--refutation", type=Path, required=True)
    parser.add_argument("--eight-pool", type=Path, required=True)
    parser.add_argument("--eight-cpsat", type=Path, required=True)
    parser.add_argument("--eight-cegar", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.minimal_core,
        args.cap6_escape,
        args.anneal,
        args.cegar,
        args.refutation,
        args.eight_pool,
        args.eight_cpsat,
        args.eight_cegar,
        args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
