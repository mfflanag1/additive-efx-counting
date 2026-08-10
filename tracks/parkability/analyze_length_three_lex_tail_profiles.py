#!/usr/bin/env python3
"""Audit lexicographic tail-payment modes on the frozen adversarial corpus."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .analyze_alternating_singleton_return_models import make_cell
    from .analyze_dual_mode_adversarial_profiles import (
        P,
        Q,
        R,
        S,
        allocation_efx,
        compatible_pair,
        labels,
        load_profiles,
        parse_value,
        submasks,
        subset_tables,
    )
except ImportError:
    from analyze_alternating_singleton_return_models import make_cell
    from analyze_dual_mode_adversarial_profiles import (
        P,
        Q,
        R,
        S,
        allocation_efx,
        compatible_pair,
        labels,
        load_profiles,
        parse_value,
        submasks,
        subset_tables,
    )


SCHEMA = "length-three-lex-tail-adversarial-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def witness_json(assigned, totals, goods, mode):
    return {
        "mode": mode,
        "bundles": {
            name: labels(assigned[agent], goods)
            for agent, name in enumerate(("p", "r", "s", "q"))
        },
        "utilities": [str(totals[agent][assigned[agent]]) for agent in range(4)],
    }


def analyze_profile(label, raw_values, sizes):
    cell = make_cell(sizes)
    values = tuple(tuple(parse_value(value) for value in row) for row in raw_values)
    totals, tails = subset_tables(values, cell["m"])
    tr, br, tq, bq = cell["packets"]
    base_bundles = ((cell["x"],), tr + br, (cell["y"],), tq + bq)
    base_masks = tuple(sum(1 << good for good in bundle) for bundle in base_bundles)
    base = tuple(totals[agent][base_masks[agent]] for agent in range(4))
    y_mask = 1 << cell["y"]
    full_without_y = ((1 << cell["m"]) - 1) ^ y_mask
    witnesses = {"p_first": None, "s_then_p": None}
    compatible_count = 0

    p_mask = full_without_y
    while True:
        remaining = full_without_y ^ p_mask
        q_mask = remaining
        while True:
            if compatible_pair(totals, tails, base, p_mask, q_mask):
                compatible_count += 1
                residual = remaining ^ q_mask
                for payment in submasks(residual):
                    if witnesses["p_first"] is None:
                        for mode in ("r_tail", "s_tail"):
                            assigned = [p_mask, 0, 0, q_mask]
                            if mode == "r_tail":
                                assigned[R], assigned[S] = payment, y_mask
                            else:
                                assigned[R], assigned[S] = y_mask, payment
                            if allocation_efx(totals, tails, assigned):
                                witnesses["p_first"] = witness_json(
                                    assigned, totals, cell["goods"], mode
                                )
                                break
                    if witnesses["s_then_p"] is None:
                        assigned = [p_mask, payment, y_mask, q_mask]
                        if allocation_efx(totals, tails, assigned):
                            witnesses["s_then_p"] = witness_json(
                                assigned, totals, cell["goods"], "r_tail_keep_y"
                            )
                        elif totals[S][payment] >= base[S]:
                            assigned = [p_mask, y_mask, payment, q_mask]
                            if allocation_efx(totals, tails, assigned):
                                witnesses["s_then_p"] = witness_json(
                                    assigned, totals, cell["goods"], "s_base_pay_r_y"
                                )
                    if all(witnesses.values()):
                        break
            if all(witnesses.values()) or q_mask == 0:
                break
            q_mask = (q_mask - 1) & remaining
        if all(witnesses.values()) or p_mask == 0:
            break
        p_mask = (p_mask - 1) & full_without_y

    return {
        "label": label,
        "packet_sizes": list(sizes),
        "compatible_pairs_examined": compatible_count,
        "witnesses": witnesses,
    }


def run(output: Path):
    root = Path(__file__).resolve().parents[2]
    profiles, inputs = load_profiles(root)
    records = [analyze_profile(*profile) for profile in profiles]
    result = {
        "schema": SCHEMA,
        "status": "EXACT_ADVERSARIAL_CORPUS_AUDIT",
        "profile_count": len(records),
        "p_first_escape_count": sum(
            record["witnesses"]["p_first"] is not None for record in records
        ),
        "s_then_p_escape_count": sum(
            record["witnesses"]["s_then_p"] is not None for record in records
        ),
        "profiles": records,
        "claim_boundary": {
            "proved": "an exact lex-tail escape for each listed frozen profile",
            "not_proved": "the cap-free adaptive-root/order lemma",
        },
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(root)),
            "script_sha256": sha256(Path(__file__).resolve()),
            "inputs": [
                {"path": str(path.relative_to(root)), "sha256": sha256(path)}
                for path in inputs
            ],
        },
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "profile_count",
                    "p_first_escape_count",
                    "s_then_p_escape_count",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
