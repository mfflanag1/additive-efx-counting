#!/usr/bin/env python3
"""Aggregate a proof-checked all-distinct bottom-pair conversion theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import conversion_closure
    from .run_bottom_pair_pattern_selector_cegar import (
        goods_pattern,
        multiplicity_signature,
    )
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import conversion_closure
    from run_bottom_pair_pattern_selector_cegar import (
        goods_pattern,
        multiplicity_signature,
    )


SCHEMA = "all-distinct-bottom-pair-conversion-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def run(
    pattern_index,
    symmetry_breaking,
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
    pattern = goods_pattern(pattern_index)
    if multiplicity_signature(pattern) != (1, 1, 1, 1):
        raise ValueError("pattern must have four distinct selected pairs")
    family, source_pairing_count = conversion_closure(pattern)

    card = load(cardinal)
    z3_replay = load(external_z3)
    sort = load(sorting)
    cvc5_replay = load(cvc5)
    normalized = load(normalization)
    certificate = load(cpc)
    symmetry = load(symmetry_audit)
    orbits = load(orbit_audit)
    normalized_formula = normalization.parent / Path(normalized["output"]).name

    if not (
        card.get("schema") == "bottom-pattern-conversion-selector-lra-v1"
        and card.get("status") == "UNSAT_CANDIDATE"
        and card.get("solver_status") == "unsat"
        and card.get("pattern_index") == pattern_index
        and card.get("distinct_conversion_partition_count") == len(family)
        and card.get("pool_size") == len(family)
        and card.get("source_pairing_count") == source_pairing_count
        and card.get("threshold_encoding") == "cardinal"
        and card.get("symmetry_breaking") == symmetry_breaking
    ):
        raise AssertionError("cardinality theorem endpoint changed")
    if not (
        z3_replay.get("confirmed_expected") is True
        and z3_replay.get("verdict") == "unsat"
        and z3_replay.get("formula_sha256")
        in {card.get("smt2_sha256"), sort.get("smt2_sha256")}
    ):
        raise AssertionError("fresh Z3 replay changed")
    if not (
        sort.get("status") == "UNSAT_CANDIDATE"
        and sort.get("solver_status") == "unsat"
        and sort.get("pattern_index") == pattern_index
        and sort.get("pool_size") == len(family)
        and sort.get("threshold_encoding") == "sorting"
        and sort.get("symmetry_breaking") == symmetry_breaking
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

    orbit_sizes = [entry["size"] for entry in orbits["conversion_orbits"]]
    if not (
        symmetry.get("pattern_index") == pattern_index
        and symmetry.get("agent_bottom_pairs")
        == [list(pair) for pair in pattern]
        and symmetry.get("conversion_partition_count") == len(family)
        and symmetry.get("source_pairing_count") == source_pairing_count
        and symmetry.get("conversion_orbit_sizes") == orbit_sizes
        and symmetry.get("group_size")
        == card.get("symmetry_encoding", {}).get("group_size")
        and symmetry.get("action_invariance_checked") is True
        and symmetry.get("random_canonical_representatives_checked", 0) >= 128
        and orbits.get("schema")
        == "bottom-pattern-conversion-orbit-audit-v1"
        and orbits.get("pattern_index") == pattern_index
        and orbits.get("agent_bottom_pairs")
        == [list(pair) for pair in pattern]
        and orbits.get("source_pairing_count") == source_pairing_count
        and orbits.get("conversion_partition_count") == len(family)
        and sum(orbit_sizes) == len(family)
        and orbits.get("automorphism_count")
        == symmetry.get("goods_automorphism_count")
    ):
        raise AssertionError("symmetry or conversion-orbit audit changed")

    result = {
        "schema": SCHEMA,
        "status": "ALL_DISTINCT_BOTTOM_CONVERSION_PROOF_CHECKED",
        "pattern_index": pattern_index,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(family),
        "goods_automorphism_count": symmetry["goods_automorphism_count"],
        "full_formula_symmetry_group_size": symmetry["group_size"],
        "conversion_orbit_sizes": orbit_sizes,
        "z3_cardinal_unsat": True,
        "z3_fresh_process_unsat": True,
        "fresh_z3_formula_encoding": (
            "cardinal"
            if z3_replay["formula_sha256"] == card["smt2_sha256"]
            else "sorting"
        ),
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
            "This closes one pairwise-distinct selected-bottom-pair pattern "
            "inside the strict-common-favorite universal-threshold branch. "
            "It does not close any other bottom pattern or general additive EFX."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern-index", type=int, required=True)
    parser.add_argument(
        "--symmetry-breaking",
        required=True,
        choices=(
            "all_distinct_canonical",
            "four_cycle_canonical",
            "four_disconnected_edges_canonical",
        ),
    )
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
                args.pattern_index,
                args.symmetry_breaking,
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
