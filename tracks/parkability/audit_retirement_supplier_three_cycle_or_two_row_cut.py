#!/usr/bin/env python3
"""Exact support/QF_LRA audit of the retirement-supplier three-cycle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    # Disjoint symbolic supports: holder response D contains K, holder keeps
    # L, source and supplier have their own cells.
    k = {0, 1}
    d = k | {2}
    ell = {3, 4}
    z_t = {5, 6}
    z_u = {7, 8, 9}
    old = {"h": d | ell, "t": z_t, "u": z_u}
    new = {"h": ell | z_u, "t": d, "u": z_t}
    assert set().union(*old.values()) == set().union(*new.values())
    assert sum(map(len, old.values())) == sum(map(len, new.values()))
    assert new["h"].isdisjoint(k)
    assert new["t"] & k == k

    d_h, ell_h, zu_h = z3.Reals("d_h ell_h zu_h")
    holder = z3.SolverFor("QF_LRA")
    holder.add(zu_h >= d_h, z3.Not(ell_h + zu_h >= ell_h + d_h))
    holder_payment_exact = holder.check() == z3.unsat

    zt_u, zu_u = z3.Reals("zt_u zu_u")
    supplier = z3.SolverFor("QF_LRA")
    supplier.add(zt_u >= zu_u, z3.Not(zt_u >= zu_u))
    supplier_payment_exact = supplier.check() == z3.unsat

    cut = z3.SolverFor("QF_LRA")
    cut.add(
        z3.Not(z3.And(zt_u >= zu_u, zu_h >= d_h)),
        z3.Not(z3.Or(zt_u < zu_u, zu_h < d_h)),
    )
    two_row_cut_exhaustive = cut.check() == z3.unsat
    assert holder_payment_exact and supplier_payment_exact and two_row_cut_exhaustive

    theorem = ROOT / "results/RETIREMENT_SUPPLIER_THREE_CYCLE_OR_TWO_ROW_CUT_LEMMA_20260814.md"
    bilateral = ROOT / "results/CANONICAL_WHOLE_HIT_BILATERAL_SWAP_OR_SOURCE_UNDERPAYMENT_LEMMA_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retirement-supplier-three-cycle-or-two-row-cut-audit-v1",
        "status": "SUPPLIER_CYCLE_OR_EXACT_TWO_ROW_CUT",
        "support_conserved": True,
        "named_packet_absent_from_new_holder_target": True,
        "holder_payment_exact": holder_payment_exact,
        "supplier_payment_exact": supplier_payment_exact,
        "two_row_cut_exhaustive": two_row_cut_exhaustive,
        "other_retired_support_normalization_required": True,
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, bilateral, contract, script)
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
