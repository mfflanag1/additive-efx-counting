#!/usr/bin/env python3
"""Aggregate the proof-checked overlapping double-bottom conversion theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import conversion_closure
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import conversion_closure
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "overlap-double-bottom-conversion-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def run(
    cardinal,
    external_z3,
    sorting,
    cvc5,
    normalization,
    cpc,
    proof,
    symmetry_audit,
    orbit_audit,
    output,
):
    card = load(cardinal)
    z3_replay = load(external_z3)
    sort = load(sorting)
    cvc5_replay = load(cvc5)
    normalized = load(normalization)
    certificate = load(cpc)
    symmetry = load(symmetry_audit)
    orbits = load(orbit_audit)
    normalized_formula = normalization.parent / Path(normalized["output"]).name
    pattern = goods_pattern(0)
    family, source_pairing_count = conversion_closure(
        tuple(dict.fromkeys(pattern))
    )

    if not (
        card.get("schema") == "bottom-pattern-conversion-selector-lra-v1"
        and card.get("status") == "UNSAT_CANDIDATE"
        and card.get("solver_status") == "unsat"
        and card.get("pattern_index") == 0
        and card.get("distinct_conversion_partition_count") == 165
        and card.get("pool_size") == 165
        and card.get("threshold_encoding") == "cardinal"
        and card.get("symmetry_breaking") == "overlap_canonical"
        and card.get("symmetry_encoding", {}).get("group_size") == 960
    ):
        raise AssertionError("cardinality theorem endpoint changed")
    if not (
        z3_replay.get("confirmed_expected") is True
        and z3_replay.get("verdict") == "unsat"
        and z3_replay.get("formula_sha256") == card.get("smt2_sha256")
    ):
        raise AssertionError("fresh Z3 replay changed")
    if not (
        sort.get("status") == "UNSAT_CANDIDATE"
        and sort.get("solver_status") == "unsat"
        and sort.get("pattern_index") == 0
        and sort.get("pool_size") == 165
        and sort.get("threshold_encoding") == "sorting"
        and sort.get("symmetry_encoding") == card.get("symmetry_encoding")
    ):
        raise AssertionError("sorting-network theorem endpoint changed")
    if not (
        normalized.get("schema") == "strict-smt2-normalization-v1"
        and normalized.get("source_sha256") == sort.get("smt2_sha256")
        and normalized.get("output_sha256") == sha256(normalized_formula)
        and cvc5_replay.get("confirmed_expected") is True
        and cvc5_replay.get("verdict") == "unsat"
        and cvc5_replay.get("formula_sha256") == normalized.get("output_sha256")
    ):
        raise AssertionError("cvc5 sorting replay changed")
    if not (
        certificate.get("verified") is True
        and certificate.get("formula_sha256") == normalized.get("output_sha256")
        and certificate.get("proof_sha256") == sha256(proof)
        and certificate.get("proof_bytes") == proof.stat().st_size
        and certificate.get("check", {}).get("status") == "correct"
    ):
        raise AssertionError("CPC/Ethos certificate changed")
    if not (
        symmetry.get("status") == "OVERLAP_PATTERN_SYMMETRY_AUDITED"
        and symmetry.get("group_size") == 960
        and symmetry.get("conversion_partition_count") == len(family) == 165
        and symmetry.get("conversion_orbit_sizes") == [15, 60, 30, 60]
        and orbits.get("pattern_index") == 0
        and orbits.get("automorphism_count") == 240
        and [entry["size"] for entry in orbits["conversion_orbits"]]
        == [15, 60, 30, 60]
    ):
        raise AssertionError("symmetry or conversion-orbit audit changed")

    result = {
        "schema": SCHEMA,
        "status": "OVERLAP_DOUBLE_BOTTOM_CONVERSION_PROOF_CHECKED",
        "pattern_index": 0,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(family),
        "goods_automorphism_count": 240,
        "full_formula_symmetry_group_size": 960,
        "conversion_orbit_sizes": [15, 60, 30, 60],
        "z3_cardinal_unsat": True,
        "z3_fresh_process_unsat": True,
        "z3_sorting_unsat": True,
        "cvc5_sorting_unsat": True,
        "ethos_status": "correct",
        "cardinal_formula_sha256": card["smt2_sha256"],
        "sorting_formula_sha256": normalized["output_sha256"],
        "proof_sha256": certificate["proof_sha256"],
        "proof_bytes": certificate["proof_bytes"],
        "proof_step_lines": certificate["proof_step_lines"],
        "sources": {
            "cardinal": str(cardinal),
            "external_z3": str(external_z3),
            "sorting": str(sorting),
            "cvc5": str(cvc5),
            "normalization": str(normalization),
            "cpc": str(cpc),
            "proof": str(proof),
            "symmetry_audit": str(symmetry_audit),
            "orbit_audit": str(orbit_audit),
        },
        "claim_boundary": (
            "This closes the overlapping 2+2 selected-bottom-pair pattern "
            "inside the strict-common-favorite universal-threshold branch. "
            "Together with the disjoint theorem it closes both 2+2 "
            "patterns, but not the seven 2+1+1 patterns, the eleven "
            "all-distinct patterns, or general additive EFX."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cardinal", type=Path, required=True)
    parser.add_argument("--external-z3", type=Path, required=True)
    parser.add_argument("--sorting", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--symmetry-audit", type=Path, required=True)
    parser.add_argument("--orbit-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.cardinal,
                args.external_z3,
                args.sorting,
                args.cvc5,
                args.normalization,
                args.cpc,
                args.proof,
                args.symmetry_audit,
                args.orbit_audit,
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
