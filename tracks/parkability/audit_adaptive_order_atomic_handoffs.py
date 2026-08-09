#!/usr/bin/env python3
"""Exhaustive handoff audit for the six strict alternating-order countermodels."""

from __future__ import annotations

import json
import itertools
from pathlib import Path

SCHEMA = "alternating-adaptive-order-atomic-handoff-audit-v1"
N = 4
M = 7
AGENTS = ("p", "r", "s", "q")
GOODS = ("tr", "br", "tq", "bq", "x", "y", "f")
Owner = tuple[int | None, ...]
BASE_OWNER: Owner = (1, 1, 3, 3, 0, 2, None)
ALL_OWNERS: tuple[Owner, ...] = tuple(
    tuple(None if assigned == N else assigned for assigned in raw)
    for raw in itertools.product(range(N + 1), repeat=M)
)
ROOT_FLIP_OWNERS: dict[str, Owner] = {
    "p_root_first": (2, None, 3, 3, 0, 1, 2),
    "p_root_second": (0, None, 2, 2, 3, 1, 0),
    "s_root_first": (1, 1, 0, None, 3, 2, 0),
    "s_root_second": (0, 0, 2, None, 3, 1, 2),
}


def bundles(owner: Owner) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(N)
    )


def numeric_utilities(
    values: tuple[tuple[int, ...], ...], owner: Owner
) -> tuple[int, ...]:
    assigned = bundles(owner)
    return tuple(
        sum(values[agent][good] for good in assigned[agent]) for agent in range(N)
    )


def numeric_efx(values: tuple[tuple[int, ...], ...], owner: Owner) -> bool:
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return all(
        own[observer]
        >= sum(
            values[observer][good]
            for good in assigned[target]
            if good != removed
        )
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )


def changed_goods(owner: Owner) -> int:
    return sum(left != right for left, right in zip(owner, BASE_OWNER))


def encode_owner(owner: Owner) -> list[int | None]:
    return list(owner)


def allocation_record(
    values: tuple[tuple[int, ...], ...],
    base_utility: tuple[int, ...],
    owner: Owner,
) -> dict:
    utility = numeric_utilities(values, owner)
    delta = tuple(right - left for left, right in zip(base_utility, utility))
    return {
        "owner": encode_owner(owner),
        "utility": list(utility),
        "delta": list(delta),
        "efx": numeric_efx(values, owner),
        "changed_goods": changed_goods(owner),
        "losing_agents": [AGENTS[index] for index, entry in enumerate(delta) if entry < 0],
        "improving_agents": [AGENTS[index] for index, entry in enumerate(delta) if entry > 0],
    }


def canonical(records: list[tuple[int, int, Owner]]) -> dict | None:
    if not records:
        return None
    changed, loss, owner = min(records, key=lambda entry: (entry[0], entry[1], str(entry[2])))
    return {"owner": encode_owner(owner), "changed_goods": changed, "total_loss": loss}


def audit_profile(profile: dict) -> dict:
    values = tuple(tuple(row) for row in profile["values"])
    order = tuple(profile["agent_order"])
    base_utility = numeric_utilities(values, BASE_OWNER)
    base_key = tuple(base_utility[agent] for agent in order)
    efx_count = 0
    strict_pareto: list[tuple[int, int, Owner]] = []
    weak_pareto: list[tuple[int, int, Owner]] = []
    one_loser: list[tuple[int, int, Owner]] = []
    lex_improving = 0
    minimum_losers = 4
    minimum_total_loss = None
    for owner in ALL_OWNERS:
        if not numeric_efx(values, owner):
            continue
        efx_count += 1
        utility = numeric_utilities(values, owner)
        delta = tuple(right - left for left, right in zip(base_utility, utility))
        positives = sum(entry > 0 for entry in delta)
        losers = sum(entry < 0 for entry in delta)
        total_loss = sum(-entry for entry in delta if entry < 0)
        if tuple(utility[agent] for agent in order) > base_key:
            lex_improving += 1
        if positives:
            minimum_losers = min(minimum_losers, losers)
            if minimum_total_loss is None or total_loss < minimum_total_loss:
                minimum_total_loss = total_loss
            record = (changed_goods(owner), total_loss, owner)
            if losers == 0:
                weak_pareto.append(record)
                if all(entry > 0 for entry in delta):
                    strict_pareto.append(record)
            if losers <= 1:
                one_loser.append(record)
    return {
        "agent_order": list(order),
        "agent_order_names": [AGENTS[agent] for agent in order],
        "base_utility": list(base_utility),
        "efx_assignment_count": efx_count,
        "lex_improving_efx_count": lex_improving,
        "weak_pareto_improving_efx_count": len(weak_pareto),
        "strict_pareto_improving_efx_count": len(strict_pareto),
        "one_loser_improving_efx_count": len(one_loser),
        "minimum_losers_for_any_improving_efx": minimum_losers,
        "minimum_total_loss_for_any_improving_efx": minimum_total_loss,
        "canonical_weak_pareto_escape": canonical(weak_pareto),
        "canonical_one_loser_escape": canonical(one_loser),
        "root_flip_allocations": {
            name: allocation_record(values, base_utility, owner)
            for name, owner in ROOT_FLIP_OWNERS.items()
        },
    }


def main() -> None:
    repo = Path(__file__).resolve().parents[2]
    source_path = repo / "results/alternating_anchored_or_promoted_atomic_audit.json"
    result_path = repo / "results/alternating_adaptive_order_atomic_handoff_audit.json"
    source = json.loads(source_path.read_text())
    profiles = [audit_profile(profile) for profile in source["anchored_countermodels"]]
    payload = {
        "schema": SCHEMA,
        "source": str(source_path.relative_to(repo)),
        "claim_boundary": (
            "Exhaustive only for the six frozen seven-good strict fixed-order "
            "countermodels; it tests candidate global handoff potentials and is not "
            "a theorem for arbitrary additive instances."
        ),
        "base_owner": encode_owner(BASE_OWNER),
        "goods": list(GOODS),
        "agents": list(AGENTS),
        "root_flip_owners": {
            name: encode_owner(owner) for name, owner in ROOT_FLIP_OWNERS.items()
        },
        "profiles": profiles,
        "summary": {
            "profile_count": len(profiles),
            "profiles_with_weak_pareto_escape": sum(
                profile["weak_pareto_improving_efx_count"] > 0 for profile in profiles
            ),
            "profiles_with_one_loser_escape": sum(
                profile["one_loser_improving_efx_count"] > 0 for profile in profiles
            ),
            "profiles_with_p_root_efx": sum(
                profile["root_flip_allocations"]["p_root_first"]["efx"]
                or profile["root_flip_allocations"]["p_root_second"]["efx"]
                for profile in profiles
            ),
            "profiles_with_s_root_efx": sum(
                profile["root_flip_allocations"]["s_root_first"]["efx"]
                or profile["root_flip_allocations"]["s_root_second"]["efx"]
                for profile in profiles
            ),
        },
    }
    temporary = result_path.with_suffix(result_path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    temporary.replace(result_path)
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
