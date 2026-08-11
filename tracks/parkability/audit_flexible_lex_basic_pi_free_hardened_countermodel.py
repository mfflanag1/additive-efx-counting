#!/usr/bin/env python3
"""Exact audit of the hardened basic-PI-free radius-three obstruction."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_lex_radius3_hardened_countermodel import subset_sum_count
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        validate_flower_master,
    )
    from .decide_flexible_later_owner_connected_transfer import enumerate_connected
    from .harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from .harden_flexible_lex_radius3_countermodel import live_polarity
except ImportError:
    from audit_flexible_lex_radius3_hardened_countermodel import subset_sum_count
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        validate_flower_master,
    )
    from decide_flexible_later_owner_connected_transfer import enumerate_connected
    from harden_flexible_lex_basic_pi_free_countermodel import basic_pi_free
    from harden_flexible_lex_radius3_countermodel import live_polarity


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(source_path, escape_path, response_path):
    source = json.loads(source_path.read_text())
    if source.get("status") != "HARDENED_COUNTERMODEL":
        raise ValueError("source is not a hardened countermodel")
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(values)
    assert live_polarity(values)
    assert basic_pi_free(values, old)
    expected_subsets = 1 << len(values[AGENTS[0]])
    subset_counts = {
        agent: subset_sum_count(values[agent]) for agent in AGENTS
    }
    assert set(subset_counts.values()) == {expected_subsets}

    candidates = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    radius_counts = Counter()
    lex_count = 0
    later_count = 0
    for allocation in candidates:
        radius_counts[len(transfer_topology(old, allocation)["moved_goods"])] += 1
        lex_count += lex_endpoint_succeeds(values, old, allocation)
        later_count += endpoint_succeeds(values, old, allocation)
    assert radius_counts == Counter({1: 72, 2: 1770, 3: 39552})
    assert lex_count == later_count == 0

    escape = json.loads(escape_path.read_text())
    allocation = escape["allocation"]
    assert escape["status"] == "FOUND" and escape["objective"] == "later"
    assert endpoint_succeeds(values, old, allocation)
    topology = transfer_topology(old, allocation)
    assert topology == escape["topology"]
    assert len(topology["moved_goods"]) == 4
    assert len(topology["nontrivial_components"]) == 1
    response = json.loads(response_path.read_text())
    assert response["status"] == "NO_INTERNAL_SDR"
    assert response["incoming_disjoint"] and response["all_incoming_supplied"]

    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-basic-pi-free-hardened-countermodel-audit-v1",
        "status": "VERIFIED",
        "positive_additive": True,
        "flower_master_valid": True,
        "live_polarity_valid": True,
        "subset_sum_injective": True,
        "subset_sum_counts": subset_counts,
        "basic_pi_free": True,
        "basic_pi_free_scope": (
            "no genuine self-champion, ordinary envy cycle, or simple cycle "
            "with exactly one genuine champion edge"
        ),
        "connected_candidate_counts": {
            str(radius): radius_counts[radius] for radius in sorted(radius_counts)
        },
        "connected_candidate_total": len(candidates),
        "lex_endpoint_count": lex_count,
        "later_owner_endpoint_count": later_count,
        "minimum_connected_later_owner_radius": 4,
        "radius4_topology": topology,
        "radius4_response_hall_status": response["status"],
        "claim_boundary": (
            "solver-independent exact-Fraction verification of a positive "
            "subset-sum-injective full-capture flower with no basic PI cycle "
            "and no connected radius-three lex endpoint; generalized PI-freeness "
            "and global lex maximality remain unproved, so this is not a literal "
            "counterexample to the globally hard-state theorem"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "escape": str(escape_path.relative_to(root)),
            "escape_sha256": sha256(escape_path),
            "response": str(response_path.relative_to(root)),
            "response_sha256": sha256(response_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--escape", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.source.resolve(), args.escape.resolve(), args.response.resolve()
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_total": result["connected_candidate_total"],
        "lex_endpoint_count": result["lex_endpoint_count"],
        "basic_pi_free": result["basic_pi_free"],
    }, indent=2))


if __name__ == "__main__":
    main()
