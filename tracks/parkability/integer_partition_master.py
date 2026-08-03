#!/usr/bin/env python3
"""CP-SAT master for bounded additive-EFX partition obstructions."""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Sequence

from ortools.sat.python import cp_model

try:
    from .core import validate_values
    from .master import add_lex_ge
except ImportError:
    from core import validate_values
    from master import add_lex_ge


Partition = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class IntegerPartitionMasterResult:
    status: str
    raw_status: str
    values: tuple[tuple[int, ...], ...] | None
    wall_time_seconds: float
    conflicts: int
    branches: int
    deterministic_time: float


class IntegerPartitionMaster:
    """Find a bounded integer instance obstructing every pooled partition."""

    def __init__(
        self,
        n: int,
        m: int,
        upper: int,
        *,
        exclude_universal_min: bool = False,
        exclude_peelable: bool = False,
        require_pairwise_distinct_rows: bool = False,
        require_pairwise_nonproportional_rows: bool = False,
        require_distinct_item_values: bool = False,
        require_upper_used: bool = False,
        symmetry: str = "none",
        fixed_values: Sequence[Sequence[int]] | None = None,
    ) -> None:
        if (
            type(n) is not int
            or n < 2
            or type(m) is not int
            or m < n
            or type(upper) is not int
            or upper < 1
        ):
            raise ValueError("n >= 2, m >= n, and a positive upper bound are required")
        if symmetry not in {"none", "double_lex"}:
            raise ValueError("symmetry must be 'none' or 'double_lex'")

        self.n = n
        self.m = m
        self.upper = upper
        self.exclude_universal_min = exclude_universal_min
        self.exclude_peelable = exclude_peelable
        self.require_pairwise_distinct_rows = require_pairwise_distinct_rows
        self.require_pairwise_nonproportional_rows = (
            require_pairwise_nonproportional_rows
        )
        self.require_distinct_item_values = require_distinct_item_values
        self.require_upper_used = require_upper_used
        self.symmetry = symmetry
        self.model = cp_model.CpModel()
        self.values = [
            [
                self.model.NewIntVar(1, upper, f"value_{observer}_{good}")
                for good in range(m)
            ]
            for observer in range(n)
        ]
        self._partitions: set[Partition] = set()
        self._comparison_variables: dict[
            tuple[int, int, int], cp_model.IntVar
        ] = {}
        self.matching_clauses = 0
        self.hall_selectors = 0
        self.hall_edge_clauses = 0
        self.owner_threshold_clauses = 0
        self.owner_threshold_envelope_rows = 0

        if fixed_values is not None:
            fixed = validate_values(
                fixed_values,
                expected_n=n,
                expected_m=m,
                lower=1,
                upper=upper,
            )
            for observer, row in enumerate(fixed):
                for good, value in enumerate(row):
                    self.model.Add(self.values[observer][good] == value)

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

        if exclude_universal_min:
            for good in range(m):
                not_universal = []
                for observer in range(n):
                    for other in range(m):
                        if other == good:
                            continue
                        witness = self.model.NewBoolVar(
                            f"not_universal_min_{good}_{observer}_{other}"
                        )
                        self.model.Add(
                            self.values[observer][good]
                            >= self.values[observer][other] + 1
                        ).OnlyEnforceIf(witness)
                        self.model.Add(
                            self.values[observer][good]
                            <= self.values[observer][other]
                        ).OnlyEnforceIf(witness.Not())
                        not_universal.append(witness)
                self.model.AddBoolOr(not_universal)

        if exclude_peelable:
            for observer in range(n):
                for good in range(m):
                    rest = tuple(other for other in range(m) if other != good)
                    witnesses = []
                    for removed in rest:
                        remainder = sum(
                            self.values[observer][other]
                            for other in rest
                            if other != removed
                        )
                        witness = self.model.NewBoolVar(
                            f"not_peelable_{observer}_{good}_{removed}"
                        )
                        self.model.Add(
                            self.values[observer][good] + 1 <= remainder
                        ).OnlyEnforceIf(witness)
                        self.model.Add(
                            self.values[observer][good] >= remainder
                        ).OnlyEnforceIf(witness.Not())
                        witnesses.append(witness)
                    self.model.AddBoolOr(witnesses)

        if require_pairwise_distinct_rows:
            for left in range(n):
                for right in range(left + 1, n):
                    differences = []
                    for good in range(m):
                        different = self.model.NewBoolVar(
                            f"rows_{left}_{right}_different_{good}"
                        )
                        self.model.Add(
                            self.values[left][good] != self.values[right][good]
                        ).OnlyEnforceIf(different)
                        self.model.Add(
                            self.values[left][good] == self.values[right][good]
                        ).OnlyEnforceIf(different.Not())
                        differences.append(different)
                    self.model.AddBoolOr(differences)

        if require_pairwise_nonproportional_rows:
            for left in range(n):
                for right in range(left + 1, n):
                    differences = []
                    for good in range(1, m):
                        left_cross = self.model.NewIntVar(
                            1,
                            upper * upper,
                            f"rows_{left}_{right}_left_cross_{good}",
                        )
                        right_cross = self.model.NewIntVar(
                            1,
                            upper * upper,
                            f"rows_{left}_{right}_right_cross_{good}",
                        )
                        self.model.AddMultiplicationEquality(
                            left_cross,
                            [self.values[left][good], self.values[right][0]],
                        )
                        self.model.AddMultiplicationEquality(
                            right_cross,
                            [self.values[right][good], self.values[left][0]],
                        )
                        different = self.model.NewBoolVar(
                            f"rows_{left}_{right}_nonproportional_{good}"
                        )
                        self.model.Add(left_cross != right_cross).OnlyEnforceIf(
                            different
                        )
                        self.model.Add(left_cross == right_cross).OnlyEnforceIf(
                            different.Not()
                        )
                        differences.append(different)
                    self.model.AddBoolOr(differences)

        if require_distinct_item_values:
            for row in self.values:
                self.model.AddAllDifferent(row)

        if require_upper_used:
            upper_hits = []
            for observer, row in enumerate(self.values):
                for good, value in enumerate(row):
                    hit = self.model.NewBoolVar(
                        f"upper_used_{observer}_{good}"
                    )
                    self.model.Add(value == upper).OnlyEnforceIf(hit)
                    self.model.Add(value <= upper - 1).OnlyEnforceIf(hit.Not())
                    upper_hits.append(hit)
            self.model.AddBoolOr(upper_hits)

    @property
    def pool_size(self) -> int:
        return len(self._partitions)

    @property
    def comparison_variable_count(self) -> int:
        return len(self._comparison_variables)

    def _sum_mask(self, observer: int, mask: int):
        return sum(
            self.values[observer][good]
            for good in range(self.m)
            if mask & (1 << good)
        )

    def _violation(
        self,
        observer: int,
        own_mask: int,
        remainder_mask: int,
    ) -> cp_model.IntVar:
        key = observer, own_mask, remainder_mask
        existing = self._comparison_variables.get(key)
        if existing is not None:
            return existing
        witness = self.model.NewBoolVar(
            f"violation_{observer}_{own_mask}_{remainder_mask}"
        )
        own = self._sum_mask(observer, own_mask)
        remainder = self._sum_mask(observer, remainder_mask)
        self.model.Add(own + 1 <= remainder).OnlyEnforceIf(witness)
        self.model.Add(own >= remainder).OnlyEnforceIf(witness.Not())
        self._comparison_variables[key] = witness
        return witness

    def _edge_violations(
        self,
        observer: int,
        own_bundle: int,
        bundles: Partition,
        masks: tuple[int, ...],
    ) -> tuple[cp_model.IntVar, ...]:
        violations = []
        for target_bundle, target in enumerate(bundles):
            if target_bundle == own_bundle:
                continue
            for removed in target:
                remainder_mask = masks[target_bundle] ^ (1 << removed)
                if remainder_mask:
                    violations.append(
                        self._violation(
                            observer,
                            masks[own_bundle],
                            remainder_mask,
                        )
                    )
        return tuple(violations)

    def add_partition_obstruction(
        self,
        raw_bundles: Sequence[Sequence[int]],
        *,
        encoding: str = "matching_clauses",
        activation: cp_model.IntVar | None = None,
    ) -> bool:
        if encoding not in {"matching_clauses", "hall_selectors"}:
            raise ValueError("unknown partition-obstruction encoding")
        if len(raw_bundles) != self.n:
            raise ValueError("partition must contain one nonempty bundle per agent")
        bundles = tuple(sorted(tuple(sorted(bundle)) for bundle in raw_bundles))
        if (
            any(not bundle for bundle in bundles)
            or sorted(good for bundle in bundles for good in bundle)
            != list(range(self.m))
        ):
            raise ValueError("partition bundles must cover every good exactly once")
        if bundles in self._partitions:
            return False

        masks = tuple(
            sum(1 << good for good in bundle)
            for bundle in bundles
        )
        edge_violations = {
            (observer, own_bundle): self._edge_violations(
                observer,
                own_bundle,
                bundles,
                masks,
            )
            for observer in range(self.n)
            for own_bundle in range(self.n)
        }
        partition_index = len(self._partitions)

        if encoding == "matching_clauses":
            for matching in itertools.permutations(range(self.n)):
                violations = tuple(
                    literal
                    for observer, own_bundle in enumerate(matching)
                    for literal in edge_violations[observer, own_bundle]
                )
                if not violations:
                    constraint = self.model.AddBoolOr([])
                else:
                    constraint = self.model.AddBoolOr(violations)
                if activation is not None:
                    constraint.OnlyEnforceIf(activation)
                self.matching_clauses += 1
        else:
            selectors = []
            for observer_mask in range(1, 1 << self.n):
                observers = tuple(
                    observer
                    for observer in range(self.n)
                    if observer_mask & (1 << observer)
                )
                for neighborhood_size in range(len(observers)):
                    for neighborhood in itertools.combinations(
                        range(self.n),
                        neighborhood_size,
                    ):
                        selector = self.model.NewBoolVar(
                            f"partition_{partition_index}_hall_"
                            f"{observer_mask}_{'_'.join(map(str, neighborhood))}"
                        )
                        if activation is not None:
                            self.model.AddImplication(selector, activation)
                        selectors.append(selector)
                        neighborhood_set = set(neighborhood)
                        for observer in observers:
                            for own_bundle in range(self.n):
                                if own_bundle in neighborhood_set:
                                    continue
                                violations = edge_violations[observer, own_bundle]
                                if violations:
                                    self.model.AddBoolOr(violations).OnlyEnforceIf(
                                        selector
                                    )
                                else:
                                    self.model.Add(selector == 0)
                                self.hall_edge_clauses += 1
            obstruction = self.model.AddBoolOr(selectors)
            if activation is not None:
                obstruction.OnlyEnforceIf(activation)
            self.hall_selectors += len(selectors)

        self._partitions.add(bundles)
        return True

    def add_duplicate_row_partition_obstruction(
        self,
        raw_bundles: Sequence[Sequence[int]],
        duplicate_observers: tuple[int, int],
        *,
        encoding: str = "duplicate_hall_selectors",
        activation: cp_model.IntVar | None = None,
    ) -> bool:
        """Block EFX support when the caller has equated two observer rows."""
        if (
            len(duplicate_observers) != 2
            or len(set(duplicate_observers)) != 2
            or any(
                type(observer) is not int or not 0 <= observer < self.n
                for observer in duplicate_observers
            )
            or self.n != 4
            or len(raw_bundles) != self.n
            or encoding
            not in {"duplicate_matching_clauses", "duplicate_hall_selectors"}
        ):
            raise ValueError("a valid duplicate pair in a four-agent partition is required")
        bundles = tuple(sorted(tuple(sorted(bundle)) for bundle in raw_bundles))
        if (
            any(not bundle for bundle in bundles)
            or sorted(good for bundle in bundles for good in bundle)
            != list(range(self.m))
        ):
            raise ValueError("partition bundles must cover every good exactly once")
        if bundles in self._partitions:
            return False

        representative = duplicate_observers[0]
        singletons = tuple(
            observer
            for observer in range(self.n)
            if observer not in duplicate_observers
        )
        masks = tuple(sum(1 << good for good in bundle) for bundle in bundles)
        edge_violations = {
            (observer, own_bundle): self._edge_violations(
                observer,
                own_bundle,
                bundles,
                masks,
            )
            for observer in (representative,) + singletons
            for own_bundle in range(self.n)
        }
        if encoding == "duplicate_matching_clauses":
            for duplicate_bundles in itertools.combinations(range(self.n), 2):
                remaining = tuple(
                    bundle
                    for bundle in range(self.n)
                    if bundle not in duplicate_bundles
                )
                for singleton_bundles in (remaining, remaining[::-1]):
                    violations = tuple(
                        literal
                        for own_bundle in duplicate_bundles
                        for literal in edge_violations[representative, own_bundle]
                    ) + tuple(
                        literal
                        for observer, own_bundle in zip(
                            singletons,
                            singleton_bundles,
                            strict=True,
                        )
                        for literal in edge_violations[observer, own_bundle]
                    )
                    constraint = self.model.AddBoolOr(violations)
                    if activation is not None:
                        constraint.OnlyEnforceIf(activation)
                    self.matching_clauses += 1
        else:
            hall_cases = (
                ((representative,), 1),
                ((singletons[0],), 0),
                ((singletons[1],), 0),
                (singletons, 1),
                ((representative, singletons[0]), 2),
                ((representative, singletons[1]), 2),
                ((representative,) + singletons, 3),
            )
            partition_index = len(self._partitions)
            selectors = []
            for case_index, (observers, max_neighborhood_size) in enumerate(
                hall_cases
            ):
                for neighborhood_size in range(max_neighborhood_size + 1):
                    for neighborhood in itertools.combinations(
                        range(self.n),
                        neighborhood_size,
                    ):
                        selector = self.model.NewBoolVar(
                            f"partition_{partition_index}_duplicate_hall_"
                            f"{case_index}_{'_'.join(map(str, neighborhood))}"
                        )
                        if activation is not None:
                            self.model.AddImplication(selector, activation)
                        selectors.append(selector)
                        neighborhood_set = set(neighborhood)
                        for observer in observers:
                            for own_bundle in range(self.n):
                                if own_bundle in neighborhood_set:
                                    continue
                                violations = edge_violations[observer, own_bundle]
                                if violations:
                                    self.model.AddBoolOr(violations).OnlyEnforceIf(
                                        selector
                                    )
                                else:
                                    self.model.Add(selector == 0)
                                self.hall_edge_clauses += 1
            obstruction = self.model.AddBoolOr(selectors)
            if activation is not None:
                obstruction.OnlyEnforceIf(activation)
            self.hall_selectors += len(selectors)
        self._partitions.add(bundles)
        return True

    def add_owner_threshold_obstruction(
        self,
        observer: int,
        singleton_good: int,
        raw_bundles: Sequence[Sequence[int]],
    ) -> None:
        if (
            type(observer) is not int
            or not 0 <= observer < self.n
            or type(singleton_good) is not int
            or not 0 <= singleton_good < self.m
            or len(raw_bundles) != self.n - 1
        ):
            raise ValueError("invalid owner-threshold obstruction")
        bundles = tuple(tuple(sorted(bundle)) for bundle in raw_bundles)
        if (
            any(not bundle for bundle in bundles)
            or sorted(good for bundle in bundles for good in bundle)
            != [good for good in range(self.m) if good != singleton_good]
        ):
            raise ValueError(
                "residual bundles must cover every nonsingleton good exactly once"
            )
        own_mask = 1 << singleton_good
        violations = []
        for bundle in bundles:
            bundle_mask = sum(1 << good for good in bundle)
            for removed in bundle:
                remainder_mask = bundle_mask ^ (1 << removed)
                if remainder_mask:
                    violations.append(
                        self._violation(observer, own_mask, remainder_mask)
                    )
        self.model.AddBoolOr(violations)
        self.owner_threshold_clauses += 1

    def add_owner_threshold_shape_envelope(
        self,
        observer: int,
        singleton_good: int,
    ) -> None:
        """Require universal threshold failure in the 4x9 singleton branch."""
        if (
            self.n != 4
            or self.m != 9
            or type(observer) is not int
            or not 0 <= observer < self.n
            or type(singleton_good) is not int
            or not 0 <= singleton_good < self.m
        ):
            raise ValueError("the owner-threshold envelope requires a 4x9 cell")
        favorite = self.values[observer][singleton_good]
        residual = [
            self.values[observer][good]
            for good in range(self.m)
            if good != singleton_good
        ]
        for value in residual:
            self.model.Add(favorite >= value)

        wires = residual
        comparator = 0
        for right in range(1, len(wires)):
            for position in range(right, 0, -1):
                high = self.model.NewIntVar(
                    1,
                    self.upper,
                    f"threshold_sort_high_{observer}_{singleton_good}_{comparator}",
                )
                low = self.model.NewIntVar(
                    1,
                    self.upper,
                    f"threshold_sort_low_{observer}_{singleton_good}_{comparator}",
                )
                self.model.AddMaxEquality(
                    high,
                    [wires[position - 1], wires[position]],
                )
                self.model.AddMinEquality(
                    low,
                    [wires[position - 1], wires[position]],
                )
                wires[position - 1] = high
                wires[position] = low
                comparator += 1

        self.model.Add(
            wires[4] + wires[5] + wires[6] >= favorite + 1
        )
        first_wall = self.model.NewBoolVar(
            f"threshold_first_wall_{observer}_{singleton_good}"
        )
        second_wall = self.model.NewBoolVar(
            f"threshold_second_wall_{observer}_{singleton_good}"
        )
        self.model.Add(
            wires[2] + wires[6] >= favorite + 1
        ).OnlyEnforceIf(first_wall)
        self.model.Add(
            wires[3] + wires[4] >= favorite + 1
        ).OnlyEnforceIf(second_wall)
        self.model.AddBoolOr([first_wall, second_wall])
        self.owner_threshold_envelope_rows += 1

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
            for other in range(self.m):
                if other != favorite:
                    self.model.Add(
                        self.values[observer][favorite]
                        >= self.values[observer][other] + 1
                    )

    def add_half_favorite_representatives(
        self,
        favorite_goods: Sequence[int],
        representative_goods: Sequence[int],
    ) -> None:
        favorites = tuple(favorite_goods)
        representatives = tuple(representative_goods)
        if (
            len(favorites) != self.n
            or len(representatives) != self.n
            or any(
                type(good) is not int or not 0 <= good < self.m
                for good in favorites + representatives
            )
            or any(
                favorite == representative
                for favorite, representative in zip(
                    favorites,
                    representatives,
                )
            )
        ):
            raise ValueError("half-favorite representatives are invalid")
        for observer, (favorite, representative) in enumerate(
            zip(favorites, representatives)
        ):
            self.model.Add(
                2 * self.values[observer][representative]
                >= self.values[observer][favorite] + 1
            )

    def add_half_favorite_representative_stabilizer(
        self,
        favorite_goods: Sequence[int],
        representative_goods: Sequence[int],
    ) -> None:
        favorites = tuple(favorite_goods)
        representatives = tuple(representative_goods)
        if (
            len(favorites) != self.n
            or len(representatives) != self.n
            or len(set(favorites)) != 1
            or len(set(representatives)) != self.n
        ):
            raise ValueError(
                "representative stabilizer requires one common favorite "
                "and distinct representatives"
            )
        diagonal = [
            self.values[observer][representative]
            for observer, representative in enumerate(representatives)
        ]
        for left, right in zip(diagonal, diagonal[1:]):
            self.model.Add(left >= right)
        fixed_goods = set(favorites) | set(representatives)
        unused_goods = [
            good for good in range(self.m) if good not in fixed_goods
        ]
        for left, right in zip(unused_goods, unused_goods[1:]):
            add_lex_ge(
                self.model,
                [self.values[observer][left] for observer in range(self.n)],
                [self.values[observer][right] for observer in range(self.n)],
                f"half_representative_unused_column_{left}_{right}",
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
                add_lex_ge(
                    self.model,
                    self.values[left],
                    self.values[right],
                    f"favorite_row_{favorite}_{left}_{right}",
                )
        unused_goods = [good for good in range(self.m) if good not in pattern]
        for left, right in zip(unused_goods, unused_goods[1:]):
            add_lex_ge(
                self.model,
                [self.values[observer][left] for observer in range(self.n)],
                [self.values[observer][right] for observer in range(self.n)],
                f"unused_column_{left}_{right}",
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
                for other in range(self.m):
                    if other not in ranking[: position + 1]:
                        self.model.Add(
                            self.values[observer][good]
                            >= self.values[observer][other] + 1
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
                add_lex_ge(
                    self.model,
                    self.values[left],
                    self.values[right],
                    f"ranking_row_{'_'.join(map(str, ranking))}_{left}_{right}",
                )
        used_goods = {good for ranking in rankings for good in ranking}
        unused_goods = [good for good in range(self.m) if good not in used_goods]
        for left, right in zip(unused_goods, unused_goods[1:]):
            add_lex_ge(
                self.model,
                [self.values[observer][left] for observer in range(self.n)],
                [self.values[observer][right] for observer in range(self.n)],
                f"ranking_unused_column_{left}_{right}",
            )

    def solve(
        self,
        *,
        time_limit_s: float = 60,
        workers: int = 1,
        random_seed: int = 1,
        log_search_progress: bool = False,
    ) -> IntegerPartitionMasterResult:
        if (
            time_limit_s <= 0
            or type(workers) is not int
            or workers < 1
            or type(random_seed) is not int
        ):
            raise ValueError("positive timeout, worker count, and integer seed required")
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_s
        solver.parameters.num_search_workers = workers
        solver.parameters.random_seed = random_seed
        solver.parameters.log_search_progress = log_search_progress
        status = solver.Solve(self.model)
        raw_status = solver.StatusName(status)
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            values = tuple(
                tuple(
                    solver.Value(self.values[observer][good])
                    for good in range(self.m)
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
        return IntegerPartitionMasterResult(
            status=normalized_status,
            raw_status=raw_status,
            values=values,
            wall_time_seconds=solver.WallTime(),
            conflicts=solver.NumConflicts(),
            branches=solver.NumBranches(),
            deterministic_time=solver.ResponseProto().deterministic_time,
        )
