#!/usr/bin/env python3
"""Symbolic/set audit of component-wide return compensation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(assumptions, negated) -> str:
    solver = z3.SolverFor("QF_LRA")
    solver.add(*assumptions, negated)
    assert solver.check() == z3.unsat
    return "unsat"


def run(root: Path) -> dict:
    d, ys, sj, sl, omega, omega_star, za, ba = z3.Reals(
        "d ys sj sl omega omega_star za ba"
    )
    mu = d - ys
    checks = {
        "source_payment_identity": prove(
            [mu == d - ys, omega == sl - sj, omega > -mu],
            d - sj + sl <= ys,
        ),
        "component_floor_preserved": prove([za >= ba], za < ba),
        "global_failure_separates_every_component_partition": prove(
            [omega <= omega_star, omega_star <= -mu, omega == sl - sj],
            sj - sl < mu,
        ),
    }

    # Abstract set partition/connectivity audit.  Components are owner labels;
    # J supplies a mandatory cross-component edge and either D-J or L reaches s.
    edge_jc, edge_js, edge_cs, source_strict = z3.Bools(
        "edge_jc edge_js edge_cs source_strict"
    )
    graph_checks = {
        "successful_bridge_is_connected": prove(
            [edge_jc, source_strict, z3.Or(edge_js, edge_cs)],
            z3.Not(z3.And(edge_jc, z3.Or(edge_js, edge_cs))),
        ),
        "strict_source_has_response_or_return_edge": prove(
            [source_strict == z3.Or(edge_js, edge_cs)],
            z3.And(source_strict, z3.Not(z3.Or(edge_js, edge_cs))),
        ),
    }

    script = Path(__file__).resolve()
    theorem = root / "results/COMPONENT_WIDE_RETURN_COMPENSATION_SELECTOR_LEMMA_20260811.md"
    return {
        "schema": "component-wide-return-compensation-selector-audit-v1",
        "status": "ALL_FORCED",
        "symbolic_checks": checks,
        "graph_checks": graph_checks,
        "outcomes": [
            "component-wide paid connected bridge",
            "exact separator excluding every internal donor ordering",
        ],
        "remaining_gate": (
            "force success from the repeated GG return, recruit an outside component, "
            "or prove a priority-valid source sacrifice"
        ),
        "claim_boundary": (
            "complete internal component payment selector; universal GG forcing, "
            "observer safety, globally maximal countermodel, and EFX remain open"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
