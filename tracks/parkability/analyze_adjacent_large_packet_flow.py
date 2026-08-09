#!/usr/bin/env python3
"""Classify adjacent-large reservoir walls and unrestricted escape motifs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

try:
    from .run_alternating_variable_packet_rooted_cegar import make_cell
except ImportError:
    from run_alternating_variable_packet_rooted_cegar import make_cell


SCHEMA = "adjacent-large-packet-flow-analysis-v1"
AGENTS = ("p", "r", "s", "q")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bundle_value(row, bundle) -> int:
    return sum(row[good] for good in bundle)


def tau(row, bundle) -> int:
    return max(
        (bundle_value(row, tuple(good for good in bundle if good != removed)) for removed in bundle),
        default=0,
    )


def subsets(pool):
    pool = tuple(pool)
    for mask in range(1, 1 << len(pool)):
        yield tuple(pool[index] for index in range(len(pool)) if mask & (1 << index))


def common_safe(values, base, bundle) -> bool:
    return all(tau(values[observer], bundle) <= base[observer] for observer in range(4))


def desired_sources(values, base, bundle):
    if not common_safe(values, base, bundle):
        return ()
    return tuple(
        source
        for source in range(4)
        if bundle_value(values[source], bundle) > base[source]
    )


def inclusion_minimal_desired_sets(values, base, pool):
    records = []
    for bundle in sorted(subsets(pool), key=lambda item: (len(item), item)):
        sources = desired_sources(values, base, bundle)
        if not sources:
            continue
        if any(set(previous["bundle"]).issubset(bundle) for previous in records):
            continue
        records.append({"bundle": bundle, "sources": sources})
    return records


def quota_partition(values, base, r_set, p_set):
    overlap = tuple(sorted(set(r_set).intersection(p_set)))
    r_fixed = tuple(good for good in r_set if good not in overlap)
    p_fixed = tuple(good for good in p_set if good not in overlap)
    for p_share in itertools.chain(((),), subsets(overlap)):
        p_share = tuple(p_share)
        r_share = tuple(good for good in overlap if good not in p_share)
        new_r = r_fixed + r_share
        new_p = p_fixed + p_share
        if (
            bundle_value(values[1], new_r) > base[1]
            and bundle_value(values[0], new_p) > base[0]
        ):
            return new_r, new_p
    return None


def profile_analysis(values, cell):
    base_bundles = cell["base_bundles"]
    base = tuple(bundle_value(values[agent], base_bundles[agent]) for agent in range(4))
    tr, br, tq, bq = cell["packets"]
    f = cell["floater"]
    d_p = tr + (f,)
    d_r = tq + (f,)
    w = br + tq + bq
    u = tr + br + bq
    t_r = tau(values[1], d_p)
    t_p = tau(values[0], d_r)

    w_safe = [bundle for bundle in subsets(w) if common_safe(values, base, bundle)]
    u_safe = [bundle for bundle in subsets(u) if common_safe(values, base, bundle)]
    direct_p = [bundle for bundle in w_safe if bundle_value(values[1], bundle) >= t_r]
    direct_r = [bundle for bundle in u_safe if bundle_value(values[0], bundle) >= t_p]
    w_minimal = inclusion_minimal_desired_sets(values, base, w)
    u_minimal = inclusion_minimal_desired_sets(values, base, u)
    r_walls = [
        record["bundle"]
        for record in w_minimal
        if 1 in record["sources"] and bundle_value(values[1], record["bundle"]) < t_r
    ]
    p_walls = [
        record["bundle"]
        for record in u_minimal
        if 0 in record["sources"] and bundle_value(values[0], record["bundle"]) < t_p
    ]

    pair_count = 0
    disjoint_count = 0
    splittable_count = 0
    blocked_examples = []
    for r_set in r_walls:
        for p_set in p_walls:
            pair_count += 1
            if set(r_set).isdisjoint(p_set):
                disjoint_count += 1
                splittable_count += 1
                continue
            if quota_partition(values, base, r_set, p_set) is not None:
                splittable_count += 1
            elif len(blocked_examples) < 3:
                blocked_examples.append(
                    {
                        "r_wall": list(r_set),
                        "p_wall": list(p_set),
                        "overlap": sorted(set(r_set).intersection(p_set)),
                    }
                )

    return {
        "direct_p_payment_count": len(direct_p),
        "direct_r_payment_count": len(direct_r),
        "w_minimal_desired_source_sets": [
            {
                "bundle": list(record["bundle"]),
                "sources": [AGENTS[source] for source in record["sources"]],
            }
            for record in w_minimal
        ],
        "u_minimal_desired_source_sets": [
            {
                "bundle": list(record["bundle"]),
                "sources": [AGENTS[source] for source in record["sources"]],
            }
            for record in u_minimal
        ],
        "r_wall_count": len(r_walls),
        "p_wall_count": len(p_walls),
        "wall_pair_count": pair_count,
        "disjoint_wall_pair_count": disjoint_count,
        "quota_splittable_wall_pair_count": splittable_count,
        "quota_blocked_examples": blocked_examples,
    }


def assigned_bundles(owner):
    return tuple(
        tuple(good for good, assigned in enumerate(owner) if assigned == agent)
        for agent in range(4)
    )


def escape_record(values, owner, cell, order):
    bundles = assigned_bundles(owner)
    base = tuple(
        bundle_value(values[agent], cell["base_bundles"][agent]) for agent in range(4)
    )
    utilities = tuple(bundle_value(values[agent], bundles[agent]) for agent in range(4))
    first_changed = next(agent for agent in order if utilities[agent] != base[agent])
    p_bundle = bundles[0]
    selected_offer = set(cell["base_bundles"][1] + (cell["floater"],))
    p_sources = desired_sources(values, base, p_bundle) if p_bundle else ()
    if p_bundle == cell["base_bundles"][0]:
        p_kind = "anchored_x"
    elif 0 in p_sources and set(p_bundle).issubset(selected_offer):
        p_kind = "selected_offer_desired"
    elif 0 in p_sources:
        p_kind = "cross_face_desired"
    elif utilities[0] > base[0]:
        p_kind = "endogenous_p_improvement"
    else:
        p_kind = "other"
    touched_packets = sum(bool(set(p_bundle).intersection(packet)) for packet in cell["packets"])
    return {
        "first_changed": AGENTS[first_changed],
        "p_kind": p_kind,
        "p_packet_faces": touched_packets,
        "p_has_f": cell["floater"] in p_bundle,
        "charity_size": sum(assigned is None for assigned in owner),
    }


def analyze(result_path: Path, pool_path: Path):
    result = json.loads(result_path.read_text())
    pool = json.loads(pool_path.read_text())
    sizes = tuple(result["packet_sizes"])
    order = tuple(result["agent_order"])
    cell = make_cell(sizes)
    owners = [tuple(owner) for owner in pool["rivals"]]
    offset = 0
    profile_records = []
    motif_counts = Counter()
    for iteration in result["iterations"]:
        values = tuple(tuple(row) for row in iteration["values"])
        new_count = iteration["new_count"]
        batch = owners[offset : offset + new_count]
        offset += new_count
        for owner in batch:
            motif = escape_record(values, owner, cell, order)
            motif_counts[
                (
                    motif["first_changed"],
                    motif["p_kind"],
                    motif["p_packet_faces"],
                    motif["p_has_f"],
                )
            ] += 1
        profile_records.append(
            {
                "iteration": iteration["iteration"],
                **profile_analysis(values, cell),
            }
        )
    if offset != len(owners):
        raise AssertionError(("pool/trace mismatch", offset, len(owners)))

    return {
        "schema": SCHEMA,
        "status": "DIAGNOSTIC_ONLY",
        "packet_sizes": list(sizes),
        "agent_order": list(order),
        "profile_count": len(profile_records),
        "escape_count": len(owners),
        "profiles": profile_records,
        "profile_summary": {
            "direct_p_payment": sum(record["direct_p_payment_count"] > 0 for record in profile_records),
            "direct_r_payment": sum(record["direct_r_payment_count"] > 0 for record in profile_records),
            "both_direct_payments_fail": sum(
                record["direct_p_payment_count"] == 0
                and record["direct_r_payment_count"] == 0
                for record in profile_records
            ),
            "has_r_and_p_wall": sum(
                record["r_wall_count"] > 0 and record["p_wall_count"] > 0
                for record in profile_records
            ),
            "has_quota_blocked_wall_pair": sum(
                record["wall_pair_count"] > record["quota_splittable_wall_pair_count"]
                for record in profile_records
            ),
        },
        "escape_motifs": [
            {
                "first_changed": key[0],
                "p_kind": key[1],
                "p_packet_faces": key[2],
                "p_has_f": key[3],
                "count": count,
            }
            for key, count in sorted(motif_counts.items())
        ],
        "claim_boundary": (
            "Classifies exact finite profiles and learned escapes. It does not prove "
            "the cap-free adjacent-large lemma."
        ),
        "provenance": {
            "result": str(result_path),
            "result_sha256": sha256(result_path),
            "pool": str(pool_path),
            "pool_sha256": sha256(pool_path),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--pool", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = analyze(args.result, args.pool)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["profile_summary"], indent=2, sort_keys=True))
    print(json.dumps(payload["escape_motifs"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
