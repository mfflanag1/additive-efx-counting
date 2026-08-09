#!/usr/bin/env python3
"""Decide the two-base-safe-bundle gate in one alternating packet cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from .run_alternating_singleton_return_cegar import (
        ORDER,
        dominates,
        integerize,
        singleton_return_candidates,
    )
    from .run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
        subset_sum,
    )
except ImportError:
    from run_alternating_singleton_return_cegar import (
        ORDER,
        dominates,
        integerize,
        singleton_return_candidates,
    )
    from run_alternating_variable_packet_rooted_cegar import (
        AGENTS,
        desired_expression,
        make_cell,
        numeric_efx,
        numeric_utilities,
        structural_solver,
        subset_sum,
    )


SCHEMA = "alternating-two-safe-bundle-gate-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def powerset(goods):
    for size in range(len(goods) + 1):
        yield from itertools.combinations(goods, size)


def desired_bundles(cell):
    residual = tuple(
        good for good in range(cell["m"]) if good not in (cell["x"], cell["y"])
    )
    for size in range(1, len(residual) + 1):
        yield from itertools.combinations(residual, size)


def safe_expression(values, own, candidate):
    return z3.And(
        *(
            own[observer]
            >= subset_sum(
                values,
                observer,
                tuple(good for good in candidate if good != removed),
            )
            for observer in range(4)
            for removed in candidate
        )
    )


def pair_expression(values, own, source, desired_bundle, q_bundle):
    return z3.And(
        desired_expression(values, own, source, desired_bundle),
        safe_expression(values, own, q_bundle),
        *(
            subset_sum(values, 3, q_bundle)
            >= subset_sum(
                values,
                3,
                tuple(good for good in desired_bundle if good != removed),
            )
            for removed in desired_bundle
        ),
    )


def numeric_safe(values, own, candidate) -> bool:
    return all(
        own[observer]
        >= sum(values[observer][good] for good in candidate if good != removed)
        for observer in range(4)
        for removed in candidate
    )


def numeric_desired(values, own, source, candidate) -> bool:
    return (
        sum(values[source][good] for good in candidate) > own[source]
        and numeric_safe(values, own, candidate)
    )


def numeric_pair_count(values, cell, bundles) -> int:
    own = numeric_utilities(values, cell["base_owner"])
    count = 0
    for source in (2, 1):
        for desired_bundle in bundles:
            if not numeric_desired(values, own, source, desired_bundle):
                continue
            complement = tuple(
                good
                for good in range(cell["m"])
                if good not in (cell["x"], cell["y"])
                and good not in desired_bundle
            )
            threshold = max(
                sum(values[3][good] for good in desired_bundle if good != removed)
                for removed in desired_bundle
            )
            for q_bundle in powerset(complement):
                if not numeric_safe(values, own, q_bundle):
                    continue
                if sum(values[3][good] for good in q_bundle) >= threshold:
                    count += 1
    return count


def decide(sizes, timeout_seconds: float) -> dict:
    cell = make_cell(sizes)
    bundles = tuple(desired_bundles(cell))
    solver, values, own = structural_solver(cell)
    candidate_count = 0
    for source in (2, 1):
        for desired_bundle in bundles:
            complement = tuple(
                good
                for good in range(cell["m"])
                if good not in (cell["x"], cell["y"])
                and good not in desired_bundle
            )
            for q_bundle in powerset(complement):
                if not q_bundle and len(desired_bundle) > 1:
                    continue
                solver.add(
                    z3.Not(
                        pair_expression(
                            values, own, source, desired_bundle, q_bundle
                        )
                    )
                )
                candidate_count += 1
    solver.set(timeout=max(1, int(timeout_seconds * 1000)))
    status = solver.check()
    result = {
        "schema": SCHEMA,
        "packet_sizes": list(sizes),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "desired_bundle_count_per_source": len(bundles),
        "symbolic_pair_count": candidate_count,
        "solver_status": str(status),
        "claim_boundary": {
            "unsat": "the two-base-safe-bundle gate holds in this exact packet cell",
            "sat": "only the two-base-safe-bundle gate is refuted; the broader singleton-return and external-observer lemmas require separate checks",
            "unknown": "no mathematical decision",
        },
    }
    if status == z3.sat:
        integers = integerize(solver.model(), values)
        pair_count = numeric_pair_count(integers, cell, bundles)
        if pair_count:
            raise AssertionError("SAT model still has a two-safe-bundle pair")
        singleton_escapes = sum(
            numeric_efx(integers, allocation)
            and dominates(integers, cell, allocation)
            for allocation in singleton_return_candidates(cell)
        )
        result.update(
            {
                "status": "TWO_SAFE_BUNDLE_GATE_REFUTED",
                "values": [list(row) for row in integers],
                "two_safe_bundle_pair_count": pair_count,
                "singleton_return_escape_count": singleton_escapes,
            }
        )
    elif status == z3.unsat:
        result["status"] = "UNSAT_TWO_SAFE_BUNDLE_GATE"
    else:
        result["status"] = "UNKNOWN"
        result["reason_unknown"] = solver.reason_unknown()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", default="2,2,2,2")
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sizes = tuple(int(part) for part in args.sizes.split(","))
    if len(sizes) != 4 or any(size < 1 for size in sizes):
        raise ValueError("--sizes must contain four positive integers")
    result = decide(sizes, args.timeout_seconds)
    script = Path(__file__).resolve()
    result["provenance"] = {
        "script": str(script.relative_to(script.parents[2])),
        "script_sha256": sha256(script),
        "z3_version": z3.get_version_string(),
    }
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
