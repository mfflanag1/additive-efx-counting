#!/usr/bin/env python3
"""Mine valuation-ranked Hamiltonian-path selectors from exact row-merge traces."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "row-merge-q4-valuation-selector-mining-v1"
N = 4
BASE = ((0, 1), (2, 3), (4, 5), (6, 7, 8))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_post_values(trace_path: Path, round_index: int) -> tuple[tuple[int, ...], ...]:
    trace = json.loads(trace_path.read_text())
    if trace.get("schema") == "row-merge-q4-exchange-chain-cegar-v1":
        rounds = {
            record["round"]: record
            for record in trace["rounds"]
            if record.get("solver_status") == "sat"
        }
        record = rounds[round_index]
        return tuple(tuple(row) for row in record["post_wall_values"])
    if (
        trace.get("schema") == "row-merge-q4-cycle023-gate-v1"
        and trace.get("solver_status") == "sat"
        and round_index == 0
    ):
        return tuple(tuple(row) for row in trace["post_wall_values"])
    raise ValueError(f"unsupported exact trace: {trace_path}")


def criterion_scores(
    values: tuple[tuple[int, ...], ...],
    source: int,
) -> dict[str, dict[int, int]]:
    goods = BASE[source]
    scores = {
        f"row{agent}_{direction}": {
            good: values[agent][good] for good in goods
        }
        for agent in range(N)
        for direction in ("min", "max")
    }
    total = {good: sum(values[agent][good] for agent in range(N)) for good in goods}
    scores["rowsum_min"] = total
    scores["rowsum_max"] = total
    return scores


def selected_goods(scores: dict[str, dict[int, int]], criterion: str) -> set[int]:
    direction = criterion.rsplit("_", 1)[1]
    extremum = min(scores[criterion].values()) if direction == "min" else max(
        scores[criterion].values()
    )
    return {
        good for good, score in scores[criterion].items() if score == extremum
    }


def policy_key(policy_class: str, source: int, target: int) -> str:
    if policy_class == "global":
        return "global"
    if policy_class == "source":
        return f"source:{source}"
    if policy_class == "target":
        return f"target:{target}"
    if policy_class == "edge":
        return f"edge:{source}>{target}"
    raise ValueError(f"unknown policy class: {policy_class}")


def policy_keys(policy_class: str) -> tuple[str, ...]:
    if policy_class == "global":
        return ("global",)
    if policy_class == "source":
        return tuple(f"source:{source}" for source in range(N))
    if policy_class == "target":
        return tuple(f"target:{target}" for target in range(N))
    if policy_class == "edge":
        return tuple(
            f"edge:{source}>{target}"
            for source in range(N)
            for target in range(N)
            if source != target
        )
    raise ValueError(f"unknown policy class: {policy_class}")


def compatible_criteria(
    values: tuple[tuple[int, ...], ...],
    source: int,
    good: int,
    criteria: tuple[str, ...],
) -> tuple[int, ...]:
    scores = criterion_scores(values, source)
    return tuple(
        index
        for index, criterion in enumerate(criteria)
        if good in selected_goods(scores, criterion)
    )


def hamiltonian_actions(model: dict) -> tuple[dict, ...]:
    actions = {}
    for support in model["supports"]:
        for action in support["actions"]:
            if action["kind"] != "path" or action["length"] != N - 1:
                continue
            if len(set(action["vertices"])) != N:
                continue
            key = (tuple(action["vertices"]), tuple(action["goods"]))
            actions[key] = {
                "vertices": tuple(action["vertices"]),
                "goods": tuple(action["goods"]),
                "partition": tuple(tuple(bundle) for bundle in support["partition"]),
                "matching_count": support["matching_count"],
            }
    return tuple(actions[key] for key in sorted(actions))


def decide_policy(
    models: tuple[dict, ...],
    policy_class: str,
    criteria: tuple[str, ...],
) -> dict:
    keys = policy_keys(policy_class)
    choices = {key: z3.Int(f"choice_{key.replace(':', '_').replace('>', '_')}") for key in keys}
    solver = z3.Solver()
    solver.add(*(z3.And(choice >= 0, choice < len(criteria)) for choice in choices.values()))
    cached_allowed: dict[tuple[int, int, int], tuple[int, ...]] = {}
    compatible_by_model: list[list[tuple[dict, list[tuple[str, tuple[int, ...]]]]]] = []
    for model_index, model in enumerate(models):
        compatible_actions = []
        action_formulas = []
        for action in model["hamiltonian_actions"]:
            edge_conditions = []
            edge_records = []
            vertices = action["vertices"]
            for edge_index, good in enumerate(action["goods"]):
                source = vertices[edge_index]
                target = vertices[edge_index + 1]
                cache_key = (model_index, source, good)
                if cache_key not in cached_allowed:
                    cached_allowed[cache_key] = compatible_criteria(
                        model["post_wall_values"], source, good, criteria
                    )
                allowed = cached_allowed[cache_key]
                if not allowed:
                    edge_conditions = []
                    break
                key = policy_key(policy_class, source, target)
                edge_conditions.append(
                    z3.Or(*(choices[key] == criterion for criterion in allowed))
                )
                edge_records.append((key, allowed))
            if edge_conditions:
                action_formulas.append(z3.And(*edge_conditions))
                compatible_actions.append((action, edge_records))
        if not action_formulas:
            return {
                "status": "unsat",
                "reason": f"model {model_index} has no criterion-compatible supporting action",
            }
        solver.add(z3.Or(*action_formulas))
        compatible_by_model.append(compatible_actions)

    used = [z3.Bool(f"used_{index}") for index in range(len(criteria))]
    for criterion, flag in enumerate(used):
        solver.add(flag == z3.Or(*(choice == criterion for choice in choices.values())))
    minimum_used = None
    solved_model = None
    for limit in range(1, len(criteria) + 1):
        solver.push()
        solver.add(z3.PbLe([(flag, 1) for flag in used], limit))
        if solver.check() == z3.sat:
            solved_model = solver.model()
            minimum_used = limit
            solver.pop()
            break
        solver.pop()
    if solved_model is None or minimum_used is None:
        return {"status": "unsat"}

    policy = {
        key: criteria[solved_model.eval(choice).as_long()]
        for key, choice in sorted(choices.items())
    }
    minimum_policies = []
    if len(keys) <= 4:
        solver.add(z3.PbLe([(flag, 1) for flag in used], minimum_used))
        while len(minimum_policies) < 512 and solver.check() == z3.sat:
            enumerated_model = solver.model()
            enumerated = {
                key: criteria[enumerated_model.eval(choice).as_long()]
                for key, choice in sorted(choices.items())
            }
            minimum_policies.append(enumerated)
            solver.add(
                z3.Or(
                    *(
                        choice != enumerated_model.eval(choice)
                        for choice in choices.values()
                    )
                )
            )
    witnesses = []
    for model_index, compatible_actions in enumerate(compatible_by_model):
        witness = None
        for action, edge_records in compatible_actions:
            if all(
                policy[key] in {criteria[index] for index in allowed}
                for key, allowed in edge_records
            ):
                witness = {
                    "vertices": list(action["vertices"]),
                    "goods": list(action["goods"]),
                    "partition": [list(bundle) for bundle in action["partition"]],
                    "matching_count": action["matching_count"],
                    "edge_rules": [
                        {
                            "edge": key.split(":", 1)[-1],
                            "criterion": policy[key],
                        }
                        for key, _allowed in edge_records
                    ],
                }
                break
        if witness is None:
            raise AssertionError("decoded policy lacks its asserted witness")
        witnesses.append({"model_index": model_index, **witness})
    return {
        "status": "sat",
        "minimum_distinct_criterion_count": minimum_used,
        "minimum_policy_count": len(minimum_policies) if len(keys) <= 4 else None,
        "minimum_policies": minimum_policies if len(keys) <= 4 else None,
        "policy": policy,
        "witnesses": witnesses,
    }


def run(analysis_path: Path, output_path: Path) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    analysis = json.loads(analysis_path.read_text())
    if (
        analysis.get("schema") != "row-merge-q4-chain-trace-analysis-v1"
        or tuple(tuple(bundle) for bundle in analysis.get("wall_partition", ())) != BASE
    ):
        raise ValueError("analysis describes another exchange-chain cell")

    trace_hashes = {}
    models = []
    for record in analysis["models"]:
        trace_path = Path(record["trace"])
        trace_hash = sha256(trace_path)
        if trace_hash != record["trace_sha256"]:
            raise AssertionError(f"trace hash changed: {trace_path}")
        trace_hashes[str(trace_path)] = trace_hash
        actions = hamiltonian_actions(record)
        if not actions:
            raise AssertionError("a stored exact model lost Hamiltonian-path support")
        models.append(
            {
                "trace": str(trace_path),
                "trace_sha256": trace_hash,
                "round": record["round"],
                "post_wall_values": load_post_values(trace_path, record["round"]),
                "hamiltonian_actions": actions,
            }
        )

    criterion_families = {
        "row_min": tuple(f"row{agent}_min" for agent in range(N)),
        "row_extrema": tuple(
            f"row{agent}_{direction}"
            for agent in range(N)
            for direction in ("min", "max")
        ),
        "row_and_sum_extrema": (
            *(
                f"row{agent}_{direction}"
                for agent in range(N)
                for direction in ("min", "max")
            ),
            "rowsum_min",
            "rowsum_max",
        ),
    }
    decisions = {}
    for family_name, criteria in criterion_families.items():
        decisions[family_name] = {
            policy_class: decide_policy(tuple(models), policy_class, criteria)
            for policy_class in ("global", "source", "target", "edge")
        }

    supported = [
        (family, policy_class, decision)
        for family, family_decisions in decisions.items()
        for policy_class, decision in family_decisions.items()
        if decision["status"] == "sat"
    ]
    simplest = min(
        supported,
        key=lambda entry: (
            ("global", "source", "target", "edge").index(entry[1]),
            entry[2]["minimum_distinct_criterion_count"],
            len(criterion_families[entry[0]]),
        ),
        default=None,
    )
    result = {
        "schema": SCHEMA,
        "status": "FINITE_TRACE_SELECTOR_FOUND" if simplest else "NO_TESTED_SELECTOR",
        "analysis": str(analysis_path),
        "analysis_sha256": sha256(analysis_path),
        "wall_partition": [list(bundle) for bundle in BASE],
        "exact_model_count": len(models),
        "trace_hashes": dict(sorted(trace_hashes.items())),
        "criterion_families": {
            name: list(criteria) for name, criteria in criterion_families.items()
        },
        "decisions": decisions,
        "simplest_surviving_selector": (
            {
                "criterion_family": simplest[0],
                "policy_class": simplest[1],
                **simplest[2],
            }
            if simplest
            else None
        ),
        "claim_boundary": (
            "This is exact finite-trace proof mining. A surviving selector is not "
            "a wall-pivot theorem; it must be encoded against fresh adversarial "
            "models or proved analytically."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--analysis", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.analysis, args.output)


if __name__ == "__main__":
    main()
