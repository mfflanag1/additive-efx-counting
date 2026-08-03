#!/usr/bin/env python3
"""Scan stored profiles for a blocked partial-EFX Nash maximizer."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .anneal_partial_linear_potential import exact_landscape
    from .fast_count import FastParkability
except ImportError:
    import core
    from anneal import atomic_json
    from anneal_partial_linear_potential import exact_landscape
    from fast_count import FastParkability


SCHEMA = "partial-nash-potential-corpus-scan-v2"


def matrices(path: Path) -> list[tuple[str, tuple[tuple[int, ...], ...]]]:
    try:
        document = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(document, dict):
        return []
    candidates = [
        ("values", document.get("values")),
        ("candidate_values", document.get("candidate_values")),
        ("post_wall_values", document.get("post_wall_values")),
        ("wall_values", document.get("wall_values")),
    ]
    lift = document.get("positive_nondegenerate_lift")
    if isinstance(lift, dict):
        candidates.append(("positive_nondegenerate_lift.values", lift.get("values")))
    records = []
    for key, raw in candidates:
        if raw is None:
            continue
        try:
            values = core.validate_values(raw, lower=1)
        except ValueError:
            continue
        records.append((key, values))
    return records


def run(directory: Path, output: Path, max_goods: int) -> dict:
    evaluators: dict[tuple[int, int], FastParkability] = {}
    seen = set()
    records = []
    exact_counterexamples = []
    exact_boundary_audits = []
    paths = sorted(directory.glob("*.json"))
    for position, path in enumerate(paths, 1):
        for value_key, values in matrices(path):
            n = len(values)
            m = len(values[0])
            if n != 4 or m > max_goods:
                continue
            if values in seen:
                continue
            seen.add(values)
            if (n, m) not in evaluators:
                evaluators[(n, m)] = FastParkability(n, m)
            evaluator = evaluators[(n, m)]
            landscape = evaluator.partial_linear_potential_landscape(
                values,
                potential="normalized_nash",
            )
            margin = landscape["best_maximizer_host_normalized_margin"]
            record = {
                "source": str(path),
                "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "value_key": value_key,
                "n": n,
                "m": m,
                "values_sha256": hashlib.sha256(
                    json.dumps(values, separators=(",", ":")).encode()
                ).hexdigest(),
                "eligible_base_count": landscape["eligible_base_count"],
                "maximizer_count": landscape["maximizer_count"],
                "insertable_maximizer_count": landscape[
                    "insertable_maximizer_count"
                ],
                "best_maximizer_host_normalized_margin": margin,
            }
            records.append(record)
            if margin <= 1e-12:
                exact = exact_landscape(
                    [list(row) for row in values],
                    "normalized_nash",
                    Fraction(1),
                )
                exact_margin = exact[
                    "best_maximizer_host_normalized_margin"
                ]
                boundary = {
                    **record,
                    "exact_maximizer_count": exact["maximizer_count"],
                    "exact_insertable_maximizer_count": exact[
                        "insertable_maximizer_count"
                    ],
                    "exact_best_maximizer_host_normalized_margin": exact_margin,
                }
                exact_boundary_audits.append(boundary)
                if exact["insertable_maximizer_count"] == 0:
                    exact_counterexamples.append({**record, "exact_audit": exact})
            if position % 100 == 0:
                print(
                    f"files={position}/{len(paths)} profiles={len(records)}",
                    flush=True,
                )
    ordered = sorted(
        records,
        key=lambda record: record["best_maximizer_host_normalized_margin"],
    )
    result = {
        "schema": SCHEMA,
        "status": (
            "BLOCKED_MAXIMIZER_FOUND"
            if exact_counterexamples
            else "NO_COUNTEREXAMPLE_IN_CORPUS"
        ),
        "meaning": (
            "Nash maximizers are selected by exact integer products and exact "
            "replay is attached to every zero/negative-margin endpoint; "
            "absence from this finite stored corpus is not a theorem"
        ),
        "directory": str(directory),
        "json_file_count": len(paths),
        "distinct_profile_count": len(records),
        "max_goods": max_goods,
        "zero_margin_profile_count": sum(
            abs(record["best_maximizer_host_normalized_margin"]) <= 1e-12
            for record in records
        ),
        "negative_margin_profile_count": sum(
            record["best_maximizer_host_normalized_margin"] < -1e-12
            for record in records
        ),
        "exact_counterexamples": exact_counterexamples,
        "exact_boundary_audits": exact_boundary_audits,
        "closest_profiles": ordered[:50],
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--max-goods", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.directory.is_dir() or args.max_goods < 1:
        parser.error("a valid directory and positive goods bound are required")
    run(args.directory, args.output, args.max_goods)


if __name__ == "__main__":
    main()
