#!/usr/bin/env python3
"""Symbolically audit the charity/minimum exchange inequalities."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "charity-minimum-swap-audit-v1"


def threshold(core_total, core_minimum, token):
    return core_total + token - z3.If(token <= core_minimum, token, core_minimum)


def prove_unsat(name, constraints):
    solver = z3.Solver()
    solver.add(*constraints)
    verdict = solver.check()
    if verdict != z3.unsat:
        raise AssertionError(f"{name} audit returned {verdict}")
    return {"claim": name, "verdict": str(verdict)}


def run(output: Path) -> dict:
    if output.exists():
        raise ValueError("output already exists")
    core, core_minimum, incoming, released, own, charity, target = z3.Reals(
        "core core_minimum incoming released own charity target"
    )
    positive = [
        core > 0,
        core_minimum > 0,
        incoming > 0,
        released > 0,
        own > 0,
        charity >= 0,
        core >= core_minimum,
    ]
    claims = [
        prove_unsat(
            "plateau_gain_nonnegative",
            positive
            + [incoming - z3.If(incoming <= core_minimum, incoming, core_minimum) < 0],
        ),
        prove_unsat(
            "plateau_equality_makes_incoming_a_minimum",
            positive
            + [
                incoming
                - z3.If(incoming <= core_minimum, incoming, core_minimum)
                == 0,
                incoming > core_minimum,
            ],
        ),
        prove_unsat(
            "incoming_target_wall_forces_incoming_above_released",
            positive
            + [
                own >= threshold(core, core_minimum, released),
                own < threshold(core, core_minimum, incoming),
                incoming <= released,
            ],
        ),
        prove_unsat(
            "external_charity_wall_forces_released_above_incoming",
            positive
            + [
                own >= charity + incoming,
                own < charity + released,
                released <= incoming,
            ],
        ),
        prove_unsat(
            "source_efx_wall_forces_released_above_incoming",
            positive
            + [
                core + released >= target,
                core + incoming < target,
                released <= incoming,
            ],
        ),
        prove_unsat(
            "source_charity_wall_forces_released_above_incoming",
            positive
            + [
                core + released >= charity + incoming,
                core + incoming < charity + released,
                released <= incoming,
            ],
        ),
        prove_unsat(
            "old_efx_makes_released_good_unenvied_for_nonsingleton_source",
            positive
            + [
                own >= threshold(core, core_minimum, released),
                own < released,
            ],
        ),
    ]
    result = {
        "schema": SCHEMA,
        "status": "ALL_SYMBOLIC_IMPLICATIONS_UNSAT",
        "meaning": (
            "QF_LRA audits of every algebraic implication in the "
            "charity/minimum exchange and one-floater obstruction lemmas."
        ),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "claim_count": len(claims),
        "claims": claims,
        "claim_boundary": (
            "The audit verifies local inequalities, not existence of an "
            "eligible simultaneous exchange cycle."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
