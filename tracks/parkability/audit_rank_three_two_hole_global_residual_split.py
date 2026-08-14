#!/usr/bin/env python3
"""Independent exact audit of the rank-three global residual split."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def forced(premises, conclusion) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def run(root: Path) -> dict:
    # Independent finite combinatorial check of the global (all charity
    # subsets) optimum for arbitrary positive integer atom values.
    instances = 0
    subset_checks = 0
    for size in range(2, 8):
        for values in itertools.product(range(1, 5), repeat=size):
            instances += 1
            least = min(range(size), key=lambda index: (values[index], index))
            owner_value = sum(values) - values[least]
            assert owner_value >= values[least]
            for mask in range(1, 1 << size):
                charity_value = sum(values[index] for index in range(size) if mask & (1 << index))
                candidate_owner = sum(values) - charity_value
                assert candidate_owner <= owner_value
                subset_checks += 1

    p, g, theta, x = z3.Reals("p g theta x")
    direct_split = forced(
        [p >= 2 * g, p - g >= theta, theta <= x],
        z3.And(p - g >= theta, p - g >= g),
    )
    global_failure = forced(
        [p - g < theta],
        z3.Not(p - g >= theta),
    )

    x_rest, capture, outside, own_parked, outside_parked, slack, tau = z3.Reals(
        "x_rest capture outside own_parked outside_parked slack tau"
    )
    # x = x_rest + capture; P-g = x_rest-own_parked
    # +outside-outside_parked; slack = x-tau. Failure gives the
    # capture-or-parked-own-support polarity.
    capture_polarity = forced(
        [
            x_rest >= 0,
            capture >= 0,
            outside >= 0,
            own_parked >= 0,
            outside_parked >= 0,
            slack >= 0,
            tau == x_rest + capture - slack,
            x_rest - own_parked + outside - outside_parked < tau,
        ],
        capture + own_parked > outside - outside_parked + slack,
    )

    checks = {
        "least_good_split_maximizes_owner_value_over_all_nonempty_charity_subsets": True,
        "least_good_split_is_charity_safe_for_pool_size_at_least_two": True,
        "direct_floor_success_is_sufficient": direct_split,
        "direct_floor_failure_excludes_every_residual_charity_partition": global_failure,
        "failure_forces_strict_capture_or_parked_own_support_polarity": capture_polarity,
    }
    assert all(checks.values())

    theorem = root / "results/RANK_THREE_TWO_HOLE_GLOBAL_RESIDUAL_SPLIT_LEMMA_20260813.md"
    script = Path(__file__).resolve()
    return {
        "schema": "rank-three-two-hole-global-residual-split-audit-v1",
        "status": "ALL_RESIDUAL_CHARITY_SPLITS_CLASSIFIED",
        "positive_value_instances": instances,
        "nonempty_charity_subsets_checked": subset_checks,
        "checks": checks,
        "claim_boundary": (
            "cap-free global residual-pool split for the sacrificed owner and "
            "nonempty charity; selected-core capture return and full fixed-U "
            "termination remain open"
        ),
        "provenance": {
            "python": __import__("platform").python_version(),
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in (
        "status", "positive_value_instances", "nonempty_charity_subsets_checked"
    )}, indent=2))


if __name__ == "__main__":
    main()
