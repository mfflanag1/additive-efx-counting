#!/usr/bin/env python3
"""Audit partial returns while the singleton stays at its owner."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import z3


NONE, PROPER, ALL = 0, 1, 2


def edge_count(lx, ly, lz):
    # charity->z and the nonempty W cell z->y are mandatory.
    return 2 + sum((
        lx != NONE,
        ly != ALL,
        ly != NONE,
        lz != ALL,
    ))


def run(root: Path):
    rows = []
    obstruction = []
    minimum_edge_distribution = Counter()
    for response in itertools.product((NONE, PROPER, ALL), repeat=3):
        if response == (NONE, NONE, NONE):
            continue
        options = [tuple(range(state + 1)) for state in response]
        feasible = []
        for returned in itertools.product(*options):
            if returned == (NONE, NONE, NONE):
                continue
            count = edge_count(*returned)
            if count <= 4:
                feasible.append((returned, count))
        minimum = min((count for _, count in feasible), default=None)
        if minimum is None:
            obstruction.append(response)
        else:
            minimum_edge_distribution[minimum] += 1
        predicted = response[2] != NONE or response[1] == ALL
        assert bool(feasible) == predicted
        rows.append({
            "response_signature": list(response),
            "has_four_edge_partial_return": bool(feasible),
            "minimum_edge_count": minimum,
            "feasible_returns": [
                {"signature": list(signature), "edge_count": count}
                for signature, count in feasible
            ],
        })
    expected_obstruction = {
        (NONE, PROPER, NONE),
        (PROPER, NONE, NONE),
        (PROPER, PROPER, NONE),
        (ALL, NONE, NONE),
        (ALL, PROPER, NONE),
    }
    assert len(rows) == 26
    assert sum(row["has_four_edge_partial_return"] for row in rows) == 21
    assert set(obstruction) == expected_obstruction
    assert minimum_edge_distribution == {3: 9, 4: 12}

    # Atom-level replay of every returned signature used above.
    states = {NONE: set(), PROPER: {0}, ALL: {0, 1}}
    for row in rows:
        for feasible in row["feasible_returns"]:
            lx, ly, lz = feasible["signature"]
            cells = {
                "X": {"X0", "X1"}, "U": {"U0", "U1"},
                "V": {"V0", "V1"}, "W": {"W0", "W1"},
                "Y": {"Y0", "Y1"},
            }
            returned = set()
            for name, state in zip(("X", "U", "V"), (lx, ly, lz)):
                returned |= {sorted(cells[name])[index] for index in states[state]}
            supplier_owner = {"X": "x", "U": "y", "V": "z", "Y": "y", "W": "z"}
            supplier = {good: supplier_owner[name]
                        for name, goods in cells.items() for good in goods}
            supplier["p"] = "charity"
            bx = cells["X"] | cells["U"] | cells["V"]
            by = cells["Y"] | cells["W"]
            after = {"x": bx - returned, "y": by, "z": returned | {"p"}}
            edges = {
                (supplier[good], owner) for owner, goods in after.items() for good in goods
                if supplier[good] != owner
            }
            assert len(edges) == feasible["edge_count"]

    root_before, base, loss, root_after = z3.Reals(
        "root_before base loss root_after"
    )
    delta = root_before - base
    solver = z3.SolverFor("QF_LRA")
    solver.add(root_before > base, root_after == root_before - loss,
               loss < delta, root_after <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(root_before > base, root_after == root_before - loss,
               root_after > base, loss >= delta)
    reverse = solver.check() == z3.unsat
    assert forward and reverse

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_SINGLETON_RETAINED_PARTIAL_RETURN_TOPOLOGY_OR_ROOT_CAPTURE_LEMMA_20260814.md"
    return {
        "schema": "r3-singleton-retained-partial-return-v1",
        "status": "PARTIAL_RETURN_OR_ROOT_MARGIN_CAPTURE",
        "response_signature_count": len(rows),
        "signatures_with_four_edge_partial_return": 21,
        "minimum_edge_distribution": {
            str(k): v for k, v in sorted(minimum_edge_distribution.items())
        },
        "obstruction_signatures": [list(item) for item in sorted(obstruction)],
        "root_payment_equivalence": forward and reverse,
        "rows": rows,
        "claim_boundary": (
            "cap-free partial-return topology and root capture; five signatures, "
            "observer/repeat, backward path, and singleton star remain open"
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
        "covered": result["signatures_with_four_edge_partial_return"],
        "obstructions": len(result["obstruction_signatures"]),
    }, indent=2))


if __name__ == "__main__":
    main()
