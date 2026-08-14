#!/usr/bin/env python3
"""Exact support/QF_LRA audit of the global root sacrifice-pool theorem."""

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
    x, delta, d, ell, pool, pi = z3.Reals("x delta d ell pool pi")
    margin = z3.SolverFor("QF_LRA")
    margin.add(
        d + ell == x + delta,
        pi == d - delta,
        ell + pool - x != pool - pi,
    )
    root_margin_identity_exact = margin.check() == z3.unsat

    strict = z3.SolverFor("QF_LRA")
    strict.add(
        d + ell == x + delta,
        pi == d - delta,
        pool > pi,
        ell + pool <= x,
    )
    strict_pool_keeps_root_above_base = strict.check() == z3.unsat

    equality = z3.SolverFor("QF_LRA")
    equality.add(
        d + ell == x + delta,
        pi == d - delta,
        pool == pi,
        ell + pool != x,
    )
    equality_pool_returns_root_to_base = equality.check() == z3.unsat

    # Exact physical support census for arbitrary donor subsets. Goods 0..2
    # form D, 3..4 form L, and 5..10 are exterior owner/charity goods.
    goods = set(range(11))
    d_support = {0, 1, 2}
    l_support = {3, 4}
    exterior = goods - d_support - l_support
    source_old = {5, 6}
    charity_old = {10}
    support_cases = 0
    for mask in range(1, 1 << len(exterior)):
        ordered = tuple(sorted(exterior))
        packet = {ordered[j] for j in range(len(ordered)) if mask & (1 << j)}
        root_new = l_support | packet
        source_new = d_support
        charity_new = (charity_old - packet) | (source_old - packet)
        residual = exterior - packet - (source_old - packet) - (charity_old - packet)
        targets = (root_new, source_new, charity_new, residual)
        assert set().union(*targets) == goods
        assert sum(map(len, targets)) == len(goods)
        assert not (root_new & d_support)
        assert not (charity_new & d_support)
        support_cases += 1

    assert all((
        root_margin_identity_exact,
        strict_pool_keeps_root_above_base,
        equality_pool_returns_root_to_base,
        support_cases > 0,
    ))
    theorem = ROOT / "results/ROOT_WHOLE_HIT_GLOBAL_SACRIFICE_POOL_OR_UNDERPAYMENT_THEOREM_20260814.md"
    envelope = ROOT / "results/NONROOT_CURRENT_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    complete_pool = ROOT / "results/COMPLETE_HOLDER_PRICE_POOL_REVERSAL_OR_UNDERPAYMENT_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-whole-hit-global-sacrifice-pool-or-underpayment-audit-v1",
        "status": "ROOT_CURRENT_WHOLE_HIT_REDUCED_TO_AGGREGATE_UNDERPAYMENT_OR_EQUALITY",
        "root_margin_identity_exact": root_margin_identity_exact,
        "strict_pool_keeps_root_above_base": strict_pool_keeps_root_above_base,
        "equality_pool_returns_root_to_base": equality_pool_returns_root_to_base,
        "physical_pool_allocations_checked": support_cases,
        "root_and_charity_targets_avoid_named_packet": True,
        "remaining_separator": "all_compatible_pools_at_most_root_price",
        "full_T_L_times_theorem_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, envelope, complete_pool, script)
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
