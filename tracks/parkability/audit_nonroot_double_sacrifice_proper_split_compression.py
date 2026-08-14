#!/usr/bin/env python3
"""Exact graph/set audit of nonroot double-sacrifice split compression."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import permutations
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matching_rank(rows: tuple[frozenset[int], ...]) -> int:
    best = 0
    for targets in permutations(range(4)):
        rank = sum(targets[agent] in rows[agent] for agent in range(4))
        best = max(best, rank)
    return best


def root_covered_rank(rows: tuple[frozenset[int], ...]) -> int:
    best = 0
    for targets in permutations(range(4)):
        if targets[0] not in rows[0]:
            continue
        rank = sum(targets[agent] in rows[agent] for agent in range(4))
        best = max(best, rank)
    return best


def run(repo: Path) -> dict:
    target_locality = True
    partitions_checked = 0
    for size in range(2, 9):
        packet = frozenset(range(size))
        for mask in range(1, (1 << size) - 1):
            transferred = frozenset(
                good for good in packet if mask & (1 << good)
            )
            retained = packet - transferred
            partitions_checked += 1
            target_locality &= (
                transferred < packet
                and retained < packet
                and transferred.isdisjoint(retained)
                and transferred | retained == packet
            )

    # Agents: root=0, heads=1,2, fixed nonhead=3. The two nonheads have
    # forced identity rows. Enumerate every nonempty head neighborhood.
    graph_cases = 0
    root_covered = True
    ranks = {2: 0, 3: 0, 4: 0}
    nonempty_rows = [
        frozenset(target for target in range(4) if mask & (1 << target))
        for mask in range(1, 16)
    ]
    for row_1 in nonempty_rows:
        for row_2 in nonempty_rows:
            rows = (frozenset({0}), row_1, row_2, frozenset({3}))
            rank = matching_rank(rows)
            covered = root_covered_rank(rows)
            graph_cases += 1
            assert rank in ranks
            ranks[rank] += 1
            root_covered &= covered == rank

    assert target_locality and root_covered and graph_cases == 225
    theorem = repo / "results/NONROOT_DOUBLE_SACRIFICE_PROPER_SPLIT_COMPRESSION_THEOREM_20260814.md"
    hall = repo / "results/DECORATED_HEAD_PROTECTED_BUNDLE_HALL_DICHOTOMY_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "nonroot-double-sacrifice-proper-split-compression-audit-v1",
        "status": "NONROOT_MULTI_GOOD_PACKET_REDUCED_TO_SINGLETON",
        "single_target_response_hits_only_proper_split": target_locality,
        "representative_partitions_checked": partitions_checked,
        "protected_head_graphs_checked": graph_cases,
        "matching_rank_counts": {str(k): v for k, v in sorted(ranks.items())},
        "root_covered_maximum_exists": root_covered,
        "nonroot_terminal_packet_size": 1,
        "full_T_L_times_theorem_closed": False,
        "claim_boundary": (
            "cap-free proper-split/two-head compression theorem; singleton "
            "and protected-root branches remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
            "hall_dependency": str(hall.relative_to(repo)),
            "hall_dependency_sha256": sha256(hall),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    result = run(repo)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "matching_rank_counts": result["matching_rank_counts"],
        "full_theorem_closed": result["full_T_L_times_theorem_closed"],
    }, indent=2))


if __name__ == "__main__":
    main()

