#!/usr/bin/env python3
"""Enumerate exact minimal common-safe desired cores inside H+L+W."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from .audit_allocated_e_physical_packet_counterprofile import expand
from .run_fixed_u_full_packet_terminal_cegar import OWNERS


ROOT = Path(__file__).resolve().parents[2]
TARGET_PIECES = ("h", "l", "m", "gq", "gr")
CURRENT_TARGET_PIECES = {
    "r": ("a0", "a1"),
    "q": ("j", "k", "q0"),
    "d": TARGET_PIECES,
    "s": ("e", "p"),
}
SUPPLIER_PIECES = {
    "r": {"h"},
    "s": {"l"},
    "d": {"m", "gq", "gr"},
}


def enumerate_cores(values, goods, piece_of, thresholds):
    candidates = []
    for size in range(1, len(goods) + 1):
        for subset in itertools.combinations(goods, size):
            source_totals = {
                owner: sum((values[owner][good] for good in subset), Fraction(0))
                for owner in OWNERS
            }
            desired_sources = [
                owner for owner, amount in source_totals.items()
                if amount > thresholds[owner]
            ]
            if not desired_sources:
                continue
            safe = True
            for observer in OWNERS:
                amounts = [values[observer][good] for good in subset]
                if sum(amounts, Fraction(0)) - min(amounts) > thresholds[observer]:
                    safe = False
                    break
            if not safe:
                continue
            # Global inclusion minimality: deleting any good destroys desire
            # for every possible source at that source's declared threshold.
            if any(
                any(
                    source_totals[owner] - values[owner][good] > thresholds[owner]
                    for owner in OWNERS
                )
                for good in subset
            ):
                continue
            pieces = {piece_of[good] for good in subset}
            suppliers = sorted(
                supplier for supplier, owned in SUPPLIER_PIECES.items()
                if pieces & owned
            )
            candidates.append({
                "goods": list(subset),
                "pieces": sorted(pieces),
                "suppliers": suppliers,
                "desired_sources": desired_sources,
                "source_totals": {owner: str(amount) for owner, amount in source_totals.items()},
            })
    return candidates


def supplier_patterns(candidates):
    patterns = {}
    for row in candidates:
        key = ",".join(row["suppliers"])
        patterns[key] = patterns.get(key, 0) + 1
    return dict(sorted(patterns.items()))


def run(source: Path, output: Path):
    source = source.resolve()
    _, expansion, values, _, _ = expand(source)
    goods = tuple(good for piece in TARGET_PIECES for good in expansion[piece])
    piece_of = {
        good: piece for piece in TARGET_PIECES for good in expansion[piece]
    }
    base_thresholds = {owner: Fraction(1) for owner in OWNERS}
    current_thresholds = {
        owner: sum(
            (
                values[owner][good]
                for piece in CURRENT_TARGET_PIECES[owner]
                for good in expansion[piece]
            ),
            Fraction(0),
        )
        for owner in OWNERS
    }
    base_candidates = enumerate_cores(
        values, goods, piece_of, base_thresholds,
    )
    current_candidates = enumerate_cores(
        values, goods, piece_of, current_thresholds,
    )
    result = {
        "schema": "hlw-physical-response-core-analysis-v2",
        "status": "COMPLETE",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "target_pieces": list(TARGET_PIECES),
        "physical_target_good_count": len(goods),
        "base_thresholds": {owner: str(amount) for owner, amount in base_thresholds.items()},
        "base_minimal_core_count": len(base_candidates),
        "base_supplier_pattern_counts": supplier_patterns(base_candidates),
        "base_cores": base_candidates,
        "current_thresholds": {
            owner: str(amount) for owner, amount in current_thresholds.items()
        },
        "current_minimal_core_count": len(current_candidates),
        "current_supplier_pattern_counts": supplier_patterns(current_candidates),
        "current_cores": current_candidates,
        "source_sha256_driver": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact base-threshold and actual-current-threshold censuses for "
            "one physically realizable SAT profile. They are descriptive "
            "evidence, not a universal response classification."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
