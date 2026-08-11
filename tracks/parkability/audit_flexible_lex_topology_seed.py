#!/usr/bin/env python3
"""Audit the frozen 37-class lex-hard flower gate census."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
    from .run_flexible_later_owner_topology_cegar import classify_candidates
except ImportError:
    from analyze_flexible_later_owner_escape_topologies import old_bundles
    from run_flexible_later_owner_topology_cegar import classify_candidates


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(seed_path):
    seed = json.loads(seed_path.read_text())
    if seed.get("objective") != "lex":
        raise ValueError("seed is not the lex-objective gate")
    groups = classify_candidates(old_bundles(), "lex")
    selected = seed["selected_topology_classes"]
    assert len(selected) == len(set(selected)) == 37
    assert all(signature in groups for signature in selected)
    selected_counts = {
        signature: len(groups[signature]) for signature in selected
    }
    assert sum(selected_counts.values()) == seed["candidate_allocation_count"] == 2514
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-topology-seed-audit-v1",
        "status": "VERIFIED_GATE",
        "full_connected_candidate_count": sum(map(len, groups.values())),
        "full_topology_class_count": len(groups),
        "selected_topology_class_count": len(selected),
        "selected_candidate_allocation_count": sum(selected_counts.values()),
        "selected_class_counts": selected_counts,
        "claim_boundary": (
            "exact census of the frozen bounded lex-hard topology union; it "
            "verifies gate construction, not SAT or UNSAT of the gate"
        ),
        "provenance": {
            "seed": str(seed_path.relative_to(root)),
            "seed_sha256": sha256(seed_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.seed.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "selected_topology_class_count": result["selected_topology_class_count"],
        "selected_candidate_allocation_count": result["selected_candidate_allocation_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
