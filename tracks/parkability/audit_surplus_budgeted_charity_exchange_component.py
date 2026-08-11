#!/usr/bin/env python3
"""Symbolic and witness audit of the charity-exchange endpoint theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    x, delta, y, tau_changed, tau_unchanged, charity = z3.Reals(
        "x delta y tau_changed tau_unchanged charity"
    )
    checks = {
        "changed_target_surplus_budget": prove(
            [delta >= 0, y == x + delta, tau_changed - x <= delta],
            y < tau_changed,
        ),
        "unchanged_target_base_safety": prove(
            [delta >= 0, y == x + delta, tau_unchanged <= x],
            y < tau_unchanged,
        ),
        "exchanged_charity_surplus_budget": prove(
            [delta >= 0, y == x + delta, charity - x <= delta],
            y < charity,
        ),
    }

    witness = json.loads((root / "results/fixed_u_global_lex_premise_audit.json").read_text())
    assert witness["status"] == "BASE_EXCLUDED"
    assert witness["all_agents_strict"]
    assert witness["charity_exchange"]
    assert witness["single_connected_transfer_component"]
    assert witness["transfer_topology"]["has_directed_cycle"]

    script = Path(__file__).resolve()
    theorem = root / "results/SURPLUS_BUDGETED_CHARITY_EXCHANGE_COMPONENT_LEMMA_20260811.md"
    return {
        "schema": "surplus-budgeted-charity-exchange-component-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "exact_witness": {
            "audit": "results/fixed_u_global_lex_premise_audit.json",
            "audit_sha256": sha256(root / "results/fixed_u_global_lex_premise_audit.json"),
            "old_charity": witness["old_charity"],
            "new_charity": witness["new_charity"],
            "all_agents_strict": witness["all_agents_strict"],
            "single_connected_transfer_component": witness["single_connected_transfer_component"],
            "has_directed_cycle": witness["transfer_topology"]["has_directed_cycle"],
        },
        "smallest_missing_operation": (
            "charity donates its old good and receives a replacement good inside the "
            "same surplus-budgeted connected cyclic component"
        ),
        "remaining_gate": (
            "extract a charity-exchange component from every full-owner repeated GG "
            "base-margin/direct-safety terminal"
        ),
        "claim_boundary": (
            "charity-exchange endpoint and one exact global exclusion; universal "
            "repeated-support GG closure and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
