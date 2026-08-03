#!/usr/bin/env python3
"""Describe the allocation moves in dependency-closed adaptive cores."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from . import core
    from .anneal import atomic_json
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .run_lexmax_partial_cegar import bundles_of
except ImportError:
    import core
    from anneal import atomic_json
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from run_lexmax_partial_cegar import bundles_of


SCHEMA = "adaptive-priority-exchange-motif-audit-v1"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transition_type(
    candidate_floater: int,
    rival_floater: int,
    moves: list[dict],
) -> str:
    if candidate_floater == rival_floater:
        if (
            len(moves) == 2
            and moves[0]["from"] == moves[1]["to"]
            and moves[0]["to"] == moves[1]["from"]
        ):
            return "two_agent_good_swap"
        return "same_floater_reallocation"
    if len(moves) == 2:
        inserted = next(
            (move for move in moves if move["from"] is None),
            None,
        )
        ejected = next(
            (move for move in moves if move["to"] is None),
            None,
        )
        if (
            inserted is not None
            and ejected is not None
            and inserted["to"] == ejected["from"]
        ):
            return "one_host_floater_exchange"
    return "floater_exchange_plus_reallocation"


def audit_core(path: Path) -> dict:
    document = json.loads(path.read_text())
    if (
        document.get("schema") != "adaptive-priority-rival-core-v1"
        or document.get("status")
        != "UNSAT_DELETION_MINIMAL_RIVAL_CORE"
        or not document.get("preserve_rival_dependencies")
    ):
        raise ValueError(f"{path} is not a dependency-closed adaptive core")
    seed_path = Path(document["seed_path"])
    if sha256(seed_path) != document["seed_sha256"]:
        raise ValueError(f"{path} seed hash mismatch")
    seed = json.loads(seed_path.read_text())
    raw_values = seed.get("values", seed.get("candidate_values"))
    values = core.validate_values(
        raw_values,
        expected_n=document["n"],
        expected_m=document["m"],
        lower=1,
    )
    cells = derive_unique_seed_cells(values)
    unique_candidates = list(
        dict.fromkeys(candidate for _, candidate in cells)
    )

    motifs = []
    for record in document["core"]:
        if record["kind"] != "rival":
            continue
        candidate = unique_candidates[record["candidate_index"]]
        rival = (
            record["rival"]["floater"],
            tuple(record["rival"]["base_owner"]),
        )
        candidate_bundles = bundles_of(candidate[1], document["n"])
        rival_bundles = bundles_of(rival[1], document["n"])
        moves = [
            {
                "good": good,
                "from": left,
                "to": right,
            }
            for good, (left, right) in enumerate(
                zip(candidate[1], rival[1])
            )
            if left != right
        ]
        order = tuple(record["agent_order"])
        candidate_utility = [
            sum(values[agent][good] for good in candidate_bundles[agent])
            for agent in range(document["n"])
        ]
        rival_utility = [
            sum(values[agent][good] for good in rival_bundles[agent])
            for agent in range(document["n"])
        ]
        rival_classification = core.classify_base(
            values,
            rival[0],
            rival[1],
        )
        rival_eligible = (
            rival_classification["base_min_efx_slack"] >= 0
            and all(
                rival_utility[agent] >= values[agent][rival[0]]
                for agent in range(document["n"])
            )
        )
        unchanged_prefix = []
        first_changed = None
        for agent in order:
            if candidate_bundles[agent] == rival_bundles[agent]:
                if first_changed is None:
                    unchanged_prefix.append(agent)
            elif first_changed is None:
                first_changed = agent
        motif = {
                "candidate_index": record["candidate_index"],
                "agent_order": list(order),
                "candidate_floater": candidate[0],
                "rival_floater": rival[0],
                "candidate_bundle_sizes": [
                    len(bundle) for bundle in candidate_bundles
                ],
                "rival_bundle_sizes": [
                    len(bundle) for bundle in rival_bundles
                ],
                "transition_type": transition_type(
                    candidate[0],
                    rival[0],
                    moves,
                ),
                "changed_good_count": len(moves),
                "changed_agents": sorted(
                    {
                        owner
                        for move in moves
                        for owner in (move["from"], move["to"])
                        if owner is not None
                    }
                ),
                "unchanged_priority_prefix": unchanged_prefix,
                "first_bundle_changed_in_order": first_changed,
                "own_utility_deltas": [
                    right - left
                    for left, right in zip(
                        candidate_utility,
                        rival_utility,
                    )
                ],
                "rival_eligible_in_seed": rival_eligible,
                "rival_lexicographically_nonlower_in_seed": (
                    tuple(rival_utility[agent] for agent in order)
                    >= tuple(candidate_utility[agent] for agent in order)
                ),
                "moves": moves,
            }
        if motif["transition_type"] == "one_host_floater_exchange":
            inserted = next(move for move in moves if move["from"] is None)
            ejected = next(move for move in moves if move["to"] is None)
            host = inserted["to"]
            floater = inserted["good"]
            removed = ejected["good"]
            observer_checks = []
            for observer in range(document["n"]):
                if observer == host:
                    continue
                own = candidate_utility[observer]
                target = rival_bundles[host]
                target_threshold = (
                    sum(values[observer][good] for good in target)
                    - min(values[observer][good] for good in target)
                )
                observer_checks.append(
                    {
                        "observer": observer,
                        "floater_at_most_removed": (
                            values[observer][floater]
                            <= values[observer][removed]
                        ),
                        "own_covers_removed": (
                            own >= values[observer][removed]
                        ),
                        "modified_host_efx_slack": own - target_threshold,
                    }
                )
            motif["one_host_exchange"] = {
                "host": host,
                "inserted_floater": floater,
                "ejected_good": removed,
                "host_weakly_improves": (
                    values[host][floater] >= values[host][removed]
                ),
                "simple_safe_exchange_conditions_hold": (
                    values[host][floater] >= values[host][removed]
                    and all(
                        check["floater_at_most_removed"]
                        and check["own_covers_removed"]
                        for check in observer_checks
                    )
                ),
                "observer_checks": observer_checks,
            }
        motifs.append(motif)
    types = Counter(motif["transition_type"] for motif in motifs)
    return {
        "core_path": str(path.resolve()),
        "core_sha256": sha256(path),
        "seed_path": str(seed_path.resolve()),
        "candidate_count": document["candidate_count"],
        "dependency_closed_candidate_count": document[
            "dependency_closed_candidate_count"
        ],
        "rival_count": len(motifs),
        "transition_type_counts": dict(sorted(types.items())),
        "motifs": motifs,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    audits = [audit_core(path) for path in args.core]
    type_counts = Counter(
        motif["transition_type"]
        for audit in audits
        for motif in audit["motifs"]
    )
    result = {
        "schema": SCHEMA,
        "status": "AUDITED",
        "meaning": (
            "combinatorial descriptions of takeover moves in fixed 4x9 "
            "dependency-closed cores; this is not a covering theorem"
        ),
        "core_count": len(audits),
        "rival_count": sum(audit["rival_count"] for audit in audits),
        "transition_type_counts": dict(sorted(type_counts.items())),
        "cores": audits,
    }
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
