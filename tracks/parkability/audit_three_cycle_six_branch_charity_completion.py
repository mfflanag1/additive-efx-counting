#!/usr/bin/env python3
"""Audit the six branching completions of the three-cycle survivor."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


CYCLE = (("r", "q"), ("q", "s"), ("s", "r"))


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(d_target, omitted_source):
    assert d_target in ("r", "q")
    active = tuple(edge for edge in CYCLE if edge[0] != omitted_source)
    assert len(active) == 2
    core = {edge: f"D[{edge[0]}->{edge[1]}]" for edge in CYCLE}
    d_core = f"C[d->{d_target}]"
    residual = {owner: f"R[{owner}]" for owner in ("r", "q", "d", "s")}
    p = "p"

    initial = {owner: {residual[owner]} for owner in residual}
    initial["charity"] = {p}
    for edge, atom in core.items():
        initial[edge[1]].add(atom)
    initial[d_target].add(d_core)

    final = {owner: {residual[owner]} for owner in residual}
    final["charity"] = set()
    final[omitted_source].add(p)
    final["d"].add(d_core)
    for edge, atom in core.items():
        source, target = edge
        if edge in active:
            final[source].add(atom)
        else:
            final[target].add(atom)

    before = {atom: owner for owner, atoms in initial.items() for atom in atoms}
    after = {atom: owner for owner, atoms in final.items() for atom in atoms}
    assert set(before) == set(after)
    edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected = {
        (target, source) for source, target in active
    } | {(d_target, "d"), ("charity", omitted_source)}
    assert set(edges) == expected
    assert len(edges) == 4

    incoming_to_d_target = next(edge for edge in CYCLE if edge[1] == d_target)
    overlap_needed = incoming_to_d_target in active
    return {
        "d_core_target": d_target,
        "omitted_cycle_source": omitted_source,
        "active_cycle_responses": [list(edge) for edge in active],
        "transfer_edges": [list(edge) for edge in edges],
        "d_core_cycle_disjointness_required": overlap_needed,
        "checks": {
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "exactly_four_support_edges": len(edges) == 4,
            "two_cycle_sources_receive_desired_cores": all(
                core[edge] in final[edge[0]] for edge in active
            ),
            "d_receives_desired_core": d_core in final["d"],
            "omitted_source_receives_charity": p in final[omitted_source],
        },
    }


def run(root: Path):
    records = [
        construct(target, omitted)
        for target in ("r", "q") for omitted in ("r", "q", "s")
    ]
    assert len(records) == 6
    assert all(all(record["checks"].values()) for record in records)
    assert sum(record["d_core_cycle_disjointness_required"] for record in records) == 4

    desired, base, extra, final = z3.Reals("desired base extra final")
    selected_payment = prove(
        [desired > base, extra >= 0, final == desired + extra], final > base
    )
    delta, loss, charity, margin = z3.Reals("delta loss charity margin")
    endpoint_identity = prove(
        [margin == delta - loss + charity], margin == delta - loss + charity
    )
    endpoint_capture = prove(
        [delta >= 0, charity >= 0, margin == delta - loss + charity, margin < 0],
        loss > delta + charity,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md"
    return {
        "schema": "three-cycle-six-branch-charity-completion-v1",
        "status": "SIX_CAP_FREE_BRANCHING_COMPLETIONS_CONSTRUCTED",
        "records": records,
        "checks": {
            "all_support_checks": True,
            "selected_sources_strictly_paid": selected_payment,
            "omitted_source_margin_identity": endpoint_identity,
            "failed_omitted_source_is_strict_capture": endpoint_capture,
            "branches_without_shared_target_overlap": sum(
                not record["d_core_cycle_disjointness_required"] for record in records
            ),
        },
        "exact_remaining_gate": (
            "among six branches, select one whose omitted paid-cycle source has "
            "nonnegative signed margin and whose changed targets are observer-safe; "
            "or convert all six capture/overlap failures into a saturated exit"
        ),
        "claim_boundary": (
            "cap-free support and three-owner payment normal form; it does not "
            "prove one of six endpoint margins and observer budgets succeeds"
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
    print(json.dumps({"status": result["status"], "branches": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
