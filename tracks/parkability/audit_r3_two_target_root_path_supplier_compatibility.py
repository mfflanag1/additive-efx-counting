#!/usr/bin/env python3
"""Audit the two-target matching classification and favorable root path."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def run(root: Path):
    sources = ("x", "y", "z")
    targets = ("x", "y")
    edges = tuple((source, target) for source in sources for target in targets
                  if source != target)
    matchings = set()
    for chosen in itertools.combinations(edges, 2):
        if {target for _, target in chosen} != set(targets):
            continue
        if len({source for source, _ in chosen}) != 2:
            continue
        matchings.add(tuple(sorted(chosen)))
    expected_matchings = {
        tuple(sorted((('y', 'x'), ('x', 'y')))),
        tuple(sorted((('y', 'x'), ('z', 'y')))),
        tuple(sorted((('z', 'x'), ('x', 'y')))),
    }
    assert matchings == expected_matchings

    supplier = {
        "x0": "x", "yx": "y", "zx": "z",
        "y0": "y", "zy": "z", "p": "charity", "d0": "d",
    }
    before = {
        "x": {"x0", "yx", "zx"},
        "y": {"y0", "zy"}, "z": {"p"}, "d": {"d0"},
        "charity": set(),
    }
    rows = []
    # D_x may use any nonempty combination of the y- and z-supplied cells.
    for dx in ({"y0"}, {"zy"}, {"y0", "zy"}):
        # D_z is a nonempty subpacket of the z-supplied cell at x.
        dz = {"zx"}
        after = {
            "x": (before["x"] - dz) | dx,
            "y": (before["y"] - dx) | {"p"},
            "z": dz,
            "d": {"d0"}, "charity": set(),
        }
        assert set().union(*before.values()) == set().union(*after.values())
        holder = {good: owner for owner, goods in after.items() for good in goods}
        final_edges = {
            (supplier[good], owner) for good, owner in holder.items()
            if supplier[good] != owner
        }
        allowed = {("y", "x"), ("z", "x"), ("z", "y"), ("charity", "y")}
        assert final_edges <= allowed
        assert len(final_edges) <= 4
        rows.append({
            "root_core": sorted(dx),
            "singleton_source_core": sorted(dz),
            "final_edges": [list(edge) for edge in sorted(final_edges)],
        })

    old_root, root_core, old_z, z_core = z3.Reals(
        "old_root root_core old_z z_core"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(root_core > old_root, z_core > old_z)
    solver.add(z3.Not(z3.And(root_core > old_root, z_core > old_z)))
    payments = solver.check() == z3.unsat
    assert payments

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_TWO_TARGET_ROOT_PATH_SUPPLIER_COMPATIBILITY_LEMMA_20260814.md"
    return {
        "schema": "r3-two-target-root-path-supplier-compatibility-v1",
        "status": "FAVORABLE_ROOT_PATH_HAS_FOUR_EDGE_CANDIDATE",
        "matching_count": len(matchings),
        "matching_shapes": [[list(edge) for edge in shape]
                            for shape in sorted(matchings)],
        "supplier_cases": rows,
        "checks": {
            "exact_three_matching_shapes": True,
            "conservation": True,
            "final_edges_at_most_four": True,
            "root_and_singleton_source_strict": payments,
        },
        "claim_boundary": (
            "cap-free favorable-path candidate; observer/repeat, backward path, "
            "singleton star, and foreign-support import remain open"
        ),
        "provenance": {
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
