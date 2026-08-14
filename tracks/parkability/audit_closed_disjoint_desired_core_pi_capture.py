#!/usr/bin/env python3
"""Independent finite audit of the closed disjoint desired-core PI lemma."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "CLOSED_DISJOINT_DESIRED_CORE_PI_CAPTURE_LEMMA_20260813.md"
OWNERS = tuple(range(4))
CHARITY = 4


def cycles(vertices):
    anchor = min(vertices)
    for rest in itertools.permutations(v for v in vertices if v != anchor):
        yield (anchor, *rest)


def audit():
    # One labeled base good per owner and two charity goods. Each good is
    # assigned to no core or exactly one source core, ensuring disjointness.
    # Unlike a one-sided audit, enumerate outside-owner support too and check
    # that exact canonical PI availability is equivalent to closure.
    goods = tuple(range(6))
    base_owner = {0: 0, 1: 1, 2: 2, 3: 3, 4: CHARITY, 5: CHARITY}
    checked = 0
    for size in range(1, 5):
        for vertices in itertools.combinations(OWNERS, size):
            vertex_set = set(vertices)
            # 0 means unused; 1..size selects the unique core receiving good.
            for assignment in itertools.product(range(size + 1), repeat=len(goods)):
                core = {owner: set() for owner in vertices}
                for good, slot in zip(goods, assignment, strict=True):
                    if slot:
                        core[vertices[slot - 1]].add(good)
                if any(not core[owner] for owner in vertices):
                    continue
                for cycle in cycles(vertices):
                    successor = {
                        cycle[index]: cycle[(index + 1) % len(cycle)]
                        for index in range(len(cycle))
                    }
                    predecessor = {target: source for source, target in successor.items()}
                    incoming = {
                        owner: {
                            good for good in core[owner]
                            if base_owner[good] != successor[owner]
                        }
                        for owner in vertices
                    }
                    released = {
                        owner: {
                            good for good in goods
                            if base_owner[good] == owner
                            and good not in core[predecessor[owner]]
                        }
                        for owner in vertices
                    }
                    incoming_sets = list(incoming.values())
                    assert all(
                        left.isdisjoint(right)
                        for index, left in enumerate(incoming_sets)
                        for right in incoming_sets[index + 1:]
                    )
                    available = all(
                        base_owner[good] == CHARITY
                        or (
                            base_owner[good] in vertex_set
                            and good in released[base_owner[good]]
                        )
                        for owner in vertices for good in incoming[owner]
                    )
                    closed = all(
                        base_owner[good] in vertex_set | {CHARITY}
                        for owner in vertices for good in core[owner]
                    )
                    assert available == closed
                    checked += 1

    c, a, floor = z3.Reals("capture complement floor")
    solver = z3.SolverFor("QF_LRA")
    solver.add(c > 0, a >= 0, floor >= 0, c > floor, c - a <= floor)
    solver.add(z3.Not(a >= c - floor))
    assert solver.check() == z3.unsat

    return {
        "schema": "closed-disjoint-desired-core-pi-capture-audit-v1",
        "status": "CLOSED_DISJOINT_CORE_PI_CHARACTERIZATION_AND_CAPTURE_VERIFIED",
        "combinatorial_records": checked,
        "owner_subsets": 15,
        "maximum_owner_count": 4,
        "symbolic_capture_status": "unsat",
        "document_sha256": hashlib.sha256(DOCUMENT.read_bytes()).hexdigest(),
        "claim_boundary": (
            "Cap-free combinatorial PI construction and exact full-margin "
            "capture implication. Reversal of capture and the four-edge EFX "
            "conclusion remain open."
        ),
    }


def main():
    output = ROOT / "results" / "closed_disjoint_desired_core_pi_capture_audit.json"
    result = audit()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "records": result["combinatorial_records"],
    }, indent=2))


if __name__ == "__main__":
    main()
