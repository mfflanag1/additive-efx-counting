#!/usr/bin/env python3
"""Symbolic and finite-interface audit of general mixed deletion return."""

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


def full_pool_local_separator() -> dict:
    agents = ("t", "d", "a", "b")
    E = ("e1", "e2", "e3", "e4")
    D = ("d1", "d2", "d3")
    K = "k"
    pool = (*E, *D, K, "ab")
    goods = (*pool, "aa", "xt", "xd", "xa", "xb")
    tiny = Fraction(1, 10)
    rows = {agent: {good: tiny for good in goods} for agent in agents}
    for agent, good in zip(agents, ("xt", "xd", "xa", "xb"), strict=True):
        rows[agent][good] = Fraction(10)
    for good in (*E, *D):
        rows["t"][good] = Fraction(4)
        rows["d"][good] = Fraction(4)
        rows["a"][good] = Fraction(6)
    for good in E:
        rows["d"][good] = Fraction(1)
    rows["t"][K] = Fraction(11)
    rows["d"][K] = tiny
    rows["a"][K] = Fraction(6)
    for good in E:
        rows["b"][good] = Fraction(3)
    rows["a"]["aa"] = Fraction(11)
    rows["a"]["ab"] = Fraction(6)
    rows["b"]["ab"] = Fraction(11)
    base = {agent: Fraction(10) for agent in agents}
    current = {"t": Fraction(12), "d": Fraction(11),
               "a": Fraction(18), "b": Fraction(11)}

    def value(agent: str, bundle) -> Fraction:
        return sum((rows[agent][good] for good in bundle), Fraction(0))

    def threshold(agent: str, bundle) -> Fraction:
        bundle = tuple(bundle)
        if len(bundle) <= 1:
            return Fraction(0)
        return value(agent, bundle) - min(rows[agent][good] for good in bundle)

    P = frozenset(E[:-1])
    assert value("t", P) == threshold("t", E) == 12
    assert value("t", {K}) == 11 < value("t", P)
    assert value("d", D) == 12 > current["d"]
    assert value("b", E) == 12 > current["b"]
    assert all(threshold(agent, E) <= current[agent] for agent in agents)
    assert all(threshold(agent, D) <= current[agent] for agent in agents)

    feasible = []
    for code in range(4 ** len(pool)):
        allocation = {"t": set(), "d": set(), "b": set()}
        cursor = code
        for good in pool:
            recipient = cursor % 4
            cursor //= 4
            if recipient < 3:
                allocation[("t", "d", "b")[recipient]].add(good)
        qt = frozenset(allocation["t"])
        qd = frozenset(allocation["d"])
        qb = frozenset(allocation["b"])
        if not all(value(agent, bundle) > base[agent] for agent, bundle in (("t", qt), ("d", qd), ("b", qb))):
            continue
        bundles = {"t": qt, "d": qd, "a": frozenset({"aa"}), "b": qb}
        if all(
            value(observer, bundles[observer]) >= threshold(observer, bundles[target])
            for observer in agents for target in agents if observer != target
        ):
            feasible.append({agent: sorted(bundle) for agent, bundle in bundles.items()})
    assert not feasible
    return {
        "pool": list(pool),
        "E": list(E), "P": sorted(P), "D": list(D), "K_t": K,
        "valuations": {
            agent: {good: str(number) for good, number in row.items()}
            for agent, row in rows.items()
        },
        "base_utilities": {agent: str(number) for agent, number in base.items()},
        "current_utilities": {agent: str(number) for agent, number in current.items()},
        "family_size": 4 ** len(pool),
        "feasible_count": 0,
        "blocking_old_observer": "a",
        "interpretation": (
            "Every pool cell paying decorated source d needs at least three pool "
            "goods, whose deletion threshold exceeds old observer a's selected-core "
            "margin. Current safety is funded by a's external signed surplus, so the "
            "next operation must retain/recruit that component."
        ),
    }


def run(root: Path) -> dict:
    source_core, current, debt = z3.Reals("source_core current debt")
    old, residual, incoming, theta, base = z3.Reals(
        "old residual incoming theta base"
    )
    symbolic = {
        "decorated_recipient_pays_every_current_safe_column": prove(
            [source_core > current, debt <= current], source_core > debt
        ),
        "old_residual_failure_forces_incoming_pivot": prove(
            [old > base, residual >= 0, old + residual < theta,
             theta <= incoming + residual],
            incoming > old,
        ),
    }
    assert all(symbolic.values())

    owners = tuple(range(4))
    records = []
    for path in itertools.permutations(owners):
        hole = path[0]
        for kappa in (1, 2, 3):
            for decorated_positions in itertools.combinations(range(4), kappa):
                for closing_position in range(1, 4):
                    decorated = set(decorated_positions)
                    allocated_decorated = decorated - {0}
                    old_recipients = [
                        position for position in range(1, 4) if position not in decorated
                    ]
                    participants = {0, closing_position} | decorated
                    records.append({
                        "path": list(path),
                        "kappa": kappa,
                        "decorated_positions": list(decorated_positions),
                        "closing_position": closing_position,
                        "hole_source_position_decorated": 0 in decorated,
                        "participant_positions": sorted(participants),
                        "participant_count": len(participants),
                        "old_recipient_positions": old_recipients,
                        "automatic_decorated_recipient_count": len(allocated_decorated),
                    })
    assert len(records) == 1008
    counts_by_kappa = {
        str(kappa): sum(record["kappa"] == kappa for record in records)
        for kappa in (1, 2, 3)
    }
    assert counts_by_kappa == {"1": 288, "2": 432, "3": 288}
    participant_count_distribution = {
        str(size): sum(record["participant_count"] == size for record in records)
        for size in range(2, 5)
    }
    assert participant_count_distribution == {"2": 216, "3": 576, "4": 216}
    local_separator = full_pool_local_separator()

    script = Path(__file__).resolve()
    theorem = root / "results/GENERAL_MIXED_EDGE_DELETION_RETURN_COMPOSITION_20260813.md"
    return {
        "schema": "general-mixed-edge-deletion-return-composition-audit-v1",
        "status": "ALL_KAPPA_REDUCED_TO_DECORATED_POOL_SEPARATOR",
        "symbolic_checks": symbolic,
        "mixed_interface_case_count": len(records),
        "counts_by_kappa": counts_by_kappa,
        "participant_count_distribution": participant_count_distribution,
        "records": records,
        "local_selected_pool_separator": local_separator,
        "smallest_terminal": "selected-core/hole-pool compensation separator",
        "claim_boundary": (
            "complete kappa=1,2,3 scalar/support interface; no GG inequality "
            "forcing pool feasibility"
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
        "cases": result["mixed_interface_case_count"],
        "smallest_terminal": result["smallest_terminal"],
    }, indent=2))


if __name__ == "__main__":
    main()
