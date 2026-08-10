#!/usr/bin/env python3
"""Audit a frozen refutation of fixed later-owner lex completion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import (
        AGENTS,
        BASE,
        candidate_covers,
    )
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import (
        AGENTS,
        BASE,
        candidate_covers,
    )


COMPONENT_BUNDLES = {
    "A_q": ("aq_tq", "aq_br"),
    "A_r": ("ar_tr", "ar_bq"),
    "D_r": ("aq_tq", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "X_q": ("aq_tq", "ar_bq"),
    "X_c": ("tc", "bc"),
    "Z": ("z",),
}
OLD_COMPONENTS = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atom_names(component: str) -> tuple[str, ...]:
    if component in ("f", "z"):
        return (component,)
    return tuple(f"{component}_{index}" for index in range(2))


def add(values: dict[str, dict[str, Fraction]], agent: str, goods) -> Fraction:
    return sum((values[agent][good] for good in goods), Fraction(0))


def tail(values: dict[str, dict[str, Fraction]], agent: str, goods) -> Fraction:
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return add(values, agent, goods) - min(values[agent][good] for good in goods)


def validate_flower_cell(values, bundles, old) -> dict:
    base = {agent: add(values, agent, old[agent]) for agent in AGENTS}
    assert all(amount > 0 for row in values.values() for amount in row.values())
    for agent in AGENTS:
        for goods in bundles.values():
            assert tail(values, agent, goods) <= base[agent]
        assert values[agent]["f"] <= base[agent]
        assert add(values, agent, bundles["X_c"]) <= base[agent]
    for name, source in {
        "D_r": "r",
        "D_q": "q",
        "D_c": "r",
        "Z": "c",
        "A_q": "c",
        "A_r": "c",
    }.items():
        assert add(values, source, bundles[name]) > base[source]

    checked_covers = 0
    covers = candidate_covers("r", "c", "c", "c", tuple(AGENTS))
    for cover in (record for record in covers if record["unpaid_agent"] is not None):
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        assert any(
            add(values, unpaid, bundles[payment])
            < tail(values, unpaid, bundles[cover["assignment"][target]])
            for target in AGENTS
            if target != unpaid
        )
        checked_covers += 1
    return {"base_values": {agent: str(amount) for agent, amount in base.items()},
            "failed_common_safe_covers_checked": checked_covers}


def validate_flexible_escape(values, atoms, old, allocation) -> dict:
    assert set(allocation) == set(AGENTS + ("_",))
    assigned = [good for recipient in AGENTS + ("_",) for good in allocation[recipient]]
    assert len(assigned) == len(atoms) and set(assigned) == set(atoms)
    base = {agent: add(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: add(values, agent, allocation[agent]) for agent in AGENTS}
    for observer in AGENTS:
        for target in AGENTS:
            assert own[observer] >= tail(values, observer, allocation[target])
        assert own[observer] >= add(values, observer, allocation["_"])
    assert own["r"] >= base["r"]
    assert own["q"] > base["q"]
    base_owner = {good: agent for agent in AGENTS for good in old[agent]}
    base_owner["f"] = "_"
    moved = sum(
        base_owner[good] != recipient
        for recipient in AGENTS + ("_",)
        for good in allocation[recipient]
    )
    return {
        "status": "VERIFIED_EFX_LEX_ESCAPE",
        "moved_goods": moved,
        "owner_utilities": {agent: str(amount) for agent, amount in own.items()},
    }


def has_boolean_completion(values, atoms, old, released):
    released = tuple(released)
    label = "__".join(released)
    recipients = AGENTS + ("_",)
    assigned = {
        (good, recipient): z3.Bool(f"has_{label}_{good}_{recipient}")
        for good in atoms
        for recipient in recipients
    }
    solver = z3.Solver()
    for good in atoms:
        solver.add(z3.PbEq([(assigned[good, recipient], 1) for recipient in recipients], 1))
        if good in (set(old["q"]) - set(released)) | {"f"}:
            solver.add(assigned[good, "q"])
        else:
            solver.add(z3.Not(assigned[good, "q"]))

    def amount(observer, recipient):
        return z3.Sum(*(
            z3.If(assigned[good, recipient], z3.RealVal(str(values[observer][good])), 0)
            for good in atoms
        ))

    base_r = sum((values["r"][good] for good in old["r"]), Fraction(0))
    solver.add(amount("r", "r") >= z3.RealVal(str(base_r)))
    for observer in AGENTS:
        own = amount(observer, observer)
        for target in AGENTS:
            total = amount(observer, target)
            for good in atoms:
                solver.add(z3.Implies(
                    assigned[good, target],
                    own >= total - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(own >= amount(observer, "_"))
    return solver.check()


def run(witness_path: Path, selector: str) -> dict:
    payload = json.loads(witness_path.read_text())
    assert payload["status"] == "SAT_COUNTEREXAMPLE"
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    components = tuple(dict.fromkeys(
        component for parts in COMPONENT_BUNDLES.values() for component in parts
    ))
    atoms = tuple(good for component in components for good in atom_names(component))
    bundles = {
        name: tuple(good for component in parts for good in atom_names(component))
        for name, parts in COMPONENT_BUNDLES.items()
    }
    old = {
        agent: tuple(good for component in parts for good in atom_names(component))
        for agent, parts in OLD_COMPONENTS.items()
    }
    assert set(atoms) == set(values[AGENTS[0]])
    flower = validate_flower_cell(values, bundles, old)
    flexible_escape = validate_flexible_escape(
        values, atoms, old, payload["flexible_escape"]
    )
    eligible_singletons = tuple(
        (good,) for good in old["q"] if values["q"]["f"] > values["q"][good]
    )
    if selector == "singleton":
        eligible = eligible_singletons
        assert [packet[0] for packet in eligible] == payload["eligible"]
    else:
        eligible_all = tuple(
            packet
            for size in range(1, len(old["q"]))
            for packet in itertools.combinations(old["q"], size)
            if values["q"]["f"] > add(values, "q", packet)
        )
        eligible = tuple(
            packet for packet in eligible_all
            if not any(set(packet) < set(other) for other in eligible_all)
        )
        assert [list(packet) for packet in eligible] == payload["eligible"]
    completion_checks = {
        "__".join(packet): str(has_boolean_completion(values, atoms, old, packet))
        for packet in eligible
    }
    assert set(completion_checks.values()) == {"unsat"}
    return {
        "schema": "fixed-replacement-lex-completion-refutation-audit-v1",
        "status": "VERIFIED_REFUTATION",
        "solver": f"Z3 {z3.get_version_string()}",
        "flower_cell": flower,
        "flexible_escape": flexible_escape,
        "selector": selector,
        "eligible_packets": [list(packet) for packet in eligible],
        "boolean_completion_checks": completion_checks,
        "claim_boundary": (
            f"refutes the fixed later-owner bundle {selector} lex-completion "
            "selector in one "
            "bounded full-capture flower cell; it does not refute EFX existence or "
            "the adaptive dependency-termination target"
        ),
        "provenance": {
            "witness": str(witness_path),
            "witness_sha256": sha256(witness_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selector", choices=("singleton", "maximal-packet"), required=True)
    args = parser.parse_args()
    result = run(args.witness.resolve(), args.selector)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
