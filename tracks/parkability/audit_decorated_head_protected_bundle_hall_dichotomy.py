#!/usr/bin/env python3
"""Exhaustive graph audit of the protected-bundle Hall dichotomy."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_perfect_matching(rows):
    return any(all(permutation[i] in rows[i] for i in range(4))
               for permutation in itertools.permutations(range(4)))


def minimal_hall_witnesses(rows):
    witnesses = []
    agents = range(4)
    for size in range(1, 5):
        for subset in itertools.combinations(agents, size):
            neighborhood = set().union(*(rows[i] for i in subset))
            if len(neighborhood) >= size:
                continue
            if any(
                len(set().union(*(rows[i] for i in proper))) < len(proper)
                for proper_size in range(1, size)
                for proper in itertools.combinations(subset, proper_size)
            ):
                continue
            witnesses.append((subset, tuple(sorted(neighborhood))))
    return witnesses


def relations(heads):
    heads = frozenset(heads)
    row_options = []
    for agent in range(4):
        options = []
        for mask in range(1 << 4):
            row = frozenset(target for target in range(4) if mask >> target & 1)
            if agent in heads:
                if not row or agent in row:
                    continue
            elif agent not in row:
                continue
            options.append(row)
        row_options.append(tuple(options))
    yield from itertools.product(*row_options)


def classify(heads):
    heads = frozenset(heads)
    total = matching = deficient = 0
    witness_distribution = Counter()
    records = []
    for rows in relations(heads):
        total += 1
        if has_perfect_matching(rows):
            matching += 1
            continue
        deficient += 1
        witnesses = minimal_hall_witnesses(rows)
        assert witnesses
        for subset, neighborhood in witnesses:
            assert set(subset) & heads
            assert len(neighborhood) == len(subset) - 1
            witness_distribution[(len(subset), len(set(subset) & heads))] += 1
        records.append({
            "rows": [sorted(row) for row in rows],
            "minimal_witnesses": [
                {"sources": list(subset), "neighbors": list(neighborhood)}
                for subset, neighborhood in witnesses
            ],
        })
    return {
        "heads": sorted(heads),
        "relation_count": total,
        "perfect_matching_count": matching,
        "deficient_relation_count": deficient,
        "witness_distribution": {
            f"size_{size}_heads_{head_count}": count
            for (size, head_count), count in sorted(witness_distribution.items())
        },
        "deficient_records": records,
    }


def run(root: Path) -> dict:
    one_head = classify({0})
    two_head = classify({0, 1})
    assert one_head["relation_count"] == 7 * 8 ** 3
    assert two_head["relation_count"] == 7 ** 2 * 8 ** 2
    assert one_head["perfect_matching_count"] + one_head["deficient_relation_count"] == one_head["relation_count"]
    assert two_head["perfect_matching_count"] + two_head["deficient_relation_count"] == two_head["relation_count"]

    script = Path(__file__).resolve()
    theorem = root / "results/DECORATED_HEAD_PROTECTED_BUNDLE_HALL_DICHOTOMY_20260813.md"
    return {
        "schema": "decorated-head-protected-bundle-hall-dichotomy-audit-v1",
        "status": "ALL_PROTECTED_GRAPHS_MATCH_OR_HAVE_HEAD_DEFICIENCY_ONE",
        "one_head": one_head,
        "two_head": two_head,
        "claim_boundary": (
            "exhaustive graph theorem for four labeled owners; graph edges are "
            "analytic consequences, but packet splitting inside a Hall witness remains open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "one_head": {key: result["one_head"][key] for key in (
            "relation_count", "perfect_matching_count", "deficient_relation_count"
        )},
        "two_head": {key: result["two_head"][key] for key in (
            "relation_count", "perfect_matching_count", "deficient_relation_count"
        )},
    }, indent=2))


if __name__ == "__main__":
    main()
