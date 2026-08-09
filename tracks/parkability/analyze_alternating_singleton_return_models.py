#!/usr/bin/env python3
"""Mine common escape motifs from frozen singleton-return countermodels."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

SCHEMA = "alternating-singleton-return-model-analysis-v1"
AGENTS = ("p", "r", "s", "q")
N = len(AGENTS)
SIZES = (2, 2, 2, 2)
ORDER = (0, 2, 1, 3)


def make_cell(sizes: tuple[int, int, int, int]) -> dict:
    labels = ("tr", "br", "tq", "bq")
    goods = []
    packets = []
    for label, size in zip(labels, sizes):
        packet = tuple(range(len(goods), len(goods) + size))
        packets.append(packet)
        goods.extend(label if size == 1 else f"{label}{index}" for index in range(size))
    x = len(goods)
    goods.append("x")
    y = len(goods)
    goods.append("y")
    goods.append("f")
    tr, br, tq, bq = packets
    base_bundles = ((x,), tr + br, (y,), tq + bq)
    base_owner = tuple(
        next((agent for agent, bundle in enumerate(base_bundles) if good in bundle), None)
        for good in range(len(goods))
    )
    return {
        "goods": tuple(goods),
        "packets": tuple(packets),
        "x": x,
        "y": y,
        "floater": len(goods) - 1,
        "base_owner": base_owner,
        "m": len(goods),
    }


def bundles(owner) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(N)
    )


def numeric_utilities(values, owner):
    assigned = bundles(owner)
    return tuple(sum(values[agent][good] for good in assigned[agent]) for agent in range(N))


def numeric_efx(values, owner) -> bool:
    assigned = bundles(owner)
    own = numeric_utilities(values, owner)
    return all(
        own[observer]
        >= sum(values[observer][good] for good in assigned[target] if good != removed)
        for observer in range(N)
        for target in range(N)
        for removed in assigned[target]
    )


def singleton_return_candidates(cell):
    x, y = cell["x"], cell["y"]
    remaining = tuple(good for good in range(cell["m"]) if good not in (x, y))
    seen = set()
    for fixed_agent, destinations in ((1, (2, 3, None)), (2, (1, 3, None))):
        for assignment in itertools.product(destinations, repeat=len(remaining)):
            owner = [None] * cell["m"]
            owner[x] = 0
            owner[y] = fixed_agent
            for good, destination in zip(remaining, assignment):
                owner[good] = destination
            allocation = tuple(owner)
            if allocation not in seen:
                seen.add(allocation)
                yield allocation


def dominates(values, cell, allocation) -> bool:
    base = numeric_utilities(values, cell["base_owner"])
    rival = numeric_utilities(values, allocation)
    return tuple(rival[agent] for agent in ORDER) > tuple(base[agent] for agent in ORDER)


def desired(values, cell, source: int, candidate: tuple[int, ...]) -> bool:
    base_own = numeric_utilities(values, cell["base_owner"])
    return bool(candidate) and sum(values[source][good] for good in candidate) > base_own[source] and base_safe(
        values, cell, candidate
    )


def base_safe(values, cell, candidate: tuple[int, ...]) -> bool:
    base_own = numeric_utilities(values, cell["base_owner"])
    return all(
        base_own[observer]
        >= sum(values[observer][good] for good in candidate if good != removed)
        for observer in range(N)
        for removed in candidate
    )


def base_safe_for(values, cell, candidate, observers) -> bool:
    base_own = numeric_utilities(values, cell["base_owner"])
    return all(
        base_own[observer]
        >= sum(values[observer][good] for good in candidate if good != removed)
        for observer in observers
        for removed in candidate
    )


def powerset(goods):
    for size in range(len(goods) + 1):
        yield from itertools.combinations(goods, size)


def selected_root_analysis(values, cell) -> dict:
    tr, br, tq, bq = cell["packets"]
    selected = tq + (cell["floater"],)
    available = tr + br + bq
    threshold = sum(values[3][good] for good in selected) - min(
        values[3][good] for good in selected
    )
    remaining_total = sum(values[3][good] for good in available)
    threshold_subsets = []
    externally_safe = []
    escapes = []
    failure_counts = Counter()
    for candidate in powerset(available):
        if sum(values[3][good] for good in candidate) < threshold:
            continue
        threshold_subsets.append(candidate)
        owner = [None] * cell["m"]
        owner[cell["x"]] = 0
        owner[cell["y"]] = 1
        for good in selected:
            owner[good] = 2
        for good in candidate:
            owner[good] = 3
        allocation = tuple(owner)
        assigned = bundles(allocation)
        own = numeric_utilities(values, allocation)
        external_failures = []
        all_failures = []
        for observer in range(N):
            for target in range(N):
                for removed in assigned[target]:
                    remainder = sum(
                        values[observer][good]
                        for good in assigned[target]
                        if good != removed
                    )
                    if own[observer] < remainder:
                        wall = (observer, target, removed)
                        all_failures.append(wall)
                        if target == 3 and observer != 3:
                            external_failures.append(wall)
        if not external_failures:
            externally_safe.append(candidate)
        if not all_failures and dominates(values, cell, allocation):
            escapes.append(candidate)
        else:
            for observer, target, removed in all_failures:
                key = f"{AGENTS[observer]}>{AGENTS[target]}-{cell['goods'][removed]}"
                failure_counts[key] += 1
    if escapes:
        classification = "DIRECT_SELECTED_ROOT_ESCAPE"
    elif remaining_total < threshold:
        classification = "INSUFFICIENT_Q_TOTAL"
    else:
        classification = "THRESHOLD_SUBSETS_BLOCKED"
    return {
        "classification": classification,
        "s_bundle": [cell["goods"][good] for good in selected],
        "q_available_goods": [cell["goods"][good] for good in available],
        "q_threshold": threshold,
        "remaining_q_total": remaining_total,
        "threshold_subset_count": len(threshold_subsets),
        "externally_safe_threshold_subset_count": len(externally_safe),
        "efx_lex_escape_count": len(escapes),
        "minimum_escape_q_bundles": [
            [cell["goods"][good] for good in candidate]
            for candidate in sorted(escapes, key=lambda item: (len(item), item))[:16]
        ],
        "failure_wall_counts": dict(sorted(failure_counts.items())),
    }


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shape(assigned) -> tuple[int, ...]:
    return tuple(len(bundle) for bundle in assigned)


def mode(cell, assigned) -> str:
    return_r = assigned[1] == (cell["y"],)
    anchor_s = assigned[2] == (cell["y"],)
    if return_r and anchor_s:
        return "both"
    if return_r:
        return "return_r"
    if anchor_s:
        return "anchor_s"
    raise AssertionError("candidate is outside singleton-return family")


def record_model(values, label, cell, candidates) -> dict:
    escapes = []
    desired_active_escapes = []
    two_base_safe_bundle_escapes = []
    base_q_remainder_escapes = []
    relaxed_base_q_remainder_escapes = []
    mode_counts = Counter()
    shape_counts = Counter()
    for allocation in candidates:
        if not numeric_efx(values, allocation) or not dominates(values, cell, allocation):
            continue
        assigned = bundles(allocation)
        allocation_mode = mode(cell, assigned)
        allocated_count = sum(len(bundle) for bundle in assigned)
        mode_counts[allocation_mode] += 1
        shape_counts[(allocation_mode, shape(assigned))] += 1
        escapes.append((allocated_count, allocation_mode, allocation, assigned))
        active_agent = 2 if allocation_mode == "return_r" else 1
        base_q = set(cell["packets"][2] + cell["packets"][3])
        if set(assigned[3]) == base_q.difference(assigned[active_agent]):
            fixed_observers = (0, 1) if active_agent == 2 else (0, 2)
            if base_safe_for(
                values, cell, assigned[active_agent], fixed_observers
            ) and base_safe_for(values, cell, assigned[3], (0, 1, 2)):
                relaxed_base_q_remainder_escapes.append(
                    (allocated_count, allocation_mode, allocation, assigned)
                )
        if desired(values, cell, active_agent, assigned[active_agent]):
            record = (allocated_count, allocation_mode, allocation, assigned)
            desired_active_escapes.append(record)
            if base_safe(values, cell, assigned[3]):
                two_base_safe_bundle_escapes.append(record)
                if set(assigned[3]) == base_q.difference(assigned[active_agent]):
                    base_q_remainder_escapes.append(record)
    if not escapes:
        raise AssertionError((label, "no singleton-return escape"))
    escapes.sort(key=lambda item: (item[0], item[1], str(item[2])))
    minimum = escapes[0][0]
    minimum_records = []
    for allocated_count, allocation_mode, allocation, assigned in escapes:
        if allocated_count != minimum or len(minimum_records) >= 32:
            continue
        minimum_records.append(
            {
                "mode": allocation_mode,
                "owner_by_good": list(allocation),
                "bundles": {
                    AGENTS[agent]: [cell["goods"][good] for good in bundle]
                    for agent, bundle in enumerate(assigned)
                },
                "utilities": list(numeric_utilities(values, allocation)),
            }
        )
    return {
        "label": label,
        "escape_count": len(escapes),
        "mode_counts": dict(sorted(mode_counts.items())),
        "base_desired_active_escape_count": len(desired_active_escapes),
        "base_desired_active_mode_counts": dict(
            sorted(Counter(item[1] for item in desired_active_escapes).items())
        ),
        "two_base_safe_bundle_escape_count": len(two_base_safe_bundle_escapes),
        "two_base_safe_bundle_mode_counts": dict(
            sorted(Counter(item[1] for item in two_base_safe_bundle_escapes).items())
        ),
        "base_q_remainder_escape_count": len(base_q_remainder_escapes),
        "base_q_remainder_mode_counts": dict(
            sorted(Counter(item[1] for item in base_q_remainder_escapes).items())
        ),
        "relaxed_base_q_remainder_escape_count": len(
            relaxed_base_q_remainder_escapes
        ),
        "relaxed_base_q_remainder_mode_counts": dict(
            sorted(
                Counter(item[1] for item in relaxed_base_q_remainder_escapes).items()
            )
        ),
        "minimum_two_base_safe_bundle_escapes": [
            {
                "mode": allocation_mode,
                "active_bundle": [
                    cell["goods"][good]
                    for good in assigned[2 if allocation_mode == "return_r" else 1]
                ],
                "q_bundle": [cell["goods"][good] for good in assigned[3]],
            }
            for _, allocation_mode, _, assigned in sorted(
                two_base_safe_bundle_escapes,
                key=lambda item: (item[0], item[1], str(item[2])),
            )[:16]
        ],
        "minimum_base_desired_active_escapes": [
            {
                "mode": allocation_mode,
                "bundles": {
                    AGENTS[agent]: [cell["goods"][good] for good in bundle]
                    for agent, bundle in enumerate(assigned)
                },
            }
            for _, allocation_mode, _, assigned in sorted(
                desired_active_escapes,
                key=lambda item: (item[0], item[1], str(item[2])),
            )[:16]
        ],
        "minimum_allocated_good_count": minimum,
        "minimum_escapes": minimum_records,
        "shape_counts": [
            {"mode": key[0], "shape": list(key[1]), "count": count}
            for key, count in sorted(shape_counts.items())
        ],
        "selected_root": selected_root_analysis(values, cell),
    }


def analyze(session_path: Path, audit_paths: list[Path]) -> dict:
    cell = make_cell(SIZES)
    candidates = tuple(singleton_return_candidates(cell))
    session = json.loads(session_path.read_text())
    profiles = [
        (f"cegar_iteration_{record['iteration']}", tuple(tuple(row) for row in record["values"]))
        for record in session["trace"]
    ]
    for audit_path in audit_paths:
        audit = json.loads(audit_path.read_text())
        profiles.append((audit_path.stem, tuple(tuple(row) for row in audit["values"])))
    records = [record_model(values, label, cell, candidates) for label, values in profiles]
    minimum_mode_presence = Counter()
    minimum_allocated_good_counts = Counter()
    selected_root_classifications = Counter()
    profiles_with_base_desired_active_escape = 0
    profiles_with_two_base_safe_bundle_escape = 0
    profiles_with_base_q_remainder_escape = 0
    profiles_with_relaxed_base_q_remainder_escape = 0
    for record in records:
        minimum_allocated_good_counts[record["minimum_allocated_good_count"]] += 1
        selected_root_classifications[record["selected_root"]["classification"]] += 1
        if record["base_desired_active_escape_count"]:
            profiles_with_base_desired_active_escape += 1
        if record["two_base_safe_bundle_escape_count"]:
            profiles_with_two_base_safe_bundle_escape += 1
        if record["base_q_remainder_escape_count"]:
            profiles_with_base_q_remainder_escape += 1
        if record["relaxed_base_q_remainder_escape_count"]:
            profiles_with_relaxed_base_q_remainder_escape += 1
        modes = {escape["mode"] for escape in record["minimum_escapes"]}
        for allocation_mode in modes:
            minimum_mode_presence[allocation_mode] += 1
    script = Path(__file__).resolve()
    return {
        "schema": SCHEMA,
        "status": "ALL_FROZEN_MODELS_HAVE_SINGLETON_RETURN_ESCAPES",
        "packet_sizes": list(SIZES),
        "goods": list(cell["goods"]),
        "agent_order": list(ORDER),
        "agent_order_names": [AGENTS[agent] for agent in ORDER],
        "candidate_count": len(candidates),
        "profile_count": len(records),
        "minimum_mode_profile_counts": dict(sorted(minimum_mode_presence.items())),
        "minimum_allocated_good_count_distribution": {
            str(count): frequency
            for count, frequency in sorted(minimum_allocated_good_counts.items())
        },
        "selected_root_classification_counts": dict(
            sorted(selected_root_classifications.items())
        ),
        "profiles_with_base_desired_active_escape": profiles_with_base_desired_active_escape,
        "profiles_with_two_base_safe_bundle_escape": profiles_with_two_base_safe_bundle_escape,
        "profiles_with_base_q_remainder_escape": profiles_with_base_q_remainder_escape,
        "profiles_with_relaxed_base_q_remainder_escape": profiles_with_relaxed_base_q_remainder_escape,
        "profiles": records,
        "claim_boundary": {
            "proved": "the exact escape census for the recorded frozen profiles",
            "not_proved": "the singleton-return lemma outside this profile corpus",
        },
        "provenance": {
            "script": str(script.relative_to(script.parents[2])),
            "script_sha256": sha256(script),
            "session": str(session_path),
            "session_sha256": sha256(session_path),
            "audits": [
                {"path": str(path), "sha256": sha256(path)} for path in audit_paths
            ],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", type=Path, required=True)
    parser.add_argument("--audit", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.session, args.audit)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "status",
                    "profile_count",
                    "candidate_count",
                    "minimum_mode_profile_counts",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
