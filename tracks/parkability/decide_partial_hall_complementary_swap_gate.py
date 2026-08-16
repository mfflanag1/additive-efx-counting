#!/usr/bin/env python3
"""Decide a complementary-swap plus short-repair Hall conversion gate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .decide_partial_hall_radius_one import integerize
    from .partial_hall_factored_master import build_factored_master
    from .run_partial_hall_utilitarian_local_cegar import add_local_rivals
except ImportError:
    from anneal import atomic_json
    from decide_partial_hall_radius_one import integerize
    from partial_hall_factored_master import build_factored_master
    from run_partial_hall_utilitarian_local_cegar import add_local_rivals


RIVALS8 = (
    {"floater": 8, "masks": (129, 14, 80, 32)},
    {"floater": 8, "masks": (80, 14, 129, 32)},
    {"floater": 8, "masks": (65, 14, 144, 32)},
    {"floater": 6, "masks": (272, 14, 129, 32)},
    {"floater": 1, "masks": (81, 264, 132, 32)},
    {"floater": 4, "masks": (320, 14, 129, 32)},
    {"floater": 7, "masks": (257, 14, 80, 32)},
    {"floater": 8, "masks": (144, 14, 65, 32)},
)
RIVALS = RIVALS8 + (
    {"floater": 1, "masks": (96, 136, 17, 260)},
)


def run(output: Path, smt2_output: Path, timeout_seconds: int) -> dict:
    solver, values, base, _, partitions, _ = build_factored_master(
        timeout_seconds * 1000, hall_encoding="witness"
    )
    sum_gain = (
        values[0][0]
        + values[0][4]
        - values[0][6]
        - values[0][7]
        + values[2][6]
        + values[2][7]
        - values[2][0]
        - values[2][4]
    )
    solver.add(sum_gain > 0)
    learned = set()
    add_local_rivals(
        solver,
        values,
        base,
        learned,
        RIVALS,
        symmetry_close=False,
    )
    verdict = solver.check()
    model_values = integerize(solver.model(), values) if verdict == z3.sat else None
    smt2_output.write_text(solver.to_smt2())
    artifact = {
        "schema": "partial-hall-complementary-swap-gate-v3",
        "status": (
            "UNSAT_PROVED" if verdict == z3.unsat else
            "SAT_COUNTEREXAMPLE" if verdict == z3.sat else "UNKNOWN"
        ),
        "meaning": (
            "UNSAT proves that a canonical Hall obstruction with positive "
            "complementary-swap sum has an eligible normalized-utilitarian "
            "improvement among the two swaps and seven stored-corpus repairs. "
            "SAT refutes only this nine-rival conversion; UNKNOWN is inconclusive."
        ),
        "positive_sum_condition": (
            "v_0_0+v_0_4-v_0_6-v_0_7+v_2_6+v_2_7-v_2_0-v_2_4>0"
        ),
        "rivals": [
            {"floater": rival["floater"], "masks": list(rival["masks"])}
            for rival in RIVALS
        ],
        "asserted_rival_count": len(learned),
        "candidate_partition_count": len(partitions),
        "solver_verdict": str(verdict),
        "solver_reason_unknown": solver.reason_unknown() if verdict == z3.unknown else None,
        "timeout_seconds": timeout_seconds,
        "values": model_values,
        "smt2_output": str(smt2_output),
        "smt2_sha256": hashlib.sha256(smt2_output.read_bytes()).hexdigest(),
    }
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--smt2-output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    print(json.dumps(run(args.output, args.smt2_output, args.timeout_seconds), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
