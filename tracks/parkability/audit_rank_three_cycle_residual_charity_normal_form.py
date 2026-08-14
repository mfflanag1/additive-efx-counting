#!/usr/bin/env python3
"""Audit the complete cycle-residual charity absorption normal form."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def prove(premises, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def construct(size, moved_bits, charity_recipient):
    owners = tuple(f"i{index}" for index in range(size))
    predecessor = {
        owners[(index + 1) % size]: owners[index] for index in range(size)
    }
    # Response i -> next(i) selects D_i inside Y_next(i).  Hence physical
    # supplier j sends D_pred(j) and optional S_j to pred(j).
    core = {owner: f"D[{owner}]" for owner in owners}
    residual_keep = {owner: f"R0[{owner}]" for owner in owners}
    residual_send = {owner: f"R1[{owner}]" for owner in owners}
    p = "p"

    initial = {owner: {residual_keep[owner], residual_send[owner]} for owner in owners}
    initial["charity"] = {p}
    for target in owners:
        initial[target].add(core[predecessor[target]])

    final = {owner: {core[owner]} for owner in owners}
    final["charity"] = set()
    for index, supplier in enumerate(owners):
        receiver = predecessor[supplier]
        final[supplier].add(residual_keep[supplier])
        if moved_bits[index]:
            final[receiver].add(residual_send[supplier])
        else:
            final[supplier].add(residual_send[supplier])
    final[charity_recipient].add(p)

    before = {atom: owner for owner, atoms in initial.items() for atom in atoms}
    after = {atom: owner for owner, atoms in final.items() for atom in atoms}
    assert set(before) == set(after)
    assert len(before) == sum(map(len, initial.values()))
    assert len(after) == sum(map(len, final.values()))
    edges = tuple(sorted({
        (before[atom], after[atom]) for atom in before if before[atom] != after[atom]
    }))
    expected_cycle = {
        (supplier, predecessor[supplier]) for supplier in owners
    }
    assert expected_cycle <= set(edges)
    assert ("charity", charity_recipient) in edges
    assert len(edges) == size + 1
    assert not final["charity"]
    return {
        "cycle_size": size,
        "moved_residual_bits": list(moved_bits),
        "charity_recipient": charity_recipient,
        "transfer_edges": [list(edge) for edge in edges],
        "initial_atoms": {owner: sorted(atoms) for owner, atoms in initial.items()},
        "final_atoms": {owner: sorted(atoms) for owner, atoms in final.items()},
        "checks": {
            "atom_conservation": set(before) == set(after),
            "charity_empty": not final["charity"],
            "cycle_edges_preserved": expected_cycle <= set(edges),
            "edge_count_is_cycle_plus_one": len(edges) == size + 1,
            "edge_count_at_most_four": len(edges) <= 4,
            "every_owner_receives_own_desired_core": all(
                core[owner] in final[owner] for owner in owners
            ),
        },
    }


def run(root: Path):
    records = []
    for size in (2, 3):
        owners = tuple(f"i{index}" for index in range(size))
        for moved_bits in itertools.product((False, True), repeat=size):
            for charity_recipient in owners:
                records.append(construct(size, moved_bits, charity_recipient))
    assert len(records) == 32
    assert all(all(record["checks"].values()) for record in records)

    incoming, base, extras, final = z3.Reals("incoming base extras final")
    payment = prove(
        [incoming > base, extras >= 0, final == incoming + extras],
        final > base,
    )
    script = Path(__file__).resolve()
    theorem = root / "results/RANK_THREE_CYCLE_RESIDUAL_CHARITY_NORMAL_FORM_LEMMA_20260813.md"
    return {
        "schema": "rank-three-cycle-residual-charity-normal-form-v1",
        "status": "ALL_TWO_AND_THREE_CYCLE_RESIDUAL_SELECTORS_VALID",
        "selector_count": len(records),
        "records": records,
        "checks": {
            "all_support_partitions_conserved": True,
            "all_charities_empty": True,
            "all_edge_counts_at_most_four": True,
            "base_desired_incoming_core_pays_owner": payment,
        },
        "exact_remaining_gate": (
            "select one cycle owner b and one arbitrary residual subpacket S_j "
            "per cycle supplier so every final observer-target EFX inequality holds"
        ),
        "claim_boundary": (
            "cap-free support/payment normal form conditional on pairwise-disjoint "
            "base-desired cycle cores; it does not prove existence of an observer-"
            "safe residual/charity selection or eliminate overlap capture"
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
        "selector_count": result["selector_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
