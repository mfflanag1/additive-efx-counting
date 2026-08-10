#!/usr/bin/env python3
"""QF_LRA checks for the charity-rooted hub-split obstruction lemma."""

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


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    result = solver.check()
    return {"claim": name, "status": str(result)}


def run() -> dict:
    core, core_min, packet, packet_min = z3.Reals(
        "leaf_core leaf_core_min leaf_packet leaf_packet_min"
    )
    old_tail = core - core_min
    new_tail = core + packet - minimum(core_min, packet_min)
    charge = packet + core_min - minimum(core_min, packet_min)
    own, gain, slack = z3.Reals("leaf_own leaf_gain leaf_slack")

    hub_core, hub_core_min, hub_packet, hub_packet_min, floater = z3.Reals(
        "hub_core hub_core_min hub_packet hub_packet_min hub_floater"
    )
    hub_old_tail = hub_core + hub_packet - minimum(hub_core_min, hub_packet_min)
    hub_new_tail = hub_core + floater - minimum(hub_core_min, floater)
    hub_own, hub_gain = z3.Reals("hub_observer_own hub_observer_gain")

    records = [
        checked(
            "leaf_insertion_charge_is_exact",
            [core >= core_min, core_min > 0, packet >= packet_min, packet_min > 0,
             new_tail - old_tail != charge],
        ),
        checked(
            "leaf_wall_forces_charge_over_gain_plus_slack",
            [core >= core_min, core_min > 0, packet >= packet_min, packet_min > 0,
             slack == own - old_tail, own + gain < new_tail,
             charge <= gain + slack],
        ),
        checked(
            "hub_target_wall_forces_floater_above_released_packet",
            [hub_core >= hub_core_min, hub_core_min > 0,
             hub_packet >= hub_packet_min, hub_packet_min > 0, floater > 0,
             hub_own >= hub_old_tail, hub_gain >= 0,
             hub_own + hub_gain < hub_new_tail, floater <= hub_packet],
        ),
        checked(
            "empty_hub_residual_has_no_target_wall",
            [hub_packet >= hub_packet_min, hub_packet_min > 0, floater > 0,
             hub_own >= 0, hub_gain >= 0, hub_own + hub_gain < 0],
        ),
    ]
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "charity-rooted-hub-split-obstruction-audit-v1",
        "status": "ALL_FORCED" if all(record["status"] == "unsat" for record in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "aggregate QF_LRA audit of the exact leaf insertion charge, overload implication, hub "
            "target polarity, and empty-residual case; the arbitrary-packet EFX exhaustion and "
            "generalized edges are analytic"
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
