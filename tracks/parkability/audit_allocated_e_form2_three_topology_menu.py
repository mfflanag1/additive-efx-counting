#!/usr/bin/env python3
"""Solver-independent structural audit of the form-2 menu CEGAR traces.

This checker deliberately does not import the primary CEGAR driver.  It
reconstructs the three packet topologies, verifies their exact allocation
counts, and checks the combinatorial semantics and global uniqueness of every
generalized-PI witness stored in one initial trace followed by zero or more
resume traces.  It does not replay the algebraic master.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


OWNERS = ("r", "q", "d", "s")
CURRENT = {
    "r": ("a0", "a1", "h"),
    "q": ("j", "k", "q0"),
    "d": ("m", "gq", "gr"),
    "s": ("l", "e"),
    "charity": ("p",),
}
BASE = {
    "r": {"a0", "m"},
    "q": {"gq", "a1", "j"},
    "d": {"h", "k", "q0", "l"},
    "s": {"e", "p"},
    "charity": {"gr"},
}
MENU = (
    (("charity", "r"), ("r", "d"), ("r", "s")),
    (("charity", "r"), ("q", "d"), ("r", "d"), ("r", "q")),
    (("charity", "q"), ("d", "q"), ("q", "d"), ("r", "s")),
)


def canonical(allocation):
    return tuple(
        (owner, tuple(sorted(goods)))
        for owner, goods in sorted(allocation.items())
    )


def allocations_for_topology(topology):
    """Independently enumerate all exact stay/send assignments."""
    outgoing = {supplier: [] for supplier in CURRENT}
    charity_target = None
    for supplier, recipient in topology:
        if supplier == "charity":
            assert charity_target is None
            charity_target = recipient
        else:
            outgoing[supplier].append(recipient)
    assert charity_target is not None

    supplier_rows = []
    for supplier in OWNERS:
        recipients = outgoing[supplier]
        destinations = (supplier, *recipients)
        rows = []
        for assignment in itertools.product(
                destinations, repeat=len(CURRENT[supplier])):
            # Every declared transfer pair must carry a nonempty packet.
            if any(recipient not in assignment for recipient in recipients):
                continue
            rows.append(dict(zip(CURRENT[supplier], assignment, strict=True)))
        supplier_rows.append(rows)

    allocations = []
    for selected in itertools.product(*supplier_rows):
        allocation = {owner: [] for owner in OWNERS}
        allocation[charity_target].append("p")
        for routing in selected:
            for good, recipient in routing.items():
                allocation[recipient].append(good)
        allocation["charity"] = []
        allocations.append(allocation)
    return allocations


def independent_menu_counts():
    per_topology = [len(allocations_for_topology(row)) for row in MENU]
    union = {
        canonical(allocation)
        for topology in MENU
        for allocation in allocations_for_topology(topology)
    }
    return per_topology, len(union)


def witness_signature(witness):
    return tuple(sorted(
        (edge["source"], tuple(sorted(edge["desired_core"])))
        for edge in witness["edges"]
    ))


def validate_witness(witness):
    cycle = tuple(witness["cycle"])
    edges = witness["edges"]
    assert cycle and len(cycle) == len(set(cycle))
    assert set(cycle) <= set(OWNERS)
    assert len(edges) == len(cycle)
    vertices = set(cycle)
    base_owner = {
        good: owner for owner, goods in BASE.items() for good in goods
    }
    cores = []
    incoming_allocated = set()
    released_union = set()
    for index, edge in enumerate(edges):
        source = cycle[index]
        target = cycle[(index + 1) % len(cycle)]
        assert edge["source"] == source
        assert edge["target"] == target
        core = set(edge["desired_core"])
        assert core
        assert all(base_owner[good] in vertices | {"charity"} for good in core)
        incoming = core - BASE[target]
        released = BASE[target] - core
        assert set(edge["incoming"]) == incoming
        assert set(edge["released"]) == released
        incoming_allocated |= {
            good for good in incoming if base_owner[good] != "charity"
        }
        released_union |= released
        cores.append(core)
    assert all(
        cores[left].isdisjoint(cores[right])
        for left in range(len(cores))
        for right in range(left + 1, len(cores))
    )
    assert incoming_allocated <= released_union
    return len(cycle)


def run(sources: list[Path], output: Path):
    topology_counts, allocation_count = independent_menu_counts()
    assert topology_counts == [12, 84, 343]
    assert allocation_count == 439

    signatures = set()
    cycle_counts = Counter()
    trace_rows = []
    previous_source = None
    for source in sources:
        raw = source.read_bytes()
        payload = json.loads(raw)
        assert payload["schema"] == "allocated-e-form2-three-topology-menu-cegar-v1"
        assert payload["form_index"] == 2
        assert payload["menu"] == [
            [list(edge) for edge in topology] for topology in MENU
        ]
        assert payload["topology_allocation_counts"] == topology_counts
        assert payload["allocation_count"] == allocation_count

        resume = payload.get("resume")
        if previous_source is None:
            assert resume is None
        else:
            assert resume is not None
            assert resume["loaded_cut_count"] == len(signatures)
            assert resume["source_sha256"] == previous_source["sha256"]

        fresh_count = 0
        for iteration in payload["iterations"]:
            witnesses = iteration.get("pi_witnesses") or ()
            if witnesses:
                assert iteration["solver_status"] == "sat"
                assert iteration["fresh_cut_count"] == len(witnesses)
                assert iteration["pi_cycle_count"] >= len(witnesses)
            for witness in witnesses:
                length = validate_witness(witness)
                signature = witness_signature(witness)
                assert signature not in signatures
                signatures.add(signature)
                cycle_counts[length] += 1
                fresh_count += 1
        assert payload["generalized_pi_cut_count"] == len(signatures)
        previous_source = {
            "path": str(source),
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
        trace_rows.append({
            **previous_source,
            "status": payload["status"],
            "iteration_count": len(payload["iterations"]),
            "fresh_cut_count": fresh_count,
            "cumulative_cut_count": len(signatures),
        })

    result = {
        "schema": "allocated-e-form2-three-topology-menu-structural-audit-v1",
        "status": "STRUCTURE_VALID",
        "topology_allocation_counts": topology_counts,
        "allocation_count": allocation_count,
        "trace_rows": trace_rows,
        "unique_pi_witness_count": len(signatures),
        "cycle_length_counts": {
            str(length): count for length, count in sorted(cycle_counts.items())
        },
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": [
            "independent enumeration of every stay/send allocation",
            "exact three-topology menu and union cardinality",
            "resume source hash and cumulative-cut continuity",
            "global uniqueness of every generalized-PI cut signature",
            "nonempty pairwise-disjoint desired cores",
            "exact base incoming/released identities and release coverage",
        ],
        "claim_boundary": (
            "Solver-independent structural audit of the allocation menu and "
            "PI witnesses. It does not replay the QF_LRA master and cannot "
            "promote a bounded verdict to a cap-free theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps({
        "status": result["status"],
        "allocation_count": result["allocation_count"],
        "unique_pi_witness_count": result["unique_pi_witness_count"],
        "cycle_length_counts": result["cycle_length_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
