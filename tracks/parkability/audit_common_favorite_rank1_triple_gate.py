#!/usr/bin/env python3
"""Audit the rank-one common-column triple conversion gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core, independent
    from .anneal import atomic_json
    from .audit_matching_augmentation import feasible_graph, matching_rank
    from .decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from .decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )
except ImportError:
    import core
    import independent
    from anneal import atomic_json
    from audit_matching_augmentation import feasible_graph, matching_rank
    from decide_common_favorite_rank1_triple_conversion import (
        FAVORITE,
        N,
        RESIDUAL,
        conversion_partitions,
        resident_graph,
    )
    from decide_common_favorite_threshold_pass_hall import (
        residual_partitions,
        threshold_passes,
    )


SCHEMA = "common-favorite-rank1-triple-gate-audit-v1"
BOUNDARY_VALUES = (
    (514, 10, 247, 267, 207, 207, 80, 504, 504),
    (183, 12, 1, 16, 9, 9, 9, 14, 1),
    (198, 15, 4, 10, 1, 1, 1, 4, 20),
    (250, 12, 116, 131, 3, 3, 3, 146, 98),
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(partition):
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


def supporting(values, partitions):
    return tuple(
        partition
        for partition in partitions
        if matching_rank(feasible_graph(values, partition)) == N
    )


def audit_unconditional_boundary():
    values = core.validate_values(
        BOUNDARY_VALUES,
        expected_n=4,
        expected_m=9,
        lower=1,
    )
    graph = resident_graph(values)
    if (
        any(row[FAVORITE] <= max(row[1:]) for row in values)
        or not threshold_passes(values, 0, RESIDUAL)
        or graph != ((True, False, False),) * 3
    ):
        raise AssertionError("unconditional boundary left the rank-one cell")
    conversions = conversion_partitions()
    if supporting(values, conversions):
        raise AssertionError("unconditional boundary gained a local conversion")

    singleton_universe = tuple(
        ((FAVORITE,),) + partition for partition in residual_partitions()
    )
    singleton_support = supporting(values, singleton_universe)
    all_support = supporting(
        values,
        tuple(core.iter_unlabeled_nonempty_partitions(4, 9)),
    )
    support_shapes = Counter(shape(partition) for partition in all_support)
    literal_count = independent.count_complete_efx0(values)
    if (
        len(singleton_support) != 116
        or len(all_support) != 116
        or support_shapes != Counter({"3321": 77, "4221": 31, "4311": 7, "5211": 1})
        or literal_count != 301
    ):
        raise AssertionError("unconditional boundary census changed")
    return {
        "values": [list(row) for row in values],
        "resident_graph": [list(row) for row in graph],
        "selected_owner_threshold_pass": True,
        "local_conversion_supporting_partition_count": 0,
        "favorite_singleton_supporting_partition_count": len(singleton_support),
        "all_supporting_partition_count": len(all_support),
        "supporting_partition_count_by_shape": dict(sorted(support_shapes.items())),
        "complete_efx_allocation_count": literal_count,
    }


def audit_dense_boundary(path):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != "common-favorite-rank1-triple-conversion-lra-v1"
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "unknown"
        or payload.get("favorite_singleton_partition_count") != 966
        or payload.get("values") is not None
    ):
        raise ValueError("dense rank-one boundary metadata changed")
    formula = path.parent / Path(payload["formula"]).name
    if not formula.is_file() or sha256(formula) != payload["formula_sha256"]:
        raise AssertionError("dense rank-one formula changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "solver_status": payload["solver_status"],
        "reason_unknown": payload["reason_unknown"],
        "time_limit_seconds": payload["time_limit_seconds"],
        "formula_sha256": payload["formula_sha256"],
        "formula_bytes": payload["formula_bytes"],
    }


def audit_cegar_boundary(path, normalization_path):
    payload = json.loads(path.read_text())
    if (
        payload.get("schema")
        != "common-favorite-rank1-triple-conversion-cegar-v1"
        or payload.get("status") != "MASTER_UNKNOWN"
        or payload.get("solver_status") != "unknown"
        or payload.get("iterations") != 1
        or payload.get("learned_singleton_count") != 185
        or payload.get("values") is not None
    ):
        raise ValueError("sparse rank-one boundary metadata changed")
    record = payload["trace"][0]
    values = tuple(tuple(row) for row in record["values"])
    if (
        record["iteration"] != 1
        or record["learned_singleton_count_before"] != 0
        or matching_rank(resident_graph(values)) != 1
        or supporting(values, conversion_partitions())
    ):
        raise AssertionError("sparse trace left the rank-one cell")
    singleton_support = supporting(
        values,
        tuple(((FAVORITE,),) + partition for partition in residual_partitions()),
    )
    if (
        len(singleton_support) != 185
        or record["supported_unlearned_singleton_count"] != 185
    ):
        raise AssertionError("sparse singleton pool changed")
    formula = path.parent / Path(payload["formula"]).name
    if not formula.is_file() or sha256(formula) != payload["formula_sha256"]:
        raise AssertionError("sparse rank-one formula changed")

    normalization = json.loads(normalization_path.read_text())
    normalized = normalization_path.parent / Path(normalization["output"]).name
    if (
        normalization.get("schema") != "strict-smt2-normalization-v1"
        or normalization["source_sha256"] != payload["formula_sha256"]
        or not normalized.is_file()
        or sha256(normalized) != normalization["output_sha256"]
    ):
        raise AssertionError("cvc5 normalization chain changed")
    return {
        "source": str(path),
        "source_sha256": sha256(path),
        "solver_status": payload["solver_status"],
        "reason_unknown": payload["reason_unknown"],
        "reconstructed_singleton_pool_size": len(singleton_support),
        "formula_sha256": payload["formula_sha256"],
        "formula_bytes": payload["formula_bytes"],
        "normalization_source": str(normalization_path),
        "normalization_source_sha256": sha256(normalization_path),
        "normalized_formula_sha256": normalization["output_sha256"],
    }


def run(dense_path, cegar_path, normalization_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    result = {
        "schema": SCHEMA,
        "status": "RANK1_TRIPLE_EARLY_GATE_SUPERSEDED",
        "n": 4,
        "m": 9,
        "domain": "positive additive valuations",
        "strict_common_favorite": FAVORITE,
        "unconditional_three_conversion_boundary": audit_unconditional_boundary(),
        "dense_exact_real_boundary": audit_dense_boundary(dense_path),
        "sparse_exact_real_boundary": audit_cegar_boundary(
            cegar_path,
            normalization_path,
        ),
        "proved_normal_form": (
            "Every row of a resident feasibility graph is nonempty. Hence "
            "rank one forces all three residents to accept only one common "
            "bundle A. For each resident i, threshold_i(A) is then strictly "
            "larger than the total value of either side bundle."
        ),
        "then_candidate_lemma": (
            "If the common bundle A is a triple and the selected 3+3+2 "
            "partition passes its owner's threshold, then either a favorite-"
            "singleton EFX partition exists or moving one good of A next to "
            "the favorite produces a balanced EFX partition."
        ),
        "superseded_by": "results/efx49_common_favorite_rank1_local6_boundary_audit.json",
        "claim_boundary": (
            "These early dense and sparse exact-real formulas ended UNKNOWN. "
            "A later exact cap-20 profile refutes the candidate lemma even "
            "with every favorite-singleton partition excluded."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dense", type=Path, required=True)
    parser.add_argument("--cegar", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.dense, args.cegar, args.normalization, args.output)


if __name__ == "__main__":
    main()
