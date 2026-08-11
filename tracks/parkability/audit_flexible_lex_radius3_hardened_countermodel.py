#!/usr/bin/env python3
"""Audit the hardened radius-three flower countermodel exactly."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        validate_flower_master,
        value,
    )
    from .decide_flexible_later_owner_connected_transfer import enumerate_connected
except ImportError:
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        endpoint_succeeds,
        lex_endpoint_succeeds,
        transfer_topology,
        validate_flower_master,
        value,
    )
    from decide_flexible_later_owner_connected_transfer import enumerate_connected


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subset_sum_count(row):
    denominator = math.lcm(*(amount.denominator for amount in row.values()))
    integers = [int(amount * denominator) for amount in row.values()]
    sums = {0}
    for amount in integers:
        extended = {current + amount for current in sums}
        assert sums.isdisjoint(extended)
        sums |= extended
    return len(sums)


def verify_escape(path, values, old, objective):
    payload = json.loads(path.read_text())
    assert payload["status"] == "FOUND"
    assert payload["objective"] == objective
    allocation = payload["allocation"]
    succeeds = lex_endpoint_succeeds if objective == "lex" else endpoint_succeeds
    assert succeeds(values, old, allocation)
    topology = transfer_topology(old, allocation)
    assert topology == payload["topology"]
    assert len(topology["moved_goods"]) == 4
    assert len(topology["nontrivial_components"]) == 1
    root = Path(__file__).resolve().parents[2]
    return {
        "source": str(path.relative_to(root)),
        "source_sha256": sha256(path),
        "topology": topology,
    }


def run(source_path, lex_escape_path, later_escape_path):
    source = json.loads(source_path.read_text())
    if source.get("status") != "HARDENED_COUNTERMODEL":
        raise ValueError("source is not a hardened countermodel")
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in source["values"].items()
    }
    old = validate_flower_master(values)
    bottom_r = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
    bottom_q = ("ar_bq_0", "ar_bq_1")
    assert value(values, "r", bottom_r) >= values["r"]["f"]
    assert values["r"]["f"] > value(values, "r", bottom_q)
    assert value(values, "q", bottom_q) > value(values, "q", bottom_r)
    subset_counts = {
        agent: subset_sum_count(values[agent]) for agent in AGENTS
    }
    expected_subsets = 1 << len(values[AGENTS[0]])
    assert set(subset_counts.values()) == {expected_subsets}

    candidates = enumerate_connected(
        old, radius=3, rooted=False, structural_reductions=False
    )
    radius_counts = Counter()
    later_successes = 0
    lex_successes = 0
    for allocation in candidates:
        radius = len(transfer_topology(old, allocation)["moved_goods"])
        radius_counts[radius] += 1
        later_successes += endpoint_succeeds(values, old, allocation)
        lex_successes += lex_endpoint_succeeds(values, old, allocation)
    assert radius_counts == Counter({1: 72, 2: 1770, 3: 39552})
    assert later_successes == 0
    assert lex_successes == 0
    lex_escape = verify_escape(lex_escape_path, values, old, "lex")
    later_escape = verify_escape(later_escape_path, values, old, "later")
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-radius3-hardened-countermodel-audit-v1",
        "status": "VERIFIED",
        "positive_additive": True,
        "flower_master_valid": True,
        "live_polarity_valid": True,
        "subset_sum_injective": True,
        "subset_sum_counts": subset_counts,
        "connected_candidate_counts": {
            str(radius): radius_counts[radius] for radius in sorted(radius_counts)
        },
        "connected_candidate_total": len(candidates),
        "later_owner_endpoint_count": later_successes,
        "lex_endpoint_count": lex_successes,
        "minimum_connected_lex_radius": 4,
        "minimum_connected_later_owner_radius": 4,
        "lex_radius4_escape": lex_escape,
        "later_owner_radius4_escape": later_escape,
        "claim_boundary": (
            "solver-independent exact-Fraction verification of a positive "
            "subset-sum-injective bounded representative hard-flower valuation "
            "with no connected EFX lex improvement through radius three; it "
            "refutes the local at-most-three-good lemma under these premises, "
            "not complete EFX existence or arbitrary transfer components"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--lex-escape", type=Path, required=True)
    parser.add_argument("--later-escape", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(
        args.source.resolve(),
        args.lex_escape.resolve(),
        args.later_escape.resolve(),
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_total": result["connected_candidate_total"],
        "lex_endpoint_count": result["lex_endpoint_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
