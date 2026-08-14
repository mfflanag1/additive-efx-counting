#!/usr/bin/env python3
"""Exact arithmetic audit of the conditional supplier-return candidate."""

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
    x, delta, k, h, ret, d = z3.Reals("x delta k h ret d")
    base = [x > 0, delta > 0, k > 0, h >= 0, k + h == x + delta]

    margin = z3.SolverFor("QF_LRA")
    margin.add(*base, h + ret - x != delta - k + ret)
    release_margin_identity_exact = margin.check() == z3.unsat

    strict = z3.SolverFor("QF_LRA")
    strict.add(*base, ret > k - delta, h + ret <= x)
    strict_payment_keeps_root_above_base = strict.check() == z3.unsat

    free = z3.SolverFor("QF_LRA")
    free.add(*base, k < delta, h <= x)
    empty_return_strict_when_packet_below_surplus = free.check() == z3.unsat

    price_order = z3.SolverFor("QF_LRA")
    packet_price = z3.If(k - delta >= 0, k - delta, 0)
    envelope_price = z3.If(d - delta >= 0, d - delta, 0)
    price_order.add(k <= d, packet_price > envelope_price)
    packet_price_no_larger_than_envelope_price = price_order.check() == z3.unsat

    # Physical support: root K+H, supplier U, another donor, charity. The
    # compatible exterior pool may include supplier goods.
    k_support, h_support = {0, 1}, {2, 3}
    u_support, donor_support, charity = {4, 5}, {6, 7}, {8}
    exterior = u_support | donor_support | charity
    universe = k_support | h_support | u_support | exterior
    support_cases = 0
    ordered = tuple(sorted(exterior))
    for mask in range(1 << len(ordered)):
        packet = {ordered[j] for j in range(len(ordered)) if mask & (1 << j)}
        targets = (
            h_support | packet,
            (u_support - packet) | k_support,
            donor_support - packet,
            charity - packet,
        )
        assert set().union(*targets) == universe
        assert sum(map(len, targets)) == len(universe)
        assert not ((h_support | packet) & k_support)
        support_cases += 1

    assert all((
        release_margin_identity_exact,
        strict_payment_keeps_root_above_base,
        empty_return_strict_when_packet_below_surplus,
        packet_price_no_larger_than_envelope_price,
        support_cases > 0,
    ))
    theorem = ROOT / "results/RETIREMENT_SUPPLIER_ROOT_PACKET_RELEASE_OR_UNDERPAYMENT_THEOREM_20260814.md"
    admission = ROOT / "results/ROOT_STRICT_CLEAN_SUBPACKET_RELEASE_ADMISSION_THEOREM_20260814.md"
    root_pool = ROOT / "results/ROOT_SAFE_WHOLE_HIT_COMPLETE_POOL_REDUCTION_THEOREM_20260814.md"
    nonroot = ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retirement-supplier-root-packet-release-or-underpayment-audit-v1",
        "status": "STRICT_ROOT_PACKET_RELEASE_ADMITTED_EQUALITY_OPEN",
        "release_margin_identity_exact": release_margin_identity_exact,
        "strict_payment_keeps_root_above_base": strict_payment_keeps_root_above_base,
        "empty_return_strict_when_packet_below_surplus": empty_return_strict_when_packet_below_surplus,
        "packet_price_no_larger_than_envelope_price": packet_price_no_larger_than_envelope_price,
        "complete_exterior_support_cases_checked": support_cases,
        "historical_recipient_identified": True,
        "historical_return_transition_admitted": False,
        "clean_controlled_release_admitted": True,
        "return_owner_may_be_sacrificed_if_transition_admitted_and_root_strict": True,
        "remaining_separator": "supplier_return_admission_then_packet_price_underpayment_or_equality",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, admission, root_pool, nonroot, script)
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
