#!/usr/bin/env python3
"""Aggregate the seven proof-checked 2+1+1 bottom-pair patterns."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        goods_pattern,
        multiplicity_signature,
    )
except ImportError:
    from anneal import atomic_json
    from run_bottom_pair_pattern_selector_cegar import (
        CANONICAL_PATTERNS,
        goods_pattern,
        multiplicity_signature,
    )


SCHEMA = "all-repeated-bottom-pair-conversions-audit-v1"
EXPECTED_PARTITIONS = {
    1: 228,
    2: 225,
    3: 240,
    4: 240,
    5: 255,
    7: 255,
    8: 270,
}
EXPECTED_STATUSES = {
    1: "STAR_REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    2: "TRIANGLE_REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    3: "REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    4: "REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    5: "REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    7: "REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
    8: "REPEATED_BOTTOM_CONVERSION_PROOF_CHECKED",
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def run(census_path, audit_paths, output):
    census = load(census_path)
    repeated_indices = tuple(
        index
        for index, pattern in enumerate(CANONICAL_PATTERNS)
        if multiplicity_signature(pattern) == (2, 1, 1)
    )
    if repeated_indices != tuple(EXPECTED_PARTITIONS):
        raise AssertionError("2+1+1 canonical pattern indices changed")
    if not (
        census.get("schema") == "bottom-pair-pattern-census-audit-v1"
        and census.get("status") == "BOTTOM_PAIR_PATTERN_CENSUS_AUDITED"
        and census.get("canonical_pattern_count") == 20
        and census.get("multiplicity_census", {}).get("2+1+1") == 7
        and census.get("canonical_patterns")
        == [[list(edge) for edge in pattern] for pattern in CANONICAL_PATTERNS]
    ):
        raise AssertionError("bottom-pair census changed")

    audits = {}
    sources = {}
    for path in audit_paths:
        payload = load(path)
        pattern_index = payload.get("pattern_index")
        if pattern_index in audits:
            raise AssertionError("duplicate repeated-pattern audit")
        if pattern_index not in EXPECTED_PARTITIONS:
            raise AssertionError("non-2+1+1 pattern entered the aggregate")
        if not (
            payload.get("status") == EXPECTED_STATUSES[pattern_index]
            and payload.get("agent_bottom_pairs")
            == [list(pair) for pair in goods_pattern(pattern_index)]
            and payload.get("conversion_partition_count")
            == EXPECTED_PARTITIONS[pattern_index]
            and payload.get("z3_cardinal_unsat") is True
            and payload.get("z3_fresh_process_unsat") is True
            and payload.get("z3_sorting_unsat") is True
            and payload.get("cvc5_sorting_unsat") is True
            and payload.get("ethos_status") == "correct"
            and isinstance(payload.get("proof_sha256"), str)
            and len(payload["proof_sha256"]) == 64
            and payload.get("proof_bytes", 0) > 0
            and payload.get("proof_step_lines", 0) > 0
        ):
            raise AssertionError("repeated-pattern proof aggregate changed")
        audits[pattern_index] = payload
        sources[str(pattern_index)] = {
            "path": str(path),
            "sha256": sha256(path),
        }
    if set(audits) != set(EXPECTED_PARTITIONS):
        raise AssertionError("the seven 2+1+1 patterns are not all present")

    ordered = [audits[index] for index in repeated_indices]
    result = {
        "schema": SCHEMA,
        "status": "ALL_2_PLUS_1_PLUS_1_BOTTOM_PATTERNS_PROOF_CHECKED",
        "canonical_pattern_indices": list(repeated_indices),
        "canonical_pattern_count": len(repeated_indices),
        "conversion_partition_counts": {
            str(index): audits[index]["conversion_partition_count"]
            for index in repeated_indices
        },
        "sum_of_case_conversion_partition_counts": sum(
            payload["conversion_partition_count"] for payload in ordered
        ),
        "total_checked_cpc_proof_bytes": sum(
            payload["proof_bytes"] for payload in ordered
        ),
        "total_checked_cpc_proof_step_lines": sum(
            payload["proof_step_lines"] for payload in ordered
        ),
        "all_z3_cardinal_unsat": True,
        "all_fresh_z3_unsat": True,
        "all_z3_sorting_unsat": True,
        "all_cvc5_sorting_unsat": True,
        "all_ethos_correct": True,
        "census": {
            "path": str(census_path),
            "sha256": sha256(census_path),
            "all_canonical_patterns": census["canonical_pattern_count"],
            "repeated_multiplicity_patterns": census["multiplicity_census"][
                "2+1+1"
            ],
        },
        "sources": sources,
        "claim_boundary": (
            "This closes every 2+1+1 selected-bottom-pair pattern inside "
            "the strict-common-favorite universal-threshold branch. The "
            "eleven all-distinct patterns, mixed-threshold branch, full "
            "four-agent/nine-good case, and general additive EFX remain open."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--audit", action="append", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.census, tuple(args.audit), args.output), indent=2))


if __name__ == "__main__":
    main()
