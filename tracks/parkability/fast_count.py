#!/usr/bin/env python3
"""Vectorized exact parkability counts for heuristic counterexample search."""

from __future__ import annotations

import itertools
import math

import numpy as np

try:
    from .core import validate_values
except ImportError:
    from core import validate_values


class FastParkability:
    def __init__(self, n: int = 4, m: int = 8) -> None:
        if type(n) is not int or n < 2 or type(m) is not int or m < 1:
            raise ValueError("n >= 2 and m >= 1 are required")
        self.n = n
        self.m = m
        self.subset_count = 1 << m
        subsets = np.arange(self.subset_count, dtype=np.int64)
        goods = np.arange(m, dtype=np.int64)
        self.bits = ((subsets[:, None] >> goods) & 1).astype(bool)
        self.base_masks = []
        assignments = np.arange(n ** (m - 1), dtype=np.int64)
        powers = n ** np.arange(m - 1, dtype=np.int64)
        choices = (assignments[:, None] // powers) % n
        rows = np.arange(len(assignments))
        for floater in range(m):
            masks = np.zeros((len(assignments), n), dtype=np.int64)
            for position, good in enumerate(
                candidate for candidate in range(m) if candidate != floater
            ):
                masks[rows, choices[:, position]] |= 1 << good
            self.base_masks.append(masks)
        complete_indices = np.arange(n**m, dtype=np.int64)
        complete_choices = (complete_indices[:, None] // (n**goods)) % n
        self.complete_masks = np.zeros((len(complete_indices), n), dtype=np.int64)
        complete_rows = np.arange(len(complete_indices))
        for good in range(m):
            self.complete_masks[complete_rows, complete_choices[:, good]] |= 1 << good
        sizes = np.stack(
            [(complete_choices == agent).sum(axis=1) for agent in range(n)],
            axis=1,
        )
        self.complete_shape_codes = (
            np.sort(sizes, axis=1)[:, ::-1]
            @ (10 ** np.arange(n - 1, -1, -1, dtype=np.int64))
        )
        self._complete_family_indices: dict[
            tuple[tuple[int, ...], tuple[int, ...]], np.ndarray
        ] = {}

    def _tables(
        self, values: tuple[tuple[int, ...], ...]
    ) -> tuple[np.ndarray, np.ndarray]:
        matrix = np.asarray(values, dtype=np.int64)
        totals = matrix @ self.bits.T
        maximum = int(matrix.max()) + 1
        masked = np.where(
            self.bits[None, :, :],
            matrix[:, None, :],
            maximum,
        )
        minima = masked.min(axis=2)
        minima[:, 0] = 0
        return totals, totals - minima

    def landscape(self, raw_values: list[list[int]] | tuple[tuple[int, ...], ...]) -> dict:
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        totals, thresholds = self._tables(values)
        row_totals = np.asarray([sum(row) for row in values], dtype=np.float64)
        by_floater_host = [[0] * self.n for _ in range(self.m)]
        positive_margin_sum = 0
        normalized_margin_sum = 0.0

        for floater, masks in enumerate(self.base_masks):
            base_margin = np.full(len(masks), np.iinfo(np.int64).max, dtype=np.int64)
            normalized_base_margin = np.full(len(masks), np.inf)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                for target in range(self.n):
                    if observer != target:
                        slack = own - thresholds[observer, masks[:, target]]
                        base_margin = np.minimum(
                            base_margin,
                            slack,
                        )
                        normalized_base_margin = np.minimum(
                            normalized_base_margin,
                            slack / row_totals[observer],
                        )

            for host in range(self.n):
                margin = base_margin.copy()
                normalized_margin = normalized_base_margin.copy()
                enlarged = masks[:, host] | (1 << floater)
                for observer in range(self.n):
                    if observer != host:
                        own = totals[observer, masks[:, observer]]
                        slack = own - thresholds[observer, enlarged]
                        margin = np.minimum(
                            margin,
                            slack,
                        )
                        normalized_margin = np.minimum(
                            normalized_margin,
                            slack / row_totals[observer],
                        )
                valid = margin >= 0
                count = int(valid.sum())
                by_floater_host[floater][host] = count
                positive_margin_sum += int((margin[valid] + 1).sum())
                normalized_margin_sum += float(normalized_margin[valid].sum())

        return {
            "parkable_triple_count": sum(map(sum, by_floater_host)),
            "parkable_triple_count_by_floater_host": by_floater_host,
            "positive_margin_sum": positive_margin_sum,
            "normalized_margin_sum": normalized_margin_sum,
        }

    def lexmax_one_unallocated_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
        *,
        agent_order: tuple[int, ...] | None = None,
    ) -> dict:
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        order = tuple(range(self.n)) if agent_order is None else agent_order
        if sorted(order) != list(range(self.n)):
            raise ValueError("agent_order must be a permutation of the agents")
        matrix = np.asarray(values, dtype=np.int64)
        totals, thresholds = self._tables(values)
        row_totals = matrix.sum(axis=1).astype(np.float64)
        best_key: tuple[int, ...] | None = None
        best_candidates: list[tuple[int, int, np.ndarray, tuple[int, ...]]] = []
        eligible_base_count = 0

        for floater, masks in enumerate(self.base_masks):
            valid = np.ones(len(masks), dtype=bool)
            own_values = np.empty((len(masks), self.n), dtype=np.int64)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                own_values[:, observer] = own
                valid &= own >= matrix[observer, floater]
                for target in range(self.n):
                    if observer != target:
                        valid &= own >= thresholds[observer, masks[:, target]]
            eligible_base_count += int(valid.sum())
            for index in np.flatnonzero(valid):
                utilities = tuple(int(value) for value in own_values[index])
                key = tuple(utilities[observer] for observer in order)
                candidate = (
                    floater,
                    int(index),
                    masks[index].copy(),
                    utilities,
                )
                if best_key is None or key > best_key:
                    best_key = key
                    best_candidates = [candidate]
                elif key == best_key:
                    best_candidates.append(candidate)

        records = []
        for floater, index, masks, utilities in best_candidates:
            host_margins = []
            for host in range(self.n):
                enlarged = int(masks[host]) | (1 << floater)
                margin = min(
                    (
                        totals[observer, masks[observer]]
                        - thresholds[observer, enlarged]
                    )
                    / row_totals[observer]
                    for observer in range(self.n)
                    if observer != host
                )
                host_margins.append(float(margin))
            records.append({
                "floater": floater,
                "base_index": index,
                "utilities": list(utilities),
                "best_host_normalized_margin": max(host_margins),
                "insertable": max(host_margins) >= 0,
            })

        return {
            "agent_order": list(order),
            "eligible_base_count": eligible_base_count,
            "lexmax_utility_key": list(best_key) if best_key is not None else None,
            "lexmax_base_count": len(records),
            "lexmax_insertable_count": sum(record["insertable"] for record in records),
            "best_lexmax_host_normalized_margin": (
                max(
                    record["best_host_normalized_margin"]
                    for record in records
                )
                if records
                else None
            ),
            "lexmax_bases": records,
        }

    def lexmax_all_agent_orders_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
    ) -> dict:
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        matrix = np.asarray(values, dtype=np.int64)
        totals, thresholds = self._tables(values)
        row_totals = matrix.sum(axis=1).astype(np.float64)
        candidates = []

        for floater, masks in enumerate(self.base_masks):
            valid = np.ones(len(masks), dtype=bool)
            own_values = np.empty((len(masks), self.n), dtype=np.int64)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                own_values[:, observer] = own
                valid &= own >= matrix[observer, floater]
                for target in range(self.n):
                    if observer != target:
                        valid &= own >= thresholds[observer, masks[:, target]]
            for index in np.flatnonzero(valid):
                candidates.append(
                    (
                        floater,
                        int(index),
                        masks[index].copy(),
                        tuple(int(value) for value in own_values[index]),
                    )
                )
        if not candidates:
            raise AssertionError("profile has no eligible one-unallocated EFX base")

        selected: dict[tuple[int, int], tuple[int, int, np.ndarray, tuple[int, ...]]] = {}
        order_selections = []
        for order in itertools.permutations(range(self.n)):
            best_key = max(
                tuple(candidate[3][agent] for agent in order)
                for candidate in candidates
            )
            best = [
                candidate
                for candidate in candidates
                if tuple(candidate[3][agent] for agent in order) == best_key
            ]
            for candidate in best:
                selected[(candidate[0], candidate[1])] = candidate
            order_selections.append((order, best_key, best))

        margins = {}
        for key, (floater, _, masks, _) in selected.items():
            host_margins = []
            for host in range(self.n):
                enlarged = int(masks[host]) | (1 << floater)
                host_margins.append(
                    min(
                        (
                            totals[observer, masks[observer]]
                            - thresholds[observer, enlarged]
                        )
                        / row_totals[observer]
                        for observer in range(self.n)
                        if observer != host
                    )
                )
            margins[key] = float(max(host_margins))

        order_records = []
        for order, best_key, best in order_selections:
            best_margin = max(margins[(candidate[0], candidate[1])] for candidate in best)
            order_records.append(
                {
                    "agent_order": list(order),
                    "lexmax_utility_key": list(best_key),
                    "lexmax_base_count": len(best),
                    "lexmax_insertable_count": sum(
                        margins[(candidate[0], candidate[1])] >= 0
                        for candidate in best
                    ),
                    "best_lexmax_host_normalized_margin": best_margin,
                }
            )

        first_agent_records = []
        for agent in range(self.n):
            records = [
                record
                for record in order_records
                if record["agent_order"][0] == agent
            ]
            best_margin = max(
                record["best_lexmax_host_normalized_margin"]
                for record in records
            )
            first_agent_records.append(
                {
                    "agent": agent,
                    "agent_order_count": len(records),
                    "insertable_agent_order_count": sum(
                        record["lexmax_insertable_count"] > 0
                        for record in records
                    ),
                    "best_rescue_order_normalized_margin": best_margin,
                }
            )

        return {
            "eligible_base_count": len(candidates),
            "agent_order_count": len(order_records),
            "insertable_agent_order_count": sum(
                record["lexmax_insertable_count"] > 0
                for record in order_records
            ),
            "blocked_agent_order_count": sum(
                record["lexmax_insertable_count"] == 0
                for record in order_records
            ),
            "best_rescue_order_normalized_margin": max(
                record["best_lexmax_host_normalized_margin"]
                for record in order_records
            ),
            "insertable_first_agent_count": sum(
                record["insertable_agent_order_count"] > 0
                for record in first_agent_records
            ),
            "positive_first_agent_margin_sum": sum(
                max(0.0, record["best_rescue_order_normalized_margin"])
                for record in first_agent_records
            ),
            "first_agent_records": first_agent_records,
            "order_records": order_records,
        }

    def partial_linear_potential_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
        *,
        potential: str = "linear_surplus",
        floater_penalty: float = 1.0,
    ) -> dict:
        """Maximize a smooth scale-invariant one-floater potential."""
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        if potential not in {
            "linear_surplus",
            "normalized_utilitarian",
            "normalized_threshold",
            "normalized_nash",
            "normalized_harmonic",
        }:
            raise ValueError("unknown partial-state potential")
        if not np.isfinite(floater_penalty) or floater_penalty < 0:
            raise ValueError("floater_penalty must be finite and nonnegative")
        matrix = np.asarray(values, dtype=np.int64)
        totals, thresholds = self._tables(values)
        row_totals = matrix.sum(axis=1).astype(np.float64)
        best_potential = -np.inf
        best_selection_key = None
        best_candidates = []
        eligible_count = 0

        for floater, masks in enumerate(self.base_masks):
            valid = np.ones(len(masks), dtype=bool)
            own_values = np.empty((len(masks), self.n), dtype=np.int64)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                own_values[:, observer] = own
                valid &= own >= matrix[observer, floater]
                for target in range(self.n):
                    if observer != target:
                        valid &= own >= thresholds[observer, masks[:, target]]
            indices = np.flatnonzero(valid)
            eligible_count += len(indices)
            if not len(indices):
                continue
            normalized_own = own_values[indices] / row_totals[None, :]
            if potential == "linear_surplus":
                potential_values = normalized_own.sum(axis=1) - (
                    floater_penalty
                    * (matrix[:, floater] / row_totals).sum()
                )
            elif potential == "normalized_utilitarian":
                common_denominator = math.lcm(
                    *(int(total) for total in matrix.sum(axis=1))
                )
                weights = np.asarray(
                    [
                        common_denominator // int(total)
                        for total in matrix.sum(axis=1)
                    ],
                    dtype=object,
                )
                potential_values = (
                    own_values[indices].astype(object) @ weights
                )
            elif potential == "normalized_threshold":
                common_denominator = math.lcm(
                    *(int(total) for total in matrix.sum(axis=1))
                )
                weights = np.asarray(
                    [
                        common_denominator // int(total)
                        for total in matrix.sum(axis=1)
                    ],
                    dtype=object,
                )
                owner_thresholds = np.column_stack(
                    [
                        thresholds[observer, masks[indices, observer]]
                        for observer in range(self.n)
                    ]
                )
                potential_values = owner_thresholds.astype(object) @ weights
            elif potential == "normalized_nash":
                potential_values = np.asarray(
                    [
                        math.prod(int(value) for value in utilities)
                        for utilities in own_values[indices]
                    ],
                    dtype=object,
                )
            else:
                potential_values = -(1 / normalized_own).sum(axis=1)
            if potential in {
                "normalized_utilitarian",
                "normalized_threshold",
                "normalized_nash",
            }:
                local_selection_key = max(potential_values)
                denominator = (
                    common_denominator
                    if potential in {
                        "normalized_utilitarian",
                        "normalized_threshold",
                    }
                    else math.prod(row_totals)
                )
                local_best = float(local_selection_key / denominator)
                better = (
                    best_selection_key is None
                    or local_selection_key > best_selection_key
                )
                tied = local_selection_key == best_selection_key
                local_offsets = np.flatnonzero(
                    potential_values == local_selection_key
                )
            else:
                local_selection_key = float(potential_values.max())
                local_best = local_selection_key
                better = local_selection_key > best_potential
                tied = np.isclose(
                    local_selection_key,
                    best_potential,
                    rtol=0,
                    atol=1e-12,
                )
                local_offsets = np.flatnonzero(
                    np.isclose(
                        potential_values,
                        local_selection_key,
                        rtol=0,
                        atol=1e-12,
                    )
                )
            if better:
                best_selection_key = local_selection_key
                best_potential = local_best
                best_candidates = []
                tied = True
            if tied:
                for offset in local_offsets:
                    index = int(indices[offset])
                    best_candidates.append(
                        (
                            floater,
                            index,
                            masks[index].copy(),
                            tuple(int(value) for value in own_values[index]),
                        )
                    )

        if not best_candidates:
            raise AssertionError("profile has no eligible one-floater EFX base")
        records = []
        for floater, index, masks, utilities in best_candidates:
            host_margins = []
            hall_margins = []
            for host in range(self.n):
                enlarged = int(masks[host]) | (1 << floater)
                host_margins.append(
                    min(
                        (
                            totals[observer, masks[observer]]
                            - thresholds[observer, enlarged]
                        )
                        / row_totals[observer]
                        for observer in range(self.n)
                        if observer != host
                    )
                )
                complete_masks = [int(mask) for mask in masks]
                complete_masks[host] = enlarged
                for permutation in itertools.permutations(range(self.n)):
                    observer_margins = []
                    for observer in range(self.n):
                        assigned = permutation[observer]
                        own = totals[observer, complete_masks[assigned]]
                        required = max(
                            thresholds[observer, complete_masks[target]]
                            for target in range(self.n)
                            if target != assigned
                        )
                        observer_margins.append(
                            (own - required) / row_totals[observer]
                        )
                    hall_margins.append(min(observer_margins))
            records.append(
                {
                    "floater": floater,
                    "base_index": index,
                    "utilities": list(utilities),
                    "best_host_normalized_margin": float(max(host_margins)),
                    "insertable": bool(max(host_margins) >= 0),
                    "best_hall_normalized_margin": float(max(hall_margins)),
                    "hall_insertable": bool(max(hall_margins) >= 0),
                }
            )
        return {
            "potential": potential,
            "floater_penalty": floater_penalty,
            "eligible_base_count": eligible_count,
            "max_potential": best_potential,
            "maximizer_count": len(records),
            "insertable_maximizer_count": sum(
                record["insertable"] for record in records
            ),
            "best_maximizer_host_normalized_margin": max(
                record["best_host_normalized_margin"] for record in records
            ),
            "hall_insertable_maximizer_count": sum(
                record["hall_insertable"] for record in records
            ),
            "best_maximizer_hall_normalized_margin": max(
                record["best_hall_normalized_margin"] for record in records
            ),
            "maximizers": records,
        }

    def partial_pareto_threshold_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
    ) -> dict:
        """Maximize normalized owner threshold over Pareto-efficient states."""
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        matrix = np.asarray(values, dtype=np.int64)
        totals, thresholds = self._tables(values)
        row_totals = tuple(int(total) for total in matrix.sum(axis=1))
        common_denominator = math.lcm(*row_totals)
        weights = np.asarray(
            [common_denominator // total for total in row_totals],
            dtype=object,
        )
        candidates = []

        for floater, masks in enumerate(self.base_masks):
            valid = np.ones(len(masks), dtype=bool)
            own_values = np.empty((len(masks), self.n), dtype=np.int64)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                own_values[:, observer] = own
                valid &= own >= matrix[observer, floater]
                for target in range(self.n):
                    if observer != target:
                        valid &= own >= thresholds[observer, masks[:, target]]
            indices = np.flatnonzero(valid)
            if not len(indices):
                continue
            owner_thresholds = np.column_stack(
                [
                    thresholds[observer, masks[indices, observer]]
                    for observer in range(self.n)
                ]
            )
            scores = owner_thresholds.astype(object) @ weights
            for offset, index in enumerate(indices):
                candidates.append(
                    (
                        floater,
                        int(index),
                        masks[index].copy(),
                        tuple(int(value) for value in own_values[index]),
                        int(scores[offset]),
                    )
                )

        if not candidates:
            raise AssertionError("profile has no eligible one-floater EFX base")
        utility_vectors = sorted({candidate[3] for candidate in candidates}, reverse=True)
        frontier = []
        for utilities in utility_vectors:
            if any(
                all(
                    other[agent] >= utilities[agent]
                    for agent in range(1, self.n)
                )
                for other in frontier
            ):
                continue
            frontier.append(utilities)
        frontier_set = set(frontier)
        efficient = [
            candidate for candidate in candidates if candidate[3] in frontier_set
        ]
        best_score = max(candidate[4] for candidate in efficient)
        winners = [candidate for candidate in efficient if candidate[4] == best_score]

        records = []
        for floater, index, masks, utilities, _score in winners:
            host_margins = []
            hall_margins = []
            for host in range(self.n):
                enlarged = int(masks[host]) | (1 << floater)
                host_margins.append(
                    min(
                        (
                            totals[observer, masks[observer]]
                            - thresholds[observer, enlarged]
                        )
                        / row_totals[observer]
                        for observer in range(self.n)
                        if observer != host
                    )
                )
                complete_masks = [int(mask) for mask in masks]
                complete_masks[host] = enlarged
                for permutation in itertools.permutations(range(self.n)):
                    observer_margins = []
                    for observer in range(self.n):
                        assigned = permutation[observer]
                        own = totals[observer, complete_masks[assigned]]
                        required = max(
                            thresholds[observer, complete_masks[target]]
                            for target in range(self.n)
                            if target != assigned
                        )
                        observer_margins.append(
                            (own - required) / row_totals[observer]
                        )
                    hall_margins.append(min(observer_margins))
            records.append(
                {
                    "floater": floater,
                    "base_index": index,
                    "utilities": list(utilities),
                    "best_host_normalized_margin": float(max(host_margins)),
                    "insertable": bool(max(host_margins) >= 0),
                    "best_hall_normalized_margin": float(max(hall_margins)),
                    "hall_insertable": bool(max(hall_margins) >= 0),
                }
            )
        return {
            "potential": "pareto_threshold",
            "eligible_base_count": len(candidates),
            "pareto_frontier_utility_vector_count": len(frontier),
            "pareto_efficient_realization_count": len(efficient),
            "max_potential": best_score / common_denominator,
            "maximizer_count": len(records),
            "insertable_maximizer_count": sum(
                record["insertable"] for record in records
            ),
            "best_maximizer_host_normalized_margin": max(
                record["best_host_normalized_margin"] for record in records
            ),
            "hall_insertable_maximizer_count": sum(
                record["hall_insertable"] for record in records
            ),
            "best_maximizer_hall_normalized_margin": max(
                record["best_hall_normalized_margin"] for record in records
            ),
            "maximizers": records,
        }

    def partial_pareto_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
        *,
        rescue_radius: int | None = None,
        completion_radius: int | None = None,
    ) -> dict:
        """Compute the exact utility-vector frontier of eligible bases."""
        if rescue_radius is not None and (
            type(rescue_radius) is not int or rescue_radius < 0
        ):
            raise ValueError("rescue_radius must be a nonnegative integer")
        if completion_radius is not None and (
            type(completion_radius) is not int or completion_radius < 0
        ):
            raise ValueError("completion_radius must be a nonnegative integer")
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        matrix = np.asarray(values, dtype=np.int64)
        totals, thresholds = self._tables(values)
        by_utilities: dict[tuple[int, ...], dict] = {}
        eligible_by_floater = {}
        eligible_count = 0

        for floater, masks in enumerate(self.base_masks):
            valid = np.ones(len(masks), dtype=bool)
            own_values = np.empty((len(masks), self.n), dtype=np.int64)
            for observer in range(self.n):
                own = totals[observer, masks[:, observer]]
                own_values[:, observer] = own
                valid &= own >= matrix[observer, floater]
                for target in range(self.n):
                    if observer != target:
                        valid &= own >= thresholds[observer, masks[:, target]]
            indices = np.flatnonzero(valid)
            eligible_count += len(indices)
            if not len(indices):
                continue
            insertable = np.zeros(len(indices), dtype=bool)
            for host in range(self.n):
                host_valid = np.ones(len(indices), dtype=bool)
                enlarged = masks[indices, host] | (1 << floater)
                for observer in range(self.n):
                    if observer != host:
                        host_valid &= (
                            own_values[indices, observer]
                            >= thresholds[observer, enlarged]
                        )
                insertable |= host_valid
            for offset, index in enumerate(indices):
                utilities = tuple(int(item) for item in own_values[index])
                record = by_utilities.setdefault(
                    utilities,
                    {
                        "realization_count": 0,
                        "insertable_realization_count": 0,
                        "representative": {
                            "floater": floater,
                            "base_index": int(index),
                        },
                        "_realizations": [],
                    },
                )
                record["realization_count"] += 1
                record["insertable_realization_count"] += int(insertable[offset])
                record["_realizations"].append((floater, int(index)))
            eligible_by_floater[floater] = {
                "indices": indices,
                "utilities": own_values[indices].copy(),
                "insertable": insertable,
            }

        if not by_utilities:
            raise AssertionError("profile has no eligible one-floater EFX base")
        frontier: list[tuple[int, ...]] = []
        for utilities in sorted(by_utilities, reverse=True):
            if any(
                all(other[agent] >= utilities[agent] for agent in range(1, self.n))
                for other in frontier
            ):
                continue
            frontier.append(utilities)
        blocked = [
            utilities
            for utilities in frontier
            if by_utilities[utilities]["insertable_realization_count"] == 0
        ]
        products = {
            utilities: math.prod(utilities) for utilities in by_utilities
        }
        maximum_product = max(products.values())
        maximum_product_vectors = [
            utilities
            for utilities, value in products.items()
            if value == maximum_product
        ]
        blocked_maximum_product = (
            max(products[utilities] for utilities in blocked)
            if blocked
            else None
        )
        result = {
            "eligible_base_count": eligible_count,
            "distinct_utility_vector_count": len(by_utilities),
            "pareto_frontier_utility_vector_count": len(frontier),
            "insertable_pareto_frontier_utility_vector_count": (
                len(frontier) - len(blocked)
            ),
            "blocked_pareto_frontier_utility_vector_count": len(blocked),
            "blocked_pareto_frontier": [
                {
                    "utilities": list(utilities),
                    **{
                        key: value
                        for key, value in by_utilities[utilities].items()
                        if not key.startswith("_")
                    },
                }
                for utilities in blocked[:50]
            ],
            "maximum_product": maximum_product,
            "maximum_product_vector_count": len(maximum_product_vectors),
            "maximum_product_has_insertable_realization": any(
                by_utilities[utilities]["insertable_realization_count"] > 0
                for utilities in maximum_product_vectors
            ),
            "blocked_pareto_maximum_product": blocked_maximum_product,
            "blocked_pareto_to_maximum_product_ratio": (
                blocked_maximum_product / maximum_product
                if blocked_maximum_product is not None
                else None
            ),
        }
        if completion_radius is not None:
            popcounts = self.bits.sum(axis=1)
            completion_targets = {}
            for utilities in maximum_product_vectors:
                for floater, base_index in by_utilities[utilities][
                    "_realizations"
                ]:
                    eligible = eligible_by_floater[floater]
                    candidate_masks = self.base_masks[floater][
                        eligible["indices"]
                    ]
                    reference_masks = self.base_masks[floater][base_index]
                    matching_good_count = np.zeros(
                        len(eligible["indices"]),
                        dtype=np.int64,
                    )
                    for agent in range(self.n):
                        matching_good_count += popcounts[
                            candidate_masks[:, agent] & reference_masks[agent]
                        ]
                    distances = self.m - 1 - matching_good_count
                    for offset in np.flatnonzero(
                        (distances <= completion_radius)
                        & eligible["insertable"]
                    ):
                        target_key = (floater, int(eligible["indices"][offset]))
                        target_utilities = tuple(
                            int(value) for value in eligible["utilities"][offset]
                        )
                        candidate = {
                            "distance": int(distances[offset]),
                            "floater": floater,
                            "base_index": target_key[1],
                            "utilities": list(target_utilities),
                            "utility_product": math.prod(target_utilities),
                        }
                        previous = completion_targets.get(target_key)
                        if previous is None or candidate["distance"] < previous[
                            "distance"
                        ]:
                            completion_targets[target_key] = candidate
            ordered_targets = sorted(
                completion_targets.values(),
                key=lambda target: (
                    target["distance"],
                    -target["utility_product"],
                    target["floater"],
                    target["base_index"],
                ),
            )
            result.update(
                {
                    "completion_radius": completion_radius,
                    "completion_scope": (
                        "same floater and good-owner Hamming distance from a "
                        "maximum-product realization"
                    ),
                    "maximum_product_completion_within_radius": bool(
                        ordered_targets
                    ),
                    "maximum_product_completion_target_count": len(
                        ordered_targets
                    ),
                    "nearest_maximum_product_completion": (
                        ordered_targets[0] if ordered_targets else None
                    ),
                }
            )

        if rescue_radius is None:
            return result

        popcounts = self.bits.sum(axis=1)
        rescue_records = []
        for utilities in blocked:
            blocked_product = math.prod(utilities)
            best_rescue = None
            strongest_target = None
            for floater, base_index in by_utilities[utilities]["_realizations"]:
                eligible = eligible_by_floater[floater]
                candidate_masks = self.base_masks[floater][eligible["indices"]]
                reference_masks = self.base_masks[floater][base_index]
                matching_good_count = np.zeros(
                    len(eligible["indices"]),
                    dtype=np.int64,
                )
                for agent in range(self.n):
                    matching_good_count += popcounts[
                        candidate_masks[:, agent] & reference_masks[agent]
                    ]
                distances = self.m - 1 - matching_good_count
                for offset in np.flatnonzero(distances <= rescue_radius):
                    target_utilities = tuple(
                        int(value) for value in eligible["utilities"][offset]
                    )
                    target_product = math.prod(target_utilities)
                    target_insertable = bool(eligible["insertable"][offset])
                    target = {
                        "distance": int(distances[offset]),
                        "floater": floater,
                        "base_index": int(eligible["indices"][offset]),
                        "utilities": list(target_utilities),
                        "utility_product": target_product,
                        "insertable": target_insertable,
                    }
                    if strongest_target is None or (
                        target["utility_product"],
                        target["insertable"],
                        -target["distance"],
                        -target["base_index"],
                    ) > (
                        strongest_target["utility_product"],
                        strongest_target["insertable"],
                        -strongest_target["distance"],
                        -strongest_target["base_index"],
                    ):
                        strongest_target = target
                    if not (
                        target_product > blocked_product
                        or (
                            target_product == blocked_product
                            and target_insertable
                        )
                    ):
                        continue
                    candidate = target
                    if best_rescue is None or (
                        candidate["distance"],
                        -candidate["utility_product"],
                        not candidate["insertable"],
                        candidate["base_index"],
                    ) < (
                        best_rescue["distance"],
                        -best_rescue["utility_product"],
                        not best_rescue["insertable"],
                        best_rescue["base_index"],
                    ):
                        best_rescue = candidate
            rescue_records.append(
                {
                    "utilities": list(utilities),
                    "utility_product": blocked_product,
                    "strongest_bounded_target": strongest_target,
                    "strongest_bounded_product_surplus": (
                        strongest_target["utility_product"] - blocked_product
                    ),
                    "bounded_rescue": best_rescue,
                }
            )
        rescued_count = sum(
            record["bounded_rescue"] is not None for record in rescue_records
        )
        result.update(
            {
                "rescue_radius": rescue_radius,
                "rescue_scope": "same floater and good-owner Hamming distance",
                "blocked_pareto_frontier_with_bounded_rescue_count": (
                    rescued_count
                ),
                "blocked_pareto_frontier_without_bounded_rescue_count": (
                    len(rescue_records) - rescued_count
                ),
                "blocked_pareto_rescues": rescue_records,
            }
        )
        return result

    def complete_efx0_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
    ) -> dict:
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        totals, thresholds = self._tables(values)
        row_totals = np.asarray([sum(row) for row in values], dtype=np.float64)
        margin = np.full(
            len(self.complete_masks),
            np.iinfo(np.int64).max,
            dtype=np.int64,
        )
        normalized_margin = np.full(len(self.complete_masks), np.inf)
        for observer in range(self.n):
            own = totals[observer, self.complete_masks[:, observer]]
            for target in range(self.n):
                if observer == target:
                    continue
                slack = own - thresholds[observer, self.complete_masks[:, target]]
                margin = np.minimum(margin, slack)
                normalized_margin = np.minimum(
                    normalized_margin,
                    slack / row_totals[observer],
                )
        valid = margin >= 0
        shape_codes, shape_counts = np.unique(
            self.complete_shape_codes[valid],
            return_counts=True,
        )
        return {
            "complete_efx0_count": int(valid.sum()),
            "complete_efx0_count_by_shape": {
                str(code): int(count)
                for code, count in zip(shape_codes, shape_counts)
            },
            "positive_margin_sum": int((margin[valid] + 1).sum()),
            "normalized_margin_sum": float(normalized_margin[valid].sum()),
        }

    def complete_efx0_family_landscape(
        self,
        raw_values: list[list[int]] | tuple[tuple[int, ...], ...],
        *,
        shape_codes: tuple[int, ...] = (),
        singleton_goods: tuple[int, ...] = (),
    ) -> dict:
        values = validate_values(
            raw_values,
            expected_n=self.n,
            expected_m=self.m,
            lower=1,
        )
        shapes = tuple(sorted(set(shape_codes)))
        singletons = tuple(sorted(set(singleton_goods)))
        if (
            any(type(code) is not int or code < 0 for code in shapes)
            or any(
                type(good) is not int or not 0 <= good < self.m
                for good in singletons
            )
            or not (shapes or singletons)
        ):
            raise ValueError("at least one valid shape or singleton good is required")
        key = (shapes, singletons)
        indices = self._complete_family_indices.get(key)
        if indices is None:
            selected = np.isin(self.complete_shape_codes, shapes)
            for good in singletons:
                selected |= np.any(
                    self.complete_masks == (1 << good),
                    axis=1,
                )
            indices = np.flatnonzero(selected)
            self._complete_family_indices[key] = indices

        totals, thresholds = self._tables(values)
        masks = self.complete_masks[indices]
        row_totals = np.asarray([sum(row) for row in values], dtype=np.float64)
        margin = np.full(
            len(masks),
            np.iinfo(np.int64).max,
            dtype=np.int64,
        )
        normalized_margin = np.full(len(masks), np.inf)
        for observer in range(self.n):
            own = totals[observer, masks[:, observer]]
            for target in range(self.n):
                if observer == target:
                    continue
                slack = own - thresholds[observer, masks[:, target]]
                margin = np.minimum(margin, slack)
                normalized_margin = np.minimum(
                    normalized_margin,
                    slack / row_totals[observer],
                )
        valid = margin >= 0
        valid_masks = masks[valid]
        valid_shape_codes = self.complete_shape_codes[indices][valid]
        singleton_branch = np.zeros(len(valid_masks), dtype=bool)
        for good in singletons:
            singleton_branch |= np.any(
                valid_masks == (1 << good),
                axis=1,
            )
        return {
            "complete_efx0_family_count": int(valid.sum()),
            "complete_efx0_shape_branch_count": int(
                np.isin(valid_shape_codes, shapes).sum()
            ),
            "complete_efx0_singleton_branch_count": int(singleton_branch.sum()),
            "family_allocation_count": len(indices),
            "positive_margin_sum": int((margin[valid] + 1).sum()),
            "normalized_margin_sum": float(normalized_margin[valid].sum()),
        }
