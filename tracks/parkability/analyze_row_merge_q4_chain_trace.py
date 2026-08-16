#!/usr/bin/env python3
"""Mine recurring exchange motifs from row-merge chain CEGAR traces."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import canonical
    from .decide_row_merge_single_wall_radius import literal_graph, matching_count
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import canonical
    from decide_row_merge_single_wall_radius import literal_graph, matching_count


SCHEMA = "row-merge-q4-chain-trace-analysis-v1"
N = 4
BASE = ((0, 1), (2, 3), (4, 5), (6, 7, 8))
PERTURBED_GOOD = 2
CRITICAL_GOOD = 3


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def action_key(action: dict) -> tuple:
    return (
        action["kind"],
        action["length"],
        tuple(action["vertices"]),
        tuple(action["goods"]),
    )


def actions_by_partition() -> dict[tuple, tuple[dict, ...]]:
    found = defaultdict(dict)
    for length in range(1, 4):
        for vertices in itertools.permutations(range(N), length + 1):
            if len(set(vertices)) != len(vertices):
                continue
            edges = tuple(zip(vertices[:-1], vertices[1:]))
            for goods in itertools.product(*(BASE[source] for source, _ in edges)):
                if any(
                    len(BASE[source])
                    == sum(edge_source == source for edge_source, _ in edges)
                    for source in range(N)
                ):
                    continue
                moved = [list(bundle) for bundle in BASE]
                for (source, target), good in zip(edges, goods):
                    moved[source].remove(good)
                    moved[target].append(good)
                action = {
                    "kind": "path",
                    "length": length,
                    "vertices": list(vertices),
                    "goods": list(goods),
                }
                found[canonical(moved)][action_key(action)] = action
    for length in range(2, 4):
        for vertices in itertools.permutations(range(N), length):
            if vertices[0] != min(vertices):
                continue
            edges = tuple(
                (vertices[index], vertices[(index + 1) % length])
                for index in range(length)
            )
            for goods in itertools.product(*(BASE[source] for source, _ in edges)):
                moved = [list(bundle) for bundle in BASE]
                for (source, target), good in zip(edges, goods):
                    moved[source].remove(good)
                    moved[target].append(good)
                action = {
                    "kind": "cycle",
                    "length": length,
                    "vertices": list(vertices),
                    "goods": list(goods),
                }
                found[canonical(moved)][action_key(action)] = action
    return {
        partition: tuple(records[key] for key in sorted(records))
        for partition, records in found.items()
    }


def action_signatures(action: dict) -> set[str]:
    kind = action["kind"]
    length = action["length"]
    vertices = tuple(action["vertices"])
    goods = tuple(action["goods"])
    sources = vertices[:-1] if kind == "path" else vertices
    touched = tuple(sorted(set(vertices)))
    edges = (
        tuple(zip(vertices[:-1], vertices[1:]))
        if kind == "path"
        else tuple(
            (vertices[index], vertices[(index + 1) % length])
            for index in range(length)
        )
    )
    signatures = {
        f"kind={kind}",
        f"length={length}",
        f"kind={kind};length={length}",
        f"vertices={','.join(map(str, vertices))}",
        f"edges={','.join(f'{source}>{target}' for source, target in edges)}",
        f"touched={','.join(map(str, touched))}",
        f"kind={kind};touched={','.join(map(str, touched))}",
        f"moves_critical={CRITICAL_GOOD in goods}",
        f"moves_perturbed={PERTURBED_GOOD in goods}",
        f"moves_from_failed_bundle={0 in sources}",
        f"moves_into_failed_bundle={any(target == 0 for _, target in edges)}",
    }
    if kind == "path":
        signatures.update(
            {
                f"path_start={vertices[0]}",
                f"path_end={vertices[-1]}",
                f"path_start={vertices[0]};end={vertices[-1]}",
                f"path_length={length};start={vertices[0]}",
                f"path_length={length};end={vertices[-1]}",
            }
        )
    return signatures


def run(trace_paths: tuple[Path, ...], output_path: Path) -> None:
    if output_path.exists():
        raise ValueError("output must be new")
    indexed_actions = actions_by_partition()
    if len(indexed_actions) != 515:
        raise AssertionError("exchange-chain universe changed")

    model_records = []
    signature_model_counts = Counter()
    action_model_counts = Counter()
    support_partition_model_counts = Counter()
    topology_model_masks = defaultdict(int)
    topology_partitions = defaultdict(set)
    for partition, actions in indexed_actions.items():
        for action in actions:
            topology_partitions[(action["kind"], tuple(action["vertices"]))].add(
                partition
            )
    fixed_graph = None
    for trace_path in trace_paths:
        trace = json.loads(trace_path.read_text())
        schema = trace.get("schema")
        if tuple(tuple(bundle) for bundle in trace.get("wall_partition", ())) != BASE:
            raise ValueError(f"incompatible trace: {trace_path}")
        if schema == "row-merge-q4-exchange-chain-cegar-v1":
            round_records = trace["rounds"]
        elif (
            schema == "row-merge-q4-cycle023-gate-v1"
            and trace.get("solver_status") == "sat"
        ):
            round_records = [
                {
                    "round": 0,
                    "cuts_before_solve": trace["combined_partition_count"],
                    "solver_status": "sat",
                    "post_wall_values": trace["post_wall_values"],
                    "chain_support_count": trace["simple_chain_support_count"],
                }
            ]
        else:
            raise ValueError(f"incompatible trace: {trace_path}")
        trace_graph = trace.get("fixed_post_wall_graph")
        if trace_graph is not None:
            graph_tuple = tuple(tuple(row) for row in trace_graph)
            if fixed_graph is None:
                fixed_graph = graph_tuple
            elif graph_tuple != fixed_graph:
                raise AssertionError("fixed graph changed across traces")
        for round_record in round_records:
            if round_record.get("solver_status") != "sat":
                continue
            post_values = round_record["post_wall_values"]
            model_graph = tuple(tuple(row) for row in literal_graph(post_values, BASE))
            if fixed_graph is None:
                fixed_graph = model_graph
            elif model_graph != fixed_graph:
                raise AssertionError("a SAT model left the fixed graph cell")
            supports = []
            model_signatures = set()
            model_actions = set()
            model_topologies = set()
            model_partitions = set()
            kind_length_counts = Counter()
            for partition, actions in indexed_actions.items():
                count = matching_count(literal_graph(post_values, partition))
                if not count:
                    continue
                model_partitions.add(partition)
                action_records = []
                for action in actions:
                    key = action_key(action)
                    model_actions.add(key)
                    model_topologies.add((action["kind"], tuple(action["vertices"])))
                    model_signatures.update(action_signatures(action))
                    kind_length_counts[(action["kind"], action["length"])] += 1
                    action_records.append(action)
                supports.append(
                    {
                        "partition": [list(bundle) for bundle in partition],
                        "matching_count": count,
                        "actions": action_records,
                    }
                )
            if len(supports) != round_record["chain_support_count"]:
                raise AssertionError("stored support count failed exact replay")
            for signature in model_signatures:
                signature_model_counts[signature] += 1
            for key in model_actions:
                action_model_counts[key] += 1
            for partition in model_partitions:
                support_partition_model_counts[partition] += 1
            model_index = len(model_records)
            for topology in model_topologies:
                topology_model_masks[topology] |= 1 << model_index
            model_records.append(
                {
                    "trace": str(trace_path),
                    "trace_sha256": sha256(trace_path),
                    "round": round_record["round"],
                    "cuts_before_solve": round_record["cuts_before_solve"],
                    "integer_upper": trace.get("integer_upper"),
                    "support_partition_count": len(supports),
                    "support_action_count": len(model_actions),
                    "kind_length_action_counts": {
                        f"{kind}_{length}": count
                        for (kind, length), count in sorted(kind_length_counts.items())
                    },
                    "supports": supports,
                }
            )

    model_count = len(model_records)
    universal_signatures = sorted(
        signature
        for signature, count in signature_model_counts.items()
        if count == model_count
    )
    universal_actions = [
        {
            "kind": key[0],
            "length": key[1],
            "vertices": list(key[2]),
            "goods": list(key[3]),
        }
        for key, count in sorted(action_model_counts.items())
        if count == model_count
    ]
    universal_partitions = [
        [list(bundle) for bundle in partition]
        for partition, count in sorted(support_partition_model_counts.items())
        if count == model_count
    ]
    full_model_mask = (1 << model_count) - 1
    topology_keys = tuple(sorted(topology_model_masks))
    minimum_topology_cover = None
    for cover_size in range(1, min(7, len(topology_keys) + 1)):
        for cover in itertools.combinations(topology_keys, cover_size):
            mask = 0
            for topology in cover:
                mask |= topology_model_masks[topology]
            if mask == full_model_mask:
                minimum_topology_cover = cover
                break
        if minimum_topology_cover is not None:
            break
    cover_partitions = set()
    if minimum_topology_cover is not None:
        for topology in minimum_topology_cover:
            cover_partitions.update(topology_partitions[topology])
    minimum_topology_cover_records = [
        {
            "kind": topology[0],
            "vertices": list(topology[1]),
            "covered_model_count": topology_model_masks[topology].bit_count(),
            "partition_count": len(topology_partitions[topology]),
        }
        for topology in minimum_topology_cover or ()
    ]
    result = {
        "schema": SCHEMA,
        "status": "EXACT_TRACE_MOTIFS_CLASSIFIED",
        "wall_partition": [list(bundle) for bundle in BASE],
        "perturbed_good": PERTURBED_GOOD,
        "critical_good": CRITICAL_GOOD,
        "fixed_post_wall_graph": (
            [list(row) for row in fixed_graph] if fixed_graph is not None else None
        ),
        "trace_count": len(trace_paths),
        "sat_model_count": model_count,
        "exchange_chain_partition_count": len(indexed_actions),
        "universal_existential_signatures": universal_signatures,
        "universal_action_count": len(universal_actions),
        "universal_actions": universal_actions,
        "universal_partition_count": len(universal_partitions),
        "universal_partitions": universal_partitions,
        "minimum_topology_cover_size": (
            len(minimum_topology_cover)
            if minimum_topology_cover is not None
            else None
        ),
        "minimum_topology_cover": minimum_topology_cover_records,
        "minimum_topology_cover_partition_count": len(cover_partitions),
        "minimum_topology_cover_partitions": [
            [list(bundle) for bundle in partition]
            for partition in sorted(cover_partitions)
        ],
        "models": model_records,
        "interpretation": (
            "A universal existential signature occurs in at least one "
            "supporting exchange action in every stored SAT model. Such a "
            "signature is proof-mining evidence only, not a theorem."
        ),
        "claim_boundary": (
            "This exactly replays a finite stored CEGAR trace. It does not "
            "prove the exchange-chain candidate or complete EFX."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(tuple(args.trace), args.output)


if __name__ == "__main__":
    main()
