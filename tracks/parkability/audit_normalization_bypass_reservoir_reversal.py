#!/usr/bin/env python3
"""Exact arithmetic audit for normalization-bypass reservoir reversal."""

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
    b_h, threshold, u, q, q_minus_g, a, e = z3.Reals(
        "b_h threshold u q q_minus_g a e"
    )
    selector_nonempty = prove(
        [u == b_h, b_h >= threshold],
        u >= threshold,
    )
    reversal_payment = prove(
        [a <= q_minus_g, q_minus_g < threshold, threshold <= e],
        a < e,
    )
    safe_packet_payment = prove(
        [q >= threshold],
        q >= threshold,
    )
    assert selector_nonempty and reversal_payment and safe_packet_payment

    theorem = repo / "results/NORMALIZATION_BYPASS_RESERVOIR_REVERSAL_LEMMA_20260813.md"
    normal_form = repo / "results/RETIRED_PACKET_COLLISION_ATOMIC_NORMAL_FORM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "normalization-bypass-reservoir-reversal-audit-v1",
        "status": "BYPASS_REDUCED_TO_COLLISION_OR_SAFE_PAYMENT_WALL",
        "selector_nonempty_from_current_safety": selector_nonempty,
        "safe_packet_pays_response_threshold": safe_packet_payment,
        "unsafe_reversal_packet_paid_by_original_response": reversal_payment,
        "collision_routes": ["proper_K_reduction", "whole_K_atomic_collision"],
        "ledger_free_routes": ["rank_or_PI_closure", "safe_threshold_payment_wall"],
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free threshold reversal and routing lemma; the source-"
            "safe threshold-payment wall remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "normal_form": str(normal_form.relative_to(repo)),
            "normal_form_sha256": sha256(normal_form),
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
        "ledger_free_routes": result["ledger_free_routes"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
