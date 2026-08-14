#!/usr/bin/env python3
"""Audit the cap-free branching completion of the two-cycle survivor."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(d_target):
    assert d_target in ("r", "q")
    other = "q" if d_target == "r" else "r"
    atoms = {
        "r_cycle": "D[r->q]",
        "q_cycle": "D[q->r]",
        "d_core": f"C[d->{d_target}]",
        "r_residual": "R[r]",
        "q_residual": "R[q]",
        "d_bundle": "Y[d]",
        "s_bundle": "Y[s]",
        "charity": "p",
    }
    initial = {
        "r": {atoms["q_cycle"], atoms["r_residual"]},
        "q": {atoms["r_cycle"], atoms["q_residual"]},
        "d": {atoms["d_bundle"]},
        "s": {atoms["s_bundle"]},
        "charity": {atoms["charity"]},
    }
    # The d-core is a disjoint atom carved from its physical target residual.
    residual_key = f"{d_target}_residual"
    initial[d_target].remove(atoms[residual_key])
    initial[d_target].update({atoms["d_core"], atoms[residual_key]})

    final = {
        "r": {atoms["r_cycle"], atoms["r_residual"]},
        "q": {atoms["q_cycle"], atoms["q_residual"]},
        "d": {atoms["d_bundle"], atoms["d_core"]},
        "s": {atoms["s_bundle"], atoms["charity"]},
        "charity": set(),
    }
    # The target residual excludes the d-core after it moves.
    final[d_target].discard(atoms["d_core"])

    before = {atom: owner for owner, goods in initial.items() for atom in goods}
    after = {atom: owner for owner, goods in final.items() for atom in goods}
    assert set(before) == set(after)
    edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected = {("q", "r"), ("r", "q"), (d_target, "d"), ("charity", "s")}
    assert set(edges) == expected
    assert len(edges) == 4
    return {
        "d_core_target": d_target,
        "transfer_edges": [list(edge) for edge in edges],
        "checks": {
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "exactly_four_support_edges": len(edges) == 4,
            "r_receives_desired_cycle_core": atoms["r_cycle"] in final["r"],
            "q_receives_desired_cycle_core": atoms["q_cycle"] in final["q"],
            "d_receives_desired_core": atoms["d_core"] in final["d"],
            "s_keeps_paid_bundle_and_receives_charity": (
                {atoms["s_bundle"], atoms["charity"]} <= final["s"]
            ),
        },
    }


def run(root: Path):
    records = [construct(target) for target in ("r", "q")]
    assert all(all(record["checks"].values()) for record in records)
    desired, base, extra, final = z3.Reals("desired base extra final")
    desired_payment = prove(
        [desired > base, extra >= 0, final == desired + extra], final > base
    )
    current, current_base, charity, s_final = z3.Reals(
        "current current_base charity s_final"
    )
    retained_payment = prove(
        [current >= current_base, charity > 0, s_final == current + charity],
        s_final > current_base,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/TWO_CYCLE_BRANCHING_CHARITY_COMPLETION_LEMMA_20260813.md"
    return {
        "schema": "two-cycle-branching-charity-completion-v1",
        "status": "TWO_DISJOINT_BRANCHING_COMPLETIONS_CONSTRUCTED",
        "records": records,
        "checks": {
            "all_support_checks": True,
            "desired_core_recipients_strictly_paid": desired_payment,
            "retained_s_plus_positive_charity_strictly_paid": retained_payment,
        },
        "exact_remaining_gate": (
            "either find a d-response core disjoint from the corresponding r/q "
            "cycle core, or prove that simultaneous full-margin overlap capture "
            "at both r and q activates a saturated exit"
        ),
        "claim_boundary": (
            "cap-free support and payment lemma conditional on disjoint selected "
            "cores and final observer safety; it does not reverse simultaneous "
            "overlap capture or prove EFX safety"
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
