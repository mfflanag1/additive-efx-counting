#!/usr/bin/env python3
"""Parse and audit the exact semantics of the eight independent SMT formulas.

This checker intentionally does not import the independent generator, Z3, or
any project encoding module.  It parses the emitted SMT-LIB, validates every
preamble assertion against a separate declarative specification, reconstructs
every bundle partition from the edge definitions, validates all edge
definitions and all 24 perfect-matching obstruction clauses, and compares the
reconstructed partitions with a brute-force enumeration of all set
partitions.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path
from typing import Iterable, Sequence


N = 4
M = 8
TOKEN = re.compile(r"\(|\)|[^\s()]+")

CELLS = {
    "favorite-211": {
        "favorites": (0, 0, 1, 2),
        "seconds": None,
        "favorite_stabilizer": False,
        "prefix_stabilizer": False,
        "lean_spec": "FavoriteCellSpec weight canonical211",
    },
    "favorite-31": {
        "favorites": (0, 0, 0, 1),
        "seconds": None,
        "favorite_stabilizer": True,
        "prefix_stabilizer": False,
        "lean_spec": "FavoriteStabilizedCellSpec weight canonical31",
    },
    "favorite-22": {
        "favorites": (0, 0, 1, 1),
        "seconds": None,
        "favorite_stabilizer": True,
        "prefix_stabilizer": False,
        "lean_spec": "FavoriteStabilizedCellSpec weight canonical22",
    },
    "top4-second1111": {
        "favorites": (0, 0, 0, 0),
        "seconds": (1, 2, 3, 4),
        "favorite_stabilizer": False,
        "prefix_stabilizer": True,
        "lean_spec": "PrefixStabilizedCellSpec weight second1111",
    },
    "top4-second4": {
        "favorites": (0, 0, 0, 0),
        "seconds": (1, 1, 1, 1),
        "favorite_stabilizer": False,
        "prefix_stabilizer": True,
        "lean_spec": "PrefixStabilizedCellSpec weight second4",
    },
    "top4-second31": {
        "favorites": (0, 0, 0, 0),
        "seconds": (1, 1, 1, 2),
        "favorite_stabilizer": False,
        "prefix_stabilizer": True,
        "lean_spec": "PrefixStabilizedCellSpec weight second31",
    },
    "top4-second22": {
        "favorites": (0, 0, 0, 0),
        "seconds": (1, 1, 2, 2),
        "favorite_stabilizer": False,
        "prefix_stabilizer": True,
        "lean_spec": "PrefixStabilizedCellSpec weight second22",
    },
    "top4-second211": {
        "favorites": (0, 0, 0, 0),
        "seconds": (1, 1, 2, 3),
        "favorite_stabilizer": False,
        "prefix_stabilizer": True,
        "lean_spec": "PrefixStabilizedCellSpec weight second211",
    },
}

LEAN_CONSTANTS = {
    "canonical211": (0, 0, 1, 2),
    "canonical31": (0, 0, 0, 1),
    "canonical22": (0, 0, 1, 1),
    "canonical4": (0, 0, 0, 0),
    "second1111": (1, 2, 3, 4),
    "second4": (1, 1, 1, 1),
    "second31": (1, 1, 1, 2),
    "second22": (1, 1, 2, 2),
    "second211": (1, 1, 2, 3),
}

CELL_LEAN_CONSTANTS = {
    "favorite-211": ("canonical211", None),
    "favorite-31": ("canonical31", None),
    "favorite-22": ("canonical22", None),
    "top4-second1111": ("canonical4", "second1111"),
    "top4-second4": ("canonical4", "second4"),
    "top4-second31": ("canonical4", "second31"),
    "top4-second22": ("canonical4", "second22"),
    "top4-second211": ("canonical4", "second211"),
}


class AuditError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_sexpr(text: str):
    tokens = TOKEN.findall(text)
    position = 0

    def parse():
        nonlocal position
        if position >= len(tokens):
            raise AuditError(f"unexpected end of expression: {text[:120]!r}")
        token = tokens[position]
        position += 1
        if token != "(":
            if token == ")":
                raise AuditError(f"unexpected ')': {text[:120]!r}")
            return token
        result = []
        while True:
            if position >= len(tokens):
                raise AuditError(f"unclosed expression: {text[:120]!r}")
            if tokens[position] == ")":
                position += 1
                return tuple(result)
            result.append(parse())

    result = parse()
    if position != len(tokens):
        raise AuditError(f"trailing tokens: {text[:120]!r}")
    return result


def app(operator: str, terms: Sequence):
    if not terms:
        raise AuditError(f"{operator} requires an operand")
    if len(terms) == 1 and operator in {"+", "and", "or"}:
        return terms[0]
    return (operator, *terms)


def value(agent: int, good: int) -> str:
    return f"v_a{agent}_g{good}"


def sum_expr(agent: int, goods: Sequence[int]):
    if not goods:
        return "0"
    return app("+", tuple(value(agent, good) for good in goods))


def lex_ge(left: Sequence[str], right: Sequence[str]):
    branches = [
        app("and", tuple(("=", x, y) for x, y in zip(left, right)))
    ]
    for index in range(len(left)):
        prefix = tuple(
            ("=", left[position], right[position])
            for position in range(index)
        )
        branches.append(
            app("and", (*prefix, (">", left[index], right[index])))
        )
    return app("or", tuple(branches))


def expected_domain_assertions() -> list:
    result = []
    for agent in range(N):
        for good in range(M):
            result.append((">", value(agent, good), "0"))
        result.append(
            ("=", sum_expr(agent, tuple(range(M))), "1")
        )
    return result


def expected_residual_assertions() -> list:
    result = []
    for good in range(M):
        result.append(
            app(
                "or",
                tuple(
                    (">", value(agent, good), value(agent, other))
                    for agent in range(N)
                    for other in range(M)
                    if other != good
                ),
            )
        )
    for agent in range(N):
        for good in range(M):
            rest = tuple(other for other in range(M) if other != good)
            result.append(
                app(
                    "or",
                    tuple(
                        (
                            "<",
                            value(agent, good),
                            sum_expr(
                                agent,
                                tuple(x for x in rest if x != removed),
                            ),
                        )
                        for removed in rest
                    ),
                )
            )
    for left in range(N):
        for right in range(left + 1, N):
            result.append(
                app(
                    "or",
                    tuple(
                        (
                            "not",
                            ("=", value(left, good), value(right, good)),
                        )
                        for good in range(M)
                    ),
                )
            )
    return result


def expected_strict_favorites(favorites: Sequence[int]) -> list:
    return [
        (">", value(agent, favorite), value(agent, other))
        for agent, favorite in enumerate(favorites)
        for other in range(M)
        if other != favorite
    ]


def expected_strict_prefixes(
    favorites: Sequence[int], seconds: Sequence[int]
) -> list:
    result = []
    for agent, (favorite, second) in enumerate(zip(favorites, seconds)):
        for position, good in enumerate((favorite, second)):
            excluded = {favorite} if position == 0 else {favorite, second}
            for other in range(M):
                if other not in excluded:
                    result.append(
                        (">", value(agent, good), value(agent, other))
                    )
    return result


def expected_favorite_stabilizer(favorites: Sequence[int]) -> list:
    result = []
    for favorite in sorted(set(favorites)):
        agents = [
            agent for agent, item in enumerate(favorites)
            if item == favorite
        ]
        for left, right in zip(agents, agents[1:]):
            result.append(
                lex_ge(
                    [value(left, good) for good in range(M)],
                    [value(right, good) for good in range(M)],
                )
            )
    unused = [good for good in range(M) if good not in favorites]
    for left, right in zip(unused, unused[1:]):
        result.append(
            lex_ge(
                [value(agent, left) for agent in range(N)],
                [value(agent, right) for agent in range(N)],
            )
        )
    return result


def expected_prefix_stabilizer(
    favorites: Sequence[int], seconds: Sequence[int]
) -> list:
    result = []
    prefixes = tuple(zip(favorites, seconds))
    for prefix in sorted(set(prefixes)):
        agents = [
            agent for agent, item in enumerate(prefixes)
            if item == prefix
        ]
        for left, right in zip(agents, agents[1:]):
            result.append(
                lex_ge(
                    [value(left, good) for good in range(M)],
                    [value(right, good) for good in range(M)],
                )
            )
    used = {good for prefix in prefixes for good in prefix}
    unused = [good for good in range(M) if good not in used]
    for left, right in zip(unused, unused[1:]):
        result.append(
            lex_ge(
                [value(agent, left) for agent in range(N)],
                [value(agent, right) for agent in range(N)],
            )
        )
    return result


def expected_cell_assertions(cell: dict) -> list:
    favorites = cell["favorites"]
    seconds = cell["seconds"]
    if seconds is None:
        result = expected_strict_favorites(favorites)
        if cell["favorite_stabilizer"]:
            result.extend(expected_favorite_stabilizer(favorites))
        return result
    result = expected_strict_prefixes(favorites, seconds)
    if cell["prefix_stabilizer"]:
        result.extend(expected_prefix_stabilizer(favorites, seconds))
    return result


def goods_in_sum(expression, agent: int) -> tuple[int, ...]:
    atoms = expression[1:] if (
        isinstance(expression, tuple) and expression
        and expression[0] == "+"
    ) else (expression,)
    goods = []
    for atom in atoms:
        match = re.fullmatch(r"v_a(\d+)_g(\d+)", atom)
        if match is None or int(match.group(1)) != agent:
            raise AuditError(
                f"invalid agent-{agent} bundle sum: {expression!r}"
            )
        goods.append(int(match.group(2)))
    if len(goods) != len(set(goods)):
        raise AuditError(f"duplicate good in sum: {expression!r}")
    return tuple(goods)


def edge_name(partition: int, agent: int, bundle: int) -> str:
    return f"edge_p{partition}_a{agent}_b{bundle}"


def edge_rhs(
    partition: Sequence[Sequence[int]], agent: int, own_bundle: int
):
    own = sum_expr(agent, partition[own_bundle])
    comparisons = []
    for target_bundle in range(N):
        if target_bundle == own_bundle:
            continue
        target = partition[target_bundle]
        for removed in target:
            comparisons.append(
                (
                    ">=",
                    own,
                    sum_expr(
                        agent,
                        tuple(good for good in target if good != removed),
                    ),
                )
            )
    return app("and", tuple(comparisons))


def canonical_partition(partition: Iterable[Iterable[int]]):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def all_bruteforce_partitions() -> set:
    result = set()
    for owners in itertools.product(range(N), repeat=M):
        if len(set(owners)) != N:
            continue
        result.add(
            canonical_partition(
                tuple(
                    tuple(
                        good for good, owner in enumerate(owners)
                        if owner == bundle
                    )
                    for bundle in range(N)
                )
            )
        )
    return result


def read_commands(path: Path) -> list:
    commands = []
    for line_number, raw in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith(";"):
            continue
        try:
            commands.append((line_number, parse_sexpr(line)))
        except AuditError as error:
            raise AuditError(f"{path}:{line_number}: {error}") from error
    return commands


def audit_lean_constants(lean_root: Path) -> dict:
    sources = (
        lean_root / "EFX48" / "FavoritePatterns.lean",
        lean_root / "EFX48" / "CanonicalCoverage.lean",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in sources)
    records = {}
    for name, expected in LEAN_CONSTANTS.items():
        match = re.search(
            rf"def\s+{re.escape(name)}\s*:\s*"
            rf"Fin\s+4\s*→\s*Fin\s+8\s*:=\s*"
            rf"!\[([0-9,\s]+)\]",
            text,
        )
        if match is None:
            raise AuditError(f"missing Lean constant definition: {name}")
        actual = tuple(
            int(item.strip())
            for item in match.group(1).split(",")
        )
        if actual != expected:
            raise AuditError(
                f"Lean constant {name} is {actual}, expected {expected}"
            )
        records[name] = list(actual)
    cell_bindings = {}
    for cell_name, (favorite_name, second_name) in (
        CELL_LEAN_CONSTANTS.items()
    ):
        cell = CELLS[cell_name]
        if (
            cell["favorites"] != LEAN_CONSTANTS[favorite_name]
            or cell["seconds"]
            != (
                LEAN_CONSTANTS[second_name]
                if second_name is not None
                else None
            )
            or favorite_name not in cell["lean_spec"]
            and second_name is None
            or second_name is not None
            and second_name not in cell["lean_spec"]
        ):
            raise AuditError(
                f"{cell_name}: Lean constant/cell binding mismatch"
            )
        cell_bindings[cell_name] = {
            "favorites": favorite_name,
            "seconds": second_name,
            "lean_spec": cell["lean_spec"],
        }
    return {
        "all_passed": True,
        "constants": records,
        "cell_bindings": cell_bindings,
        "sources": [
            {
                "path": str(path.relative_to(lean_root)),
                "sha256": sha256(path),
            }
            for path in sources
        ],
    }


def audit_formula(path: Path, name: str, universe: set) -> dict:
    cell = CELLS[name]
    commands = read_commands(path)
    cursor = 0

    def take(expected=None):
        nonlocal cursor
        if cursor >= len(commands):
            raise AuditError(f"{path}: unexpected end of command stream")
        line_number, command = commands[cursor]
        cursor += 1
        if expected is not None and command != expected:
            raise AuditError(
                f"{path}:{line_number}: expected {expected!r}, "
                f"found {command!r}"
            )
        return line_number, command

    take(("set-logic", "QF_LRA"))
    take(("set-info", ":status", "unsat"))
    for agent in range(N):
        for good in range(M):
            take(("declare-const", value(agent, good), "Real"))

    domain = expected_domain_assertions()
    residual = expected_residual_assertions()
    cell_assertions = expected_cell_assertions(cell)
    for assertion in (*domain, *residual, *cell_assertions):
        take(("assert", assertion))

    reconstructed = set()
    shape_counts: dict[str, int] = {}
    for partition_index in range(1701):
        for agent in range(N):
            for bundle in range(N):
                take(
                    (
                        "declare-const",
                        edge_name(partition_index, agent, bundle),
                        "Bool",
                    )
                )

        edge_assertions = []
        for agent in range(N):
            for bundle in range(N):
                _, command = take()
                expected_left = edge_name(partition_index, agent, bundle)
                if (
                    len(command) != 2
                    or command[0] != "assert"
                    or not isinstance(command[1], tuple)
                    or len(command[1]) != 3
                    or command[1][0] != "="
                    or command[1][1] != expected_left
                ):
                    raise AuditError(
                        f"{path}: malformed edge definition "
                        f"{partition_index}/{agent}/{bundle}: {command!r}"
                    )
                edge_assertions.append(command[1][2])

        partition = []
        for bundle in range(N):
            rhs = edge_assertions[bundle]
            comparisons = rhs[1:] if (
                isinstance(rhs, tuple) and rhs and rhs[0] == "and"
            ) else (rhs,)
            if not comparisons:
                raise AuditError(
                    f"{path}: empty edge definition at "
                    f"partition {partition_index}, bundle {bundle}"
                )
            first = comparisons[0]
            if (
                not isinstance(first, tuple)
                or len(first) != 3
                or first[0] != ">="
            ):
                raise AuditError(
                    f"{path}: malformed comparison at "
                    f"partition {partition_index}: {first!r}"
                )
            partition.append(goods_in_sum(first[1], 0))
        partition_tuple = tuple(partition)
        flat = [good for bundle in partition_tuple for good in bundle]
        if sorted(flat) != list(range(M)):
            raise AuditError(
                f"{path}: block {partition_index} is not a partition: "
                f"{partition_tuple!r}"
            )

        for agent in range(N):
            for bundle in range(N):
                actual = edge_assertions[agent * N + bundle]
                expected = edge_rhs(partition_tuple, agent, bundle)
                if actual != expected:
                    raise AuditError(
                        f"{path}: incorrect edge semantics at "
                        f"partition {partition_index}, agent {agent}, "
                        f"bundle {bundle}"
                    )

        expected_matching_clauses = {
            app(
                "or",
                tuple(
                    (
                        "not",
                        edge_name(partition_index, agent, matching[agent]),
                    )
                    for agent in range(N)
                ),
            )
            for matching in itertools.permutations(range(N))
        }
        actual_matching_clauses = set()
        for _ in range(24):
            _, command = take()
            if len(command) != 2 or command[0] != "assert":
                raise AuditError(
                    f"{path}: malformed matching clause in "
                    f"partition {partition_index}: {command!r}"
                )
            actual_matching_clauses.add(command[1])
        if actual_matching_clauses != expected_matching_clauses:
            raise AuditError(
                f"{path}: matching clauses differ in "
                f"partition {partition_index}"
            )

        canonical = canonical_partition(partition_tuple)
        if canonical in reconstructed:
            raise AuditError(
                f"{path}: duplicate partition at block {partition_index}"
            )
        reconstructed.add(canonical)
        shape = "".join(
            str(size)
            for size in sorted(
                (len(bundle) for bundle in partition_tuple), reverse=True
            )
        )
        shape_counts[shape] = shape_counts.get(shape, 0) + 1

    take(("check-sat",))
    if cursor != len(commands):
        line_number, command = commands[cursor]
        raise AuditError(
            f"{path}:{line_number}: unexpected trailing command {command!r}"
        )
    if reconstructed != universe:
        raise AuditError(
            f"{path}: reconstructed partition universe mismatch: "
            f"missing={len(universe - reconstructed)}, "
            f"extra={len(reconstructed - universe)}"
        )

    assertion_count = (
        len(domain) + len(residual) + len(cell_assertions) + 1701 * 40
    )
    return {
        "cell": name,
        "formula": str(path.resolve()),
        "formula_sha256": sha256(path),
        "lean_semantic_spec": cell["lean_spec"],
        "command_count": len(commands),
        "assertion_count": assertion_count,
        "category_counts": {
            "domain": len(domain),
            "residual": len(residual),
            "ranking_and_stabilizer": len(cell_assertions),
            "edge_definitions": 1701 * 16,
            "matching_obstructions": 1701 * 24,
        },
        "partition_count": len(reconstructed),
        "partition_count_by_shape": dict(sorted(shape_counts.items())),
        "all_24_matchings_checked_per_partition": True,
        "passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        required=True,
        help="certification root containing independent-formulas/",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--lean-root",
        type=Path,
        default=(
            Path(__file__).resolve().parents[2]
            / "formal"
            / "efx48"
        ),
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output = (
        args.output.resolve()
        if args.output
        else root / "independent-generator-audit" / "semantic-binding.json"
    )
    universe = all_bruteforce_partitions()
    if len(universe) != 1701:
        raise AuditError(
            f"brute-force partition universe has {len(universe)} elements"
        )

    records = []
    for name in CELLS:
        path = root / "independent-formulas" / f"{name}.independent.smt2"
        records.append(audit_formula(path, name, universe))
    lean_constant_binding = audit_lean_constants(
        args.lean_root.resolve()
    )

    payload = {
        "schema": "independent-formula-semantic-binding-v1",
        "meaning": (
            "Parser-based, generator-independent binding of every exact "
            "SMT assertion to the semantic terminal-cell components "
            "formalized in EFX48.TerminalCells"
        ),
        "checker": str(Path(__file__).resolve()),
        "checker_sha256": sha256(Path(__file__)),
        "all_passed": all(record["passed"] for record in records),
        "cell_count": len(records),
        "partition_universe_count": len(universe),
        "lean_constant_binding": lean_constant_binding,
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
