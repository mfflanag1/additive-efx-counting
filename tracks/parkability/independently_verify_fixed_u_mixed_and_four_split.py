#!/usr/bin/env python3
"""Independent integer-owner audit of the mixed-menu and four-split obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


WHOLE, LOW, HIGH, SELECTED, COMPLEMENT = (
    "whole", "low", "high", "selected", "complement"
)
SUPPLIER = {
    role: source for source, roles in SUPPORT_STATE.items() for role in roles
}


def q(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_rows(raw, stem):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[f"terminal_profile_{stem}"].items()
    }


def slack(totals, minima, role):
    return min(totals[o][role] // minima[o][role] for o in OWNERS)


def anchor_endpoints(totals, minima, role, anchor, observer):
    total, minimum = totals[observer][role], minima[observer][role]
    result = []
    for selected in (
        (minimum,) if observer == anchor else (minimum, total - minimum)
    ):
        result.append((selected, total - selected))
    if slack(totals, minima, role) >= 3:
        for selected in (
            (minimum,) if observer == anchor else (minimum, total - 2 * minimum)
        ):
            result.append((selected, minimum))
    return tuple(dict.fromkeys(result))


def parse_pattern(pattern):
    _, bits = pattern.split(":", 1)
    assert len(bits) == len(OWNERS)
    return dict(zip(OWNERS, map(int, bits)))


def independently_decide_mixed_cell(totals, minima, tame_role, pattern,
                                    anchor_role=None, anchor=None,
                                    edge_cap=4, timeout_seconds=60):
    bits = parse_pattern(pattern)
    pieces = tuple(
        piece for role in GOODS
        for piece in (
            ((role, LOW), (role, HIGH)) if role == tame_role
            else ((role, SELECTED), (role, COMPLEMENT))
            if role == anchor_role else ((role, WHOLE),)
        )
    )
    owner = {
        piece: z3.Int(f"mix_owner_{piece[0]}_{piece[1]}") for piece in pieces
    }
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(owner[p] >= 0, owner[p] < len(OWNERS)) for p in pieces))
    solver.add(*(z3.Or(*(owner[p] == index for p in pieces))
                 for index in range(len(OWNERS))))
    if anchor_role is not None:
        solver.add(owner[anchor_role, SELECTED] != owner[anchor_role, COMPLEMENT])

    edge_flags = []
    for source in SUPPORT_STATE:
        source_pieces = [piece for piece in pieces if SUPPLIER[piece[0]] == source]
        for index, target in enumerate(OWNERS):
            if source != target:
                edge_flags.append(z3.Or(*(owner[p] == index for p in source_pieces)))
    solver.add(z3.PbLe([(flag, 1) for flag in edge_flags], edge_cap))

    for observer_index, observer in enumerate(OWNERS):
        scenarios = (
            ((None, None),) if anchor_role is None
            else anchor_endpoints(totals, minima, anchor_role, anchor, observer)
        )
        for selected, complement_floor in scenarios:
            def value(piece):
                role, kind = piece
                if kind == WHOLE:
                    return totals[observer][role]
                if role == tame_role:
                    low_has_minimum = bits[observer] == 0
                    if (kind == LOW) == low_has_minimum:
                        return minima[observer][role]
                    return totals[observer][role] - minima[observer][role]
                if kind == SELECTED:
                    return selected
                return totals[observer][role] - selected

            def floor(piece):
                role, kind = piece
                if kind == WHOLE:
                    return minima[observer][role]
                if role == tame_role:
                    return value(piece)
                if kind == SELECTED:
                    return selected
                return complement_floor

            utility = {
                index: z3.Sum(*(
                    z3.If(owner[p] == index, q(value(p)), z3.RealVal(0))
                    for p in pieces
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


def physical_witness(totals, minima, product_cell):
    values = {}
    role_goods = {}
    sides = {}
    for role in GOODS:
        singleton = all(totals[o][role] == minima[o][role] for o in OWNERS)
        goods = (f"{role}:0",) if singleton else (f"{role}:0", f"{role}:1")
        role_goods[role] = goods
        bits = (
            parse_pattern(product_cell[role]) if role in product_cell
            else {observer: 0 for observer in OWNERS}
        )
        for observer in OWNERS:
            side = bool(bits[observer])
            sides[role, observer] = side
            if singleton:
                values[observer, goods[0]] = totals[observer][role]
            else:
                gap = totals[observer][role] - 2 * minima[observer][role]
                shift = gap if side else Fraction()
                values[observer, goods[0]] = minima[observer][role] + shift
                values[observer, goods[1]] = totals[observer][role] - minima[observer][role] - shift
                assert min(values[observer, g] for g in goods) == minima[observer][role]
    return values, role_goods


def independently_decide_physical(values, role_goods, split_cap,
                                  edge_cap=4, timeout_seconds=60):
    goods = tuple(g for role in GOODS for g in role_goods[role])
    owner = {good: z3.Int(f"phys_owner_{good.replace(':', '_')}") for good in goods}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    solver.add(*(z3.And(owner[g] >= 0, owner[g] < len(OWNERS)) for g in goods))
    solver.add(*(z3.Or(*(owner[g] == index for g in goods))
                 for index in range(len(OWNERS))))

    edge_flags = []
    for source in SUPPORT_STATE:
        source_goods = [
            good for good in goods if SUPPLIER[good.split(":", 1)[0]] == source
        ]
        for index, target in enumerate(OWNERS):
            if source != target:
                edge_flags.append(z3.Or(*(owner[g] == index for g in source_goods)))
    solver.add(z3.PbLe([(flag, 1) for flag in edge_flags], edge_cap))
    split_flags = []
    for role, members in role_goods.items():
        if len(members) == 2:
            split_flags.append(owner[members[0]] != owner[members[1]])
    solver.add(z3.PbLe([(flag, 1) for flag in split_flags], split_cap))

    for observer_index, observer in enumerate(OWNERS):
        utility = {
            index: z3.Sum(*(
                z3.If(owner[g] == index, q(values[observer, g]), z3.RealVal(0))
                for g in goods
            ))
            for index in range(len(OWNERS))
        }
        for target_index in range(len(OWNERS)):
            if target_index == observer_index:
                continue
            for good in goods:
                solver.add(z3.Implies(
                    owner[good] == target_index,
                    utility[observer_index] >= utility[target_index] - q(values[observer, good]),
                ))
    status = solver.check()
    if status != z3.sat:
        return str(status), None, (
            solver.reason_unknown() if status == z3.unknown else None
        )
    model = solver.model()
    allocation = {
        target: [
            good for good in goods
            if model.eval(owner[good]).as_long() == index
        ]
        for index, target in enumerate(OWNERS)
    }
    return "sat", allocation, None


def audit_physical_allocation(allocation, values, role_goods, edge_cap):
    goods = [good for bundle in allocation.values() for good in bundle]
    assert len(goods) == len(set(goods)) == sum(map(len, role_goods.values()))
    edges = sorted({
        (SUPPLIER[good.split(":", 1)[0]], target)
        for target, bundle in allocation.items() for good in bundle
        if SUPPLIER[good.split(":", 1)[0]] != target
    })
    assert len(edges) <= edge_cap
    split_roles = sorted(
        role for role, members in role_goods.items() if len({
            target for target, bundle in allocation.items() if set(members) & set(bundle)
        }) > 1
    )
    for observer in OWNERS:
        own = sum((values[observer, g] for g in allocation[observer]), Fraction())
        for target in OWNERS:
            if target == observer:
                continue
            total = sum((values[observer, g] for g in allocation[target]), Fraction())
            for good in allocation[target]:
                assert own >= total - values[observer, good]
    return edges, split_roles


def replay_master(totals, minima):
    solver, total, minimum = build_physical_master(2)
    for observer in OWNERS:
        for role in GOODS:
            solver.add(total[role, observer] == q(totals[observer][role]))
            solver.add(minimum[role, observer] == q(minima[observer][role]))
    return str(solver.check())


def run(profile_path, primary_audit_path, output_path, timeout_seconds):
    raw = json.loads(profile_path.read_text())
    totals = load_rows(raw, "totals")
    minima = load_rows(raw, "minima")
    primary = json.loads(primary_audit_path.read_text())
    assert primary["status"] == "SAT_PATTERN_DEPENDENT_MIXED_MENU_OBSTRUCTION"
    assert primary["unknown_cell_count"] == 0
    master_status = replay_master(totals, minima)
    assert master_status == "sat"

    mixed_witnesses = []
    for tame_role in primary["tame_roles"]:
        pattern = primary["failing_patterns_by_tame_role"][tame_role][0]
        tame_status, reason = independently_decide_mixed_cell(
            totals, minima, tame_role, pattern,
            timeout_seconds=timeout_seconds,
        )
        assert tame_status == "unsat", (tame_role, pattern, tame_status, reason)
        lanes = []
        for anchor_role in primary["eligible_anchor_roles"]:
            if anchor_role == tame_role:
                continue
            for anchor in OWNERS:
                status, reason = independently_decide_mixed_cell(
                    totals, minima, tame_role, pattern, anchor_role, anchor,
                    timeout_seconds=timeout_seconds,
                )
                assert status == "unsat", (
                    tame_role, pattern, anchor_role, anchor, status, reason
                )
                lanes.append({
                    "anchor_role": anchor_role,
                    "anchor_observer": anchor,
                    "status": status,
                })
        mixed_witnesses.append({
            "tame_role": tame_role,
            "pattern": pattern,
            "tame_status": tame_status,
            "anchor_lane_count": len(lanes),
            "anchor_lanes": lanes,
        })

    product_cell = {
        row["tame_role"]: row["pattern"] for row in mixed_witnesses
    }
    values, role_goods = physical_witness(totals, minima, product_cell)
    split_attempts = []
    certificate = None
    for split_cap in range(5):
        status, allocation, reason = independently_decide_physical(
            values, role_goods, split_cap,
            timeout_seconds=timeout_seconds,
        )
        attempt = {"split_cap": split_cap, "status": status}
        if reason is not None:
            attempt["reason_unknown"] = reason
        split_attempts.append(attempt)
        if status == "sat":
            edges, split_roles = audit_physical_allocation(
                allocation, values, role_goods, 4
            )
            certificate = {
                "allocation": allocation,
                "edges": [list(edge) for edge in edges],
                "split_roles": split_roles,
            }
            break
    assert split_attempts == [
        {"split_cap": 0, "status": "unsat"},
        {"split_cap": 1, "status": "unsat"},
        {"split_cap": 2, "status": "unsat"},
        {"split_cap": 3, "status": "unsat"},
        {"split_cap": 4, "status": "sat"},
    ]
    assert certificate is not None and len(certificate["split_roles"]) == 4

    result = {
        "schema": "fixed-u-pattern-mixed-four-split-independent-audit-v1",
        "status": "AUDIT_PASS_MIXED_MENU_REFUTED_FOUR_SPLITS_NECESSARY_AND_SUFFICIENT",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "primary_audit": str(primary_audit_path),
        "primary_audit_sha256": hashlib.sha256(primary_audit_path.read_bytes()).hexdigest(),
        "master_replay_status": master_status,
        "mixed_witnesses": mixed_witnesses,
        "global_product_cell": product_cell,
        "independent_mixed_anchor_lane_count": sum(
            row["anchor_lane_count"] for row in mixed_witnesses
        ),
        "physical_witness_side_patterns": product_cell,
        "physical_values": {
            observer: {
                good: str(values[observer, good])
                for role in GOODS for good in role_goods[role]
            } for observer in OWNERS
        },
        "split_attempts": split_attempts,
        "four_split_certificate": certificate,
        "method": (
            "independent integer-owner encodings for both mixed endpoint cells "
            "and the concrete physical split-count decision; no import of the "
            "primary Boolean mixed or two-anchor oracles"
        ),
        "claim_boundary": (
            "This exact form-2 profile refutes every one-tame-cell plus one-anchor "
            "menu, and its displayed two-good realization needs exactly four "
            "split roles under the four-edge support budget. It is not an EFX "
            "counterexample and does not prove a universal four-split theorem."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--primary-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=60)
    args = parser.parse_args()
    result = run(
        args.profile, args.primary_audit, args.output, args.timeout_seconds
    )
    print(json.dumps({
        "status": result["status"],
        "master_replay_status": result["master_replay_status"],
        "mixed_anchor_lane_count": result["independent_mixed_anchor_lane_count"],
        "split_attempts": result["split_attempts"],
        "four_split_roles": result["four_split_certificate"]["split_roles"],
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
