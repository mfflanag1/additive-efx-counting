#!/usr/bin/env python3
"""Freeze the disjoint double-bottom-pair conversion proof package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_bottom_pattern_conversion_selector import (
        conversion_closure,
        reconstruct_cegar_pool,
    )
    from .run_bottom_pair_pattern_selector_cegar import goods_pattern
except ImportError:
    from anneal import atomic_json
    from decide_bottom_pattern_conversion_selector import (
        conversion_closure,
        reconstruct_cegar_pool,
    )
    from run_bottom_pair_pattern_selector_cegar import goods_pattern


SCHEMA = "disjoint-double-bottom-pair-conversion-audit-v1"
PATTERN_INDEX = 6


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def audit_z3(path, encoding, source_hash=None):
    payload = load(path)
    formula = Path(payload["smt2_path"])
    if (
        payload.get("schema") != "bottom-pattern-conversion-selector-lra-v1"
        or payload.get("status") != "UNSAT_CANDIDATE"
        or payload.get("solver_status") != "unsat"
        or payload.get("pattern_index") != PATTERN_INDEX
        or payload.get("pool_size") != 72
        or payload.get("distinct_conversion_partition_count") != 180
        or payload.get("values") is not None
        or payload.get("smt2_sha256") != sha256(formula)
    ):
        raise AssertionError(f"disjoint-pattern Z3 record changed: {path}")
    if encoding == "sorting":
        resume = payload.get("resume_source", {})
        if (
            payload.get("threshold_encoding") != "sorting"
            or resume.get("sha256") != source_hash
            or resume.get("reconstructed_pool_size") != 72
        ):
            raise AssertionError("sorting replay source changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": str(formula),
        "formula_sha256": sha256(formula),
        "threshold_encoding": encoding,
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cvc5(path, normalization_path, sorting):
    payload = load(path)
    normalization = load(normalization_path)
    formula = Path(payload["formula"])
    if (
        payload.get("schema") != "external-smt-replay-v1"
        or payload.get("solver_interface") != "cvc5"
        or payload.get("verdict") != "unsat"
        or payload.get("confirmed_expected") is not True
        or payload.get("formula_sha256") != sha256(formula)
        or normalization.get("output_sha256") != sha256(formula)
        or normalization.get("source_sha256") != sorting["formula_sha256"]
    ):
        raise AssertionError("disjoint-pattern cvc5 replay changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "normalization": str(normalization_path),
        "normalization_sha256": sha256(normalization_path),
        "formula": str(formula),
        "formula_sha256": sha256(formula),
        "solver_sha256": payload["solver_sha256"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cpc(path, cvc5):
    payload = load(path)
    proof = Path(payload["proof"])
    if (
        payload.get("schema") != "cvc5-cpc-ethos-certificate-v1"
        or payload.get("verified") is not True
        or payload.get("formula_sha256") != cvc5["formula_sha256"]
        or payload.get("proof_sha256") != sha256(proof)
        or payload.get("proof_bytes") != proof.stat().st_size
        or payload.get("proof_step_lines", 0) <= 0
        or payload.get("solve", {}).get("returncode") != 0
        or payload.get("check", {}).get("status") != "correct"
        or payload.get("check", {}).get("returncode") != 0
        or payload.get("cvc5_sha256") != cvc5["solver_sha256"]
    ):
        raise AssertionError("disjoint-pattern CPC/Ethos record changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "proof": str(proof),
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_step_lines": payload["proof_step_lines"],
        "ethos_sha256": payload["ethos_sha256"],
        "ethos_status": payload["check"]["status"],
    }


def audit_core(path, analysis_path):
    payload = load(path)
    analysis = load(analysis_path)
    formula = Path(payload["formula"])
    if (
        payload.get("schema") != "bottom-pattern-conversion-core-lra-v1"
        or payload.get("status") != "CORE_UNSAT_CANDIDATE"
        or payload.get("solver_status") != "unsat"
        or payload.get("replay_solver_status") != "unsat"
        or payload.get("pattern_index") != PATTERN_INDEX
        or payload.get("pool_size") != 72
        or payload.get("core_size") != 19
        or len(payload.get("core_partitions", [])) != 19
        or payload.get("formula_sha256") != sha256(formula)
        or analysis.get("schema")
        != "bottom-pattern-conversion-core-analysis-v1"
        or analysis.get("pattern_index") != PATTERN_INDEX
        or analysis.get("core_size") != 19
        or analysis.get("core_count_by_conversion_orbit")
        != {"0": 6, "1": 7, "2": 4, "3": 2}
        or analysis.get("favorite_partner_goods") != [1, 2]
    ):
        raise AssertionError("disjoint-pattern compact core changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": str(formula),
        "formula_sha256": sha256(formula),
        "pool_size": 72,
        "core_size": 19,
        "analysis": str(analysis_path),
        "analysis_sha256": sha256(analysis_path),
        "core_count_by_conversion_orbit": {"0": 6, "1": 7, "2": 4, "3": 2},
        "favorite_partner_goods": [1, 2],
    }


def run(args):
    pattern = goods_pattern(PATTERN_INDEX)
    selected_pairs = tuple(dict.fromkeys(pattern))
    family, source_pairing_count = conversion_closure(selected_pairs)
    cardinal_payload = load(args.cardinal)
    pool = reconstruct_cegar_pool(cardinal_payload, family)
    if (
        pattern != ((1, 2), (1, 2), (3, 4), (3, 4))
        or source_pairing_count != 30
        or len(family) != 180
        or len(pool) != 72
        or not pool <= set(family)
    ):
        raise AssertionError("disjoint conversion family changed")
    cardinal = audit_z3(args.cardinal, "cardinal")
    sorting = audit_z3(
        args.sorting, "sorting", source_hash=cardinal["result_sha256"]
    )
    cvc5 = audit_cvc5(args.cvc5, args.normalization, sorting)
    compact_z3 = audit_core(args.core, args.core_analysis)
    compact_cvc5 = audit_cvc5(
        args.core_cvc5, args.core_normalization, compact_z3
    )
    orbit = load(args.orbit_audit)
    if (
        orbit.get("schema") != "bottom-pattern-conversion-orbit-audit-v1"
        or orbit.get("pattern_index") != PATTERN_INDEX
        or orbit.get("automorphism_count") != 192
        or orbit.get("conversion_partition_count") != 180
        or orbit.get("conversion_orbit_count") != 4
        or [record["size"] for record in orbit["conversion_orbits"]]
        != [12, 96, 24, 48]
    ):
        raise AssertionError("disjoint conversion orbit audit changed")
    result = {
        "schema": SCHEMA,
        "status": "DISJOINT_DOUBLE_BOTTOM_CONVERSION_PROOF_CHECKED",
        "pattern_index": PATTERN_INDEX,
        "agent_bottom_pairs": [list(pair) for pair in pattern],
        "source_pairing_count": source_pairing_count,
        "conversion_partition_count": len(family),
        "sufficient_partition_count": len(pool),
        "conversion_orbit_audit": {
            "path": str(args.orbit_audit),
            "sha256": sha256(args.orbit_audit),
            "automorphism_count": 192,
            "orbit_sizes": [12, 96, 24, 48],
        },
        "cardinal_z3": cardinal,
        "sorting_z3": sorting,
        "sorting_cvc5": cvc5,
        "sorting_cpc_ethos": audit_cpc(args.cpc, cvc5),
        "compact_core": {
            "z3": compact_z3,
            "cvc5": compact_cvc5,
            "cpc_ethos": audit_cpc(args.core_cpc, compact_cvc5),
        },
        "claim_boundary": (
            "This proves the conditional disjoint double-bottom conversion "
            "lemma. It does not close the overlap or lower-multiplicity "
            "branches, 4x9 EFX, or general additive EFX."
        ),
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cardinal", type=Path, required=True)
    parser.add_argument("--sorting", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--core-analysis", type=Path, required=True)
    parser.add_argument("--core-cvc5", type=Path, required=True)
    parser.add_argument("--core-normalization", type=Path, required=True)
    parser.add_argument("--core-cpc", type=Path, required=True)
    parser.add_argument("--orbit-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
