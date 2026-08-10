#!/usr/bin/env python3
"""Enumerate one-unpaid common-safe covers of every flower source/order cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
BUNDLE_SUPPORT = {
    "D_r": frozenset(("T_q", "f")),
    "D_q": frozenset(("T_r", "f")),
    "D_c": frozenset(("T_c", "f")),
    "Z": frozenset(("z",)),
    "A_q": frozenset(("T_q", "B_r")),
    "A_r": frozenset(("T_r", "B_q")),
    "X_r": frozenset(("T_r", "B_r")),
    "X_q": frozenset(("T_q", "B_q")),
    "X_c": frozenset(("T_c", "B_c")),
}
BASE = {"r": "X_r", "q": "X_q", "c": "X_c", "s": "Z"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def disjoint(bundle_names: tuple[str, ...]) -> bool:
    used = set()
    for name in bundle_names:
        if used & BUNDLE_SUPPORT[name]:
            return False
        used.update(BUNDLE_SUPPORT[name])
    return True


def candidate_covers(arm: str, envier: str, left: str, right: str, order: tuple[str, ...]):
    desired = {
        "D_r": "r",
        "D_q": "q",
        "D_c": arm,
        "Z": envier,
        "A_q": left,
        "A_r": right,
    }
    records = []
    for names in itertools.permutations(BUNDLE_SUPPORT, len(AGENTS)):
        if not disjoint(names):
            continue
        assignment = dict(zip(AGENTS, names))
        signs = {}
        for agent, name in assignment.items():
            if name == BASE[agent]:
                signs[agent] = "fixed"
            elif desired.get(name) == agent:
                signs[agent] = "improves"
            else:
                signs[agent] = "unpaid"
        unpaid = [agent for agent in AGENTS if signs[agent] == "unpaid"]
        improving = [agent for agent in AGENTS if signs[agent] == "improves"]
        if len(unpaid) > 1 or not improving:
            continue
        if unpaid and min(order.index(agent) for agent in improving) > order.index(unpaid[0]):
            continue
        records.append({
            "assignment": assignment,
            "signs": signs,
            "unpaid_agent": unpaid[0] if unpaid else None,
            "first_improver": min(improving, key=order.index),
        })
    return records


def run() -> dict:
    records = []
    uncovered = []
    exact_covers = 0
    one_unpaid_covers = 0
    for arm, envier, left, right in itertools.product(
        ("r", "q", "s"),
        ("r", "q", "c"),
        ("c", "s"),
        ("c", "s"),
    ):
        for order in itertools.permutations(AGENTS):
            covers = candidate_covers(arm, envier, left, right, order)
            key = {
                "arm_source": arm,
                "singleton_envier": envier,
                "left_bottom_source": left,
                "right_bottom_source": right,
                "priority_order": list(order),
            }
            if not covers:
                uncovered.append(key)
                records.append({**key, "status": "UNCOVERED"})
                continue
            covers.sort(key=lambda record: (
                record["unpaid_agent"] is not None,
                record["unpaid_agent"] not in (None, "r", "q"),
                (
                    record["assignment"].get(record["unpaid_agent"], "")
                    not in ("A_q", "A_r")
                ),
                order.index(record["first_improver"]),
                tuple(record["assignment"][agent] for agent in AGENTS),
            ))
            chosen = covers[0]
            if chosen["unpaid_agent"] is None:
                exact_covers += 1
                status = "ALL_FIXED_OR_IMPROVING"
            else:
                one_unpaid_covers += 1
                status = "ONE_UNPAID"
            records.append({**key, "status": status, **chosen})

    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-one-unpaid-cover-v1",
        "status": "EXHAUSTIVE" if not uncovered and len(records) == 864 else "INCOMPLETE",
        "cell_count": len(records),
        "all_fixed_or_improving_count": exact_covers,
        "one_unpaid_count": one_unpaid_covers,
        "uncovered": uncovered,
        "records": records,
        "claim_boundary": (
            "finite disjoint-support cover of the flower source/order grid; ONE_UNPAID cells "
            "become EFX only when the named recipient meets the maximum tail threshold"
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
    print(json.dumps({
        "status": result["status"],
        "cells": result["cell_count"],
        "exact": result["all_fixed_or_improving_count"],
        "one_unpaid": result["one_unpaid_count"],
        "uncovered": len(result["uncovered"]),
    }, indent=2))


if __name__ == "__main__":
    main()
