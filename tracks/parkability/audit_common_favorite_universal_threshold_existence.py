#!/usr/bin/env python3
"""Aggregate the proof chain for the universal owner-threshold branch."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_bottom_pair_pattern_selector_cegar import CANONICAL_PATTERNS
except ImportError:
    from anneal import atomic_json
    from run_bottom_pair_pattern_selector_cegar import CANONICAL_PATTERNS


SCHEMA = "common-favorite-universal-threshold-existence-audit-v1"
THREE_AGENT_STATUS = "THREE_AGENT_BOTTOM_CONVERSION_PROOF_CHECKED"
DOUBLE_BOTTOM_STATUSES = {
    0: "OVERLAP_DOUBLE_BOTTOM_CONVERSION_PROOF_CHECKED",
    6: "DISJOINT_DOUBLE_BOTTOM_CONVERSION_PROOF_CHECKED",
}
REPEATED_INDICES = (1, 2, 3, 4, 5, 7, 8)
DISTINCT_INDICES = tuple(range(9, 20))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def checked_proof(payload: dict, *, nested: str | None = None) -> tuple[int, int]:
    proof = payload[nested] if nested is not None else payload
    if not (
        proof.get("ethos_status") == "correct"
        and isinstance(proof.get("proof_sha256"), str)
        and len(proof["proof_sha256"]) == 64
        and proof.get("proof_bytes", 0) > 0
        and proof.get("proof_step_lines", 0) > 0
    ):
        raise AssertionError("component proof is not CPC/Ethos checked")
    return proof["proof_bytes"], proof["proof_step_lines"]


def run(
    owner_threshold_path: Path,
    hall_characterization_path: Path,
    census_path: Path,
    three_agent_path: Path,
    double_bottom_paths: tuple[Path, ...],
    repeated_path: Path,
    all_distinct_path: Path,
    output: Path,
) -> dict:
    owner_threshold = load(owner_threshold_path)
    if not (
        owner_threshold.get("schema")
        == "owner-threshold-shape-envelope-audit-v1"
        and owner_threshold.get("status")
        == "OWNER_THRESHOLD_SHAPE_ENVELOPE_AUDIT_PASSED"
        and owner_threshold.get("partition_profile_checks", 0) > 0
        and owner_threshold.get("universal_threshold_checks", 0) > 0
    ):
        raise AssertionError("owner-threshold shape envelope changed")
    hall_characterization = load(hall_characterization_path)
    if not (
        hall_characterization.get("schema")
        == "favorite-triple-hall-characterization-audit-v1"
        and hall_characterization.get("status")
        == "FAVORITE_TRIPLE_HALL_CHARACTERIZATION_AUDIT_PASSED"
        and hall_characterization.get("literal_partition_checks", 0) > 0
    ):
        raise AssertionError("favorite-triple Hall characterization changed")

    census = load(census_path)
    if not (
        census.get("schema") == "bottom-pair-pattern-census-audit-v1"
        and census.get("status") == "BOTTOM_PAIR_PATTERN_CENSUS_AUDITED"
        and census.get("canonical_pattern_count") == 20
        and census.get("multiplicity_census")
        == {"2+2": 2, "2+1+1": 7, "1+1+1+1": 11}
        and census.get("canonical_patterns")
        == [[list(edge) for edge in pattern] for pattern in CANONICAL_PATTERNS]
    ):
        raise AssertionError("bottom-pair census changed")

    three_agent = load(three_agent_path)
    if not (
        three_agent.get("schema")
        == "three-agent-bottom-pairing-conversion-audit-v1"
        and three_agent.get("status") == THREE_AGENT_STATUS
    ):
        raise AssertionError("three-agent-bottom theorem changed")
    proof_totals = [
        checked_proof(three_agent, nested="sorting_cpc_ethos")
    ]

    double_bottom = {}
    double_bottom_sources = {}
    for path in double_bottom_paths:
        payload = load(path)
        pattern_index = payload.get("pattern_index")
        if pattern_index in double_bottom:
            raise AssertionError("duplicate double-bottom audit")
        if not (
            pattern_index in DOUBLE_BOTTOM_STATUSES
            and payload.get("status") == DOUBLE_BOTTOM_STATUSES[pattern_index]
            and payload.get("conversion_partition_count", 0) > 0
        ):
            raise AssertionError("double-bottom theorem changed")
        nested = "sorting_cpc_ethos" if pattern_index == 6 else None
        proof_totals.append(checked_proof(payload, nested=nested))
        double_bottom[pattern_index] = payload
        double_bottom_sources[pattern_index] = path
    if set(double_bottom) != set(DOUBLE_BOTTOM_STATUSES):
        raise AssertionError("both 2+2 patterns are required")

    repeated = load(repeated_path)
    if not (
        repeated.get("schema")
        == "all-repeated-bottom-pair-conversions-audit-v1"
        and repeated.get("status")
        == "ALL_2_PLUS_1_PLUS_1_BOTTOM_PATTERNS_PROOF_CHECKED"
        and tuple(repeated.get("canonical_pattern_indices", ()))
        == REPEATED_INDICES
        and repeated.get("all_ethos_correct") is True
        and repeated.get("total_checked_cpc_proof_bytes", 0) > 0
        and repeated.get("total_checked_cpc_proof_step_lines", 0) > 0
    ):
        raise AssertionError("2+1+1 class theorem changed")
    proof_totals.append(
        (
            repeated["total_checked_cpc_proof_bytes"],
            repeated["total_checked_cpc_proof_step_lines"],
        )
    )

    all_distinct = load(all_distinct_path)
    if not (
        all_distinct.get("schema")
        == "all-distinct-bottom-pair-conversions-audit-v1"
        and all_distinct.get("status")
        == "ALL_1_PLUS_1_PLUS_1_PLUS_1_PATTERNS_PROOF_CHECKED"
        and tuple(all_distinct.get("canonical_pattern_indices", ()))
        == DISTINCT_INDICES
        and all_distinct.get("all_ethos_correct") is True
        and all_distinct.get("total_checked_cpc_proof_bytes", 0) > 0
        and all_distinct.get("total_checked_cpc_proof_step_lines", 0) > 0
    ):
        raise AssertionError("1+1+1+1 class theorem changed")
    proof_totals.append(
        (
            all_distinct["total_checked_cpc_proof_bytes"],
            all_distinct["total_checked_cpc_proof_step_lines"],
        )
    )

    covered_indices = (
        set(double_bottom) | set(REPEATED_INDICES) | set(DISTINCT_INDICES)
    )
    if covered_indices != set(range(20)):
        raise AssertionError("multiplicity-at-most-two census is incomplete")

    source_paths = {
        "owner_threshold_shape_envelope": owner_threshold_path,
        "favorite_triple_hall_characterization": hall_characterization_path,
        "census": census_path,
        "three_agent_bottom": three_agent_path,
        "double_bottom_overlap": double_bottom_sources[0],
        "double_bottom_disjoint": double_bottom_sources[6],
        "all_2_plus_1_plus_1": repeated_path,
        "all_1_plus_1_plus_1_plus_1": all_distinct_path,
    }
    result = {
        "schema": SCHEMA,
        "status": "COMMON_FAVORITE_UNIVERSAL_THRESHOLD_EFX_PROOF_CHECKED",
        "agents": 4,
        "goods": 9,
        "strict_common_favorite": True,
        "universal_owner_threshold_failure": True,
        "bottom_pair_case_split": {
            "multiplicity_at_least_three": "three-agent-bottom theorem",
            "multiplicity_at_most_two_canonical_patterns": 20,
            "2+2_pattern_indices": sorted(double_bottom),
            "2+1+1_pattern_indices": list(REPEATED_INDICES),
            "1+1+1+1_pattern_indices": list(DISTINCT_INDICES),
            "covered_pattern_indices": sorted(covered_indices),
        },
        "total_checked_cpc_proof_bytes": sum(
            proof_bytes for proof_bytes, _ in proof_totals
        ),
        "total_checked_cpc_proof_step_lines": sum(
            proof_steps for _, proof_steps in proof_totals
        ),
        "all_component_proofs_ethos_correct": True,
        "sources": {
            name: {"path": str(path), "sha256": sha256(path)}
            for name, path in source_paths.items()
        },
        "claim_boundary": (
            "This proves complete EFX only for four positive-additive agents "
            "and nine goods with a strict common favorite when every possible "
            "favorite-singleton owner fails the residual owner-threshold test. "
            "It does not cover the threshold-passing/Hall-deficient branch, "
            "the full (4,9) cell, or general additive EFX."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner-threshold-audit", type=Path, required=True)
    parser.add_argument("--hall-characterization-audit", type=Path, required=True)
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--three-agent", type=Path, required=True)
    parser.add_argument("--double-bottom", action="append", type=Path, required=True)
    parser.add_argument("--repeated", type=Path, required=True)
    parser.add_argument("--all-distinct", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.owner_threshold_audit,
                args.hall_characterization_audit,
                args.census,
                args.three_agent,
                tuple(args.double_bottom),
                args.repeated,
                args.all_distinct,
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
