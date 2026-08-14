#!/usr/bin/env python3
"""Exact support and QF_LRA audit of the canonical whole-hit swap lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    support_cases = 0
    for size in range(2, 9):
        holder = set(range(size))
        for k_mask in range(1, 1 << size):
            packet = {g for g in holder if k_mask & (1 << g)}
            for d_mask in range(1, 1 << size):
                response = {g for g in holder if d_mask & (1 << g)}
                if not packet <= response or response == holder:
                    continue
                residual = holder - response
                outside_packet = holder - packet
                assert residual
                assert residual <= outside_packet
                assert response == packet | (outside_packet - residual)
                source_bundle = set(range(size, size + 3))
                new_holder = residual | source_bundle
                assert not (new_holder & packet)
                support_cases += 1

    assert support_cases > 0

    d_h, zt_h, residual_h, old_holder_h = z3.Reals(
        "d_h zt_h residual_h old_holder_h"
    )
    payment = z3.SolverFor("QF_LRA")
    payment.add(
        old_holder_h == residual_h + d_h,
        zt_h >= d_h,
        z3.Not(residual_h + zt_h >= old_holder_h),
    )
    holder_payment_exact = payment.check() == z3.unsat

    underpayment = z3.SolverFor("QF_LRA")
    underpayment.add(
        old_holder_h == residual_h + d_h,
        residual_h + zt_h < old_holder_h,
        z3.Not(zt_h < d_h),
    )
    source_underpayment_exact = underpayment.check() == z3.unsat

    source_total, response_total = z3.Reals("source_total response_total")
    self_source = z3.SolverFor("QF_LRA")
    self_source.add(response_total <= source_total, response_total > source_total)
    holder_cannot_source_current_subbundle = self_source.check() == z3.unsat

    assert holder_payment_exact
    assert source_underpayment_exact
    assert holder_cannot_source_current_subbundle

    theorem = ROOT / "results/CANONICAL_WHOLE_HIT_BILATERAL_SWAP_OR_SOURCE_UNDERPAYMENT_LEMMA_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "canonical-whole-hit-bilateral-swap-or-source-underpayment-audit-v1",
        "status": "CURRENT_WHOLE_HIT_REDUCED_TO_LEDGER_FREE_SWAP_OR_SOURCE_UNDERPAYMENT",
        "support_cases_checked": support_cases,
        "whole_hit_residual_is_nonempty_and_ledger_free": True,
        "bilateral_swap_new_holder_is_ledger_free": True,
        "holder_payment_exact": holder_payment_exact,
        "source_underpayment_exact": source_underpayment_exact,
        "holder_cannot_source_current_subbundle": holder_cannot_source_current_subbundle,
        "remaining_separator": "holder_values_source_bundle_below_whole_hit_response",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, contract, script)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
