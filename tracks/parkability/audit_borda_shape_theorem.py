#!/usr/bin/env python3
"""Audit the dual-encoding 4x9 Borda-EFX theorem package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_generic_partition_cegar import load_pool
except ImportError:
    from anneal import atomic_json
    from run_generic_partition_cegar import load_pool


SCHEMA = "borda-efx-4x9-dual-encoding-audit-v1"
PATTERNS = {
    "4": (0, 0, 0, 0),
    "31": (0, 0, 0, 1),
    "22": (0, 0, 1, 1),
    "211": (0, 0, 1, 2),
    "1111": (0, 1, 2, 3),
}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_committed_artifact(raw_path: str, results_dir: Path) -> Path:
    """Resolve legacy absolute artifact paths inside a clean checkout."""
    path = Path(raw_path)
    if path.is_file():
        return path
    committed = results_dir / path.name
    if committed.is_file():
        return committed
    return committed


def audit(results_dir: Path) -> dict:
    cells = []
    pool_hashes = set()
    pool_paths = set()
    for pattern_name, pattern in PATTERNS.items():
        for encoding, suffix in (
            ("matching_clauses", ""),
            ("hall_selectors", "_hall"),
        ):
            stem = f"efx49_borda_shape3222_favorites{pattern_name}{suffix}_session1"
            result_path = results_dir / f"{stem}.json"
            raw = json.loads(result_path.read_text())
            expected = {
                "schema": "integer-partition-cp-sat-result-v1",
                "status": "UNSAT_BOUNDED_CELL_CANDIDATE",
                "n": 4,
                "m": 9,
                "upper": 9,
                "partition_universe_size": 1260,
                "partition_shape": [3, 2, 2, 2],
                "pool_size": 417,
                "symmetry": "none",
                "exclude_universal_min": False,
                "exclude_peelable": False,
                "require_pairwise_distinct_rows": False,
                "require_distinct_item_values": True,
                "obstruction_encoding": encoding,
                "favorite_pattern": list(pattern),
                "favorite_pattern_stabilizer": False,
                "solver_status": "INFEASIBLE",
                "values": None,
            }
            mismatches = {
                key: {"expected": value, "actual": raw.get(key)}
                for key, value in expected.items()
                if raw.get(key) != value
            }
            if mismatches:
                raise AssertionError((result_path, mismatches))
            if not raw.get("trace") or raw["trace"][-1].get(
                "solver_status"
            ) != "INFEASIBLE":
                raise AssertionError(f"{result_path} lacks an infeasible trace")
            proto_path = resolve_committed_artifact(raw["proto_path"], results_dir)
            if (
                not proto_path.is_file()
                or file_sha256(proto_path) != raw["proto_sha256"]
                or proto_path.stat().st_size != raw["proto_bytes"]
            ):
                raise AssertionError(f"{result_path} has a broken proto reference")
            raw_pool_path = raw.get("pool_path")
            pool_path = (
                resolve_committed_artifact(raw_pool_path, results_dir)
                if raw_pool_path
                else results_dir
                / f"efx49_borda_shape3222_favorites{pattern_name}"
                f"{suffix}_pool.json"
            )
            if not pool_path.is_file():
                raise AssertionError(f"{result_path} has no pool file")
            if file_sha256(pool_path) != raw["pool_sha256"]:
                raise AssertionError(f"{result_path} has a broken pool hash")
            pool = load_pool(pool_path, 4, 9)
            if len(pool) != 417 or any(
                tuple(sorted(map(len, partition), reverse=True)) != (3, 2, 2, 2)
                for partition in pool
            ):
                raise AssertionError(f"{pool_path} is not the claimed shape pool")
            pool_hashes.add(raw["pool_sha256"])
            pool_paths.add(str(pool_path.resolve()))
            cells.append({
                "favorite_multiplicity": pattern_name,
                "favorite_pattern": list(pattern),
                "encoding": encoding,
                "result_path": str(result_path.resolve()),
                "result_sha256": file_sha256(result_path),
                "proto_path": str(proto_path.resolve()),
                "proto_sha256": raw["proto_sha256"],
                "pool_path": str(pool_path.resolve()),
                "pool_sha256": raw["pool_sha256"],
                "solver_status": raw["solver_status"],
                "wall_time_seconds": raw["trace"][-1]["wall_time_seconds"],
                "comparison_variables": raw["comparison_variables"],
                "matching_clauses": raw["matching_clauses"],
                "hall_selectors": raw["hall_selectors"],
                "hall_edge_clauses": raw["hall_edge_clauses"],
            })
    if len(pool_hashes) != 1:
        raise AssertionError("the theorem cells do not use an identical pool")
    core_pool_path = (
        results_dir
        / "efx49_borda_shape3222_favorites211_core17_matching_pool.json"
    )
    core_pool = load_pool(core_pool_path, 4, 9)
    if len(core_pool) != 17:
        raise AssertionError("the proof-checked core does not have 17 partitions")
    core_pool_sha256 = file_sha256(core_pool_path)
    core_matching = json.loads(
        (
            results_dir
            / "efx49_borda_shape3222_favorites211_core17_matching.json"
        ).read_text()
    )
    core_hall = json.loads(
        (
            results_dir
            / "efx49_borda_shape3222_favorites211_core17_hall.json"
        ).read_text()
    )
    core_z3 = json.loads(
        (
            results_dir
            / "efx49_borda_shape3222_favorites211_core17_z3.json"
        ).read_text()
    )
    core_cvc5 = json.loads(
        (
            results_dir
            / "efx49_borda_shape3222_favorites211_core17_cvc5.json"
        ).read_text()
    )
    core_cpc = json.loads(
        (
            results_dir
            / "efx49_borda_shape3222_favorites211_core17_cpc_ethos.json"
        ).read_text()
    )
    if (
        core_matching.get("solver_status") != "INFEASIBLE"
        or core_matching.get("pool_sha256") != core_pool_sha256
        or core_hall.get("solver_status") != "INFEASIBLE"
        or core_hall.get("pool_sha256") != core_pool_sha256
        or core_z3.get("solver_status") != "unsat"
        or core_z3.get("pool_sha256") != core_pool_sha256
        or core_cvc5.get("verdict") != "unsat"
        or core_cvc5.get("confirmed_expected") is not True
        or core_cpc.get("verified") is not True
        or core_cpc.get("check", {}).get("status") != "correct"
    ):
        raise AssertionError("the proof-checked 17-partition core is incomplete")
    proof_path = resolve_committed_artifact(core_cpc["proof"], results_dir)
    if (
        not proof_path.is_file()
        or file_sha256(proof_path) != core_cpc["proof_sha256"]
    ):
        raise AssertionError("the proof-checked core has a broken CPC proof")
    return {
        "schema": SCHEMA,
        "status": "DUAL_ENCODING_AUDIT_PASSED",
        "claim": (
            "Every four-agent, nine-good Borda-additive instance admits "
            "a complete EFX allocation with bundle-size multiset (3,2,2,2)."
        ),
        "claim_level": (
            "computer-assisted theorem candidate: ten exact dual-encoding "
            "CP-SAT verdicts; the hardest 2+1+1 core is independently "
            "proved by Z3 and cvc5 and CPC-checked by Ethos"
        ),
        "borda_definition": (
            "For each agent, the nine item values are a permutation of "
            "1,2,...,9 (independent positive row scaling is immaterial)."
        ),
        "favorite_orbits": list(PATTERNS),
        "favorite_orbit_count": len(PATTERNS),
        "encodings": ["matching_clauses", "hall_selectors"],
        "cell_count": len(cells),
        "partition_shape": [3, 2, 2, 2],
        "shape_universe_size": 1260,
        "pooled_partition_count": 417,
        "shared_pool_sha256": next(iter(pool_hashes)),
        "pool_files": sorted(pool_paths),
        "cells": cells,
        "proof_checked_core": {
            "favorite_multiplicity": "211",
            "partition_count": 17,
            "pool_path": str(core_pool_path.resolve()),
            "pool_sha256": core_pool_sha256,
            "cp_sat_matching_result": str(
                (
                    results_dir
                    / "efx49_borda_shape3222_favorites211_core17_matching.json"
                ).resolve()
            ),
            "cp_sat_hall_result": str(
                (
                    results_dir
                    / "efx49_borda_shape3222_favorites211_core17_hall.json"
                ).resolve()
            ),
            "z3_result": str(
                (
                    results_dir
                    / "efx49_borda_shape3222_favorites211_core17_z3.json"
                ).resolve()
            ),
            "cvc5_result": str(
                (
                    results_dir
                    / "efx49_borda_shape3222_favorites211_core17_cvc5.json"
                ).resolve()
            ),
            "cpc_ethos_result": str(
                (
                    results_dir
                    / "efx49_borda_shape3222_favorites211_core17_cpc_ethos.json"
                ).resolve()
            ),
            "cpc_proof": str(proof_path.resolve()),
            "cpc_proof_sha256": core_cpc["proof_sha256"],
            "cpc_proof_bytes": core_cpc["proof_bytes"],
            "cpc_proof_steps": core_cpc["proof_step_lines"],
            "ethos_status": core_cpc["check"]["status"],
        },
        "limitations": [
            "This does not prove complete EFX for arbitrary additive values.",
            "Both encodings were solved by the same OR-Tools CP-SAT engine.",
            "Four favorite-orbit cells still lack external proof logs; only the "
            "2+1+1 core currently has a separately checked CPC proof.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.results_dir)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
