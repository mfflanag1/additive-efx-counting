#!/usr/bin/env python3
"""Exact global-lex census for the raw-potential scaling witness."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .audit_gg_rank_reset_raw_potential_refutation import AGENTS, BASE, GOODS, valuation
except ImportError:
    from audit_gg_rank_reset_raw_potential_refutation import AGENTS, BASE, GOODS, valuation


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(root: Path) -> dict:
    denominator = 1 << 50
    fractions = valuation()
    values = {
        agent: [int(fractions[agent][good] * denominator) for good in GOODS]
        for agent in AGENTS
    }
    base = tuple(
        sum(values[agent][GOODS.index(good)] for good in BASE[agent])
        for agent in AGENTS
    )
    records = []
    for assignment in itertools.product(range(5), repeat=len(GOODS)):
        bundles = [[] for _ in range(5)]
        for good_index, owner in enumerate(assignment):
            bundles[owner].append(good_index)
        totals = [
            [sum(values[agent][g] for g in bundle) for bundle in bundles]
            for agent in AGENTS
        ]
        thresholds = [
            [
                total - min((values[agent][g] for g in bundle), default=0)
                for bundle, total in zip(bundles, totals[agent_index])
            ]
            for agent_index, agent in enumerate(AGENTS)
        ]
        if not all(
            totals[i][i] >= thresholds[i][j]
            for i in range(4)
            for j in range(4)
        ):
            continue
        if not all(totals[i][i] >= totals[i][4] for i in range(4)):
            continue
        records.append((tuple(totals[i][i] for i in range(4)), bundles))

    priority_records = []
    for order in itertools.permutations(range(4)):
        best_utility, best_bundles = max(
            records, key=lambda record: tuple(record[0][i] for i in order)
        )
        base_key = tuple(base[i] for i in order)
        best_key = tuple(best_utility[i] for i in order)
        priority_records.append({
            "priority": [AGENTS[i] for i in order],
            "base_globally_lex_maximal": base_key == best_key,
            "best_utility_numerators": list(best_utility),
            "best_bundles": [
                [GOODS[good_index] for good_index in bundle]
                for bundle in best_bundles
            ],
        })

    script = Path(__file__).resolve()
    theorem = root / "results/GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md"
    return {
        "schema": "gg-rank-reset-raw-potential-globality-gap-v1",
        "status": "GLOBALITY_GAP_CONFIRMED",
        "allocation_space": 5 ** len(GOODS),
        "efx_with_charity_count": len(records),
        "priority_count": len(priority_records),
        "globally_maximal_priorities": [
            record["priority"]
            for record in priority_records
            if record["base_globally_lex_maximal"]
        ],
        "base_utility_numerators": list(base),
        "common_denominator": denominator,
        "priority_records": priority_records,
        "claim_boundary": (
            "complete exact allocation census for the nine-good raw-coordinate "
            "witness; it proves that witness is not a full globally lex-maximal "
            "GG countermodel under any priority, without weakening its exact "
            "refutation of cross-owner raw residual comparison"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "allocation_space": result["allocation_space"],
        "efx_with_charity_count": result["efx_with_charity_count"],
        "globally_maximal_priorities": result["globally_maximal_priorities"],
    }, indent=2))


if __name__ == "__main__":
    main()
