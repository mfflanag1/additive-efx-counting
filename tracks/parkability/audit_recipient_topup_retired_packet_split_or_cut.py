#!/usr/bin/env python3
"""Exact audit of recipient-top-up retired-packet split or cut."""

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
    fs, b, k, u, topup, mu, d, recipient_new = z3.Reals(
        "fs b k u topup mu d recipient_new"
    )
    premises = [
        k == mu + d,
        d == fs - b,
        recipient_new == b + k - u + topup,
    ]
    margin_identity = prove(
        premises,
        recipient_new - fs == mu - u + topup,
    )
    floor_identity = prove(
        premises,
        (recipient_new >= fs) == (topup >= u - mu),
    )
    whole_replacement = prove(
        [*premises, u == k],
        (recipient_new >= fs) == (topup >= d),
    )
    indivisible_positive_price = prove(
        [k == mu + d, k - u < d],
        u - mu > 0,
    )

    packet_size, weakest_topup = z3.Reals("packet_size weakest_topup")
    multiplicity_charge = prove(
        [k == mu + d, packet_size > 0,
         packet_size * (mu + weakest_topup) < k],
        (packet_size - 1) * mu + packet_size * weakest_topup < d,
    )

    target_locality = True
    partitions_checked = 0
    for size in range(2, 9):
        packet = frozenset(range(size))
        for mask in range(1, (1 << size) - 1):
            retained = frozenset(
                good for good in packet if mask & (1 << good)
            )
            transferred = packet - retained
            partitions_checked += 1
            target_locality &= (
                retained < packet
                and transferred < packet
                and retained.isdisjoint(transferred)
                and retained | transferred == packet
            )

    assert all((margin_identity, floor_identity, whole_replacement,
                indivisible_positive_price, multiplicity_charge,
                target_locality))
    theorem = repo / "results/RECIPIENT_TOPUP_RETIRED_PACKET_SPLIT_OR_CUT_LEMMA_20260814.md"
    sacrifice = repo / "results/PRIORITY_SACRIFICE_PROPER_RETIRED_PACKET_SPLIT_THEOREM_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "recipient-topup-retired-packet-split-or-cut-audit-v1",
        "status": "RECIPIENT_INDIVISIBILITY_REDUCED_TO_TOPUP_CUT",
        "topup_margin_identity": margin_identity,
        "topup_floor_identity": floor_identity,
        "whole_packet_replacement_threshold": whole_replacement,
        "indivisible_retained_packet_has_positive_price": (
            indivisible_positive_price
        ),
        "topup_multiplicity_charge": multiplicity_charge,
        "single_target_response_hits_only_proper_split": target_locality,
        "representative_partitions_checked": partitions_checked,
        "remaining_separator": (
            "N_s(U)<v_s(U)-mu for every nonempty proper U subset K; "
            "N_s(K)<d; (|K|-1)mu+|K|n_s<d"
        ),
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free recipient top-up split/cut theorem; top-up cut, "
            "bypass return, and protected root cut remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "sacrifice_theorem": str(sacrifice.relative_to(repo)),
            "sacrifice_theorem_sha256": sha256(sacrifice),
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
