#!/usr/bin/env python3
"""Audit the applicable form-2 exact-repeat rank-growth counterexample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


OWNERS = ("r", "q", "s", "d")
CHARITY = "charity"


def maximum_matching_rank(edges):
    best = 0
    edge_list = sorted(edges)
    for length in range(1, len(edge_list) + 1):
        for chosen in itertools.combinations(edge_list, length):
            if len({source for source, _ in chosen}) != length:
                continue
            if len({target for _, target in chosen}) != length:
                continue
            best = max(best, length)
    return best


def connected(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    frontier = [next(iter(vertices))]
    while frontier:
        vertex = frontier.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        frontier.extend(adjacency[vertex] - seen)
    return seen == vertices


def run(root: Path):
    initial = {
        "r": {"r0", "S", "Dr"},
        "q": {"q0", "R", "Dq"},
        "s": {"s0", "Q"},
        "d": {"d0"},
        CHARITY: {"p"},
    }
    final = {
        "r": {"r0", "p"},
        "q": {"q0", "R", "Dq", "Q"},
        "s": {"s0", "S"},
        "d": {"d0", "Dr"},
        CHARITY: set(),
    }
    goods = set().union(*initial.values())
    assert goods == set().union(*final.values())
    before = {good: holder for holder, bundle in initial.items() for good in bundle}
    after = {good: holder for holder, bundle in final.items() for good in bundle}
    transfers = {
        (before[good], after[good], good)
        for good in goods if before[good] != after[good]
    }
    expected = {
        (CHARITY, "r", "p"), ("r", "d", "Dr"),
        ("r", "s", "S"), ("s", "q", "Q"),
    }
    assert transfers == expected
    support_edges = {(left, right) for left, right, _ in transfers}
    assert len(support_edges) == 4
    assert connected(set(OWNERS) | {CHARITY}, support_edges)
    assert all(initial[holder] != final[holder] for holder in initial)

    values = {
        owner: {good: Fraction(1, 100) for good in goods}
        for owner in OWNERS
    }
    for owner in OWNERS:
        own_value = Fraction(3, 2)
        share = own_value / len(final[owner])
        for good in final[owner]:
            values[owner][good] = share
    special = {
        "r": {"R"}, "q": {"S"}, "s": {"r0"}, "d": {"Dq", "p"}
    }
    for owner, cores in special.items():
        for good in cores:
            values[owner][good] = Fraction(2)

    def value(owner, bundle):
        return sum((values[owner][good] for good in bundle), Fraction())

    own = {owner: value(owner, final[owner]) for owner in OWNERS}
    assert all(amount == Fraction(3, 2) for amount in own.values())
    response_edges = {
        (source, target)
        for source in OWNERS for target in OWNERS if source != target
        if value(source, final[target]) > own[source]
    }
    expected_responses = {
        ("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")
    }
    assert response_edges == expected_responses
    assert maximum_matching_rank(response_edges) == 3
    assert connected(set(OWNERS), response_edges)
    assert all(value(owner, {good}) > own[owner]
               for owner, cores in special.items() for good in cores)
    assert all(value(observer, set()) <= own[observer] for observer in OWNERS)
    non_efx_witness = value("r", final["q"] - {"q0"}) > own["r"]
    assert non_efx_witness

    script = Path(__file__).resolve()
    theorem = root / "results" / "FORM2_ALL_TARGET_CHANGE_EXACT_REPEAT_RANK_NO_GO_20260814.md"
    return {
        "schema": "form2-all-target-change-exact-repeat-rank-no-go-v1",
        "status": "EXACT_REPEAT_DOES_NOT_FORCE_RANK_FOUR",
        "support_edge_count": len(support_edges),
        "all_five_targets_changed": True,
        "all_owner_final_utilities": {k: str(v) for k, v in own.items()},
        "response_edges": [list(edge) for edge in sorted(response_edges)],
        "maximum_response_matching_rank": maximum_matching_rank(response_edges),
        "owner_response_graph_connected": True,
        "singleton_cores_common_safe": True,
        "non_efx_witness": "r envies q after deletion of q0",
        "exact_repeat": "an earlier complete record is stipulated identical to final Z",
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "refutes repeat-to-rank-four admission only; omits full saturated "
            "GG, base-margin, PI-free, and global-lex premises"
        ),
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
        "rank": result["maximum_response_matching_rank"],
    }, indent=2))


if __name__ == "__main__":
    main()
