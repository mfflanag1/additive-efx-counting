#!/usr/bin/env python3
"""Mine structural motifs from rank-three minimum-move CEGAR escapes."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

try:
    from .run_rank_three_global_lex_cegar import CURRENT, RECIPIENTS
except ImportError:
    from run_rank_three_global_lex_cegar import CURRENT, RECIPIENTS


def holder_map(allocation):
    return {
        good: recipient
        for recipient, goods in allocation.items()
        for good in goods
    }


def signature(allocation):
    old = holder_map(CURRENT)
    new = holder_map(allocation)
    edges = Counter(
        (old[good], new[good])
        for good in old
        if old[good] != new[good]
    )
    return ";".join(
        f"{source}->{target}:{count}"
        for (source, target), count in sorted(edges.items())
    )


def run(source: Path) -> dict:
    payload = json.loads(source.read_text())
    allocations = [
        record["blocking_efx_lex_allocation"]
        for record in payload["iterations"]
        if "blocking_efx_lex_allocation" in record
    ]
    old = holder_map(CURRENT)
    radius = Counter()
    signatures = Counter()
    unchanged = Counter()
    root_retention = Counter()
    recipient_frequency = {
        good: Counter() for good in old
    }
    for allocation in allocations:
        new = holder_map(allocation)
        radius[sum(old[good] != new[good] for good in old)] += 1
        signatures[signature(allocation)] += 1
        for recipient in RECIPIENTS:
            if sorted(allocation[recipient]) == sorted(CURRENT[recipient]):
                unchanged[recipient] += 1
        root_retention[
            sum(good in allocation["r"] for good in CURRENT["r"])
        ] += 1
        for good, recipient in new.items():
            recipient_frequency[good][recipient] += 1

    return {
        "schema": "rank-three-minmove-escape-analysis-v1",
        "source": str(source),
        "escape_count": len(allocations),
        "move_radius_histogram": {str(k): v for k, v in sorted(radius.items())},
        "distinct_transfer_signatures": len(signatures),
        "top_transfer_signatures": [
            {"signature": key, "count": count}
            for key, count in signatures.most_common(20)
        ],
        "unchanged_current_bundle_counts": dict(unchanged),
        "root_current_target_goods_retained_histogram": {
            str(k): v for k, v in sorted(root_retention.items())
        },
        "good_recipient_frequencies": {
            good: dict(counts) for good, counts in recipient_frequency.items()
        },
        "interpretation": (
            "bounded adversarial motif mining only; repeated minimum-move "
            "escapes suggest candidate packet operations but do not prove a "
            "cap-free selector"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "escape_count": result["escape_count"],
        "move_radius_histogram": result["move_radius_histogram"],
        "distinct_transfer_signatures": result["distinct_transfer_signatures"],
        "unchanged_current_bundle_counts": result["unchanged_current_bundle_counts"],
        "root_current_target_goods_retained_histogram": result[
            "root_current_target_goods_retained_histogram"
        ],
    }, indent=2))


if __name__ == "__main__":
    main()
