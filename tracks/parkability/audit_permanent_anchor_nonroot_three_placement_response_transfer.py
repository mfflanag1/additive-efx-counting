#!/usr/bin/env python3
"""Audit bounded-edge transfer from three nonroot singleton placements."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")


def run(root: Path):
    rows = []
    for target in OWNERS:
        for source in OWNERS:
            if source == target:
                continue
            component_choices = ((1,),)
            if target == "r":
                component_choices = tuple(
                    states for states in itertools.product((0, 1, 2), repeat=2)
                    if states != (0, 0)
                )
            for components in component_choices:
                supplier = {
                    "yr0": "r", "yr1": "r", "a0": "q", "a1": "q", "yq": "q",
                    "yd": "d", "ys": "s", "p": "charity",
                }
                base = {
                    "r": {"yr0", "yr1", "a0", "a1"}, "q": {"yq"},
                    "d": {"yd"}, "s": {"ys"}, "charity": {"p"},
                }
                target_cells = {
                    "r": (("yr0", "yr1"), ("a0", "a1")), "q": (("yq",),),
                    "d": (("yd",),), "s": (("ys",),),
                }
                core = set()
                for cell, state in zip(target_cells[target], components):
                    core.update(cell[:state])
                assert core
                final = {owner: set(goods) for owner, goods in base.items()}
                final["charity"].remove("p")
                p_holder = target if target != "r" else next(
                    owner for owner in OWNERS if owner != "r" and owner != source
                )
                final[p_holder].add("p")
                final[target] -= core
                final[source] |= core
                assert set().union(*base.values()) == set().union(*final.values())
                edges = {
                    (supplier[good], owner)
                    for owner, goods in final.items() for good in goods
                    if supplier[good] != owner
                }
                assert len(edges) <= 4
                rows.append({
                    "source": source,
                    "target": target,
                    "core": sorted(core),
                    "edges": [list(edge) for edge in sorted(edges)],
                    "edge_count": len(edges),
                })
    # Nine nonroot-target cases plus 24 mixed-root cases.
    assert len(rows) == 33
    assert max(row["edge_count"] for row in rows) == 4

    before, base, core, after = z3.Reals(
        "before base core after"
    )
    delta = before - base
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - core,
               core < delta, after <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - core,
               after > base, core >= delta)
    reverse = solver.check() == z3.unsat
    own, desired, final_source = z3.Reals("own desired final_source")
    solver = z3.SolverFor("QF_LRA")
    solver.add(own >= 0, desired > own, final_source == own + desired,
               final_source <= own)
    source_strict = solver.check() == z3.unsat
    assert forward and reverse and source_strict

    script = Path(__file__).resolve()
    theorem = root / "results" / "PERMANENT_ANCHOR_NONROOT_THREE_PLACEMENT_RESPONSE_TRANSFER_LEMMA_20260814.md"
    return {
        "schema": "permanent-anchor-nonroot-three-placement-response-transfer-v1",
        "status": "DISJOINT_RESPONSE_GIVES_FOUR_EDGE_PROBE_OR_ROOT_CAPTURE",
        "case_count": len(rows),
        "maximum_edge_count": max(row["edge_count"] for row in rows),
        "root_payment_equivalence": forward and reverse,
        "response_source_strict": source_strict,
        "cases": rows,
        "claim_boundary": (
            "cap-free response-transfer probe; root capture, exact response "
            "repeat, and global transition composition remain open"
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
