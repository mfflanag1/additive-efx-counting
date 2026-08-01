#!/usr/bin/env python3
"""Independent SMT-LIB generator for the eight positive additive (4,8) cells.

This module intentionally imports neither Z3 nor any project encoding or
partition code. It emits strict SMT-LIB 2 QF_LRA directly.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import tempfile
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


N = 4
M = 8


@dataclass(frozen=True)
class Cell:
    name: str
    favorites: tuple[int, ...]
    seconds: tuple[int, ...] | None
    favorite_stabilizer: bool
    prefix_stabilizer: bool


CELLS = (
    Cell("favorite-211", (0, 0, 1, 2), None, False, False),
    Cell("favorite-31", (0, 0, 0, 1), None, True, False),
    Cell("favorite-22", (0, 0, 1, 1), None, True, False),
    Cell("top4-second1111", (0, 0, 0, 0), (1, 2, 3, 4), False, True),
    Cell("top4-second4", (0, 0, 0, 0), (1, 1, 1, 1), False, True),
    Cell("top4-second31", (0, 0, 0, 0), (1, 1, 1, 2), False, True),
    Cell("top4-second22", (0, 0, 0, 0), (1, 1, 2, 2), False, True),
    Cell("top4-second211", (0, 0, 0, 0), (1, 1, 2, 3), False, True),
)


def value(agent: int, good: int) -> str:
    return f"v_a{agent}_g{good}"


def application(operator: str, terms: Sequence[str]) -> str:
    if not terms:
        raise ValueError(f"{operator} needs at least one operand")
    if len(terms) == 1:
        if operator in {"+", "and", "or"}:
            return terms[0]
        raise ValueError(f"cannot simplify unary {operator}")
    return f"({operator} {' '.join(terms)})"


def sum_expr(agent: int, goods: Sequence[int]) -> str:
    if not goods:
        return "0"
    return application("+", [value(agent, good) for good in goods])


def and_expr(terms: Sequence[str]) -> str:
    return application("and", terms)


def or_expr(terms: Sequence[str]) -> str:
    return application("or", terms)


def lex_ge(left: Sequence[str], right: Sequence[str]) -> str:
    if not left or len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal positive length")
    branches = [
        and_expr([f"(= {x} {y})" for x, y in zip(left, right)])
    ]
    for index in range(len(left)):
        prefix = [
            f"(= {left[position]} {right[position]})"
            for position in range(index)
        ]
        branches.append(
            and_expr([*prefix, f"(> {left[index]} {right[index]})"])
        )
    return or_expr(branches)


def iter_partitions(n: int, m: int) -> Iterable[tuple[tuple[int, ...], ...]]:
    """Yield set partitions as restricted-growth strings."""
    if n < 1 or m < n:
        return

    labels = [0]

    def visit(position: int, maximum: int) -> Iterable[tuple[tuple[int, ...], ...]]:
        if position == m:
            if maximum + 1 == n:
                yield tuple(
                    tuple(
                        good
                        for good, label in enumerate(labels)
                        if label == bundle
                    )
                    for bundle in range(n)
                )
            return
        remaining_after = m - position - 1
        for label in range(min(maximum + 1, n - 1) + 1):
            new_maximum = max(maximum, label)
            missing = n - (new_maximum + 1)
            if missing > remaining_after:
                continue
            labels.append(label)
            yield from visit(position + 1, new_maximum)
            labels.pop()

    yield from visit(1, 0)


def partition_shape(partition: Sequence[Sequence[int]]) -> str:
    return "".join(map(str, sorted(map(len, partition), reverse=True)))


class Formula:
    def __init__(self) -> None:
        self.lines = [
            "; independent direct SMT-LIB generator",
            "(set-logic QF_LRA)",
            "(set-info :status unsat)",
        ]
        self.assertion_count = 0

    def declare_real(self, name: str) -> None:
        self.lines.append(f"(declare-const {name} Real)")

    def declare_bool(self, name: str) -> None:
        self.lines.append(f"(declare-const {name} Bool)")

    def assert_(self, expression: str) -> None:
        self.lines.append(f"(assert {expression})")
        self.assertion_count += 1

    def render(self) -> bytes:
        return ("\n".join([*self.lines, "(check-sat)", ""]) + "\n").encode()


def add_domain(formula: Formula) -> None:
    for agent in range(N):
        for good in range(M):
            formula.declare_real(value(agent, good))
    for agent in range(N):
        for good in range(M):
            formula.assert_(f"(> {value(agent, good)} 0)")
        formula.assert_(
            f"(= {sum_expr(agent, tuple(range(M)))} 1)"
        )


def add_residual_reductions(formula: Formula) -> None:
    for good in range(M):
        formula.assert_(
            or_expr(
                [
                    f"(> {value(agent, good)} {value(agent, other)})"
                    for agent in range(N)
                    for other in range(M)
                    if other != good
                ]
            )
        )
    for agent in range(N):
        for good in range(M):
            rest = tuple(other for other in range(M) if other != good)
            formula.assert_(
                or_expr(
                    [
                        (
                            f"(< {value(agent, good)} "
                            f"{sum_expr(agent, tuple(x for x in rest if x != removed))})"
                        )
                        for removed in rest
                    ]
                )
            )
    for left in range(N):
        for right in range(left + 1, N):
            formula.assert_(
                or_expr(
                    [
                        f"(not (= {value(left, good)} {value(right, good)}))"
                        for good in range(M)
                    ]
                )
            )


def add_strict_favorites(formula: Formula, favorites: Sequence[int]) -> None:
    if len(favorites) != N:
        raise ValueError("one favorite per agent is required")
    for agent, favorite in enumerate(favorites):
        for other in range(M):
            if other != favorite:
                formula.assert_(
                    f"(> {value(agent, favorite)} {value(agent, other)})"
                )


def add_strict_ranking_prefixes(
    formula: Formula,
    prefixes: Sequence[Sequence[int]],
) -> None:
    if len(prefixes) != N:
        raise ValueError("one ranking prefix per agent is required")
    for agent, prefix in enumerate(prefixes):
        if not prefix or len(prefix) != len(set(prefix)):
            raise ValueError("ranking prefixes must be nonempty and distinct")
        for position, good in enumerate(prefix):
            excluded = set(prefix[: position + 1])
            for other in range(M):
                if other not in excluded:
                    formula.assert_(
                        f"(> {value(agent, good)} {value(agent, other)})"
                    )


def add_favorite_stabilizer(
    formula: Formula,
    favorites: Sequence[int],
) -> None:
    for favorite in sorted(set(favorites)):
        agents = [
            agent for agent, good in enumerate(favorites) if good == favorite
        ]
        for left, right in zip(agents, agents[1:]):
            formula.assert_(
                lex_ge(
                    [value(left, good) for good in range(M)],
                    [value(right, good) for good in range(M)],
                )
            )
    unused_goods = [good for good in range(M) if good not in favorites]
    for left, right in zip(unused_goods, unused_goods[1:]):
        formula.assert_(
            lex_ge(
                [value(agent, left) for agent in range(N)],
                [value(agent, right) for agent in range(N)],
            )
        )


def add_prefix_stabilizer(
    formula: Formula,
    prefixes: Sequence[Sequence[int]],
) -> None:
    canonical = tuple(tuple(prefix) for prefix in prefixes)
    for prefix in sorted(set(canonical)):
        agents = [
            agent for agent, item in enumerate(canonical) if item == prefix
        ]
        for left, right in zip(agents, agents[1:]):
            formula.assert_(
                lex_ge(
                    [value(left, good) for good in range(M)],
                    [value(right, good) for good in range(M)],
                )
            )
    used_goods = {good for prefix in canonical for good in prefix}
    unused_goods = [good for good in range(M) if good not in used_goods]
    for left, right in zip(unused_goods, unused_goods[1:]):
        formula.assert_(
            lex_ge(
                [value(agent, left) for agent in range(N)],
                [value(agent, right) for agent in range(N)],
            )
        )


def add_cell(formula: Formula, cell: Cell) -> None:
    if cell.seconds is None:
        add_strict_favorites(formula, cell.favorites)
        if cell.favorite_stabilizer:
            add_favorite_stabilizer(formula, cell.favorites)
        return
    prefixes = tuple(zip(cell.favorites, cell.seconds))
    add_strict_ranking_prefixes(formula, prefixes)
    if cell.prefix_stabilizer:
        add_prefix_stabilizer(formula, prefixes)


def add_partition_obstruction(
    formula: Formula,
    partition_index: int,
    partition: Sequence[Sequence[int]],
) -> None:
    edges = [
        [f"edge_p{partition_index}_a{agent}_b{bundle}" for bundle in range(N)]
        for agent in range(N)
    ]
    for row in edges:
        for edge in row:
            formula.declare_bool(edge)
    for agent in range(N):
        for own_bundle in range(N):
            own = sum_expr(agent, partition[own_bundle])
            comparisons = []
            for target_bundle in range(N):
                if target_bundle == own_bundle:
                    continue
                target = partition[target_bundle]
                for removed in target:
                    remainder = tuple(good for good in target if good != removed)
                    comparisons.append(
                        f"(>= {own} {sum_expr(agent, remainder)})"
                    )
            formula.assert_(
                f"(= {edges[agent][own_bundle]} {and_expr(comparisons)})"
            )
    for matching in itertools.permutations(range(N)):
        formula.assert_(
            or_expr(
                [
                    f"(not {edges[agent][matching[agent]]})"
                    for agent in range(N)
                ]
            )
        )


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def build(cell: Cell, *, output_dir: Path) -> dict:
    formula_path = output_dir / f"{cell.name}.independent.smt2"
    metadata_path = output_dir / f"{cell.name}.independent.json"
    if formula_path.exists() or metadata_path.exists():
        raise ValueError(f"outputs already exist for {cell.name}")
    formula = Formula()
    add_domain(formula)
    add_residual_reductions(formula)
    add_cell(formula, cell)
    shape_counts: Counter[str] = Counter()
    partition_count = 0
    for index, partition in enumerate(iter_partitions(N, M)):
        add_partition_obstruction(formula, index, partition)
        shape_counts[partition_shape(partition)] += 1
        partition_count += 1
    if partition_count != 1701:
        raise AssertionError(f"independent partition count changed: {partition_count}")
    formula_bytes = formula.render()
    atomic_write(formula_path, formula_bytes)
    metadata = {
        "schema": "independent-partition-lra-formula-v1",
        "meaning": (
            "strict SMT-LIB QF_LRA encoding written without Z3 or imports "
            "from the project encoder"
        ),
        "n": N,
        "m": M,
        "cell": asdict(cell),
        "partition_count": partition_count,
        "partition_count_by_shape": dict(sorted(shape_counts.items())),
        "assertion_count": formula.assertion_count,
        "formula": str(formula_path.resolve()),
        "formula_sha256": hashlib.sha256(formula_bytes).hexdigest(),
        "generator": str(Path(__file__).resolve()),
        "generator_sha256": source_sha256(),
    }
    atomic_write(
        metadata_path,
        (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--cell",
        action="append",
        choices=[cell.name for cell in CELLS],
        help="cell to build; omit to build all eight",
    )
    args = parser.parse_args()
    selected = set(args.cell or [cell.name for cell in CELLS])
    for cell in CELLS:
        if cell.name in selected:
            build(cell, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
