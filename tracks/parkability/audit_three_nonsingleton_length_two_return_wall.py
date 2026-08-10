#!/usr/bin/env python3
"""Exact local witness against a nonsingleton return-edge shortcut."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
GOODS = ("tr", "br", "tq", "bq", "c1", "c2", "z", "f")
BUNDLES = {
    "r": frozenset(("tr", "br")),
    "q": frozenset(("tq", "bq")),
    "c": frozenset(("c1", "c2")),
    "s": frozenset(("z",)),
}

BASE = {
    "r": (5, 5, 7, 1, 7, 1, 8, 4),
    "q": (7, 1, 5, 5, 3, 3, 8, 4),
    "c": (6, 5, 6, 5, 5, 5, 12, 3),
    "s": (4, 3, 4, 3, 3, 3, 10, 2),
}
OFFSETS = {
    "r": (1, 2, 4, 8, 16, 32, 64, 128),
    "q": (2, 8, 32, 128, 1, 4, 16, 64),
    "c": (4, 32, 1, 16, 128, 8, 64, 2),
    "s": (8, 1, 64, 4, 32, 2, 128, 16),
}
VALUES = {
    agent: {
        good: 1024 * BASE[agent][index] + OFFSETS[agent][index]
        for index, good in enumerate(GOODS)
    }
    for agent in AGENTS
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def value(agent: str, bundle) -> int:
    return sum(VALUES[agent][good] for good in bundle)


def own(agent: str) -> int:
    return value(agent, BUNDLES[agent])


def common_safe(bundle) -> bool:
    bundle = frozenset(bundle)
    return all(
        value(agent, bundle - {good}) <= own(agent)
        for agent in AGENTS
        for good in bundle
    )


def desired(agent: str, bundle) -> bool:
    bundle = frozenset(bundle)
    return value(agent, bundle) > own(agent) and common_safe(bundle)


def nondegenerate(agent: str) -> bool:
    utilities = []
    for size in range(len(GOODS) + 1):
        for bundle in itertools.combinations(GOODS, size):
            utilities.append(value(agent, bundle))
    return len(utilities) == len(set(utilities))


def allocation_efx(allocation: dict[str, frozenset[str]]) -> bool:
    return all(
        value(observer, allocation[observer]) >= value(observer, target - {good})
        for observer in AGENTS
        for target in allocation.values()
        for good in target
    )


def improvement_census() -> dict:
    old_owner = {
        good: agent
        for agent, bundle in BUNDLES.items()
        for good in bundle
    }
    old_owner["f"] = "_"
    base_vector = tuple(own(agent) for agent in AGENTS)
    recipients = AGENTS + ("_",)
    improvements = 0
    complete_improvements = 0
    minimum_moved = len(GOODS) + 1
    minimum_nonsingletons = len(AGENTS) + 1
    nearest = []
    for assignment in itertools.product(recipients, repeat=len(GOODS)):
        allocation = {
            agent: frozenset(
                good for good, recipient in zip(GOODS, assignment) if recipient == agent
            )
            for agent in AGENTS
        }
        vector = tuple(value(agent, allocation[agent]) for agent in AGENTS)
        if vector <= base_vector or not allocation_efx(allocation):
            continue
        improvements += 1
        if "_" not in assignment:
            complete_improvements += 1
        moved = sum(
            recipient != old_owner[good]
            for good, recipient in zip(GOODS, assignment)
        )
        nonsingletons = sum(len(bundle) > 1 for bundle in allocation.values())
        minimum_nonsingletons = min(minimum_nonsingletons, nonsingletons)
        record = {
            "allocation": {agent: sorted(bundle) for agent, bundle in allocation.items()},
            "unallocated": sorted(
                good for good, recipient in zip(GOODS, assignment) if recipient == "_"
            ),
            "moved_goods": moved,
            "nonsingleton_bundles": nonsingletons,
            "utility_vector": list(vector),
        }
        if moved < minimum_moved:
            minimum_moved = moved
            nearest = [record]
        elif moved == minimum_moved and len(nearest) < 8:
            nearest.append(record)
    return {
        "priority_order": list(AGENTS),
        "efx_lex_improvement_count": improvements,
        "complete_efx_lex_improvement_count": complete_improvements,
        "minimum_moved_goods": minimum_moved,
        "minimum_nonsingleton_bundles": minimum_nonsingletons,
        "nearest_improvements": nearest,
    }


def run() -> dict:
    d_rq = frozenset(("tq", "f"))
    d_qr = frozenset(("tr", "f"))
    d_rc = frozenset(("c1", "f"))
    e_cq = frozenset(("tq", "br"))
    e_cr = frozenset(("tr", "bq"))

    checks = {
        "positive": all(VALUES[a][g] > 0 for a in AGENTS for g in GOODS),
        "nondegenerate_rows": all(nondegenerate(agent) for agent in AGENTS),
        "partial_efx": all(
            own(observer) >= value(observer, bundle - {good})
            for observer in AGENTS
            for bundle in BUNDLES.values()
            for good in bundle
        ),
        "charity_unenvied": all(own(agent) >= value(agent, {"f"}) for agent in AGENTS),
        "genuine_r_to_q": desired("r", d_rq) and "f" in d_rq,
        "genuine_q_to_r": desired("q", d_qr) and "f" in d_qr,
        "genuine_r_to_c": desired("r", d_rc) and "f" in d_rc,
        "external_c_to_q": desired("c", e_cq),
        "external_c_to_r": desired("c", e_cr),
        "c_is_sole_envier_of_singleton": (
            value("c", BUNDLES["s"]) > own("c")
            and all(value(agent, BUNDLES["s"]) <= own(agent) for agent in ("r", "q", "s"))
        ),
        "external_large_c_has_no_incoming_envy": all(
            value(agent, BUNDLES["c"]) <= own(agent) for agent in AGENTS
        ),
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-length-two-return-wall-v1",
        "status": "VERIFIED" if all(checks.values()) else "FAILED",
        "checks": checks,
        "allocation": {agent: sorted(bundle) for agent, bundle in BUNDLES.items()},
        "unallocated": ["f"],
        "values": VALUES,
        "displayed_edges": {
            "r_f_champions_q_with_desired_set": sorted(d_rq),
            "q_f_champions_r_with_desired_set": sorted(d_qr),
            "r_f_champions_c_with_desired_set": sorted(d_rc),
            "c_generalized_champions_q_with_desired_set": sorted(e_cq),
            "c_generalized_champions_r_with_desired_set": sorted(e_cr),
            "ordinary_envy": "c -> s",
        },
        "full_good_level_improvement_census": improvement_census(),
        "claim_boundary": (
            "exact positive nondegenerate partial-EFX local profile refuting only the shortcut "
            "that the external nonsingleton owner in the length-two class must have an incoming "
            "ordinary envy edge; it is not asserted globally maximal and is not an EFX counterexample"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
