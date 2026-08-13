#!/usr/bin/env python3
"""Independent replay of the supplier-saturated payment countermodel."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "a", "b")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_table(raw):
    return {
        agent: {good: Fraction(number) for good, number in row.items()}
        for agent, row in raw.items()
    }


def value(values, agent, bundle):
    return sum((values[agent][good] for good in bundle), Fraction())


def threshold(values, agent, bundle):
    bundle = tuple(bundle)
    if len(bundle) <= 1:
        return Fraction()
    return value(values, agent, bundle) - min(values[agent][good] for good in bundle)


def run(root: Path) -> dict:
    source_path = root / "results/supplier_saturation_does_not_force_mixed_cycle_payment_audit.json"
    source = json.loads(source_path.read_text())
    values = parse_table(source["values"])
    floors = {agent: Fraction(number) for agent, number in source["base_floors"].items()}
    targets = {agent: tuple(bundle) for agent, bundle in source["current_targets"].items()}
    current = {agent: value(values, agent, targets[agent]) for agent in AGENTS}
    D = ("d1", "d2")
    old = {"r": ("kr",), "a": ("ka",), "b": ("kb",)}
    residuals = ("rr", "rq", "ra", "rb")

    checks = {
        "all_values_positive": all(number > 0 for row in values.values() for number in row.values()),
        "current_state_paid": all(current[agent] >= floors[agent] for agent in AGENTS),
        "decorated_source_strict": value(values, "q", D) > current["q"],
        "decorated_source_minimal": all(
            value(values, "q", (good,)) <= current["q"] for good in D
        ),
        "decorated_current_safe": all(
            threshold(values, agent, D) <= current[agent] for agent in AGENTS
        ),
        "old_cores_desired": all(
            value(values, source_agent, core) > floors[source_agent]
            for source_agent, core in old.items()
        ),
        "old_cores_base_safe": all(
            threshold(values, observer, core) <= floors[observer]
            for core in old.values() for observer in AGENTS
        ),
        "anchor_retained": source["permanent_anchor_retained"] is True,
        "supplier_closure_all_owners": set(source["supplier_closure"]) == set(AGENTS),
    }
    assert all(checks.values())

    recipients = (*AGENTS, None)
    feasible = 0
    floor_feasible = 0
    for code in range(len(recipients) ** len(residuals)):
        cells = {
            "r": {"kr"},
            "q": set(D),
            "a": {"ka"},
            "b": {"kb"},
        }
        cursor = code
        for good in residuals:
            recipient = recipients[cursor % len(recipients)]
            cursor //= len(recipients)
            if recipient is not None:
                cells[recipient].add(good)
        if not all(value(values, agent, cells[agent]) > floors[agent] for agent in AGENTS):
            continue
        floor_feasible += 1
        if all(
            value(values, observer, cells[observer])
            >= threshold(values, observer, cells[target])
            for observer in AGENTS for target in AGENTS
        ):
            feasible += 1
    assert feasible == 0
    assert len(recipients) ** len(residuals) == 625
    assert value(values, "a", old["a"] + residuals) == Fraction(57, 5)
    assert threshold(values, "a", D) == 12

    script = Path(__file__).resolve()
    return {
        "schema": "supplier-saturated-payment-refutation-independent-audit-v1",
        "status": "INDEPENDENT_EXACT_REPLAY_PASSED",
        "checks": checks,
        "residual_assignment_count": 625,
        "strict_floor_feasible_assignment_count": floor_feasible,
        "residual_only_efx_payment_count": feasible,
        "blocked_observer_full_pool_value": "57/5",
        "blocked_observer_threshold": "12",
        "implementation_relation": (
            "independent parser and allocation census; does not import the primary audit"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "assignments": result["residual_assignment_count"],
        "efx_payments": result["residual_only_efx_payment_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
