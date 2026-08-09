#!/usr/bin/env python3
"""Audit the cvc5 SAT model for the 524-rival split-packet master."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path

import z3

try:
    from .run_alternating_split_packet_cegar import (
        BASE_OWNER,
        concrete_rival_blocker,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )
except ImportError:
    from run_alternating_split_packet_cegar import (
        BASE_OWNER,
        concrete_rival_blocker,
        numeric_efx,
        numeric_utilities,
        structural_solver,
    )


SCHEMA = "alternating-split-packet-cvc5-model-audit-v1"
ORIGINAL_POOL_SIZE = 524


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_fraction(raw: str) -> Fraction:
    raw = raw.strip()
    if re.fullmatch(r"-?\d+", raw):
        return Fraction(int(raw), 1)
    quotient = re.fullmatch(r"\(/ (-?\d+) (\d+)\)", raw)
    if quotient:
        return Fraction(int(quotient.group(1)), int(quotient.group(2)))
    negative = re.fullmatch(r"\(- \(/ (\d+) (\d+)\)\)", raw)
    if negative:
        return -Fraction(int(negative.group(1)), int(negative.group(2)))
    raise ValueError(f"unsupported cvc5 rational: {raw}")


def integerize(raw_values: dict[str, str]) -> tuple[tuple[int, ...], ...]:
    rows = []
    for agent in range(4):
        row = tuple(parse_fraction(raw_values[f"u_{agent}_{good}"]) for good in range(11))
        denominator = math.lcm(*(entry.denominator for entry in row))
        integers = tuple(int(entry * denominator) for entry in row)
        divisor = math.gcd(*integers)
        rows.append(tuple(entry // divisor for entry in integers))
    return tuple(rows)


def audit(model_path: Path, pool_path: Path) -> dict:
    model_payload = json.loads(model_path.read_text())
    pool_payload = json.loads(pool_path.read_text())
    if model_payload.get("status") != "sat":
        raise AssertionError("the recorded cvc5 endpoint is not SAT")
    if len(pool_payload.get("rivals", [])) != 588:
        raise AssertionError("expected the augmented 588-rival pool")
    order = tuple(pool_payload["agent_order"])
    original = [tuple(owner) for owner in pool_payload["rivals"][:ORIGINAL_POOL_SIZE]]
    discovered = [tuple(owner) for owner in pool_payload["rivals"][ORIGINAL_POOL_SIZE:]]
    if len(discovered) != 64 or len(set(original + discovered)) != 588:
        raise AssertionError("the original/new rival partition is malformed")

    values = integerize(model_payload["values"])
    solver, symbolic_values, own = structural_solver()
    for owner in original:
        solver.add(concrete_rival_blocker(symbolic_values, own, owner, order))
    for agent in range(4):
        total = sum(values[agent])
        for good in range(11):
            solver.add(
                symbolic_values[agent][good]
                == z3.RealVal(values[agent][good]) / total
            )
    pinned_original_status = str(solver.check())
    if pinned_original_status != "sat":
        raise AssertionError(("pinned original master", pinned_original_status))

    base_utility = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base_utility[agent] for agent in order)
    rival_records = []
    for owner in discovered:
        if not numeric_efx(values, owner):
            raise AssertionError(("new rival is not EFX", owner))
        utility = numeric_utilities(values, owner)
        key = tuple(utility[agent] for agent in order)
        if key <= base_key:
            raise AssertionError(("new rival does not lex-dominate", owner))
        rival_records.append(
            {"owner_by_good": list(owner), "utilities": list(utility)}
        )

    augmented = z3.SolverFor("QF_LRA")
    augmented.add(*solver.assertions())
    for owner in discovered:
        augmented.add(
            concrete_rival_blocker(symbolic_values, own, owner, order)
        )
    pinned_augmented_status = str(augmented.check())
    if pinned_augmented_status != "unsat":
        raise AssertionError(("pinned augmented master", pinned_augmented_status))

    return {
        "schema": SCHEMA,
        "status": "CVC5_SAT_MODEL_REPLAYED_AND_64_NEW_RIVALS_VERIFIED",
        "claim_boundary": {
            "proved": "the 524-rival master was SAT and its model has at least 64 further exact EFX lexicographic dominators",
            "not_proved": "SAT or UNSAT of the augmented 588-rival master, or the arbitrary-packet alternating lemma",
        },
        "agent_order": list(order),
        "integerized_values": [list(row) for row in values],
        "original_pool_size": len(original),
        "augmented_pool_size": len(original) + len(discovered),
        "new_rival_count": len(discovered),
        "pinned_original_master_status": pinned_original_status,
        "pinned_augmented_master_status": pinned_augmented_status,
        "new_rivals": rival_records,
        "solvers": {
            "source": model_payload["solver"],
            "audit": {"name": "z3", "version": z3.get_version_string()},
        },
        "original_formula_hashes": {
            "z3_smt2_sha256": "d7206a58dcfc0e68fd7920dba9cddb1f81e578a702952ff18d95875c5a02cac6",
            "cvc5_normalized_smt2_sha256": "ae988f2016f0f2c4babd51156c0e938297ea174b57166e057bcca914ce7f332d",
        },
        "provenance": {
            "model_path": str(model_path.resolve()),
            "model_sha256": sha256(model_path),
            "augmented_pool_path": str(pool_path.resolve()),
            "augmented_pool_sha256": sha256(pool_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.model, args.pool)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload)


if __name__ == "__main__":
    main()
