#!/usr/bin/env python3
"""Quotient a minimum-slot UNSAT core by cyclic owner relabeling."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .run_minimum_slot_orbit_cegar import relabeled_state_orbit, state_key
except ImportError:
    from anneal import atomic_json
    from run_minimum_slot_orbit_cegar import relabeled_state_orbit, state_key


SCHEMA = "minimum-slot-unsat-core-cyclic-quotient-audit-v1"


def mapped_good(good, shift):
    if int(good) == 8:
        return 8
    return 2 * ((int(good) // 2 + shift) % 4) + int(good) % 2


def completion_key(record, shift):
    assignment = [None] * 5
    for owner in range(4):
        assignment[(owner + shift) % 4] = mapped_good(
            record["assignment"][owner], shift
        )
    assignment[4] = mapped_good(record["assignment"][4], shift)
    permutation = [None] * 4
    for observer in range(4):
        permutation[(observer + shift) % 4] = (
            int(record["permutation"][observer]) + shift
        ) % 4
    return (
        tuple(assignment),
        (int(record["host"]) + shift) % 4,
        tuple(permutation),
    )


def run(source, output):
    document = json.loads(source.read_text())
    global_groups = {}
    for record in document["global_cuts"]:
        state = {
            "floater": int(record["floater"]),
            "masks": tuple(int(mask) for mask in record["masks"]),
        }
        key = min(
            state_key(mapped)
            for mapped in relabeled_state_orbit(state, "cyclic")
        )
        global_groups.setdefault(key, []).append(record)

    completion_groups = {}
    for record in document["completion_cuts"]:
        key = min(completion_key(record, shift) for shift in range(4))
        completion_groups.setdefault(key, []).append(record)

    global_histogram = Counter(len(records) for records in global_groups.values())
    completion_histogram = Counter(
        len(records) for records in completion_groups.values()
    )
    result = {
        "schema": SCHEMA,
        "status": "CYCLIC_CORE_QUOTIENT_EXACT",
        "meaning": (
            "Exact quotient of persisted global and completion cuts under "
            "simultaneous cyclic relabeling of owners, paired goods, hosts, "
            "observers, and assigned bundles."
        ),
        "claim_boundary": (
            "The quotient counts analytic templates in this fixed edge cell. "
            "It does not prove that one representative implies every partially "
            "present orbit member without the corresponding relabeling argument."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "global_cut_count": len(document["global_cuts"]),
        "global_template_count": len(global_groups),
        "global_template_coverage_histogram": {
            str(size): count for size, count in sorted(global_histogram.items())
        },
        "completion_cut_count": len(document["completion_cuts"]),
        "completion_template_count": len(completion_groups),
        "completion_template_coverage_histogram": {
            str(size): count
            for size, count in sorted(completion_histogram.items())
        },
        "total_template_count": len(global_groups) + len(completion_groups),
        "global_templates": [
            {
                "canonical_floater": key[0],
                "canonical_masks": list(key[1]),
                "member_count": len(records),
                "owner_distance": records[0].get("owner_distance"),
            }
            for key, records in sorted(global_groups.items())
        ],
        "completion_templates": [
            {
                "canonical_assignment": list(key[0]),
                "canonical_host": key[1],
                "canonical_permutation": list(key[2]),
                "member_count": len(records),
            }
            for key, records in sorted(completion_groups.items())
        ],
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
