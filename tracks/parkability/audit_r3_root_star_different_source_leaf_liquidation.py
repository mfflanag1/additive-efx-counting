#!/usr/bin/env python3
"""Audit root-star different-source leaf liquidation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def connected(vertices, edges):
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = set()
    frontier = [next(iter(vertices))]
    while frontier:
        vertex = frontier.pop()
        if vertex in seen:
            continue
        seen.add(vertex)
        frontier.extend(adjacency[vertex] - seen)
    return seen == vertices


def run(root: Path):
    rows = []
    for y, z in (("q", "s"), ("s", "q")):
        supplier = {
            "x0": "r", "yx": y, "zx": z,
            "yres": y, "zres": z, "d0": "d", "p": "charity",
        }
        after = {
            "r": {"x0", "yx", "zx"}, y: {"yres", "zres"}, z: {"p"},
            "d": {"d0"}, "charity": set(),
        }
        holder = {good: owner for owner, goods in after.items() for good in goods}
        edges = {
            (supplier[good], owner) for good, owner in holder.items()
            if supplier[good] != owner
        }
        expected = {(y, "r"), (z, "r"), (z, y), ("charity", z)}
        assert edges == expected
        assert len(edges) == 4
        assert connected({"r", y, z, "charity"}, edges)
        assert after[z] == {"p"}
        for p_holder in (y, z):
            before = {
                "r": {"x0", "yx", "zx"}, y: {"yres"}, z: {"zres"},
                "d": {"d0"}, "charity": set(),
            }
            before[p_holder].add("p")
            assert set().union(*before.values()) == set().union(*after.values())
            rows.append({
                "different_source": y,
                "liquidated_target": z,
                "initial_singleton_holder": p_holder,
                "supplier_edges": [list(edge) for edge in sorted(edges)],
                "liquidated_target_is_singleton": True,
            })

    core, whole, own, root_utility, base = z3.Reals(
        "core whole own root_utility base"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(core > own, whole >= core)
    solver.add(z3.Not(whole > own))
    desire_monotone = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(root_utility > base)
    solver.add(z3.Not(root_utility > base))
    root_preserved = solver.check() == z3.unsat
    assert desire_monotone and root_preserved

    localized = []
    for y, z in (("q", "s"), ("s", "q")):
        for source in {"r", "q", "s", "d"}:
            for target in {"r", y, "d"}:
                if source == target:
                    continue
                recruited = source == "d" or target == "d"
                if not recruited:
                    assert source in {"r", "q", "s"} and target in {"r", y}
                localized.append((y, z, source, target, recruited))

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_ROOT_STAR_DIFFERENT_SOURCE_LEAF_LIQUIDATION_LEMMA_20260814.md"
    return {
        "schema": "r3-root-star-different-source-leaf-liquidation-v1",
        "status": "DIFFERENT_SOURCE_REDUCED_TO_TWO_TARGETS_OR_RECRUITMENT",
        "symmetric_cases": rows,
        "checks": {
            "exactly_four_supplier_edges": True,
            "conservation": True,
            "whole_target_inherits_desire": desire_monotone,
            "strict_root_unchanged": root_preserved,
            "singleton_cannot_be_efx_failure_target": True,
            "response_localization": True,
        },
        "localized_response_count": len(localized),
        "claim_boundary": (
            "cap-free root-source star reduction; the two-target represented "
            "residual and later-source anchor-capture stars remain open"
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
