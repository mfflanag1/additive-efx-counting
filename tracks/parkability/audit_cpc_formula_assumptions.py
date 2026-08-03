#!/usr/bin/env python3
"""Bind each SMT assertion to the permanent assumptions in its CPC proof.

The audit is deliberately independent of cvc5.  It parses the emitted SMT-LIB
assertions and the initial, top-level CPC assumption block, expands the CPC term
DAG by structural hashing, and requires an ordered one-to-one match.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path


CELLS = (
    "favorite-211",
    "favorite-31",
    "favorite-22",
    "top4-second1111",
    "top4-second4",
    "top4-second31",
    "top4-second22",
    "top4-second211",
)

TOKEN = re.compile(r"\(|\)|[^\s()]+")
INTEGER = re.compile(r"-?\d+")
RATIONAL = re.compile(r"(-?\d+)/(\d+)")


class AuditError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
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


def rational_atom(numerator: int, denominator: int) -> str:
    if denominator == 0:
        raise AuditError("zero rational denominator")
    if denominator < 0:
        numerator = -numerator
        denominator = -denominator
    divisor = math.gcd(abs(numerator), denominator)
    numerator //= divisor
    denominator //= divisor
    if denominator == 1:
        return str(numerator)
    return f"{numerator}/{denominator}"


def normalized_numeric(node) -> str | None:
    if isinstance(node, str):
        if INTEGER.fullmatch(node):
            return str(int(node))
        match = RATIONAL.fullmatch(node)
        if match:
            return rational_atom(int(match.group(1)), int(match.group(2)))
        return None
    if (
        isinstance(node, tuple)
        and len(node) == 2
        and node[0] == "-"
    ):
        value = normalized_numeric(node[1])
        if value is not None:
            match = RATIONAL.fullmatch(value)
            if match:
                return rational_atom(-int(match.group(1)), int(match.group(2)))
            return str(-int(value))
    if (
        isinstance(node, tuple)
        and len(node) == 3
        and node[0] == "/"
    ):
        numerator = normalized_numeric(node[1])
        denominator = normalized_numeric(node[2])
        if (
            numerator is not None
            and denominator is not None
            and "/" not in numerator
            and "/" not in denominator
        ):
            return rational_atom(int(numerator), int(denominator))
    return None


def structural_digest(node, definitions: dict[str, bytes]) -> bytes:
    numeric = normalized_numeric(node)
    if numeric is not None:
        return hashlib.sha256(b"N" + numeric.encode()).digest()
    if isinstance(node, str):
        if node.startswith("@t"):
            try:
                return definitions[node]
            except KeyError as error:
                raise AuditError(f"undefined CPC term reference: {node}") from error
        return hashlib.sha256(b"A" + node.encode()).digest()
    digest = hashlib.sha256()
    digest.update(b"(")
    for child in node:
        child_digest = structural_digest(child, definitions)
        digest.update(len(child_digest).to_bytes(2, "big"))
        digest.update(child_digest)
    digest.update(b")")
    return digest.digest()


def read_formula_assertions(path: Path) -> list[bytes]:
    assertions = []
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.startswith("(assert"):
                continue
            command = parse_sexpr(line)
            if (
                not isinstance(command, tuple)
                or len(command) != 2
                or command[0] != "assert"
            ):
                raise AuditError(f"{path}:{line_number}: malformed assertion")
            assertions.append(structural_digest(command[1], {}))
    return assertions


def read_permanent_cpc_assumptions(
    path: Path,
) -> tuple[list[bytes], int]:
    definitions: dict[str, bytes] = {}
    assumptions = []
    assumption_block_started = False
    with path.open() as handle:
        for line_number, line in enumerate(handle, 1):
            if line.startswith("(define @t"):
                if assumption_block_started:
                    raise AuditError(
                        f"{path}:{line_number}: definition inside assumption block"
                    )
                command = parse_sexpr(line)
                if (
                    not isinstance(command, tuple)
                    or len(command) != 4
                    or command[0] != "define"
                    or command[2] != ()
                    or not isinstance(command[1], str)
                ):
                    raise AuditError(
                        f"{path}:{line_number}: malformed term definition"
                    )
                definitions[command[1]] = structural_digest(
                    command[3],
                    definitions,
                )
                continue
            if line.startswith("(assume "):
                assumption_block_started = True
                command = parse_sexpr(line)
                if (
                    not isinstance(command, tuple)
                    or len(command) != 3
                    or command[0] != "assume"
                ):
                    raise AuditError(f"{path}:{line_number}: malformed assumption")
                assumptions.append(
                    structural_digest(command[2], definitions)
                )
                continue
            if assumption_block_started:
                break
    if not assumption_block_started:
        raise AuditError(f"{path}: no permanent assumption block")
    return assumptions, len(definitions)


def audit_cell(root: Path, cell: str) -> dict:
    formula = root / "independent-formulas" / f"{cell}.independent.smt2"
    proof = root / "proofs" / f"{cell}.independent.cpc"
    if not formula.is_file() or not proof.is_file():
        raise AuditError(f"{cell}: missing formula or proof")

    assertions = read_formula_assertions(formula)
    assumptions, definition_count = read_permanent_cpc_assumptions(proof)
    mismatch_indices = [
        index
        for index, (assertion, assumption) in enumerate(
            zip(assertions, assumptions),
            1,
        )
        if assertion != assumption
    ]
    if len(assertions) != len(assumptions):
        raise AuditError(
            f"{cell}: {len(assertions)} assertions but "
            f"{len(assumptions)} permanent assumptions"
        )
    if mismatch_indices:
        raise AuditError(
            f"{cell}: {len(mismatch_indices)} ordered assumption mismatches; "
            f"first at assertion {mismatch_indices[0]}"
        )
    return {
        "cell": cell,
        "formula": str(formula.relative_to(root)),
        "formula_sha256": sha256(formula),
        "proof": str(proof.relative_to(root)),
        "proof_sha256": sha256(proof),
        "term_definition_count": definition_count,
        "formula_assertion_count": len(assertions),
        "permanent_cpc_assumption_count": len(assumptions),
        "ordered_mismatch_count": 0,
        "passed": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    cells = [audit_cell(root, cell) for cell in CELLS]
    report = {
        "schema": "efx48-cpc-formula-assumption-audit-v1",
        "method": (
            "Independent S-expression parsing and ordered structural hashing "
            "after expansion of the CPC @t term DAG"
        ),
        "cell_count": len(cells),
        "formula_assertion_count": sum(
            cell["formula_assertion_count"] for cell in cells
        ),
        "permanent_cpc_assumption_count": sum(
            cell["permanent_cpc_assumption_count"] for cell in cells
        ),
        "ordered_mismatch_count": 0,
        "all_passed": True,
        "cells": cells,
    }
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
