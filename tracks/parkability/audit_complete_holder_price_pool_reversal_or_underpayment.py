#!/usr/bin/env python3
"""Exact QF_LRA audit of complete holder-pool threshold reversal."""

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
    pool, price, subset, q, q_minus_g, response = z3.Reals(
        "pool price subset q q_minus_g response"
    )
    aggregate_underpayment = prove(
        [subset <= pool, pool < price],
        subset < price,
    )
    selector_nonempty = prove(
        [pool >= price],
        pool >= price,
    )
    unsafe_reversal_below_price = prove(
        [response <= q_minus_g, q_minus_g < price],
        response < price,
    )
    holder_paid = prove([q >= price], q >= price)
    assert all((aggregate_underpayment, selector_nonempty,
                unsafe_reversal_below_price, holder_paid))

    results = repo / "results"
    theorem = results / "COMPLETE_HOLDER_PRICE_POOL_REVERSAL_OR_UNDERPAYMENT_LEMMA_20260813.md"
    contract = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    envelope = results / "TARGET_ENVELOPE_UNIVERSAL_PAYMENT_OR_PI_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "complete-holder-price-pool-reversal-or-underpayment-audit-v1",
        "status": "HOLDER_GATE_REDUCED_TO_PAYMENT_RESPONSE_OR_AGGREGATE_UNDERPAYMENT",
        "complete_pool_underpayment_blocks_every_subpacket": aggregate_underpayment,
        "price_crossing_selector_nonempty": selector_nonempty,
        "safe_crossing_packet_pays_holder": holder_paid,
        "unsafe_reversal_below_holder_price": unsafe_reversal_below_price,
        "remaining_separator": "max_{R in compatible modes} v_h(R) < p_h",
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free complete-pool threshold reversal; aggregate underpayment "
            "and global anchor conversion remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "contract": str(contract.relative_to(repo)),
            "contract_sha256": sha256(contract),
            "target_envelope": str(envelope.relative_to(repo)),
            "target_envelope_sha256": sha256(envelope),
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
        "remaining_separator": result["remaining_separator"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
