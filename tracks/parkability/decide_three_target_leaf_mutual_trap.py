#!/usr/bin/env python3
"""Decide the smallest additive realization of the leaf-mutual hub trap."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


AGENTS = ("h", "r", "s", "q")
GOODS = ("hc1", "hc2", "a", "b", "r1", "r2", "z", "q1", "q2", "f")
BASE = {
    "h": ("hc1", "hc2", "a", "b"),
    "r": ("r1", "r2"),
    "s": ("z",),
    "q": ("q1", "q2"),
}
NEW = {
    "h": ("hc1", "hc2", "f"),
    "r": ("r1", "r2", "a"),
    "s": ("z", "b"),
    "q": ("q1", "q2"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def total(values, observer, bundle):
    return z3.Sum(*(values[observer, good] for good in bundle))


def minimum(values, observer, bundle):
    current = values[observer, bundle[0]]
    for good in bundle[1:]:
        current = z3.If(current <= values[observer, good], current, values[observer, good])
    return current


def tail(values, observer, bundle):
    if len(bundle) == 1:
        return z3.IntVal(0)
    return total(values, observer, bundle) - minimum(values, observer, bundle)


def concrete_total(model_values, observer, bundle):
    return sum(model_values[observer][good] for good in bundle)


def concrete_tail(model_values, observer, bundle):
    if len(bundle) == 1:
        return 0
    entries = [model_values[observer][good] for good in bundle]
    return sum(entries) - min(entries)


def audit_frozen(payload) -> bool:
    cap = payload["cap"]
    model_values = payload["values"]
    if payload["status"] != "sat" or model_values is None:
        return False
    if any(
        not 1 <= model_values[agent][good] <= cap
        for agent in AGENTS
        for good in GOODS
    ):
        return False
    for observer in AGENTS:
        own = concrete_total(model_values, observer, BASE[observer])
        if own < model_values[observer]["f"]:
            return False
        if any(own < concrete_tail(model_values, observer, BASE[target]) for target in AGENTS):
            return False
    if model_values["h"]["f"] <= model_values["h"]["a"] + model_values["h"]["b"]:
        return False
    strict_walls = {
        "r_to_s": concrete_tail(model_values, "r", NEW["s"])
        - concrete_total(model_values, "r", NEW["r"]),
        "s_to_r": concrete_tail(model_values, "s", NEW["r"])
        - concrete_total(model_values, "s", NEW["s"]),
        "r_to_h": concrete_tail(model_values, "r", NEW["h"])
        - concrete_total(model_values, "r", NEW["r"]),
        "s_to_h": concrete_tail(model_values, "s", NEW["h"])
        - concrete_total(model_values, "s", NEW["s"]),
    }
    hub_safety = {
        leaf: concrete_total(model_values, "h", NEW["h"])
        - concrete_tail(model_values, "h", NEW[leaf])
        for leaf in ("r", "s")
    }
    return (
        min(strict_walls.values()) > 0
        and min(hub_safety.values()) >= 0
        and strict_walls == payload["diagnostics"]["strict_wall_margins"]
        and hub_safety == payload["diagnostics"]["hub_to_leaf_safety_slacks"]
    )


def run(cap: int) -> dict:
    values = {
        (agent, good): z3.Int(f"v_{agent}_{good}") for agent in AGENTS for good in GOODS
    }
    solver = z3.Solver()
    for value in values.values():
        solver.add(value >= 1, value <= cap)

    for observer in AGENTS:
        own = total(values, observer, BASE[observer])
        solver.add(own >= values[observer, "f"])
        for target in AGENTS:
            solver.add(own >= tail(values, observer, BASE[target]))

    solver.add(values["h", "f"] > values["h", "a"] + values["h", "b"])

    solver.add(
        total(values, "r", NEW["r"]) < tail(values, "r", NEW["s"]),
        total(values, "s", NEW["s"]) < tail(values, "s", NEW["r"]),
        total(values, "r", NEW["r"]) < tail(values, "r", NEW["h"]),
        total(values, "s", NEW["s"]) < tail(values, "s", NEW["h"]),
    )

    solver.add(
        total(values, "h", NEW["h"]) >= tail(values, "h", NEW["r"]),
        total(values, "h", NEW["h"]) >= tail(values, "h", NEW["s"]),
    )

    status = solver.check()
    model_values = None
    diagnostics = None
    if status == z3.sat:
        model = solver.model()
        model_values = {
            agent: {good: model.eval(values[agent, good]).as_long() for good in GOODS}
            for agent in AGENTS
        }
        diagnostics = {
            "minimum_base_efx_slack": min(
                concrete_total(model_values, observer, BASE[observer])
                - concrete_tail(model_values, observer, BASE[target])
                for observer in AGENTS
                for target in AGENTS
            ),
            "minimum_base_charity_slack": min(
                concrete_total(model_values, observer, BASE[observer])
                - model_values[observer]["f"]
                for observer in AGENTS
            ),
            "hub_owner_gain": (
                concrete_total(model_values, "h", NEW["h"])
                - concrete_total(model_values, "h", BASE["h"])
            ),
            "strict_wall_margins": {
                "r_to_s": (
                    concrete_tail(model_values, "r", NEW["s"])
                    - concrete_total(model_values, "r", NEW["r"])
                ),
                "s_to_r": (
                    concrete_tail(model_values, "s", NEW["r"])
                    - concrete_total(model_values, "s", NEW["s"])
                ),
                "r_to_h": (
                    concrete_tail(model_values, "r", NEW["h"])
                    - concrete_total(model_values, "r", NEW["r"])
                ),
                "s_to_h": (
                    concrete_tail(model_values, "s", NEW["h"])
                    - concrete_total(model_values, "s", NEW["s"])
                ),
            },
            "hub_to_leaf_safety_slacks": {
                leaf: (
                    concrete_total(model_values, "h", NEW["h"])
                    - concrete_tail(model_values, "h", NEW[leaf])
                )
                for leaf in ("r", "s")
            },
        }

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "three-target-leaf-mutual-trap-v1",
        "status": str(status),
        "cap": cap,
        "base_allocation": BASE,
        "candidate_allocation": NEW,
        "values": model_values,
        "diagnostics": diagnostics,
        "claim_boundary": (
            "tests compatibility of base EFX, charity dominance, hub improvement, the four hard-trap "
            "walls, and absence of hub-to-leaf walls; it omits the flower champion constraints and "
            "does not refute the hub selector or EFX"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cap", type=int, default=30)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.cap)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cap": result["cap"]}, indent=2))


if __name__ == "__main__":
    main()
