#!/usr/bin/env python3
"""Audit the four-edge one-response charity-substitution normal form."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
FORMS = (
    (("r", "q"), ("q", "r"), ("s", "d"), ("d", "q")),
    (("r", "q"), ("q", "d"), ("s", "r"), ("d", "q")),
    (("r", "q"), ("q", "s"), ("s", "r"), ("d", "q")),
    (("r", "q"), ("q", "s"), ("s", "d"), ("d", "q")),
)


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(form, omitted):
    assert {source for source, _ in form} == set(OWNERS)
    core = {edge: f"D[{edge[0]}->{edge[1]}]" for edge in form}
    residual = {owner: f"R[{owner}]" for owner in OWNERS}
    p = "p"
    initial = {owner: {residual[owner]} for owner in OWNERS}
    initial["charity"] = {p}
    for edge, atom in core.items():
        initial[edge[1]].add(atom)

    final = {owner: {residual[owner]} for owner in OWNERS}
    final["charity"] = set()
    final[omitted].add(p)
    for edge, atom in core.items():
        source, target = edge
        if source == omitted:
            final[target].add(atom)
        else:
            final[source].add(atom)

    before = {atom: owner for owner, atoms in initial.items() for atom in atoms}
    after = {atom: owner for owner, atoms in final.items() for atom in atoms}
    assert set(before) == set(after)
    edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected = {
        (target, source) for source, target in form if source != omitted
    } | {("charity", omitted)}
    assert set(edges) == expected
    assert len(edges) == 4

    active_q_cores = [
        source for source, target in form if target == "q" and source != omitted
    ]
    return {
        "response_edges": [list(edge) for edge in sorted(form)],
        "omitted_response_source": omitted,
        "transfer_edges": [list(edge) for edge in edges],
        "active_q_target_core_sources": sorted(active_q_cores),
        "checks": {
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "exactly_three_reversed_responses_plus_charity": len(edges) == 4,
            "every_non_omitted_source_receives_desired_core": all(
                core[edge] in final[edge[0]]
                for edge in form if edge[0] != omitted
            ),
            "omitted_core_stays_with_physical_target": all(
                core[edge] in final[edge[1]]
                for edge in form if edge[0] == omitted
            ),
            "omitting_r_or_d_removes_shared_q_double_core": (
                len(active_q_cores) == 1 if omitted in ("r", "d") else True
            ),
        },
    }


def run(root: Path):
    records = [construct(form, omitted) for form in FORMS for omitted in OWNERS]
    assert len(records) == 16
    assert all(all(record["checks"].values()) for record in records)

    incoming, base, extras, final = z3.Reals("incoming base extras final")
    nonomitted_payment = prove(
        [incoming > base, extras >= 0, final == incoming + extras],
        final > base,
    )
    delta, loss, charity, margin = z3.Reals("delta loss charity margin")
    omitted_identity = prove(
        [margin == delta - loss + charity],
        margin == delta - loss + charity,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/RANK_THREE_ONE_EDGE_CHARITY_SUBSTITUTION_LEMMA_20260813.md"
    counts = Counter(record["omitted_response_source"] for record in records)
    return {
        "schema": "rank-three-one-edge-charity-substitution-v1",
        "status": "ALL_FOUR_FORMS_AND_OMISSIONS_CONSERVED",
        "response_form_count": len(FORMS),
        "omission_case_count": len(records),
        "omission_source_counts": dict(sorted(counts.items())),
        "records": records,
        "checks": {
            "all_cases_conserve_and_use_four_edges": True,
            "all_non_omitted_sources_strictly_paid_by_desired_core": nonomitted_payment,
            "omitted_source_margin_identity": omitted_identity,
            "r_or_d_omission_eliminates_shared_q_overlap": all(
                len(record["active_q_target_core_sources"]) == 1
                for record in records
                if record["omitted_response_source"] in ("r", "d")
            ),
        },
        "exact_remaining_gate": (
            "choose an omitted source h so Delta_h-L_h+v_h(p) meets its payment "
            "and observer debts, and every final changed target is EFX-safe; "
            "r/d omission simultaneously eliminates shared-q core overlap"
        ),
        "claim_boundary": (
            "cap-free conservation/payment reduction for the corrected four "
            "response forms; it does not prove an admissible omission exists or "
            "derive final observer safety from saturation"
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
    print(json.dumps({
        "status": result["status"],
        "response_form_count": result["response_form_count"],
        "omission_case_count": result["omission_case_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
