#!/usr/bin/env python3
"""Replay scalar implications in the early-r dual-base reduction."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from z3 import Real, Solver, sat


ROOT = Path(__file__).resolve().parents[2]


def prove_unsat(name: str, assumptions: list, negated_claim) -> dict:
    solver = Solver()
    solver.add(*assumptions, negated_claim)
    status = solver.check()
    if status == sat:
        raise AssertionError(f"{name} is SAT: {solver.model()}")
    return {"name": name, "negated_status": str(status).upper()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/length_three_early_r_dual_base_scalar_audit.json"),
    )
    args = parser.parse_args()

    tr, br, tq = Real("tr"), Real("br"), Real("tq")
    r_minus, a_r, base_r = Real("r_minus"), Real("a_r"), Real("base_r")
    q_j, q_bq, q_missing = Real("q_j"), Real("q_bq"), Real("q_missing")
    r_j, r_bq = Real("r_j"), Real("r_bq")

    checks = [
        prove_unsat(
            "critical_pool_strictly_exceeds_r_base",
            [tr >= 0, br >= 0, tq > tr],
            br + tq <= br + tr,
        ),
        prove_unsat(
            "unsafe_boundary_is_below_r_base",
            [a_r >= 0, a_r <= r_minus, r_minus < base_r],
            a_r >= base_r,
        ),
        prove_unsat(
            "q_source_foreign_bottom_exceeds_own_bottom",
            [q_bq >= 0, q_missing >= 0, q_j > q_bq + q_missing],
            q_j <= q_bq,
        ),
        prove_unsat(
            "profitable_bottom_replacement_raises_r",
            [r_j >= 0, r_bq > r_j],
            base_r - r_j + r_bq <= base_r,
        ),
    ]

    profile = json.loads(
        (ROOT / "results/length_three_dual_mode_split_refutation.json").read_text()
    )
    names = ("tr0", "tr1", "br0", "br1", "tq0", "tq1", "bq0", "bq1", "x", "y", "f")
    index = {name: good for good, name in enumerate(names)}
    values = profile["values"]
    base_bundles = (
        ("x",),
        ("tr0", "tr1", "br0", "br1"),
        ("tq0", "tq1", "bq0", "bq1"),
        ("y",),
    )
    base = [
        sum(values[agent][index[good]] for good in bundle)
        for agent, bundle in enumerate(base_bundles)
    ]
    joint_suffix = (
        ("x", "tr1"),
        ("tr0", "br0", "tq0"),
        ("br1", "tq1", "bq0", "bq1"),
        ("y",),
    )

    def bundle_value(agent: int, bundle: tuple[str, ...]) -> int:
        return sum(values[agent][index[good]] for good in bundle)

    def tail(agent: int, bundle: tuple[str, ...]) -> int:
        return max(
            (bundle_value(agent, bundle[:offset] + bundle[offset + 1 :]) for offset in range(len(bundle))),
            default=0,
        )

    q_bundle = joint_suffix[2]
    r_bundle = joint_suffix[1]
    assert all(tail(agent, q_bundle) <= base[agent] for agent in (0, 1, 3))
    assert all(tail(agent, r_bundle) <= base[agent] for agent in (0, 2, 3))
    assert bundle_value(2, q_bundle) >= values[2][index["x"]]
    assert bundle_value(1, r_bundle) >= base[1]
    utilities = [bundle_value(agent, joint_suffix[agent]) for agent in range(4)]
    assert all(
        utilities[observer] >= tail(observer, joint_suffix[target])
        for observer in range(4)
        for target in range(4)
    )
    assert utilities[3] == base[3]
    assert utilities[1] >= base[1]
    assert utilities[0] > base[0]

    payload = {
        "schema": "length-three-early-r-dual-base-scalar-audit-v1",
        "status": "ALL_NEGATED_IMPLICATIONS_UNSAT",
        "checks": checks,
        "joint_suffix_split_profile": {
            "status": "DIRECT_EFX_ESCAPE_VERIFIED",
            "bundles": {
                agent: list(joint_suffix[offset])
                for offset, agent in enumerate(("p", "r", "q", "s"))
            },
            "utilities": utilities,
        },
        "claim_boundary": (
            "Checks only the four displayed additive implications in the "
            "early-r reduction. Desired-set extraction and PI routing remain "
            "analytic; the p/q cross-packet walls remain open."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
