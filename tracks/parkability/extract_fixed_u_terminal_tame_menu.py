#!/usr/bin/env python3
"""Extract and audit a realization-free tame menu for a terminal profile."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path

from .run_fixed_u_multi_split_chart_theorem import (
    audit_certificate_at_profile,
    close_profile,
)


def rows(raw, key):
    return {
        observer: {role: Fraction(value) for role, value in row.items()}
        for observer, row in raw[key].items()
    }


def run(input_path, output_path, edge_cap, pattern_budget, timeout_seconds):
    raw = json.loads(input_path.read_text())
    totals = rows(raw, "terminal_profile_totals")
    minima = rows(raw, "terminal_profile_minima")
    status, certificate, detail = close_profile(
        totals, minima, edge_cap, pattern_budget, timeout_seconds
    )
    assert certificate is not None, (status, detail)
    audit_certificate_at_profile(certificate, totals, minima, edge_cap)
    result = {
        "schema": "fixed-u-terminal-tame-menu-extraction-v1",
        "status": "VERIFIED_REALIZATION_FREE_TAME_MENU",
        "source": str(input_path),
        "source_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
        "oracle_status": status,
        "detail": detail,
        "certificate": certificate,
        "claim_boundary": (
            "This exact full side-pattern menu repairs the displayed profile. "
            "It does not prove the tame-menu chart theorem for every profile."
        ),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--edge-cap", type=int, default=4)
    parser.add_argument("--pattern-budget", type=int, default=20000)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    result = run(
        args.input, args.output, args.edge_cap,
        args.pattern_budget, args.timeout_seconds,
    )
    print(json.dumps({
        "status": result["status"],
        "split_roles": result["certificate"]["split_roles"],
        "pattern_count": result["certificate"]["pattern_count"],
        "detail": result["detail"],
    }, indent=2))


if __name__ == "__main__":
    main()
