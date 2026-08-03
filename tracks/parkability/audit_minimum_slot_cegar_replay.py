#!/usr/bin/env python3
"""Record and validate a fresh replay of a minimum-slot CEGAR certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "minimum-slot-cegar-replay-audit-v1"
SUCCESS = "FIXED_PAIR_TOKEN_ORBIT_FORCED"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(certificate_path, replay_path, output_path):
    certificate = json.loads(certificate_path.read_text())
    replay = json.loads(replay_path.read_text())
    replay_mode = "one_check" if replay.get("iterations") == 1 else "staged"
    checks = {
        "certificate_unsat": certificate.get("status") == SUCCESS,
        "replay_unsat": replay.get("status") == SUCCESS,
        "replay_not_unknown": replay.get("solver_reason_unknown") is None,
        "same_global_cuts": replay.get("global_cuts") == certificate.get("global_cuts"),
        "same_orbit_hall_cuts": (
            replay.get("orbit_hall_cuts") == certificate.get("orbit_hall_cuts")
        ),
        "same_completion_cuts": (
            replay.get("completion_cuts") == certificate.get("completion_cuts")
        ),
        "same_edge_cell_source_hash": (
            replay.get("base_host_edge_cell_source_sha256")
            == certificate.get("base_host_edge_cell_source_sha256")
        ),
        "same_offhost_edge_cell_source_hash": (
            replay.get("base_host_offhost_edge_cell_source_sha256")
            == certificate.get("base_host_offhost_edge_cell_source_sha256")
        ),
        "same_pair_hall_cycle": (
            replay.get("base_host_pair_hall_cycle")
            == certificate.get("base_host_pair_hall_cycle")
        ),
        "same_diagonal_pattern": (
            replay.get("base_host_diagonal_pattern")
            == certificate.get("base_host_diagonal_pattern")
        ),
    }
    success = all(checks.values())
    result = {
        "schema": SCHEMA,
        "status": "FRESH_REPLAY_CONFIRMED" if success else "REPLAY_MISMATCH",
        "meaning": (
            (
                "A newly constructed solver containing the persisted cut pool and "
                "host-edge constraints returned UNSAT in one check."
            )
            if replay_mode == "one_check"
            else (
                "A fresh staged CEGAR reconstruction returned UNSAT and reproduced "
                "the certificate's complete ordered cut pools exactly."
            )
        ),
        "claim_boundary": (
            "The replay confirms the exact bounded formula and its persisted cut "
            "pool. It does not remove any recorded edge-cell assumptions or prove "
            "general four-agent EFX."
        ),
        "certificate": str(certificate_path),
        "certificate_sha256": sha256(certificate_path),
        "replay": str(replay_path),
        "replay_sha256": sha256(replay_path),
        "replay_elapsed_seconds": replay.get("elapsed_seconds"),
        "replay_mode": replay_mode,
        "replay_iteration_count": replay.get("iterations"),
        "global_cut_count": replay.get("global_cut_count"),
        "completion_cut_count": replay.get("completion_cut_count"),
        "orbit_hall_cut_count": replay.get("orbit_hall_cut_count"),
        "checks": checks,
    }
    atomic_json(output_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.certificate, args.replay, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
