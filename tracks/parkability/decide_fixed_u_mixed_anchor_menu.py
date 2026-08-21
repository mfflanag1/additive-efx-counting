#!/usr/bin/env python3
"""Construct a tame-side-pattern menu with anchor repairs on failing sides."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .fixed_u_dynamic_anchor import anchor_scenarios, role_slack, rv, supplier_map
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE
from .run_fixed_u_multi_split_chart_theorem import (
    HIGH,
    LOW,
    WHOLE,
    exact_audit,
    numeric_floor,
    numeric_oracle,
    numeric_value,
    pattern_key,
    role_patterns,
)


SELECTED, COMPLEMENT = "selected", "complement"


def rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def mixed_pieces(tame_role, anchor_role):
    return tuple(
        piece for role in GOODS
        for piece in (
            ((role, LOW), (role, HIGH)) if role == tame_role
            else ((role, SELECTED), (role, COMPLEMENT)) if role == anchor_role
            else ((role, WHOLE),)
        )
    )


def mixed_value(totals, minima, observer, piece, vector, anchor_role,
                selected_value):
    role, kind = piece
    if role in vector:
        return numeric_value(totals, minima, observer, piece, vector)
    if role == anchor_role:
        return selected_value if kind == SELECTED else totals[observer][role] - selected_value
    return totals[observer][role]


def mixed_floor(totals, minima, observer, piece, vector, anchor_role,
                selected_value, complement_floor):
    role, kind = piece
    if role in vector:
        return numeric_floor(totals, minima, observer, piece, vector)
    if role == anchor_role:
        return selected_value if kind == SELECTED else complement_floor
    return minima[observer][role]


def audit_mixed(allocation, totals, minima, tame_role, vector, anchor_role,
                anchor, edge_cap):
    expected = sorted(mixed_pieces(tame_role, anchor_role))
    placed = [tuple(piece) for bundle in allocation.values() for piece in bundle]
    assert sorted(placed) == expected and len(placed) == len(set(placed))
    assert all(allocation[owner] for owner in OWNERS)
    holders = {
        kind: owner for owner, bundle in allocation.items()
        for role, kind in map(tuple, bundle) if role == anchor_role
    }
    assert holders[SELECTED] != holders[COMPLEMENT]
    supplier = supplier_map()
    edges = sorted({
        (supplier[role], owner)
        for owner, bundle in allocation.items() for role, _ in map(tuple, bundle)
        if supplier[role] != owner
    })
    assert len(edges) <= edge_cap
    minimum_slack = None
    for observer in OWNERS:
        for _, selected_value, complement_floor in anchor_scenarios(
            totals, minima, anchor_role, anchor, observer
        ):
            utility = {
                owner: sum((
                    mixed_value(
                        totals, minima, observer, tuple(piece), vector,
                        anchor_role, selected_value,
                    ) for piece in allocation[owner]
                ), Fraction())
                for owner in OWNERS
            }
            for target in OWNERS:
                if target == observer:
                    continue
                for piece in allocation[target]:
                    slack = utility[observer] - utility[target] + mixed_floor(
                        totals, minima, observer, tuple(piece), vector,
                        anchor_role, selected_value, complement_floor,
                    )
                    assert slack >= 0
                    minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    return [list(edge) for edge in edges], minimum_slack


def mixed_oracle(totals, minima, tame_role, vector, anchor_role, anchor,
                 edge_cap, timeout_seconds):
    all_pieces = mixed_pieces(tame_role, anchor_role)
    supplier = supplier_map()
    place = {(piece, owner): z3.Bool(
        f"mixed_{tame_role}_{anchor_role}_{anchor}_{piece[0]}_{piece[1]}_{owner}"
    ) for piece in all_pieces for owner in OWNERS}
    edge = {(source, target): z3.Bool(f"mixed_edge_{source}_{target}")
            for source in SUPPORT_STATE for target in OWNERS if source != target}
    solver = z3.Solver(); solver.set(timeout=timeout_seconds * 1000)
    for piece in all_pieces:
        solver.add(z3.PbEq([(place[piece, owner], 1) for owner in OWNERS], 1))
        source = supplier[piece[0]]
        for owner in OWNERS:
            if owner != source:
                solver.add(z3.Implies(place[piece, owner], edge[source, owner]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))
    solver.add(*(z3.Or(*(place[piece, owner] for piece in all_pieces)) for owner in OWNERS))
    solver.add(*(z3.Not(z3.And(
        place[(anchor_role, SELECTED), owner],
        place[(anchor_role, COMPLEMENT), owner],
    )) for owner in OWNERS))
    for observer in OWNERS:
        for _, selected_value, complement_floor in anchor_scenarios(
            totals, minima, anchor_role, anchor, observer
        ):
            utility = {owner: z3.Sum(*(
                z3.If(place[piece, owner], rv(mixed_value(
                    totals, minima, observer, piece, vector,
                    anchor_role, selected_value,
                )), z3.RealVal(0)) for piece in all_pieces
            )) for owner in OWNERS}
            for target in OWNERS:
                if target == observer:
                    continue
                for piece in all_pieces:
                    solver.add(z3.Implies(
                        place[piece, target], utility[observer] >= utility[target]
                        - rv(mixed_floor(
                            totals, minima, observer, piece, vector,
                            anchor_role, selected_value, complement_floor,
                        )),
                    ))
    status = solver.check()
    if status != z3.sat:
        return str(status), None
    model = solver.model()
    allocation = {owner: [list(piece) for piece in all_pieces
                          if z3.is_true(model.eval(place[piece, owner]))]
                  for owner in OWNERS}
    audit_mixed(
        allocation, totals, minima, tame_role, vector,
        anchor_role, anchor, edge_cap,
    )
    return "sat", allocation


def run(profile_path, output_path, tame_role, edge_cap, timeout_seconds):
    raw = json.loads(profile_path.read_text())
    totals = rows(raw, "terminal_profile_totals")
    minima = rows(raw, "terminal_profile_minima")
    assert role_slack(totals, minima, tame_role) == 2
    entries = []
    terminal = None
    for vector_pattern in role_patterns():
        vector = {tame_role: vector_pattern}
        allocation = numeric_oracle(totals, minima, (tame_role,), vector, edge_cap)
        if allocation is not None:
            exact_audit(allocation, totals, minima, (tame_role,), vector, edge_cap)
            entries.append({
                "pattern": pattern_key((tame_role,), vector),
                "kind": "tame",
                "allocation": allocation,
            })
            continue
        found = None
        unknowns = []
        for anchor_role in GOODS:
            if anchor_role == tame_role or role_slack(totals, minima, anchor_role) < 2:
                continue
            for anchor in OWNERS:
                status, allocation = mixed_oracle(
                    totals, minima, tame_role, vector, anchor_role, anchor,
                    edge_cap, timeout_seconds,
                )
                if status == "sat":
                    edges, slack = audit_mixed(
                        allocation, totals, minima, tame_role, vector,
                        anchor_role, anchor, edge_cap,
                    )
                    found = {
                        "pattern": pattern_key((tame_role,), vector),
                        "kind": "mixed_anchor",
                        "anchor_role": anchor_role,
                        "anchor_observer": anchor,
                        "edges": edges,
                        "minimum_certified_slack": str(slack),
                        "allocation": allocation,
                    }
                    break
                if status == "unknown":
                    unknowns.append({
                        "anchor_role": anchor_role,
                        "anchor_observer": anchor,
                    })
            if found is not None:
                break
        if found is None:
            terminal = {
                "pattern": pattern_key((tame_role,), vector),
                "vector": vector,
                "status": "UNKNOWN" if unknowns else "UNSAT",
                "unknown_lanes": unknowns,
            }
            break
        entries.append(found)
    result = {
        "schema": "fixed-u-mixed-anchor-menu-v1",
        "status": (
            "VERIFIED_FULL_EIGHT_PATTERN_MIXED_MENU" if terminal is None
            else "UNKNOWN_MIXED_MENU" if terminal["status"] == "UNKNOWN"
            else "SAT_ONE_TAME_PLUS_ONE_ANCHOR_MENU_OBSTRUCTION"
        ),
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "tame_role": tame_role,
        "closed_pattern_count": len(entries),
        "entries": entries,
        "terminal": terminal,
        "claim_boundary": (
            "This exact mixed menu closes the displayed obstruction profile. It "
            "is the minimal mechanism suggested by the failure, not a universal "
            "form-2 theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tame-role", default="gq")
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    result = run(
        args.profile, args.output, args.tame_role,
        args.edge_cap, args.timeout_seconds,
    )
    print(json.dumps({
        "status": result["status"],
        "closed_pattern_count": result["closed_pattern_count"],
        "kinds": [entry["kind"] for entry in result["entries"]],
        "anchors": sorted({
            (entry.get("anchor_role"), entry.get("anchor_observer"))
            for entry in result["entries"] if entry["kind"] == "mixed_anchor"
        }),
    }, indent=2))


if __name__ == "__main__":
    main()
