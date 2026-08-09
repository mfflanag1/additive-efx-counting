#!/usr/bin/env python3
"""Replay every frozen length-three atomic rival core exactly."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_global_lex_cegar import rival_blocker
    from .run_length_three_global_lex_atomic_cegar import GOODS, structural_solver
except ImportError:
    from run_alternating_global_lex_cegar import rival_blocker
    from run_length_three_global_lex_atomic_cegar import GOODS, structural_solver


def owner_from_bundles(named_bundles):
    owner = [None] * len(GOODS)
    for agent, bundle in enumerate(named_bundles):
        for name in bundle:
            good = GOODS.index(name)
            if owner[good] is not None:
                raise ValueError("good assigned twice")
            owner[good] = agent
    return tuple(owner)


def audit(source_path):
    payload = json.loads(source_path.read_text())
    records = payload["records"]
    expected_types = {
        (source, order)
        for source in range(3)
        for order in itertools.permutations(range(4))
    }
    actual_types = {
        (record["singleton_champion_source"], tuple(record["agent_order"]))
        for record in records
    }
    if actual_types != expected_types or len(records) != len(expected_types):
        raise AssertionError("source/order coverage mismatch")
    maximum_core = 0
    for record in records:
        if record["status"] != "UNSAT_ATOMIC_SOURCE_ORDER_CELL":
            raise AssertionError("non-UNSAT frozen record")
        source = record["singleton_champion_source"]
        order = tuple(record["agent_order"])
        solver, values, own = structural_solver(source)
        if solver.check() != z3.sat:
            raise AssertionError("structural source cell is empty")
        owners = [owner_from_bundles(bundles) for bundles in record["core_bundles"]]
        maximum_core = max(maximum_core, len(owners))
        solver.add(*(rival_blocker(values, own, owner, order) for owner in owners))
        if solver.check() != z3.unsat:
            raise AssertionError(("frozen core is not UNSAT", source, order))
    raw = source_path.read_bytes()
    script = Path(__file__).resolve()
    return {
        "schema": "length-three-global-lex-atomic-sweep-audit-v1",
        "status": "ALL_72_ATOMIC_SOURCE_ORDER_CORES_UNSAT",
        "source_type_count": 3,
        "priority_order_count_per_source": 24,
        "total_cell_count": 72,
        "maximum_core_size": maximum_core,
        "claim_boundary": "exact atomic motif audit only; not a packet theorem",
        "provenance": {
            "source": str(source_path),
            "source_sha256": hashlib.sha256(raw).hexdigest(),
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.source)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
