#!/usr/bin/env python3
"""Extract normalized valuation rows from a cvc5 dumped model."""

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


VALUE_DEFINITION = re.compile(
    r"^\(define-fun value_(\d+)_(\d+) \(\) Real (.+)\)$"
)


def parse_rational(raw: str) -> Fraction:
    text = raw.strip()
    if text.startswith("(/ ") and text.endswith(")"):
        numerator, denominator = text[3:-1].split()
        return Fraction(int(numerator), int(denominator))
    if text.startswith("(- ") and text.endswith(")"):
        return -parse_rational(text[3:-1])
    return Fraction(text)


def decode(stdout: str, n: int, m: int) -> tuple[tuple[int, ...], ...]:
    entries = {}
    for line in stdout.splitlines():
        match = VALUE_DEFINITION.fullmatch(line.strip())
        if match is None:
            continue
        agent, good = map(int, match.group(1, 2))
        key = agent, good
        if key in entries:
            raise ValueError("model repeats a valuation variable")
        entries[key] = parse_rational(match.group(3))
    expected = {(agent, good) for agent in range(n) for good in range(m)}
    if set(entries) != expected:
        raise ValueError("model does not define the requested valuation matrix")
    rows = []
    for agent in range(n):
        fractions = [entries[agent, good] for good in range(m)]
        denominator = math.lcm(*(value.denominator for value in fractions))
        row = [int(value * denominator) for value in fractions]
        divisor = math.gcd(*row)
        row = [value // divisor for value in row]
        if any(value <= 0 for value in row):
            raise ValueError("decoded valuations are not strictly positive")
        rows.append(tuple(row))
    return tuple(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--m", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.input.read_text())
    if raw.get("verdict") != "sat" or not isinstance(raw.get("stdout"), str):
        raise ValueError("input does not contain a cvc5 SAT model")
    values = decode(raw["stdout"], args.n, args.m)
    result = {
        "schema": "cvc5-valuation-model-v1",
        "n": args.n,
        "m": args.m,
        "source": str(args.input.resolve()),
        "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "values": [list(row) for row in values],
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
