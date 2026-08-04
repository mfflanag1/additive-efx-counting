#!/usr/bin/env python3
"""Exact CEGAR for the canonical 3+2+1+1 multi-bottom extremal cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster, _model_rows
    from .scan_charity_threshold_absorption import eligible, tables, theta
except ImportError:
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster, _model_rows
    from scan_charity_threshold_absorption import eligible, tables, theta


SCHEMA = "unique-defect-extremal-cell-cegar-v1"
N = 4
M = 8
BUNDLES = ((0, 1, 2), (3, 4), (5,), (6,))
MASKS = (7, 24, 32, 64)
HOST = 0
BAD = 1
FLOATER = 7
SELECTED_DESIRED = (0, 7)


def zmax(expressions):
    result = expressions[0]
    for expression in expressions[1:]:
        result = z3.If(result >= expression, result, expression)
    return result


def lex_gt(left, right):
    return z3.Or(
        *(
            z3.And(
                *(left[prefix] == right[prefix] for prefix in range(index)),
                left[index] > right[index],
            )
            for index in range(len(left))
        )
    )


class CellMaster:
    def __init__(self):
        self.master = ParkabilityLRAMaster(N, M)
        self.solver = self.master.solver
        self.values = self.master.values
        self.base_score = self.score(BUNDLES)
        self.base_utilities = tuple(
            self.sum(agent, BUNDLES[agent]) for agent in range(N)
        )
        self.add_cell()

    def sum(self, observer, goods):
        return z3.Sum(*(self.values[observer][good] for good in goods))

    def threshold(self, observer, goods):
        if not goods:
            return z3.RealVal(0)
        return zmax(
            [
                self.sum(observer, tuple(item for item in goods if item != removed))
                for removed in goods
            ]
        )

    def score(self, bundles):
        return z3.Sum(
            *(self.threshold(agent, bundles[agent]) for agent in range(N))
        )

    def state_eligible(self, bundles, charity):
        constraints = []
        for observer in range(N):
            own = self.sum(observer, bundles[observer])
            constraints.append(own >= self.sum(observer, charity))
            for target in range(N):
                for removed in bundles[target]:
                    constraints.append(
                        own
                        >= self.sum(
                            observer,
                            tuple(
                                good
                                for good in bundles[target]
                                if good != removed
                            ),
                        )
                    )
        return z3.And(*constraints)

    def add_cell(self):
        self.solver.add(self.state_eligible(BUNDLES, (FLOATER,)))
        augmented = list(BUNDLES)
        augmented[HOST] = BUNDLES[HOST] + (FLOATER,)
        for observer in range(N):
            own = self.sum(observer, augmented[observer])
            comparisons = [
                self.sum(
                    observer,
                    tuple(good for good in augmented[target] if good != removed),
                )
                for target in range(N)
                for removed in augmented[target]
            ]
            self.solver.add(
                z3.Or(*(own < comparison for comparison in comparisons))
                if observer == BAD
                else z3.And(*(own >= comparison for comparison in comparisons))
            )

        for observer in range(N):
            assigned_bad = self.sum(observer, BUNDLES[BAD])
            self.solver.add(
                z3.Or(
                    *(
                        assigned_bad
                        < self.sum(
                            observer,
                            tuple(
                                good
                                for good in augmented[target]
                                if good != removed
                            ),
                        )
                        for target in range(N)
                        for removed in augmented[target]
                    )
                )
            )

        self.solver.add(
            self.sum(BAD, BUNDLES[BAD]) >= self.sum(BAD, BUNDLES[HOST]),
            self.sum(BAD, SELECTED_DESIRED) > self.sum(BAD, BUNDLES[BAD]),
        )
        for observer in range(N):
            for removed in SELECTED_DESIRED:
                self.solver.add(
                    self.sum(observer, BUNDLES[observer])
                    >= self.sum(
                        observer,
                        tuple(
                            good
                            for good in SELECTED_DESIRED
                            if good != removed
                        ),
                    )
                )

        full_augmented = BUNDLES[HOST] + (FLOATER,)
        for discarded in BUNDLES[HOST]:
            target = tuple(good for good in full_augmented if good != discarded)
            strong_walls = [
                self.sum(observer, BUNDLES[observer])
                < self.sum(
                    observer,
                    tuple(good for good in target if good != removed),
                )
                for observer in range(N)
                for removed in target
            ]
            self.solver.add(
                z3.Or(
                    self.sum(BAD, target) <= self.sum(BAD, BUNDLES[BAD]),
                    *strong_walls,
                )
            )

        partitions = set()
        for destinations in itertools.product(range(N), repeat=len(BUNDLES[HOST])):
            redistributed = [
                list(bundle) if owner != HOST else []
                for owner, bundle in enumerate(BUNDLES)
            ]
            for good, owner in zip(BUNDLES[HOST], destinations):
                redistributed[owner].append(good)
            for insertion_host in range(N):
                complete = [list(bundle) for bundle in redistributed]
                complete[insertion_host].append(FLOATER)
                if all(complete):
                    partitions.add(
                        tuple(sorted(tuple(sorted(bundle)) for bundle in complete))
                    )
        for partition in sorted(partitions):
            self.master.add_partition_obstruction(
                partition, encoding="matching_clauses"
            )
        self.reachable_partition_count = len(partitions)

    def add_extremal_cut(self, masks, charity):
        bundles = tuple(
            tuple(good for good in range(M) if mask & (1 << good))
            for mask in masks
        )
        charity_goods = tuple(
            good for good in range(M) if charity & (1 << good)
        )
        candidate_score = self.score(bundles)
        candidate_utilities = tuple(
            self.sum(agent, bundles[agent]) for agent in range(N)
        )
        improves = z3.Or(
            candidate_score > self.base_score,
            z3.And(
                candidate_score == self.base_score,
                lex_gt(candidate_utilities, self.base_utilities),
            ),
        )
        self.solver.add(
            z3.Implies(improves, z3.Not(self.state_eligible(bundles, charity_goods)))
        )


def extremal_improvements(values, limit):
    totals, thresholds = tables(values)
    row_totals = tuple(sum(row) for row in values)
    base_theta = theta(MASKS, totals, thresholds, row_totals)
    base_utilities = tuple(totals[agent][MASKS[agent]] for agent in range(N))
    improvements = []
    for floater in range(M):
        allocated = tuple(good for good in range(M) if good != floater)
        for owners in itertools.product(range(N), repeat=len(allocated)):
            masks = [0] * N
            for good, owner in zip(allocated, owners):
                masks[owner] |= 1 << good
            masks = tuple(masks)
            if not all(masks) or not eligible(
                masks, 1 << floater, totals, thresholds
            ):
                continue
            candidate_theta = theta(masks, totals, thresholds, row_totals)
            utilities = tuple(
                totals[agent][masks[agent]] for agent in range(N)
            )
            if (candidate_theta, utilities) > (base_theta, base_utilities):
                improvements.append(
                    (candidate_theta, utilities, masks, 1 << floater)
                )
    improvements.sort(reverse=True)
    return improvements[:limit], len(improvements)


def load_pool(path):
    if not path.exists():
        return []
    document = json.loads(path.read_text())
    if document.get("schema") != SCHEMA:
        raise ValueError("pool schema mismatch")
    return [
        (tuple(record["masks"]), record["charity_mask"])
        for record in document["cuts"]
    ]


def save_pool(path, pool):
    atomic_json(
        path,
        {
            "schema": SCHEMA,
            "cuts": [
                {"masks": list(masks), "charity_mask": charity}
                for masks, charity in pool
            ],
        },
    )


def run(pool_path, result_path, smt2_path, iterations, batch, timeout_ms):
    started = time.time()
    cell = CellMaster()
    pool = load_pool(pool_path)
    seen = set(pool)
    for masks, charity in pool:
        cell.add_extremal_cut(masks, charity)

    status = "ITERATION_LIMIT"
    last_values = None
    last_improvement_count = None
    for iteration in range(1, iterations + 1):
        cell.solver.set(timeout=timeout_ms)
        verdict = cell.solver.check()
        if verdict == z3.unsat:
            status = "CELL_UNSAT"
            break
        if verdict == z3.unknown:
            status = "SOLVER_UNKNOWN"
            break
        last_values = _model_rows(cell.solver.model(), cell.values)
        improvements, last_improvement_count = extremal_improvements(
            last_values, batch
        )
        new = [
            (masks, charity)
            for _score, _utilities, masks, charity in improvements
            if (masks, charity) not in seen
        ]
        if not new:
            status = (
                "SELECTOR_COUNTEREXAMPLE"
                if last_improvement_count == 0
                else "DUPLICATE_CUT_STALL"
            )
            break
        for masks, charity in new:
            cell.add_extremal_cut(masks, charity)
            pool.append((masks, charity))
            seen.add((masks, charity))
        save_pool(pool_path, pool)
        print(
            f"iteration={iteration} pool={len(pool)} "
            f"improvements={last_improvement_count}",
            flush=True,
        )

    smt2_path.write_text(cell.solver.to_smt2())
    result = {
        "schema": SCHEMA,
        "status": status,
        "iterations_requested": iterations,
        "pool_size": len(pool),
        "pool_path": str(pool_path),
        "pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(),
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
        "reachable_host_redistribution_partitions": cell.reachable_partition_count,
        "last_improvement_count": last_improvement_count,
        "last_values": [list(row) for row in last_values] if last_values else None,
        "elapsed_seconds": round(time.time() - started, 6),
        "solver_reason_unknown": (
            cell.solver.reason_unknown() if status == "SOLVER_UNKNOWN" else None
        ),
        "claim_boundary": (
            "CELL_UNSAT proves only the canonical 3+2+1+1 selected-desired "
            "multi-bottom cell under the encoded host-redistribution alternative. "
            "Any other status is an exact resumable checkpoint, not a theorem."
        ),
    }
    atomic_json(result_path, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pool", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    parser.add_argument("--smt2", required=True, type=Path)
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--timeout-ms", type=int, default=300000)
    args = parser.parse_args()
    print(
        json.dumps(
            run(
                args.pool,
                args.result,
                args.smt2,
                args.iterations,
                args.batch,
                args.timeout_ms,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
