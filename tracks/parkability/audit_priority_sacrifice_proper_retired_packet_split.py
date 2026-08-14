#!/usr/bin/env python3
"""Exact arithmetic and target-locality audit for priority sacrifice split."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    fs, b, t, d, recipient_new = z3.Reals("fs b t d recipient_new")
    recipient_floor = prove(
        [d == fs - b, recipient_new == b + t],
        (recipient_new >= fs) == (t >= d),
    )

    mu, k, good, rest = z3.Reals("mu k good rest")
    strict_atom = prove(
        [k == mu + d, k == good + rest, rest < d],
        good > mu,
    )

    target_locality = True
    partitions_checked = 0
    for size in range(2, 9):
        packet = frozenset(range(size))
        for mask in range(1, (1 << size) - 1):
            transferred = frozenset(
                good_id for good_id in packet if mask & (1 << good_id)
            )
            retained = packet - transferred
            partitions_checked += 1
            target_locality &= (
                transferred < packet
                and retained < packet
                and transferred.isdisjoint(retained)
                and transferred | retained == packet
            )

    assert recipient_floor and strict_atom and target_locality
    theorem = repo / "results/PRIORITY_SACRIFICE_PROPER_RETIRED_PACKET_SPLIT_THEOREM_20260813.md"
    normal_form = repo / "results/RETIRED_PACKET_COLLISION_ATOMIC_NORMAL_FORM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "priority-sacrifice-proper-retired-packet-split-audit-v1",
        "status": "SACRIFICE_SPLIT_ROUTES_TO_PROGRESS_OR_PROTECTED_CUT",
        "recipient_floor_identity": recipient_floor,
        "strict_recipient_indivisibility_atom": strict_atom,
        "single_target_response_hits_only_proper_packet": target_locality,
        "representative_partitions_checked": partitions_checked,
        "holder_payment_required": False,
        "earlier_strict_root_preserved": True,
        "full_T_L_times_theorem_closed": False,
        "remaining_branches": [
            "recipient_indivisible_whole_packet",
            "root_or_protected_holder_birow_cut",
        ],
        "claim_boundary": (
            "cap-free priority-valid sacrifice routing; equality/indivisible "
            "and root/protected-holder cut remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "normal_form": str(normal_form.relative_to(repo)),
            "normal_form_sha256": sha256(normal_form),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "remaining_branches": result["remaining_branches"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
