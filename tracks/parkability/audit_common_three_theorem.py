#!/usr/bin/env python3
"""Audit the two exact-real encodings of the common-three theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_common_three_anchored import anchored_partitions
except ImportError:
    from anneal import atomic_json
    from decide_common_three_anchored import anchored_partitions


SCHEMA = "common-three-dual-encoding-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(results_dir: Path) -> dict:
    records = []
    expected = (
        ("matching_clauses", "efx49_common_three_anchored_matching_session1.json"),
        ("hall_selectors", "efx49_common_three_anchored_hall_session1.json"),
    )
    for encoding, filename in expected:
        result_path = results_dir / filename
        source = json.loads(result_path.read_text())
        if (
            source.get("schema") != "common-three-anchored-lra-result-v1"
            or source.get("status") != "UNSAT"
            or source.get("solver_status") != "unsat"
            or source.get("domain")
            != "strictly positive reals normalized per row"
            or source.get("n") != 4
            or source.get("m") != 9
            or source.get("favorite") != 0
            or source.get("shared_half_favorite_set") != [1, 2, 3]
            or source.get("low_goods") != [4, 5, 6, 7, 8]
            or source.get("target_partition_count") != 240
            or source.get("obstruction_encoding") != encoding
            or source.get("values") is not None
        ):
            raise AssertionError((encoding, "result scope changed"))
        smt2_path = Path(source["smt2_path"])
        if sha256(smt2_path) != source["smt2_sha256"]:
            raise AssertionError((encoding, "SMT-LIB hash mismatch"))
        records.append({
            "encoding": encoding,
            "result": str(result_path.resolve()),
            "result_sha256": sha256(result_path),
            "smt2": str(smt2_path.resolve()),
            "smt2_sha256": source["smt2_sha256"],
        })
    if len(anchored_partitions()) != 240:
        raise AssertionError("anchored family reconstruction changed")
    return {
        "schema": SCHEMA,
        "status": "COMMON_THREE_DUAL_ENCODING_AUDIT_PASSED",
        "domain": "strictly positive reals normalized per row",
        "target_partition_count": 240,
        "encodings": records,
        "claim": (
            "Matching-clause and Hall-selector QF_LRA encodings both reject "
            "a common-three profile with no anchor-separated balanced EFX "
            "partition."
        ),
        "trust_boundary": (
            "These Z3 UNSAT results corroborate the cap-free analytic "
            "exchange proof but are not independently proof-checked certificates."
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
