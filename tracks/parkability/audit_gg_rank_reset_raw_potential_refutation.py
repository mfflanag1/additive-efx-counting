#!/usr/bin/env python3
"""Exact audit of the raw missing-owner coordinate obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
GOODS = ("r1", "r2", "q1", "q2", "c1", "c2", "s1", "s2", "f")
BASE = {
    "r": ("r1", "r2"),
    "q": ("q1", "q2"),
    "c": ("c1", "c2"),
    "s": ("s1", "s2"),
}

# Integral parts have slack at least 1 in every strict comparison used below.
# Distinct dyadic tags make all subset sums injective without changing a sign.
MAJOR = {
    "r": (5, 5, 6, 4, 6, 5, 6, 2, 1),
    "q": (2, 2, 6, 4, 3, 1, 4, 4, 3),
    "c": (1, 1, 1, 8, 6, 4, 1, 1, Fraction(3, 2)),
    "s": (6, 6, 1, 2, 1, 1, 5, 5, 2),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valuation() -> dict[str, dict[str, Fraction]]:
    denominator = 1 << 50
    return {
        agent: {
            good: Fraction(MAJOR[agent][index])
            + Fraction(1 << (index + agent_index * len(GOODS)), denominator)
            for index, good in enumerate(GOODS)
        }
        for agent_index, agent in enumerate(AGENTS)
    }


def value(values, agent: str, bundle) -> Fraction:
    return sum((values[agent][good] for good in bundle), Fraction())


def threshold(values, agent: str, bundle) -> Fraction:
    if not bundle:
        return Fraction()
    return value(values, agent, bundle) - min(values[agent][good] for good in bundle)


def common_safe(values, base_value, bundle) -> bool:
    return all(threshold(values, agent, bundle) <= base_value[agent] for agent in AGENTS)


def response_neighborhood(values, base_value, bundle) -> tuple[str, ...]:
    assert common_safe(values, base_value, bundle)
    return tuple(
        agent for agent in AGENTS
        if value(values, agent, bundle) > base_value[agent]
    )


def maximum_rank(neighborhoods: dict[str, tuple[str, ...]]) -> int:
    targets = tuple(neighborhoods)
    for rank in range(len(targets), 0, -1):
        for chosen_targets in itertools.combinations(targets, rank):
            for sources in itertools.permutations(AGENTS, rank):
                if all(
                    source in neighborhoods[target]
                    for target, source in zip(chosen_targets, sources)
                ):
                    return rank
    return 0


def subset_sum_injective(row: dict[str, Fraction]) -> bool:
    sums = set()
    for bits in itertools.product((0, 1), repeat=len(GOODS)):
        total = sum(
            (row[good] for good, bit in zip(GOODS, bits) if bit),
            Fraction(),
        )
        if total in sums:
            return False
        sums.add(total)
    return True


def is_efx(values, allocation) -> bool:
    return all(
        value(values, observer, allocation[observer])
        >= threshold(values, observer, allocation[target])
        for observer in AGENTS
        for target in AGENTS
    )


def run(root: Path) -> dict:
    values = valuation()
    base_value = {
        agent: value(values, agent, BASE[agent]) for agent in AGENTS
    }
    assert all(amount > 0 for row in values.values() for amount in row.values())
    assert all(subset_sum_injective(values[agent]) for agent in AGENTS)
    base_allocation = {**BASE, "_": ("f",)}
    assert is_efx(values, base_allocation)
    assert all(base_value[agent] > values[agent]["f"] for agent in AGENTS)

    bundles = {
        "A_r": ("q1", "c2"),
        "A_c": ("q2", "s2", "f"),
        "A_s": ("r1", "r2"),
        "W": ("c1", "s1"),
    }
    assert set().union(*map(set, bundles.values())) == set(GOODS)
    assert sum(map(len, bundles.values())) == len(GOODS)
    assert all(common_safe(values, base_value, bundle) for bundle in bundles.values())

    neighborhoods = {
        name: response_neighborhood(values, base_value, bundle)
        for name, bundle in bundles.items()
    }
    expected = {
        "A_r": ("r",),
        "A_c": ("q", "c"),
        "A_s": ("s",),
        "W": ("r",),
    }
    assert neighborhoods == expected
    assert maximum_rank(neighborhoods) == 3

    before = {
        "r": bundles["A_r"],
        "q": bundles["W"],
        "c": bundles["A_c"],
        "s": bundles["A_s"],
        "_": (),
    }
    after = {
        "r": bundles["W"],
        "q": bundles["A_c"],
        "c": bundles["A_r"],
        "s": bundles["A_s"],
        "_": (),
    }
    assert not is_efx(values, before)
    assert not is_efx(values, after)
    assert value(values, "q", bundles["W"]) < threshold(
        values, "q", bundles["A_c"]
    )

    old_residual = value(values, "q", bundles["W"])
    new_residual = value(values, "c", bundles["A_r"])
    assert new_residual < old_residual

    scaled = {
        agent: {
            good: amount * (2 if agent == "c" else 1)
            for good, amount in row.items()
        }
        for agent, row in values.items()
    }
    scaled_base = {
        agent: value(scaled, agent, BASE[agent]) for agent in AGENTS
    }
    scaled_neighborhoods = {
        name: response_neighborhood(scaled, scaled_base, bundle)
        for name, bundle in bundles.items()
    }
    assert scaled_neighborhoods == neighborhoods
    assert is_efx(scaled, base_allocation)
    scaled_new_residual = value(scaled, "c", bundles["A_r"])
    assert scaled_new_residual > old_residual

    script = Path(__file__).resolve()
    theorem = root / "results/GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md"
    return {
        "schema": "gg-rank-reset-raw-potential-refutation-v1",
        "status": "EXACT_SCALE_REFUTATION",
        "positive_additive": True,
        "subset_sum_injective": True,
        "base_efx": True,
        "charity_dominated": True,
        "common_safe_partition": {name: list(bundle) for name, bundle in bundles.items()},
        "response_neighborhoods": {
            name: list(sources) for name, sources in neighborhoods.items()
        },
        "maximum_response_rank_before": 3,
        "maximum_response_rank_after": 3,
        "represented_owner_union_size_before": 4,
        "represented_owner_union_size_after": 4,
        "missing_owner_before": "q",
        "missing_owner_after": "c",
        "raw_residual_before": str(old_residual),
        "raw_residual_after": str(new_residual),
        "raw_residual_after_c_row_scaled_by_2": str(scaled_new_residual),
        "response_relation_unchanged_by_scaling": True,
        "both_displayed_states_non_efx": True,
        "claim_boundary": (
            "exact positive subset-sum-injective counterexample to comparing "
            "raw residual utilities across a rank-preserving hole change; it "
            "refutes the proposed fourth potential coordinate, not GG closure, "
            "and does not assert generalized PI-freeness or global lex maximality"
        ),
        "smallest_repair": (
            "replace raw current-hole utility by an owner-indexed scale-invariant "
            "residual ledger, and retain historical rank/owner-union maxima across resets"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results/gg_rank_reset_raw_potential_refutation_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
