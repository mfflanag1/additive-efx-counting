#!/usr/bin/env python3
"""Export the frozen 37-class lex-hard flower gate as SMT-LIB 2."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_flexible_later_owner_connected_transfer import endpoint_formula
    from .decide_flexible_later_owner_topology_menu import build_master
    from .run_flexible_later_owner_topology_cegar import classify_candidates
except ImportError:
    from decide_flexible_later_owner_connected_transfer import endpoint_formula
    from decide_flexible_later_owner_topology_menu import build_master
    from run_flexible_later_owner_topology_cegar import classify_candidates


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    seed_path,
    output_path,
    atom_order_symmetry=False,
    live_polarity=False,
):
    seed = json.loads(seed_path.read_text())
    if seed.get("objective") != "lex":
        raise ValueError("seed is not the lex topology gate")
    solver, atoms, old, value, base = build_master()
    symmetry_constraint_count = 0
    if atom_order_symmetry:
        atom_set = set(atoms)
        for atom in atoms:
            if not atom.endswith("_0"):
                continue
            partner = atom[:-1] + "1"
            if partner not in atom_set:
                continue
            # Swapping the two physical goods in a packet is a global item
            # relabeling.  Canonicalize that orbit in one reference row only;
            # independent row-wise swaps would be unsound.
            solver.add(value[atom, "r"] <= value[partner, "r"])
            symmetry_constraint_count += 1
    if live_polarity:
        bottom_r = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
        bottom_q = ("ar_bq_0", "ar_bq_1")
        solver.add(
            z3.Sum(*(value[good, "r"] for good in bottom_r))
            >= value["f", "r"]
        )
        solver.add(
            value["f", "r"]
            > z3.Sum(*(value[good, "r"] for good in bottom_q))
        )
        solver.add(
            z3.Sum(*(value[good, "q"] for good in bottom_q))
            > z3.Sum(*(value[good, "q"] for good in bottom_r))
        )
    groups = classify_candidates(old, "lex")
    selected = seed["selected_topology_classes"]
    count = 0
    for signature in selected:
        for allocation in groups[signature]:
            solver.add(z3.Not(endpoint_formula(
                allocation, old, value, base, "lex"
            )))
            count += 1
    assert count == seed["candidate_allocation_count"] == 2514
    smt2 = solver.to_smt2().encode()
    output_path.write_bytes(smt2)
    script = Path(__file__).resolve()
    root = script.parents[2]
    return {
        "schema": "flexible-lex-topology-gate-export-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "selected_topology_class_count": len(selected),
        "selected_candidate_allocation_count": count,
        "atom_order_symmetry": atom_order_symmetry,
        "live_polarity": live_polarity,
        "symmetry_constraint_count": symmetry_constraint_count,
        "smt2_bytes": len(smt2),
        "smt2_sha256": sha256_bytes(smt2),
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
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--atom-order-symmetry", action="store_true")
    parser.add_argument("--live-polarity", action="store_true")
    args = parser.parse_args()
    result = run(
        args.seed.resolve(),
        args.output.resolve(),
        args.atom_order_symmetry,
        args.live_polarity,
    )
    args.metadata.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
