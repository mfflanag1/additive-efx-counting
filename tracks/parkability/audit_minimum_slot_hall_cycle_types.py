#!/usr/bin/env python3
"""Classify token-orbit Hall cuts by distinguished-floater cycle type."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import TOKENS
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import TOKENS


SCHEMA = "minimum-slot-hall-cycle-type-audit-v1"


def cycle_signature(assignment):
    token_index = {good: index for index, good in enumerate(TOKENS)}
    permutation = tuple(token_index[good] for good in assignment)
    seen = set()
    cycles = []
    for start in range(len(TOKENS)):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        cycles.append(tuple(cycle))
    floater_cycle = next(cycle for cycle in cycles if 4 in cycle)
    owner_cycle_lengths = tuple(
        sorted(
            (len(cycle) for cycle in cycles if 4 not in cycle),
            reverse=True,
        )
    )
    return len(floater_cycle), owner_cycle_lengths


def signature_record(signature):
    return {
        "floater_cycle_length": signature[0],
        "other_cycle_lengths": list(signature[1]),
    }


def run(source, output):
    document = json.loads(source.read_text())
    universe = Counter(
        cycle_signature(assignment)
        for assignment in itertools.permutations(TOKENS)
    )
    observed_assignments = [
        tuple(int(good) for good in record["assignment"])
        for record in document["orbit_hall_cuts"]
    ]
    observed = Counter(cycle_signature(assignment) for assignment in observed_assignments)
    records = []
    for signature in sorted(universe):
        records.append(
            {
                **signature_record(signature),
                "universe_size": universe[signature],
                "observed_count": observed[signature],
                "fully_covered": observed[signature] == universe[signature],
            }
        )
    result = {
        "schema": SCHEMA,
        "status": "HALL_CYCLE_TYPES_CLASSIFIED",
        "meaning": (
            "Exact conjugacy classification of five-token permutations under "
            "owner relabeling with the floater slot distinguished."
        ),
        "claim_boundary": (
            "Observed coverage describes this finite CEGAR cut pool and is "
            "not a proof that unobserved cycle types are unnecessary."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "orbit_state_count": sum(universe.values()),
        "cycle_type_count": len(universe),
        "observed_hall_cut_count": len(observed_assignments),
        "observed_cycle_type_count": len(observed),
        "fully_covered_cycle_type_count": sum(
            record["fully_covered"] for record in records
        ),
        "cycle_types": records,
        "observed_assignments": [list(assignment) for assignment in observed_assignments],
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
