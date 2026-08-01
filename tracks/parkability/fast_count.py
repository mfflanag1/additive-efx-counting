#!/usr/bin/env python3
"""Vectorized exact parkability counts for heuristic counterexample search."""

from __future__ import annotations

import itertools

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
            "order_records": order_records,
        }

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
