#!/usr/bin/env python3
"""Audit the direct singleton-source return and exact edge criterion."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


NONE, PROPER, ALL = 0, 1, 2


def direct_edges(ax, ay, az):
    owner_indicators = {
        "x_to_z": ax != NONE,
        "y_to_x": ay != ALL,
        "y_to_z": ay != NONE,
        "z_to_x": az != ALL,
    }
    # charity->x and the nonempty W cell z->y are mandatory.
    return owner_indicators, 2 + sum(owner_indicators.values())


def full_edges(ax, ay, az, cy, cz):
    return 1 + sum((
        ax != NONE,
        ay != ALL or cy != NONE,
        ay != NONE,
        az != ALL or cz != NONE,
        cz != ALL,
    ))


def run(root: Path):
    signatures = []
    distribution = Counter()
    for signature in itertools.product((NONE, PROPER, ALL), repeat=3):
        if signature == (NONE, NONE, NONE):
            continue
        indicators, edge_count = direct_edges(*signature)
        distribution[edge_count] += 1
        signatures.append({
            "signature": list(signature),
            "indicators": indicators,
            "edge_count": edge_count,
            "four_edge_feasible": edge_count <= 4,
        })
    assert len(signatures) == 26
    assert distribution == {3: 2, 4: 8, 5: 12, 6: 4}
    assert sum(row["four_edge_feasible"] for row in signatures) == 10

    full_feasible = direct_feasible = union_feasible = rescued = 0
    five_cell_count = 0
    for ax, ay, az, cy, cz in itertools.product((NONE, PROPER, ALL), repeat=5):
        if ax == ay == az == NONE or cy == cz == NONE:
            continue
        five_cell_count += 1
        full_ok = full_edges(ax, ay, az, cy, cz) <= 4
        direct_ok = direct_edges(ax, ay, az)[1] <= 4
        full_feasible += full_ok
        direct_feasible += direct_ok
        union_feasible += full_ok or direct_ok
        rescued += (not full_ok) and direct_ok
    assert five_cell_count == 208
    assert (full_feasible, direct_feasible, union_feasible, rescued) == (69, 80, 102, 33)

    # Atom-level replay for all 26 signatures.
    states = {NONE: set(), PROPER: {0}, ALL: {0, 1}}
    for row in signatures:
        ax, ay, az = row["signature"]
        cells = {
            "X": {"X0", "X1"}, "U": {"U0", "U1"},
            "V": {"V0", "V1"}, "W": {"W0", "W1"},
            "Y": {"Y0", "Y1"},
        }
        picks = {}
        for name, state in zip(("X", "U", "V"), (ax, ay, az)):
            picks[name] = {sorted(cells[name])[index] for index in states[state]}
        supplier_owner = {"X": "x", "U": "y", "V": "z", "Y": "y", "W": "z"}
        supplier = {good: supplier_owner[name]
                    for name, goods in cells.items() for good in goods}
        supplier["p"] = "charity"
        bx = cells["X"] | cells["U"] | cells["V"]
        by = cells["Y"] | cells["W"]
        dz = picks["X"] | picks["U"] | picks["V"]
        after = {"x": (bx - dz) | {"p"}, "y": by, "z": dz}
        edges = {
            (supplier[good], owner) for owner, goods in after.items() for good in goods
            if supplier[good] != owner
        }
        assert len(edges) == row["edge_count"]

    bx, base, core, singleton, final = z3.Reals(
        "bx base core singleton final"
    )
    delta = bx - base
    # Check both directions of the strict-root equivalence separately.
    solver = z3.SolverFor("QF_LRA")
    solver.add(bx > base, final == bx - core + singleton,
               core < delta + singleton, final <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(bx > base, final == bx - core + singleton,
               final > base, core >= delta + singleton)
    reverse = solver.check() == z3.unsat
    assert forward and reverse

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_SINGLETON_SOURCE_ROOT_COMPENSATED_DIRECT_RETURN_LEMMA_20260814.md"
    return {
        "schema": "r3-singleton-source-root-compensated-direct-return-v1",
        "status": "DIRECT_RETURN_OR_ROOT_MARGIN_CHARITY_CAPTURE",
        "signature_count": len(signatures),
        "edge_distribution": {str(k): v for k, v in sorted(distribution.items())},
        "direct_four_edge_feasible": 10,
        "five_cell_full_path_feasible": full_feasible,
        "five_cell_direct_path_feasible": direct_feasible,
        "five_cell_union_feasible": union_feasible,
        "five_cell_rescued_by_direct": rescued,
        "root_payment_equivalence": forward and reverse,
        "signatures": signatures,
        "claim_boundary": (
            "cap-free direct selector and exact root capture; edge-overflow, "
            "observer/repeat, backward path, and star remain open"
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
    print(json.dumps({
        "status": result["status"],
        "direct_feasible": result["direct_four_edge_feasible"],
        "union_feasible": result["five_cell_union_feasible"],
    }, indent=2))


if __name__ == "__main__":
    main()
