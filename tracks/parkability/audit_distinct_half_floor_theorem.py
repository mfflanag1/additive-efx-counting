#!/usr/bin/env python3
"""Audit dual exact-real encodings of the distinct-half floor theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_distinct_half_pair_cover import favorite_pair_balanced_universe
except ImportError:
    from anneal import atomic_json
    from decide_distinct_half_pair_cover import favorite_pair_balanced_universe


SCHEMA = "distinct-half-floor-dual-encoding-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(results_dir: Path) -> dict:
    expected = (
        (
            "matching_clauses",
            "favorite-pair-balanced-floor",
            "efx49_distinct_half_favorite_pair_floor_lra_session2.json",
        ),
        (
            "hall_selectors",
            "favorite-pair-balanced-floor-hall",
            "efx49_distinct_half_favorite_pair_floor_hall_session1.json",
        ),
    )
    records = []
    for encoding, target_kind, filename in expected:
        result_path = results_dir / filename
        source = json.loads(result_path.read_text())
        if (
            source.get("schema") != "distinct-half-pair-cover-lra-result-v1"
            or source.get("status") != "UNSAT_CANDIDATE"
            or source.get("solver_status") != "unsat"
            or source.get("domain")
            != "strictly positive reals normalized per row"
            or source.get("n") != 4
            or source.get("m") != 9
            or source.get("favorite") != 0
            or source.get("fixed_half_favorite_representatives") != [1, 2, 3, 4]
            or source.get("universal_owner_threshold_failure") is not True
            or source.get("target_kind") != target_kind
            or source.get("target_state_count") != 840
            or source.get("pool_size") != 840
            or source.get("values") is not None
        ):
            raise AssertionError((encoding, "result scope changed"))
        smt2_path = results_dir / Path(source["smt2_path"]).name
        if sha256(smt2_path) != source["smt2_sha256"]:
            raise AssertionError((encoding, "SMT-LIB hash mismatch"))
        records.append({
            "encoding": encoding,
            "result": str(result_path.resolve()),
            "result_sha256": sha256(result_path),
            "smt2": str(smt2_path.resolve()),
            "smt2_sha256": source["smt2_sha256"],
        })
    if len(favorite_pair_balanced_universe()) != 840:
        raise AssertionError("favorite-pair balanced universe changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_FLOOR_DUAL_ENCODING_AUDIT_PASSED",
        "domain": "strictly positive reals normalized per row",
        "target_partition_count": 840,
        "encodings": records,
        "claim": (
            "Matching-clause and Hall-selector QF_LRA encodings both reject "
            "a universally owner-threshold-obstructed strict-common-favorite "
            "profile with fixed distinct half-favorite representatives and "
            "no favorite-pair balanced owner-floor matching."
        ),
        "trust_boundary": (
            "This is a dual-encoded Z3 UNSAT theorem candidate, not an "
            "independently proof-checked certificate or an analytic proof."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.results_dir)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
