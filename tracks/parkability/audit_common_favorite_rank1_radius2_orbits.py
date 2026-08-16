#!/usr/bin/env python3
"""Audit the radius-two orbit compression for the rank-one Hall gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from .decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        CONTESTED,
        FAVORITE,
        N,
        RESIDUAL,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
    from decide_common_favorite_threshold_pass_hall_cpsat import (
        balanced_transfer_neighborhood,
    )


SCHEMA = "common-favorite-rank1-radius2-orbits-audit-v1"
EXPECTED_ORBITS = {
    "partnerA_tripleAAB_pairsBB_CC": (9, 4),
    "partnerA_tripleABF_pairsAA_BB_CC": (9, 0),
    "partnerA_tripleBBB_pairsAA_CC": (3, 0),
    "partnerA_tripleBCC_pairsAA_BB": (9, 4),
    "partnerB_tripleAAA_pairsBB_CC": (3, 0),
    "partnerB_tripleABB_pairsAA_CC": (9, 3),
    "partnerB_tripleACC_pairsAA_BB": (9, 3),
    "partnerC_tripleAAA_pairsBB_BC": (6, 0),
    "partnerC_tripleBBB_pairsAA_AC": (6, 1),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def origin_map():
    return {
        FAVORITE: "F",
        **{good: "A" for good in RESIDUAL[0]},
        **{good: "B" for good in RESIDUAL[1]},
        **{good: "C" for good in RESIDUAL[2]},
    }


def orbit_signature(partition):
    origins = origin_map()
    favorite_bundle = next(bundle for bundle in partition if FAVORITE in bundle)
    partner_origin = "A" if len(favorite_bundle) != 2 else origins[
        next(good for good in favorite_bundle if good != FAVORITE)
    ]
    triple = next(bundle for bundle in partition if len(bundle) == 3)
    triple_signature = "".join(sorted(origins[good] for good in triple))
    pair_signatures = sorted(
        "".join(sorted(origins[good] for good in bundle))
        for bundle in partition
        if len(bundle) == 2 and FAVORITE not in bundle
    )
    return (
        f"partner{partner_origin}_triple{triple_signature}_pairs"
        f"{'_'.join(pair_signatures)}"
    )


def contested_family(neighborhood):
    return tuple(
        partition
        for partition in neighborhood
        for favorite_bundle in [
            next(bundle for bundle in partition if FAVORITE in bundle)
        ]
        if len(favorite_bundle) == 2
        and next(good for good in favorite_bundle if good != FAVORITE)
        in CONTESTED
    )


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def reconstruct_pool(trace, blocked):
    pool = []
    pool_set = set()
    sequence = []
    for expected_iteration, record in enumerate(trace, 1):
        values = tuple(tuple(row) for row in record["values"])
        if (
            record["iteration"] != expected_iteration
            or record["singleton_pool_size_before"] != len(pool)
            or not threshold_passes(values, 0, RESIDUAL)
            or resident_graph(values) != ((True, False, False),) * 3
            or any(
                matching_rank(feasible_graph(values, partition)) == N
                for partition in (*pool, *blocked)
            )
        ):
            raise AssertionError("contested-radius trace left the decision cell")
        survivors = []
        for residual in residual_partitions():
            partition = ((FAVORITE,),) + residual
            key = canonical(partition)
            if key in pool_set:
                continue
            if matching_rank(feasible_graph(values, partition)) == N:
                survivors.append(partition)
        if len(survivors) != record[
            "supported_unpooled_singleton_partition_count"
        ]:
            raise AssertionError("contested-radius singleton census changed")
        sequence.append(len(survivors))
        for partition in survivors[:256]:
            pool.append(partition)
            pool_set.add(canonical(partition))
    return pool, sequence


def run(local6_path, contested_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    local6 = json.loads(local6_path.read_text())
    if (
        local6.get("schema")
        != "common-favorite-rank1-triple-conversion-cpsat-v1"
        or local6.get("status") != "RANK1_TRIPLE_DICHOTOMY_COUNTEREXAMPLE"
        or local6.get("values") is None
    ):
        raise ValueError("local-six source metadata changed")
    values = core.validate_values(
        local6["values"],
        expected_n=4,
        expected_m=9,
        lower=1,
        upper=20,
    )
    neighborhood = balanced_transfer_neighborhood(RESIDUAL, 2)
    if len(neighborhood) != 63:
        raise AssertionError("radius-two neighborhood changed")
    orbit_total = Counter(orbit_signature(partition) for partition in neighborhood)
    orbit_support = Counter(
        orbit_signature(partition)
        for partition in neighborhood
        if matching_rank(feasible_graph(values, partition)) == N
    )
    observed_orbits = {
        key: (orbit_total[key], orbit_support[key])
        for key in sorted(orbit_total)
    }
    if observed_orbits != EXPECTED_ORBITS:
        raise AssertionError("radius-two orbit census changed")
    contested = contested_family(neighborhood)
    contested_support = sum(
        matching_rank(feasible_graph(values, partition)) == N
        for partition in contested
    )
    if len(contested) != 21 or contested_support != 8:
        raise AssertionError("contested-family census changed")

    boundary = json.loads(contested_path.read_text())
    if (
        boundary.get("schema")
        != "common-favorite-rank1-triple-conversion-cpsat-v1"
        or boundary.get("status") != "MASTER_UNKNOWN"
        or boundary.get("solver_status") != "UNKNOWN"
        or boundary.get("conversion_scope") != "radius2_contested"
        or boundary.get("blocked_partition_count") != 21
        or boundary.get("values") is not None
    ):
        raise ValueError("contested-radius boundary metadata changed")
    pool, sequence = reconstruct_pool(boundary["cegar_trace"], contested)
    if len(pool) != 302 or len(pool) != boundary["singleton_obstruction_pool_size"]:
        raise AssertionError("contested-radius pool changed")
    proto = Path(boundary["proto"])
    if not proto.is_file() or sha256(proto) != boundary["proto_sha256"]:
        raise AssertionError("contested-radius CP-SAT proto changed")

    result = {
        "schema": SCHEMA,
        "status": "CONTESTED_RADIUS_TWO_EARLY_GATE_SUPERSEDED",
        "n": 4,
        "m": 9,
        "domain": "positive additive valuations",
        "strict_common_favorite": FAVORITE,
        "source_profile": str(local6_path),
        "source_profile_sha256": sha256(local6_path),
        "radius_two_partition_count": len(neighborhood),
        "radius_two_orbit_count": len(observed_orbits),
        "orbit_census": {
            key: {"partition_count": total, "supporting_count": support}
            for key, (total, support) in observed_orbits.items()
        },
        "contested_partner_family": {
            "partition_count": len(contested),
            "supporting_count_in_source_profile": contested_support,
            "description": (
                "The favorite receives a good from the common contested "
                "triple; the family contains three direct and eighteen "
                "two-step favorite-pair conversions."
            ),
        },
        "decision_boundary": {
            "source": str(contested_path),
            "source_sha256": sha256(contested_path),
            "reconstructed_singleton_pool_size": len(pool),
            "supported_singleton_count_sequence": sequence,
            "solver_status": boundary["solver_status"],
            "solver_wall_seconds": boundary["solver_wall_seconds"],
            "proto_sha256": boundary["proto_sha256"],
        },
        "superseded_by": (
            "results/efx49_common_favorite_rank1_contested_refutation_audit.json"
        ),
        "claim_boundary": (
            "This historical UNKNOWN endpoint decided neither direction. A "
            "later exact cap-6 profile refutes the 21-state implication and "
            "is recorded in the superseding audit."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local6", type=Path, required=True)
    parser.add_argument("--contested", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.local6, args.contested, args.output)


if __name__ == "__main__":
    main()
