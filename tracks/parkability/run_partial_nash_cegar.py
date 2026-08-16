#!/usr/bin/env python3
"""Exact-NRA CEGAR for a blocked maximum-Nash partial EFX state."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import time
from fractions import Fraction
from functools import reduce
from math import gcd
from operator import mul
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .anneal_lexmax_all_orders import load_values
except ImportError:
    import core
    from anneal import atomic_json
    from anneal_lexmax_all_orders import load_values


SCHEMA = "partial-nash-nra-cegar-v1"
POOL_SCHEMA = "partial-nash-rival-pool-v1"


def product(expressions):
    return reduce(mul, expressions, z3.RealVal(1))


def model_rows(model: z3.ModelRef, variables) -> tuple[tuple[int, ...], ...]:
    rows = []
    for variable_row in variables:
        fractions = []
        for variable in variable_row:
            value = model.eval(variable, model_completion=True)
            fractions.append(
                Fraction(value.as_long(), 1)
                if z3.is_int_value(value)
                else Fraction(
                    value.numerator_as_long(),
                    value.denominator_as_long(),
                )
            )
        denominator = 1
        for value in fractions:
            denominator = math.lcm(denominator, value.denominator)
        row = [int(value * denominator) for value in fractions]
        divisor = reduce(gcd, row)
        rows.append(tuple(value // divisor for value in row))
    return tuple(rows)


def bundles(base_owner: tuple[int | None, ...], n: int):
    return tuple(
        tuple(good for good, owner in enumerate(base_owner) if owner == agent)
        for agent in range(n)
    )


class NashMaster:
    def __init__(
        self,
        n: int,
        m: int,
        candidate: tuple[int, tuple[int | None, ...]],
        source_host: int | None = None,
    ) -> None:
        self.n = n
        self.m = m
        self.candidate = candidate
        self.solver = z3.SolverFor("QF_NRA")
        self.values = [
            [z3.Real(f"value_{agent}_{good}") for good in range(m)]
            for agent in range(n)
        ]
        for row in self.values:
            self.solver.add(*(value > 0 for value in row))
            self.solver.add(z3.Sum(*row) == 1)
        candidate_eligible, candidate_insertable, self.candidate_nash = (
            self.state_formulas(candidate)
        )
        self.solver.add(candidate_eligible)
        self.solver.add(z3.Not(candidate_insertable))
        self.rivals = set()
        self.bundle_cycle_cut_count = self.add_bundle_cycle_cuts()
        source_formulas = self.source_host_formulas()
        if source_host is None:
            self.solver.add(z3.Or(*source_formulas))
        else:
            if not 0 <= source_host < n:
                raise ValueError("source host is outside the agent range")
            self.solver.add(source_formulas[source_host])
        self.source_host = source_host

    def value(self, agent: int, goods: tuple[int, ...]):
        return z3.Sum(*(self.values[agent][good] for good in goods))

    def state_formulas(
        self,
        state: tuple[int, tuple[int | None, ...]],
    ):
        floater, base_owner = state
        state_bundles = bundles(base_owner, self.n)
        own = [self.value(agent, state_bundles[agent]) for agent in range(self.n)]
        eligible = []
        for observer in range(self.n):
            eligible.append(own[observer] >= self.values[observer][floater])
            for target in range(self.n):
                if observer == target:
                    continue
                for removed in state_bundles[target]:
                    remainder = tuple(
                        good for good in state_bundles[target] if good != removed
                    )
                    eligible.append(
                        own[observer] >= self.value(observer, remainder)
                    )
        host_formulas = []
        for host in range(self.n):
            enlarged = state_bundles[host] + (floater,)
            host_formulas.append(
                z3.And(
                    *(
                        own[observer]
                        >= self.value(
                            observer,
                            tuple(good for good in enlarged if good != removed),
                        )
                        for observer in range(self.n)
                        if observer != host
                        for removed in enlarged
                    )
                )
            )
        return z3.And(*eligible), z3.Or(*host_formulas), product(own)

    def add_rival(
        self,
        state: tuple[int, tuple[int | None, ...]],
    ) -> bool:
        if state in self.rivals or state == self.candidate:
            return False
        eligible, insertable, nash = self.state_formulas(state)
        self.solver.add(z3.Or(z3.Not(eligible), nash <= self.candidate_nash))
        self.solver.add(
            z3.Or(
                z3.Not(eligible),
                z3.Not(insertable),
                nash < self.candidate_nash,
            )
        )
        self.rivals.add(state)
        return True

    def candidate_bundles(self):
        return bundles(self.candidate[1], self.n)

    def source_host_formulas(self):
        candidate_bundles = self.candidate_bundles()
        own = [
            self.value(agent, candidate_bundles[agent])
            for agent in range(self.n)
        ]
        return tuple(
            z3.And(
                *(
                    own[observer]
                    >= self.value(observer, candidate_bundles[host])
                    for observer in range(self.n)
                    if observer != host
                )
            )
            for host in range(self.n)
        )

    def add_bundle_cycle_cuts(self) -> int:
        candidate_bundles = self.candidate_bundles()
        own = [
            self.value(agent, candidate_bundles[agent])
            for agent in range(self.n)
        ]
        count = 0
        for length in range(2, self.n + 1):
            for cycle in itertools.permutations(range(self.n), length):
                if cycle[0] != min(cycle):
                    continue
                successor = [
                    self.value(
                        agent,
                        candidate_bundles[cycle[(index + 1) % length]],
                    )
                    for index, agent in enumerate(cycle)
                ]
                self.solver.add(
                    z3.Not(
                        z3.And(
                            *(
                                successor[index] >= own[agent]
                                for index, agent in enumerate(cycle)
                            ),
                            z3.Or(
                                *(
                                    successor[index] > own[agent]
                                    for index, agent in enumerate(cycle)
                                )
                            ),
                        )
                    )
                )
                count += 1
        return count

    def solve(self, time_limit_s: float):
        self.solver.set(timeout=max(1, math.ceil(time_limit_s * 1000)))
        status = self.solver.check()
        if status == z3.sat:
            return "SAT", model_rows(self.solver.model(), self.values), None
        if status == z3.unsat:
            return "UNSAT", None, None
        return "UNKNOWN", None, self.solver.reason_unknown()


def state_identity(floater: int, base_owner) -> tuple[int, tuple[int | None, ...]]:
    return floater, tuple(base_owner)


def eligible_states(values: tuple[tuple[int, ...], ...]):
    states = []
    row_totals = tuple(map(sum, values))
    for floater in range(len(values[0])):
        for base in core.iter_efx_bases(values, floater):
            utilities = tuple(base["own_values"])
            if not all(
                utilities[agent] >= values[agent][floater]
                for agent in range(len(values))
            ):
                continue
            normalized_product = math.prod(
                Fraction(utilities[agent], row_totals[agent])
                for agent in range(len(values))
            )
            states.append(
                {
                    "identity": state_identity(floater, base["base_owner"]),
                    "nash": normalized_product,
                    "utilities": utilities,
                    "parkable_hosts": tuple(base["parkable_hosts"]),
                }
            )
    return states


def public_state(state):
    return {
        "floater": state[0],
        "base_owner": list(state[1]),
    }


def write_pool(
    path: Path,
    *,
    n: int,
    m: int,
    candidate: tuple[int, tuple[int | None, ...]],
    rivals,
) -> None:
    atomic_json(
        path,
        {
            "schema": POOL_SCHEMA,
            "n": n,
            "m": m,
            "candidate": public_state(candidate),
            "rivals": [
                public_state(rival) for rival in sorted(rivals, key=repr)
            ],
        },
    )


def bundle_cycle_rivals(
    candidate: tuple[int, tuple[int | None, ...]],
    n: int,
) -> tuple[tuple[int, tuple[int | None, ...]], ...]:
    floater, owner = candidate
    rivals = set()
    for length in range(2, n + 1):
        for cycle in itertools.permutations(range(n), length):
            if cycle[0] != min(cycle):
                continue
            owner_map = {
                cycle[(index + 1) % length]: cycle[index]
                for index in range(length)
            }
            rival_owner = tuple(
                None if assigned is None else owner_map.get(assigned, assigned)
                for assigned in owner
            )
            rivals.add((floater, rival_owner))
    return tuple(sorted(rivals, key=repr))


def source_substitution_rivals(
    candidate: tuple[int, tuple[int | None, ...]],
    n: int,
    source_host: int,
) -> tuple[tuple[int, tuple[int | None, ...]], ...]:
    floater, owner = candidate
    candidate_bundles = bundles(owner, n)
    if not 0 <= source_host < n:
        raise ValueError("source host is outside the agent range")
    rivals = set()
    for removed in candidate_bundles[source_host]:
        modified = list(candidate_bundles)
        modified[source_host] = tuple(
            good
            for good in candidate_bundles[source_host]
            if good != removed
        ) + (floater,)
        for permutation in itertools.permutations(range(n)):
            rival_owner: list[int | None] = [None] * len(owner)
            for agent, bundle_index in enumerate(permutation):
                for good in modified[bundle_index]:
                    rival_owner[good] = agent
            if rival_owner[removed] is not None or any(
                assigned is None
                for good, assigned in enumerate(rival_owner)
                if good != removed
            ):
                raise AssertionError("source substitution is not a partial state")
            rivals.add((removed, tuple(rival_owner)))
    return tuple(sorted(rivals, key=repr))


def load_pool(
    path: Path,
    *,
    n: int,
    m: int,
    candidate: tuple[int, tuple[int | None, ...]],
) -> tuple[tuple[int, tuple[int | None, ...]], ...]:
    document = json.loads(path.read_text())
    observed_candidate = state_identity(
        document["candidate"]["floater"],
        document["candidate"]["base_owner"],
    )
    if (
        document.get("schema") != POOL_SCHEMA
        or document.get("n") != n
        or document.get("m") != m
        or observed_candidate != candidate
    ):
        raise ValueError("resume pool does not match the fixed candidate")
    return tuple(
        state_identity(record["floater"], record["base_owner"])
        for record in document["rivals"]
    )


def seed_candidate(values: list[list[int]]):
    normalized = core.validate_values(values, lower=1)
    states = eligible_states(normalized)
    best = max(state["nash"] for state in states)
    winners = [state for state in states if state["nash"] == best]
    return winners[0]["identity"], winners


def run(
    *,
    seed_path: Path,
    result_path: Path,
    pool_path: Path,
    smt2_path: Path,
    resume_pool_path: Path | None,
    source_host: int | None,
    add_source_substitution_rivals: bool,
    add_per_iteration: int,
    max_iterations: int,
    time_limit_s: float,
) -> dict:
    seed = load_values(seed_path)
    n = len(seed)
    m = len(seed[0])
    candidate, seed_winners = seed_candidate(seed)
    master = NashMaster(n, m, candidate, source_host=source_host)
    resumed_rival_count = 0
    if resume_pool_path is not None:
        for rival in load_pool(
            resume_pool_path,
            n=n,
            m=m,
            candidate=candidate,
        ):
            resumed_rival_count += master.add_rival(rival)
    for winner in seed_winners:
        if winner["identity"] != candidate:
            master.add_rival(winner["identity"])
    cycle_rival_count = sum(
        master.add_rival(rival)
        for rival in bundle_cycle_rivals(candidate, n)
    )
    if add_source_substitution_rivals:
        substitution_rival_count = sum(
            master.add_rival(rival)
            for host in range(n)
            for rival in source_substitution_rivals(candidate, n, host)
        )
    else:
        substitution_rival_count = 0
    write_pool(
        pool_path,
        n=n,
        m=m,
        candidate=candidate,
        rivals=master.rivals,
    )
    started = time.time()
    trace = []
    status = "ITERATION_LIMIT"
    result_values = None
    reason_unknown = None
    for iteration in range(1, max_iterations + 1):
        solved, values, reason_unknown = master.solve(time_limit_s)
        if solved == "UNSAT":
            status = "FIXED_CANDIDATE_UNSAT"
            break
        if solved != "SAT":
            status = "MASTER_UNKNOWN"
            break
        assert values is not None
        states = eligible_states(values)
        candidate_record = next(
            state for state in states if state["identity"] == candidate
        )
        if candidate_record["parkable_hosts"]:
            raise AssertionError("NRA model made the blocked candidate insertable")
        violations = [
            state
            for state in states
            if state["identity"] != candidate
            and (
                state["nash"] > candidate_record["nash"]
                or (
                    state["nash"] >= candidate_record["nash"]
                    and state["parkable_hosts"]
                )
            )
        ]
        violations.sort(
            key=lambda state: (
                state["nash"],
                bool(state["parkable_hosts"]),
            ),
            reverse=True,
        )
        record = {
            "iteration": iteration,
            "rival_pool_size_before": len(master.rivals),
            "eligible_state_count": len(states),
            "candidate_nash": {
                "numerator": candidate_record["nash"].numerator,
                "denominator": candidate_record["nash"].denominator,
            },
            "violating_rival_count": len(violations),
            "values": [list(row) for row in values],
        }
        trace.append(record)
        print(
            f"iteration={iteration} pool={len(master.rivals)} "
            f"eligible={len(states)} rivals={len(violations)}",
            flush=True,
        )
        if not violations:
            status = "BLOCKED_NASH_MAXIMIZER_COUNTEREXAMPLE"
            result_values = values
            break
        added = 0
        for rival in violations[:add_per_iteration]:
            added += master.add_rival(rival["identity"])
        if not added:
            raise AssertionError("violating Nash rivals were already pooled")
        write_pool(
            pool_path,
            n=n,
            m=m,
            candidate=candidate,
            rivals=master.rivals,
        )
    smt2_path.write_text(master.solver.to_smt2())
    result = {
        "schema": SCHEMA,
        "status": status,
        "meaning": (
            "a counterexample refutes only maximum-Nash direct completion; "
            "UNSAT excludes only the seed-derived candidate identity"
        ),
        "n": n,
        "m": m,
        "seed_path": str(seed_path),
        "seed_sha256": hashlib.sha256(seed_path.read_bytes()).hexdigest(),
        "candidate": public_state(candidate),
        "seed_nash_maximizer_count": len(seed_winners),
        "resume_pool_path": str(resume_pool_path) if resume_pool_path else None,
        "resumed_rival_count": resumed_rival_count,
        "bundle_cycle_cut_count": master.bundle_cycle_cut_count,
        "source_host_cut_count": 1,
        "fixed_source_host": source_host,
        "bundle_cycle_rival_count": cycle_rival_count,
        "source_substitution_rival_count": substitution_rival_count,
        "iterations": iteration,
        "rival_pool_size": len(master.rivals),
        "elapsed_seconds": time.time() - started,
        "reason_unknown": reason_unknown,
        "values": [list(row) for row in result_values] if result_values else None,
        "trace": trace,
        "pool_path": str(pool_path),
        "pool_sha256": (
            hashlib.sha256(pool_path.read_bytes()).hexdigest()
            if pool_path.exists()
            else None
        ),
        "smt2_path": str(smt2_path),
        "smt2_sha256": hashlib.sha256(smt2_path.read_bytes()).hexdigest(),
    }
    atomic_json(result_path, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--smt2", type=Path, required=True)
    parser.add_argument("--resume-pool", type=Path)
    parser.add_argument("--source-host", type=int)
    parser.add_argument("--source-substitution-rivals", action="store_true")
    parser.add_argument("--add", type=int, default=32)
    parser.add_argument("--max-iterations", type=int, default=20)
    parser.add_argument("--time-limit", type=float, default=60)
    args = parser.parse_args()
    if args.add < 1 or args.max_iterations < 1 or args.time_limit <= 0:
        parser.error("positive CEGAR limits are required")
    result = run(
        seed_path=args.seed,
        result_path=args.result,
        pool_path=args.pool,
        smt2_path=args.smt2,
        resume_pool_path=args.resume_pool,
        source_host=args.source_host,
        add_source_substitution_rivals=args.source_substitution_rivals,
        add_per_iteration=args.add,
        max_iterations=args.max_iterations,
        time_limit_s=args.time_limit,
    )
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
