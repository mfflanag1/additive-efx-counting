#!/usr/bin/env python3
"""Audit cyclic symmetry of the fixed off-host edge profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        numeric_complete_edges,
    )
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import (
        BASE,
        FLOATER,
        PAIR_HALL_CYCLE,
        numeric_complete_edges,
    )


SCHEMA = "minimum-slot-diagonal-symmetry-audit-v1"


def run(source, theorem_pattern, output):
    document = json.loads(source.read_text())
    values = document.get("values", document)
    offhost = {}
    diagonal = {}
    diagonal_order = []
    for host, pair in enumerate(PAIR_HALL_CYCLE):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], FLOATER)))
        edges = numeric_complete_edges(values, complete)
        for observer in sorted(set(range(4)) - set(pair)):
            for assigned in range(4):
                key = (host, observer, assigned)
                if assigned == host:
                    diagonal_order.append((host, observer))
                    diagonal[(host, observer)] = bool(edges[observer][assigned])
                else:
                    offhost[key] = bool(edges[observer][assigned])

    shifts = []
    for shift in range(4):
        mismatches = []
        for key, value in offhost.items():
            mapped = tuple((entry + shift) % 4 for entry in key)
            if offhost[mapped] != value:
                mismatches.append(
                    {
                        "edge": list(key),
                        "mapped_edge": list(mapped),
                        "edge_value": value,
                        "mapped_value": offhost[mapped],
                    }
                )
        pair_cycle_preserved = all(
            {
                (observer + shift) % 4
                for observer in PAIR_HALL_CYCLE[host]
            }
            == set(PAIR_HALL_CYCLE[(host + shift) % 4])
            for host in range(4)
        )
        shifts.append(
            {
                "shift": shift,
                "pair_hall_cycle_preserved": pair_cycle_preserved,
                "offhost_mismatch_count": len(mismatches),
                "offhost_mismatches": mismatches,
            }
        )

    bit_index = {edge: bit for bit, edge in enumerate(diagonal_order)}
    bit_permutations = []
    pattern_orbit = set()
    for shift in range(4):
        permutation = []
        mapped_pattern = 0
        for bit, (host, observer) in enumerate(diagonal_order):
            mapped_edge = ((host + shift) % 4, (observer + shift) % 4)
            mapped_bit = bit_index[mapped_edge]
            permutation.append(mapped_bit)
            if theorem_pattern & (1 << bit):
                mapped_pattern |= 1 << mapped_bit
        bit_permutations.append(
            {"shift": shift, "bit_permutation": permutation}
        )
        pattern_orbit.add(mapped_pattern)

    offhost_invariant = all(
        shift["offhost_mismatch_count"] == 0 for shift in shifts
    )
    pair_cycle_invariant = all(
        shift["pair_hall_cycle_preserved"] for shift in shifts
    )
    source_diagonal_pattern = sum(
        (1 << bit) * int(diagonal[edge])
        for bit, edge in enumerate(diagonal_order)
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "CYCLIC_PATTERN_ORBIT_CERTIFIED"
            if offhost_invariant and pair_cycle_invariant
            else "CYCLIC_SYMMETRY_FAILED"
        ),
        "meaning": (
            "Exact Boolean audit of simultaneous cyclic relabeling on the source's "
            "24 fixed off-host edge values and eight diagonal host-edge positions."
        ),
        "claim_boundary": (
            "When the off-host profile is invariant, any theorem for the input "
            "diagonal pattern transfers by relabeling to the reported pattern orbit. "
            "This does not cover the other diagonal orbit or free the off-host bits."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "offhost_edge_count": len(offhost),
        "offhost_profile_cyclic_invariant": offhost_invariant,
        "pair_hall_cycle_cyclic_invariant": pair_cycle_invariant,
        "source_diagonal_pattern": source_diagonal_pattern,
        "diagonal_edge_order": [list(edge) for edge in diagonal_order],
        "theorem_pattern": theorem_pattern,
        "theorem_pattern_cyclic_orbit": sorted(pattern_orbit),
        "bit_permutations": bit_permutations,
        "shift_audits": shifts,
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--theorem-pattern", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.theorem_pattern, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
