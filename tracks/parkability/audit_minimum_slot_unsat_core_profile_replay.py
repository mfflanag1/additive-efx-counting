#!/usr/bin/env python3
"""Audit three Z3 profiles, frozen-binary replay, and cvc5 status for a core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-unsat-core-profile-replay-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    core_path,
    default_path,
    qflra_path,
    arith2_path,
    smt2_path,
    external_path,
    normalized_path,
    normalization_path,
    cvc5_path,
    output_path,
):
    core = json.loads(core_path.read_text())
    replays = {
        "default": json.loads(default_path.read_text()),
        "qf_lra": json.loads(qflra_path.read_text()),
        "arith2": json.loads(arith2_path.read_text()),
    }
    external = json.loads(external_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    cut_checks = {
        f"{profile}_cuts_match_core": (
            replay.get("global_cuts") == core.get("global_cuts")
            and replay.get("completion_cuts") == core.get("completion_cuts")
            and replay.get("orbit_hall_cuts") == core.get("orbit_hall_cuts")
        )
        for profile, replay in replays.items()
    }
    checks = {
        "core_pool_status": core.get("status") == "EXTRACTED_UNSAT_CORE_POOL",
        "default_z3_unsat": (
            replays["default"].get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED"
            and replays["default"].get("solver_profile") == "default"
            and replays["default"].get("iterations") == 1
        ),
        "qflra_z3_unsat": (
            replays["qf_lra"].get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED"
            and replays["qf_lra"].get("solver_profile") == "qf_lra"
            and replays["qf_lra"].get("iterations") == 1
        ),
        "arith2_z3_unsat": (
            replays["arith2"].get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED"
            and replays["arith2"].get("solver_profile") == "arith2"
            and replays["arith2"].get("iterations") == 1
        ),
        **cut_checks,
        "external_z3_unsat": (
            external.get("verdict") == "unsat"
            and external.get("confirmed_expected") is True
            and external.get("returncode") == 0
            and external.get("timed_out") is False
        ),
        "external_formula_hash": external.get("formula_sha256") == sha256(smt2_path),
        "normalization_source_hash": (
            normalization.get("source_sha256") == sha256(smt2_path)
        ),
        "normalization_output_hash": (
            normalization.get("output_sha256") == sha256(normalized_path)
        ),
        "cvc5_source_hash": cvc5.get("source_sha256") == sha256(normalized_path),
        "cvc5_logic": cvc5.get("logic") == "QF_LRA",
        "cvc5_verdict_recorded": cvc5.get("status") in {
            "UNSAT",
            "UNKNOWN (TIMEOUT)",
        },
    }
    cvc5_unsat = cvc5.get("status") == "UNSAT"
    if not all(checks.values()):
        status = "PROFILE_REPLAY_MISMATCH"
    elif cvc5_unsat:
        status = "TRIPLE_Z3_AND_CVC5_CORE_REPLAY_CONFIRMED"
    else:
        status = "TRIPLE_Z3_CORE_REPLAY_CONFIRMED_CVC5_UNKNOWN"
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "The extracted core is UNSAT in fresh default, QF_LRA, and "
            "arithmetic-solver-2 Z3 profiles and in a frozen external Z3 "
            "binary replay. The independently parsed cvc5 verdict is recorded "
            "separately and is confirmation only when it is UNSAT."
        ),
        "claim_boundary": (
            "This validates the fixed pattern-2 edge-cell theorem and its "
            "cyclic relabelings, not the full switch cell or four-agent EFX."
        ),
        "core": str(core_path),
        "core_sha256": sha256(core_path),
        "smt2": str(smt2_path),
        "smt2_sha256": sha256(smt2_path),
        "normalized_smt2": str(normalized_path),
        "normalized_smt2_sha256": sha256(normalized_path),
        "checks": checks,
        "cvc5_independent_unsat": cvc5_unsat,
        "cvc5_status": cvc5.get("status"),
        "replays": {
            profile: {
                "path": str(path),
                "sha256": sha256(path),
                "elapsed_seconds": replays[profile].get("elapsed_seconds"),
            }
            for profile, path in (
                ("default", default_path),
                ("qf_lra", qflra_path),
                ("arith2", arith2_path),
            )
        },
        "external_replay": str(external_path),
        "external_replay_sha256": sha256(external_path),
        "normalization": str(normalization_path),
        "normalization_sha256": sha256(normalization_path),
        "cvc5_replay": str(cvc5_path),
        "cvc5_replay_sha256": sha256(cvc5_path),
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--default", type=Path, required=True)
    parser.add_argument("--qflra", type=Path, required=True)
    parser.add_argument("--arith2", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--external", type=Path, required=True)
    parser.add_argument("--normalized", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.core,
        args.default,
        args.qflra,
        args.arith2,
        args.smt2,
        args.external,
        args.normalized,
        args.normalization,
        args.cvc5,
        args.output,
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
