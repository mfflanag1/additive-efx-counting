#!/usr/bin/env python3
"""Exact support audit for supplier-aligned base donation packet spread."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> dict[str, object]:
    # Labels 0..3 are owners (root 0); label 4 is charity.
    cells = range(5)
    goods = tuple(range(5))
    multi_cases = 0
    multi_whole_hits = 0
    singleton_cases = 0
    singleton_whole_hit_targets: set[int] = set()
    singleton_residual_cases = 0
    off_packet_cases = 0
    off_packet_whole_hits = 0

    for base_cell in itertools.product(cells, repeat=len(goods)):
        x_r = {g for g in goods if base_cell[g] == 0}
        outside_root = set(goods) - x_r
        for sp_mask in range(1, 1 << len(goods)):
            s_plus = {g for g in goods if sp_mask & (1 << g)}
            if not s_plus <= outside_root:
                continue
            for u_mask in range(0, 1 << len(goods)):
                u = {g for g in goods if u_mask & (1 << g)}
                if not u <= x_r:
                    continue
                k = s_plus | u
                residual_outside = outside_root - k
                if u and s_plus and residual_outside:
                    for h in residual_outside:
                        off_targets = {
                            cell: {z for z in goods if base_cell[z] == cell}
                            for cell in cells
                        }
                        off_targets[base_cell[h]].remove(h)
                        off_targets[0].add(h)
                        off_packet_cases += 1
                        for target in off_targets.values():
                            if k <= target:
                                off_packet_whole_hits += 1
                for g in s_plus:
                    targets = {
                        cell: {h for h in goods if base_cell[h] == cell}
                        for cell in cells
                    }
                    targets[base_cell[g]].remove(g)
                    targets[0].add(g)
                    assert set().union(*targets.values()) == set(goods)
                    assert sum(len(t) for t in targets.values()) == len(goods)

                    if len(s_plus) >= 2:
                        multi_cases += 1
                        for target in targets.values():
                            if k <= target:
                                multi_whole_hits += 1
                    else:
                        singleton_cases += 1
                        for cell, target in targets.items():
                            if k <= target:
                                singleton_whole_hit_targets.add(cell)
                                # Audit every proper response D in the root
                                # target that contains K.
                                if cell == 0:
                                    ordered = tuple(sorted(target))
                                    for d_mask in range(1, 1 << len(ordered)):
                                        d = {
                                            ordered[j]
                                            for j in range(len(ordered))
                                            if d_mask & (1 << j)
                                        }
                                        if d == target or not k <= d:
                                            continue
                                        residual = target - d
                                        assert residual
                                        assert residual <= (x_r - u)
                                        assert d == (x_r - residual) | {g}
                                        singleton_residual_cases += 1

    assert multi_cases > 0
    assert multi_whole_hits == 0
    assert singleton_cases > 0
    assert singleton_whole_hit_targets <= {0}
    assert singleton_residual_cases > 0
    assert off_packet_cases > 0
    assert off_packet_whole_hits == 0

    theorem = ROOT / "results/SUPPLIER_ALIGNED_BASE_DONATION_PACKET_SPREAD_THEOREM_20260814.md"
    dependency = ROOT / "results/NONDEGENERATE_ROOT_EQUALITY_BASE_RESTORATION_LEMMA_20260814.md"
    equality_admission = ROOT / "results/ROOT_EQUALITY_BASE_RESTORATION_PACKET_SPREAD_ADMISSION_THEOREM_20260814.md"
    blocker = ROOT / "results/ROOT_DONATION_GLOBAL_BLOCKER_LEMMA_20260811.md"
    return {
        "schema": "supplier-aligned-base-donation-packet-spread-audit-v1",
        "status": "SUPPORT_SPREAD_GENERAL_ADMISSION_OPEN_EQUALITY_FACE_ADMITTED",
        "multi_surplus_cases_checked": multi_cases,
        "multi_surplus_whole_target_hits": multi_whole_hits,
        "singleton_surplus_cases_checked": singleton_cases,
        "singleton_whole_hit_target_cells": sorted(singleton_whole_hit_targets),
        "singleton_proper_whole_packet_response_residuals_checked": (
            singleton_residual_cases
        ),
        "off_packet_donation_cases_checked": off_packet_cases,
        "off_packet_whole_target_hits": off_packet_whole_hits,
        "remaining_root_terminal": (
            "restoration_donation_transition_admission_then_root_price"
        ),
        "admissible_transition_proved": False,
        "equality_face_transition_admitted": True,
        "claim_boundary": (
            "exact support census only; it proves no target contains the whole "
            "packet in the stated donation geometries, but does not prove that "
            "base restoration/donation is an admissible ledger transition"
        ),
        "full_T_L_times_theorem_closed": False,
        "sources": {
            str(theorem.relative_to(ROOT)): sha256(theorem),
            str(dependency.relative_to(ROOT)): sha256(dependency),
            str(equality_admission.relative_to(ROOT)): sha256(equality_admission),
            str(blocker.relative_to(ROOT)): sha256(blocker),
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
