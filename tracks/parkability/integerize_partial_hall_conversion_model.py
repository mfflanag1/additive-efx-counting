#!/usr/bin/env python3
"""Integerize a realizable two-good-per-bundle aggregate conversion model."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(text: str) -> Fraction:
    text = text.strip()
    match = re.fullmatch(r"\(/\s+(-?\d+)(?:\.0)?\s+(\d+)(?:\.0)?\)", text)
    if match:
        return Fraction(int(match.group(1)), int(match.group(2)))
    match = re.fullmatch(r"(-?\d+)(?:\.0)?", text)
    if match:
        return Fraction(int(match.group(1)))
    raise ValueError(f"unsupported rational expression: {text}")


def run(source: Path, output: Path) -> dict:
    document = json.loads(source.read_text())
    if document["status"] != "AGGREGATE_COUNTEREXAMPLE":
        raise ValueError("source is not a completed aggregate counterexample")
    model = document["model"]
    selected = [[rational(value) for value in row] for row in model["selected_goods"]]
    remainders = [
        [rational(value) for value in row] for row in model["remainder_totals"]
    ]
    floaters = [rational(value) for value in model["floaters"]]
    values = []
    row_scales = []
    for observer in range(4):
        entries = [
            value
            for bundle in range(4)
            for value in (selected[observer][bundle], remainders[observer][bundle])
        ] + [floaters[observer]]
        scale = math.lcm(*(value.denominator for value in entries))
        row_scales.append(scale)
        values.append([int(value * scale) for value in entries])
    if min(min(row) for row in values) <= 0:
        raise AssertionError("integerization did not preserve positivity")
    artifact = {
        "schema": "partial-hall-conversion-model-integerization-v1",
        "source": str(source),
        "source_sha256": sha256(source),
        "meaning": (
            "Exact positive integer realization with selected and remainder "
            "goods alternating within each of four two-good base bundles."
        ),
        "row_scales": row_scales,
        "base_masks": [3, 12, 48, 192],
        "floater": 8,
        "values": values,
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2))


if __name__ == "__main__":
    main()
