#!/usr/bin/env python3
"""Audit the cap-free reverse-response construction at the rank-three gate.

The three minimum response normal forms have three matching edges and one
unmatched root-facing edge.  The anchor target q has two incoming response
cores.  When those two physical cores are disjoint, reversing all four
responses gives a complete allocation through exactly four support edges.

Each symbolic atom below denotes an arbitrary nonempty packet, not one good.
Consequently the conservation/topology statement is independent of packet
cardinality.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


OWNERS = ("r", "q", "c", "s")
CHARITY = "charity"
ANCHOR_TARGET = "q"

# These are the three minimum selected-matching forms in the independent
# rank-three exact-repeat audit, each augmented by the unmatched c -> q edge.
FORMS = (
    (("q", CHARITY), ("r", "q"), ("s", "r"), ("c", "q")),
    (("q", CHARITY), ("r", "q"), ("s", "c"), ("c", "q")),
    (("q", "s"), ("r", "q"), ("s", CHARITY), ("c", "q")),
)


def weakly_connected(edges):
    vertices = set(OWNERS) | {CHARITY}
    adjacency = defaultdict(set)
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen, stack = set(), [CHARITY]
    while stack:
        vertex = stack.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        stack.extend(adjacency[vertex] - seen)
    return seen == vertices


def construct(response_edges):
    response_edges = tuple(response_edges)
    assert len(response_edges) == 4
    assert {source for source, _ in response_edges} == set(OWNERS)
    assert Counter(target for _, target in response_edges)[ANCHOR_TARGET] == 2
    assert Counter(target for _, target in response_edges)[CHARITY] == 1

    # D[source,target] is an arbitrary nonempty desired core contained in the
    # physical target bundle.  Cores with a common target are separate atoms;
    # this is exactly the disjoint-double-core hypothesis at q.
    cores = {
        (source, target): f"D[{source}->{target}]"
        for source, target in response_edges
    }
    residual = {
        owner: f"R[{owner}]" for owner in OWNERS
    }

    initial = {owner: {residual[owner]} for owner in OWNERS}
    initial[CHARITY] = set()
    for edge, atom in cores.items():
        initial[edge[1]].add(atom)

    # The charity packet is a singleton physical packet and its unique
    # nonempty response core is therefore the entire charity bundle.
    charity_edge = next(edge for edge in response_edges if edge[1] == CHARITY)
    initial[CHARITY] = {cores[charity_edge]}

    final = {owner: {residual[owner]} for owner in OWNERS}
    final[CHARITY] = set()
    for edge, atom in cores.items():
        final[edge[0]].add(atom)

    initial_atoms = set().union(*initial.values())
    final_atoms = set().union(*final.values())
    assert sum(map(len, initial.values())) == len(initial_atoms)
    assert sum(map(len, final.values())) == len(final_atoms)
    assert initial_atoms == final_atoms
    assert not final[CHARITY]

    holder_before = {
        atom: owner for owner, atoms in initial.items() for atom in atoms
    }
    holder_after = {
        atom: owner for owner, atoms in final.items() for atom in atoms
    }
    transfer_edges = tuple(sorted({
        (holder_before[atom], holder_after[atom])
        for atom in initial_atoms
        if holder_before[atom] != holder_after[atom]
    }))
    expected = tuple(sorted((target, source) for source, target in response_edges))
    assert transfer_edges == expected
    assert len(transfer_edges) == 4
    assert weakly_connected(transfer_edges)

    outgoing = Counter(source for source, _ in transfer_edges)
    assert outgoing[ANCHOR_TARGET] == 2
    assert max(outgoing.values()) == 2
    return {
        "response_edges": [list(edge) for edge in sorted(response_edges)],
        "transfer_edges": [list(edge) for edge in transfer_edges],
        "initial_atoms": {
            owner: sorted(atoms) for owner, atoms in initial.items()
        },
        "final_atoms": {
            owner: sorted(atoms) for owner, atoms in final.items()
        },
        "checks": {
            "all_four_sources_receive_one_desired_core": (
                {source for source, _ in response_edges} == set(OWNERS)
            ),
            "shared_q_cores_are_distinct_atoms": (
                len({cores[edge] for edge in response_edges if edge[1] == "q"}) == 2
            ),
            "charity_is_empty": not final[CHARITY],
            "atom_conservation": initial_atoms == final_atoms,
            "exactly_four_support_edges": len(transfer_edges) == 4,
            "transfer_graph_connected": weakly_connected(transfer_edges),
            "q_must_supply_two_recipients": outgoing["q"] == 2,
            "construction_is_not_functional": len(outgoing) < len(transfer_edges),
        },
    }


def run(root: Path):
    records = [construct(form) for form in FORMS]
    assert len(records) == 3
    assert all(all(record["checks"].values()) for record in records)
    script = Path(__file__).resolve()
    theorem = root / "results/RANK_THREE_DISJOINT_DOUBLE_CORE_COMPLETE_FOUR_EDGE_LEMMA_20260813.md"
    return {
        "schema": "rank-three-disjoint-double-core-four-edge-v1",
        "status": "ALL_THREE_NORMAL_FORMS_CLOSE_CONDITIONALLY",
        "normal_form_count": len(records),
        "records": records,
        "cap_free_reason": (
            "each D and R atom represents an arbitrary finite physical packet; "
            "the proof uses only disjointness, nonemptiness, and conservation"
        ),
        "exact_remaining_gate": (
            "derive two disjoint response/payment cores inside the shared q target, "
            "or repair their overlap while preserving the four support-edge budget; "
            "then establish the owner-payment and observer-safety inequalities"
        ),
        "claim_boundary": (
            "cap-free conservation and graph lemma conditional on disjoint shared-"
            "target cores and the endpoint payment/safety inequalities; it does not "
            "derive those conditions from saturation and is not the universal "
            "four-edge extraction theorem"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
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
        "normal_form_count": result["normal_form_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
