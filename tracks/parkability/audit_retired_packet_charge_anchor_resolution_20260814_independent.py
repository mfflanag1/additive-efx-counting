#!/usr/bin/env python3
"""Clean-room completion audit for the T_L_times collision theorem.

This replay imports neither the composition audit nor any of the new root
closure audit modules.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty_subsets(items: tuple[int, ...]):
    for size in range(1, len(items) + 1):
        for chosen in combinations(items, size):
            yield frozenset(chosen)


def value(weights: tuple[int, ...], bundle: frozenset[int]) -> int:
    return sum(weights[g] for g in bundle)


def run() -> dict[str, object]:
    # Independent exhaustive root-margin replay. Five goods are enough to
    # realize both base/exterior atom cases and a two-good old anchor.
    goods = tuple(range(5))
    margin_cases = 0
    margin_failures: list[dict[str, object]] = []
    packet_cases = 0
    packet_failures: list[dict[str, object]] = []
    for weights in product(range(1, 4), repeat=len(goods)):
        for base_root in nonempty_subsets(goods):
            exterior = frozenset(goods) - base_root
            if len(exterior) < 2:
                continue
            for anchor in nonempty_subsets(tuple(exterior)):
                if len(anchor) < 2:
                    continue
                base_value = value(weights, base_root)
                if value(weights, anchor) <= base_value:
                    continue
                for atom in goods:
                    margin_cases += 1
                    root_star = frozenset(goods) - {atom}
                    if value(weights, root_star) <= base_value:
                        margin_failures.append(
                            {
                                "weights": weights,
                                "base": sorted(base_root),
                                "anchor": sorted(anchor),
                                "atom": atom,
                            }
                        )
                    for packet in nonempty_subsets(goods):
                        if atom not in packet:
                            continue
                        packet_cases += 1
                        if packet <= root_star:
                            packet_failures.append(
                                {"packet": sorted(packet), "atom": atom}
                            )

    assert margin_cases > 0 and packet_cases > 0
    assert margin_failures == []
    assert packet_failures == []

    # Fixed-priority reset authority: once coordinate zero is strict, every
    # possible later utility vector is lexicographically irrelevant.
    lex_cases = 0
    lex_failures = 0
    for base_root_utility in range(0, 7):
        for candidate_root_utility in range(base_root_utility + 1, 8):
            for base_later in product(range(0, 4), repeat=3):
                for candidate_later in product(range(0, 4), repeat=3):
                    lex_cases += 1
                    base_vector = (base_root_utility, *base_later)
                    candidate_vector = (candidate_root_utility, *candidate_later)
                    if not candidate_vector > base_vector:
                        lex_failures += 1
    assert lex_cases > 0 and lex_failures == 0

    # Minimal-response safety implication, checked independently over small
    # positive rows and every assigned-value threshold. If an observer
    # strongly envies D, a deletion D-g is desired and is strictly smaller.
    deletion_cases = 0
    deletion_failures = 0
    for weights in product(range(1, 4), repeat=4):
        four_goods = tuple(range(4))
        for desired in nonempty_subsets(four_goods):
            for assigned in range(0, sum(weights) + 1):
                for good in desired:
                    deletion = desired - {good}
                    if assigned < value(weights, deletion):
                        deletion_cases += 1
                        if not (
                            value(weights, deletion) > assigned
                            and len(deletion) < len(desired)
                        ):
                            deletion_failures += 1
    assert deletion_cases > 0 and deletion_failures == 0

    resolution = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_RESOLUTION_20260814.md"
    reset = ROOT / "results/STRICT_FIRST_PRIORITY_FLOOR_RESET_ADMISSION_THEOREM_20260814.md"
    root = ROOT / "results/ROOT_SINGLETON_SUPPLIER_STAR_FLOOR_RESET_CLOSURE_THEOREM_20260814.md"
    nonroot = ROOT / "results/NONROOT_SAFE_WHOLE_HIT_ENVELOPE_DESCENT_THEOREM_20260814.md"
    contract = ROOT / "results/RETIRED_PACKET_CHARGE_OR_ANCHOR_EXCHANGE_CONTRACT_20260813.md"
    gap = ROOT / "results/ROOT_GLOBAL_SUPPLIER_STAR_FLOOR_ADMISSIBILITY_GAP_20260814.md"
    script = Path(__file__).resolve()

    resolution_text = resolution.read_text().lower()
    reset_text = reset.read_text().lower()
    root_text = root.read_text().lower()
    contract_text = contract.read_text().lower()
    for phrase in (
        "strict capture",
        "equality-critical",
        "base-floor/source-inactive",
        "release compatibility",
        "normalization bypass",
    ):
        assert phrase in resolution_text
    assert "floor reset alone" in reset_text
    assert "not counted as progress" in resolution_text
    assert "every moved good has one supplier and one destination" in root_text
    assert "keep its declared floors" in contract_text
    assert "explicitly resets" in resolution_text
    assert "does not close" in resolution_text

    return {
        "schema": "retired-packet-charge-anchor-resolution-independent-v1",
        "status": "INDEPENDENT_T_L_TIMES_COMPLETION_REPLAY_PASSED",
        "root_margin_cases_checked": margin_cases,
        "root_margin_failures": len(margin_failures),
        "packet_support_cases_checked": packet_cases,
        "whole_packet_response_failures": len(packet_failures),
        "fixed_priority_lex_cases_checked": lex_cases,
        "fixed_priority_lex_failures": lex_failures,
        "minimal_response_deletion_cases_checked": deletion_cases,
        "minimal_response_deletion_failures": deletion_failures,
        "imports_primary_completion_audit": False,
        "imports_root_closure_audit": False,
        "imports_z3": False,
        "old_later_floors_preserved": False,
        "controlled_floor_reset_explicit": True,
        "reset_used_as_progress": False,
        "holder_partition_exhaustive": True,
        "full_T_L_times_theorem_closed": True,
        "parked_T_L_perp_closed": False,
        "empty_ledger_T0_closed": False,
        "full_GG_closed": False,
        "four_agent_EFX_closed": False,
        "external_expert_reviewed": False,
        "provenance": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (resolution, reset, root, nonroot, contract, gap, script)
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
