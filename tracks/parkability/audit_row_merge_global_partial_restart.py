#!/usr/bin/env python3
"""Audit the dual-solver seven-good global partial-restart lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_row_merge_partial_entry_radius import (
        global_any_deletion_candidates,
    )
    from .decide_row_merge_single_wall_radius import make_bundles
except ImportError:
    from anneal import atomic_json
    from decide_row_merge_partial_entry_radius import (
        global_any_deletion_candidates,
    )
    from decide_row_merge_single_wall_radius import make_bundles


SCHEMA = "row-merge-global-partial-restart-audit-v1"
SOLVER_SHA256 = "fae4cef47a4e82e3b37f8928b5cb275c8a86d138a33e49d54a9933a157b57f74"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_record(source_path, normalization_path, cvc5_path, witness_size):
    source = json.loads(source_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    formula_path = Path(source["smt2_path"])
    normalized_path = Path(normalization["output"])
    if (
        source.get("schema") != "row-merge-partial-entry-radius-lra-v1"
        or source.get("status") != "UNSAT_CANDIDATE"
        or source.get("solver_status") != "unsat"
        or source.get("n") != 4
        or source.get("m") != 7
        or source.get("bundle_sizes_excluding_critical_good") != [2, 1, 2, 1]
        or source.get("minimal_hall_witness_size") != witness_size
        or source.get("restart_mode") != "global-any-deletion"
        or source.get("partial_entry_radius") != 1
        or source.get("eligible_deleted_goods") != list(range(7))
        or source.get("candidate_partition_count") != 81
        or not source.get("global_wall_isolation_encoded")
        or not formula_path.is_file()
        or sha256(formula_path) != source.get("smt2_sha256")
        or normalization.get("source_sha256") != source.get("smt2_sha256")
        or not normalized_path.is_file()
        or sha256(normalized_path) != normalization.get("output_sha256")
        or cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("formula_sha256") != normalization.get("output_sha256")
        or cvc5.get("solver_sha256") != SOLVER_SHA256
    ):
        raise AssertionError(f"Hall-size-{witness_size} solver chain failed")
    return {
        "minimal_hall_witness_size": witness_size,
        "z3_source": str(source_path),
        "z3_source_sha256": sha256(source_path),
        "z3_formula": str(formula_path),
        "z3_formula_sha256": source["smt2_sha256"],
        "z3_status": "unsat",
        "cvc5_normalization": str(normalization_path),
        "cvc5_normalized_formula_sha256": normalization["output_sha256"],
        "cvc5_result": str(cvc5_path),
        "cvc5_result_sha256": sha256(cvc5_path),
        "cvc5_status": "unsat",
        "candidate_partition_count": 81,
    }


def run(sources, normalizations, cvc5_results, output_path):
    if output_path.exists():
        raise ValueError("output path must be new")
    if not (len(sources) == len(normalizations) == len(cvc5_results) == 3):
        raise ValueError("three Hall-size solver chains are required")
    original, _w, _critical_good, m = make_bundles((2, 1, 2, 1))
    candidates = global_any_deletion_candidates(original, 1)
    if m != 7 or len(candidates) != 81:
        raise AssertionError("the global radius-one candidate universe changed")
    records = [
        audit_record(source, normalization, cvc5, witness_size)
        for witness_size, source, normalization, cvc5 in zip(
            (2, 3, 4), sources, normalizations, cvc5_results
        )
    ]
    result = {
        "schema": SCHEMA,
        "status": "GLOBAL_PARTIAL_RESTART_LEMMA_AUDITED",
        "scope": (
            "four agents, seven goods, wall shape 2+2+2+1, generic "
            "single-wall crossing, Hall sizes 2, 3, and 4"
        ),
        "candidate_construction": (
            "Choose one good to leave unallocated and move at most one of "
            "the six remaining goods between bundles; bundle ownership may change."
        ),
        "candidate_partition_count_per_hall_size": len(candidates),
        "records": records,
        "claim": (
            "For every encoded wall state, at least one of the 81 global "
            "one-good partial-restart partitions supports an EFX matching."
        ),
        "claim_boundary": (
            "This is a fixed seven-good computer-assisted lemma. It does not "
            "complete the unallocated good, extend to larger bundle shapes, "
            "or prove row-merge continuation."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument(
        "--normalization", type=Path, action="append", required=True
    )
    parser.add_argument("--cvc5", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.source, args.normalization, args.cvc5, args.output)


if __name__ == "__main__":
    main()
