#!/usr/bin/env python3
"""Aggregate the proof-checked overlap-orbit shared-active certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .decide_two_pair_bottom_cross_conversion import (
        FIRST_LOWS,
        cells,
        overlap_matching_orbits,
    )
    from .run_two_pair_bottom_cross_cegar import target_universe
except ImportError:
    from anneal import atomic_json
    from decide_two_pair_bottom_cross_conversion import (
        FIRST_LOWS,
        cells,
        overlap_matching_orbits,
    )
    from run_two_pair_bottom_cross_cegar import target_universe


SCHEMA = "overlap-orbit1-shared-active-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def run(cardinal, external_z3, cvc5, normalization, cpc, proof, output):
    card = load(cardinal)
    z3_replay = load(external_z3)
    cvc5_replay = load(cvc5)
    normalized = load(normalization)
    certificate = load(cpc)
    normalized_formula = normalization.parent / Path(normalized["output"]).name
    if not (
        card.get("schema") == "two-pair-bottom-cross-cegar-v1"
        and card.get("status") == "UNSAT_CANDIDATE"
        and card.get("solver_status") == "unsat"
        and card.get("pattern") == "overlap"
        and card.get("matching_orbit_index") == 1
        and card.get("partition_family") == "shared_low_active"
        and card.get("pool_size") == 107
    ):
        raise AssertionError("cardinality CEGAR endpoint changed")
    if not (
        z3_replay.get("confirmed_expected") is True
        and z3_replay.get("verdict") == "unsat"
        and z3_replay.get("formula_sha256") == card.get("smt2_sha256")
    ):
        raise AssertionError("fresh Z3 replay changed")
    if not (
        normalized.get("schema") == "strict-smt2-normalization-v1"
        and normalized.get("output_sha256") == sha256(normalized_formula)
        and cvc5_replay.get("confirmed_expected") is True
        and cvc5_replay.get("verdict") == "unsat"
        and cvc5_replay.get("formula_sha256") == normalized.get("output_sha256")
    ):
        raise AssertionError("sorting/cvc5 replay changed")
    if not (
        certificate.get("verified") is True
        and certificate.get("formula_sha256") == normalized.get("output_sha256")
        and certificate.get("proof_sha256") == sha256(proof)
        and certificate.get("proof_bytes") == proof.stat().st_size
        and certificate.get("check", {}).get("status") == "correct"
    ):
        raise AssertionError("CPC/Ethos certificate changed")

    orbits = overlap_matching_orbits()
    first_matching, second_lows, second_agents, second_matching, orbit_count = (
        cells("overlap", 1)
    )
    family = target_universe("overlap", second_lows, "shared_low_active")
    if len(orbits) != 4 or orbit_count != 4 or len(family) != 420:
        raise AssertionError("overlap orbit or partition-family census changed")
    result = {
        "schema": SCHEMA,
        "status": "OVERLAP_ORBIT1_SHARED_ACTIVE_PROOF_CHECKED",
        "pattern": "overlap",
        "matching_orbit_index": 1,
        "matching_orbit_count": len(orbits),
        "selected_cells": [
            {
                "low_pair": list(FIRST_LOWS),
                "matching": [list(edge) for edge in first_matching],
            },
            {
                "low_pair": list(second_lows),
                "matching": [list(edge) for edge in second_matching],
            },
        ],
        "second_bottom_agents": list(second_agents),
        "partition_family": "shared_low_active",
        "partition_family_size": len(family),
        "sufficient_pool_size": card["pool_size"],
        "cardinal_formula_sha256": card["smt2_sha256"],
        "sorting_formula_sha256": normalized["output_sha256"],
        "proof_sha256": certificate["proof_sha256"],
        "proof_bytes": certificate["proof_bytes"],
        "proof_step_lines": certificate["proof_step_lines"],
        "z3_fresh_process_unsat": True,
        "cvc5_independent_unsat": True,
        "ethos_status": "correct",
        "sources": {
            "cardinal": str(cardinal),
            "external_z3": str(external_z3),
            "cvc5": str(cvc5),
            "normalization": str(normalization),
            "cpc": str(cpc),
            "proof": str(proof),
        },
        "claim_boundary": (
            "This proves the fixed overlap relative-matching orbit 1 for "
            "the 420-state shared-low-active family. It does not close the "
            "other three matching orbits or the overlap bottom-pair pattern."
        ),
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cardinal", type=Path, required=True)
    parser.add_argument("--external-z3", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cpc", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.cardinal,
                args.external_z3,
                args.cvc5,
                args.normalization,
                args.cpc,
                args.proof,
                args.output,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
