#!/usr/bin/env python3
"""Freeze the proof package for the three-agent-bottom conversion theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from . import independent
    from .anneal import atomic_json
    from .audit_common_bottom_pairing_conversion import audit_injection
    from .decide_common_bottom_pairing_conversion import (
        LOWS,
        MATCHING,
        RESIDUAL,
        conversion_partitions,
    )
    from .run_distinct_half_full_cell_cegar import favorite_pair_universe
    from .run_generic_partition_cegar import supported_partitions
    from .run_universal_threshold_balanced_cegar import audit_threshold_failure
except ImportError:
    import independent
    from anneal import atomic_json
    from audit_common_bottom_pairing_conversion import audit_injection
    from decide_common_bottom_pairing_conversion import (
        LOWS,
        MATCHING,
        RESIDUAL,
        conversion_partitions,
    )
    from run_distinct_half_full_cell_cegar import favorite_pair_universe
    from run_generic_partition_cegar import supported_partitions
    from run_universal_threshold_balanced_cegar import audit_threshold_failure


SCHEMA = "three-agent-bottom-pairing-conversion-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def portable(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def audit_z3(path, encoding, witness, bottom_agents):
    payload = load(path)
    formula = Path(payload["smt2_path"])
    if (
        payload.get("schema") != "common-bottom-pairing-conversion-lra-v1"
        or payload.get("status") != "UNSAT_CANDIDATE"
        or payload.get("solver_status") != "unsat"
        or payload.get("threshold_encoding") != encoding
        or payload.get("hall_witness_type") != witness
        or payload.get("bottom_order_agents") != list(bottom_agents)
        or payload.get("bottom_order_constraint_count")
        != 12 * len(bottom_agents)
        or payload.get("conversion_partition_count") != 6
        or payload.get("conversion_scope") != "all"
        or payload.get("values") is not None
        or payload.get("smt2_sha256") != sha256(formula)
    ):
        raise AssertionError(f"three-agent Z3 record changed: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": portable(formula),
        "formula_sha256": sha256(formula),
        "threshold_encoding": encoding,
        "hall_witness_type": witness,
        "bottom_order_agents": list(bottom_agents),
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cvc5(path, normalization_path, sorting_record):
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
        or normalization.get("source_sha256")
        != sorting_record["formula_sha256"]
    ):
        raise AssertionError("three-agent cvc5 replay changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "normalization": str(normalization_path),
        "normalization_sha256": sha256(normalization_path),
        "formula": portable(formula),
        "formula_sha256": sha256(formula),
        "solver_sha256": payload["solver_sha256"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cpc(path, cvc5_record):
    payload = load(path)
    proof = Path(payload["proof"])
    if (
        payload.get("schema") != "cvc5-cpc-ethos-certificate-v1"
        or payload.get("verified") is not True
        or payload.get("formula_sha256") != cvc5_record["formula_sha256"]
        or payload.get("proof_sha256") != sha256(proof)
        or payload.get("proof_bytes") != proof.stat().st_size
        or payload.get("proof_step_lines", 0) <= 0
        or payload.get("solve", {}).get("returncode") != 0
        or payload.get("solve", {}).get("timed_out") is not False
        or payload.get("check", {}).get("status") != "correct"
        or payload.get("check", {}).get("returncode") != 0
        or payload.get("check", {}).get("timed_out") is not False
        or payload.get("cvc5_sha256") != cvc5_record["solver_sha256"]
    ):
        raise AssertionError("three-agent CPC/Ethos certificate changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "proof": portable(proof),
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_step_lines": payload["proof_step_lines"],
        "ethos_sha256": payload["ethos_sha256"],
        "ethos_status": payload["check"]["status"],
    }


def audit_order_core(path):
    payload = load(path)
    formula = Path(payload["formula_path"])
    counts = payload.get("order_counts_by_agent")
    if (
        payload.get("schema") != "common-bottom-conversion-order-core-v1"
        or payload.get("status")
        != "DELETION_MINIMAL_SUFFICIENT_ORDER_CORE"
        or payload.get("solver_status") != "unsat"
        or payload.get("hall_witness_type") != "zero_neighbor"
        or payload.get("initial_order_inequality_count") != 48
        or payload.get("minimized_order_inequality_count") != 36
        or counts != {"0": 0, "1": 12, "2": 12, "3": 12}
        or payload.get("formula_sha256") != sha256(formula)
        or any(
            record.get("solver_status") == "unknown"
            for record in payload.get("deletion_trace", [])
        )
    ):
        raise AssertionError("three-agent bottom-order core changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": portable(formula),
        "formula_sha256": sha256(formula),
        "retained_order_inequality_count": 36,
        "order_counts_by_agent": counts,
    }


def audit_two_agent_boundary(path):
    payload = load(path)
    formula = Path(payload["smt2_path"])
    values = tuple(tuple(row) for row in payload["values"])
    audit_threshold_failure(values)
    if (
        payload.get("status") != "CONVERSION_COUNTEREXAMPLE"
        or payload.get("solver_status") != "sat"
        or payload.get("bottom_order_agents") != [0, 1]
        or payload.get("bottom_order_constraint_count") != 24
        or payload.get("hall_witness_type") != "zero_neighbor"
        or payload.get("smt2_sha256") != sha256(formula)
        or any(row[0] <= max(row[1:]) for row in values)
        or any(
            values[agent][low] > values[agent][good]
            for agent in (0, 1)
            for low in LOWS
            for good in RESIDUAL
        )
        or any(
            sum(row[good] for good in MATCHING[0])
            >= row[0] + max(row[low] for low in LOWS)
            for row in values
        )
        or supported_partitions(values, list(conversion_partitions()))
    ):
        raise AssertionError("two-agent sharpness boundary changed")
    repairs = supported_partitions(
        values, list(favorite_pair_universe("all"))
    )
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": portable(formula),
        "formula_sha256": sha256(formula),
        "favorite_pair_efx_partition_count": len(repairs),
        "literal_complete_efx_count": independent.count_complete_efx0(values),
    }


def run(args):
    cardinal = audit_z3(args.cardinal, "cardinal", "all", (0, 1, 2))
    sorting = audit_z3(args.sorting, "sorting", "all", (0, 1, 2))
    expected_splits = (
        ("zero_neighbor", (0, 1, 2)),
        ("two_edges_one_neighbor", (0, 1, 2)),
        ("two_edges_one_neighbor", (1, 2, 3)),
        ("three_edges_two_neighbors", (0, 1, 2)),
        ("three_edges_two_neighbors", (1, 2, 3)),
    )
    if len(args.split) != len(expected_splits):
        raise ValueError("five canonical role cells are required")
    splits = [
        audit_z3(path, "cardinal", witness, agents)
        for path, (witness, agents) in zip(args.split, expected_splits)
    ]
    cvc5 = audit_cvc5(args.cvc5, args.normalization, sorting)
    result = {
        "schema": SCHEMA,
        "status": "THREE_AGENT_BOTTOM_CONVERSION_PROOF_CHECKED",
        "cardinal_z3": cardinal,
        "sorting_z3": sorting,
        "sorting_cvc5": cvc5,
        "sorting_cpc_ethos": audit_cpc(args.cpc, cvc5),
        "canonical_hall_role_cells": splits,
        "bottom_order_core": audit_order_core(args.order_core),
        "two_agent_sharpness_boundary": audit_two_agent_boundary(
            args.two_agent_boundary
        ),
        "injection_census": audit_injection(),
        "claim_boundary": (
            "This closes profiles with a pair ranked bottom-two by at least "
            "three agents. It does not close the remaining multiplicity-at-"
            "most-two branch or general additive EFX."
        ),
    }
    atomic_json(args.output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cardinal", type=Path, required=True)
    parser.add_argument("--sorting", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--split", type=Path, action="append", required=True)
    parser.add_argument("--order-core", type=Path, required=True)
    parser.add_argument("--two-agent-boundary", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
