#!/usr/bin/env python3
"""Audit the root-sourced anchor-retaining sacrifice handoff."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    root_base, root_current, response, anchor = z3.Reals(
        "root_base root_current response anchor"
    )
    root_gain = prove(
        [root_current >= root_base, response > root_current, anchor > 0],
        response + anchor > root_base,
    )
    assert root_gain

    # Atomic physical census. E may intersect the displaced core A, but is
    # disjoint from the permanent anchor and both retained cores. The exact
    # complement therefore partitions the active pool for every overlap and
    # residual-consumption mask.
    physical = []
    atoms = {"anchor", "overlap", "response_only", "A_only", "C", "S", "R0", "R1"}
    for consume_mask in range(4):
        response_bundle = {"overlap", "response_only"}
        if consume_mask & 1:
            response_bundle.add("R0")
        if consume_mask & 2:
            response_bundle.add("R1")
        root_bundle = {"anchor"} | response_bundle
        retained = {"C", "S"}
        residual = atoms - root_bundle - retained
        assert root_bundle.isdisjoint(retained)
        assert root_bundle.isdisjoint(residual)
        assert retained.isdisjoint(residual)
        assert root_bundle | retained | residual == atoms
        physical.append({
            "response_residual_mask": consume_mask,
            "root_bundle": sorted(root_bundle),
            "retained_cores": sorted(retained),
            "sacrificed_owner_residual": sorted(residual),
        })

    # Abstract wall exclusion: represented owners meet all retained-core
    # thresholds; the sacrificed owner owns W. Only sacrificed-to-core/root,
    # represented-to-W, and represented-to-root comparisons are not assumed.
    assigned = z3.RealVector("assigned", 4)
    retained_tau = [[z3.Real(f"retained_tau_{i}_{k}") for k in range(2)] for i in range(4)]
    residual_tau = z3.RealVector("residual_tau", 4)
    root_tau = z3.RealVector("root_tau", 4)
    sacrificed = 3
    represented = range(3)
    solver = z3.SolverFor("QF_LRA")
    for i in represented:
        for k in range(2):
            solver.add(assigned[i] >= retained_tau[i][k])
    solver.add(assigned[sacrificed] >= residual_tau[sacrificed])
    assert solver.check() == z3.sat
    for i in represented:
        for k in range(2):
            probe = z3.SolverFor("QF_LRA")
            probe.add(solver.assertions(), assigned[i] < retained_tau[i][k])
            assert probe.check() == z3.unsat
    probe = z3.SolverFor("QF_LRA")
    probe.add(solver.assertions(), assigned[sacrificed] < residual_tau[sacrificed])
    assert probe.check() == z3.unsat

    # Rebuild a positive full-pool-failure row: A=overlap+remainder is above
    # floor, yet remainder plus every residual is below it. The handoff stays
    # physically feasible and root-priority-valid because it sacrifices a.
    A, overlap, remainder, pool, floor = z3.Reals(
        "A overlap remainder pool floor"
    )
    witness = z3.SolverFor("QF_LRA")
    witness.add(
        A == overlap + remainder,
        A > floor,
        remainder + pool <= floor,
        overlap > 0,
        remainder > 0,
        pool > 0,
    )
    assert witness.check() == z3.sat
    model = witness.model()

    theorem = root / "results/ROOT_SOURCED_ANCHOR_RETAINING_SACRIFICE_HANDOFF_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-sourced-anchor-retaining-sacrifice-handoff-audit-v1",
        "status": "FULL_POOL_PAYMENT_SUPERSEDED_BY_PRIORITY_VALID_SACRIFICE",
        "root_strict_after_anchor_response_union": root_gain,
        "physical_records": physical,
        "wall_exclusions": {
            "represented_to_retained_core": True,
            "sacrificed_owner_to_own_residual": True,
        },
        "surviving_wall_forms": [
            "sacrificed owner to retained core or enlarged root target",
            "represented source to residual",
            "represented nonroot source to enlarged root target",
        ],
        "full_pool_failure_consistent": True,
        "sample_full_pool_failure": {
            name: str(model.eval(variable, model_completion=True))
            for name, variable in {
                "A": A, "overlap": overlap, "remainder": remainder,
                "pool": pool, "floor": floor,
            }.items()
        },
        "claim_boundary": (
            "cap-free priority-valid handoff; enlarged-root-target/residual "
            "response recurrence and root-critical good remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "surviving_wall_forms": result["surviving_wall_forms"],
    }, indent=2))


if __name__ == "__main__":
    main()

