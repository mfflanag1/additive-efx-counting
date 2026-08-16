#!/usr/bin/env python3
"""Symbolic and literal audit of the safe floater-exchange lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
except ImportError:
    import core
    import independent
    from anneal import atomic_json


SCHEMA = "safe-floater-exchange-lemma-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbolic_checks() -> tuple[dict, str, str]:
    host_rest, host_f, host_r = z3.Reals("host_rest host_f host_r")
    other_own, other_rest, other_g = z3.Reals(
        "other_own other_rest other_g"
    )
    other_f, other_r = z3.Reals("other_f other_r")
    target_threshold = z3.Real("target_threshold")

    old_host = host_rest + host_r
    new_host = host_rest + host_f
    weak_premises = (
        host_rest >= 0,
        host_f >= 0,
        host_r >= 0,
        other_own >= 0,
        other_rest >= 0,
        other_g >= 0,
        other_f >= 0,
        other_r >= 0,
        target_threshold >= 0,
        host_f >= host_r,
        other_f <= other_r,
        other_own >= other_rest + other_g,
        other_own >= other_rest + other_r,
        old_host >= target_threshold,
    )
    weak_conclusions = {
        "host_weakly_improves": new_host >= old_host,
        "host_does_not_envy_new_floater": new_host >= host_r,
        "other_observer_remove_new_floater": (
            other_own >= other_rest + other_g
        ),
        "other_observer_remove_old_good": (
            other_own >= other_rest + other_f
        ),
        "other_observer_does_not_envy_new_floater": other_own >= other_r,
        "host_retains_old_target_inequality": new_host >= target_threshold,
    }
    weak = z3.SolverFor("QF_LRA")
    weak.add(*weak_premises)
    if weak.check() != z3.sat:
        raise AssertionError("weak exchange premises are inconsistent")
    weak.add(z3.Or(*(z3.Not(item) for item in weak_conclusions.values())))
    weak_status = str(weak.check())
    if weak_status != "unsat":
        raise AssertionError("a weak exchange conclusion was not proved")

    other_utilities = z3.Reals("other_utility_1 other_utility_2 other_utility_3")
    strict = z3.SolverFor("QF_NRA")
    strict.add(
        host_rest >= 0,
        host_r > 0,
        host_f > host_r,
        *(utility > 0 for utility in other_utilities),
    )
    old_nash = old_host * z3.Product(*other_utilities)
    new_nash = new_host * z3.Product(*other_utilities)
    strict.add(z3.Not(new_nash > old_nash))
    strict_status = str(strict.check())
    if strict_status != "unsat":
        raise AssertionError("strict Nash increase was not proved")

    return (
        {
            "weak_premise_status": "sat",
            "negated_weak_conclusion_status": weak_status,
            "weak_conclusions": list(weak_conclusions),
            "negated_strict_nash_conclusion_status": strict_status,
            "solver": {
                "name": "z3",
                "version": z3.get_version_string(),
                "weak_logic": "QF_LRA",
                "strict_logic": "QF_NRA",
            },
        },
        weak.to_smt2(),
        strict.to_smt2(),
    )


def own_value(
    values: tuple[tuple[int, ...], ...],
    owner: tuple[int | None, ...],
    agent: int,
) -> int:
    return sum(
        values[agent][good]
        for good, assigned in enumerate(owner)
        if assigned == agent
    )


def exhaustive_literal_audit() -> dict:
    n = 2
    m = 4
    profile_count = 0
    eligible_base_count = 0
    premise_exchange_count = 0
    strict_exchange_count = 0
    for flat in itertools.product((1, 2), repeat=n * m):
        values = tuple(
            tuple(flat[agent * m:(agent + 1) * m])
            for agent in range(n)
        )
        profile_count += 1
        for floater in range(m):
            for base in core.iter_efx_bases(values, floater):
                owner = tuple(base["base_owner"])
                if not all(
                    base["own_values"][agent] >= values[agent][floater]
                    for agent in range(n)
                ):
                    continue
                eligible_base_count += 1
                for host, bundle in enumerate(base["bundles"]):
                    if len(bundle) < 2:
                        continue
                    for removed in bundle:
                        if values[host][floater] < values[host][removed]:
                            continue
                        if any(
                            values[agent][floater] > values[agent][removed]
                            for agent in range(n)
                            if agent != host
                        ):
                            continue
                        premise_exchange_count += 1
                        exchanged = list(owner)
                        exchanged[floater] = host
                        exchanged[removed] = None
                        if not independent.is_removed_good_efx0(
                            values,
                            exchanged,
                            removed,
                        ):
                            raise AssertionError(
                                (values, floater, owner, host, removed, "EFX")
                            )
                        new_utilities = tuple(
                            own_value(values, tuple(exchanged), agent)
                            for agent in range(n)
                        )
                        if any(
                            new_utilities[agent] < values[agent][removed]
                            for agent in range(n)
                        ):
                            raise AssertionError(
                                (
                                    values,
                                    floater,
                                    owner,
                                    host,
                                    removed,
                                    "floater nonenvy",
                                )
                            )
                        old_nash = 1
                        new_nash = 1
                        for old_utility, new_utility in zip(
                            base["own_values"], new_utilities
                        ):
                            old_nash *= old_utility
                            new_nash *= new_utility
                        if new_nash < old_nash:
                            raise AssertionError("safe exchange reduced Nash welfare")
                        if values[host][floater] > values[host][removed]:
                            strict_exchange_count += 1
                            if new_nash <= old_nash:
                                raise AssertionError(
                                    "strict safe exchange failed to increase Nash"
                                )
    if not premise_exchange_count or not strict_exchange_count:
        raise AssertionError("literal grid did not exercise both exchange cases")
    return {
        "status": "EXHAUSTIVE_LITERAL_AUDIT_PASSED",
        "n": n,
        "m": m,
        "value_domain": [1, 2],
        "profile_count": profile_count,
        "eligible_base_count": eligible_base_count,
        "premise_exchange_count": premise_exchange_count,
        "strict_exchange_count": strict_exchange_count,
        "verifier": "independent literal removed-good EFX expansion",
    }


def run(output: Path, weak_smt2: Path, strict_smt2: Path) -> dict:
    symbolic, weak_formula, strict_formula = symbolic_checks()
    weak_smt2.write_text(weak_formula)
    strict_smt2.write_text(strict_formula)
    result = {
        "schema": SCHEMA,
        "status": "PROVED_SYMBOLIC_SCALAR_SCHEMA_AND_EXHAUSTIVE_LITERAL_AUDIT",
        "claim": (
            "Replacing r in a nonsingleton host bundle by floater f preserves "
            "EFX and floater nonenvy when the host weakly prefers f to r and "
            "every other agent weakly prefers r to f; a strict host preference "
            "strictly increases Nash welfare."
        ),
        "scope": (
            "The symbolic proof uses an aggregate for all untouched host goods, "
            "so it is independent of the number of goods and agents."
        ),
        "symbolic": symbolic,
        "literal": exhaustive_literal_audit(),
        "weak_smt2": weak_smt2.name,
        "weak_smt2_sha256": sha256(weak_smt2),
        "strict_smt2": strict_smt2.name,
        "strict_smt2_sha256": sha256(strict_smt2),
        "claim_boundary": (
            "This is one local exchange unit, not the covering argument needed "
            "to prove maximum-Nash completion or general complete EFX."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--weak-smt2", type=Path, required=True)
    parser.add_argument("--strict-smt2", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output, args.weak_smt2, args.strict_smt2)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
