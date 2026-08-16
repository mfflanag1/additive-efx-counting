#!/usr/bin/env python3
"""Audit scale-invariant potentials on eligible one-floater EFX states."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Callable

import numpy as np

try:
    from . import core
    from .anneal import atomic_json
except ImportError:
    import core
    from anneal import atomic_json


SCHEMA = "partial-state-potential-audit-v1"
Potential = Callable[[dict], tuple[Fraction, ...]]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def product(items: tuple[Fraction, ...]) -> Fraction:
    return reduce(mul, items, Fraction(1))


def nested_value(document: dict, keys: tuple[str, ...]):
    value = document
    for key in keys:
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def profile_records(path: Path) -> list[dict]:
    document = json.loads(path.read_text())
    candidates = (
        (("values",), "values"),
        (("positive_nondegenerate_lift", "values"), "positive_lift"),
        (("post_wall_values",), "post_wall"),
        (("wall_values",), "wall"),
    )
    records = []
    for keys, label in candidates:
        raw = nested_value(document, keys)
        if raw is None:
            continue
        values = core.validate_values(raw, lower=1)
        records.append(
            {
                "label": f"{path.stem}:{label}",
                "source": str(path),
                "source_sha256": sha256(path),
                "value_key": ".".join(keys),
                "values": values,
            }
        )
        if label in {"values", "positive_lift"}:
            break
    if not records:
        raise ValueError(f"{path} has no recognized positive valuation matrix")
    return records


def subset_tables(values: tuple[tuple[int, ...], ...]):
    m = len(values[0])
    subsets = np.arange(1 << m, dtype=np.int64)
    goods = np.arange(m, dtype=np.int64)
    bits = ((subsets[:, None] >> goods) & 1).astype(bool)
    matrix = np.asarray(values, dtype=np.int64)
    totals = matrix @ bits.T
    sentinel = int(matrix.max()) + 1
    minima = np.where(bits[None, :, :], matrix[:, None, :], sentinel).min(axis=2)
    minima[:, 0] = 0
    return totals, totals - minima


def partial_masks(n: int, m: int, floater: int) -> np.ndarray:
    assignments = np.arange(n ** (m - 1), dtype=np.int64)
    powers = n ** np.arange(m - 1, dtype=np.int64)
    choices = (assignments[:, None] // powers) % n
    masks = np.zeros((len(assignments), n), dtype=np.int64)
    rows = np.arange(len(assignments))
    for position, good in enumerate(
        item for item in range(m) if item != floater
    ):
        masks[rows, choices[:, position]] |= 1 << good
    return masks


def enumerate_states(values: tuple[tuple[int, ...], ...]) -> list[dict]:
    n = len(values)
    m = len(values[0])
    matrix = np.asarray(values, dtype=np.int64)
    totals, thresholds = subset_tables(values)
    row_totals = tuple(map(sum, values))
    states = []
    for floater in range(m):
        masks = partial_masks(n, m, floater)
        valid = np.ones(len(masks), dtype=bool)
        own_values = np.empty((len(masks), n), dtype=np.int64)
        for observer in range(n):
            own = totals[observer, masks[:, observer]]
            own_values[:, observer] = own
            valid &= own >= matrix[observer, floater]
            for target in range(n):
                if observer != target:
                    valid &= own >= thresholds[observer, masks[:, target]]
        for index in np.flatnonzero(valid):
            masks_at_index = tuple(int(mask) for mask in masks[index])
            own = tuple(int(value) for value in own_values[index])
            insertable_hosts = []
            for host in range(n):
                enlarged = masks_at_index[host] | (1 << floater)
                if all(
                    own[observer] >= thresholds[observer, enlarged]
                    for observer in range(n)
                    if observer != host
                ):
                    insertable_hosts.append(host)
            normalized = tuple(
                Fraction(own[agent], row_totals[agent]) for agent in range(n)
            )
            ratios = tuple(
                Fraction(own[agent], values[agent][floater])
                for agent in range(n)
            )
            surplus = tuple(
                Fraction(
                    own[agent] - values[agent][floater],
                    row_totals[agent],
                )
                for agent in range(n)
            )
            states.append(
                {
                    "floater": floater,
                    "base_index": int(index),
                    "masks": masks_at_index,
                    "utilities": own,
                    "normalized": normalized,
                    "floater_ratios": ratios,
                    "normalized_floater_surplus": surplus,
                    "insertable_hosts": tuple(insertable_hosts),
                }
            )
    if not states:
        raise AssertionError("profile has no eligible one-floater EFX state")
    return states


def potentials() -> dict[str, Potential]:
    return {
        "normalized_utilitarian": lambda state: (
            sum(state["normalized"], Fraction()),
        ),
        "normalized_nash": lambda state: (
            product(state["normalized"]),
        ),
        "normalized_leximin": lambda state: tuple(
            sorted(state["normalized"])
        ),
        "normalized_leximax": lambda state: tuple(
            sorted(state["normalized"], reverse=True)
        ),
        "normalized_harmonic": lambda state: (
            -sum(
                (Fraction(1, share) for share in state["normalized"]),
                Fraction(),
            ),
        ),
        "floater_ratio_nash": lambda state: (
            product(state["floater_ratios"]),
        ),
        "floater_ratio_leximin": lambda state: tuple(
            sorted(state["floater_ratios"])
        ),
        "floater_ratio_harmonic": lambda state: (
            -sum(
                (Fraction(1, ratio) for ratio in state["floater_ratios"]),
                Fraction(),
            ),
        ),
        "floater_surplus_utilitarian": lambda state: (
            sum(state["normalized_floater_surplus"], Fraction()),
        ),
        "floater_surplus_nash": lambda state: (
            product(state["normalized_floater_surplus"]),
        ),
        "floater_surplus_leximin": lambda state: tuple(
            sorted(state["normalized_floater_surplus"])
        ),
    }


def public_fraction(value: Fraction) -> dict[str, int]:
    return {"numerator": value.numerator, "denominator": value.denominator}


def public_key(key: tuple[Fraction, ...]) -> list[dict[str, int]]:
    return [public_fraction(value) for value in key]


def dominates(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return all(a >= b for a, b in zip(left, right)) and left != right


def pareto_record(states: list[dict]) -> dict:
    by_utilities: dict[tuple[int, ...], bool] = {}
    for state in states:
        utilities = state["utilities"]
        by_utilities[utilities] = (
            by_utilities.get(utilities, False) or bool(state["insertable_hosts"])
        )
    points = tuple(by_utilities)
    frontier = [
        point
        for point in points
        if not any(dominates(other, point) for other in points)
    ]
    insertable_frontier = [point for point in frontier if by_utilities[point]]
    return {
        "distinct_utility_vector_count": len(points),
        "pareto_frontier_utility_vector_count": len(frontier),
        "insertable_pareto_frontier_utility_vector_count": len(
            insertable_frontier
        ),
        "has_insertable_pareto_frontier_state": bool(insertable_frontier),
    }


def audit_profile(record: dict) -> dict:
    values = record.pop("values")
    n = len(values)
    m = len(values[0])
    states = enumerate_states(values)
    potential_records = {}
    for name, potential in potentials().items():
        keys = [potential(state) for state in states]
        best_key = max(keys)
        winners = [state for state, key in zip(states, keys) if key == best_key]
        insertable = [state for state in winners if state["insertable_hosts"]]
        potential_records[name] = {
            "winner_count": len(winners),
            "insertable_winner_count": len(insertable),
            "has_insertable_winner": bool(insertable),
            "all_winners_insertable": len(insertable) == len(winners),
            "best_key": public_key(best_key),
            "representative_winner": {
                "floater": winners[0]["floater"],
                "base_index": winners[0]["base_index"],
                "utilities": list(winners[0]["utilities"]),
                "insertable_hosts": list(winners[0]["insertable_hosts"]),
            },
        }
    return {
        **record,
        "n": n,
        "m": m,
        "values_sha256": hashlib.sha256(
            json.dumps(values, separators=(",", ":")).encode()
        ).hexdigest(),
        "eligible_state_count": len(states),
        "insertable_state_count": sum(
            bool(state["insertable_hosts"]) for state in states
        ),
        "pareto": pareto_record(states),
        "potentials": potential_records,
    }


def run(paths: list[Path], output: Path) -> dict:
    raw_records = [record for path in paths for record in profile_records(path)]
    seen = set()
    records = []
    for record in raw_records:
        values = record["values"]
        key = tuple(values)
        if key in seen:
            continue
        seen.add(key)
        print(f"auditing {record['label']}", flush=True)
        records.append(audit_profile(record))
    names = tuple(potentials())
    summary = {
        name: {
            "profile_count": len(records),
            "profile_count_with_insertable_winner": sum(
                record["potentials"][name]["has_insertable_winner"]
                for record in records
            ),
            "profile_count_with_all_winners_insertable": sum(
                record["potentials"][name]["all_winners_insertable"]
                for record in records
            ),
            "refuting_profiles": [
                record["label"]
                for record in records
                if not record["potentials"][name]["has_insertable_winner"]
            ],
        }
        for name in names
    }
    result = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "exact census of scale-invariant potential maximizers among "
            "eligible one-floater EFX states; survival on this finite corpus "
            "is not a theorem"
        ),
        "profile_count": len(records),
        "potential_summary": summary,
        "pareto_summary": {
            "profile_count_with_insertable_frontier_state": sum(
                record["pareto"]["has_insertable_pareto_frontier_state"]
                for record in records
            ),
            "refuting_profiles": [
                record["label"]
                for record in records
                if not record["pareto"]["has_insertable_pareto_frontier_state"]
            ],
        },
        "profiles": records,
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not all(path.exists() for path in args.profile):
        parser.error("every profile path must exist")
    run(args.profile, args.output)


if __name__ == "__main__":
    main()
