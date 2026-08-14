#!/usr/bin/env python3
"""Greedily deletion-minimize the 53-family allocated-E R2 UNSAT core."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import time
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_generalized_pi_named_selector_cegar import generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results" / "allocated_e_form0_pi_unsat_core.json"


def run(output: Path, timeout_seconds: int, random_seed: int, order_seed: int):
    source = json.loads(SOURCE.read_text())
    rows = source["core"]
    solver, value = build_master(0)
    labels = []
    for position, row in enumerate(rows):
        label = z3.Bool(f"candidate_family_{position}")
        solver.add(z3.Implies(label, generalized_pi_cut(value, row["witness"])))
        labels.append(label)
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    active = list(range(len(rows)))
    checks = []
    changed = True
    pass_index = 0
    while changed:
        changed = False
        order = list(active)
        random.Random(order_seed + pass_index).shuffle(order)
        for position in order:
            trial = [labels[index] for index in active if index != position]
            started = time.monotonic()
            status = solver.check(*trial)
            record = {
                "pass": pass_index,
                "position": position,
                "original_index": rows[position]["index"],
                "active_before": len(active),
                "status_without": str(status),
                "elapsed_seconds": time.monotonic() - started,
            }
            if status == z3.unsat:
                active.remove(position)
                record["removed"] = True
                changed = True
            else:
                record["removed"] = False
                if status == z3.unknown:
                    record["reason_unknown"] = solver.reason_unknown()
            checks.append(record)
            print(
                pass_index, position, rows[position]["index"], status,
                "active", len(active), flush=True,
            )
        pass_index += 1

    final_status = solver.check(*(labels[index] for index in active))
    result = {
        "schema": "allocated-e-form0-pi-greedy-minimal-core-v1",
        "status": str(final_status),
        "solver": f"Z3 {z3.get_version_string()}",
        "random_seed": random_seed,
        "order_seed": order_seed,
        "timeout_seconds_per_check": timeout_seconds,
        "source": "results/allocated_e_form0_pi_unsat_core.json",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "starting_count": len(rows),
        "core_count": len(active),
        "passes": pass_index,
        "checks": checks,
        "core": [rows[index] for index in active],
        "claim_boundary": (
            "Greedy deletion-minimal family core for the bounded allocated-E "
            "R2 master. It is not guaranteed minimum-cardinality and does not "
            "by itself prove a cap-free theorem."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--random-seed", type=int, default=8423)
    parser.add_argument("--order-seed", type=int, default=0)
    args = parser.parse_args()
    result = run(args.output, args.timeout_seconds, args.random_seed, args.order_seed)
    print(json.dumps({
        "status": result["status"],
        "starting_count": result["starting_count"],
        "core_count": result["core_count"],
        "passes": result["passes"],
    }, indent=2))


if __name__ == "__main__":
    main()
