#!/usr/bin/env python3
"""Audit minimum-good diversion from a permanent-anchor root target."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


OWNERS = ("q", "d", "s")


def run(root: Path):
    rows = []
    for source in OWNERS:
        for good in ("yr", "a0", "a1"):
            supplier = {
                "yr": "r", "a0": "q", "a1": "q", "yq": "q",
                "yd": "d", "ys": "s", "p": "charity",
            }
            before = {
                "r": {"yr", "a0", "a1"}, "q": {"yq"},
                "d": {"yd"}, "s": {"ys"}, "charity": {"p"},
            }
            after = {owner: set(goods) for owner, goods in before.items()}
            after["r"].remove(good)
            after["charity"].remove("p")
            after[source].update({good, "p"})
            assert set().union(*before.values()) == set().union(*after.values())
            edges = {
                (supplier[item], owner)
                for owner, goods in after.items() for item in goods
                if supplier[item] != owner
            }
            assert len(edges) <= 3
            rows.append({
                "source": source,
                "diverted_good": good,
                "edges": [list(edge) for edge in sorted(edges)],
                "edge_count": len(edges),
            })
    assert len(rows) == 9
    assert max(row["edge_count"] for row in rows) == 3

    before, base, good, after = z3.Reals("before base good after")
    delta = before - base
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - good,
               good < delta, after <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - good,
               after > base, good >= delta)
    reverse = solver.check() == z3.unsat
    minimum, other = z3.Reals("minimum other")
    solver = z3.SolverFor("QF_LRA")
    solver.add(minimum >= delta, other >= minimum, other < delta)
    itemwise = solver.check() == z3.unsat
    gain, old_source, new_source = z3.Reals("gain old_source new_source")
    solver = z3.SolverFor("QF_LRA")
    solver.add(gain > 0, new_source == old_source + gain,
               new_source <= old_source)
    source_strict = solver.check() == z3.unsat
    assert forward and reverse and itemwise and source_strict

    script = Path(__file__).resolve()
    theorem = root / "results" / "PERMANENT_ANCHOR_ROOT_TARGET_MINIMUM_GOOD_DIVERSION_LEMMA_20260814.md"
    return {
        "schema": "permanent-anchor-root-target-minimum-good-diversion-v1",
        "status": "THREE_EDGE_PROBE_OR_ITEMWISE_ROOT_CAPTURE",
        "case_count": len(rows),
        "maximum_edge_count": max(row["edge_count"] for row in rows),
        "root_payment_equivalence": forward and reverse,
        "itemwise_capture": itemwise,
        "source_strict": source_strict,
        "cases": rows,
        "claim_boundary": (
            "cap-free minimum-good diversion; item-critical envelope and exact "
            "response recurrence remain open"
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
        "status": result["status"], "cases": result["case_count"],
        "maximum_edges": result["maximum_edge_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
