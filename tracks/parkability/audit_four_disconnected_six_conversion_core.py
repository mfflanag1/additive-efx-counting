#!/usr/bin/env python3
"""Aggregate the checked six-conversion core for bottom pattern nineteen."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "four-disconnected-six-conversion-core-audit-v1"
EXPECTED_CORE = [
    [[0, 7], [1, 4], [2, 6, 8], [3, 5]],
    [[0, 7], [1, 4, 8], [2, 6], [3, 5]],
    [[0, 7], [1, 6], [2, 4, 8], [3, 5]],
    [[0, 8], [1, 4, 7], [2, 6], [3, 5]],
    [[0, 8], [1, 6], [2, 4, 7], [3, 5]],
    [[0, 8], [1, 6, 7], [2, 4], [3, 5]],
]


def load(path):
    return json.loads(path.read_text())


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    core_path,
    minimized_core_path,
    analysis_path,
    cvc5_path,
    normalization_path,
    cpc_path,
    proof_path,
    without_symmetry_path,
    minimality_path,
    output,
):
    core = load(core_path)
    minimized = load(minimized_core_path)
    analysis = load(analysis_path)
    cvc5 = load(cvc5_path)
    normalization = load(normalization_path)
    cpc = load(cpc_path)
    without_symmetry = load(without_symmetry_path)
    minimality = load(minimality_path)
    normalized_formula = normalization_path.parent / Path(
        normalization["output"]
    ).name

    for payload, minimized_flag in ((core, False), (minimized, True)):
        if not (
            payload.get("schema") == "bottom-pattern-conversion-core-lra-v1"
            and payload.get("status") == "CORE_UNSAT_CANDIDATE"
            and payload.get("solver_status") == "unsat"
            and payload.get("replay_solver_status") == "unsat"
            and payload.get("pattern_index") == 19
            and payload.get("pool_size") == 360
            and payload.get("core_size") == 6
            and payload.get("core_partitions") == EXPECTED_CORE
            and payload.get("core_minimization") is minimized_flag
            and payload.get("symmetry_breaking")
            == "four_disconnected_edges_canonical"
            and payload.get("universal_threshold_encoding") == "sorting"
        ):
            raise AssertionError("six-partition Z3 core changed")
    if core.get("formula_sha256") != minimized.get("formula_sha256"):
        raise AssertionError("ordinary and minimized cores differ")
    if not (
        analysis.get("schema")
        == "bottom-pattern-conversion-core-analysis-v1"
        and analysis.get("pattern_index") == 19
        and analysis.get("core_size") == 6
        and analysis.get("conversion_family_size") == 360
        and analysis.get("conversion_orbit_count") == 4
        and analysis.get("core_count_by_conversion_orbit") == {"3": 6}
        and analysis.get("core_count_by_favorite_partner")
        == {"7": 3, "8": 3}
    ):
        raise AssertionError("six-partition orbit analysis changed")
    if not (
        normalization.get("schema") == "strict-smt2-normalization-v1"
        and normalization.get("source_sha256") == core.get("formula_sha256")
        and normalization.get("output_sha256") == sha256(normalized_formula)
        and cvc5.get("confirmed_expected") is True
        and cvc5.get("verdict") == "unsat"
        and cvc5.get("formula_sha256") == normalization.get("output_sha256")
        and cpc.get("verified") is True
        and cpc.get("formula_sha256") == normalization.get("output_sha256")
        and cpc.get("proof_sha256") == sha256(proof_path)
        and cpc.get("proof_bytes") == proof_path.stat().st_size
        and cpc.get("check", {}).get("status") == "correct"
    ):
        raise AssertionError("compact cvc5/CPC certificate changed")
    if not (
        without_symmetry.get("schema")
        == "bottom-pattern-core-without-symmetry-boundary-v1"
        and without_symmetry.get("status") == "SAT_BOUNDARY"
        and without_symmetry.get("solver_status") == "sat"
        and without_symmetry.get("pattern_index") == 19
        and without_symmetry.get("core_size") == 6
        and without_symmetry.get("tested_symmetry_breaking") == "none"
        and without_symmetry.get("values") is not None
    ):
        raise AssertionError("no-symmetry boundary changed")
    checks = minimality.get("checks", [])
    if not (
        minimality.get("schema")
        == "bottom-pattern-conversion-core-minimality-audit-v1"
        and minimality.get("status") == "DELETION_MINIMAL_CORE_AUDITED"
        and minimality.get("pattern_index") == 19
        and minimality.get("core_size") == 6
        and minimality.get("deletion_minimal") is True
        and len(checks) == 6
        and {check.get("omitted_index") for check in checks} == set(range(6))
        and all(
            check.get("status") == "SAT"
            and check.get("omitted_partition_supports_efx") is True
            for check in checks
        )
    ):
        raise AssertionError("deletion-minimality audit changed")

    result = {
        "schema": SCHEMA,
        "status": "SIX_CONVERSION_CANONICAL_CORE_PROOF_CHECKED",
        "pattern_index": 19,
        "full_conversion_family_size": 360,
        "core_size": 6,
        "core_partitions": EXPECTED_CORE,
        "core_conversion_orbit": 3,
        "favorite_partner_counts": {"7": 3, "8": 3},
        "z3_assumption_core_unsat": True,
        "z3_minimized_core_unsat": True,
        "z3_unguarded_replay_unsat": True,
        "cvc5_unsat": True,
        "ethos_status": "correct",
        "deletion_minimal": True,
        "without_symmetry_sat": True,
        "compact_formula_sha256": normalization["output_sha256"],
        "proof_sha256": cpc["proof_sha256"],
        "proof_bytes": cpc["proof_bytes"],
        "proof_step_lines": cpc["proof_step_lines"],
        "sources": {
            "core": str(core_path),
            "minimized_core": str(minimized_core_path),
            "analysis": str(analysis_path),
            "cvc5": str(cvc5_path),
            "normalization": str(normalization_path),
            "cpc": str(cpc_path),
            "proof": str(proof_path),
            "without_symmetry": str(without_symmetry_path),
            "minimality": str(minimality_path),
        },
        "claim_boundary": (
            "This certifies a WLOG canonical six-conversion core for the "
            "four-disconnected-pairs pattern. It is not label-free and "
            "does not cover another bottom-pair pattern."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--minimized-core", type=Path, required=True)
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--without-symmetry", type=Path, required=True)
    parser.add_argument("--minimality", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.core,
                args.minimized_core,
                args.analysis,
                args.cvc5,
                args.normalization,
                args.cpc,
                args.proof,
                args.without_symmetry,
                args.minimality,
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
