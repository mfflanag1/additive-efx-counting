#!/usr/bin/env python3
"""CP-SAT master for the bounded zero-parkable-triple search."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ortools.sat.python import cp_model

try:
    from .core import (
        Triple,
        bundles_of_base_owner,
        validate_triple,
        validate_values,
    )
except ImportError:
    from core import (
        Triple,
        bundles_of_base_owner,
        validate_triple,
        validate_values,
    )


@dataclass(frozen=True)
class MasterResult:
    status: str
    raw_status: str
    values: tuple[tuple[int, ...], ...] | None
    wall_time_seconds: float
    conflicts: int
    branches: int


def add_lex_ge(
    model: cp_model.CpModel,
    left: Sequence[cp_model.IntVar],
    right: Sequence[cp_model.IntVar],
    name: str,
) -> None:
    if not left or len(left) != len(right):
        raise ValueError("lexicographic sequences must have equal positive length")
    equal = []
    for index, (left_value, right_value) in enumerate(zip(left, right)):
        same = model.NewBoolVar(f"{name}_equal_{index}")
        model.Add(left_value == right_value).OnlyEnforceIf(same)
        model.Add(left_value != right_value).OnlyEnforceIf(same.Not())
        equal.append(same)
    model.Add(left[0] >= right[0])
    for index in range(1, len(left)):
        model.Add(left[index] >= right[index]).OnlyEnforceIf(equal[:index])


class ParkabilityMaster:
    """Find a bounded matrix invalidating every pooled parking triple."""

    def __init__(
        self,
        n: int,
        m: int,
        lower: int,
        upper: int,
        *,
        symmetry: str = "none",
        fixed_values: Sequence[Sequence[int]] | None = None,
    ) -> None:
        if type(n) is not int or n < 2 or type(m) is not int or m < 1:
            raise ValueError("n >= 2 and m >= 1 are required")
        if (
            type(lower) is not int
            or type(upper) is not int
            or lower < 0
            or lower > upper
        ):
            raise ValueError("invalid integer value interval")
        if symmetry not in {"none", "double_lex"}:
            raise ValueError("symmetry must be 'none' or 'double_lex'")

        self.n = n
        self.m = m
        self.lower = lower
        self.upper = upper
        self.symmetry = symmetry
        self.model = cp_model.CpModel()
        self.values = [
            [
                self.model.NewIntVar(lower, upper, f"value_{observer}_{good}")
                for good in range(m)
            ]
            for observer in range(n)
        ]
        self._triples: set[Triple] = set()

        if fixed_values is not None:
            fixed = validate_values(
                fixed_values,
                expected_n=n,
                expected_m=m,
                lower=lower,
                upper=upper,
            )
            for observer in range(n):
                for good in range(m):
                    self.model.Add(self.values[observer][good] == fixed[observer][good])

        if symmetry == "double_lex":
            for observer in range(n - 1):
                add_lex_ge(
                    self.model,
                    self.values[observer],
                    self.values[observer + 1],
                    f"row_{observer}_{observer + 1}",
                )
            for good in range(m - 1):
                add_lex_ge(
                    self.model,
                    [self.values[observer][good] for observer in range(n)],
                    [self.values[observer][good + 1] for observer in range(n)],
                    f"column_{good}_{good + 1}",
                )

    @property
    def pool_size(self) -> int:
        return len(self._triples)

    def _new_violation(
        self,
        observer: int,
        own_bundle: Sequence[int],
        target_remainder: Sequence[int],
        name: str,
    ) -> cp_model.IntVar:
        witness = self.model.NewBoolVar(name)
        self.model.Add(
            sum(self.values[observer][good] for good in own_bundle) + 1
            <= sum(self.values[observer][good] for good in target_remainder)
        ).OnlyEnforceIf(witness)
        return witness

    def add_triple(self, raw_triple: Triple | dict) -> bool:
        triple = validate_triple(raw_triple, self.n, self.m)
        if triple in self._triples:
            return False
        bundles = bundles_of_base_owner(triple.base_owner, self.n)
        violations = []
        prefix = f"triple_{len(self._triples)}"

        for observer in range(self.n):
            own_bundle = bundles[observer]
            for target in range(self.n):
                if observer == target:
                    continue
                for removed in bundles[target]:
                    target_remainder = tuple(
                        good for good in bundles[target] if good != removed
                    )
                    violations.append(
                        self._new_violation(
                            observer,
                            own_bundle,
                            target_remainder,
                            (
                                f"{prefix}_base_observer_{observer}"
                                f"_target_{target}_remove_{removed}"
                            ),
                        )
                    )

        enlarged = bundles[triple.host] + (triple.floater,)
        for observer in range(self.n):
            if observer == triple.host:
                continue
            own_bundle = bundles[observer]
            for removed in enlarged:
                target_remainder = tuple(good for good in enlarged if good != removed)
                violations.append(
                    self._new_violation(
                        observer,
                        own_bundle,
                        target_remainder,
                        (
                            f"{prefix}_parking_observer_{observer}"
                            f"_host_{triple.host}_remove_{removed}"
                        ),
                    )
                )

        if not violations:
            raise ValueError("triple generated no EFX inequalities")
        self.model.AddBoolOr(violations)
        self._triples.add(triple)
        return True

    def solve(
        self,
        *,
        time_limit_s: float = 60.0,
        workers: int = 1,
        random_seed: int = 1,
    ) -> MasterResult:
        if time_limit_s <= 0 or type(workers) is not int or workers < 1:
            raise ValueError("positive time limit and worker count are required")
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_s
        solver.parameters.num_search_workers = workers
        solver.parameters.random_seed = random_seed
        status = solver.Solve(self.model)
        raw_status = solver.StatusName(status)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            values = tuple(
                tuple(
                    solver.Value(self.values[observer][good]) for good in range(self.m)
                )
                for observer in range(self.n)
            )
            normalized_status = "SAT"
        elif status == cp_model.INFEASIBLE:
            values = None
            normalized_status = "UNSAT"
        else:
            values = None
            normalized_status = "UNKNOWN"
        return MasterResult(
            status=normalized_status,
            raw_status=raw_status,
            values=values,
            wall_time_seconds=solver.WallTime(),
            conflicts=solver.NumConflicts(),
            branches=solver.NumBranches(),
        )
