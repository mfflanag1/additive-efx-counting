#!/usr/bin/env python3
"""Independent integer-owner audit of a dynamic-anchor obstruction profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


WHOLE, SELECTED, COMPLEMENT = "whole", "selected", "complement"
SUPPLIER = {
    role: source for source, roles in SUPPORT_STATE.items() for role in roles
}


def q(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_profile(path):
    raw = json.loads(path.read_text())
    totals = {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw["terminal_profile_totals"].items()
    }
    minima = {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw["terminal_profile_minima"].items()
    }
    return raw, totals, minima


def slack(totals, minima, role):
    return min(totals[o][role] // minima[o][role] for o in OWNERS)


def scenarios(totals, minima, role, anchor, observer):
    total, minimum = totals[observer][role], minima[observer][role]
    result = []
    for x in ((minimum,) if observer == anchor else (minimum, total - minimum)):
        result.append((x, total - x))
    if slack(totals, minima, role) >= 3:
        for x in ((minimum,) if observer == anchor else (minimum, total - 2 * minimum)):
            result.append((x, minimum))
    return tuple(dict.fromkeys(result))


def independent_oracle(totals, minima, split_role=None, anchor=None,
                       edge_cap=4, timeout_seconds=60):
    pieces = tuple(
        piece for role in GOODS
        for piece in (
            ((role, SELECTED), (role, COMPLEMENT))
            if role == split_role else ((role, WHOLE),)
        )
    )
    owner = {
        piece: z3.Int(f"ind_owner_{piece[0]}_{piece[1]}") for piece in pieces
    }
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(owner[piece] >= 0, owner[piece] < len(OWNERS))
                 for piece in pieces))
    solver.add(*(z3.Or(*(owner[piece] == index for piece in pieces))
                 for index in range(len(OWNERS))))
    if split_role is not None:
        solver.add(
            owner[split_role, SELECTED] != owner[split_role, COMPLEMENT]
        )

    edge_flags = []
    for source in SUPPORT_STATE:
        source_pieces = [piece for piece in pieces if SUPPLIER[piece[0]] == source]
        for index, target in enumerate(OWNERS):
            if source == target:
                continue
            edge_flags.append(z3.Or(*(
                owner[piece] == index for piece in source_pieces
            )))
    solver.add(z3.PbLe([(flag, 1) for flag in edge_flags], edge_cap))

    for observer_index, observer in enumerate(OWNERS):
        row_scenarios = (
            ((None, None),) if split_role is None
            else scenarios(totals, minima, split_role, anchor, observer)
        )
        for selected_value, complement_floor in row_scenarios:
            def value(piece):
                role, kind = piece
                if kind == WHOLE:
                    return totals[observer][role]
                if kind == SELECTED:
                    return selected_value
                return totals[observer][role] - selected_value

            def floor(piece):
                role, kind = piece
                if kind == WHOLE:
                    return minima[observer][role]
                if kind == SELECTED:
                    return selected_value
                return complement_floor

            utility = {
                index: z3.Sum(*(
                    z3.If(owner[piece] == index, q(value(piece)), z3.RealVal(0))
                    for piece in pieces
                ))
                for index in range(len(OWNERS))
            }
            for target_index in range(len(OWNERS)):
                if target_index == observer_index:
                    continue
                for piece in pieces:
                    solver.add(z3.Implies(
                        owner[piece] == target_index,
                        utility[observer_index] >= utility[target_index] - q(floor(piece)),
                    ))
    status = solver.check()
    return str(status), solver.reason_unknown() if status == z3.unknown else None


def replay_master(totals, minima):
    solver, total, minimum = build_physical_master(2)
    for observer in OWNERS:
        for role in GOODS:
            solver.add(total[role, observer] == q(totals[observer][role]))
            solver.add(minimum[role, observer] == q(minima[observer][role]))
    return str(solver.check())


def audit_physical_decision(path, source_path):
    raw = json.loads(path.read_text())
    assert raw["source_profile_sha256"] == hashlib.sha256(
        source_path.read_bytes()
    ).hexdigest()
    assert raw["status"] == "SAT_COMPLETE_EFX_SPLIT_REPAIR"
    assert raw["attempts"][:2] == [
        {"split_cap": 0, "status": "unsat"},
        {"split_cap": 1, "status": "sat"},
    ]
    assert len(raw["terminal"]["split_roles"]) == 1
    return {
        "status": raw["status"],
        "attempts": raw["attempts"],
        "split_roles": raw["terminal"]["split_roles"],
        "used_edges": raw["terminal"]["used_edges"],
    }


def run(profile_path, physical_decision_path, output_path, timeout_seconds):
    raw, totals, minima = load_profile(profile_path)
    assert raw["status"] == "SAT_DYNAMIC_ANCHOR_OBSTRUCTION"
    assert raw["oracle_status"] == "unsat"
    master_status = replay_master(totals, minima)
    assert master_status == "sat"
    whole_status, whole_reason = independent_oracle(
        totals, minima, timeout_seconds=timeout_seconds
    )
    assert whole_status == "unsat", whole_reason
    lanes = []
    for role in GOODS:
        if slack(totals, minima, role) < 2:
            continue
        for anchor in OWNERS:
            status, reason = independent_oracle(
                totals, minima, role, anchor,
                timeout_seconds=timeout_seconds,
            )
            assert status == "unsat", (role, anchor, status, reason)
            lanes.append({
                "split_role": role,
                "anchor_observer": anchor,
                "status": status,
            })
    physical = audit_physical_decision(physical_decision_path, profile_path)
    result = {
        "schema": "fixed-u-dynamic-anchor-obstruction-independent-audit-v1",
        "status": "AUDIT_PASS_DYNAMIC_ANCHOR_REFUTED_EFX_NOT_REFUTED",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "physical_decision": str(physical_decision_path),
        "physical_decision_sha256": hashlib.sha256(
            physical_decision_path.read_bytes()
        ).hexdigest(),
        "master_replay_status": master_status,
        "independent_whole_role_status": whole_status,
        "independent_anchor_lane_count": len(lanes),
        "independent_anchor_lanes": lanes,
        "canonical_physical_repair": physical,
        "method": (
            "independent integer-owner placement encoding with edge flags derived "
            "from owner equalities; does not import the primary Boolean oracle"
        ),
        "claim_boundary": (
            "This refutes the dynamic-anchor theorem for the declared form-2 "
            "master. The canonical physical realization has a one-split four-edge "
            "EFX repair, so it is not an EFX countermodel."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--physical-decision", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    result = run(
        args.profile, args.physical_decision, args.output, args.timeout_seconds
    )
    print(json.dumps({
        "status": result["status"],
        "master_replay_status": result["master_replay_status"],
        "whole_role_status": result["independent_whole_role_status"],
        "anchor_lane_count": result["independent_anchor_lane_count"],
        "canonical_physical_repair": result["canonical_physical_repair"],
    }, indent=2))


if __name__ == "__main__":
    main()
