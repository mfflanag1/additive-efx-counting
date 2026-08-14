#!/usr/bin/env python3
"""Audit paid-cycle rotation with charity to sacrificed d."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


FORMS = {
    "R2": (("r", "q"), ("q", "r")),
    "R3": (("r", "q"), ("q", "s"), ("s", "r")),
}


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def construct(form, responses):
    owners = ("r", "q", "d", "s")
    initial = {owner: {f"bundle_{owner}"} for owner in owners}
    initial["charity"] = {"p"}
    cores = {}
    for source, target in responses:
        core = f"core_{source}_from_{target}"
        cores[source, target] = core
        initial[target].add(core)
    final = {owner: set(initial[owner]) for owner in owners}
    final["charity"] = set()
    for source, target in responses:
        core = cores[source, target]
        final[target].remove(core)
        final[source].add(core)
    final["d"].add("p")
    edges = {(target, source) for source, target in responses} | {("charity", "d")}
    represented = {source for source, _ in responses}
    return {
        "form": form,
        "responses": [list(edge) for edge in responses],
        "transfer_edges": [list(edge) for edge in sorted(edges)],
        "checks": {
            "charity_empty": not final["charity"],
            "atom_conservation": set().union(*initial.values()) == set().union(*final.values()),
            "functional_on_suppliers": len({source for source, _ in edges}) == len(edges),
            "edge_count": len(edges) == (3 if form == "R2" else 4),
            "d_keeps_old_bundle_and_receives_charity": initial["d"] < final["d"],
            "every_cycle_source_receives_desired_core": all(
                cores[source, target] in final[source] for source, target in responses
            ),
            "off_cycle_s_preserved_in_r2": form != "R2" or initial["s"] == final["s"],
            "represented_sources_are_cycle_sources": represented == (
                {"r", "q"} if form == "R2" else {"r", "q", "s"}
            ),
        },
    }


def run(root):
    records = [construct(form, responses) for form, responses in FORMS.items()]
    assert all(all(record["checks"].values()) for record in records)
    current, base, final = z3.Reals("current base final")
    retained_payment = prove([current >= base, final == current], final >= base)
    incoming, extras, paid_final = z3.Reals("incoming extras paid_final")
    desired_payment = prove(
        [incoming > base, extras >= 0, paid_final == incoming + extras],
        paid_final > base,
    )
    residual, charity, d_margin = z3.Reals("residual charity d_margin")
    d_identity = prove(
        [d_margin == residual + charity - base],
        d_margin == residual + charity - base,
    )
    d_failure = prove(
        [d_margin == residual + charity - base, d_margin < 0],
        residual + charity < base,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/PAID_CYCLE_CHARITY_TO_SACRIFICED_LEMMA_20260813.md"
    return {
        "schema": "paid-cycle-charity-to-sacrificed-v1",
        "status": "R2_THREE_EDGE_AND_R3_FOUR_EDGE_PAYMENT_SKELETONS_VERIFIED",
        "records": records,
        "checks": {
            "retained_owner_stays_paid": retained_payment,
            "desired_core_strictly_pays_cycle_source": desired_payment,
            "d_margin_identity": d_identity,
            "d_failure_is_bare_residual_deficit": d_failure,
        },
        "claim_boundary": (
            "cap-free graph/conservation/payment reduction; it does not exclude "
            "the sacrificed-owner deficit or establish observer EFX"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
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
