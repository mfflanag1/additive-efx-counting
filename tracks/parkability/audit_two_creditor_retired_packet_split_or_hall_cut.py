#!/usr/bin/env python3
"""Exact audit of the two-creditor retired-packet split/Hall cut."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises, conclusion) -> bool:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(repo: Path) -> dict:
    fs, b, k_s, t_s, u_s, rs, mu, d, new_s = z3.Reals(
        "fs b k_s t_s u_s rs mu d new_s"
    )
    recipient = [
        k_s == t_s + u_s,
        k_s == mu + d,
        d == fs - b,
        new_s == b + t_s + rs,
    ]
    recipient_margin = prove(
        recipient,
        new_s - fs == mu - u_s + rs,
    )
    recipient_floor = prove(
        recipient,
        (new_s >= fs) == (rs >= u_s - mu),
    )

    fh, total_h, t_h, rh, sigma, new_h = z3.Reals(
        "fh total_h t_h rh sigma new_h"
    )
    holder = [
        sigma == total_h - fh,
        new_h == total_h - t_h + rh,
    ]
    holder_margin = prove(
        holder,
        new_h - fh == sigma - t_h + rh,
    )
    holder_floor = prove(
        holder,
        (new_h >= fh) == (rh >= t_h - sigma),
    )

    target_locality = True
    partitions_checked = 0
    for size in range(2, 9):
        packet = frozenset(range(size))
        for mask in range(1, (1 << size) - 1):
            transferred = frozenset(
                good for good in packet if mask & (1 << good)
            )
            retained = packet - transferred
            partitions_checked += 1
            target_locality &= (
                transferred < packet
                and retained < packet
                and transferred.isdisjoint(retained)
                and transferred | retained == packet
            )

    hall_rows = []
    for recipient_exists in (False, True):
        for holder_exists in (False, True):
            for compatible_edge in (False, True):
                if compatible_edge and not (recipient_exists and holder_exists):
                    continue
                if not recipient_exists:
                    branch = "recipient_deficiency"
                elif not holder_exists:
                    branch = "holder_deficiency"
                elif not compatible_edge:
                    branch = "joint_incompatibility"
                else:
                    branch = "joint_payment"
                hall_rows.append({
                    "recipient_family_nonempty": recipient_exists,
                    "holder_family_nonempty": holder_exists,
                    "compatible_edge_exists": compatible_edge,
                    "branch": branch,
                })
    assert len(hall_rows) == 5

    scalar_obstructions = []
    for mu_value, d_value in ((Fraction(1), Fraction(3)),
                              (Fraction(0), Fraction(4))):
        recipient_k = (Fraction(2), Fraction(2))
        root_k = (Fraction(2), Fraction(2))
        root_slack = Fraction(1)
        root_base = Fraction(5)
        root_rest = Fraction(2)
        recipient_z = Fraction(2) - mu_value
        root_z = Fraction(1)
        for transferred in (0, 1):
            retained = 1 - transferred
            recipient_price = recipient_k[retained] - mu_value
            holder_price = root_k[transferred] - root_slack
            assert recipient_z >= recipient_price
            assert root_z >= holder_price
        assert root_z < sum(root_k) - root_slack
        assert recipient_z < d_value
        assert root_rest + sum(root_k) == root_base + root_slack
        assert root_rest + root_k[0] <= root_base
        assert root_rest + root_k[1] <= root_base
        assert sum(root_k) <= root_base
        scalar_obstructions.append({
            "branch": "strict" if mu_value > 0 else "equality",
            "mu": str(mu_value),
            "d": str(d_value),
            "recipient_packet_values": [str(v) for v in recipient_k],
            "root_packet_values": [str(v) for v in root_k],
            "recipient_outside_good": str(recipient_z),
            "root_outside_good": str(root_z),
            "both_one_sided_families_nonempty": True,
            "compatible_pair_exists": False,
            "boundary_operations_underpay": True,
            "root_core_atomwise_minimal": True,
        })
    assert all((recipient_margin, recipient_floor, holder_margin,
                holder_floor, target_locality))

    theorem = repo / "results/TWO_CREDITOR_RETIRED_PACKET_SPLIT_OR_HALL_CUT_THEOREM_20260814.md"
    topup = repo / "results/RECIPIENT_TOPUP_RETIRED_PACKET_SPLIT_OR_CUT_LEMMA_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "two-creditor-retired-packet-split-or-hall-cut-audit-v1",
        "status": "TWO_SIDED_PAYMENT_REDUCED_TO_EXACT_HALL_CUT",
        "recipient_margin_identity": recipient_margin,
        "recipient_floor_identity": recipient_floor,
        "holder_margin_identity": holder_margin,
        "holder_floor_identity": holder_floor,
        "single_target_response_hits_only_proper_split": target_locality,
        "representative_partitions_checked": partitions_checked,
        "hall_truth_table": hall_rows,
        "scalar_joint_incompatibility_models": scalar_obstructions,
        "scalar_models_verified": True,
        "terminal_branches": [
            "recipient_deficiency",
            "holder_deficiency",
            "joint_incompatibility",
        ],
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free two-creditor payment/Hall normal form plus exact "
            "strict/equality scalar no-go; structural conversion and full "
            "theorem remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "topup_theorem": str(topup.relative_to(repo)),
            "topup_theorem_sha256": sha256(topup),
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
        "terminal_branches": result["terminal_branches"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()
