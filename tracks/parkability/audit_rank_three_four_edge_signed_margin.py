#!/usr/bin/env python3
"""Audit the exact signed owner/observer budget for response reversal."""

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


def run(root: Path):
    current, base, outgoing, incoming, final = z3.Reals(
        "current base outgoing incoming final"
    )
    identity = prove(
        [final == current - outgoing + incoming],
        final - base == (current - base) - outgoing + incoming,
    )
    current_response_pays = prove(
        [
            current >= base,
            outgoing >= 0,
            outgoing <= current,
            incoming > current,
            final == current - outgoing + incoming,
        ],
        final > current,
    )
    base_response_pays = prove(
        [
            current >= base,
            outgoing >= 0,
            outgoing <= current,
            incoming > base,
            final == current - outgoing + incoming,
        ],
        final > base,
    )

    margin, debt = z3.Reals("margin debt")
    observer_budget = prove(
        [final - base == margin, debt >= 0, margin >= debt],
        final >= base + debt,
    )

    checks = {
        "signed_owner_margin_identity": identity,
        "current_desired_core_automatically_pays_after_any_own_subpacket_release": (
            current_response_pays
        ),
        "base_desired_core_automatically_pays_after_any_own_subpacket_release": (
            base_response_pays
        ),
        "observer_surplus_budget_is_sufficient": observer_budget,
    }
    assert all(checks.values())
    script = Path(__file__).resolve()
    theorem = root / "results/RANK_THREE_FOUR_EDGE_SIGNED_MARGIN_IDENTITY_LEMMA_20260813.md"
    return {
        "schema": "rank-three-four-edge-signed-margin-v1",
        "status": "EXACT_MARGIN_IDENTITY_AND_ALL_RESPONSE_PAYMENT",
        "checks": checks,
        "identity": "m_i = Delta_i - L_i + I_i",
        "efx_budget": "m_i >= max_{j != i}(tau_i(Z_j)-v_i(X_i))_+",
        "claim_boundary": (
            "cap-free linear identity and payment for every owner receiving a "
            "base- or current-desired response core; response-free endpoints and "
            "final enlarged-target safety remain"
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
    print(json.dumps({"status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()
