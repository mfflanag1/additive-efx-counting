#!/usr/bin/env python3
"""Recover the immutable terminal profile from its frozen physical repair.

The campaign summary was intentionally resumable and was overwritten by a
later continuation before the terminal profile had been committed separately.
The repair artifact contains every physical value, so totals and minima are
recovered losslessly and replayed against the complete form-2 master.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def recover(repair_path, prior_audit_path, output_path):
    repair = json.loads(repair_path.read_text())
    prior_audit = json.loads(prior_audit_path.read_text())
    physical = {
        observer: {good: Fraction(amount) for good, amount in row.items()}
        for observer, row in repair["terminal"]["physical_values"].items()
    }
    totals, minima = {}, {}
    for observer in OWNERS:
        totals[observer], minima[observer] = {}, {}
        for role in GOODS:
            goods = [g for g in physical[observer] if g.split(":")[0] == role]
            assert goods
            totals[observer][role] = sum(
                (physical[observer][g] for g in goods), Fraction()
            )
            minima[observer][role] = min(physical[observer][g] for g in goods)

    solver, total, minimum = build_physical_master(2)
    solver.add(*(
        total[role, observer] == z3.RealVal(str(totals[observer][role]))
        for observer in OWNERS for role in GOODS
    ))
    solver.add(*(
        minimum[role, observer] == z3.RealVal(str(minima[observer][role]))
        for observer in OWNERS for role in GOODS
    ))
    master_status = str(solver.check())
    assert master_status == "sat"

    slacks = {
        role: min(totals[o][role] // minima[o][role] for o in OWNERS)
        for role in GOODS
    }
    assert {role: str(v) for role, v in slacks.items()} == prior_audit["role_slacks"]
    result = {
        "schema": "fixed-u-wild-forced-terminal-profile-v1",
        "status": "SAT_NO_TAME_COVERING_MENU_FOR_THIS_PROFILE",
        "halt_reason": "wide_family_failed",
        "halt_detail": {"wide_status": "UNSAT_NO_TAME_SPLIT_ALLOCATION"},
        "form_index": 2,
        "edge_cap": 4,
        "profile_totals": {
            o: {g: str(totals[o][g]) for g in GOODS} for o in OWNERS
        },
        "profile_minima": {
            o: {g: str(minima[o][g]) for g in GOODS} for o in OWNERS
        },
        "profile_role_slacks": {role: str(value) for role, value in slacks.items()},
        "profile_wild_roles": prior_audit["wild_roles"],
        "profile_tame_roles": prior_audit["tame_roles"],
        "declared_form2_master_replay_status": master_status,
        "recovered_from_repair": str(repair_path),
        "recovered_from_repair_sha256": hashlib.sha256(repair_path.read_bytes()).hexdigest(),
        "prior_mutable_summary_sha256": repair["source_profile_sha256"],
        "prior_audit_role_ledger": {
            "wild_roles": prior_audit["wild_roles"],
            "tame_roles": prior_audit["tame_roles"],
            "role_slacks": prior_audit["role_slacks"],
        },
        "recovery_note": (
            "The mutable campaign summary was resumed after the terminal verdict. "
            "This immutable profile is recovered losslessly by summing and minimizing "
            "the complete rational physical columns frozen in the repair artifact."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--prior-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = recover(args.repair, args.prior_audit, args.output)
    print(json.dumps({
        "status": result["status"],
        "master_replay": result["declared_form2_master_replay_status"],
        "wild_roles": result["profile_wild_roles"],
    }, indent=2))


if __name__ == "__main__":
    main()
