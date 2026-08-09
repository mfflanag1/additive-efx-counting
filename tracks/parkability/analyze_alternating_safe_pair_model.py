#!/usr/bin/env python3
"""Enumerate unrestricted safe pairs in a saved alternating gate model."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

try:
    from .decide_alternating_two_safe_bundle_gate import (
        desired_bundles,
        numeric_desired,
        numeric_safe,
        powerset,
    )
    from .run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, numeric_utilities
except ImportError:
    from decide_alternating_two_safe_bundle_gate import (
        desired_bundles,
        numeric_desired,
        numeric_safe,
        powerset,
    )
    from run_alternating_variable_packet_rooted_cegar import AGENTS, make_cell, numeric_utilities


SCHEMA = "alternating-safe-pair-model-analysis-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze(path: Path):
    payload = json.loads(path.read_text())
    sizes = tuple(payload["packet_sizes"])
    cell = make_cell(sizes)
    values = tuple(tuple(Fraction(entry) for entry in row) for row in payload["model"])
    own = numeric_utilities(values, cell["base_owner"])
    residual = tuple(
        good for good in range(cell["m"]) if good not in (cell["x"], cell["y"])
    )
    pairs = []
    for source in (2, 1):
        for desired_bundle in desired_bundles(cell):
            if not numeric_desired(values, own, source, desired_bundle):
                continue
            complement = tuple(good for good in residual if good not in desired_bundle)
            threshold = max(
                sum(values[3][good] for good in desired_bundle if good != removed)
                for removed in desired_bundle
            )
            for q_bundle in powerset(complement):
                if not numeric_safe(values, own, q_bundle):
                    continue
                q_value = sum(values[3][good] for good in q_bundle)
                if q_value < threshold:
                    continue
                pairs.append(
                    {
                        "source": AGENTS[source],
                        "desired_bundle": [cell["goods"][good] for good in desired_bundle],
                        "q_bundle": [cell["goods"][good] for good in q_bundle],
                        "desired_size": len(desired_bundle),
                        "q_size": len(q_bundle),
                        "allocated_size": len(desired_bundle) + len(q_bundle),
                        "q_slack": str(q_value - threshold),
                    }
                )
    pairs.sort(
        key=lambda record: (
            record["allocated_size"],
            record["desired_size"],
            record["q_size"],
            record["source"],
            record["desired_bundle"],
            record["q_bundle"],
        )
    )
    return {
        "schema": SCHEMA,
        "status": "UNRESTRICTED_SAFE_PAIRS_FOUND" if pairs else "NO_UNRESTRICTED_SAFE_PAIR",
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "pair_count": len(pairs),
        "minimum_allocated_size": pairs[0]["allocated_size"] if pairs else None,
        "minimum_pairs": pairs[:64],
        "claim_boundary": "analysis of one saved exact model, not a universal theorem",
        "provenance": {
            "script": "tracks/parkability/analyze_alternating_safe_pair_model.py",
            "script_sha256": sha256(Path(__file__).resolve()),
            "input": str(path),
            "input_sha256": sha256(path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.input)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                "status": result["status"],
                "pair_count": result["pair_count"],
                "minimum_allocated_size": result["minimum_allocated_size"],
                "minimum_pairs": result["minimum_pairs"][:16],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
