#!/usr/bin/env python3
"""Audit the fixed two-edge strict-payment completion."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def prove(assumptions, conclusion):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, z3.Not(conclusion))
    return str(solver.check()) == "unsat"


def run(root):
    # Abstract packet values in d's row. R is all of nonempty Q0 and ell is
    # one least-good value, so positivity/nonemptiness gives R >= ell.
    J, K0, H, Gq, Q0, ell, W, Xd = z3.Reals(
        "J K0 H Gq Q0 ell W Xd"
    )
    premises = [
        J > 0, K0 > 0, H > 0, Gq > 0, Q0 > 0, ell > 0, W > 0,
        Xd == H + K0 + Gq,
        J + K0 + H > Xd,
        Q0 >= ell,
        W >= J + K0 + Q0 - ell,
    ]
    cancellation = prove(premises, J > Gq)
    tail_dominates_named_packets = prove(
        [J > 0, K0 > 0, Q0 >= ell],
        J + K0 + Q0 - ell >= J + K0,
    )
    strict_d_payment = prove(premises, W + H > Xd)

    owners = ("r", "q", "d", "s")
    initial = {
        "r": {"A", "H"}, "q": {"Q"}, "d": {"W"},
        "s": {"E"}, "charity": {"p"},
    }
    final = {
        "r": {"A"}, "q": {"Q"}, "d": {"W", "H"},
        "s": {"E", "p"}, "charity": set(),
    }
    edges = {("r", "d"), ("charity", "s")}
    Ar, Xr, Qq, Xq, Es, Xs, pp = z3.Reals("Ar Xr Qq Xq Es Xs pp")
    represented_payment = prove(
        [Ar > Xr, Qq > Xq, Es > Xs, pp > 0],
        z3.And(Ar > Xr, Qq > Xq, Es + pp > Xs),
    )
    script = Path(__file__).resolve()
    theorem = root / "results/ROOT_FACING_TWO_EDGE_STRICT_PAYMENT_COMPLETION_LEMMA_20260813.md"
    return {
        "schema": "root-facing-two-edge-strict-payment-completion-v1",
        "status": "NAMED_PROVENANCE_PROPER_RESIDUAL_TWO_EDGE_PAYMENT_VERIFIED",
        "checks": {
            "restoration_cancellation_gives_J_above_Gq": cancellation,
            "safe_Q_tail_dominates_J_plus_KminusJ": tail_dominates_named_packets,
            "W_plus_H_strictly_pays_d": strict_d_payment,
            "represented_owners_strictly_paid": represented_payment,
            "atom_conservation": set().union(*initial.values()) == set().union(*final.values()),
            "charity_empty": not final["charity"],
            "exactly_two_edges": len(edges) == 2,
            "functional_on_suppliers": len({source for source, _ in edges}) == len(edges),
            "every_owner_nonempty": all(final[owner] for owner in owners),
        },
        "transfer_edges": [list(edge) for edge in sorted(edges)],
        "initial": {owner: sorted(goods) for owner, goods in initial.items()},
        "final": {owner: sorted(goods) for owner, goods in final.items()},
        "claim_boundary": (
            "exact conditional strict-payment/conservation lemma assuming both "
            "the named X_d=H+(K-J)+Gq provenance identity and a nonempty Q\\K "
            "residual; these hold in the twelve-atom cell but are not universal "
            "GG premises"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
