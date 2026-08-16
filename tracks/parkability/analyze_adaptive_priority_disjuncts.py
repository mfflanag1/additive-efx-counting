#!/usr/bin/env python3
"""Classify witness alternatives in an adaptive-priority inequality core."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )


SCHEMA = "adaptive-priority-disjunct-landscape-v1"
VALUE_ROW = re.compile(r"^value_(\d+)_\d+$")


def flattened_or(expression: z3.BoolRef) -> list[z3.BoolRef]:
    if not z3.is_or(expression):
        return [expression]
    result = []
    for child in expression.children():
        result.extend(flattened_or(child))
    return result


def row_support(expression: z3.ExprRef) -> list[int]:
    rows = set()
    stack = [expression]
    seen = set()
    while stack:
        item = stack.pop()
        identity = item.get_id()
        if identity in seen:
            continue
        seen.add(identity)
        if z3.is_const(item):
            match = VALUE_ROW.match(str(item.decl().name()))
            if match:
                rows.add(int(match.group(1)))
        stack.extend(item.children())
    return sorted(rows)


def run(
    *,
    seed_path: Path,
    compact_core_path: Path,
    inequality_core_path: Path,
    output_path: Path,
    time_limit_s: float,
) -> dict:
    if time_limit_s <= 0:
        raise ValueError("a positive time limit is required")
    seed = json.loads(seed_path.read_text())
    raw_values = seed.get("values", seed.get("candidate_values"))
    if raw_values is None:
        raise ValueError("seed JSON contains no values")
    values = core.validate_values(raw_values, lower=1)
    n = len(values)
    m = len(values[0])
    cells = derive_unique_seed_cells(values)
    compact_core = json.loads(compact_core_path.read_text())
    inequality_core = json.loads(inequality_core_path.read_text())
    if (
        compact_core.get("schema") != "adaptive-priority-rival-core-v1"
        or inequality_core.get("schema")
        != "adaptive-priority-inequality-core-v1"
        or inequality_core.get("status")
        != "UNSAT_DELETION_MINIMAL_INEQUALITY_CORE"
    ):
        raise ValueError("invalid adaptive-priority core input")

    symbolic_master = ParkabilityLRAMaster(n, m)
    source_records = assumption_records(symbolic_master, cells, compact_core)
    active = []
    for record in inequality_core["core"]:
        index = record["assumption_index"]
        source = source_records[index]
        if {
            key: value
            for key, value in record.items()
            if key != "assumption_index"
        } != public_record(source):
            raise ValueError("inequality-core semantic record mismatch")
        active.append((index, source))

    candidate_expressions = [
        record["expression"]
        for _, record in active
        if record["kind"] == "candidate_constraint"
    ]
    landscapes = []
    disjunction_specs = []
    total_checks = 0
    for assumption_index, record in active:
        expression = record["expression"]
        alternatives = flattened_or(expression)
        if len(alternatives) == 1:
            continue
        baseline = candidate_expressions
        if record["kind"] == "candidate_constraint":
            baseline = [
                other
                for other in candidate_expressions
                if not z3.eq(other, expression)
            ]
        probe = ParkabilityLRAMaster(n, m)
        probe.solver.add(*baseline)
        probe.solver.set(timeout=round(time_limit_s * 1000))
        alternative_records = []
        for alternative_index, alternative in enumerate(alternatives):
            probe.solver.push()
            probe.solver.add(alternative)
            verdict = probe.solver.check()
            total_checks += 1
            alternative_records.append(
                {
                    "alternative_index": alternative_index,
                    "row_support": row_support(alternative),
                    "status": str(verdict),
                    "reason_unknown": (
                        probe.solver.reason_unknown()
                        if verdict == z3.unknown
                        else None
                    ),
                }
            )
            probe.solver.pop()
        status_counts = Counter(
            item["status"] for item in alternative_records
        )
        landscapes.append(
            {
                "assumption_index": assumption_index,
                **public_record(record),
                "alternative_count": len(alternatives),
                "status_counts": dict(sorted(status_counts.items())),
                "feasible_row_supports": sorted(
                    {
                        tuple(item["row_support"])
                        for item in alternative_records
                        if item["status"] == "sat"
                    }
                ),
                "alternatives": alternative_records,
            }
        )
        disjunction_specs.append(
            {
                "assumption_index": assumption_index,
                "record": record,
                "expression": expression,
                "alternatives": alternatives,
            }
        )

    simple_candidate_expressions = [
        record["expression"]
        for _, record in active
        if record["kind"] == "candidate_constraint"
        and not z3.is_or(record["expression"])
    ]
    candidate_disjunction_expressions = [
        spec["expression"]
        for spec in disjunction_specs
        if spec["record"]["kind"] == "candidate_constraint"
    ]
    forced_alternatives = {}
    propagation = []
    contradiction = None
    round_index = 0
    while contradiction is None:
        round_index += 1
        changed = False
        for spec in disjunction_specs:
            assumption_index = spec["assumption_index"]
            if assumption_index in forced_alternatives:
                continue
            baseline = simple_candidate_expressions + [
                expression
                for expression in candidate_disjunction_expressions
                if (
                    spec["record"]["kind"] != "candidate_constraint"
                    or not z3.eq(expression, spec["expression"])
                )
            ] + list(forced_alternatives.values())
            probe = ParkabilityLRAMaster(n, m)
            probe.solver.add(*baseline)
            probe.solver.set(timeout=round(time_limit_s * 1000))
            feasible = []
            unknown = []
            for alternative_index, alternative in enumerate(
                spec["alternatives"]
            ):
                probe.solver.push()
                probe.solver.add(alternative)
                verdict = probe.solver.check()
                total_checks += 1
                if verdict == z3.sat:
                    feasible.append(alternative_index)
                elif verdict == z3.unknown:
                    unknown.append(alternative_index)
                probe.solver.pop()
            if unknown:
                continue
            if not feasible:
                contradiction = {
                    "round": round_index,
                    "assumption_index": assumption_index,
                    **public_record(spec["record"]),
                }
                break
            if len(feasible) == 1:
                alternative_index = feasible[0]
                alternative = spec["alternatives"][alternative_index]
                forced_alternatives[assumption_index] = alternative
                propagation.append(
                    {
                        "round": round_index,
                        "assumption_index": assumption_index,
                        **public_record(spec["record"]),
                        "forced_alternative_index": alternative_index,
                        "row_support": row_support(alternative),
                    }
                )
                changed = True
        if not changed:
            break

    result = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "each disjunct is tested against all active candidate premises "
            "except the disjunction being analyzed; this is local witness "
            "classification, not a covering theorem"
        ),
        "n": n,
        "m": m,
        "active_assumption_count": len(active),
        "active_candidate_constraint_count": len(candidate_expressions),
        "disjunction_count": len(landscapes),
        "solver_check_count": total_checks,
        "fully_forced_disjunction_count": sum(
            landscape["status_counts"].get("sat", 0) == 1
            for landscape in landscapes
        ),
        "unit_propagation": {
            "forced_disjunction_count": len(propagation),
            "round_count": round_index,
            "contradiction": contradiction,
            "forced": propagation,
        },
        "landscapes": landscapes,
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--compact-core", type=Path, required=True)
    parser.add_argument("--inequality-core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=30.0)
    args = parser.parse_args()
    run(
        seed_path=args.seed,
        compact_core_path=args.compact_core,
        inequality_core_path=args.inequality_core,
        output_path=args.output,
        time_limit_s=args.time_limit,
    )


if __name__ == "__main__":
    main()
