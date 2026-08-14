#!/usr/bin/env python3
"""Exact audit of the cap-free scalar family realizing the bi-row cut."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subsets(values: tuple[Fraction, ...]):
    for size in range(len(values) + 1):
        for indices in combinations(range(len(values)), size):
            yield sum((values[i] for i in indices), Fraction(0))


def check_family(size: int, equality: bool) -> dict:
    # Positive exact weights, with the singleton case kept nondegenerate.
    recipient = tuple(Fraction(i + 2) for i in range(size))
    total = sum(recipient, Fraction(0))
    d = total if equality else total - Fraction(1)
    mu = total - d
    scale = Fraction(3, 2)
    holder = tuple(scale * value for value in recipient)
    slack = Fraction(0)
    mode_value = Fraction(0)
    root_slack = scale * d / 2
    root_base = sum(holder) + 1
    root_rest = root_base + root_slack - sum(holder)
    assert root_rest > 0

    checked = 0
    feasible = 0
    for s_value, h_value in zip(subsets(recipient), subsets(holder)):
        checked += 1
        if s_value >= d:
            feasible += 1
            assert h_value > slack + mode_value
            assert h_value > root_slack + mode_value
            assert h_value < root_base
    assert mode_value < sum(holder) - slack
    if equality:
        assert feasible == 1
    else:
        assert mu > 0
    return {
        "packet_size": size,
        "branch": "equality" if equality else "strict",
        "subsets_checked": checked,
        "recipient_feasible_subsets": feasible,
        "d": str(d),
        "mu": str(mu),
        "cut_verified": True,
        "full_packet_underpayment": True,
        "root_band_verified": True,
        "root_base": str(root_base),
        "root_slack": str(root_slack),
        "root_rest": str(root_rest),
    }


def run(repo: Path) -> dict:
    cases = [
        check_family(size, equality)
        for size in range(1, 9)
        for equality in (False, True)
    ]
    theorem = repo / "results/RETIRED_PACKET_BIROW_CUT_SCALAR_REALIZABILITY_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "retired-packet-birow-cut-scalar-realizability-v1",
        "status": "BIROW_CUT_CAPFREE_SCALAR_REALIZABILITY",
        "formula": "v_h(g)=L*v_s(g), sigma=0, M_h(T)=0",
        "branches": ["strict", "equality"],
        "representative_packet_sizes": [1, 2, 3, 4, 5, 6, 7, 8],
        "cases": cases,
        "all_cases_verified": all(case["cut_verified"] for case in cases),
        "all_root_band_cases_verified": all(
            case["root_band_verified"] for case in cases
        ),
        "full_T_L_times_theorem_refuted": False,
        "smallest_missing_operation": "global cut-to-anchor conversion",
        "claim_boundary": (
            "analytic cap-free row-local no-go with exact finite replays; "
            "not a complete GG state or theorem counterexample"
        ),
        "provenance": {
            "script": str(script.relative_to(repo)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(repo)),
            "theorem_sha256": sha256(theorem),
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
        "all_cases_verified": result["all_cases_verified"],
        "full_theorem_refuted": result["full_T_L_times_theorem_refuted"],
    }, indent=2))


if __name__ == "__main__":
    main()
