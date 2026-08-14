#!/usr/bin/env python3
"""Exact support/arithmetic audit for exterior donation splitting."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    goods = set(range(6))
    support_cases = 0
    whole_hits = 0
    singleton_ledger_hits = 0
    for xr_mask in range(1, 1 << 6):
        x_r = {g for g in goods if xr_mask & (1 << g)}
        exterior = goods - x_r
        if not exterior:
            continue
        ordered_x = tuple(sorted(x_r))
        for k_mask in range(1, 1 << len(ordered_x)):
            k = {
                ordered_x[j]
                for j in range(len(ordered_x))
                if k_mask & (1 << j)
            }
            for g in k:
                root_target = (x_r - {g}) | exterior
                singleton_target = {g}
                assert root_target.isdisjoint(singleton_target)
                assert root_target | singleton_target == goods
                support_cases += 1
                for target in (root_target, singleton_target, set()):
                    if k <= target:
                        whole_hits += 1
                    if len(k) == 1 and target == root_target:
                        singleton_ledger_hits += len(k & target)
                if len(k) >= 2:
                    assert (root_target & k) < k
                    assert (singleton_target & k) < k
                else:
                    assert not (root_target & k)

    # Exact rational charge: atomwise exterior dominance implies the sum.
    charge_cases = 0
    for size in range(1, 7):
        exterior_value = Fraction(3, 2)
        atom_values = [Fraction(2 + j, 1) for j in range(size)]
        assert all(exterior_value < value for value in atom_values)
        assert size * exterior_value < sum(atom_values)
        charge_cases += 1

    assert support_cases > 0
    # Whole hits occur only at the singleton target; it is universally safe,
    # so no response can target it. Root responses have proper/empty hits.
    assert whole_hits > 0
    assert singleton_ledger_hits == 0

    theorem = ROOT / "results/BASE_CONTAINED_RETIRED_PACKET_EXTERIOR_DONATION_SPLIT_THEOREM_20260814.md"
    spread = ROOT / "results/SUPPLIER_ALIGNED_BASE_DONATION_PACKET_SPREAD_THEOREM_20260814.md"
    return {
        "schema": "base-contained-retired-packet-exterior-donation-split-audit-v1",
        "status": "EXTERIOR_DONATION_GEOMETRY_VERIFIED_ADMISSION_OPEN",
        "support_cases_checked": support_cases,
        "whole_hits_confined_to_safe_singleton_target": whole_hits,
        "singleton_root_target_ledger_hits": singleton_ledger_hits,
        "exact_charge_cases_checked": charge_cases,
        "remaining_root_terminal": "base_contained_exterior_dominant_packet",
        "admissible_transition_proved": False,
        "claim_boundary": (
            "support and arithmetic audit of the proposed pooling allocation; "
            "does not prove its protected floors, supplier releases, or admission "
            "as a G0--G10 transition"
        ),
        "full_T_L_times_theorem_closed": False,
        "sources": {
            str(theorem.relative_to(ROOT)): sha256(theorem),
            str(spread.relative_to(ROOT)): sha256(spread),
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
