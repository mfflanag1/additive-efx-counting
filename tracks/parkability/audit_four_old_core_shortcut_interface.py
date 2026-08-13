#!/usr/bin/env python3
"""Audit the four-old-core shortcut and the frozen local witnesses."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path

import z3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prove(premises: list[z3.BoolRef], conclusion: z3.BoolRef) -> bool:
    solver = z3.Solver()
    solver.add(*premises, z3.Not(conclusion))
    return solver.check() == z3.unsat


def load_referee(root: Path):
    source = root / "tracks/parkability/audit_closing_source_deletion_return_referee.py"
    spec = importlib.util.spec_from_file_location("closing_referee", source)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay(payload: dict) -> dict:
    agents = ("t", "u", "s", "w")
    rows = {
        agent: {good: Fraction(number) for good, number in row.items()}
        for agent, row in payload["valuations"].items()
    }
    base = (
        {agent: frozenset(bundle) for agent, bundle in payload["base"].items()}
        if "base" in payload
        else {
            "t": frozenset({"x0"}), "u": frozenset({"x1"}),
            "s": frozenset({"x2"}), "w": frozenset({"x3"}),
        }
    )
    cores = (
        {agent: frozenset(bundle) for agent, bundle in payload["old_cores"].items()}
        if "old_cores" in payload
        else {
            "t": frozenset({"a0"}), "u": frozenset({"a1"}),
            "s": frozenset({"a2"}), "w": frozenset({"a3"}),
        }
    )

    def value(agent: str, bundle: frozenset[str]) -> Fraction:
        return sum((rows[agent][good] for good in bundle), Fraction(0))

    def threshold(agent: str, bundle: frozenset[str]) -> Fraction:
        if len(bundle) <= 1:
            return Fraction(0)
        return value(agent, bundle) - min(rows[agent][good] for good in bundle)

    disjoint = all(
        left.isdisjoint(right)
        for index, left in enumerate(cores.values())
        for right in list(cores.values())[index + 1 :]
    )
    desired = all(value(agent, cores[agent]) > value(agent, base[agent]) for agent in agents)
    common_safe = all(
        threshold(observer, cores[target]) <= value(observer, base[observer])
        for observer in agents for target in agents
    )
    efx = all(
        value(observer, cores[observer]) >= threshold(observer, cores[target])
        for observer in agents for target in agents if observer != target
    )
    pareto = desired
    assert disjoint and desired and common_safe and efx and pareto
    return {
        "shortcut_allocation": {agent: sorted(bundle) for agent, bundle in cores.items()},
        "utilities": {agent: str(value(agent, cores[agent])) for agent in agents},
        "base_utilities": {agent: str(value(agent, base[agent])) for agent in agents},
        "pairwise_disjoint": disjoint,
        "all_desired": desired,
        "base_common_safe": common_safe,
        "efx": efx,
        "pareto_improves_all_owners": pareto,
    }


def run(root: Path) -> dict:
    own, base, debt = z3.Reals("own base debt")
    symbolic = {
        "desired_plus_base_safety_implies_efx_row": prove(
            [own > base, debt <= base], own >= debt
        ),
        "desired_implies_strict_lex_coordinate": prove([own > base], own > base),
    }
    assert all(symbolic.values())
    referee = load_referee(root)
    replays = {
        "first": replay(referee.rational_witness()),
        "trimmed": replay(referee.trimmed_rational_witness()),
    }
    manuscript = root / "results/CLOSING_SOURCE_DELETION_RETURN_RESIDUAL_COMPLETION_LEMMA_20260811.md"
    text = manuscript.read_text()
    asserted_phrases = {
        "four_source_path_cores": "For each source `i`, let `A_i`" in text,
        "all_base_common_safe_desired": "All `A_i,C_i` are base-common-safe desired cores" in text,
        "distinct_matching_targets": "distinct matched target" in text,
    }
    assert all(asserted_phrases.values())
    script = Path(__file__).resolve()
    theorem = root / "results/FOUR_OLD_CORE_SHORTCUT_AND_INTERFACE_REFUTATION_20260813.md"
    return {
        "schema": "four-old-core-shortcut-interface-audit-v1",
        "status": "STATED_SPLICE_NORMAL_FORM_VACUOUS",
        "symbolic_checks": symbolic,
        "manuscript_premises_detected": asserted_phrases,
        "frozen_local_witness_shortcuts": replays,
        "required_interface_correction": (
            "identify the one mixed current-safe edge and retain only the "
            "simultaneously physical old cores, or specify exact generalized-edge overlaps"
        ),
        "claim_boundary": (
            "logical inconsistency of the stated local/global premises; no GG "
            "closure or general EFX theorem"
        ),
        "provenance": {
            "z3_version": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "manuscript": str(manuscript.relative_to(root)),
            "manuscript_sha256": sha256(manuscript),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "correction": result["required_interface_correction"]}, indent=2))


if __name__ == "__main__":
    main()
