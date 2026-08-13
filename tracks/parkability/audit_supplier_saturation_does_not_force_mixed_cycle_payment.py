#!/usr/bin/env python3
"""Exact audit of the anchored supplier-saturated mixed-cycle falsifier."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3


AGENTS = ("r", "q", "a", "b")
GOODS = ("kr", "d1", "d2", "ka", "kb", "rr", "rq", "ra", "rb")
OLD_CORES = {"r": ("kr",), "a": ("ka",), "b": ("kb",)}
DECORATED = ("d1", "d2")
RESIDUALS = {agent: ("r" + agent,) for agent in AGENTS}
BASE = {agent: Fraction(10) for agent in AGENTS}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valuation_table() -> dict[str, dict[str, Fraction]]:
    tiny = Fraction(1, 10)
    values = {agent: {good: tiny for good in GOODS} for agent in AGENTS}

    # Old source margins.
    values["r"]["kr"] = Fraction(11)
    values["a"]["ka"] = Fraction(11)
    values["b"]["kb"] = Fraction(11)

    # D is inclusion-minimal current-desired for q.
    values["q"].update({"d1": Fraction(7), "d2": Fraction(6),
                        "kr": Fraction(11), "rq": Fraction(1)})

    # a is the decorated target owner and the unpaid observer.
    values["a"].update({"d1": Fraction(12), "d2": Fraction(1)})

    # Current target utilities for r and b remain above base.
    values["r"].update({"kb": Fraction(12), "rr": Fraction(1, 10)})
    values["b"].update({"ka": Fraction(12), "rb": Fraction(1, 10)})
    return values


def value(values, agent: str, bundle) -> Fraction:
    return sum((values[agent][good] for good in bundle), Fraction())


def tau(values, agent: str, bundle) -> Fraction:
    bundle = tuple(bundle)
    if len(bundle) <= 1:
        return Fraction()
    return value(values, agent, bundle) - min(values[agent][good] for good in bundle)


def run(root: Path) -> dict:
    values = valuation_table()
    targets = {
        "r": ("kb", "rr"),
        "q": ("kr", "rq"),
        "a": ("d1", "d2", "ra"),
        "b": ("ka", "rb"),
    }
    current = {agent: value(values, agent, targets[agent]) for agent in AGENTS}

    assert all(current[agent] >= BASE[agent] for agent in AGENTS)
    assert value(values, "q", DECORATED) > current["q"]
    assert all(
        value(values, "q", DECORATED[:index] + DECORATED[index + 1 :])
        <= current["q"]
        for index in range(len(DECORATED))
    )
    assert all(tau(values, observer, DECORATED) <= current[observer] for observer in AGENTS)
    assert all(
        value(values, source, core) > BASE[source]
        for source, core in OLD_CORES.items()
    )
    assert all(
        tau(values, observer, core) <= BASE[observer]
        for core in OLD_CORES.values()
        for observer in AGENTS
    )

    residual_pool = tuple(good for residual in RESIDUALS.values() for good in residual)
    blocked_with_full_pool = value(values, "a", OLD_CORES["a"] + residual_pool)
    decorated_threshold = tau(values, "a", DECORATED)
    assert blocked_with_full_pool < decorated_threshold

    rotated = {
        "r": OLD_CORES["r"] + RESIDUALS["r"],
        "q": DECORATED + RESIDUALS["q"],
        "a": OLD_CORES["a"] + RESIDUALS["a"],
        "b": OLD_CORES["b"] + RESIDUALS["b"],
    }
    assert all(value(values, agent, rotated[agent]) > BASE[agent] for agent in AGENTS)
    assert value(values, "a", rotated["a"]) < tau(values, "a", rotated["q"])

    # Exact residual census. Cores remain fixed; each residual may go to one
    # of four owners or charity. No assignment can make the resulting
    # allocation EFX while keeping all owners strictly above base.
    feasible = []
    recipients = (*AGENTS, None)
    for code in range(len(recipients) ** len(residual_pool)):
        bundles = {
            "r": set(OLD_CORES["r"]),
            "q": set(DECORATED),
            "a": set(OLD_CORES["a"]),
            "b": set(OLD_CORES["b"]),
        }
        cursor = code
        for good in residual_pool:
            recipient = recipients[cursor % len(recipients)]
            cursor //= len(recipients)
            if recipient is not None:
                bundles[recipient].add(good)
        if not all(value(values, agent, bundles[agent]) > BASE[agent] for agent in AGENTS):
            continue
        if all(
            value(values, observer, bundles[observer])
            >= tau(values, observer, bundles[target])
            for observer in AGENTS
            for target in AGENTS
        ):
            feasible.append({agent: sorted(bundle) for agent, bundle in bundles.items()})
    assert not feasible

    outgoing, residual, incoming, threshold = z3.Reals(
        "outgoing residual incoming threshold"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(
        outgoing + residual < threshold,
        threshold <= incoming + residual,
        z3.Not(incoming > outgoing),
    )
    assert solver.check() == z3.unsat

    script = Path(__file__).resolve()
    theorem = root / "results/SUPPLIER_SATURATION_DOES_NOT_FORCE_MIXED_CYCLE_PAYMENT_20260813.md"
    return {
        "schema": "supplier-saturation-mixed-cycle-payment-refutation-v1",
        "status": "GENERIC_SUPPLIER_SATURATED_PAYMENT_IMPLICATION_REFUTED",
        "cycle": ["r->q:K_r(old anchor)", "q->a:D(decorated)",
                  "a->b:K_a(old)", "b->r:K_b(old)"],
        "supplier_closure": list(AGENTS),
        "permanent_anchor_retained": True,
        "values": {
            agent: {good: str(number) for good, number in row.items()}
            for agent, row in values.items()
        },
        "base_floors": {agent: str(number) for agent, number in BASE.items()},
        "current_targets": {agent: list(bundle) for agent, bundle in targets.items()},
        "current_utilities": {agent: str(number) for agent, number in current.items()},
        "decorated_core": list(DECORATED),
        "decorated_source_value": str(value(values, "q", DECORATED)),
        "blocked_observer_threshold": str(decorated_threshold),
        "blocked_observer_full_residual_value": str(blocked_with_full_pool),
        "residual_assignment_count": len(recipients) ** len(residual_pool),
        "residual_only_efx_payment_count": len(feasible),
        "row_cancellation_forces_incoming_over_outgoing": True,
        "smallest_missing_operation": (
            "decorated-head exchange: split/replace D, change its source, or "
            "release another selected core while preserving q's current floor"
        ),
        "claim_boundary": (
            "refutes payment from mixed response safety plus supplier saturation; "
            "not a globally recurrent or globally lex-maximal GG countermodel"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
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
        "residual_assignments": result["residual_assignment_count"],
        "efx_payments": result["residual_only_efx_payment_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
