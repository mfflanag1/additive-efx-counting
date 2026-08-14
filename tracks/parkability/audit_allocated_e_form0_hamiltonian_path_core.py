#!/usr/bin/env python3
"""Independent combinatorial audit of the form-0 path/core certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


BASE = {
    "r": {"a0", "m"},
    "q": {"gq", "a1", "j"},
    "d": {"h", "k", "q0", "l"},
    "s": {"e", "p"},
    "charity": {"gr"},
}
OWNERS = {"r", "q", "d", "s"}


def validate_closed_core_witness(witness):
    cycle = witness["cycle"]
    edges = witness["edges"]
    assert len(cycle) == len(set(cycle))
    assert set(cycle) <= OWNERS
    assert len(edges) == len(cycle)
    vertices = set(cycle)
    cores = []
    released_union = set()
    incoming_allocated = set()
    base_owner = {
        good: owner for owner, goods in BASE.items() for good in goods
    }

    for index, edge in enumerate(edges):
        source = cycle[index]
        target = cycle[(index + 1) % len(cycle)]
        assert edge["source"] == source
        assert edge["target"] == target
        core = set(edge["desired_core"])
        assert core
        assert all(base_owner[good] in vertices | {"charity"} for good in core)
        expected_incoming = core - BASE[target]
        expected_released = BASE[target] - core
        assert set(edge["incoming"]) == expected_incoming
        assert set(edge["released"]) == expected_released
        incoming_allocated |= {
            good for good in expected_incoming if base_owner[good] != "charity"
        }
        released_union |= expected_released
        cores.append(core)

    assert all(
        cores[left].isdisjoint(cores[right])
        for left in range(len(cores))
        for right in range(left + 1, len(cores))
    )
    assert incoming_allocated <= released_union
    return {
        "cycle_length": len(cycle),
        "core_good_count": sum(map(len, cores)),
        "incoming_allocated_count": len(incoming_allocated),
    }


def run(source: Path, output: Path):
    payload = json.loads(source.read_text())
    assert payload["status"] == "UNSAT_REPLAYED"
    assert payload["core_only_replay_status"] == "unsat"
    rows = [
        validate_closed_core_witness(witness)
        for witness in payload["core_witnesses"]
    ]
    assert len(rows) == payload["core_cut_count"]
    result = {
        "schema": "allocated-e-form0-hamiltonian-path-core-audit-v1",
        "status": "CORE_SEMANTICS_VALID",
        "core_witness_count": len(rows),
        "cycle_length_counts": {
            str(length): sum(row["cycle_length"] == length for row in rows)
            for length in sorted({row["cycle_length"] for row in rows})
        },
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "checks": [
            "distinct cycle owners and canonical cyclic targets",
            "nonempty pairwise-disjoint desired cores",
            "base-owner closure inside cycle owners plus charity",
            "exact incoming/released packet identities",
            "release coverage of every allocated incoming good",
        ],
        "claim_boundary": (
            "Solver-independent combinatorial audit of the 70 PI witnesses; "
            "the UNSAT master replay still uses the primary algebraic encoding."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps({
        "status": result["status"],
        "core_witness_count": result["core_witness_count"],
        "cycle_length_counts": result["cycle_length_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
