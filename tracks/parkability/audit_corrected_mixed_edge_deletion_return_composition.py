#!/usr/bin/env python3
"""Exact audit of corrected one-decorated deletion-return composition."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def subsets(items: tuple[str, ...]):
    for mask in range(1 << len(items)):
        yield frozenset(item for index, item in enumerate(items) if mask >> index & 1)


def cross_decorated_local_separator() -> dict:
    agents = ("t", "d", "a", "b")
    p = ("p1", "p2")
    e = ("p1", "p2", "g")
    dcore = ("d1", "d2", "d3")
    old = {"t": "at", "a": "aa", "b": "ab"}
    goods = (*e, *dcore, *old.values(), "xt", "xd", "xa", "xb")
    tiny = Fraction(1, 10)
    rows = {agent: {good: tiny for good in goods} for agent in agents}
    # Base utilities are represented by the x-singletons.
    for agent, good in zip(agents, ("xt", "xd", "xa", "xb"), strict=True):
        rows[agent][good] = Fraction(10)
    rows["t"].update({"p1": Fraction(11, 2), "p2": Fraction(11, 2), "g": Fraction(1),
                      "d1": Fraction(6), "d2": Fraction(6), "d3": Fraction(6),
                      "at": Fraction(21, 2)})
    rows["d"].update({"d1": Fraction(5), "d2": Fraction(5), "d3": Fraction(5),
                      "p1": Fraction(1), "p2": Fraction(1), "g": Fraction(1)})
    rows["a"]["aa"] = Fraction(11)
    rows["b"]["ab"] = Fraction(11)
    current_utility = {"t": Fraction(25, 2), "d": Fraction(12),
                       "a": Fraction(12), "b": Fraction(12)}
    base_utility = {agent: Fraction(10) for agent in agents}

    def value(agent: str, bundle) -> Fraction:
        return sum((rows[agent][good] for good in bundle), Fraction(0))

    def threshold(agent: str, bundle) -> Fraction:
        bundle = tuple(bundle)
        if len(bundle) <= 1:
            return Fraction(0)
        return value(agent, bundle) - min(rows[agent][good] for good in bundle)

    P = frozenset(p)
    E = frozenset(e)
    D = frozenset(dcore)
    assert min(E, key=lambda good: rows["t"][good]) == "g"
    assert value("t", P) == threshold("t", E) == 11
    assert value("t", {old["t"]}) == Fraction(21, 2) < value("t", P)
    assert all(threshold(agent, E) <= current_utility[agent] for agent in agents)
    assert all(threshold(agent, D) <= current_utility[agent] for agent in agents)
    assert value("d", D) > current_utility["d"]
    assert value("t", P) > base_utility["t"]
    feasible = []
    failures = []
    for J in subsets(dcore):
        qt = P | J
        qd = D - J
        conditions = {
            "d_strict": value("d", qd) > base_utility["d"],
            "t_safe_against_d": value("t", qt) >= threshold("t", qd),
            "d_safe_against_t": value("d", qd) >= threshold("d", qt),
            "a_safe": value("a", {old["a"]}) >= max(threshold("a", qt), threshold("a", qd)),
            "b_safe": value("b", {old["b"]}) >= max(threshold("b", qt), threshold("b", qd)),
        }
        record = {"J": sorted(J), "conditions": conditions}
        if all(conditions.values()):
            feasible.append(record)
        else:
            failures.append(record)
    assert not feasible
    assert failures[0]["J"] == []
    assert not failures[0]["conditions"]["t_safe_against_d"]
    assert all(
        (not rec["conditions"]["d_strict"]) for rec in failures if rec["J"]
    )
    complete_pool = tuple(e) + (old["t"],) + tuple(dcore)
    complete_feasible = []
    recipients = ("t", "d", None)
    for code in range(3 ** len(complete_pool)):
        allocation = {"t": set(), "d": set()}
        cursor = code
        for good in complete_pool:
            recipient = cursor % 3
            cursor //= 3
            if recipient < 2:
                allocation[recipients[recipient]].add(good)
        qt = frozenset(allocation["t"])
        qd = frozenset(allocation["d"])
        if not (value("t", qt) > base_utility["t"] and value("d", qd) > base_utility["d"]):
            continue
        if value("t", qt) < threshold("t", qd) or value("d", qd) < threshold("d", qt):
            continue
        if any(
            value(agent, {old[agent]}) < max(threshold(agent, qt), threshold(agent, qd))
            for agent in ("a", "b")
        ):
            continue
        complete_feasible.append({"t": sorted(qt), "d": sorted(qd)})
    assert len(complete_feasible) == 89
    return {
        "valuations": {
            agent: {good: str(number) for good, number in row.items()}
            for agent, row in rows.items()
        },
        "base_utilities": {agent: str(number) for agent, number in base_utility.items()},
        "current_utilities": {agent: str(number) for agent, number in current_utility.items()},
        "P": sorted(P), "E": sorted(E), "D": sorted(D),
        "deleted_good": "g",
        "old_cores": old,
        "exchange_family_size": 2 ** len(dcore),
        "feasible_exchange_count": len(feasible),
        "complete_pool_family_size": 3 ** len(complete_pool),
        "complete_pool_feasible_count": len(complete_feasible),
        "first_complete_pool_escape": complete_feasible[0],
        "failed_exchanges": failures,
        "interpretation": (
            "empty J leaves the hole owner below D's threshold; every nonempty "
            "J consumes the mixed source's strict base margin; the complete "
            "pool nevertheless escapes, so this is not a terminal model"
        ),
    }


def run(root: Path) -> dict:
    old, residual, incoming, theta, base = z3.Reals(
        "old residual incoming theta base"
    )
    d_value, y_d, p_tau = z3.Reals("d_value y_d p_tau")
    p_value, d_tau_t = z3.Reals("p_value d_tau_t")
    symbolic = {
        "residual_failure_forces_incoming_replacement": prove(
            [old > base, residual >= 0, old + residual < theta,
             theta <= incoming + residual],
            incoming > old,
        ),
        "mixed_source_automatically_observes_deleted_closing_core": prove(
            [d_value > y_d, y_d >= p_tau], d_value > p_tau
        ),
        "cross_decorated_debt_is_exact": prove(
            [p_value > base, p_value < d_tau_t], d_tau_t > base
        ),
    }
    assert all(symbolic.values())

    cases = []
    owners = tuple(range(4))
    for path in itertools.permutations(owners):
        for mixed_position in range(4):
            for closing_position in range(1, 4):
                d_equals_t = mixed_position == 0
                cases.append({
                    "path": list(path),
                    "mixed_position": mixed_position,
                    "closing_position": closing_position,
                    "mixed_source_is_hole": d_equals_t,
                    "allocated_special_core_count": 1 if d_equals_t else 2,
                    "old_core_recipient_count": 3 if d_equals_t else 2,
                    "cross_decorated_gate_applicable": not d_equals_t,
                })
    assert len(cases) == 288
    counts = {
        "mixed_source_is_hole": sum(case["mixed_source_is_hole"] for case in cases),
        "two_special_cores": sum(case["allocated_special_core_count"] == 2 for case in cases),
    }
    assert counts == {"mixed_source_is_hole": 72, "two_special_cores": 216}

    witness = cross_decorated_local_separator()
    script = Path(__file__).resolve()
    theorem = root / "results/CORRECTED_MIXED_EDGE_DELETION_RETURN_COMPOSITION_20260813.md"
    return {
        "schema": "corrected-mixed-edge-deletion-return-composition-audit-v1",
        "status": "KAPPA1_REDUCED_TO_CROSS_DECORATED_EXCHANGE",
        "symbolic_checks": symbolic,
        "case_count": len(cases),
        "case_counts": counts,
        "cases": cases,
        "local_cross_decorated_separator": witness,
        "smallest_terminal": "direct two-core separator, superseded by complete selected pool",
        "independent_open_branch": "kappa in {2,3} multi-decorated matching",
        "claim_boundary": (
            "correct kappa=1 payment/debt composition and local separator; "
            "not a globally maximal GG countermodel or GG closure"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "smallest_terminal": result["smallest_terminal"],
        "open_branch": result["independent_open_branch"],
    }, indent=2))


if __name__ == "__main__":
    main()
