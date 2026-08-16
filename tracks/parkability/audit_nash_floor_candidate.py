#!/usr/bin/env python3
"""Adversarial audit of a Nash-product floor-allocation proof candidate."""

from __future__ import annotations

import argparse
import itertools
import json
import random
from pathlib import Path

import numpy as np

try:
    from .anneal import atomic_json
    from .fast_count import FastParkability
except ImportError:
    from anneal import atomic_json
    from fast_count import FastParkability


N = 4
M = 9
FAVORITE = 0
SCHEMA = "nash-floor-candidate-audit-v1"
SOURCE_FILES = (
    "efx49_common_favorite_real_shape6111_session1.json",
    "efx49_universal_threshold_distinct_reps_cegar_session1.json",
    "efx49_universal_threshold_balanced_envelope_cegar_session1.json",
    "efx49_universal_threshold_balanced_cegar_session1.json",
)


def universal_threshold_failure(row: tuple[int, ...]) -> bool:
    favorite = row[FAVORITE]
    residual = sorted(row[1:], reverse=True)
    return (
        residual[4] + residual[5] + residual[6] > favorite
        and (
            residual[2] + residual[6] > favorite
            or residual[3] + residual[4] > favorite
        )
    )


def half_favorite_matching(values: tuple[tuple[int, ...], ...]) -> tuple[int, ...] | None:
    for goods in itertools.permutations(range(1, M), N):
        if all(2 * values[agent][goods[agent]] > values[agent][FAVORITE]
               for agent in range(N)):
            return goods
    return None


class NashFloorAudit:
    def __init__(self) -> None:
        counter = FastParkability(n=N, m=M)
        selected = counter.complete_shape_codes == 3222
        self.masks = counter.complete_masks[selected]
        if len(self.masks) != 30240:
            raise AssertionError("balanced labeled-allocation census changed")
        self.bits = counter.bits
        sizes = self.bits[self.masks].sum(axis=2)
        self.triple_owners = sizes.argmax(axis=1)
        favorite_owners = ((self.masks & (1 << FAVORITE)) != 0).argmax(axis=1)
        self.favorite_in_pair = sizes[
            np.arange(len(self.masks)), favorite_owners
        ] == 2

    def allocation_record(
        self,
        index: int,
        totals: np.ndarray,
        thresholds: np.ndarray,
    ) -> dict:
        masks = self.masks[index]
        bundles = [
            [good for good in range(M) if int(mask) & (1 << good)]
            for mask in masks
        ]
        own = [int(totals[agent, masks[agent]]) for agent in range(N)]
        violations = []
        for observer in range(N):
            for target in range(N):
                if observer == target:
                    continue
                threshold = int(thresholds[observer, masks[target]])
                if own[observer] < threshold:
                    violations.append({
                        "observer": observer,
                        "target": target,
                        "own_value": own[observer],
                        "target_efx_threshold": threshold,
                        "deficit": threshold - own[observer],
                    })
        return {
            "bundles_by_owner": bundles,
            "owner_utilities": own,
            "nash_product": int(np.prod(own, dtype=np.int64)),
            "efx_violations": violations,
        }

    def evaluate(self, values: tuple[tuple[int, ...], ...]) -> dict:
        if any(
            row[FAVORITE] <= max(row[1:])
            or not universal_threshold_failure(row)
            for row in values
        ):
            raise ValueError("profile is outside the strict universal-threshold cell")
        representatives = half_favorite_matching(values)
        if representatives is None:
            raise ValueError("half-favorite graph has no saturating matching")

        matrix = np.asarray(values, dtype=np.int64)
        totals = matrix @ self.bits.T
        maximum = int(matrix.max()) + 1
        masked = np.where(self.bits[None, :, :], matrix[:, None, :], maximum)
        minima = masked.min(axis=2)
        minima[:, 0] = 0
        thresholds = totals - minima

        own = np.stack(
            [totals[agent, self.masks[:, agent]] for agent in range(N)],
            axis=1,
        )
        floor = np.all(own >= matrix[:, FAVORITE], axis=1)
        if not np.any(floor):
            return {
                "half_favorite_representatives": list(representatives),
                "floor_allocation_count": 0,
                "status": "NO_FLOOR_ALLOCATION",
            }

        products = np.prod(own, axis=1, dtype=np.int64)
        surpluses = own - matrix[:, FAVORITE]
        surplus_products = np.prod(surpluses, axis=1, dtype=np.int64)
        efx = np.ones(len(self.masks), dtype=bool)
        for observer in range(N):
            for target in range(N):
                if observer != target:
                    efx &= (
                        own[:, observer]
                        >= thresholds[observer, self.masks[:, target]]
                    )
        rows = np.arange(len(self.masks))
        triple_masks = self.masks[rows, self.triple_owners]
        triple_owner_thresholds = thresholds[self.triple_owners, triple_masks]
        triple_owner_favorites = matrix[self.triple_owners, FAVORITE]
        peelable_triple = triple_owner_thresholds >= triple_owner_favorites
        favorite_pair_floor = floor & self.favorite_in_pair
        favorite_pair_bad = favorite_pair_floor & ~efx
        terminal_bad = favorite_pair_bad & ~peelable_triple
        first_terminal_bad = (
            int(np.flatnonzero(terminal_bad)[0]) if np.any(terminal_bad) else None
        )
        floor_efx = floor & efx
        best_product = int(products[floor].max())
        maximizers = floor & (products == best_product)
        maximizer_count = int(maximizers.sum())
        efx_maximizer_count = int((maximizers & efx).sum())
        best_efx_product = (
            int(products[floor_efx].max()) if np.any(floor_efx) else None
        )
        best_non_efx_product = (
            int(products[floor & ~efx].max()) if np.any(floor & ~efx) else None
        )
        first_maximizer = int(np.flatnonzero(maximizers)[0])
        first_best_efx = (
            int(np.flatnonzero(floor_efx & (products == best_efx_product))[0])
            if best_efx_product is not None
            else None
        )
        best_surplus_product = int(surplus_products[floor].max())
        surplus_maximizers = floor & (surplus_products == best_surplus_product)
        surplus_maximizer_count = int(surplus_maximizers.sum())
        efx_surplus_maximizer_count = int((surplus_maximizers & efx).sum())
        return {
            "half_favorite_representatives": list(representatives),
            "floor_allocation_count": int(floor.sum()),
            "floor_efx_allocation_count": int(floor_efx.sum()),
            "favorite_pair_floor_allocation_count": int(favorite_pair_floor.sum()),
            "favorite_pair_non_efx_allocation_count": int(favorite_pair_bad.sum()),
            "nonpeelable_favorite_pair_non_efx_count": int(terminal_bad.sum()),
            "first_nonpeelable_favorite_pair_non_efx": (
                self.allocation_record(first_terminal_bad, totals, thresholds)
                if first_terminal_bad is not None
                else None
            ),
            "maximum_nash_product": best_product,
            "nash_maximizer_count": maximizer_count,
            "efx_nash_maximizer_count": efx_maximizer_count,
            "best_efx_nash_product": best_efx_product,
            "best_non_efx_nash_product": best_non_efx_product,
            "first_nash_maximizer": self.allocation_record(
                first_maximizer,
                totals,
                thresholds,
            ),
            "first_best_efx_allocation": (
                self.allocation_record(first_best_efx, totals, thresholds)
                if first_best_efx is not None
                else None
            ),
            "weak_candidate_holds": efx_maximizer_count > 0,
            "strong_candidate_holds": efx_maximizer_count == maximizer_count,
            "maximum_favorite_surplus_product": best_surplus_product,
            "favorite_surplus_maximizer_count": surplus_maximizer_count,
            "efx_favorite_surplus_maximizer_count": efx_surplus_maximizer_count,
            "weak_favorite_surplus_candidate_holds": (
                efx_surplus_maximizer_count > 0
            ),
            "strong_favorite_surplus_candidate_holds": (
                efx_surplus_maximizer_count == surplus_maximizer_count
            ),
            "status": (
                "NASH_CANDIDATE_PASSED"
                if efx_maximizer_count == maximizer_count
                else "STRONG_NASH_CANDIDATE_FALSIFIED"
                if efx_maximizer_count > 0
                else "WEAK_NASH_CANDIDATE_FALSIFIED"
            ),
        }


def load_source_profile(path: Path) -> tuple[tuple[int, ...], ...]:
    payload = json.loads(path.read_text())
    raw = payload.get("values")
    if raw is None:
        trace = payload.get("trace", [])
        raw = trace[-1]["values"]
    return tuple(tuple(map(int, row)) for row in raw)


def random_row(rng: random.Random, max_favorite: int) -> tuple[int, ...]:
    while True:
        favorite = rng.randint(4, max_favorite)
        residual = [rng.randint(1, favorite - 1) for _ in range(M - 1)]
        row = (favorite,) + tuple(residual)
        if universal_threshold_failure(row):
            return row


def random_profile(
    rng: random.Random,
    max_favorite: int,
) -> tuple[tuple[int, ...], ...]:
    while True:
        values = tuple(random_row(rng, max_favorite) for _ in range(N))
        if half_favorite_matching(values) is not None:
            return values


def audit(results_dir: Path, random_profiles: int, seed: int, max_favorite: int) -> dict:
    engine = NashFloorAudit()
    source_records = []
    weak_failures = []
    strong_failures = []
    weak_surplus_failures = []
    strong_surplus_failures = []
    no_floor = []
    minimum_efx_share = 1.0

    for filename in SOURCE_FILES:
        values = load_source_profile(results_dir / filename)
        record = engine.evaluate(values)
        record["source"] = filename
        source_records.append(record)

    rng = random.Random(seed)
    for profile_index in range(random_profiles):
        values = random_profile(rng, max_favorite)
        record = engine.evaluate(values)
        if record["status"] == "NO_FLOOR_ALLOCATION":
            no_floor.append({"profile_index": profile_index, "values": values})
            continue
        share = record["efx_nash_maximizer_count"] / record["nash_maximizer_count"]
        minimum_efx_share = min(minimum_efx_share, share)
        if not record["weak_candidate_holds"]:
            weak_failures.append({
                "profile_index": profile_index,
                "values": values,
                "landscape": record,
            })
        elif not record["strong_candidate_holds"]:
            strong_failures.append({
                "profile_index": profile_index,
                "values": values,
                "landscape": record,
            })
        if not record["weak_favorite_surplus_candidate_holds"]:
            weak_surplus_failures.append({
                "profile_index": profile_index,
                "values": values,
                "landscape": record,
            })
        elif not record["strong_favorite_surplus_candidate_holds"]:
            strong_surplus_failures.append({
                "profile_index": profile_index,
                "values": values,
                "landscape": record,
            })

    all_records = source_records
    source_weak_failures = sum(not r.get("weak_candidate_holds", False) for r in all_records)
    source_strong_failures = sum(not r.get("strong_candidate_holds", False) for r in all_records)
    status = (
        "WEAK_NASH_CANDIDATE_FALSIFIED"
        if weak_failures or source_weak_failures or no_floor
        else "STRONG_NASH_CANDIDATE_FALSIFIED"
        if strong_failures or source_strong_failures
        else "NASH_FLOOR_CANDIDATE_STRESS_AUDIT_PASSED"
    )
    return {
        "schema": SCHEMA,
        "status": status,
        "cell": {
            "agents": N,
            "goods": M,
            "common_strict_favorite": FAVORITE,
            "complete_shape": [3, 2, 2, 2],
            "balanced_labeled_allocation_count": len(engine.masks),
            "conditions": [
                "exact universal owner-threshold failure for every row",
                "the strict half-favorite graph saturates all four agents",
            ],
        },
        "candidate": (
            "Every Nash-product-maximal balanced allocation among those giving "
            "each owner at least the value of the common favorite is EFX."
        ),
        "source_profile_records": source_records,
        "deterministic_random_profiles": random_profiles,
        "random_seed": seed,
        "maximum_random_favorite": max_favorite,
        "random_profiles_without_floor_allocation": len(no_floor),
        "random_weak_candidate_failures": len(weak_failures),
        "random_strong_candidate_failures": len(strong_failures),
        "random_weak_favorite_surplus_candidate_failures": len(
            weak_surplus_failures
        ),
        "random_strong_favorite_surplus_candidate_failures": len(
            strong_surplus_failures
        ),
        "minimum_random_efx_share_among_nash_maximizers": minimum_efx_share,
        "first_no_floor_profile": no_floor[:1],
        "first_weak_failure": weak_failures[:1],
        "first_strong_failure": strong_failures[:1],
        "first_weak_favorite_surplus_failure": weak_surplus_failures[:1],
        "first_strong_favorite_surplus_failure": strong_surplus_failures[:1],
        "scope_warning": (
            "This finite deterministic audit can falsify the candidate but "
            "cannot prove its cap-free real-valued statement."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, default=Path("results"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--random-profiles", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260731)
    parser.add_argument("--max-favorite", type=int, default=80)
    args = parser.parse_args()
    if args.random_profiles < 0:
        parser.error("random profile count cannot be negative")
    if args.max_favorite < 4:
        parser.error("maximum favorite must be at least four")
    result = audit(
        args.results_dir,
        args.random_profiles,
        args.seed,
        args.max_favorite,
    )
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
