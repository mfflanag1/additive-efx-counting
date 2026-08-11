#!/usr/bin/env python3
"""QF_LRA checks for the joint-packet maximal donation frontier."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked(name: str, constraints) -> dict:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    return {"claim": name, "status": str(solver.check())}


def run(root: Path) -> dict:
    root_base, packet, donation, good, root_new, root_floater = z3.Reals(
        "root_base packet donation good root_new root_floater"
    )
    old_threshold, new_threshold, owner_base = z3.Reals(
        "old_threshold new_threshold owner_base"
    )
    floater, external_donation = z3.Reals("floater external_donation")
    positive = [
        root_base > 0,
        packet > 0,
        donation >= 0,
        good > 0,
        root_floater > 0,
        owner_base > 0,
        floater > 0,
        external_donation >= 0,
    ]
    records = [
        checked(
            "empty_donation_is_root_charity_feasible",
            positive + [root_base >= root_floater, root_base + packet < root_floater],
        ),
        checked(
            "joint_packet_strictly_improves_root",
            positive
            + [packet > donation, root_new == root_base - donation + packet, root_new <= root_base],
        ),
        checked(
            "selected_root_dominates_enlarged_charity",
            positive
            + [
                root_new == root_base - donation + packet,
                root_new >= root_floater + donation,
                root_new < root_floater + donation,
            ],
        ),
        checked(
            "maximality_forces_gain_or_charity_criticality",
            positive
            + [
                z3.Not(
                    z3.And(
                        donation + good < packet,
                        root_base - donation - good + packet
                        >= root_floater + donation + good,
                    )
                ),
                donation + good <= packet,
                donation + good != packet,
                root_base - donation - good + packet
                >= root_floater + donation + good,
            ],
        ),
        checked(
            "external_root_wall_forces_threshold_increase",
            positive
            + [owner_base >= old_threshold, owner_base < new_threshold, new_threshold <= old_threshold],
        ),
        checked(
            "external_charity_wall_forces_donation_deficit",
            positive
            + [owner_base >= floater, owner_base < floater + external_donation, external_donation <= owner_base - floater],
        ),
    ]
    script = Path(__file__).resolve()
    theorem = root / "results/JOINT_PACKET_MAXIMAL_LEX_DONATION_FRONTIER_LEMMA_20260811.md"
    return {
        "schema": "joint-packet-maximal-lex-donation-frontier-audit-v1",
        "status": "ALL_FORCED" if all(r["status"] == "unsat" for r in records) else "OPEN",
        "records": records,
        "claim_boundary": (
            "QF_LRA audit of constrained-frontier feasibility, root gain, "
            "maximality criticality, and blocker polarities; connected-component "
            "termination is outside scope"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "records": result["records"]}, indent=2))


if __name__ == "__main__":
    main()
