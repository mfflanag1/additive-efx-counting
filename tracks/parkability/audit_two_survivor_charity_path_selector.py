#!/usr/bin/env python3
"""Audit the Hamiltonian charity-path selectors in the two surviving forms."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


SURVIVORS = {
    "two_cycle": {
        "response_edges": (
            ("r", "q"), ("q", "r"), ("s", "d"), ("d", "q"), ("d", "r")
        ),
        "paths": (("s", "d", "r", "q"), ("s", "d", "q", "r")),
    },
    "three_cycle": {
        "response_edges": (
            ("r", "q"), ("q", "s"), ("s", "r"), ("d", "q"), ("d", "r")
        ),
        "paths": (("d", "r", "q", "s"), ("d", "q", "s", "r")),
    },
}


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(kind, path, response_edges):
    response_edges = set(response_edges)
    path_edges = tuple(zip(path, path[1:]))
    assert all(edge in response_edges for edge in path_edges)
    start, endpoint = path[0], path[-1]
    core = {edge: f"D[{edge[0]}->{edge[1]}]" for edge in path_edges}
    residual = {owner: f"R[{owner}]" for owner in path}
    p = "p"

    initial = {owner: {residual[owner]} for owner in path}
    initial["charity"] = {p}
    for edge, atom in core.items():
        initial[edge[1]].add(atom)
    # The start target has no incoming path edge; its full support is retained.
    final = {owner: set() for owner in path}
    final["charity"] = set()
    final[start].add(residual[start])
    for edge, atom in core.items():
        source, target = edge
        final[source].add(atom)
        final[target].add(residual[target])
    final[endpoint].add(p)

    before = {atom: owner for owner, atoms in initial.items() for atom in atoms}
    after = {atom: owner for owner, atoms in final.items() for atom in atoms}
    assert set(before) == set(after)
    transfer_edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected = {
        (target, source) for source, target in path_edges
    } | {("charity", endpoint)}
    assert set(transfer_edges) == expected
    assert len(transfer_edges) == 4
    return {
        "kind": kind,
        "response_path": list(path),
        "response_path_edges": [list(edge) for edge in path_edges],
        "omitted_cycle_source": endpoint,
        "transfer_edges": [list(edge) for edge in transfer_edges],
        "checks": {
            "all_path_edges_are_live_responses": all(
                edge in response_edges for edge in path_edges
            ),
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "exactly_four_support_edges": len(transfer_edges) == 4,
            "three_nonendpoint_sources_receive_desired_cores": all(
                core[edge] in final[edge[0]] for edge in path_edges
            ),
        },
    }


def run(root: Path):
    records = []
    for kind, data in SURVIVORS.items():
        for path in data["paths"]:
            records.append(construct(kind, path, data["response_edges"]))
    assert len(records) == 4
    assert all(all(record["checks"].values()) for record in records)

    current, base, incoming, extras, final = z3.Reals(
        "current base incoming extras final"
    )
    nonendpoint_payment = prove(
        [incoming > base, extras >= 0, final == incoming + extras],
        final > base,
    )
    delta, lost_core, charity, endpoint_margin = z3.Reals(
        "delta lost_core charity endpoint_margin"
    )
    endpoint_identity = prove(
        [endpoint_margin == delta - lost_core + charity],
        endpoint_margin == delta - lost_core + charity,
    )
    capture = prove(
        [delta >= 0, charity >= 0, endpoint_margin == delta - lost_core + charity,
         endpoint_margin < 0],
        lost_core > delta + charity,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/TWO_SURVIVOR_HAMILTONIAN_CHARITY_PATH_SELECTOR_LEMMA_20260813.md"
    return {
        "schema": "two-survivor-hamiltonian-charity-path-selector-v1",
        "status": "FOUR_CAP_FREE_PATH_SELECTORS_CONSTRUCTED",
        "records": records,
        "checks": {
            "all_support_checks": True,
            "nonendpoint_desired_core_payment": nonendpoint_payment,
            "endpoint_margin_identity": endpoint_identity,
            "endpoint_failure_is_strict_incoming_core_capture": capture,
        },
        "endpoint_choices": {
            "two_cycle": ["q", "r"],
            "three_cycle": ["s", "r"],
        },
        "exact_remaining_gate": (
            "prove at least one of the two endpoints has nonnegative signed "
            "margin and all enlarged targets are observer-safe, or convert both "
            "strict incoming-core capture inequalities into a saturated PI, "
            "support-growth, or response-augmentation exit"
        ),
        "claim_boundary": (
            "cap-free four-edge support and payment reduction for the two exact "
            "response forms; endpoint payment and observer safety are not proved"
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
    print(json.dumps({"status": result["status"], "selectors": len(result["records"])}, indent=2))


if __name__ == "__main__":
    main()
