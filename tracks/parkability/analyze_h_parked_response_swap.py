#!/usr/bin/env python3
"""Audit the four-edge d/s swap induced by an H-avoiding response core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

from .analyze_hlw_physical_response_cores import CURRENT_TARGET_PIECES
from .audit_allocated_e_physical_packet_counterprofile import expand
from .run_fixed_u_full_packet_terminal_cegar import OWNERS


ROOT = Path(__file__).resolve().parents[2]


def amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if not goods:
        return Fraction(0)
    return amount(values, observer, goods) - min(values[observer][good] for good in goods)


def minimal_current_cores(values, target, thresholds):
    target = tuple(sorted(target))
    rows = []
    for size in range(1, len(target) + 1):
        for subset in itertools.combinations(target, size):
            totals = {
                owner: amount(values, owner, subset) for owner in OWNERS
            }
            sources = [
                owner for owner in OWNERS if totals[owner] > thresholds[owner]
            ]
            if not sources:
                continue
            if any(
                tail(values, observer, subset) > thresholds[observer]
                for observer in OWNERS
            ):
                continue
            if any(
                any(
                    totals[owner] - values[owner][good] > thresholds[owner]
                    for owner in OWNERS
                )
                for good in subset
            ):
                continue
            rows.append({"goods": list(subset), "desired_sources": sources})
    return rows


def run(source: Path, cores_source: Path, output: Path):
    source = source.resolve()
    cores_source = cores_source.resolve()
    _, expansion, values, _, support = expand(source)
    current = {
        owner: tuple(
            good
            for piece in CURRENT_TARGET_PIECES[owner]
            for good in expansion[piece]
        )
        for owner in OWNERS
    }
    all_goods = set().union(*(set(goods) for goods in current.values()))
    supplier = {
        good: owner for owner, goods in support.items() for good in goods
    }
    payload = json.loads(cores_source.read_text())
    rows = []
    for core in payload["current_cores"]:
        D = set(core["goods"])
        if any(good in expansion["h"] for good in D):
            continue
        if "s" not in core["desired_sources"]:
            continue
        allocation = {
            "r": set(current["r"]),
            "q": set(current["q"]),
            "d": (set(current["d"]) - D) | set(current["s"]),
            "s": D,
        }
        assert set().union(*allocation.values()) == all_goods
        assert sum(map(len, allocation.values())) == len(all_goods)
        edges = sorted({
            (supplier[good], owner)
            for owner, goods in allocation.items()
            for good in goods
            if supplier[good] != owner
        })
        utility = {
            owner: amount(values, owner, allocation[owner]) for owner in OWNERS
        }
        failures = []
        for observer in OWNERS:
            for target in OWNERS:
                if observer == target:
                    continue
                rhs = tail(values, observer, allocation[target])
                if utility[observer] < rhs:
                    failures.append({
                        "observer": observer,
                        "target": target,
                        "own": str(utility[observer]),
                        "target_tail": str(rhs),
                    })
        response_cores = minimal_current_cores(
            values, allocation["d"], utility,
        )
        h_goods = set(expansion["h"])
        for response in response_cores:
            response["touches_h"] = bool(set(response["goods"]) & h_goods)
        rows.append({
            "core": sorted(D),
            "pieces": core["pieces"],
            "edges": [list(edge) for edge in edges],
            "edge_count": len(edges),
            "utility": {owner: str(value) for owner, value in utility.items()},
            "efx": not failures,
            "failures": failures,
            "response_core_count": len(response_cores),
            "response_cores_touching_h": sum(
                response["touches_h"] for response in response_cores
            ),
            "response_cores": response_cores,
        })
    result = {
        "schema": "h-parked-response-swap-analysis-v1",
        "status": "COMPLETE",
        "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "cores_source": str(cores_source.relative_to(ROOT)),
        "cores_source_sha256": hashlib.sha256(cores_source.read_bytes()).hexdigest(),
        "candidate_count": len(rows),
        "efx_candidate_count": sum(row["efx"] for row in rows),
        "all_within_four_edges": all(row["edge_count"] <= 4 for row in rows),
        "every_swap_response_core_touches_h": all(
            row["response_cores"]
            and all(response["touches_h"] for response in row["response_cores"])
            for row in rows
        ),
        "rows": rows,
        "source_sha256_driver": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact swap census for the H-avoiding current-response cores in "
            "one physical SAT profile. It does not prove a universal selector."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cores-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.source, args.cores_source, args.output), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
