#!/usr/bin/env python3
"""Independently audit the q=4 small-step radius-two boundary at m=9."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

try:
    from .anneal import atomic_json
    from .audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        minimal_hall_witnesses,
        radius_ball,
        transfer_distance,
    )
    from .core import iter_unlabeled_nonempty_partitions, validate_values
except ImportError:
    from anneal import atomic_json
    from audit_row_merge_single_wall_radius import (
        canonical,
        graph,
        matching_count,
        minimal_hall_witnesses,
        radius_ball,
        transfer_distance,
    )
    from core import iter_unlabeled_nonempty_partitions, validate_values


SCHEMA = "row-merge-q4-small-step-radius-boundary-audit-v1"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(seed_path, normalization_path, cvc5_path, terminal_path, output_path):
    if output_path.exists():
        raise ValueError("output must be new")
    seed = json.loads(seed_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    terminal = json.loads(terminal_path.read_text())
    seed_formula = Path(seed["formula"])
    normalized_formula = Path(normalization["output"])
    terminal_formula = Path(terminal["formula"])
    if (
        seed.get("schema") != "row-merge-q4-small-step-radius-cegar-v1"
        or seed.get("status") != "CEGAR_INCOMPLETE"
        or seed.get("m") != 9
        or seed.get("radius") != 2
        or seed.get("radius_partition_count") != 319
        or seed.get("initial_cut_count") != 16
        or seed.get("final_cut_count") != 27
        or not seed_formula.is_file()
        or sha256(seed_formula) != seed["formula_sha256"]
        or normalization["source_sha256"] != seed["formula_sha256"]
        or not normalized_formula.is_file()
        or sha256(normalized_formula) != normalization["output_sha256"]
        or cvc5.get("verdict") != "sat"
        or cvc5.get("returncode") != 0
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
    ):
        raise AssertionError("the 27-cut cvc5 SAT chain failed")
    if (
        terminal.get("schema") != "row-merge-q4-small-step-radius-cegar-v1"
        or terminal.get("status") != "RADIUS_PIVOT_REFUTATION_FOUND"
        or terminal.get("m") != 9
        or terminal.get("radius") != 2
        or terminal.get("radius_partition_count") != 319
        or terminal.get("initial_cut_count") != 27
        or terminal.get("final_cut_count") != 37
        or terminal.get("warm_source") != str(seed_path)
        or terminal.get("warm_source_sha256") != sha256(seed_path)
        or not terminal_formula.is_file()
        or sha256(terminal_formula) != terminal["formula_sha256"]
        or terminal["rounds"][-1].get("radius_support_count") != 0
    ):
        raise AssertionError("the terminal 37-cut trace failed")

    wall = validate_values(
        terminal["terminal_wall_values"], expected_n=4, lower=1
    )
    post = validate_values(
        terminal["terminal_post_wall_values"], expected_n=4, lower=1
    )
    partition = tuple(tuple(bundle) for bundle in terminal["wall_partition"])
    if partition != ((0, 1), (2, 3), (4, 5), (6, 7, 8)):
        raise AssertionError("unexpected wall partition")
    if wall[1:] != post[1:]:
        raise AssertionError("a resident row changed")
    epsilon = post[0][2] - wall[0][2]
    if (
        epsilon <= 0
        or any(
            post[0][good]
            != wall[0][good] + (epsilon if good == 2 else 0)
            for good in range(9)
        )
        or epsilon >= min(wall[0][good] for good in (4, 5, 6, 7, 8))
        or wall[0][0] + wall[0][1] != wall[0][2]
    ):
        raise AssertionError("the recorded transition is not a small wall step")

    wall_graph = graph(wall, partition)
    post_graph = graph(post, partition)
    changed = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(4)
        for bundle in range(4)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if changed != ((0, 0, True, False),):
        raise AssertionError("the wall changed more than the critical edge")
    if any(not wall_graph[agent][agent] for agent in range(4)):
        raise AssertionError("the wall allocation is not EFX")
    witnesses = minimal_hall_witnesses(post_graph)
    if witnesses != (((0, 1, 2, 3), (1, 2, 3)),):
        raise AssertionError("the post-wall graph is not the q=4 Hall cell")

    radius = radius_ball(partition, 2)
    if len(radius) != 319:
        raise AssertionError("the radius-two partition census changed")
    if any(matching_count(graph(post, candidate)) for candidate in radius):
        raise AssertionError("a radius-two partition supports EFX")

    support_count = 0
    allocation_count = 0
    histogram = Counter()
    nearest = None
    for candidate in iter_unlabeled_nonempty_partitions(4, 9):
        count = matching_count(graph(post, candidate))
        if not count:
            continue
        distance = transfer_distance(canonical(partition), candidate)
        support_count += 1
        allocation_count += count
        histogram[distance] += 1
        if nearest is None or (distance, candidate) < nearest:
            nearest = (distance, candidate)
    expected_histogram = {3: 20, 4: 62, 5: 41}
    if (
        support_count != 123
        or allocation_count != 206
        or dict(histogram) != expected_histogram
        or nearest
        != (3, ((0, 1, 3, 6), (2, 7), (4, 5), (8,)))
    ):
        raise AssertionError("the complete EFX census changed")

    result = {
        "schema": SCHEMA,
        "status": "Q4_SMALL_STEP_RADIUS_TWO_BOUNDARY_AUDITED",
        "seed_source": str(seed_path),
        "seed_source_sha256": sha256(seed_path),
        "seed_formula_sha256": seed["formula_sha256"],
        "seed_normalized_formula_sha256": normalization["output_sha256"],
        "seed_cvc5_status": cvc5["verdict"],
        "seed_cvc5_solver_sha256": cvc5["solver_sha256"],
        "terminal_source": str(terminal_path),
        "terminal_source_sha256": sha256(terminal_path),
        "terminal_formula_sha256": terminal["formula_sha256"],
        "n": 4,
        "m": 9,
        "wall_partition": [list(bundle) for bundle in partition],
        "small_step_epsilon": epsilon,
        "changed_edge": list(changed[0]),
        "minimal_hall_witness": {
            "agents": list(witnesses[0][0]),
            "neighbors": list(witnesses[0][1]),
        },
        "radius": 2,
        "radius_partition_count": len(radius),
        "radius_support_count": 0,
        "complete_efx_supporting_partition_count": support_count,
        "complete_efx_allocation_count": allocation_count,
        "minimum_supporting_partition_transfer_distance": nearest[0],
        "supporting_partition_transfer_distance_histogram": {
            str(distance): histogram[distance] for distance in sorted(histogram)
        },
        "nearest_supporting_partition": [list(bundle) for bundle in nearest[1]],
        "claim": (
            "A positive-additive four-agent nine-good q=4 small-step wall can "
            "have no complete EFX partition within transfer radius two."
        ),
        "claim_boundary": (
            "The post-wall profile has 206 complete EFX allocations beginning "
            "at distance three. This refutes a local radius bound, not complete "
            "additive EFX existence."
        ),
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.seed,
        args.normalization,
        args.cvc5,
        args.terminal,
        args.output,
    )


if __name__ == "__main__":
    main()
