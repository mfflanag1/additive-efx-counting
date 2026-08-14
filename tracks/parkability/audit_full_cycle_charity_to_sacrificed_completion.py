#!/usr/bin/env python3
"""Audit full paid-cycle rotation with charity donated to sacrificed d."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


CASES = {
    "two_cycle": {
        "cycle": (("r", "q"), ("q", "r")),
        "extra": (("s", "d"),),
    },
    "three_cycle": {
        "cycle": (("r", "q"), ("q", "s"), ("s", "r")),
        "extra": (),
    },
}


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(kind, data):
    selected = (*data["cycle"], *data["extra"])
    core = {edge: f"D[{edge[0]}->{edge[1]}]" for edge in selected}
    residual = {owner: f"R[{owner}]" for owner in ("r", "q", "d", "s")}
    p = "p"
    initial = {owner: {residual[owner]} for owner in residual}
    initial["charity"] = {p}
    for edge, atom in core.items():
        initial[edge[1]].add(atom)
    final = {owner: {residual[owner]} for owner in residual}
    final["charity"] = set()
    final["d"].add(p)
    for edge, atom in core.items():
        final[edge[0]].add(atom)
    before = {atom: owner for owner, atoms in initial.items() for atom in atoms}
    after = {atom: owner for owner, atoms in final.items() for atom in atoms}
    assert set(before) == set(after)
    edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected = {(target, source) for source, target in selected} | {("charity", "d")}
    assert set(edges) == expected
    assert len(edges) == 4
    return {
        "kind": kind,
        "selected_responses": [list(edge) for edge in selected],
        "transfer_edges": [list(edge) for edge in edges],
        "d_loses_response_core": bool(data["extra"]),
        "checks": {
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "exactly_four_support_edges": len(edges) == 4,
            "every_selected_source_receives_desired_core": all(
                core[edge] in final[edge[0]] for edge in selected
            ),
            "d_receives_charity": p in final["d"],
        },
    }


def run(root: Path):
    records = [construct(kind, data) for kind, data in CASES.items()]
    assert all(all(record["checks"].values()) for record in records)
    desired, base, extra, final = z3.Reals("desired base extra final")
    selected_payment = prove(
        [desired > base, extra >= 0, final == desired + extra], final > base
    )
    delta, loss, charity, margin = z3.Reals("delta loss charity margin")
    d_identity = prove(
        [margin == delta - loss + charity], margin == delta - loss + charity
    )
    d_failure = prove(
        [charity >= 0, margin == delta - loss + charity, margin < 0],
        loss > delta + charity,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/FULL_CYCLE_CHARITY_TO_SACRIFICED_COMPLETION_LEMMA_20260813.md"
    return {
        "schema": "full-cycle-charity-to-sacrificed-completion-v1",
        "status": "BOTH_FULL_CYCLE_D_ENDPOINTS_CONSTRUCTED",
        "records": records,
        "checks": {
            "all_support_checks": True,
            "selected_sources_strictly_paid": selected_payment,
            "d_margin_identity": d_identity,
            "d_failure_is_strict_deficit_or_capture": d_failure,
        },
        "exact_remaining_gate": (
            "two-cycle: eliminate d's lost-W-core capture; three-cycle: eliminate "
            "the bare residual deficit v_d(W)+v_d(p)<v_d(X_d), jointly with the "
            "represented-owner endpoint failures"
        ),
        "claim_boundary": (
            "cap-free four-edge support and all-non-d payment lemma; it does not "
            "prove d is paid or final targets are observer-safe"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
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
    print(json.dumps({"status": result["status"], "cases": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
