#!/usr/bin/env python3
"""Audit universal incoming-cell return while z retains singleton p."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def physical_edges(supplier, allocation):
    return {
        (supplier[good], owner)
        for owner, goods in allocation.items()
        for good in goods
        if supplier[good] != owner
    }


def run(root: Path):
    rows = []
    for u_present, v_present, w_present in itertools.product((False, True), repeat=3):
        supplier = {"x0": "x", "p": "charity", "y0": "y"}
        before = {"x": {"x0"}, "y": {"y0"}, "z": {"p"}, "d": {"d0"}}
        supplier["d0"] = "d"
        if u_present:
            before["x"].update({"u0", "u1"})
            supplier.update({"u0": "y", "u1": "y"})
        if v_present:
            before["x"].update({"v0", "v1"})
            supplier.update({"v0": "z", "v1": "z"})
        if w_present:
            before["y"].add("w0")
            supplier["w0"] = "z"

        candidates = []
        if v_present:
            candidates.extend(({"v0"}, {"v1"}))
        if u_present:
            candidates.append({"u0", "u1"})
        if not u_present and not v_present:
            candidates.append({"x0"})
        assert candidates

        candidate_rows = []
        for packet in candidates:
            after = {owner: set(goods) for owner, goods in before.items()}
            after["x"] -= packet
            after["z"] |= packet
            assert set().union(*before.values()) == set().union(*after.values())
            edges = physical_edges(supplier, after)
            assert len(edges) <= 4
            candidate_rows.append({
                "packet": sorted(packet),
                "edges": [list(edge) for edge in sorted(edges)],
                "edge_count": len(edges),
            })
        rows.append({
            "u_present": u_present,
            "v_present": v_present,
            "w_present": w_present,
            "candidate_count": len(candidate_rows),
            "candidates": candidate_rows,
        })
    assert len(rows) == 8
    assert all(row["candidate_count"] >= 1 for row in rows)

    before, base, packet, after = z3.Reals("before base packet after")
    delta = before - base
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - packet,
               packet < delta, after <= base)
    forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(before > base, after == before - packet,
               after > base, packet >= delta)
    reverse = solver.check() == z3.unsat
    gain, old_z, new_z = z3.Reals("gain old_z new_z")
    solver = z3.SolverFor("QF_LRA")
    solver.add(gain > 0, new_z == old_z + gain, new_z <= old_z)
    z_strict = solver.check() == z3.unsat
    assert forward and reverse and z_strict

    script = Path(__file__).resolve()
    theorem = root / "results" / "R3_SINGLETON_RETAINED_INCOMING_CELL_RETURN_LEMMA_20260814.md"
    return {
        "schema": "r3-singleton-retained-incoming-cell-return-v1",
        "status": "ALL_SUPPORT_SIGNATURES_HAVE_RETURN_OR_ROOT_CAPTURE",
        "presence_pattern_count": len(rows),
        "all_patterns_have_candidate": True,
        "all_candidates_at_most_four_edges": True,
        "root_payment_equivalence": forward and reverse,
        "singleton_owner_strict": z_strict,
        "patterns": rows,
        "claim_boundary": (
            "cap-free topology closure; root-critical incoming support and "
            "observer/repeat continuation remain open"
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
        "patterns": result["presence_pattern_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
