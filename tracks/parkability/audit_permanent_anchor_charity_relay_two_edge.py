#!/usr/bin/env python3
"""Independent audit of the permanent-anchor charity-relay theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/PERMANENT_ANCHOR_CHARITY_RELAY_TWO_EDGE_THEOREM_20260814.md"
COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"


def _edges(source, target):
    holder = {good: owner for owner, bundle in source.items() for good in bundle}
    return {
        (holder[good], owner)
        for owner, bundle in target.items()
        for good in bundle
        if holder[good] != owner
    }


def _case(anchor_holder_is_sacrifice):
    q = "d" if anchor_holder_is_sacrifice else "q"
    owners = ("r", "q", "d", "s")
    current = {owner: {f"res_{owner}"} for owner in owners}
    current[q].add("A")
    current["charity"] = {"p"}

    base = {owner: set(bundle) for owner, bundle in current.items()}
    base[q].remove("A")
    base["r"].add("A")

    r_alloc = {owner: set(bundle) for owner, bundle in base.items()}
    d_alloc = {owner: set(bundle) for owner, bundle in base.items()}
    r_alloc["charity"].remove("p")
    r_alloc["r"].add("p")
    d_alloc["charity"].remove("p")
    d_alloc["d"].add("p")

    goods = set().union(*current.values())
    for allocation in (r_alloc, d_alloc):
        assert set().union(*allocation.values()) == goods
        assert sum(map(len, allocation.values())) == len(goods)

    r_edges = _edges(current, r_alloc)
    d_edges = _edges(current, d_alloc)
    assert r_edges == {(q, "r"), ("charity", "r")}
    assert d_edges == {(q, "r"), ("charity", "d")}
    assert _edges(d_alloc, r_alloc) == {("d", "r")}
    return {
        "anchor_holder_equals_sacrifice": anchor_holder_is_sacrifice,
        "root_endpoint_edges": sorted([list(edge) for edge in r_edges]),
        "sacrifice_endpoint_edges": sorted([list(edge) for edge in d_edges]),
    }


def _linear_audit():
    x, anchor, residual, p_r = z3.Reals("x anchor residual p_r")
    strict = z3.SolverFor("QF_LRA")
    strict.add(
        x >= 0,
        anchor > x,
        residual >= 0,
        p_r > 0,
        z3.Or(anchor + residual <= x, anchor + residual + p_r <= x),
    )
    strict_status = str(strict.check())
    assert strict_status == "unsat"

    residual_d, p_d, floor_d, after_return = z3.Reals(
        "residual_d p_d floor_d after_return"
    )
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        residual_d >= 0,
        p_d > 0,
        floor_d == residual_d + p_d,
        after_return == residual_d,
        z3.Or(
            after_return >= floor_d,
            floor_d - after_return != p_d,
            floor_d - after_return <= 0,
        ),
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"
    return strict_status, capture_status


def run(output: Path):
    cases = [_case(False), _case(True)]
    strict_status, capture_status = _linear_audit()
    result = {
        "schema": "permanent-anchor-charity-relay-two-edge-audit-v1",
        "status": "CONDITIONAL_COMPOSITION_AUDIT_PASSED",
        "cases": cases,
        "physical_conservation": True,
        "maximum_support_provenance_edges": 2,
        "relay_edge_from_sacrifice_to_root": ["d", "r"],
        "canonical_cancellation_restores_sacrifice_endpoint": True,
        "strict_root_negation_status": strict_status,
        "reset_floor_capture_negation_status": capture_status,
        "retired_packet": ["p"],
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Checks both anchor-holder/sacrifice incidences, conservation, "
            "two-edge provenance, strict root, reset deficit, and exact "
            "cancellation. It does not independently certify that the floor "
            "reset and staged relay are admitted G0--G10 operations or "
            "reprove the imported collision theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
