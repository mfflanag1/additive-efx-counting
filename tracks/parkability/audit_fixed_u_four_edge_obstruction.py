#!/usr/bin/env python3
"""Adversarial two-good realization CEGAR against the four-edge/four-split theorem.

For an admissible form-2 totals/minima profile, the solver chooses a two-good
side pattern (which good carries each observer's minimum in every
non-singleton role) and the widest oracle (any complete allocation, any
number of split roles, at most ``edge_cap`` support-transfer edges) answers.
Allocations returned by the oracle become cuts on the pattern solver.  The
loop ends with either a realization admitting no capped complete EFX
allocation (``obstruction``) or a proof that every two-good realization has
one (``closed``).  Exact rational arithmetic throughout; Boolean one-hot owner
encoding, independent of the integer-owner oracles used elsewhere.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

from .run_exact_response_physical_minimum_cegar import build_physical_master
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE

SUPPLIER = {role: source for source, roles in SUPPORT_STATE.items() for role in roles}
SOURCES = tuple(SUPPORT_STATE)


def q(value):
    value = Fraction(value)
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def load_rows(raw, stem):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[f"terminal_profile_{stem}"].items()
    }


def singleton(totals, minima, role):
    return all(totals[o][role] == minima[o][role] for o in OWNERS)


def realization(totals, minima, bits):
    """Two goods per non-singleton role; observer o's minimum sits on good 0 iff bits[role,o]==0."""
    values, role_goods = {}, {}
    for role in GOODS:
        if singleton(totals, minima, role):
            role_goods[role] = (f"{role}:0",)
            for o in OWNERS:
                values[o, f"{role}:0"] = totals[o][role]
        else:
            role_goods[role] = (f"{role}:0", f"{role}:1")
            for o in OWNERS:
                gap = totals[o][role] - 2 * minima[o][role]
                assert gap >= 0
                low = minima[o][role] + (gap if bits.get((role, o), 0) else 0)
                values[o, f"{role}:0"] = low
                values[o, f"{role}:1"] = totals[o][role] - low
    return values, role_goods


def exact_efx(values, role_goods, allocation):
    goods = [g for gs in role_goods.values() for g in gs]
    assert sorted(g for b in allocation.values() for g in b) == sorted(goods)
    for i in OWNERS:
        own = sum((values[i, g] for g in allocation[i]), Fraction())
        for j in OWNERS:
            if j == i:
                continue
            total = sum((values[i, g] for g in allocation[j]), Fraction())
            for g in allocation[j]:
                if own < total - values[i, g]:
                    return False
    return True


def allocation_stats(role_goods, allocation):
    owner = {g: o for o, bundle in allocation.items() for g in bundle}
    edges = sorted({(SUPPLIER[g.split(":")[0]], owner[g]) for g in owner
                    if SUPPLIER[g.split(":")[0]] != owner[g]})
    splits = sorted(role for role, gs in role_goods.items()
                    if len({owner[g] for g in gs}) > 1)
    return edges, splits


def widest_oracle(values, role_goods, split_cap=None, edge_cap=None, timeout_seconds=60):
    goods = [g for gs in role_goods.values() for g in gs]
    x = {(g, o): z3.Bool(f"x_{g.replace(':', '_')}_{o}") for g in goods for o in OWNERS}
    solver = z3.Solver()
    solver.set(timeout=timeout_seconds * 1000)
    for g in goods:
        solver.add(z3.PbEq([(x[g, o], 1) for o in OWNERS], 1))
    for o in OWNERS:
        solver.add(z3.Or(*(x[g, o] for g in goods)))
    if edge_cap is not None:
        flags = []
        for source in SOURCES:
            sg = [g for g in goods if SUPPLIER[g.split(":")[0]] == source]
            for o in OWNERS:
                if o != source:
                    flags.append(z3.Or(*(x[g, o] for g in sg)))
        solver.add(z3.PbLe([(f, 1) for f in flags], edge_cap))
    if split_cap is not None:
        sflags = []
        for role, gs in role_goods.items():
            if len(gs) >= 2:
                sflags.append(z3.Or(*(
                    z3.Not(z3.And(*(x[g, o] == x[gs[0], o] for g in gs[1:]))) for o in OWNERS
                )))
        solver.add(z3.PbLe([(f, 1) for f in sflags], split_cap))
    for i in OWNERS:
        utility = {o: z3.Sum(*(z3.If(x[g, o], q(values[i, g]), z3.RealVal(0)) for g in goods))
                   for o in OWNERS}
        for j in OWNERS:
            if j == i:
                continue
            for g in goods:
                solver.add(z3.Implies(x[g, j], utility[i] >= utility[j] - q(values[i, g])))
    status = solver.check()
    if status == z3.sat:
        model = solver.model()
        allocation = {o: [g for g in goods if z3.is_true(model.eval(x[g, o], model_completion=True))]
                      for o in OWNERS}
        assert exact_efx(values, role_goods, allocation)
        return "sat", allocation
    return ("unsat" if status == z3.unsat else f"unknown:{solver.reason_unknown()}"), None


def pattern_cegar(totals, minima, split_cap, edge_cap, max_rounds, timeout_seconds, max_bits=None):
    multi = [role for role in GOODS if not singleton(totals, minima, role)]
    b = {(role, o): z3.Bool(f"b_{role}_{o}") for role in multi for o in OWNERS}
    pattern_solver = z3.Solver()
    pattern_solver.set(timeout=timeout_seconds * 1000)
    for role in multi:                       # relabeling of the two goods of a role
        pattern_solver.add(z3.Not(b[role, "r"]))
    if max_bits is not None:
        pattern_solver.add(z3.PbLe([(v, 1) for v in b.values()], max_bits))

    def value_expr(o, good):
        role, index = good.split(":")
        if role not in multi:
            return q(totals[o][role])
        gap = totals[o][role] - 2 * minima[o][role]
        low = q(minima[o][role]) + z3.If(b[role, o], q(gap), z3.RealVal(0))
        return low if index == "0" else q(totals[o][role]) - low

    cuts = []
    for rounds in range(max_rounds):
        status = pattern_solver.check()
        if status == z3.unsat:
            return {"result": "closed", "rounds": rounds, "cut_count": len(cuts)}
        if status != z3.sat:
            return {"result": "unknown_pattern_solver", "rounds": rounds, "cut_count": len(cuts)}
        model = pattern_solver.model()
        bits = {(role, o): int(z3.is_true(model.eval(b[role, o], model_completion=True)))
                for role in multi for o in OWNERS}
        values, role_goods = realization(totals, minima, bits)
        oracle_status, allocation = widest_oracle(values, role_goods, split_cap, edge_cap, timeout_seconds)
        if oracle_status == "unsat":
            return {"result": "obstruction", "rounds": rounds, "cut_count": len(cuts),
                    "pattern": {f"{role}:{o}": v for (role, o), v in bits.items()}}
        if oracle_status != "sat":
            return {"result": "unknown_oracle", "rounds": rounds, "cut_count": len(cuts)}
        cuts.append(allocation)
        violations = []
        for i in OWNERS:
            utility = {o: z3.Sum(*(value_expr(i, g) for g in allocation[o])) for o in OWNERS}
            for j in OWNERS:
                if j == i:
                    continue
                for g in allocation[j]:
                    violations.append(utility[i] < utility[j] - value_expr(i, g))
        pattern_solver.add(z3.Or(*violations))
    return {"result": "budget", "rounds": max_rounds, "cut_count": len(cuts)}


def replay_master(totals, minima):
    solver, total, minimum = build_physical_master(2)
    for observer in OWNERS:
        for role in GOODS:
            solver.add(total[role, observer] == q(totals[observer][role]))
            solver.add(minimum[role, observer] == q(minima[observer][role]))
    return str(solver.check())


def verdict_matrix(values, role_goods, timeout_seconds):
    rows = []
    for edge_cap in (3, 4, 5):
        for split_cap in (0, 4, None):
            status, allocation = widest_oracle(values, role_goods, split_cap, edge_cap, timeout_seconds)
            row = {"edge_cap": edge_cap, "split_cap": split_cap, "status": status}
            if allocation is not None:
                edges, splits = allocation_stats(role_goods, allocation)
                row.update({"allocation": allocation, "edges": [list(e) for e in edges], "split_roles": splits})
            rows.append(row)
    status, allocation = widest_oracle(values, role_goods, 0, None, timeout_seconds)
    edges, splits = allocation_stats(role_goods, allocation) if allocation else ([], [])
    rows.append({"edge_cap": None, "split_cap": 0, "status": status,
                 "edges": [list(e) for e in edges], "split_roles": splits})
    return rows


def run(profile_path, output_path, timeout_seconds, max_rounds):
    raw = json.loads(profile_path.read_text())
    totals, minima = load_rows(raw, "totals"), load_rows(raw, "minima")
    master = replay_master(totals, minima)
    assert master == "sat", master
    # smallest side-bit obstruction under the four-edge cap, splits unbounded
    minimal = None
    for max_bits in range(0, 6):
        result = pattern_cegar(totals, minima, None, 4, max_rounds, timeout_seconds, max_bits=max_bits)
        assert result["result"] in ("closed", "obstruction"), result
        if result["result"] == "obstruction":
            minimal = (max_bits, result)
            break
    assert minimal is not None, "no four-edge obstruction found"
    bits = {tuple(k.split(":")): v for k, v in minimal[1]["pattern"].items()}
    values, role_goods = realization(totals, minima, bits)
    matrix = verdict_matrix(values, role_goods, timeout_seconds)
    four_split_closed = pattern_cegar(totals, minima, 4, 4, max_rounds, timeout_seconds)
    five_edge_zero_split = pattern_cegar(totals, minima, 0, 5, max_rounds, timeout_seconds)
    result = {
        "schema": "fixed-u-four-edge-obstruction-audit-v1",
        "status": "SAT_FOUR_EDGE_DECLARATION_OBSTRUCTION",
        "profile": str(profile_path),
        "profile_sha256": hashlib.sha256(profile_path.read_bytes()).hexdigest(),
        "master_replay_status": master,
        "minimal_side_bits": minimal[0],
        "minimal_obstruction_pattern": minimal[1]["pattern"],
        "minimal_search_rounds": minimal[1]["rounds"],
        "physical_values": {o: {g: str(values[o, g]) for gs in role_goods.values() for g in gs} for o in OWNERS},
        "role_goods": {role: list(gs) for role, gs in role_goods.items()},
        "verdict_matrix": matrix,
        "four_split_four_edge_pattern_cegar": four_split_closed,
        "five_edge_zero_split_pattern_cegar": five_edge_zero_split,
        "claim_boundary": (
            "The displayed two-good realization of this admissible form-2 profile has no "
            "complete EFX allocation with at most four support-transfer edges, for any number of "
            "split roles; five edges suffice with no split at all. This refutes the four-edge "
            "declaration of the universal four-split form-2 theorem. It is not an EFX "
            "counterexample and says nothing about profiles outside the declared master."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    assert all(row["status"] == "unsat" for row in matrix if row["edge_cap"] in (3, 4))
    assert all(row["status"] == "sat" for row in matrix if row["edge_cap"] == 5 or row["edge_cap"] is None)
    assert four_split_closed["result"] == "obstruction"
    assert five_edge_zero_split["result"] == "closed"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--max-rounds", type=int, default=5000)
    args = parser.parse_args()
    result = run(args.profile, args.output, args.timeout_seconds, args.max_rounds)
    print(json.dumps({k: result[k] for k in ("status", "minimal_side_bits", "minimal_obstruction_pattern",
                                              "four_split_four_edge_pattern_cegar",
                                              "five_edge_zero_split_pattern_cegar")}, indent=2))
    for row in result["verdict_matrix"]:
        print(row["edge_cap"], row["split_cap"], row["status"], row.get("edges"), row.get("split_roles"))


if __name__ == "__main__":
    main()
