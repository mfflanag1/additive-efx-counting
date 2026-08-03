#!/usr/bin/env python3
"""Compare connected exchange templates across two diagonal cells."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_nearest_exchange_components import transfer_components
    from .run_minimum_slot_orbit_cegar import (
        owner_assignment,
        relabeled_state_orbit,
        state_key,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_nearest_exchange_components import transfer_components
    from run_minimum_slot_orbit_cegar import (
        owner_assignment,
        relabeled_state_orbit,
        state_key,
    )


SCHEMA = "minimum-slot-diagonal-topology-union-audit-v1"
BASE_STATE = {"floater": 8, "masks": (3, 12, 48, 192)}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_key(record):
    state = {
        "floater": int(record["floater"]),
        "masks": tuple(int(mask) for mask in record["masks"]),
    }
    return min(
        state_key(mapped)
        for mapped in relabeled_state_orbit(state, "cyclic")
    )


def template_record(key, member_count):
    state = {"floater": key[0], "masks": key[1]}
    left = owner_assignment(BASE_STATE)
    right = owner_assignment(state)
    components = transfer_components(left, right)
    moved_goods = sum(source != destination for source, destination in zip(left, right))
    bundle_shape = sorted(int(mask).bit_count() for mask in state["masks"])
    return {
        "canonical_floater": key[0],
        "canonical_masks": list(key[1]),
        "member_count": member_count,
        "moved_goods": moved_goods,
        "transfer_component_count": len(components),
        "transfer_support_size": len(components[0]["vertices"]),
        "bundle_shape": bundle_shape,
    }


def groups(document):
    result = {}
    for record in document["global_cuts"]:
        result.setdefault(canonical_key(record), []).append(record)
    return result


def signature(record):
    return (
        record["moved_goods"],
        record["transfer_support_size"],
        tuple(record["bundle_shape"]),
    )


def common_template_record(key, pattern1_records, pattern2_records):
    record = template_record(key, len(pattern1_records) + len(pattern2_records))
    record["pattern1_member_count"] = len(pattern1_records)
    record["pattern2_member_count"] = len(pattern2_records)
    return record


def run(pattern1, pattern2, output):
    documents = {
        "pattern1": json.loads(pattern1.read_text()),
        "pattern2": json.loads(pattern2.read_text()),
    }
    grouped = {name: groups(document) for name, document in documents.items()}
    templates = {
        name: [
            template_record(key, len(records))
            for key, records in sorted(source_groups.items())
        ]
        for name, source_groups in grouped.items()
    }
    histograms = {}
    for name, records in templates.items():
        counts = Counter(signature(record) for record in records)
        histograms[name] = [
            {
                "moved_goods": key[0],
                "transfer_support_size": key[1],
                "bundle_shape": list(key[2]),
                "template_count": count,
            }
            for key, count in sorted(counts.items())
        ]
    keys1 = set(grouped["pattern1"])
    keys2 = set(grouped["pattern2"])
    checks = {
        "all_templates_connected": all(
            record["transfer_component_count"] == 1
            for records in templates.values()
            for record in records
        ),
        "all_moves_at_most_four_goods": all(
            record["moved_goods"] <= 4
            for records in templates.values()
            for record in records
        ),
        "pattern1_templates": len(keys1) == 8,
        "pattern2_templates": len(keys2) == 13,
        "common_templates": len(keys1 & keys2) == 3,
        "union_templates": len(keys1 | keys2) == 18,
    }
    result = {
        "schema": SCHEMA,
        "status": (
            "DIAGONAL_TOPOLOGY_UNION_EXACT"
            if all(checks.values())
            else "DIAGONAL_TOPOLOGY_UNION_MISMATCH"
        ),
        "meaning": (
            "Exact cyclic quotient and transfer-topology comparison of the "
            "persisted pattern-1 theorem core and pattern-2 Hall witness pool."
        ),
        "claim_boundary": (
            "Pattern 1 is an UNSAT theorem core. Pattern 2 is an incomplete "
            "CEGAR pool, so its templates are evidence and analytic targets, "
            "not a complete theorem menu."
        ),
        "sources": {
            "pattern1": {"path": str(pattern1), "sha256": sha256(pattern1)},
            "pattern2": {"path": str(pattern2), "sha256": sha256(pattern2)},
        },
        "checks": checks,
        "pattern1_global_cut_count": len(documents["pattern1"]["global_cuts"]),
        "pattern2_global_cut_count": len(documents["pattern2"]["global_cuts"]),
        "pattern1_template_count": len(keys1),
        "pattern2_template_count": len(keys2),
        "common_template_count": len(keys1 & keys2),
        "union_template_count": len(keys1 | keys2),
        "topology_histograms": histograms,
        "common_templates": [
            common_template_record(
                key,
                grouped["pattern1"][key],
                grouped["pattern2"][key],
            )
            for key in sorted(keys1 & keys2)
        ],
        "pattern1_only_templates": [
            template_record(key, len(grouped["pattern1"][key]))
            for key in sorted(keys1 - keys2)
        ],
        "pattern2_only_templates": [
            template_record(key, len(grouped["pattern2"][key]))
            for key in sorted(keys2 - keys1)
        ],
    }
    atomic_json(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pattern1", type=Path, required=True)
    parser.add_argument("--pattern2", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.pattern1, args.pattern2, args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
