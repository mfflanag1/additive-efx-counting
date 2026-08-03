#!/usr/bin/env python3
"""Audit provenance and fresh replay of an extracted minimum-slot UNSAT core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-unsat-core-replay-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(core_path, replay_path, output_path):
    core = json.loads(core_path.read_text())
    replay = json.loads(replay_path.read_text())
    derivation_path = Path(core["source"])
    derivation = json.loads(derivation_path.read_text())
    checks = {
        "core_pool_schema": (
            core.get("schema") == "minimum-slot-orbit-global-threshold-cegar-v1"
        ),
        "core_pool_status": core.get("status") == "EXTRACTED_UNSAT_CORE_POOL",
        "derivation_hash": core.get("source_sha256") == sha256(derivation_path),
        "derivation_unsat": (
            derivation.get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED"
        ),
        "derivation_tracked": derivation.get("track_unsat_core") is True,
        "core_size_accounting": (
            core.get("unsat_core_size")
            == core.get("global_cut_count")
            + core.get("completion_cut_count")
            + core.get("orbit_hall_cut_count")
        ),
        "replay_unsat": replay.get("status") == "FIXED_PAIR_TOKEN_ORBIT_FORCED",
        "replay_not_unknown": replay.get("solver_reason_unknown") is None,
        "single_replay_check": replay.get("iterations") == 1,
        "same_global_cuts": replay.get("global_cuts") == core.get("global_cuts"),
        "same_completion_cuts": (
            replay.get("completion_cuts") == core.get("completion_cuts")
        ),
        "same_orbit_hall_cuts": (
            replay.get("orbit_hall_cuts") == core.get("orbit_hall_cuts")
        ),
        "same_diagonal_pattern": (
            replay.get("base_host_diagonal_pattern")
            == derivation.get("base_host_diagonal_pattern")
        ),
        "same_offhost_source_hash": (
            replay.get("base_host_offhost_edge_cell_source_sha256")
            == derivation.get("base_host_offhost_edge_cell_source_sha256")
        ),
        "same_pair_hall_cycle": (
            replay.get("base_host_pair_hall_cycle")
            == derivation.get("base_host_pair_hall_cycle")
        ),
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "FRESH_CORE_REPLAY_CONFIRMED"
            if all(checks.values())
            else "CORE_REPLAY_MISMATCH"
        ),
        "meaning": (
            "The tracked UNSAT derivation, extracted raw core, and fresh one-check "
            "replay agree on provenance, edge-cell hypotheses, and every cut."
        ),
        "claim_boundary": (
            "This confirms the 76-cut fixed-edge-cell theorem, not the entire "
            "eight-switch subcell, pair-Hall cell, or four-agent EFX."
        ),
        "core": str(core_path),
        "core_sha256": sha256(core_path),
        "derivation": str(derivation_path),
        "derivation_sha256": sha256(derivation_path),
        "replay": str(replay_path),
        "replay_sha256": sha256(replay_path),
        "replay_elapsed_seconds": replay.get("elapsed_seconds"),
        "global_cut_count": core.get("global_cut_count"),
        "completion_cut_count": core.get("completion_cut_count"),
        "orbit_hall_cut_count": core.get("orbit_hall_cut_count"),
        "checks": checks,
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.core, args.replay, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
