#!/usr/bin/env python3
"""Freeze the dual verification of the common-bottom conversion theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        canonical_partition,
        conversion_partitions,
    )
    from .run_distinct_half_two_core_cegar import perfect_pairings
except ImportError:
    from anneal import atomic_json
    from decide_common_bottom_pairing_conversion import (
        FAVORITE,
        LOWS,
        canonical_partition,
        conversion_partitions,
    )
    from run_distinct_half_two_core_cegar import perfect_pairings


SCHEMA = "common-bottom-pairing-conversion-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def portable_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def load(path: Path):
    return json.loads(path.read_text())


def audit_z3(path: Path, expected_encoding, expected_witness):
    payload = load(path)
    formula = Path(payload["smt2_path"])
    if (
        payload.get("schema") != "common-bottom-pairing-conversion-lra-v1"
        or payload.get("status") != "UNSAT_CANDIDATE"
        or payload.get("solver_status") != "unsat"
        or payload.get("threshold_encoding") != expected_encoding
        or payload.get("hall_witness_type", "all") != expected_witness
        or payload.get("conversion_partition_count") != 6
        or payload.get("values") is not None
        or payload.get("smt2_sha256") != sha256(formula)
    ):
        raise AssertionError(f"Z3 theorem record changed: {path}")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "formula": portable_path(formula),
        "formula_sha256": sha256(formula),
        "threshold_encoding": expected_encoding,
        "hall_witness_type": expected_witness,
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cvc5(path: Path, normalization_path: Path, sorting_record):
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
        raise AssertionError("cvc5 theorem replay changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "normalization": str(normalization_path),
        "normalization_sha256": sha256(normalization_path),
        "formula": portable_path(formula),
        "formula_sha256": sha256(formula),
        "solver_sha256": payload["solver_sha256"],
        "elapsed_seconds": payload["elapsed_seconds"],
    }


def audit_cpc(path: Path, cvc5_record):
    payload = load(path)
    proof = Path(payload["proof"])
    if (
        payload.get("schema") != "cvc5-cpc-ethos-certificate-v1"
        or payload.get("verified") is not True
        or payload.get("formula_sha256") != cvc5_record["formula_sha256"]
        or payload.get("proof_sha256") != sha256(proof)
        or payload.get("proof_bytes") != proof.stat().st_size
        or payload.get("proof_step_lines") != 218320
        or payload.get("solve", {}).get("returncode") != 0
        or payload.get("solve", {}).get("timed_out") is not False
        or payload.get("check", {}).get("status") != "correct"
        or payload.get("check", {}).get("returncode") != 0
        or payload.get("check", {}).get("timed_out") is not False
        or payload.get("cvc5_sha256") != cvc5_record["solver_sha256"]
    ):
        raise AssertionError("CPC/Ethos theorem certificate changed")
    return {
        "result": str(path),
        "result_sha256": sha256(path),
        "proof": portable_path(proof),
        "proof_sha256": sha256(proof),
        "proof_bytes": proof.stat().st_size,
        "proof_step_lines": payload["proof_step_lines"],
        "ethos_sha256": payload["ethos_sha256"],
        "ethos_status": payload["check"]["status"],
    }


def audit_injection():
    residual = tuple(range(1, 7))
    matchings = tuple(perfect_pairings(residual))
    images = {}
    for matching in matchings:
        converted = tuple(
            canonical_partition(
                (FAVORITE, high),
                (*edge, low),
                *(pair for pair in matching if pair != edge),
            )
            for high, low in (LOWS, tuple(reversed(LOWS)))
            for edge in matching
        )
        if len(converted) != 6 or len(set(converted)) != 6:
            raise AssertionError("per-matching conversion census changed")
        for partition in converted:
            if partition in images:
                raise AssertionError("conversion no longer reconstructs its matching")
            images[partition] = matching
    if (
        len(matchings) != 15
        or len(images) != 90
        or set(conversion_partitions())
        != {
            partition
            for partition, matching in images.items()
            if matching == ((1, 2), (3, 4), (5, 6))
        }
    ):
        raise AssertionError("15-to-90 injection census changed")
    return {
        "perfect_matching_count": len(matchings),
        "conversions_per_matching": 6,
        "distinct_conversion_partition_count": len(images),
    }


def run(
    cardinal_path,
    sorting_path,
    cvc5_path,
    cpc_path,
    normalization_path,
    split_paths,
    output,
):
    cardinal = audit_z3(
        cardinal_path,
        "sorting-free cardinal degree characterization",
        "all",
    )
    sorting = audit_z3(sorting_path, "sorting", "all")
    expected_splits = (
        "zero_neighbor",
        "two_edges_one_neighbor",
        "three_edges_two_neighbors",
    )
    splits = [
        audit_z3(path, "sorting", expected)
        for path, expected in zip(split_paths, expected_splits)
    ]
    cvc5 = audit_cvc5(cvc5_path, normalization_path, sorting)
    result = {
        "schema": SCHEMA,
        "status": "COMMON_BOTTOM_PAIRING_CONVERSION_DUAL_VERIFIED",
        "cardinal_z3": cardinal,
        "sorting_z3": sorting,
        "sorting_cvc5": cvc5,
        "sorting_cpc_ethos": audit_cpc(cpc_path, cvc5),
        "canonical_hall_witness_cells": splits,
        "injection_census": audit_injection(),
        "claim_boundary": (
            "This certifies the common-bottom conversion and counting "
            "corollary. It does not prove that every no-favorite-pair "
            "profile has a common bottom pair."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cardinal", type=Path, required=True)
    parser.add_argument("--sorting", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--split", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if len(args.split) != 3:
        parser.error("exactly three canonical Hall-witness cells are required")
    result = run(
        args.cardinal,
        args.sorting,
        args.cvc5,
        args.cpc,
        args.normalization,
        tuple(args.split),
        args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
