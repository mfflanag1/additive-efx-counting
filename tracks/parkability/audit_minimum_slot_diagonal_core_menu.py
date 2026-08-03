#!/usr/bin/env python3
"""Audit the balanced connected menu in an extracted diagonal UNSAT core."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_diagonal_topology_union import (
        canonical_key,
        template_record,
    )
    from .audit_minimum_slot_unsat_core_quotient import completion_key
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_diagonal_topology_union import (
        canonical_key,
        template_record,
    )
    from audit_minimum_slot_unsat_core_quotient import completion_key


SCHEMA = "minimum-slot-diagonal-core-menu-audit-v1"


def run(source, output):
    document = json.loads(source.read_text())
    global_groups = {}
    for record in document["global_cuts"]:
        global_groups.setdefault(canonical_key(record), []).append(record)
    completion_groups = {}
    for record in document["completion_cuts"]:
        key = min(completion_key(record, shift) for shift in range(4))
        completion_groups.setdefault(key, []).append(record)
    templates = [
        template_record(key, len(records))
        for key, records in sorted(global_groups.items())
    ]
    topology = Counter(
        (
            record["moved_goods"],
            record["transfer_support_size"],
            tuple(record["bundle_shape"]),
        )
        for record in templates
    )
    checks = {
        "source_is_extracted_core": (
            document.get("status") == "EXTRACTED_UNSAT_CORE_POOL"
        ),
        "41_global_cuts": len(document["global_cuts"]) == 41,
        "22_completion_cuts": len(document["completion_cuts"]) == 22,
        "no_orbit_hall_cuts": not document.get("orbit_hall_cuts"),
        "15_global_templates": len(global_groups) == 15,
        "12_completion_templates": len(completion_groups) == 12,
        "all_global_templates_connected": all(
            record["transfer_component_count"] == 1 for record in templates
        ),
        "all_global_templates_balanced": all(
            record["bundle_shape"] == [2, 2, 2, 2] for record in templates
        ),
        "all_global_templates_move_at_most_four_goods": all(
            record["moved_goods"] <= 4 for record in templates
        ),
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "BALANCED_CONNECTED_CORE_MENU_EXACT"
            if all(checks.values())
            else "BALANCED_CONNECTED_CORE_MENU_MISMATCH"
        ),
        "meaning": (
            "Exact cyclic quotient and transfer-topology audit of the "
            "extracted pattern-2 UNSAT core menu."
        ),
        "claim_boundary": (
            "This audit proves the structure of the persisted core. The "
            "separate untracked replay establishes whether its formulas are UNSAT."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "checks": checks,
        "global_cut_count": len(document["global_cuts"]),
        "completion_cut_count": len(document["completion_cuts"]),
        "global_template_count": len(global_groups),
        "completion_template_count": len(completion_groups),
        "topology_histogram": [
            {
                "moved_goods": key[0],
                "transfer_support_size": key[1],
                "bundle_shape": list(key[2]),
                "template_count": count,
            }
            for key, count in sorted(topology.items())
        ],
        "global_templates": templates,
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
