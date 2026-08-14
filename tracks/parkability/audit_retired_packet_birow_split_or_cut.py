#!/usr/bin/env python3
"""Exact QF_LRA audit of retired-packet bi-row split or cut."""

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
    fs, b, t_s, recipient_new, d, mu, k_s = z3.Reals(
        "fs b t_s recipient_new d mu k_s"
    )
    recipient = [recipient_new == b + t_s, d == fs - b]
    recipient_floor = prove(recipient, (recipient_new >= fs) == (t_s >= d))
    recipient_margin = prove(recipient, recipient_new - fs == t_s - d)

    fh, total_h, t_h, compensation, holder_new, slack = z3.Reals(
        "fh total_h t_h compensation holder_new slack"
    )
    holder = [
        slack == total_h - fh,
        holder_new == total_h - t_h + compensation,
    ]
    holder_floor = prove(
        holder,
        (holder_new >= fh) == (t_h <= slack + compensation),
    )

    full_mode, full_k_h = z3.Reals("full_mode full_k_h")
    full_packet_infeasible = prove(
        [full_mode < full_k_h - slack],
        z3.Not(full_k_h <= slack + full_mode),
    )

    # If every proper deletion of K is below the recipient threshold, each
    # good exceeds the strict full-packet margin.  The displayed scalar check
    # is one arbitrary deletion; summing it gives the analytic multiplicity
    # consequence in the theorem.
    good_s, k_minus_good_s = z3.Reals("good_s k_minus_good_s")
    critical_good = prove(
        [k_s == mu + d, k_s == good_s + k_minus_good_s,
         k_minus_good_s < d],
        good_s > mu,
    )
    equality_proper_impossible = prove(
        [mu == 0, k_s == mu + d, t_s < k_s],
        t_s < d,
    )

    # Physical target locality is cap-free: for every nonempty proper T,
    # the tested allocation partitions K between two targets.  Every
    # single-target response therefore meets a proper subset of K.  The
    # finite loop is an independent executable sanity check of the set
    # identity for representative packet sizes; the markdown proof is the
    # general argument.
    target_locality = True
    for size in range(2, 9):
        packet = frozenset(range(size))
        for mask in range(1, (1 << size) - 1):
            transferred = frozenset(
                good for good in packet if mask & (1 << good)
            )
            retained = packet - transferred
            target_locality &= (
                bool(transferred)
                and bool(retained)
                and transferred < packet
                and retained < packet
                and transferred.isdisjoint(retained)
                and transferred | retained == packet
            )
    assert all((recipient_floor, recipient_margin, holder_floor,
                full_packet_infeasible, critical_good,
                equality_proper_impossible, target_locality))

    results = repo / "results"
    theorem = results / "RETIRED_PACKET_BIROW_SPLIT_OR_CUT_LEMMA_20260813.md"
    pool = results / "COMPLETE_HOLDER_PRICE_POOL_REVERSAL_OR_UNDERPAYMENT_LEMMA_20260813.md"
    contract = results / "RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-birow-split-or-cut-audit-v1",
        "status": "PROPER_PACKET_REDUCTION_OR_EXACT_BIROW_CUT",
        "recipient_floor_identity": recipient_floor,
        "recipient_margin_identity": recipient_margin,
        "holder_floor_identity": holder_floor,
        "full_packet_blocked_by_aggregate_underpayment": full_packet_infeasible,
        "recipient_critical_good_exceeds_strict_margin": critical_good,
        "equality_capture_has_no_proper_recipient_feasible_packet": (
            equality_proper_impossible
        ),
        "single_target_response_cannot_reassemble_split_packet": target_locality,
        "remaining_separator": (
            "v_s(T)>=d implies v_h(T)>sigma+M_h(T) for every T subset K"
        ),
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free two-row split/locality theorem; global contradiction "
            "or anchor release from the bi-row cut remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "pool_theorem": str(pool.relative_to(repo)),
            "pool_theorem_sha256": sha256(pool),
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
        "remaining_separator": result["remaining_separator"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
