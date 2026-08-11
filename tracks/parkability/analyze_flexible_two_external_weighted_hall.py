#!/usr/bin/env python3
"""Census all minimal-payment residual partitions in an atomized flower."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

try:
    from .analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from .audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        tail,
        value,
    )
    from .analyze_flexible_later_owner_escape_topologies import old_bundles
except ImportError:
    from analyze_flexible_lex_radius3_hardness_gap import desired_subsets
    from audit_flexible_later_owner_rooted_connected_transfer_refutation import (
        AGENTS,
        tail,
        value,
    )
    from analyze_flexible_later_owner_escape_topologies import old_bundles


TOP_R = ("ar_tr_0", "ar_tr_1", "tr_rest_0", "tr_rest_1")
BOTTOM_R = ("aq_br_0", "aq_br_1", "br_rest_0", "br_rest_1")
TOP_Q = ("aq_tq_0", "aq_tq_1")
BOTTOM_Q = ("ar_bq_0", "ar_bq_1")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_efx(values, allocation):
    return all(
        value(values, observer, allocation[observer])
        >= tail(values, observer, allocation[target])
        for observer in AGENTS for target in AGENTS
    ) and all(
        value(values, observer, allocation[observer])
        >= value(values, observer, allocation["_"])
        for observer in AGENTS
    )


def minimal_payment_packets(values):
    threshold = value(values, "q", TOP_Q)
    result = []
    for size in range(1, len(TOP_R) + 1):
        for packet in itertools.combinations(TOP_R, size):
            if value(values, "q", packet) <= threshold:
                continue
            if all(
                value(values, "q", tuple(good for good in packet if good != removed))
                <= threshold
                for removed in packet
            ):
                result.append(packet)
    return result


def find_sdr(targets, response):
    for sources in itertools.permutations(targets):
        if all(sources[index] in response[target] for index, target in enumerate(targets)):
            return dict(zip(targets, sources))
    return None


def run(source_path):
    payload = json.loads(source_path.read_text())
    values = {
        agent: {good: Fraction(amount) for good, amount in row.items()}
        for agent, row in payload["values"].items()
    }
    base = old_bundles()
    base_value = {agent: value(values, agent, base[agent]) for agent in AGENTS}
    payments = minimal_payment_packets(values)
    counts = Counter()
    matching_signatures = Counter()
    partition_shapes = Counter()
    examples = {}
    response_cache = {}

    def response_sources(offer):
        key = tuple(sorted(offer))
        if key not in response_cache:
            response_cache[key] = sorted(
                source
                for source in AGENTS
                if desired_subsets(values, base_value, source, key)
            )
        return response_cache[key]

    for payment in payments:
        residual = tuple(good for good in TOP_R if good not in payment) + BOTTOM_R
        root_core = TOP_Q + ("f",)
        evolved_q = BOTTOM_Q + payment
        for destinations in itertools.product(("r", "c", "s", "_"), repeat=len(residual)):
            cells = {recipient: [] for recipient in ("r", "c", "s", "_")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            allocation = {
                "r": tuple(root_core + tuple(cells["r"])),
                "q": tuple(evolved_q),
                "c": tuple(base["c"] + tuple(cells["c"])),
                "s": tuple(base["s"] + tuple(cells["s"])),
                "_": tuple(cells["_"]),
            }
            targets = ("r", "q") + tuple(
                owner for owner in ("c", "s") if cells[owner]
            )
            response = {
                target: sorted(set(response_sources(allocation[target])).intersection(targets))
                for target in targets
            }
            matching = find_sdr(targets, response)
            if is_efx(values, allocation):
                classification = "EFX"
            elif matching is not None:
                classification = "INTERNAL_SDR"
            else:
                classification = "HALL_DEFICIENT"
            counts[classification] += 1
            counts[f"TARGETS_{len(targets)}"] += 1
            shape = tuple(len(cells[recipient]) for recipient in ("r", "c", "s", "_"))
            partition_shapes[(classification, shape)] += 1
            if matching is not None:
                signature = ";".join(
                    f"{target}<-{matching[target]}" for target in targets
                )
                matching_signatures[signature] += 1
            if classification not in examples:
                examples[classification] = {
                    "payment_packet": list(payment),
                    "residual": list(residual),
                    "destinations": {
                        good: recipient
                        for good, recipient in zip(residual, destinations)
                    },
                    "allocation": {
                        recipient: list(goods) for recipient, goods in allocation.items()
                    },
                    "targets": list(targets),
                    "internal_response_sets": response,
                    "internal_sdr": matching,
                }
    script = Path(__file__).resolve()
    root = script.parents[2]
    closure_count = counts["EFX"] + counts["INTERNAL_SDR"]
    payment_diagnostics = []
    for payment in payments:
        residual = tuple(good for good in TOP_R if good not in payment) + BOTTOM_R
        root_core = TOP_Q + ("f",)
        evolved_q = BOTTOM_Q + payment
        own_after_rotation = {
            "r": value(values, "r", root_core),
            "q": value(values, "q", evolved_q),
            "c": base_value["c"],
            "s": base_value["s"],
        }
        threshold = {
            observer: tail(values, observer, evolved_q) for observer in AGENTS
        }
        walls = [
            observer
            for observer in AGENTS
            if own_after_rotation[observer] < threshold[observer]
        ]
        response_details = {
            source: desired_subsets(values, base_value, source, evolved_q)
            for source in AGENTS
        }
        response_details = {
            source: subsets for source, subsets in response_details.items() if subsets
        }
        payment_feasibility = Counter()
        payment_examples = {}
        for destinations in itertools.product(("r", "c", "s", "_"), repeat=len(residual)):
            cells = {recipient: [] for recipient in ("r", "c", "s", "_")}
            for good, recipient in zip(residual, destinations):
                cells[recipient].append(good)
            paid = tuple(
                owner
                for owner in ("r", "c", "s")
                if (
                    value(values, "q", root_core + tuple(cells["r"]))
                    > base_value["q"]
                    if owner == "r"
                    else base_value[owner] + value(values, owner, cells[owner])
                    >= threshold[owner]
                )
            )
            payment_feasibility[paid] += 1
            payment_examples.setdefault(
                paid,
                {good: recipient for good, recipient in zip(residual, destinations)},
            )
        payment_diagnostics.append({
            "payment_packet": list(payment),
            "residual": list(residual),
            "rotation_wall_observers": walls,
            "rotation_wall_margins": {
                observer: str(threshold[observer] - own_after_rotation[observer])
                for observer in walls
            },
            "evolved_q_response_sources": response_details,
            "full_residual_payability": {
                observer: (
                    own_after_rotation[observer] + value(values, observer, residual)
                    >= threshold[observer]
                )
                for observer in ("c", "s")
            },
            "unpayable_bottom_polarity": {
                observer: (
                    value(values, observer, BOTTOM_Q)
                    > value(values, observer, residual)
                )
                for observer in ("c", "s")
            },
            "q_full_root_payment": (
                value(values, "q", root_core + residual) > base_value["q"]
            ),
            "q_root_payment_margin": str(
                value(values, "q", root_core + residual) - base_value["q"]
            ),
            "weighted_payment_patterns": [
                {
                    "paid_demands": list(paid),
                    "count": count,
                    "example": payment_examples[paid],
                }
                for paid, count in sorted(
                    payment_feasibility.items(), key=lambda item: (len(item[0]), item[0])
                )
            ],
        })
    return {
        "schema": "flexible-two-external-weighted-hall-census-v1",
        "status": "RESPONSE_CLOSURE_FOUND" if closure_count else "NO_CLOSURE_FOUND",
        "minimal_payment_packets": [list(packet) for packet in payments],
        "partition_count": sum(counts[key] for key in ("EFX", "INTERNAL_SDR", "HALL_DEFICIENT")),
        "counts": dict(sorted(counts.items())),
        "matching_signatures": [
            {"signature": signature, "count": count}
            for signature, count in sorted(matching_signatures.items())
        ],
        "partition_shapes": [
            {
                "classification": classification,
                "cell_sizes_r_c_s_charity": list(shape),
                "count": count,
            }
            for (classification, shape), count in sorted(partition_shapes.items())
        ],
        "response_offer_cache_size": len(response_cache),
        "minimal_examples": examples,
        "payment_diagnostics": payment_diagnostics,
        "claim_boundary": (
            "solver-free exact-Fraction census of all minimal-payment residual "
            "partitions in one hardened atomized flower; closure supports the "
            "cap-free response-Hall lemma but does not prove a universal selector"
        ),
        "provenance": {
            "source": str(source_path.relative_to(root)),
            "source_sha256": sha256(source_path),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
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
