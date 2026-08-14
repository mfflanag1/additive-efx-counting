#!/usr/bin/env python3
"""Independent audit of the rank-three matching charity-relay theorem."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
THEOREM = ROOT / "results/RANK_THREE_MATCHING_CHARITY_RELAY_FOUR_EDGE_THEOREM_20260814.md"
COLLISION_COMMIT = "34709c9ce22dbde23a5fa381a2ccea7898dfe1ca"
OWNERS = ("r", "q", "d", "s")
SOURCES = ("r", "q", "s")


def _rotate(targets):
    current = {owner: {f"res_{owner}", f"core_{owner}"} for owner in OWNERS}
    current["charity"] = {"p"}
    target_core = {target: f"core_{target}" for target in targets}
    incoming = dict(zip(SOURCES, (target_core[target] for target in targets)))
    rotated = {}
    for owner in OWNERS:
        bundle = set(current[owner])
        if owner in target_core:
            bundle.remove(target_core[owner])
        if owner in incoming:
            bundle.add(incoming[owner])
        rotated[owner] = bundle
    rotated["charity"] = {"p"}
    return current, rotated


def _edges(source, target):
    holder = {good: owner for owner, bundle in source.items() for good in bundle}
    return {
        (holder[good], owner)
        for owner, bundle in target.items()
        for good in bundle
        if holder[good] != owner
    }


def _combinatorial_audit():
    records = []
    for targets in itertools.permutations(OWNERS, 3):
        if any(source == target for source, target in zip(SOURCES, targets)):
            continue
        current, rotated = _rotate(targets)
        r_alloc = {owner: set(bundle) for owner, bundle in rotated.items()}
        d_alloc = {owner: set(bundle) for owner, bundle in rotated.items()}
        r_alloc["charity"].remove("p")
        r_alloc["r"].add("p")
        d_alloc["charity"].remove("p")
        d_alloc["d"].add("p")

        goods = set().union(*current.values())
        for allocation in (rotated, r_alloc, d_alloc):
            assert set().union(*allocation.values()) == goods
            assert sum(map(len, allocation.values())) == len(goods)

        matching_edges = {(target, source) for source, target in zip(SOURCES, targets)}
        assert _edges(current, rotated) == matching_edges
        assert _edges(current, r_alloc) == matching_edges | {("charity", "r")}
        assert _edges(current, d_alloc) == matching_edges | {("charity", "d")}
        assert len(_edges(current, r_alloc)) <= 4
        assert len(_edges(current, d_alloc)) <= 4
        assert _edges(d_alloc, r_alloc) == {("d", "r")}

        records.append(
            {
                "targets": list(targets),
                "matching_edges": sorted([list(edge) for edge in matching_edges]),
                "root_endpoint_edge_count": len(_edges(current, r_alloc)),
                "sacrifice_endpoint_edge_count": len(_edges(current, d_alloc)),
            }
        )
    assert records
    return records


def _linear_audit():
    x, core_r, residual_r, p_r = z3.Reals("x core_r residual_r p_r")
    strict = z3.SolverFor("QF_LRA")
    strict.add(
        x >= 0,
        core_r > x,
        residual_r >= 0,
        p_r > 0,
        z3.Or(core_r + residual_r <= x, core_r + residual_r + p_r <= x),
    )
    strict_status = str(strict.check())
    assert strict_status == "unsat"

    b_d, p_d, floor_d, returned_d = z3.Reals("b_d p_d floor_d returned_d")
    capture = z3.SolverFor("QF_LRA")
    capture.add(
        b_d >= 0,
        p_d > 0,
        floor_d == b_d + p_d,
        returned_d == b_d,
        z3.Or(
            returned_d >= floor_d,
            floor_d - returned_d != p_d,
            floor_d - returned_d <= 0,
        ),
    )
    capture_status = str(capture.check())
    assert capture_status == "unsat"
    return strict_status, capture_status


def run(output: Path):
    records = _combinatorial_audit()
    strict_status, capture_status = _linear_audit()
    result = {
        "schema": "rank-three-matching-charity-relay-four-edge-audit-v1",
        "status": "CONDITIONAL_COMPOSITION_AUDIT_PASSED",
        "nonself_rank_three_matchings_checked": len(records),
        "matching_records": records,
        "physical_conservation": True,
        "maximum_support_provenance_edges": 4,
        "relay_edge_from_sacrifice_to_root": ["d", "r"],
        "canonical_cancellation_restores_sacrifice_endpoint": True,
        "strict_root_negation_status": strict_status,
        "reset_floor_capture_negation_status": capture_status,
        "retired_packet": ["p"],
        "imported_collision_theorem_commit": COLLISION_COMMIT,
        "theorem_sha256": hashlib.sha256(THEOREM.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exhausts all nonself rank-three matching target patterns and "
            "checks conservation, provenance-edge counts, strict-root, exact "
            "reset deficit, and cancellation. It does not independently "
            "certify controlled floor-reset admission or reprove the imported "
            "T_L_times collision theorem."
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
