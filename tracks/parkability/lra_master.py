#!/usr/bin/env python3
"""Exact positive-real master for the parkable-deletion search."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Sequence

import z3

try:
    from .core import Triple, bundles_of_base_owner, validate_triple, validate_values
except ImportError:
    from core import Triple, bundles_of_base_owner, validate_triple, validate_values


@dataclass(frozen=True)
class LRAMasterResult:
    status: str
    raw_status: str
    values: tuple[tuple[int, ...], ...] | None
    reason_unknown: str | None


def _rational(value: Fraction) -> z3.RatNumRef:
    return z3.RealVal(f"{value.numerator}/{value.denominator}")


def _model_rows(
    model: z3.ModelRef,
    variables: Sequence[Sequence[z3.ArithRef]],
) -> tuple[tuple[int, ...], ...]:
    rows = []
    for variables_row in variables:
        fractions = []
        for variable in variables_row:
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
            denominator = denominator * value.denominator // gcd(
                denominator, value.denominator
            )
        row = [int(value * denominator) for value in fractions]
        divisor = 0
        for value in row:
            divisor = gcd(divisor, value)
        rows.append(tuple(value // divisor for value in row))
    return tuple(rows)


def lex_ge(
    left: Sequence[z3.ArithRef],
    right: Sequence[z3.ArithRef],
) -> z3.BoolRef:
    if not left or len(left) != len(right):
        raise ValueError("lexicographic sequences must have equal positive length")
    strict_branches = [
        z3.And(
            *(left[prefix] == right[prefix] for prefix in range(index)),
            left[index] > right[index],
        )
        for index in range(len(left))
    ]
    return z3.Or(
        z3.And(*(x == y for x, y in zip(left, right))),
        *strict_branches,
    )


class ParkabilityLRAMaster:
    """Find a positive-real matrix invalidating every pooled parking triple."""

    def __init__(
        self,
        n: int,
        m: int,
        *,
        exclude_universal_min: bool = False,
        exclude_peelable: bool = False,
        require_pairwise_distinct_rows: bool = False,
        require_distinct_item_values: bool = False,
        require_favorite_hall_deficiency: bool = False,
        symmetry: str = "none",
        fixed_values: Sequence[Sequence[int]] | None = None,
        integer_upper: int | None = None,
    ) -> None:
        if type(n) is not int or n < 2 or type(m) is not int or m < 1:
            raise ValueError("n >= 2 and m >= 1 are required")
        if symmetry not in {"none", "double_lex"}:
            raise ValueError("symmetry must be 'none' or 'double_lex'")
        if integer_upper is not None and (
            type(integer_upper) is not int or integer_upper < 1
        ):
            raise ValueError("integer upper bound must be a positive integer")
        self.n = n
        self.m = m
        self.exclude_universal_min = exclude_universal_min
        self.exclude_peelable = exclude_peelable
        self.require_pairwise_distinct_rows = require_pairwise_distinct_rows
        self.require_distinct_item_values = require_distinct_item_values
        self.require_favorite_hall_deficiency = (
            require_favorite_hall_deficiency
        )
        self.symmetry = symmetry
        self.integer_upper = integer_upper
        self.solver = z3.SolverFor(
            "QF_LIA" if integer_upper is not None else "QF_LRA"
        )
        self.values = [
            [
                (
                    z3.Int(f"value_{observer}_{good}")
                    if integer_upper is not None
                    else z3.Real(f"value_{observer}_{good}")
                )
                for good in range(m)
            ]
            for observer in range(n)
        ]
        self._triples: set[Triple] = set()
        self._complete_allocations: set[tuple[int, ...]] = set()
        self._partitions: set[tuple[tuple[int, ...], ...]] = set()

        for row in self.values:
            self.solver.add(*(value > 0 for value in row))
            if integer_upper is None:
                self.solver.add(z3.Sum(row) == 1)
            else:
                self.solver.add(*(value <= integer_upper for value in row))

        if symmetry == "double_lex":
            for observer in range(n - 1):
                self.solver.add(
                    lex_ge(self.values[observer], self.values[observer + 1])
                )
            for good in range(m - 1):
                self.solver.add(
                    lex_ge(
                        [self.values[observer][good] for observer in range(n)],
                        [
                            self.values[observer][good + 1]
                            for observer in range(n)
                        ],
                    )
                )

        if exclude_universal_min:
            for good in range(m):
                self.solver.add(
                    z3.Or(
                        *(
                            self.values[observer][good]
                            > self.values[observer][other]
                            for observer in range(n)
                            for other in range(m)
                            if other != good
                        )
                    )
                )

        if exclude_peelable:
            for observer in range(n):
                for good in range(m):
                    rest = tuple(other for other in range(m) if other != good)
                    self.solver.add(
                        z3.Or(
                            *(
                                self.values[observer][good]
                                < self._sum(
                                    observer,
                                    tuple(other for other in rest if other != removed),
                                )
                                for removed in rest
                            )
                        )
                    )

        if require_pairwise_distinct_rows:
            for left in range(n):
                for right in range(left + 1, n):
                    self.solver.add(
                        z3.Or(
                            *(
                                self.values[left][good]
                                != self.values[right][good]
                                for good in range(m)
                            )
                        )
                    )

        if require_distinct_item_values:
            for row in self.values:
                self.solver.add(z3.Distinct(*row))

        if require_favorite_hall_deficiency:
            if m < n:
                raise ValueError("favorite-good matching requires at least n goods")
            favorite = [
                [
                    z3.Bool(f"favorite_agent_{observer}_good_{good}")
                    for good in range(m)
                ]
                for observer in range(n)
            ]
            for observer in range(n):
                for good in range(m):
                    self.solver.add(
                        favorite[observer][good]
                        == z3.And(
                            *(
                                self.values[observer][good]
                                >= self.values[observer][other]
                                for other in range(m)
                            )
                        )
                    )
            for matching in itertools.permutations(range(m), n):
                self.solver.add(
                    z3.Or(
                        *(
                            z3.Not(favorite[observer][matching[observer]])
                            for observer in range(n)
                        )
                    )
                )

        if fixed_values is not None:
            fixed = validate_values(
                fixed_values,
                expected_n=n,
                expected_m=m,
                lower=1,
            )
            for observer, row in enumerate(fixed):
                for good, value in enumerate(row):
                    self.solver.add(
                        self.values[observer][good]
                        == (
                            value
                            if integer_upper is not None
                            else _rational(Fraction(value, sum(row)))
                        )
                    )

    @property
    def pool_size(self) -> int:
        return (
            len(self._triples)
            + len(self._complete_allocations)
            + len(self._partitions)
        )

    def _sum(self, observer: int, goods: Sequence[int]) -> z3.ArithRef:
        return z3.Sum(*(self.values[observer][good] for good in goods))

    def add_triple(self, raw_triple: Triple | dict) -> bool:
        triple = validate_triple(raw_triple, self.n, self.m)
        if triple in self._triples:
            return False
        bundles = bundles_of_base_owner(triple.base_owner, self.n)
        violations = []

        for observer in range(self.n):
            own = self._sum(observer, bundles[observer])
            for target in range(self.n):
                if observer == target:
                    continue
                for removed in bundles[target]:
                    remainder = tuple(
                        good for good in bundles[target] if good != removed
                    )
                    violations.append(own < self._sum(observer, remainder))

        enlarged = bundles[triple.host] + (triple.floater,)
        for observer in range(self.n):
            if observer == triple.host:
                continue
            own = self._sum(observer, bundles[observer])
            for removed in enlarged:
                remainder = tuple(good for good in enlarged if good != removed)
                violations.append(own < self._sum(observer, remainder))

        if not violations:
            raise ValueError("triple generated no EFX inequalities")
        self.solver.add(z3.Or(*violations))
        self._triples.add(triple)
        return True

    def add_complete_allocation(self, assignment: Sequence[int]) -> bool:
        allocation = tuple(assignment)
        if len(allocation) != self.m or any(
            type(owner) is not int or not 0 <= owner < self.n
            for owner in allocation
        ):
            raise ValueError("complete allocation must assign every good to an agent")
        if allocation in self._complete_allocations:
            return False
        bundles = tuple(
            tuple(good for good, owner in enumerate(allocation) if owner == target)
            for target in range(self.n)
        )
        violations = []
        for observer in range(self.n):
            own = self._sum(observer, bundles[observer])
            for target in range(self.n):
                if observer == target:
                    continue
                for removed in bundles[target]:
                    remainder = tuple(
                        good for good in bundles[target] if good != removed
                    )
                    violations.append(own < self._sum(observer, remainder))
        self.solver.add(z3.Or(*violations) if violations else z3.BoolVal(False))
        self._complete_allocations.add(allocation)
        return True

    def add_partition_obstruction(
        self,
        raw_bundles: Sequence[Sequence[int]],
        *,
        encoding: str = "matching_clauses",
        activation: z3.BoolRef | None = None,
    ) -> bool:
        if encoding not in {
            "matching_clauses",
            "inline_matching_clauses",
            "hall_selectors",
        }:
            raise ValueError("unknown partition-obstruction encoding")
        if len(raw_bundles) != self.n:
            raise ValueError("partition must contain one nonempty bundle per agent")
        bundles = tuple(
            sorted(tuple(sorted(bundle)) for bundle in raw_bundles)
        )
        if (
            any(not bundle for bundle in bundles)
            or sorted(good for bundle in bundles for good in bundle)
            != list(range(self.m))
        ):
            raise ValueError("partition bundles must cover every good exactly once")
        if bundles in self._partitions:
            return False
        if activation is not None and not z3.is_bool(activation):
            raise ValueError("partition activation must be Boolean")

        partition_index = len(self._partitions)
        if encoding == "inline_matching_clauses":
            for matching in itertools.permutations(range(self.n)):
                violations = []
                for observer, own_bundle in enumerate(matching):
                    own = self._sum(observer, bundles[own_bundle])
                    for target_bundle, target in enumerate(bundles):
                        if target_bundle == own_bundle:
                            continue
                        for removed in target:
                            remainder = tuple(
                                good for good in target if good != removed
                            )
                            violations.append(
                                own < self._sum(observer, remainder)
                            )
                obstruction = z3.Or(*violations)
                self.solver.add(
                    obstruction
                    if activation is None
                    else z3.Implies(activation, obstruction)
                )
            self._partitions.add(bundles)
            return True

        feasible = [
            [
                z3.Bool(
                    f"partition_{partition_index}_agent_{observer}_bundle_{bundle}"
                )
                for bundle in range(self.n)
            ]
            for observer in range(self.n)
        ]
        for observer in range(self.n):
            for own_bundle in range(self.n):
                own = self._sum(observer, bundles[own_bundle])
                comparisons = []
                for target_bundle in range(self.n):
                    if target_bundle == own_bundle:
                        continue
                    for removed in bundles[target_bundle]:
                        remainder = tuple(
                            good
                            for good in bundles[target_bundle]
                            if good != removed
                        )
                        comparisons.append(own >= self._sum(observer, remainder))
                self.solver.add(
                    feasible[observer][own_bundle] == z3.And(*comparisons)
                )

        if encoding == "matching_clauses":
            for matching in itertools.permutations(range(self.n)):
                obstruction = z3.Or(
                    *(
                        z3.Not(feasible[observer][matching[observer]])
                        for observer in range(self.n)
                    )
                )
                self.solver.add(
                    obstruction
                    if activation is None
                    else z3.Implies(activation, obstruction)
                )
        else:
            hall_selectors = []
            for observer_mask in range(1, 1 << self.n):
                if observer_mask.bit_count() == 1:
                    continue
                selector = z3.Bool(
                    f"partition_{partition_index}_hall_{observer_mask}"
                )
                hall_selectors.append(selector)
                observers = tuple(
                    observer
                    for observer in range(self.n)
                    if observer_mask & (1 << observer)
                )
                neighborhood = [
                    z3.Or(
                        *(feasible[observer][bundle] for observer in observers)
                    )
                    for bundle in range(self.n)
                ]
                for forbidden in itertools.combinations(
                    neighborhood,
                    len(observers),
                ):
                    self.solver.add(
                        z3.Implies(
                            selector,
                            z3.Or(*(z3.Not(neighbor) for neighbor in forbidden)),
                        )
                    )
            obstruction = z3.Or(*hall_selectors)
            self.solver.add(
                obstruction
                if activation is None
                else z3.Implies(activation, obstruction)
            )
        self._partitions.add(bundles)
        return True

    def add_normalized_box(
        self,
        center_values: Sequence[Sequence[int]],
        radius: Fraction,
    ) -> None:
        if radius <= 0:
            raise ValueError("box radius must be positive")
        center = validate_values(
            center_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        for observer, row in enumerate(center):
            total = sum(row)
            for good, value in enumerate(row):
                midpoint = Fraction(value, total)
                self.solver.add(
                    self.values[observer][good] >= _rational(midpoint - radius),
                    self.values[observer][good] <= _rational(midpoint + radius),
                )

    def add_minimum_cover(self, goods: Sequence[int]) -> None:
        cover = tuple(goods)
        if (
            len(cover) < 1
            or len(cover) != len(set(cover))
            or any(type(good) is not int or not 0 <= good < self.m for good in cover)
        ):
            raise ValueError("minimum-cover goods must be distinct valid indices")
        for observer in range(self.n):
            self.solver.add(
                z3.Or(
                    *(
                        z3.And(
                            *(
                                self.values[observer][good]
                                <= self.values[observer][other]
                                for other in range(self.m)
                            )
                        )
                        for good in cover
                    )
                )
            )

    def add_minimum_pattern(self, goods_by_observer: Sequence[int]) -> None:
        pattern = tuple(goods_by_observer)
        if len(pattern) != self.n or any(
            type(good) is not int or not 0 <= good < self.m for good in pattern
        ):
            raise ValueError("minimum pattern must specify one valid good per observer")
        for observer, good in enumerate(pattern):
            self.solver.add(
                *(
                    self.values[observer][good] <= self.values[observer][other]
                    for other in range(self.m)
                )
            )

    def add_strict_minimum_pattern(
        self,
        goods_by_observer: Sequence[int],
    ) -> None:
        pattern = tuple(goods_by_observer)
        if len(pattern) != self.n or any(
            type(good) is not int or not 0 <= good < self.m for good in pattern
        ):
            raise ValueError("minimum pattern must specify one valid good per observer")
        for observer, minimum in enumerate(pattern):
            self.solver.add(
                *(
                    self.values[observer][minimum]
                    < self.values[observer][other]
                    for other in range(self.m)
                    if other != minimum
                )
            )

    def add_bottom_set(self, goods: Sequence[int]) -> None:
        bottom = tuple(goods)
        if (
            len(bottom) < 1
            or len(bottom) != len(set(bottom))
            or any(type(good) is not int or not 0 <= good < self.m for good in bottom)
        ):
            raise ValueError("bottom-set goods must be distinct valid indices")
        outside = tuple(good for good in range(self.m) if good not in bottom)
        if not outside:
            raise ValueError("bottom set must omit at least one good")
        for observer in range(self.n):
            self.solver.add(
                *(
                    self.values[observer][good]
                    <= self.values[observer][other]
                    for good in bottom
                    for other in outside
                )
            )

    def add_aggregate_minimum_good(
        self,
        good: int,
        *,
        strict: bool = False,
    ) -> None:
        if type(good) is not int or not 0 <= good < self.m:
            raise ValueError("aggregate-minimum good is outside the goods range")
        selected_total = z3.Sum(
            *(self.values[observer][good] for observer in range(self.n))
        )
        for other in range(self.m):
            if other == good:
                continue
            other_total = z3.Sum(
                *(self.values[observer][other] for observer in range(self.n))
            )
            self.solver.add(
                selected_total < other_total
                if strict
                else selected_total <= other_total
            )

    def add_strict_favorite_pattern(
        self,
        goods_by_observer: Sequence[int],
    ) -> None:
        pattern = tuple(goods_by_observer)
        if len(pattern) != self.n or any(
            type(good) is not int or not 0 <= good < self.m for good in pattern
        ):
            raise ValueError("favorite pattern must specify one valid good per agent")
        for observer, favorite in enumerate(pattern):
            self.solver.add(
                *(
                    self.values[observer][favorite]
                    > self.values[observer][other]
                    for other in range(self.m)
                    if other != favorite
                )
            )

    def add_favorite_pattern_stabilizer(
        self,
        goods_by_observer: Sequence[int],
    ) -> None:
        pattern = tuple(goods_by_observer)
        if len(pattern) != self.n or any(
            type(good) is not int or not 0 <= good < self.m for good in pattern
        ):
            raise ValueError("favorite pattern must specify one valid good per agent")
        for favorite in sorted(set(pattern)):
            agents = [
                observer
                for observer, good in enumerate(pattern)
                if good == favorite
            ]
            for left, right in zip(agents, agents[1:]):
                self.solver.add(lex_ge(self.values[left], self.values[right]))
        unused_goods = [good for good in range(self.m) if good not in pattern]
        for left, right in zip(unused_goods, unused_goods[1:]):
            self.solver.add(
                lex_ge(
                    [self.values[observer][left] for observer in range(self.n)],
                    [self.values[observer][right] for observer in range(self.n)],
                )
            )

    def add_strict_ranking_prefixes(
        self,
        rankings_by_observer: Sequence[Sequence[int]],
    ) -> None:
        rankings = tuple(tuple(ranking) for ranking in rankings_by_observer)
        if len(rankings) != self.n or any(
            not ranking
            or len(ranking) != len(set(ranking))
            or any(
                type(good) is not int or not 0 <= good < self.m
                for good in ranking
            )
            for ranking in rankings
        ):
            raise ValueError("each agent needs a valid distinct ranking prefix")
        for observer, ranking in enumerate(rankings):
            for position, good in enumerate(ranking):
                lower_goods = [
                    other
                    for other in range(self.m)
                    if other not in ranking[: position + 1]
                ]
                self.solver.add(
                    *(
                        self.values[observer][good]
                        > self.values[observer][other]
                        for other in lower_goods
                    )
                )

    def add_ranking_prefix_stabilizer(
        self,
        rankings_by_observer: Sequence[Sequence[int]],
    ) -> None:
        rankings = tuple(tuple(ranking) for ranking in rankings_by_observer)
        if len(rankings) != self.n:
            raise ValueError("ranking-prefix stabilizer needs one prefix per agent")
        for ranking in sorted(set(rankings)):
            agents = [
                observer
                for observer, item in enumerate(rankings)
                if item == ranking
            ]
            for left, right in zip(agents, agents[1:]):
                self.solver.add(lex_ge(self.values[left], self.values[right]))
        used_goods = {good for ranking in rankings for good in ranking}
        unused_goods = [good for good in range(self.m) if good not in used_goods]
        for left, right in zip(unused_goods, unused_goods[1:]):
            self.solver.add(
                lex_ge(
                    [self.values[observer][left] for observer in range(self.n)],
                    [self.values[observer][right] for observer in range(self.n)],
                )
            )

    def solve(self, *, time_limit_s: float = 0) -> LRAMasterResult:
        if time_limit_s < 0:
            raise ValueError("time limit cannot be negative")
        self.solver.set(timeout=int(time_limit_s * 1000))
        status = self.solver.check()
        if status == z3.sat:
            return LRAMasterResult(
                status="SAT",
                raw_status=str(status),
                values=_model_rows(self.solver.model(), self.values),
                reason_unknown=None,
            )
        if status == z3.unsat:
            return LRAMasterResult(
                status="UNSAT",
                raw_status=str(status),
                values=None,
                reason_unknown=None,
            )
        return LRAMasterResult(
            status="UNKNOWN",
            raw_status=str(status),
            values=None,
            reason_unknown=self.solver.reason_unknown(),
        )

    def to_smt2(self) -> str:
        return self.solver.to_smt2()
