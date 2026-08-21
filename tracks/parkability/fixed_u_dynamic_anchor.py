"""Exact whole-role and one-anchor oracles for fixed-U totals/minima profiles."""

from __future__ import annotations

from fractions import Fraction

import z3

from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


WHOLE = "whole"
SELECTED = "selected"
COMPLEMENT = "complement"


def rv(amount):
    amount = Fraction(amount)
    return z3.RealVal(f"{amount.numerator}/{amount.denominator}")


def supplier_map():
    return {
        role: source
        for source, roles in SUPPORT_STATE.items() for role in roles
    }


def role_slack(totals, minima, role):
    return min(totals[observer][role] // minima[observer][role] for observer in OWNERS)


def anchor_scenarios(totals, minima, role, anchor, observer):
    """Exact realization scenarios needed for one selected anchor good.

    At cardinality two, a non-anchor row puts its minimum on either selected
    good, so x is M or T-M and the complement deletion value is T-x.
    At any cardinality at least three, feasible selected coordinates fill the
    interval [M,T-2M]; every affine inequality is controlled by its endpoints,
    and a complement deletion can attain M.  Higher cardinalities only shrink
    this interval and add no condition.
    """
    total = totals[observer][role]
    minimum = minima[observer][role]
    slack = role_slack(totals, minima, role)
    assert slack >= 2
    scenarios = []

    two_good_x = (minimum,) if observer == anchor else (minimum, total - minimum)
    for x in two_good_x:
        scenarios.append(("k2", x, total - x))

    if slack >= 3:
        three_good_x = (
            (minimum,) if observer == anchor
            else (minimum, total - 2 * minimum)
        )
        for x in three_good_x:
            scenarios.append(("k3plus", x, minimum))

    unique = []
    seen = set()
    for scenario in scenarios:
        key = scenario[1:]
        if key not in seen:
            seen.add(key)
            unique.append(scenario)
    return tuple(unique)


def pieces(split_role=None):
    return tuple(
        piece
        for role in GOODS
        for piece in (
            ((role, SELECTED), (role, COMPLEMENT))
            if role == split_role else ((role, WHOLE),)
        )
    )


def piece_value(totals, observer, piece, selected_value=None):
    role, kind = piece
    if kind == WHOLE:
        return totals[observer][role]
    assert selected_value is not None
    if kind == SELECTED:
        return selected_value
    return totals[observer][role] - selected_value


def piece_floor(minima, observer, piece, selected_value=None,
                complement_floor=None):
    role, kind = piece
    if kind == WHOLE:
        return minima[observer][role]
    if kind == SELECTED:
        assert selected_value is not None
        return selected_value
    assert complement_floor is not None
    return complement_floor


def placement_edges(allocation):
    supplier = supplier_map()
    return tuple(sorted({
        (supplier[role], owner)
        for owner, owner_pieces in allocation.items()
        for role, _ in owner_pieces
        if supplier[role] != owner
    }))


def audit_complete(allocation, split_role, edge_cap):
    expected = sorted(pieces(split_role))
    placed = [tuple(piece) for bundle in allocation.values() for piece in bundle]
    assert sorted(placed) == expected
    assert len(placed) == len(set(placed))
    assert all(allocation[owner] for owner in OWNERS)
    if split_role is not None:
        holders = {
            kind: owner
            for owner, bundle in allocation.items()
            for role, kind in bundle if role == split_role
        }
        assert holders[SELECTED] != holders[COMPLEMENT]
    edges = placement_edges(allocation)
    assert len(edges) <= edge_cap
    return edges


def exact_audit_whole(allocation, totals, minima, edge_cap=4):
    edges = audit_complete(allocation, None, edge_cap)
    minimum_slack = None
    for observer in OWNERS:
        utility = {
            owner: sum(
                (totals[observer][role] for role, _ in allocation[owner]),
                Fraction(),
            )
            for owner in OWNERS
        }
        for target in OWNERS:
            if target == observer:
                continue
            for role, _ in allocation[target]:
                slack = utility[observer] - utility[target] + minima[observer][role]
                assert slack >= 0
                minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
    return edges, minimum_slack


def exact_audit_anchor(allocation, totals, minima, split_role, anchor, edge_cap=4):
    edges = audit_complete(allocation, split_role, edge_cap)
    minimum_slack = None
    for observer in OWNERS:
        for _, selected_value, complement_floor in anchor_scenarios(
            totals, minima, split_role, anchor, observer
        ):
            utility = {
                owner: sum(
                    (piece_value(totals, observer, tuple(piece), selected_value)
                     for piece in allocation[owner]),
                    Fraction(),
                )
                for owner in OWNERS
            }
            for target in OWNERS:
                if target == observer:
                    continue
                for raw_piece in allocation[target]:
                    piece = tuple(raw_piece)
                    slack = (
                        utility[observer] - utility[target]
                        + piece_floor(
                            minima, observer, piece, selected_value, complement_floor
                        )
                    )
                    assert slack >= 0, (
                        split_role, anchor, observer, target, piece, slack
                    )
                    minimum_slack = (
                        slack if minimum_slack is None else min(minimum_slack, slack)
                    )
    return edges, minimum_slack


def _placement_solver(split_role, edge_cap, timeout_seconds, prefix):
    all_pieces = pieces(split_role)
    supplier = supplier_map()
    place = {
        (piece, owner): z3.Bool(
            f"{prefix}_{piece[0]}_{piece[1]}_{owner}"
        )
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
    if split_role is not None:
        selected = (split_role, SELECTED)
        complement = (split_role, COMPLEMENT)
        for owner in OWNERS:
            solver.add(z3.Not(z3.And(
                place[selected, owner], place[complement, owner]
            )))
    return solver, place, all_pieces


def _extract_allocation(model, place, all_pieces):
    return {
        owner: [list(piece) for piece in all_pieces
                if z3.is_true(model.eval(place[piece, owner]))]
        for owner in OWNERS
    }


def whole_role_oracle(totals, minima, edge_cap=4, timeout_seconds=30):
    solver, place, all_pieces = _placement_solver(
        None, edge_cap, timeout_seconds, "dynamic_whole"
    )
    utility = {
        (observer, owner): z3.Sum(*(
            z3.If(place[piece, owner], rv(totals[observer][piece[0]]), z3.RealVal(0))
            for piece in all_pieces
        ))
        for observer in OWNERS for owner in OWNERS
    }
    for observer in OWNERS:
        for target in OWNERS:
            if target == observer:
                continue
            for piece in all_pieces:
                solver.add(z3.Implies(
                    place[piece, target],
                    utility[observer, observer] >= utility[observer, target]
                    - rv(minima[observer][piece[0]]),
                ))
    status = solver.check()
    if status != z3.sat:
        return str(status), None, solver.reason_unknown() if status == z3.unknown else None
    allocation = _extract_allocation(solver.model(), place, all_pieces)
    exact_audit_whole(allocation, totals, minima, edge_cap)
    return "sat", allocation, None


def anchor_oracle_for_role(totals, minima, split_role, anchor, edge_cap=4,
                           timeout_seconds=30):
    if role_slack(totals, minima, split_role) < 2:
        return "inapplicable", None, None
    solver, place, all_pieces = _placement_solver(
        split_role, edge_cap, timeout_seconds,
        f"dynamic_anchor_{split_role}_{anchor}",
    )
    for observer in OWNERS:
        for _, selected_value, complement_floor in anchor_scenarios(
            totals, minima, split_role, anchor, observer
        ):
            utility = {
                owner: z3.Sum(*(
                    z3.If(
                        place[piece, owner],
                        rv(piece_value(totals, observer, piece, selected_value)),
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
                            minima, observer, piece,
                            selected_value, complement_floor,
                        )),
                    ))
    status = solver.check()
    if status != z3.sat:
        return str(status), None, solver.reason_unknown() if status == z3.unknown else None
    allocation = _extract_allocation(solver.model(), place, all_pieces)
    exact_audit_anchor(
        allocation, totals, minima, split_role, anchor, edge_cap
    )
    return "sat", allocation, None


def dynamic_anchor_oracle(totals, minima, edge_cap=4, timeout_seconds=30):
    unknowns = []
    for split_role in GOODS:
        if role_slack(totals, minima, split_role) < 2:
            continue
        for anchor in OWNERS:
            status, allocation, reason = anchor_oracle_for_role(
                totals, minima, split_role, anchor, edge_cap, timeout_seconds
            )
            if status == "sat":
                return "sat", {
                    "split_role": split_role,
                    "anchor_observer": anchor,
                    "allocation": allocation,
                }, None
            if status == "unknown":
                unknowns.append((split_role, anchor, reason))
    if unknowns:
        return "unknown", None, unknowns
    return "unsat", None, None


def _symbolic_piece_value(total, observer, piece, selected_value=None):
    role, kind = piece
    if kind == WHOLE:
        return total[role, observer]
    assert selected_value is not None
    if kind == SELECTED:
        return selected_value
    return total[role, observer] - selected_value


def _symbolic_piece_floor(minimum, observer, piece, selected_value=None,
                          complement_floor=None):
    role, kind = piece
    if kind == WHOLE:
        return minimum[role, observer]
    if kind == SELECTED:
        assert selected_value is not None
        return selected_value
    assert complement_floor is not None
    return complement_floor


def symbolic_scenario_efx(allocation, total, minimum, observer,
                          selected_value=None, complement_floor=None):
    utility = {
        owner: z3.Sum(*(
            _symbolic_piece_value(
                total, observer, tuple(piece), selected_value
            )
            for piece in allocation[owner]
        ))
        for owner in OWNERS
    }
    return z3.And(*(
        utility[observer] >= utility[target] - _symbolic_piece_floor(
            minimum, observer, tuple(piece), selected_value, complement_floor
        )
        for target in OWNERS if target != observer
        for piece in allocation[target]
    ))


def symbolic_whole_closes(allocation, total, minimum):
    return z3.And(*(
        symbolic_scenario_efx(allocation, total, minimum, observer)
        for observer in OWNERS
    ))


def symbolic_anchor_class_formula(allocation, total, minimum, split_role,
                                  anchor, include_three_plus):
    clauses = []
    for observer in OWNERS:
        total_value = total[split_role, observer]
        minimum_value = minimum[split_role, observer]
        two_values = (
            (minimum_value,) if observer == anchor
            else (minimum_value, total_value - minimum_value)
        )
        for selected_value in two_values:
            clauses.append(symbolic_scenario_efx(
                allocation, total, minimum, observer,
                selected_value, total_value - selected_value,
            ))
        if include_three_plus:
            three_values = (
                (minimum_value,) if observer == anchor
                else (minimum_value, total_value - 2 * minimum_value)
            )
            for selected_value in three_values:
                clauses.append(symbolic_scenario_efx(
                    allocation, total, minimum, observer,
                    selected_value, minimum_value,
                ))
    return z3.And(*clauses)


def symbolic_anchor_closes(allocation, total, minimum, split_role, anchor):
    multi = z3.And(*(
        2 * minimum[split_role, observer] <= total[split_role, observer]
        for observer in OWNERS
    ))
    wild = z3.And(*(
        3 * minimum[split_role, observer] <= total[split_role, observer]
        for observer in OWNERS
    ))
    tame = z3.And(multi, z3.Not(wild))
    two_formula = symbolic_anchor_class_formula(
        allocation, total, minimum, split_role, anchor, False
    )
    three_formula = symbolic_anchor_class_formula(
        allocation, total, minimum, split_role, anchor, True
    )
    return z3.Or(
        z3.And(tame, two_formula),
        z3.And(wild, three_formula),
    )


def candidate_signature(candidate):
    allocation = candidate["allocation"]
    normalized = tuple(
        (owner, tuple(sorted(tuple(piece) for piece in allocation[owner])))
        for owner in OWNERS
    )
    return (
        candidate["kind"],
        candidate.get("split_role"),
        candidate.get("anchor_observer"),
        normalized,
    )


def symbolic_candidate_closes(candidate, total, minimum):
    if candidate["kind"] == "whole":
        return symbolic_whole_closes(candidate["allocation"], total, minimum)
    assert candidate["kind"] == "anchor"
    return symbolic_anchor_closes(
        candidate["allocation"], total, minimum,
        candidate["split_role"], candidate["anchor_observer"],
    )
