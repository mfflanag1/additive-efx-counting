#!/usr/bin/env python3
"""Audit exact edge indicators for the two-target favorable root path."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


NONE, PROPER, ALL = 0, 1, 2


def indicator_count(ax, ay, az, cy, cz):
    indicators = {
        "x_to_z": ax != NONE,
        "y_to_x": ay != ALL or cy != NONE,
        "y_to_z": ay != NONE,
        "z_to_x": az != ALL or cz != NONE,
        "z_to_y": cz != ALL,
    }
    return indicators, 1 + sum(indicators.values())


def run(root: Path):
    rows = []
    distribution = Counter()
    feasible = 0
    feasible_foreign = 0
    feasible_own_only = 0
    for signature in itertools.product((NONE, PROPER, ALL), repeat=5):
        ax, ay, az, cy, cz = signature
        if ax == ay == az == NONE or cy == cz == NONE:
            continue
        indicators, edge_count = indicator_count(*signature)
        distribution[edge_count] += 1
        is_feasible = edge_count <= 4
        foreign = ax != NONE or ay != NONE
        feasible += is_feasible
        feasible_foreign += is_feasible and foreign
        feasible_own_only += is_feasible and not foreign
        rows.append({
            "signature": list(signature),
            "indicators": indicators,
            "edge_count": edge_count,
            "four_edge_feasible": is_feasible,
            "uses_foreign_support": foreign,
        })
    assert len(rows) == 208
    assert feasible == 69
    assert feasible_foreign == 53
    assert feasible_own_only == 16
    assert distribution == {3: 11, 4: 58, 5: 93, 6: 46}

    # Independent atom-level replay of every signature.
    states = {NONE: set(), PROPER: {0}, ALL: {0, 1}}
    for row in rows:
        ax, ay, az, cy, cz = row["signature"]
        cells = {
            "X": {"X0", "X1"}, "U": {"U0", "U1"},
            "V": {"V0", "V1"}, "Y": {"Y0", "Y1"},
            "W": {"W0", "W1"},
        }
        picks = {}
        for name, state in zip(("X", "U", "V", "Y", "W"),
                               (ax, ay, az, cy, cz)):
            picks[name] = {sorted(cells[name])[index] for index in states[state]}
        supplier = {good: name for name, cell in cells.items() for good in cell}
        supplier.update({"p": "charity"})
        supplier_owner = {"X": "x", "U": "y", "V": "z", "Y": "y", "W": "z"}
        supplier = {good: supplier_owner.get(source, source)
                    for good, source in supplier.items()}
        bx = cells["X"] | cells["U"] | cells["V"]
        by = cells["Y"] | cells["W"]
        dz = picks["X"] | picks["U"] | picks["V"]
        dx = picks["Y"] | picks["W"]
        after = {
            "x": (bx - dz) | dx,
            "y": (by - dx) | {"p"},
            "z": dz,
        }
        physical_edges = {
            (supplier[good], owner) for owner, goods in after.items() for good in goods
            if supplier[good] != owner
        }
        assert len(physical_edges) == row["edge_count"]

    foreign, own_part, desired, singleton, margin = z3.Reals(
        "foreign own_part desired singleton margin"
    )
    solver = z3.SolverFor("QF_LRA")
    solver.add(desired == foreign + own_part, margin == desired - singleton,
               desired > singleton, own_part <= singleton)
    solver.add(z3.Not(foreign >= margin))
    margin_capture = solver.check() == z3.unsat
    assert margin_capture

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_TWO_TARGET_FOREIGN_IMPORT_EDGE_CANCELLATION_AND_MARGIN_LEMMA_20260814.md"
    return {
        "schema": "r3-two-target-foreign-import-edge-cancellation-v1",
        "status": "EXACT_FIVE_INDICATOR_EDGE_CRITERION",
        "signature_count": len(rows),
        "edge_distribution": {str(k): v for k, v in sorted(distribution.items())},
        "four_edge_feasible": feasible,
        "four_edge_feasible_with_foreign_support": feasible_foreign,
        "four_edge_feasible_own_support_only": feasible_own_only,
        "foreign_margin_capture": margin_capture,
        "rows": rows,
        "claim_boundary": (
            "cap-free edge identity and margin separator; incompatible foreign "
            "packets are not yet routed to PI/progress/base-margin admission"
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
        "feasible": result["four_edge_feasible"],
        "foreign_feasible": result["four_edge_feasible_with_foreign_support"],
    }, indent=2))


if __name__ == "__main__":
    main()
