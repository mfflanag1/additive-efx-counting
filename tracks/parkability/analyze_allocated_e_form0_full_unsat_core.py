#!/usr/bin/env python3
"""Decode the categorized allocated-E R2 core into desired-core families."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from .run_allocated_e_capture_rank_three_cegar import (
    ALLOCATED_E_BASE, FIXED_CORES,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "results" / "allocated_e_form0_full_unsat_core.json"


def generalized_self_descriptors():
    rows = []
    charity = tuple(ALLOCATED_E_BASE["charity"])
    charity_set = set(charity)
    for owner in OWNERS:
        universe = (*tuple(ALLOCATED_E_BASE[owner]), *charity)
        for mask in range(1, 1 << len(universe)):
            goods = tuple(
                good for index, good in enumerate(universe)
                if mask & (1 << index)
            )
            if set(goods) & charity_set:
                rows.append(((owner, goods),))
    return rows


def anchored_descriptors():
    base_owner = {
        good: owner
        for owner, goods in ALLOCATED_E_BASE.items()
        for good in goods
    }
    excluded = {}
    fixed_sources = tuple(FIXED_CORES)
    for source in OWNERS:
        available_fixed = tuple(owner for owner in fixed_sources if owner != source)
        for subset_size in range(1, len(available_fixed) + 1):
            for fixed_subset in itertools.combinations(available_fixed, subset_size):
                vertices = set(fixed_subset) | {source}
                fixed_union = set().union(*(set(FIXED_CORES[owner]) for owner in fixed_subset))
                if any(base_owner[good] not in vertices | {"charity"} for good in fixed_union):
                    continue
                complement = tuple(good for good in GOODS if good not in fixed_union)
                for mask in range(1, 1 << len(complement)):
                    goods = tuple(
                        good for index, good in enumerate(complement)
                        if mask & (1 << index)
                    )
                    if any(base_owner[good] not in vertices | {"charity"} for good in goods):
                        continue
                    key = (source, tuple(sorted(goods)))
                    excluded.setdefault(key, set()).add(tuple(sorted(fixed_subset)))
    rows = []
    for source, goods in sorted(excluded):
        fixed_subset = min(excluded[(source, goods)], key=lambda row: (len(row), row))
        fixed = tuple(
            (owner, tuple(FIXED_CORES[owner]))
            for owner in fixed_subset
        )
        # The formula forbids the alternative response because at least one
        # fixed-core subset closes with it. Report a smallest canonical one.
        rows.append(((source, goods), *fixed))
    return rows


def pairwise_descriptors():
    rows = []
    for left, right in itertools.combinations(OWNERS, 2):
        allowed = tuple(
            good for owner in (left, right, "charity")
            for good in ALLOCATED_E_BASE[owner]
        )
        for assignment in itertools.product(range(3), repeat=len(allowed)):
            left_core = tuple(
                good for good, slot in zip(allowed, assignment, strict=True)
                if slot == 1
            )
            right_core = tuple(
                good for good, slot in zip(allowed, assignment, strict=True)
                if slot == 2
            )
            if left_core and right_core:
                rows.append(((left, left_core), (right, right_core)))
    return rows


def serial(family):
    return [[source, list(goods)] for source, goods in family]


def run():
    source = json.loads(SOURCE.read_text())
    self_rows = generalized_self_descriptors()
    anchored_rows = anchored_descriptors()
    pair_rows = pairwise_descriptors()
    families = []
    numerical = []
    for row in source["core"]:
        if row["kind"] == "higher_family":
            families.append({"kind": "higher", "family": row["signature"]})
            continue
        category, *suffix = row["category"].split(":")
        if category == "generalized_self_pi":
            families.append({"kind": "self", "family": serial(self_rows[int(suffix[0])])})
        elif category == "fixed_anchored_pi":
            families.append({"kind": "anchored", "family": serial(anchored_rows[int(suffix[0])])})
        elif category == "pairwise_closed_pi":
            families.append({"kind": "pair", "family": serial(pair_rows[int(suffix[0])])})
        else:
            numerical.append({
                "category": row["category"],
                "formula": row["formula"],
            })
    return {
        "schema": "allocated-e-form0-full-core-analysis-v1",
        "status": "CORE_DECODED",
        "source": "results/allocated_e_form0_full_unsat_core.json",
        "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "core_count": source["core_count"],
        "pi_family_count": len(families),
        "pi_family_kind_counts": dict(sorted(Counter(row["kind"] for row in families).items())),
        "numerical_premise_count": len(numerical),
        "numerical_category_counts": dict(sorted(Counter(
            row["category"].split(":")[0] for row in numerical
        ).items())),
        "pi_families": families,
        "numerical_premises": numerical,
        "claim_boundary": (
            "Human-readable decoding of one bounded SMT core. Anchored rows "
            "use a smallest fixed-core family witnessing the exclusion. This "
            "is a proof-discovery map, not a cap-free proof."
        ),
    }


def main():
    output = ROOT / "results" / "allocated_e_form0_full_unsat_core_analysis.json"
    result = run()
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "core_count": result["core_count"],
        "pi_family_count": result["pi_family_count"],
        "numerical_premise_count": result["numerical_premise_count"],
        "kind_counts": result["pi_family_kind_counts"],
    }, indent=2))


if __name__ == "__main__":
    main()
