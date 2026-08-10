#!/usr/bin/env python3
"""QF_LRA checks for the packet-for-charity obstruction lemma."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum(left, right):
    return z3.If(left <= right, left, right)


def check(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    checked = solver.check()
    return {"claim": name, "status": str(checked)}


def run() -> dict:
    core, core_min, packet, packet_min, floater, own = z3.Reals(
        "core core_min packet packet_min floater own"
    )
    positive = [
        core >= core_min,
        core_min > 0,
        packet >= packet_min,
        packet_min > 0,
        floater > 0,
    ]
    old_tail = core + packet - minimum(core_min, packet_min)
    new_tail = core + floater - minimum(core_min, floater)
    records = [
        check(
            "target_threshold_increase_forces_floater_above_packet",
            positive + [new_tail > old_tail, floater <= packet],
        ),
        check(
            "empty_core_target_threshold_cannot_increase_under_packet_bound",
            [packet >= packet_min, packet_min > 0, floater > 0,
             z3.RealVal(0) > packet - packet_min],
        ),
        check(
            "charity_wall_forces_packet_above_floater",
            [own >= floater, own < packet, packet <= floater],
        ),
        check(
            "improving_owner_is_safe_against_released_packet",
            positive + [floater > packet, core + floater < packet],
        ),
    ]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "packet-charity-replacement-obstruction-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "unsat" for record in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit of the scalar implications in the arbitrary-packet analytic lemma; "
            "generalized-edge existence and EFX exhaustiveness are proved in the accompanying text"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
