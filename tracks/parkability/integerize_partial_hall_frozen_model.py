#!/usr/bin/env python3
"""Convert a rational frozen-cell model to primitive positive integer rows."""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import reduce
from math import gcd, lcm
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    values = []
    for row in document["model_values"]:
        denominator_lcm = lcm(*(entry["denominator"] for entry in row))
        integer_row = [
            entry["numerator"] * (denominator_lcm // entry["denominator"])
            for entry in row
        ]
        row_gcd = reduce(gcd, integer_row)
        values.append([entry // row_gcd for entry in integer_row])
    artifact = {
        "schema": "partial-hall-frozen-model-integerization-v1",
        "status": "EXACT_INTEGERIZATION",
        "meaning": (
            "Each positive rational valuation row is multiplied by its common "
            "denominator and divided by its row gcd. All within-row additive "
            "comparisons are therefore preserved exactly."
        ),
        "source": str(source),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "fixed_state": document["fixed_state"],
        "values": values,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
