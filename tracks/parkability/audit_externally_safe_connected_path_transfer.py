#!/usr/bin/env python3
"""Audit the externally-safe path lemma and its two frozen exemplars."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        tail,
        transfer_topology,
        value,
    )
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import old_bundles
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        lex_endpoint_succeeds,
        tail,
        transfer_topology,
        value,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints: z3.BoolRef) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def audit_profile(root: Path, source_name: str, escape_name: str) -> dict:
    source_path = root / "results" / source_name
    escape_path = root / "results" / escape_name
    source = json.loads(source_path.read_text())
    escape = json.loads(escape_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = old_bundles()
    allocation = {
        recipient: tuple(goods)
        for recipient, goods in escape["allocation"].items()
    }
    base = {agent: value(values, agent, old[agent]) for agent in AGENTS}
    own = {agent: value(values, agent, allocation[agent]) for agent in AGENTS}
    topology = transfer_topology(old, allocation)
    changed = {
        agent for agent in AGENTS if set(allocation[agent]) != set(old[agent])
    }
    incoming = {agent: 0 for agent in AGENTS}
    outgoing = {agent: 0 for agent in AGENTS}
    for edge in topology["edge_counts"]:
        if edge["source"] in AGENTS and edge["target"] in AGENTS:
            outgoing[edge["source"]] += 1
            incoming[edge["target"]] += 1
    sources = [
        agent for agent in changed
        if outgoing[agent] == 1 and incoming[agent] == 0
    ]
    assert len(sources) == 1
    path_source = sources[0]

    external_safety_failures = []
    for target in changed:
        for observer in AGENTS:
            if observer == target:
                continue
            if tail(values, observer, allocation[target]) > base[observer]:
                external_safety_failures.append([observer, target])

    paid_non_source = {
        agent: own[agent] >= base[agent]
        for agent in changed if agent != path_source
    }
    source_direct_efx = all(
        own[path_source] >= tail(values, path_source, allocation[target])
        for target in AGENTS
    ) and own[path_source] >= value(values, path_source, allocation["_"])

    assert not external_safety_failures
    assert all(paid_non_source.values())
    assert source_direct_efx
    assert lex_endpoint_succeeds(values, old, allocation)
    assert len(topology["nontrivial_components"]) == 1

    return {
        "source": source_name,
        "source_sha256": sha256(source_path),
        "escape": escape_name,
        "escape_sha256": sha256(escape_path),
        "signature": topology["signature"],
        "path_source": path_source,
        "changed_owners": sorted(changed, key=AGENTS.index),
        "external_safety_failures": external_safety_failures,
        "paid_non_source": paid_non_source,
        "source_direct_efx": source_direct_efx,
        "lex_endpoint": True,
        "connected": True,
    }


def run(root: Path) -> dict:
    own, base, target_tail = z3.Reals("own base target_tail")
    external_safety_lifts_through_payment = check_unsat(
        own >= base,
        target_tail <= base,
        z3.Not(own >= target_tail),
    )

    records = [
        audit_profile(
            root,
            "two_external_weighted_hall_hardened_countermodel.json",
            "two_external_weighted_hall_hardened_countermodel_escape.json",
        ),
        audit_profile(
            root,
            "two_external_weighted_hall_radius2_hardened_countermodel.json",
            "two_external_weighted_hall_radius2_hardened_countermodel_escape.json",
        ),
    ]
    assert {record["signature"] for record in records} == {
        "c->r:1",
        "q->r:1;r->c:2",
    }

    script = Path(__file__).resolve()
    theorem = root / "results/EXTERNALLY_SAFE_CONNECTED_PATH_TRANSFER_LEMMA_20260811.md"
    return {
        "schema": "externally-safe-connected-path-transfer-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": {
            "external_safety_lifts_through_weak_payment": (
                external_safety_lifts_through_payment
            ),
        },
        "profile_records": records,
        "claim_boundary": (
            "cap-free sufficient-condition lemma with two exact exemplars; "
            "terminal-polarity packet selection is not proved"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/externally_safe_connected_path_transfer_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
