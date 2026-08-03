#!/usr/bin/env python3
"""Audit dual-Z3 and independent-cvc5 replay of a minimum-slot core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-unsat-core-dual-replay-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    core_path,
    replay_path,
    qflra_path,
    smt2_path,
    normalized_path,
    normalization_path,
    cvc5_path,
    output_path,
):
    core = json.loads(core_path.read_text())
    replay = json.loads(replay_path.read_text())
    qflra = json.loads(qflra_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    checks = {
        "core_pool_status": core.get("status") == "EXTRACTED_UNSAT_CORE_POOL",
        "default_z3_unsat": replay.get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED",
        "default_z3_one_check": replay.get("iterations") == 1,
        "qflra_z3_unsat": qflra.get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED",
        "qflra_z3_one_check": qflra.get("iterations") == 1,
        "qflra_profile": qflra.get("solver_profile") == "qf_lra",
        "z3_global_cuts_match_core": (
            replay.get("global_cuts") == qflra.get("global_cuts") == core.get("global_cuts")
        ),
        "z3_completion_cuts_match_core": (
            replay.get("completion_cuts")
            == qflra.get("completion_cuts")
            == core.get("completion_cuts")
        ),
        "z3_orbit_cuts_match_core": (
            replay.get("orbit_hall_cuts")
            == qflra.get("orbit_hall_cuts")
            == core.get("orbit_hall_cuts")
        ),
        "normalization_source_hash": (
            normalization.get("source_sha256") == sha256(smt2_path)
        ),
        "normalization_output_hash": (
            normalization.get("output_sha256") == sha256(normalized_path)
        ),
        "normalization_qf_lra": (
            normalization.get("transformation", {}).get("inserted_logic") == "QF_LRA"
        ),
        "cvc5_unsat": cvc5.get("status") == "UNSAT",
        "cvc5_source_hash": cvc5.get("source_sha256") == sha256(normalized_path),
        "cvc5_logic": cvc5.get("logic") == "QF_LRA",
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "DUAL_SOLVER_CORE_REPLAY_CONFIRMED"
            if all(checks.values())
            else "DUAL_SOLVER_REPLAY_MISMATCH"
        ),
        "meaning": (
            f"The {core.get('unsat_core_size')}-cut core is UNSAT in fresh "
            "one-check default and QF_LRA Z3 replays and in an independently "
            "parsed cvc5 QF_LRA replay."
        ),
        "claim_boundary": (
            "The audit validates one cyclic orbit of exact diagonal edge cells, "
            "not the full eight-switch subcell, pair-Hall cell, or four-agent EFX."
        ),
        "core": str(core_path),
        "core_sha256": sha256(core_path),
        "default_z3_replay": str(replay_path),
        "default_z3_replay_sha256": sha256(replay_path),
        "default_z3_elapsed_seconds": replay.get("elapsed_seconds"),
        "qflra_z3_replay": str(qflra_path),
        "qflra_z3_replay_sha256": sha256(qflra_path),
        "qflra_z3_elapsed_seconds": qflra.get("elapsed_seconds"),
        "smt2": str(smt2_path),
        "smt2_sha256": sha256(smt2_path),
        "normalized_smt2": str(normalized_path),
        "normalized_smt2_sha256": sha256(normalized_path),
        "normalization": str(normalization_path),
        "normalization_sha256": sha256(normalization_path),
        "cvc5_replay": str(cvc5_path),
        "cvc5_replay_sha256": sha256(cvc5_path),
        "cvc5_elapsed_seconds": cvc5.get("elapsed_seconds"),
        "checks": checks,
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--qflra", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--normalized", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.core,
        args.replay,
        args.qflra,
        args.smt2,
        args.normalized,
        args.normalization,
        args.cvc5,
        args.output,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
