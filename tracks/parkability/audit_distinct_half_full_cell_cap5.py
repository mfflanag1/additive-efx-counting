#!/usr/bin/env python3
"""Audit the independently corroborated cap-5 full-cell closure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_distinct_half_rank_augmentation import audit_branch
    from .decide_distinct_half_full_cell_lia import reconstruct_pool
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from .run_distinct_half_full_cell_cegar import full_hall_cells
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_rank_augmentation import audit_branch
    from decide_distinct_half_full_cell_lia import reconstruct_pool
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe
    from run_distinct_half_full_cell_cegar import full_hall_cells


SCHEMA = "distinct-half-full-cell-cap5-audit-v1"
SOURCE_SCHEMA = "distinct-half-full-cell-cpsat-cegar-v1"
CORE_SCHEMA = "distinct-half-full-cell-cpsat-assumption-core-v1"
REPLAY_SCHEMA = "distinct-half-full-cell-lia-replay-v1"
LIA_CORE_SCHEMA = "distinct-half-full-cell-lia-assumption-core-v1"
MINIMAL_CORE_SCHEMA = "distinct-half-full-cell-threshold-cnf-minimal-core-v1"
CNF_SCHEMA = "distinct-half-full-cell-threshold-cnf-result-v1"
DRAT_SCHEMA = "distinct-half-full-cell-drat-verification-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repo_relative(path: Path) -> Path:
    """Normalize recorded absolute paths without weakening file identity."""
    path = Path(path)
    for anchor in ("results", "output"):
        if anchor in path.parts:
            return Path(*path.parts[path.parts.index(anchor) :])
    return path


def decode_partition(raw):
    return tuple(tuple(bundle) for bundle in raw)


def audit(
    source_path: Path,
    core_path: Path,
    replay_path: Path,
    smt2_path: Path,
    lia_core2_path: Path,
    lia_core3_path: Path,
    minimal_core_path: Path,
    cnf_result_path: Path,
    cnf_path: Path,
    drat_result_path: Path,
    compressed_proof_path: Path,
):
    source = json.loads(source_path.read_text())
    core = json.loads(core_path.read_text())
    replay = json.loads(replay_path.read_text())
    lia_core2 = json.loads(lia_core2_path.read_text())
    lia_core3 = json.loads(lia_core3_path.read_text())
    minimal_core = json.loads(minimal_core_path.read_text())
    cnf_result = json.loads(cnf_result_path.read_text())
    drat_result = json.loads(drat_result_path.read_text())
    universe = tuple(favorite_pair_balanced_universe())
    universe_set = set(universe)
    reconstructed_source, pool, trace_counts = reconstruct_pool(
        source_path, universe
    )
    if reconstructed_source != source:
        raise AssertionError("source reconstruction changed")

    core_partitions = tuple(
        decode_partition(partition) for partition in core["core_partitions"]
    )
    if len(core_partitions) != len(set(core_partitions)):
        raise AssertionError("core contains duplicate partitions")
    if not set(core_partitions).issubset(pool):
        raise AssertionError("core is not a subset of the reconstructed pool")
    if not set(core_partitions).issubset(universe_set):
        raise AssertionError("core contains a non-favorite-pair partition")
    lia_core2_partitions = tuple(
        decode_partition(partition) for partition in lia_core2["core_partitions"]
    )
    lia_core3_partitions = tuple(
        decode_partition(partition) for partition in lia_core3["core_partitions"]
    )
    minimal_core_partitions = tuple(
        decode_partition(partition)
        for partition in minimal_core["core_partitions"]
    )
    if (
        len(lia_core2_partitions) != len(set(lia_core2_partitions))
        or len(lia_core3_partitions) != len(set(lia_core3_partitions))
        or not set(lia_core2_partitions).issubset(core_partitions)
        or not set(lia_core3_partitions).issubset(lia_core2_partitions)
        or len(minimal_core_partitions) != len(set(minimal_core_partitions))
        or not set(minimal_core_partitions).issubset(lia_core3_partitions)
    ):
        raise AssertionError("nested arithmetic cores changed")

    trace_values = source["trace"][0]["values"]
    audit_branch(trace_values)
    if full_hall_cells(trace_values):
        raise AssertionError("CEGAR trace model unexpectedly has a full cell")

    source_hash = sha256(source_path)
    core_hash = sha256(core_path)
    smt2_hash = sha256(smt2_path)
    lia_core2_hash = sha256(lia_core2_path)
    lia_core3_hash = sha256(lia_core3_path)
    minimal_core_hash = sha256(minimal_core_path)
    lia_core2_smt2 = Path(lia_core2["smt2_path"])
    lia_core3_smt2 = Path(lia_core3["smt2_path"])
    cnf_hash = sha256(cnf_path)
    compressed_proof_hash = sha256(compressed_proof_path)
    expected_cp_counts = {
        "low_pair_cells": 28,
        "accept_literals": 1680,
        "hall_failure_templates_per_pairing": 21,
        "hall_witness_literals": 8820,
    }
    expected_lia_counts = {
        "low_pair_cells": 28,
        "accept_literals": 1680,
        "hall_failure_templates_per_pairing": 21,
        "pairing_failure_terms": 420,
    }
    expected_symmetry = [
        "nonincreasing favorite values by agent",
        "nonincreasing agent-0 values on goods 5..8",
    ]
    if (
        source.get("schema") != SOURCE_SCHEMA
        or source.get("status") != "FINITE_CAP_UNSAT_CANDIDATE"
        or source.get("solver_status") != "INFEASIBLE"
        or source.get("cap") != 5
        or source.get("pool_size") != 416
        or trace_counts != [361]
        or core.get("schema") != CORE_SCHEMA
        or core.get("status") != "ASSUMPTION_CORE_EXTRACTED"
        or core.get("solver_status") != "INFEASIBLE"
        or core.get("cap") != 5
        or core.get("pool_size") != 416
        or core.get("core_size") != 330
        or len(core_partitions) != 330
        or core.get("source_sha256") != source_hash
        or replay.get("schema") != REPLAY_SCHEMA
        or replay.get("status") != "FINITE_CAP_UNSAT_CANDIDATE"
        or replay.get("solver_status") != "unsat"
        or replay.get("cap") != 5
        or replay.get("pool_size") != 330
        or replay.get("source_sha256") != source_hash
        or replay.get("core_source", {}).get("sha256") != core_hash
        or replay.get("smt2_sha256") != smt2_hash
        or not replay.get("full_hall_cell_forbidden")
        or source.get("favorite_pair_partition_count") != len(universe)
        or replay.get("favorite_pair_partition_count") != len(universe)
        or source.get("full_cell_encoding") != expected_cp_counts
        or replay.get("full_cell_encoding") != expected_lia_counts
        or source.get("symmetry_breaking") != expected_symmetry
        or replay.get("symmetry_breaking") != expected_symmetry
        or lia_core2.get("schema") != LIA_CORE_SCHEMA
        or lia_core2.get("status") != "ASSUMPTION_CORE_EXTRACTED"
        or lia_core2.get("solver_status") != "unsat"
        or lia_core2.get("cap") != 5
        or lia_core2.get("pool_size") != 330
        or lia_core2.get("core_size") != 204
        or Path(lia_core2.get("source")) != core_path
        or lia_core2.get("source_sha256") != core_hash
        or lia_core2.get("symmetry_breaking") != expected_symmetry
        or sha256(lia_core2_smt2) != lia_core2.get("smt2_sha256")
        or lia_core3.get("schema") != LIA_CORE_SCHEMA
        or lia_core3.get("status") != "ASSUMPTION_CORE_EXTRACTED"
        or lia_core3.get("solver_status") != "unsat"
        or lia_core3.get("cap") != 5
        or lia_core3.get("pool_size") != 204
        or lia_core3.get("core_size") != 193
        or Path(lia_core3.get("source")) != lia_core2_path
        or lia_core3.get("source_sha256") != lia_core2_hash
        or lia_core3.get("symmetry_breaking") != expected_symmetry
        or sha256(lia_core3_smt2) != lia_core3.get("smt2_sha256")
        or minimal_core.get("schema") != MINIMAL_CORE_SCHEMA
        or minimal_core.get("status")
        != "DELETION_MINIMAL_UNSAT_CORE_VERIFIED"
        or minimal_core.get("cap") != 5
        or Path(minimal_core.get("parent")) != lia_core3_path
        or minimal_core.get("parent_sha256") != lia_core3_hash
        or minimal_core.get("parent_core_size") != 193
        or minimal_core.get("core_size") != 17
        or len(minimal_core_partitions) != 17
        or len(minimal_core.get("removal_boundaries", [])) != 17
        or cnf_result.get("schema") != CNF_SCHEMA
        or cnf_result.get("status") != "UNSAT"
        or cnf_result.get("cap") != 5
        or cnf_result.get("partition_pool_size") != 17
        or repo_relative(cnf_result.get("source"))
        != repo_relative(minimal_core_path)
        or cnf_result.get("source_sha256") != minimal_core_hash
        or repo_relative(cnf_result.get("dimacs_path"))
        != repo_relative(cnf_path)
        or cnf_result.get("dimacs_sha256") != cnf_hash
        or cnf_result.get("variables") != 337000
        or cnf_result.get("clauses") != 702820
        or cnf_result.get("solver", {}).get("status") != "UNSAT"
        or drat_result.get("schema") != DRAT_SCHEMA
        or drat_result.get("status") != "VERIFIED"
        or drat_result.get("cnf", {}).get("sha256") != cnf_hash
        or drat_result.get("cnf_result_sha256") != sha256(cnf_result_path)
        or drat_result.get("proof", {}).get("compressed_sha256")
        != compressed_proof_hash
        or drat_result.get("proof_checker", {}).get("returncode") != 0
        or "s VERIFIED"
        not in drat_result.get("proof_checker", {}).get("transcript", "")
    ):
        raise AssertionError("cap-5 closure evidence changed")

    formula = smt2_path.read_text()
    if (
        "(declare-fun value_0_0 () Int)" not in formula
        or "(check-sat)" not in formula
        or "() Real)" in formula
    ):
        raise AssertionError("expected a self-contained QF_LIA replay formula")

    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FULL_CELL_CAP5_CORROBORATED",
        "scope": {
            "agents": 4,
            "goods": 9,
            "item_values": "integers in {1,2,3,4,5}",
            "strict_common_favorite": 0,
            "fixed_half_favorite_representatives": [1, 2, 3, 4],
            "universal_owner_threshold_failure": True,
        },
        "conclusion": (
            "Some favorite-pair balanced partition is EFX-supporting, or "
            "some favorite-triple low pair has all 15 residual pairings "
            "passing the Hall test; either alternative yields complete EFX."
        ),
        "universe": {
            "favorite_pair_partitions": len(universe),
            "initial_complement_pool": 55,
            "cegar_trace_survivors": trace_counts,
            "closed_pool": len(pool),
            "cp_sat_core": len(core_partitions),
            "first_qf_lia_core": len(lia_core2_partitions),
            "qf_lia_core": len(lia_core3_partitions),
            "sufficient_core": len(minimal_core_partitions),
        },
        "independent_encodings": {
            "cp_sat": {
                "status": source["solver_status"],
                "pool_size": source["pool_size"],
            },
            "qf_lia": {
                "status": replay["solver_status"],
                "pool_size": replay["pool_size"],
                "threshold_encoding": replay["universal_threshold_encoding"],
            },
            "threshold_cnf": {
                "status": cnf_result["status"],
                "pool_size": cnf_result["partition_pool_size"],
                "variables": cnf_result["variables"],
                "clauses": cnf_result["clauses"],
                "solver": cnf_result["solver"]["backend"],
                "drat_proof": drat_result["status"],
            },
        },
        "artifacts": {
            "cp_sat_cegar_sha256": source_hash,
            "cp_sat_core_sha256": core_hash,
            "qf_lia_result_sha256": sha256(replay_path),
            "qf_lia_formula_sha256": smt2_hash,
            "qf_lia_core204_sha256": lia_core2_hash,
            "qf_lia_core204_formula_sha256": sha256(lia_core2_smt2),
            "qf_lia_core193_sha256": lia_core3_hash,
            "qf_lia_core193_formula_sha256": sha256(lia_core3_smt2),
            "deletion_minimal_core17_sha256": minimal_core_hash,
            "threshold_cnf_result_sha256": sha256(cnf_result_path),
            "threshold_cnf_formula_sha256": cnf_hash,
            "drat_verification_sha256": sha256(drat_result_path),
            "compressed_drat_sha256": compressed_proof_hash,
        },
        "trust_boundary": (
            "This is a finite integer-cap theorem in one structural branch. "
            "It is not a real-valued theorem and does not resolve general "
            "additive EFX. CP-SAT, Z3/QF_LIA, and threshold CNF are three "
            "distinct encodings, and the frozen CNF UNSAT verdict has a "
            "binary DRAT proof independently accepted by drat-trim."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--lia-core2", type=Path, required=True)
    parser.add_argument("--lia-core3", type=Path, required=True)
    parser.add_argument("--minimal-core", type=Path, required=True)
    parser.add_argument("--cnf-result", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--drat-result", type=Path, required=True)
    parser.add_argument("--compressed-proof", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(
        args.source,
        args.core,
        args.replay,
        args.smt2,
        args.lia_core2,
        args.lia_core3,
        args.minimal_core,
        args.cnf_result,
        args.cnf,
        args.drat_result,
        args.compressed_proof,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
