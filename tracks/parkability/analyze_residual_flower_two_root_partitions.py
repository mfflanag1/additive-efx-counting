#!/usr/bin/env python3
"""Exact response census for two-root partitions of a frozen flower profile."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path


AGENTS = ("r", "q", "c", "s")
RECIPIENTS = AGENTS + ("_",)
PACKET_BASE = {
    "r": ("k", "j", "br"),
    "q": ("tq", "bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}


def amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def tail(values, observer, goods):
    return amount(values, observer, goods) - min(
        (values[observer][good] for good in goods), default=Fraction()
    )


def is_efx(values, allocation):
    return all(
        amount(values, observer, allocation[observer])
        >= tail(values, observer, allocation[target])
        for observer in AGENTS for target in AGENTS
    ) and all(
        amount(values, observer, allocation[observer])
        >= amount(values, observer, allocation["_"])
        for observer in AGENTS
    )


def minimal_response_sources(values, base, offer):
    minimal = []
    for size in range(1, len(offer) + 1):
        for subset in itertools.combinations(offer, size):
            sources = tuple(
                agent for agent in AGENTS
                if amount(values, agent, subset)
                > amount(values, agent, base[agent])
            )
            if sources and not any(
                set(old_subset) < set(subset)
                for old_subset, _ in minimal
            ):
                minimal.append((subset, sources))
    return minimal


def find_sdr(targets, response):
    for sources in itertools.permutations(targets):
        if all(sources[index] in response[target] for index, target in enumerate(targets)):
            return sources
    return None


def minimal_payment_packets(values, packet_goods):
    top_r = tuple(packet_goods["k"] + packet_goods["j"])
    top_q = tuple(packet_goods["tq"])
    threshold = amount(values, "q", top_q)
    result = []
    for size in range(1, len(top_r) + 1):
        for subset in itertools.combinations(top_r, size):
            if amount(values, "q", subset) <= threshold:
                continue
            if all(
                amount(values, "q", tuple(good for good in subset if good != removed))
                <= threshold
                for removed in subset
            ):
                result.append(subset)
    return result


def run(source_path):
    payload = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(value) for good, value in row.items()}
        for agent, row in payload["values"].items()
    }
    packet_goods = {
        name: list(goods) for name, goods in payload["packet_goods"].items()
    }
    base = {
        agent: tuple(
            good for name in PACKET_BASE[agent] for good in packet_goods[name]
        )
        for agent in AGENTS
    }
    base["_"] = tuple(packet_goods["f"])
    payments = minimal_payment_packets(values, packet_goods)
    records = []
    counts = {"EFX": 0, "INTERNAL_SDR": 0, "HALL_DEFICIENT": 0}
    for payment in payments:
        residual = tuple(
            good
            for good in packet_goods["k"] + packet_goods["j"]
            if good not in payment
        ) + tuple(packet_goods["br"])
        root_core = tuple(packet_goods["tq"] + packet_goods["f"])
        evolved_q = tuple(packet_goods["bq"]) + payment
        for destinations in itertools.product(("r", "c", "s", "_"), repeat=len(residual)):
            cells = {recipient: [] for recipient in ("r", "c", "s", "_")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            allocation = {
                "r": root_core + tuple(cells["r"]),
                "q": evolved_q,
                "c": base["c"] + tuple(cells["c"]),
                "s": base["s"] + tuple(cells["s"]),
                "_": tuple(cells["_"]),
            }
            targets = ("r", "q") + tuple(
                owner for owner in ("c", "s") if cells[owner]
            )
            response = {}
            response_details = {}
            for target in targets:
                details = minimal_response_sources(values, base, allocation[target])
                response_details[target] = [
                    {"bundle": list(bundle), "sources": list(sources)}
                    for bundle, sources in details
                ]
                response[target] = sorted(
                    set(source for _, sources in details for source in sources)
                    & set(targets)
                )
            matching = find_sdr(targets, response)
            if is_efx(values, allocation):
                classification = "EFX"
            elif matching is not None:
                classification = "INTERNAL_SDR"
            else:
                classification = "HALL_DEFICIENT"
            counts[classification] += 1
            records.append({
                "payment_packet": list(payment),
                "residual": list(residual),
                "destinations": {
                    good: recipient for good, recipient in zip(residual, destinations)
                },
                "classification": classification,
                "targets": list(targets),
                "internal_response_sets": response,
                "internal_sdr": list(matching) if matching is not None else None,
                "response_details": response_details,
            })
    return {
        "schema": "residual-flower-two-root-partition-census-v1",
        "status": (
            "RESPONSE_CLOSURE_FOUND"
            if counts["EFX"] + counts["INTERNAL_SDR"] > 0
            else "NO_CLOSURE_FOUND"
        ),
        "minimal_payment_packets": [list(packet) for packet in payments],
        "partition_count": len(records),
        "counts": counts,
        "records": records,
        "claim_boundary": (
            "solver-free exact-Fraction response census for one frozen "
            "nondegenerate profile; internal SDRs compose with the cap-free "
            "release lemma but do not prove the universal partition selector"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "minimal_payment_packets": result["minimal_payment_packets"],
        "partition_count": result["partition_count"],
        "counts": result["counts"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
