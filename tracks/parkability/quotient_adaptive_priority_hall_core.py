#!/usr/bin/env python3
"""Quotient row-local Hall conflicts into exact inequality templates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from fractions import Fraction
from functools import reduce
from pathlib import Path

import networkx as nx
import z3

try:
    from . import core
    from .anneal import atomic_json
    from .analyze_adaptive_priority_disjuncts import flattened_or
    from .lra_master import ParkabilityLRAMaster
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from analyze_adaptive_priority_disjuncts import flattened_or
    from lra_master import ParkabilityLRAMaster
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )


SCHEMA = "adaptive-priority-hall-template-quotient-v1"
VALUE_NAME = re.compile(r"^value_(\d+)_(\d+)$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_linear(
    left: tuple[dict[str, Fraction], Fraction],
    right: tuple[dict[str, Fraction], Fraction],
    scale: Fraction = Fraction(1),
) -> tuple[dict[str, Fraction], Fraction]:
    coefficients = dict(left[0])
    for variable, coefficient in right[0].items():
        coefficients[variable] = coefficients.get(variable, Fraction()) + (
            scale * coefficient
        )
        if not coefficients[variable]:
            del coefficients[variable]
    return coefficients, left[1] + scale * right[1]


def linearize(expression: z3.ArithRef) -> tuple[dict[str, Fraction], Fraction]:
    if z3.is_rational_value(expression):
        return {}, Fraction(
            expression.numerator_as_long(),
            expression.denominator_as_long(),
        )
    if z3.is_const(expression) and expression.num_args() == 0:
        return {expression.decl().name(): Fraction(1)}, Fraction()
    kind = expression.decl().kind()
    children = expression.children()
    if kind == z3.Z3_OP_ADD:
        result = ({}, Fraction())
        for child in children:
            result = add_linear(result, linearize(child))
        return result
    if kind == z3.Z3_OP_SUB:
        result = linearize(children[0])
        for child in children[1:]:
            result = add_linear(result, linearize(child), Fraction(-1))
        return result
    if kind == z3.Z3_OP_UMINUS:
        return add_linear(({}, Fraction()), linearize(children[0]), Fraction(-1))
    if kind == z3.Z3_OP_MUL:
        rational_children = [child for child in children if z3.is_rational_value(child)]
        nonrational_children = [
            child for child in children if not z3.is_rational_value(child)
        ]
        if len(nonrational_children) != 1:
            raise ValueError(f"nonlinear arithmetic term: {expression}")
        scale = reduce(
            lambda left, right: left * right,
            (
                Fraction(child.numerator_as_long(), child.denominator_as_long())
                for child in rational_children
            ),
            Fraction(1),
        )
        return add_linear(
            ({}, Fraction()),
            linearize(nonrational_children[0]),
            scale,
        )
    if kind == z3.Z3_OP_TO_REAL:
        return linearize(children[0])
    raise ValueError(f"unsupported arithmetic term: {expression}")


def normalized_atom(atom: z3.BoolRef) -> dict:
    kind = atom.decl().kind()
    if kind not in {
        z3.Z3_OP_LT,
        z3.Z3_OP_LE,
        z3.Z3_OP_GT,
        z3.Z3_OP_GE,
        z3.Z3_OP_EQ,
    } or atom.num_args() != 2:
        raise ValueError(f"unsupported Boolean atom: {atom}")
    left = linearize(atom.arg(0))
    right = linearize(atom.arg(1))
    relation = {
        z3.Z3_OP_LT: "strict",
        z3.Z3_OP_GT: "strict",
        z3.Z3_OP_LE: "weak",
        z3.Z3_OP_GE: "weak",
        z3.Z3_OP_EQ: "equality",
    }[kind]
    difference = (
        add_linear(left, right, Fraction(-1))
        if kind in {z3.Z3_OP_LT, z3.Z3_OP_LE, z3.Z3_OP_EQ}
        else add_linear(right, left, Fraction(-1))
    )
    denominators = [
        value.denominator
        for value in [*difference[0].values(), difference[1]]
    ]
    multiplier = math.lcm(*denominators) if denominators else 1
    integer_coefficients = {
        variable: int(coefficient * multiplier)
        for variable, coefficient in difference[0].items()
    }
    integer_constant = int(difference[1] * multiplier)
    divisor = reduce(
        math.gcd,
        [abs(value) for value in [*integer_coefficients.values(), integer_constant]],
        0,
    ) or 1
    integer_coefficients = {
        variable: coefficient // divisor
        for variable, coefficient in integer_coefficients.items()
    }
    integer_constant //= divisor
    if relation == "equality":
        oriented = [
            integer_coefficients[variable]
            for variable in sorted(integer_coefficients)
        ] + [integer_constant]
        first_nonzero = next((value for value in oriented if value), 1)
        if first_nonzero < 0:
            integer_coefficients = {
                variable: -coefficient
                for variable, coefficient in integer_coefficients.items()
            }
            integer_constant = -integer_constant
    return {
        "relation": relation,
        "coefficients": integer_coefficients,
        "constant": integer_constant,
    }


def flattened_and(expression: z3.BoolRef) -> list[z3.BoolRef]:
    if not z3.is_and(expression):
        return [expression]
    result = []
    for child in expression.children():
        result.extend(flattened_and(child))
    return result


def premise_color(metadata: dict) -> str:
    if metadata["source"] == "base":
        return f"base:{metadata['record']['constraint_kind']}"
    record = metadata["record"]
    return (
        f"choice:{record.get('constraint_kind')}"
        if record["kind"] == "candidate_constraint"
        else "choice:rival_blocker"
    )


def build_template_graph(premises: list[dict]) -> tuple[nx.Graph, dict] | None:
    parsed = []
    supported_rows = set()
    for premise_index, premise in enumerate(premises):
        atoms = []
        for atom in flattened_and(premise["expression"]):
            normalized = normalized_atom(atom)
            variable_records = []
            for variable, coefficient in normalized["coefficients"].items():
                match = VALUE_NAME.match(variable)
                if match is None:
                    raise ValueError(f"unexpected variable name: {variable}")
                row = int(match.group(1))
                good = int(match.group(2))
                supported_rows.add(row)
                variable_records.append((row, good, coefficient))
            atoms.append(
                {
                    "relation": normalized["relation"],
                    "constant": normalized["constant"],
                    "variables": variable_records,
                }
            )
        parsed.append(
            {
                "premise_index": premise_index,
                "color": premise_color(premise),
                "atoms": atoms,
            }
        )
    if len(supported_rows) != 1:
        return None

    graph = nx.Graph()
    goods = set()
    atom_shapes = []
    for premise in parsed:
        premise_node = f"premise_{premise['premise_index']}"
        graph.add_node(premise_node, color=f"premise:{premise['color']}")
        for atom_index, atom in enumerate(premise["atoms"]):
            atom_node = f"atom_{premise['premise_index']}_{atom_index}"
            graph.add_node(
                atom_node,
                color=(
                    f"atom:{atom['relation']}:constant={atom['constant']}"
                ),
            )
            graph.add_edge(premise_node, atom_node, coefficient="contains")
            positive = 0
            negative = 0
            for _, good, coefficient in atom["variables"]:
                goods.add(good)
                if coefficient > 0:
                    positive += coefficient
                else:
                    negative -= coefficient
                graph.add_edge(
                    atom_node,
                    f"good_{good}",
                    coefficient=str(coefficient),
                )
            atom_shapes.append(
                {
                    "premise_color": premise["color"],
                    "relation": atom["relation"],
                    "positive_mass": positive,
                    "negative_mass": negative,
                    "constant": atom["constant"],
                }
            )
    for good in goods:
        graph.add_node(f"good_{good}", color="good")
    return graph, {
        "premise_count": len(premises),
        "atom_count": sum(len(premise["atoms"]) for premise in parsed),
        "good_count": len(goods),
        "atom_shapes": sorted(
            atom_shapes,
            key=lambda record: tuple(record.values()),
        ),
    }


def run(
    *,
    seed_path: Path,
    compact_core_path: Path,
    inequality_core_path: Path,
    hall_core_path: Path,
    output_path: Path,
    time_limit_s: float,
) -> dict:
    if time_limit_s <= 0:
        raise ValueError("a positive time limit is required")
    seed = json.loads(seed_path.read_text())
    raw_values = seed.get("values", seed.get("candidate_values"))
    values = core.validate_values(raw_values, lower=1)
    n = len(values)
    m = len(values[0])
    cells = derive_unique_seed_cells(values)
    compact_core = json.loads(compact_core_path.read_text())
    inequality_core = json.loads(inequality_core_path.read_text())
    hall_core = json.loads(hall_core_path.read_text())
    if (
        hall_core.get("schema") != "adaptive-priority-witness-hall-core-v1"
        or hall_core.get("status")
        != "UNSAT_DELETION_MINIMAL_CONFLICT_COVER"
        or hall_core.get("seed_sha256") != sha256(seed_path)
        or hall_core.get("compact_core_sha256") != sha256(compact_core_path)
        or hall_core.get("inequality_core_sha256")
        != sha256(inequality_core_path)
    ):
        raise ValueError("Hall-core metadata mismatch")

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
    base_records = [
        {
            "assumption_index": assumption_index,
            "record": public_record(record),
            "expression": record["expression"],
        }
        for assumption_index, record in active_records
        if not z3.is_or(record["expression"])
    ]
    raw_clauses = [
        {
            "assumption_index": assumption_index,
            "record": public_record(record),
            "alternatives": flattened_or(record["expression"]),
        }
        for assumption_index, record in active_records
        if z3.is_or(record["expression"])
    ]
    if len(raw_clauses) != len(hall_core["clauses"]):
        raise ValueError("Hall clause census mismatch")
    choice_records = {}
    for clause in hall_core["clauses"]:
        clause_index = clause["clause_index"]
        raw_clause = raw_clauses[clause_index]
        if (
            clause["assumption_index"] != raw_clause["assumption_index"]
            or {
                key: value
                for key, value in clause.items()
                if key
                not in {
                    "clause_index",
                    "assumption_index",
                    "raw_alternative_count",
                    "feasible_alternatives",
                }
            }
            != raw_clause["record"]
        ):
            raise ValueError("Hall clause identity mismatch")
        for alternative in clause["feasible_alternatives"]:
            choice_records[
                (clause_index, alternative["alternative_index"])
            ] = {
                "record": raw_clause["record"],
                "expression": raw_clause["alternatives"][
                    alternative["raw_alternative_index"]
                ],
            }

    solver = ParkabilityLRAMaster(n, m)
    solver.solver.set(timeout=round(time_limit_s * 1000))
    selector_records = {}
    base_selectors = []
    for base_index, base in enumerate(base_records):
        selector = z3.Bool(f"template_base_{base_index}")
        solver.solver.add(z3.Implies(selector, base["expression"]))
        selector_records[selector.decl().name()] = {
            "source": "base",
            **base,
        }
        base_selectors.append(selector)
    choice_selectors = {}
    for identity, choice in choice_records.items():
        selector = z3.Bool(f"template_choice_{identity[0]}_{identity[1]}")
        solver.solver.add(z3.Implies(selector, choice["expression"]))
        selector_records[selector.decl().name()] = {
            "source": "choice",
            "clause_index": identity[0],
            "alternative_index": identity[1],
            **choice,
        }
        choice_selectors[identity] = selector

    node_match = nx.algorithms.isomorphism.categorical_node_match("color", "")
    edge_match = nx.algorithms.isomorphism.categorical_edge_match(
        "coefficient", ""
    )
    template_buckets = defaultdict(list)
    template_records = []
    conflict_template_map = []
    premise_count_distribution = Counter()
    mixed_distribution = Counter()
    solver_checks = 0
    started = time.time()
    for position, conflict in enumerate(hall_core["conflicts"], start=1):
        selected_choices = [
            choice_selectors[
                (choice["clause_index"], choice["alternative_index"])
            ]
            for choice in conflict["choices"]
        ]
        active = base_selectors + selected_choices
        verdict = solver.solver.check(*active)
        solver_checks += 1
        if verdict != z3.unsat:
            raise AssertionError(f"Hall conflict is {verdict}")
        by_name = {selector.decl().name(): selector for selector in active}
        minimal = [
            by_name[item.decl().name()]
            for item in solver.solver.unsat_core()
        ]
        for selector in minimal[:]:
            trial = [item for item in minimal if not z3.eq(item, selector)]
            verdict = solver.solver.check(*trial)
            solver_checks += 1
            if verdict == z3.unsat:
                minimal = trial
            elif verdict != z3.sat:
                raise RuntimeError(
                    f"premise shrink is {verdict}: "
                    f"{solver.solver.reason_unknown()}"
                )
        premises = [
            selector_records[selector.decl().name()] for selector in minimal
        ]
        choice_premise_count = sum(
            premise["source"] == "choice" for premise in premises
        )
        if choice_premise_count != len(selected_choices):
            raise AssertionError("Hall conflict was not choice-minimal")
        built = build_template_graph(premises)
        if built is None:
            mixed_distribution[len(premises)] += 1
            conflict_template_map.append(
                {
                    "conflict_index": conflict["conflict_index"],
                    "template_id": None,
                    "minimal_premise_count": len(premises),
                }
            )
        else:
            graph, summary = built
            graph_hash = nx.weisfeiler_lehman_graph_hash(
                graph,
                node_attr="color",
                edge_attr="coefficient",
            )
            template_id = None
            for candidate_id in template_buckets[graph_hash]:
                if nx.is_isomorphic(
                    graph,
                    template_records[candidate_id]["graph"],
                    node_match=node_match,
                    edge_match=edge_match,
                ):
                    template_id = candidate_id
                    break
            if template_id is None:
                template_id = len(template_records)
                template_buckets[graph_hash].append(template_id)
                template_records.append(
                    {
                        "graph": graph,
                        "graph_hash": graph_hash,
                        "summary": summary,
                        "count": 0,
                        "representative_conflict_index": conflict[
                            "conflict_index"
                        ],
                        "representative_premises": [
                            {
                                key: value
                                for key, value in premise.items()
                                if key != "expression"
                            }
                            for premise in premises
                        ],
                    }
                )
            template_records[template_id]["count"] += 1
            premise_count_distribution[len(premises)] += 1
            conflict_template_map.append(
                {
                    "conflict_index": conflict["conflict_index"],
                    "template_id": template_id,
                    "minimal_premise_count": len(premises),
                }
            )
        if position % 100 == 0:
            print(
                f"processed={position}/{len(hall_core['conflicts'])} "
                f"templates={len(template_records)}",
                flush=True,
            )

    public_templates = [
        {
            "template_id": template_id,
            "count": record["count"],
            "graph_hash": record["graph_hash"],
            **record["summary"],
            "representative_conflict_index": record[
                "representative_conflict_index"
            ],
            "representative_premises": record["representative_premises"],
        }
        for template_id, record in enumerate(template_records)
    ]
    result = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "each row-local Hall conflict is reduced to a deletion-minimal "
            "arithmetic premise set and quotiented exactly under good and "
            "same-colored-premise relabeling; mixed-row conflicts are "
            "reported separately"
        ),
        "n": n,
        "m": m,
        "seed_sha256": sha256(seed_path),
        "compact_core_sha256": sha256(compact_core_path),
        "inequality_core_sha256": sha256(inequality_core_path),
        "hall_core_sha256": sha256(hall_core_path),
        "hall_conflict_count": len(hall_core["conflicts"]),
        "row_local_conflict_count": sum(
            record["template_id"] is not None
            for record in conflict_template_map
        ),
        "mixed_row_conflict_count": sum(
            record["template_id"] is None
            for record in conflict_template_map
        ),
        "exact_row_local_template_count": len(public_templates),
        "row_local_minimal_premise_count_distribution": dict(
            sorted(premise_count_distribution.items())
        ),
        "mixed_row_minimal_premise_count_distribution": dict(
            sorted(mixed_distribution.items())
        ),
        "solver_check_count": solver_checks,
        "elapsed_seconds": time.time() - started,
        "templates": public_templates,
        "conflict_template_map": conflict_template_map,
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--compact-core", type=Path, required=True)
    parser.add_argument("--inequality-core", type=Path, required=True)
    parser.add_argument("--hall-core", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=30.0)
    args = parser.parse_args()
    run(
        seed_path=args.seed,
        compact_core_path=args.compact_core,
        inequality_core_path=args.inequality_core,
        hall_core_path=args.hall_core,
        output_path=args.output,
        time_limit_s=args.time_limit,
    )


if __name__ == "__main__":
    main()
