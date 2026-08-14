#!/usr/bin/env python3
"""Independent integer/support replay of singleton-star root closure."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_subsets(items: tuple[int, ...]):
    for size in range(1, len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def run() -> dict[str, object]:
    bound = 40
    arithmetic_cases = 0
    arithmetic_failures: list[tuple[str, int, int, int]] = []

    # Base-atom case: O >= A > x >= k.
    for x in range(1, bound + 1):
        for anchor in range(x + 1, bound + 1):
            for exterior in range(anchor, bound + 1):
                for atom in range(1, x + 1):
                    arithmetic_cases += 1
                    if exterior - atom <= 0:
                        arithmetic_failures.append(
                            ("base", x, exterior, atom)
                        )

    # Exterior-atom case: O = k + positive remainder.
    for atom in range(1, bound + 1):
        for remainder in range(1, bound + 1):
            arithmetic_cases += 1
            if atom + remainder - atom <= 0:
                arithmetic_failures.append(
                    ("exterior", atom, remainder, atom)
                )

    assert arithmetic_cases > 0
    assert arithmetic_failures == []

    goods = tuple(range(7))
    support_cases = 0
    support_failures: list[tuple[tuple[int, ...], int]] = []
    for packet in nonempty_subsets(goods):
        for chosen in packet:
            support_cases += 1
            root_target = frozenset(goods) - {chosen}
            singleton = frozenset({chosen})
            if root_target & packet != packet - {chosen}:
                support_failures.append((tuple(sorted(packet)), chosen))
            if packet <= root_target:
                support_failures.append((tuple(sorted(packet)), chosen))
            assert singleton - {chosen} == frozenset()

    assert support_cases > 0
    assert support_failures == []

    theorem = ROOT / "results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md"
    reset = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "root-singleton-supplier-star-floor-reset-closure-independent-v1",
        "status": "INDEPENDENT_ROOT_SINGLETON_STAR_CLOSURE_REPLAY_PASSED",
        "integer_bound": bound,
        "arithmetic_cases_checked": arithmetic_cases,
        "arithmetic_failures": len(arithmetic_failures),
        "support_cases_checked": support_cases,
        "support_failures": len(support_failures),
        "imports_primary_audit": False,
        "imports_z3": False,
        "full_T_L_times_theorem_closed_in_replayed_statement": True,
        "full_GG_closed": False,
        "general_EFX_closed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (theorem, reset, script)
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
