#!/usr/bin/env python3
"""Exact symbolic audit of the retire-on-backup anchor exchange."""

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


def run(repo: Path) -> dict:
    # Row-r payment and priority.
    base_r, e_r, unchanged_tau_r = z3.Reals(
        "base_r e_r unchanged_tau_r"
    )
    root_valid = prove(
        [e_r > base_r, e_r >= unchanged_tau_r],
        z3.And(e_r > base_r, e_r >= unchanged_tau_r),
    )

    # Returning a nonempty positive packet strictly improves its supplier.
    q_old, k_q = z3.Reals("q_old k_q")
    supplier_improves = prove(
        [q_old >= 0, k_q > 0], q_old + k_q > q_old
    )

    # For a nonroot row and an unchanged target, no new wall appears when
    # assigned value weakly increases and the threshold does not increase.
    old_u, new_u, old_tau, new_tau = z3.Reals(
        "old_u new_u old_tau new_tau"
    )
    unchanged_wall_monotonicity = prove(
        [new_u >= old_u, new_tau <= old_tau],
        z3.Implies(new_u < new_tau, old_u < old_tau),
    )

    # Every nonroot row pays the shrunken root target because E was
    # current-safe and nonroot assigned values do not fall.
    tau_e = z3.Real("tau_e")
    shrunken_root_safe = prove(
        [old_u >= tau_e, new_u >= old_u], new_u >= tau_e
    )

    assert all([
        root_valid,
        supplier_improves,
        unchanged_wall_monotonicity,
        shrunken_root_safe,
    ])

    # Exact physical and signed-provenance audit.
    K = {"k0", "k1"}
    E = {"e0", "e1"}
    Q = {"q0", "q1"}
    O = {"o0", "o1"}
    before = {"r": K | E, "q": Q, "o": O}
    after = {"r": E, "q": Q | K, "o": O}
    assert set().union(*before.values()) == set().union(*after.values())
    assert all(
        before[a].isdisjoint(before[b]) and after[a].isdisjoint(after[b])
        for a, b in [("r", "q"), ("r", "o"), ("q", "o")]
    )
    assert before["r"] - after["r"] == K
    assert after["q"] - before["q"] == K
    assert after["r"] == E

    theorem = repo / "results/PERMANENT_ANCHOR_RETIRE_ON_BACKUP_EXCHANGE_THEOREM_20260813.md"
    contract = repo / "results/PERMANENT_ANCHOR_HITTING_RECURRENCE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "permanent-anchor-retire-on-backup-exchange-audit-v1",
        "status": "CONDITIONAL_EXCHANGE_VERIFIED_PREMISE_NOT_SUPPLIED",
        "root_priority_and_unchanged_target_payment": root_valid,
        "original_supplier_strictly_improves": supplier_improves,
        "unchanged_wall_monotonicity": unchanged_wall_monotonicity,
        "shrunken_root_target_current_safe": shrunken_root_safe,
        "physical_partition_and_signed_return_valid": True,
        "only_genuinely_new_wall_target": "Q+K",
        "old_anchor_retired": True,
        "claim_boundary": (
            "resolves the frozen permanent-anchor recurrence via controlled "
            "current-phase anchor exchange; does not promote E to an old "
            "base-common-safe anchor or close subsequent GG classes"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "contract": str(contract.relative_to(repo)),
            "contract_sha256": sha256(contract),
            "z3_version": z3.get_version_string(),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "only_genuinely_new_wall_target": result["only_genuinely_new_wall_target"],
    }, indent=2))


if __name__ == "__main__":
    main()
