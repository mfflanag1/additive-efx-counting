#!/usr/bin/env python3
"""Extract human-scale strict-order payment menus from low-wall UNSAT cells."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_abstract_low_wall import run as run_walls
    from .decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, candidate_covers
except ImportError:
    from decide_three_nonsingleton_flower_abstract_low_wall import run as run_walls
    from decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, candidate_covers


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clause(cover: dict) -> tuple[str, tuple[str, ...]]:
    unpaid = cover["unpaid_agent"]
    payment = cover["assignment"][unpaid]
    targets = tuple(sorted({
        name
        for agent, name in cover["assignment"].items()
        if agent != unpaid and name != "Z"
    }))
    return payment, targets


def satisfying_order(covers: list[dict]):
    clauses = [clause(cover) for cover in covers]
    names = sorted({name for payment, targets in clauses for name in (payment, *targets)})
    for order in itertools.permutations(names):
        rank = {name: index for index, name in enumerate(order)}
        if all(rank[payment] < max(rank[target] for target in targets) for payment, targets in clauses):
            return order
    return None


def deterministic_menu(record: dict) -> list[dict]:
    covers = candidate_covers(
        record["arm_source"],
        record["singleton_envier"],
        record["left_bottom_source"],
        record["right_bottom_source"],
        tuple(record["priority_order"]),
    )
    covers = [cover for cover in covers if cover["unpaid_agent"] is not None]
    covers.sort(key=lambda cover: (
        cover["unpaid_agent"],
        tuple(cover["assignment"][agent] for agent in AGENTS),
    ))
    for size in range(1, 5):
        for menu in itertools.combinations(covers, size):
            if len({cover["unpaid_agent"] for cover in menu}) != 1:
                continue
            if satisfying_order(list(menu)) is None:
                return list(menu)
    raise AssertionError("no four-cover strict-order menu found")


def run() -> dict:
    walls = run_walls()
    records = []
    for record in walls["records"]:
        if record["status"] != "IMPOSSIBLE":
            continue
        menu = deterministic_menu(record)
        assert satisfying_order(menu) is None
        deletion_witnesses = []
        for index in range(len(menu)):
            witness = satisfying_order(menu[:index] + menu[index + 1:])
            assert witness is not None
            deletion_witnesses.append(list(witness))
        records.append({
            "source_order_key": {
                field: record[field]
                for field in (
                    "arm_source",
                    "singleton_envier",
                    "left_bottom_source",
                    "right_bottom_source",
                    "priority_order",
                )
            },
            "unpaid_agent": menu[0]["unpaid_agent"],
            "menu": [
                {
                    "payment": clause(cover)[0],
                    "possible_larger_bundles": list(clause(cover)[1]),
                    "assignment": cover["assignment"],
                }
                for cover in menu
            ],
            "deletion_order_witnesses": deletion_witnesses,
        })
    sizes = sorted({len(record["menu"]) for record in records})
    signatures = Counter(
        json.dumps(sorted(
            (
                entry["payment"],
                tuple(entry["possible_larger_bundles"]),
            )
            for entry in record["menu"]
        ))
        for record in records
    )
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    return {
        "schema": "three-nonsingleton-flower-payment-menu-v1",
        "status": "ALL_MINIMAL" if len(records) == 148 else "INCOMPLETE",
        "record_count": len(records),
        "menu_sizes": {
            str(size): sum(len(record["menu"]) == size for record in records)
            for size in sizes
        },
        "canonical_menu_types": [
            {"clauses": json.loads(signature), "count": count}
            for signature, count in sorted(signatures.items(), key=lambda item: (-item[1], item[0]))
        ],
        "records": records,
        "claim_boundary": (
            "strict-order certificates for the 148 abstract-UNSAT cells: low failure of every menu cover "
            "would force each payment below another displayed bundle and hence a directed strict cycle"
        ),
        "provenance": {
            "wall_script_sha256": walls["provenance"]["script_sha256"],
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
        "records": result["record_count"],
        "menu_sizes": result["menu_sizes"],
    }, indent=2))


if __name__ == "__main__":
    main()
