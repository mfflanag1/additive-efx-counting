#!/usr/bin/env python3
"""Extract a finite witness-choice core from an adaptive-priority LRA core."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .analyze_adaptive_priority_disjuncts import (
        flattened_or,
        row_support,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from analyze_adaptive_priority_disjuncts import flattened_or, row_support
    from lra_master import ParkabilityLRAMaster
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )


SCHEMA = "adaptive-priority-witness-hall-core-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(
    *,
    seed_path: Path,
    compact_core_path: Path,
    inequality_core_path: Path,
    output_path: Path,
    time_limit_s: float,
    max_iterations: int,
) -> dict:
    if time_limit_s <= 0 or max_iterations < 1:
        raise ValueError("positive time and iteration limits are required")
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
    active_records = []
    for record in inequality_core["core"]:
        assumption_index = record["assumption_index"]
        source = source_records[assumption_index]
        if {
            key: value
            for key, value in record.items()
            if key != "assumption_index"
        } != public_record(source):
            raise ValueError("inequality-core semantic record mismatch")
        active_records.append((assumption_index, source))

    simple_expressions = [
        record["expression"]
        for _, record in active_records
        if not z3.is_or(record["expression"])
    ]
    raw_clauses = [
        {
            "assumption_index": assumption_index,
            "record": record,
            "alternatives": flattened_or(record["expression"]),
        }
        for assumption_index, record in active_records
        if z3.is_or(record["expression"])
    ]

    theory = ParkabilityLRAMaster(n, m)
    theory.solver.add(*simple_expressions)
    theory.solver.set(timeout=round(time_limit_s * 1000))
    clauses = []
    individual_checks = 0
    for clause_index, raw_clause in enumerate(raw_clauses):
        feasible = []
        for raw_alternative_index, alternative in enumerate(
            raw_clause["alternatives"]
        ):
            theory.solver.push()
            theory.solver.add(alternative)
            verdict = theory.solver.check()
            individual_checks += 1
            theory.solver.pop()
            if verdict == z3.unknown:
                raise RuntimeError(
                    "individual witness check is unknown: "
                    f"{theory.solver.reason_unknown()}"
                )
            if verdict == z3.sat:
                feasible.append(
                    {
                        "raw_alternative_index": raw_alternative_index,
                        "expression": alternative,
                        "row_support": row_support(alternative),
                    }
                )
        if not feasible:
            raise AssertionError(
                f"clause {clause_index} has no individually feasible witness"
            )
        clauses.append(
            {
                "assumption_index": raw_clause["assumption_index"],
                "record": raw_clause["record"],
                "raw_alternative_count": len(raw_clause["alternatives"]),
                "alternatives": feasible,
            }
        )

    choice_solver = z3.Solver()
    choice_variables = []
    theory_selectors = []
    selector_identity = {}
    for clause_index, clause in enumerate(clauses):
        clause_choices = []
        clause_selectors = []
        for alternative_index, alternative in enumerate(
            clause["alternatives"]
        ):
            choice = z3.Bool(
                f"choose_clause_{clause_index}_alternative_{alternative_index}"
            )
            selector = z3.Bool(
                f"theory_clause_{clause_index}_alternative_{alternative_index}"
            )
            choice_solver.add(choice == selector)
            theory.solver.add(
                z3.Implies(selector, alternative["expression"])
            )
            clause_choices.append(choice)
            clause_selectors.append(selector)
            selector_identity[selector.decl().name()] = (
                clause_index,
                alternative_index,
            )
        choice_solver.add(z3.PbEq([(choice, 1) for choice in clause_choices], 1))
        choice_variables.append(clause_choices)
        theory_selectors.append(clause_selectors)

    conflicts = []
    theory_checks = 0
    started = time.time()
    status = "ITERATION_LIMIT"
    for iteration in range(1, max_iterations + 1):
        choice_verdict = choice_solver.check()
        if choice_verdict == z3.unsat:
            status = "BOOLEAN_COVER_UNSAT"
            break
        if choice_verdict != z3.sat:
            raise RuntimeError(f"choice solver is {choice_verdict}")
        model = choice_solver.model()
        selected = [
            theory_selectors[clause_index][alternative_index]
            for clause_index, alternatives in enumerate(choice_variables)
            for alternative_index, choice in enumerate(alternatives)
            if z3.is_true(model.eval(choice, model_completion=True))
        ]
        if len(selected) != len(clauses):
            raise AssertionError("choice model did not select one witness per clause")
        theory_verdict = theory.solver.check(*selected)
        theory_checks += 1
        if theory_verdict == z3.sat:
            raise AssertionError(
                "witness-choice abstraction found a model of the UNSAT core"
            )
        if theory_verdict != z3.unsat:
            raise RuntimeError(
                f"theory check is {theory_verdict}: "
                f"{theory.solver.reason_unknown()}"
            )
        by_name = {
            selector.decl().name(): selector for selector in selected
        }
        conflict = [
            by_name[item.decl().name()]
            for item in theory.solver.unsat_core()
        ]
        for selector in conflict[:]:
            trial = [item for item in conflict if not z3.eq(item, selector)]
            verdict = theory.solver.check(*trial)
            theory_checks += 1
            if verdict == z3.unsat:
                conflict = trial
            elif verdict != z3.sat:
                raise RuntimeError(
                    f"theory conflict shrink is {verdict}: "
                    f"{theory.solver.reason_unknown()}"
                )
        identities = sorted(
            selector_identity[selector.decl().name()]
            for selector in conflict
        )
        choice_solver.add(
            z3.Or(
                *(
                    z3.Not(choice_variables[clause][alternative])
                    for clause, alternative in identities
                )
            )
        )
        conflicts.append(identities)

    if status != "BOOLEAN_COVER_UNSAT":
        result = {
            "schema": SCHEMA,
            "status": status,
            "meaning": (
                "bounded witness-choice extraction did not close; this is "
                "not a theorem or counterexample"
            ),
            "n": n,
            "m": m,
            "seed_sha256": sha256(seed_path),
            "compact_core_sha256": sha256(compact_core_path),
            "inequality_core_sha256": sha256(inequality_core_path),
            "clause_count": len(clauses),
            "individual_witness_check_count": individual_checks,
            "theory_check_count": theory_checks,
            "learned_conflict_count": len(conflicts),
            "max_iterations": max_iterations,
            "elapsed_seconds": time.time() - started,
        }
        atomic_json(output_path, result)
        print(json.dumps(result, indent=2, sort_keys=True), flush=True)
        return result

    conflict_solver = z3.Solver()
    for alternatives in choice_variables:
        conflict_solver.add(
            z3.PbEq([(choice, 1) for choice in alternatives], 1)
        )
    conflict_activations = []
    for conflict_index, conflict in enumerate(conflicts):
        activation = z3.Bool(f"active_conflict_{conflict_index}")
        conflict_activations.append(activation)
        conflict_solver.add(
            z3.Implies(
                activation,
                z3.Or(
                    *(
                        z3.Not(choice_variables[clause][alternative])
                        for clause, alternative in conflict
                    )
                ),
            )
        )
    if conflict_solver.check(*conflict_activations) != z3.unsat:
        raise AssertionError("learned conflicts do not close the choice system")
    activation_by_name = {
        item.decl().name(): index
        for index, item in enumerate(conflict_activations)
    }
    active_conflicts = [
        activation_by_name[item.decl().name()]
        for item in conflict_solver.unsat_core()
    ]
    boolean_checks = 1
    for conflict_index in active_conflicts[:]:
        trial = [
            index for index in active_conflicts if index != conflict_index
        ]
        verdict = conflict_solver.check(
            *(conflict_activations[index] for index in trial)
        )
        boolean_checks += 1
        if verdict == z3.unsat:
            active_conflicts = trial
        elif verdict != z3.sat:
            raise RuntimeError(f"Boolean conflict shrink is {verdict}")

    public_clauses = []
    for clause_index, clause in enumerate(clauses):
        public_clauses.append(
            {
                "clause_index": clause_index,
                "assumption_index": clause["assumption_index"],
                **public_record(clause["record"]),
                "raw_alternative_count": clause["raw_alternative_count"],
                "feasible_alternatives": [
                    {
                        "alternative_index": alternative_index,
                        "raw_alternative_index": alternative[
                            "raw_alternative_index"
                        ],
                        "row_support": alternative["row_support"],
                    }
                    for alternative_index, alternative in enumerate(
                        clause["alternatives"]
                    )
                ],
            }
        )
    public_conflicts = [
        {
            "conflict_index": conflict_index,
            "choice_count": len(conflicts[conflict_index]),
            "choices": [
                {
                    "clause_index": clause,
                    "alternative_index": alternative,
                    "raw_alternative_index": clauses[clause][
                        "alternatives"
                    ][alternative]["raw_alternative_index"],
                    "row_support": clauses[clause]["alternatives"][
                        alternative
                    ]["row_support"],
                }
                for clause, alternative in conflicts[conflict_index]
            ],
        }
        for conflict_index in active_conflicts
    ]
    result = {
        "schema": SCHEMA,
        "status": "UNSAT_DELETION_MINIMAL_CONFLICT_COVER",
        "meaning": (
            "a deletion-minimal finite family of exact LRA conflicts rules "
            "out every choice of one witness per disjunction in one fixed "
            "4x9 cell; this is a Hall-style local certificate, not a "
            "general adaptive-priority theorem"
        ),
        "n": n,
        "m": m,
        "seed_sha256": sha256(seed_path),
        "compact_core_sha256": sha256(compact_core_path),
        "inequality_core_sha256": sha256(inequality_core_path),
        "simple_inequality_count": len(simple_expressions),
        "clause_count": len(clauses),
        "feasible_alternative_count": sum(
            len(clause["alternatives"]) for clause in clauses
        ),
        "individual_witness_check_count": individual_checks,
        "theory_check_count": theory_checks,
        "learned_conflict_count": len(conflicts),
        "deletion_minimal_conflict_count": len(active_conflicts),
        "boolean_shrink_check_count": boolean_checks,
        "elapsed_seconds": time.time() - started,
        "clauses": public_clauses,
        "conflicts": public_conflicts,
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
    parser.add_argument("--max-iterations", type=int, default=10_000)
    args = parser.parse_args()
    run(
        seed_path=args.seed,
        compact_core_path=args.compact_core,
        inequality_core_path=args.inequality_core,
        output_path=args.output,
        time_limit_s=args.time_limit,
        max_iterations=args.max_iterations,
    )


if __name__ == "__main__":
    main()
