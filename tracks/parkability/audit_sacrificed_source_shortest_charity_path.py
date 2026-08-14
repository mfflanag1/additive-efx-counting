#!/usr/bin/env python3
"""Audit shortest response paths beginning at sacrificed owner d."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


FORMS = {
    "R2": (("d", "r", "q"), ("d", "q", "r")),
    "R3": (("d", "r", "q", "s"), ("d", "q", "s", "r")),
}


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def construct(form, path):
    owners = ("r", "q", "d", "s")
    endpoint = path[-1]
    initial = {owner: {f"bundle_{owner}"} for owner in owners}
    initial["charity"] = {"p"}
    final = {owner: set(initial[owner]) for owner in owners}
    final["charity"] = set()
    response_edges = tuple(zip(path[:-1], path[1:]))
    cores = {}
    for source, target in response_edges:
        core = f"core_{source}_from_{target}"
        cores[source, target] = core
        initial[target].add(core)
        final[target].add(core)
    # Rebuild final from the augmented initial state.
    final = {owner: set(initial[owner]) for owner in owners}
    final["charity"] = set()
    for source, target in response_edges:
        core = cores[source, target]
        final[target].remove(core)
        final[source].add(core)
    final[endpoint].add("p")
    edges = {(target, source) for source, target in response_edges}
    edges.add(("charity", endpoint))
    off_path = set(owners) - set(path)
    return {
        "form": form,
        "response_path": list(path),
        "endpoint": endpoint,
        "transfer_edges": [list(edge) for edge in sorted(edges)],
        "checks": {
            "charity_empty": not final["charity"],
            "atom_conservation": set().union(*initial.values()) == set().union(*final.values()),
            "edge_count_is_path_length": len(edges) == len(path),
            "at_most_four_edges": len(edges) <= 4,
            "functional_on_suppliers": len({source for source, _ in edges}) == len(edges),
            "off_path_bundles_preserved": all(initial[o] == final[o] for o in off_path),
            "d_keeps_complete_old_bundle": initial["d"] <= final["d"],
            "each_nonendpoint_path_source_receives_core": all(
                cores[source, target] in final[source]
                for source, target in response_edges
            ),
            "endpoint_receives_charity": "p" in final[endpoint],
        },
    }


def run(root):
    records = [
        construct(form, path) for form, paths in FORMS.items() for path in paths
    ]
    assert all(all(record["checks"].values()) for record in records)
    incoming, base, extras, final = z3.Reals("incoming base extras final")
    nonendpoint_payment = prove(
        [incoming > base, extras >= 0, final == incoming + extras], final > base
    )
    delta, loss, charity, margin = z3.Reals("delta loss charity margin")
    endpoint_identity = prove(
        [margin == delta - loss + charity], margin == delta - loss + charity
    )
    endpoint_failure = prove(
        [margin == delta - loss + charity, margin < 0], loss > delta + charity
    )
    script = Path(__file__).resolve()
    theorem = root / "results/SACRIFICED_SOURCE_SHORTEST_CHARITY_PATH_LEMMA_20260813.md"
    return {
        "schema": "sacrificed-source-shortest-charity-path-v1",
        "status": "FOUR_SHORTEST_PATH_PAYMENT_SKELETONS_VERIFIED",
        "records": records,
        "checks": {
            "nonendpoint_desired_core_strictly_pays": nonendpoint_payment,
            "endpoint_margin_identity": endpoint_identity,
            "endpoint_failure_is_capture": endpoint_failure,
        },
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
        "claim_boundary": (
            "cap-free graph/conservation/payment reduction; it does not prove an "
            "endpoint with nonnegative margin exists or establish observer EFX"
        ),
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
