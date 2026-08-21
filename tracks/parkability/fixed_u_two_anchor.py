"""Exact two-anchor completion oracle for fixed-U totals/minima profiles.

Two distinct roles are split.  In each role the selected good is required to
be a minimum good for its declared anchor observer.  The allocation must be
EFX for every physical realization compatible with the totals and minima.
The endpoint product below is exact because the two roles contain disjoint
goods and every EFX slack is affine in their selected-good coordinates.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

import z3

from .fixed_u_dynamic_anchor import (
    COMPLEMENT,
    SELECTED,
    WHOLE,
    anchor_scenarios,
    role_slack,
    rv,
    supplier_map,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


def two_anchor_pieces(split_roles):
    split_roles = frozenset(split_roles)
    assert len(split_roles) == 2
    return tuple(
        piece
        for role in GOODS
        for piece in (
            ((role, SELECTED), (role, COMPLEMENT))
            if role in split_roles else ((role, WHOLE),)
        )
    )


def scenario_product(totals, minima, split_roles, anchors, observer):
    """All exact endpoint combinations for one observer and two roles."""
    lanes = [
        anchor_scenarios(totals, minima, role, anchors[role], observer)
        for role in split_roles
    ]
    return tuple(itertools.product(*lanes))


def scenario_maps(split_roles, scenario):
    selected = {}
    complement_floor = {}
    labels = {}
    for role, (label, value, floor) in zip(split_roles, scenario):
        labels[role] = label
        selected[role] = value
        complement_floor[role] = floor
    return labels, selected, complement_floor


def piece_value(totals, observer, piece, selected):
    role, kind = piece
    if kind == WHOLE:
        return totals[observer][role]
    if kind == SELECTED:
        return selected[role]
    return totals[observer][role] - selected[role]


def piece_floor(minima, observer, piece, selected, complement_floor):
    role, kind = piece
    if kind == WHOLE:
        return minima[observer][role]
    if kind == SELECTED:
        return selected[role]
    return complement_floor[role]


def audit_two_anchor(allocation, totals, minima, split_roles, anchors,
                     edge_cap=4):
    split_roles = tuple(split_roles)
    expected = sorted(two_anchor_pieces(split_roles))
    placed = [tuple(piece) for bundle in allocation.values() for piece in bundle]
    assert sorted(placed) == expected
    assert len(placed) == len(set(placed))
    assert all(allocation[owner] for owner in OWNERS)
    for role in split_roles:
        holders = {
            kind: owner
            for owner, bundle in allocation.items()
            for raw_piece in bundle
            for piece_role, kind in (tuple(raw_piece),)
            if piece_role == role
        }
        assert holders[SELECTED] != holders[COMPLEMENT]

    supplier = supplier_map()
    edges = tuple(sorted({
        (supplier[role], owner)
        for owner, bundle in allocation.items()
        for role, _ in map(tuple, bundle)
        if supplier[role] != owner
    }))
    assert len(edges) <= edge_cap

    minimum_slack = None
    for observer in OWNERS:
        for scenario in scenario_product(
            totals, minima, split_roles, anchors, observer
        ):
            _, selected, complement_floor = scenario_maps(split_roles, scenario)
            utility = {
                owner: sum((
                    piece_value(totals, observer, tuple(piece), selected)
                    for piece in allocation[owner]
                ), Fraction())
                for owner in OWNERS
            }
            for target in OWNERS:
                if target == observer:
                    continue
                for raw_piece in allocation[target]:
                    piece = tuple(raw_piece)
                    slack = utility[observer] - utility[target] + piece_floor(
                        minima, observer, piece, selected, complement_floor
                    )
                    assert slack >= 0, (
                        observer, target, piece, split_roles, anchors, scenario,
                        slack,
                    )
                    minimum_slack = (
                        slack if minimum_slack is None
                        else min(minimum_slack, slack)
                    )
    return edges, minimum_slack


def two_anchor_oracle_for_pair(totals, minima, split_roles, anchors,
                               edge_cap=4, timeout_seconds=60):
    split_roles = tuple(split_roles)
    assert len(split_roles) == 2 and len(set(split_roles)) == 2
    if any(role_slack(totals, minima, role) < 2 for role in split_roles):
        return "inapplicable", None, None

    all_pieces = two_anchor_pieces(split_roles)
    supplier = supplier_map()
    prefix = "two_anchor_" + "_".join(
        f"{role}_{anchors[role]}" for role in split_roles
    )
    place = {
        (piece, owner): z3.Bool(f"{prefix}_{piece[0]}_{piece[1]}_{owner}")
        for piece in all_pieces for owner in OWNERS
    }
    edge = {
        (source, target): z3.Bool(f"{prefix}_edge_{source}_{target}")
        for source in SUPPORT_STATE for target in OWNERS if source != target
    }
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for piece in all_pieces:
        solver.add(z3.PbEq([(place[piece, owner], 1) for owner in OWNERS], 1))
        source = supplier[piece[0]]
        for owner in OWNERS:
            if owner != source:
                solver.add(z3.Implies(place[piece, owner], edge[source, owner]))
    solver.add(z3.PbLe([(flag, 1) for flag in edge.values()], edge_cap))
    for owner in OWNERS:
        solver.add(z3.Or(*(place[piece, owner] for piece in all_pieces)))
    for role in split_roles:
        for owner in OWNERS:
            solver.add(z3.Not(z3.And(
                place[(role, SELECTED), owner],
                place[(role, COMPLEMENT), owner],
            )))

    for observer in OWNERS:
        for scenario in scenario_product(
            totals, minima, split_roles, anchors, observer
        ):
            _, selected, complement_floor = scenario_maps(split_roles, scenario)
            utility = {
                owner: z3.Sum(*(
                    z3.If(
                        place[piece, owner],
                        rv(piece_value(totals, observer, piece, selected)),
                        z3.RealVal(0),
                    )
                    for piece in all_pieces
                ))
                for owner in OWNERS
            }
            for target in OWNERS:
                if target == observer:
                    continue
                for piece in all_pieces:
                    solver.add(z3.Implies(
                        place[piece, target],
                        utility[observer] >= utility[target] - rv(piece_floor(
                            minima, observer, piece, selected, complement_floor
                        )),
                    ))

    status = solver.check()
    if status != z3.sat:
        reason = solver.reason_unknown() if status == z3.unknown else None
        return str(status), None, reason
    model = solver.model()
    allocation = {
        owner: [
            list(piece) for piece in all_pieces
            if z3.is_true(model.eval(place[piece, owner]))
        ]
        for owner in OWNERS
    }
    audit_two_anchor(
        allocation, totals, minima, split_roles, anchors, edge_cap
    )
    return "sat", allocation, None


def two_anchor_oracle(totals, minima, edge_cap=4, timeout_seconds=60):
    """Exhaust every unordered role pair and ordered anchor-observer pair."""
    eligible = [
        role for role in GOODS if role_slack(totals, minima, role) >= 2
    ]
    unknowns = []
    lanes = 0
    for split_roles in itertools.combinations(eligible, 2):
        for anchor_pair in itertools.product(OWNERS, repeat=2):
            anchors = dict(zip(split_roles, anchor_pair))
            lanes += 1
            status, allocation, reason = two_anchor_oracle_for_pair(
                totals, minima, split_roles, anchors,
                edge_cap, timeout_seconds,
            )
            if status == "sat":
                return "sat", {
                    "split_roles": list(split_roles),
                    "anchors": anchors,
                    "allocation": allocation,
                    "lanes_examined": lanes,
                }, None
            if status == "unknown":
                unknowns.append({
                    "split_roles": list(split_roles),
                    "anchors": anchors,
                    "reason": reason,
                })
    if unknowns:
        return "unknown", None, unknowns
    return "unsat", None, {"lanes_examined": lanes}
