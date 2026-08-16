#!/usr/bin/env python3
"""Audit the floater-substitution preference-path improvement lemma."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

import z3

try:
    from . import core, independent
    from .anneal import atomic_json
except ImportError:
    import core
    import independent
    from anneal import atomic_json


SCHEMA = "floater-substitution-cycle-lemma-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbolic_checks() -> tuple[dict, tuple[str, str]]:
    old_own, new_own, old_target, old_own_remainder = z3.Reals(
        "old_own new_own old_target old_own_remainder"
    )
    rest, old_r, floater, old_other = z3.Reals(
        "rest old_r floater old_other"
    )
    receiver_new = z3.Real("receiver_new")
    weak = z3.SolverFor("QF_LRA")
    weak.add(
        old_own > 0,
        new_own >= old_own,
        old_target <= old_own,
        old_own_remainder <= old_own,
        rest >= 0,
        old_r >= 0,
        floater >= 0,
        old_other >= 0,
        floater <= old_r,
        old_own >= rest + old_other,
        old_own >= rest + old_r,
        receiver_new > old_own,
        receiver_new >= floater,
        z3.Or(
            new_own < old_target,
            new_own < old_own_remainder,
            new_own < rest + old_other,
            new_own < rest + floater,
            receiver_new < old_target,
            receiver_new < old_own_remainder,
            receiver_new < old_r,
        ),
    )
    weak_status = str(weak.check())
    if weak_status != "unsat":
        raise AssertionError("substitution-cycle EFX implication failed")

    old = z3.Reals("sub_old_0 sub_old_1 sub_old_2 sub_old_3")
    new = z3.Reals("sub_new_0 sub_new_1 sub_new_2 sub_new_3")
    nash = z3.SolverFor("QF_NRA")
    nash.add(
        *(utility > 0 for utility in old),
        *(new[index] >= old[index] for index in range(4)),
        z3.Or(*(new[index] > old[index] for index in range(4))),
        z3.Not(z3.Product(*new) > z3.Product(*old)),
    )
    nash_status = str(nash.check())
    if nash_status != "unsat":
        raise AssertionError("substitution-cycle Nash implication failed")

    return (
        {
            "negated_efx_and_floater_conclusion_status": weak_status,
            "negated_strict_nash_conclusion_status": nash_status,
            "solver": {
                "name": "z3",
                "version": z3.get_version_string(),
                "logics": ["QF_LRA", "QF_NRA"],
            },
        },
        (weak.to_smt2(), nash.to_smt2()),
    )


def value(
    values: tuple[tuple[int, ...], ...],
    observer: int,
    bundle: tuple[int, ...] | list[int],
) -> int:
    return sum(values[observer][good] for good in bundle)


def paths(n: int, start: int, end: int) -> tuple[tuple[int, ...], ...]:
    middle = tuple(agent for agent in range(n) if agent not in {start, end})
    return tuple(
        (start, *inside, end)
        for length in range(len(middle) + 1)
        for inside in itertools.permutations(middle, length)
    )


def rotated_owner(
    bundles: tuple[tuple[int, ...], ...],
    floater: int,
    removed: int,
    path: tuple[int, ...],
    m: int,
) -> tuple[int | None, ...]:
    new_bundles = [tuple(bundle) for bundle in bundles]
    host = path[0]
    receiver = path[-1]
    for index in range(len(path) - 1):
        new_bundles[path[index]] = bundles[path[index + 1]]
    new_bundles[receiver] = tuple(
        good for good in bundles[host] if good != removed
    ) + (floater,)
    owner: list[int | None] = [None] * m
    for agent, bundle in enumerate(new_bundles):
        for good in bundle:
            if owner[good] is not None:
                raise AssertionError("substitution bundles overlap")
            owner[good] = agent
    if owner[removed] is not None or any(
        assigned is None for good, assigned in enumerate(owner) if good != removed
    ):
        raise AssertionError("substitution did not allocate exactly m-1 goods")
    return tuple(owner)


def audit_profiles(
    profiles: tuple[tuple[tuple[int, ...], ...], ...],
    *,
    label: str,
) -> dict:
    eligible_base_count = 0
    premise_path_count = 0
    path_length_counts: dict[int, int] = {}
    n = len(profiles[0])
    m = len(profiles[0][0])
    for values in profiles:
        for floater in range(m):
            for base in core.iter_efx_bases(values, floater):
                old_utilities = tuple(base["own_values"])
                if not all(
                    old_utilities[agent] >= values[agent][floater]
                    for agent in range(n)
                ):
                    continue
                eligible_base_count += 1
                bundles = tuple(tuple(bundle) for bundle in base["bundles"])
                for host, host_bundle in enumerate(bundles):
                    if len(host_bundle) < 2:
                        continue
                    for removed in host_bundle:
                        supporters = tuple(
                            agent
                            for agent in range(n)
                            if values[agent][floater] > values[agent][removed]
                        )
                        if len(supporters) != 1 or supporters[0] == host:
                            continue
                        receiver = supporters[0]
                        modified = tuple(
                            good for good in host_bundle if good != removed
                        ) + (floater,)
                        if value(values, receiver, modified) <= old_utilities[receiver]:
                            continue
                        for path in paths(n, host, receiver):
                            if any(
                                value(values, path[index], bundles[path[index + 1]])
                                < old_utilities[path[index]]
                                for index in range(len(path) - 1)
                            ):
                                continue
                            premise_path_count += 1
                            path_length = len(path) - 1
                            path_length_counts[path_length] = (
                                path_length_counts.get(path_length, 0) + 1
                            )
                            owner = rotated_owner(
                                bundles,
                                floater,
                                removed,
                                path,
                                m,
                            )
                            if not independent.is_removed_good_efx0(
                                values,
                                owner,
                                removed,
                            ):
                                raise AssertionError(
                                    (
                                        label,
                                        values,
                                        floater,
                                        base["base_owner"],
                                        removed,
                                        path,
                                        "EFX",
                                    )
                                )
                            new_utilities = tuple(
                                value(
                                    values,
                                    agent,
                                    tuple(
                                        good
                                        for good, assigned in enumerate(owner)
                                        if assigned == agent
                                    ),
                                )
                                for agent in range(n)
                            )
                            if any(
                                new_utilities[agent] < values[agent][removed]
                                for agent in range(n)
                            ):
                                raise AssertionError("new floater became envied")
                            old_nash = new_nash = 1
                            for old_utility, new_utility in zip(
                                old_utilities, new_utilities
                            ):
                                old_nash *= old_utility
                                new_nash *= new_utility
                            if new_nash <= old_nash:
                                raise AssertionError(
                                    "substitution path failed strict Nash increase"
                                )
    if not premise_path_count:
        raise AssertionError(f"{label} did not exercise the lemma")
    return {
        "label": label,
        "n": n,
        "m": m,
        "profile_count": len(profiles),
        "eligible_base_count": eligible_base_count,
        "premise_path_count": premise_path_count,
        "path_length_counts": {
            str(length): count
            for length, count in sorted(path_length_counts.items())
        },
    }


def literal_audits() -> list[dict]:
    binary_2x4 = tuple(
        tuple(
            tuple(flat[agent * 4:(agent + 1) * 4])
            for agent in range(2)
        )
        for flat in itertools.product((1, 2), repeat=8)
    )
    rng = random.Random(20260801)
    sampled_3x5 = tuple(
        tuple(
            tuple(rng.randrange(1, 5) for _ in range(5))
            for _ in range(3)
        )
        for _ in range(1024)
    )
    return [
        audit_profiles(binary_2x4, label="exhaustive_binary_2x4"),
        audit_profiles(sampled_3x5, label="deterministic_sample_3x5"),
    ]


def run(
    output: Path,
    weak_smt2: Path,
    nash_smt2: Path,
) -> dict:
    symbolic, formulas = symbolic_checks()
    paths_out = (weak_smt2, nash_smt2)
    for path, formula in zip(paths_out, formulas):
        path.write_text(formula)
    result = {
        "schema": SCHEMA,
        "status": "PROVED_FLOATER_SUBSTITUTION_PREFERENCE_PATH_LEMMA",
        "lemma": (
            "Replace r in host bundle X_h by floater f. If exactly one agent "
            "i ranks f above r, i strictly prefers the modified host bundle, "
            "and the original weak bundle-preference graph has a simple path "
            "from h to i, rotate bundles along that path and give the modified "
            "bundle to i. The resulting one-floater state is EFX and eligible "
            "and has strictly larger Nash welfare."
        ),
        "corollary": (
            "At a maximum-Nash eligible state, a source-host blocker with a "
            "unique floater supporter cannot be reachable from the source in "
            "the weak bundle-preference graph."
        ),
        "symbolic": symbolic,
        "literal_audits": literal_audits(),
        "formulas": [
            {"path": path.name, "sha256": sha256(path)}
            for path in paths_out
        ],
        "claim_boundary": (
            "The remaining case has either multiple floater supporters or a "
            "unique supporter separated from the source by weak-preference "
            "reachability; the lemma does not eliminate those cases."
        ),
    }
    atomic_json(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--weak-smt2", type=Path, required=True)
    parser.add_argument("--nash-smt2", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.output, args.weak_smt2, args.nash_smt2)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
