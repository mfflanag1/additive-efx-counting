#!/usr/bin/env python3
"""Exact finite/set audit for base-crossing reference-floor rigidity."""

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
    # Exhaust all base-owner labels of four goods and all nonempty packets.
    # If K is contained in X_s, disjoint base ownership forbids K cap X_r.
    goods = range(4)
    owners = range(4)
    checked = 0
    contradictions = 0
    for base_owner in itertools.product(owners, repeat=len(tuple(goods))):
        r, s = 0, 1
        x_r = {g for g in goods if base_owner[g] == r}
        x_s = {g for g in goods if base_owner[g] == s}
        assert x_r.isdisjoint(x_s)
        for mask in range(1, 1 << len(tuple(goods))):
            k = {g for g in goods if mask & (1 << g)}
            checked += 1
            if k <= x_s and k & x_r:
                contradictions += 1
    assert contradictions == 0

    # Audit the set identity behind reference-floor rigidity: when
    # Q=B dot-union T dot-union R equals W, every element of T lies in W.
    support_cases = 0
    for labels in itertools.product(range(4), repeat=4):
        # 0=B, 1=T, 2=R, 3=outside; these labels make B,T,R disjoint.
        b = {g for g, label in enumerate(labels) if label == 0}
        t = {g for g, label in enumerate(labels) if label == 1}
        rr = {g for g, label in enumerate(labels) if label == 2}
        q = b | t | rr
        w = set(q)
        assert t <= w
        support_cases += 1

    # Current-floor equality is impossible when a genuinely transferred
    # packet is disjoint from the old current bundle.
    current_floor_cases = 0
    for y_mask in range(1 << 4):
        y = {g for g in goods if y_mask & (1 << g)}
        outside = set(goods) - y
        for t_mask in range(1, 1 << 4):
            t = {g for g in goods if t_mask & (1 << g)}
            if t <= outside:
                current_floor_cases += 1
                assert not (t <= y)

    theorem = ROOT / "results/BASE_CROSSING_REFERENCE_FLOOR_RIGIDITY_LEMMA_20260814.md"
    dependency = ROOT / "results/NONDEGENERATE_ROOT_EQUALITY_BASE_RESTORATION_LEMMA_20260814.md"
    return {
        "schema": "base-crossing-reference-floor-rigidity-audit-v1",
        "status": "BASE_FLOOR_EQUALITY_FACE_EXCLUDED",
        "base_packet_cases_checked": checked,
        "forbidden_base_crossings_found": contradictions,
        "reference_support_cases_checked": support_cases,
        "current_floor_foreign_transfer_cases_checked": current_floor_cases,
        "remaining_root_terminal": (
            "strict_or_nonbase_reference_floor_supplier_overlap_cut_or_"
            "root_payment_deficiency"
        ),
        "full_T_L_times_theorem_closed": False,
        "sources": {
            str(theorem.relative_to(ROOT)): sha256(theorem),
            str(dependency.relative_to(ROOT)): sha256(dependency),
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
