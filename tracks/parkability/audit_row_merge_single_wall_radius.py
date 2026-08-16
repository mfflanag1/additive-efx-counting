#!/usr/bin/env python3
"""Independently audit SAT single-wall transfer-radius refutations."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path

try:
    from .anneal import atomic_json
    from .core import iter_unlabeled_nonempty_partitions, validate_values
except ImportError:
    from anneal import atomic_json
    from core import iter_unlabeled_nonempty_partitions, validate_values


SCHEMA = "row-merge-single-wall-radius-refutation-audit-v1"
N = 4
MATCHINGS = tuple(itertools.permutations(range(N)))


def canonical(partition):
    return tuple(sorted(tuple(sorted(bundle)) for bundle in partition))


def neighbors(partition):
    found = set()
    for source, bundle in enumerate(partition):
        if len(bundle) == 1:
            continue
        for good in bundle:
            for target in range(N):
                if source == target:
                    continue
                moved = [list(block) for block in partition]
                moved[source].remove(good)
                moved[target].append(good)
                found.add(canonical(moved))
    return tuple(sorted(found))


def radius_ball(partition, radius):
    start = canonical(partition)
    distance = {start: 0}
    queue = deque([start])
    while queue:
        current = queue.popleft()
        if distance[current] == radius:
            continue
        for neighbor in neighbors(current):
            if neighbor not in distance:
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)
    return distance


def edge(row, partition, own):
    own_total = sum(row[good] for good in partition[own])
    return all(
        own_total >= sum(row[good] for good in target if good != removed)
        for target_index, target in enumerate(partition)
        if target_index != own
        for removed in target
    )


def graph(values, partition):
    return tuple(
        tuple(edge(values[agent], partition, bundle) for bundle in range(N))
        for agent in range(N)
    )


def matching_count(feasible):
    return sum(
        all(feasible[agent][matching[agent]] for agent in range(N))
        for matching in MATCHINGS
    )


def minimal_hall_witnesses(feasible):
    deficient = []
    for size in range(1, N + 1):
        for agents in itertools.combinations(range(N), size):
            neighborhood = tuple(
                bundle
                for bundle in range(N)
                if any(feasible[agent][bundle] for agent in agents)
            )
            if len(neighborhood) < len(agents):
                deficient.append((agents, neighborhood))
    return tuple(
        witness
        for witness in deficient
        if not any(set(other[0]) < set(witness[0]) for other in deficient)
    )


def transfer_distance(left, right):
    retained = max(
        sum(len(set(left[index]) & set(right[order[index]])) for index in range(N))
        for order in MATCHINGS
    )
    return sum(map(len, left)) - retained


def disjoint_pairs(m):
    for labels in itertools.product(range(3), repeat=m):
        left = tuple(good for good, label in enumerate(labels) if label == 1)
        right = tuple(good for good, label in enumerate(labels) if label == 2)
        if left and right and left < right:
            yield left, right


def audit_source(path):
    source = json.loads(path.read_text())
    if source.get("status") != "RADIUS_PIVOT_REFUTATION_FOUND":
        raise ValueError("the audit requires a SAT radius-pivot refutation")
    formula_path = Path(source["smt2_path"])
    if (
        not formula_path.is_file()
        or hashlib.sha256(formula_path.read_bytes()).hexdigest()
        != source["smt2_sha256"]
    ):
        raise AssertionError("archived SMT2 formula hash disagrees with the source")
    wall = validate_values(source["wall_values"], expected_n=N, lower=1)
    post = validate_values(source["post_wall_values"], expected_n=N, lower=1)
    if wall[1:] != post[1:]:
        raise AssertionError("a fixed resident row changed across the wall")
    partition = tuple(tuple(bundle) for bundle in source["wall_partition"])
    critical = source["critical_wall"]
    u = tuple(critical["moving_bundle_u"])
    w = tuple(critical["envied_remainder_w"])
    critical_good = critical["critical_good"]
    perturb_good = critical["perturbed_good"]
    if partition[0] != u or partition[1] != (*w, critical_good):
        raise AssertionError("critical bundles do not reconstruct the wall partition")
    if any(
        post[0][good] != wall[0][good] + (source["scaled_wall_epsilon"] if good == perturb_good else 0)
        for good in range(len(wall[0]))
    ):
        raise AssertionError("post row is not the recorded one-coordinate perturbation")
    if sum(wall[0][good] for good in u) != sum(wall[0][good] for good in w):
        raise AssertionError("the critical subset-sum equality is absent")
    critical_pair = tuple(sorted((u, w)))
    for left, right in disjoint_pairs(len(wall[0])):
        wall_sign = (sum(wall[0][good] for good in left) > sum(wall[0][good] for good in right)) - (
            sum(wall[0][good] for good in left) < sum(wall[0][good] for good in right)
        )
        post_sign = (sum(post[0][good] for good in left) > sum(post[0][good] for good in right)) - (
            sum(post[0][good] for good in left) < sum(post[0][good] for good in right)
        )
        if tuple(sorted((left, right))) == critical_pair:
            if wall_sign != 0 or post_sign == 0:
                raise AssertionError("critical wall did not cross generically")
        elif wall_sign == 0 or wall_sign != post_sign:
            raise AssertionError("a second subset-sum wall is present or crossed")

    wall_graph = graph(wall, partition)
    post_graph = graph(post, partition)
    changed = tuple(
        (agent, bundle, wall_graph[agent][bundle], post_graph[agent][bundle])
        for agent in range(N)
        for bundle in range(N)
        if wall_graph[agent][bundle] != post_graph[agent][bundle]
    )
    if changed != ((0, 0, True, False),):
        raise AssertionError("the original partition changed by more than one edge")
    if any(not wall_graph[agent][agent] for agent in range(N)):
        raise AssertionError("the designated wall allocation is not EFX")
    witnesses = minimal_hall_witnesses(post_graph)
    witness_sizes = {len(agents) for agents, _neighbors in witnesses}
    if witness_sizes != {source["minimal_hall_witness_size"]}:
        raise AssertionError("minimal Hall witness size disagrees with the source")

    radius = source["obstructed_transfer_radius"]
    ball = radius_ball(partition, radius)
    if len(ball) != source["candidate_partition_count"]:
        raise AssertionError("transfer-radius census changed")
    if any(matching_count(graph(post, candidate)) for candidate in ball):
        raise AssertionError("an EFX partition exists inside the claimed obstruction radius")

    support_count = 0
    allocation_count = 0
    histogram = Counter()
    nearest = None
    for candidate in iter_unlabeled_nonempty_partitions(N, len(wall[0])):
        feasible = graph(post, candidate)
        count = matching_count(feasible)
        if not count:
            continue
        distance = transfer_distance(canonical(partition), candidate)
        support_count += 1
        allocation_count += count
        histogram[distance] += 1
        if nearest is None or (distance, candidate) < nearest:
            nearest = (distance, candidate)
    recorded = source["audit"]
    expected_histogram = {str(key): histogram[key] for key in sorted(histogram)}
    if (
        support_count != recorded["complete_efx_supporting_partition_count"]
        or allocation_count != recorded["complete_efx_allocation_count"]
        or nearest[0] != recorded["minimum_supporting_partition_transfer_distance"]
        or [list(bundle) for bundle in nearest[1]] != recorded["nearest_supporting_partition"]
        or expected_histogram != recorded["supporting_partition_transfer_distance_histogram"]
    ):
        raise AssertionError("independent global EFX census disagrees with the source")
    return {
        "source": str(path),
        "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "smt2": str(formula_path),
        "smt2_sha256": source["smt2_sha256"],
        "minimal_hall_witness_size": source["minimal_hall_witness_size"],
        "obstructed_transfer_radius": radius,
        "minimal_hall_witnesses": [
            {"agents": list(agents), "neighbors": list(neighborhood)}
            for agents, neighborhood in witnesses
        ],
        "candidate_partition_count": len(ball),
        "complete_efx_supporting_partition_count": support_count,
        "complete_efx_allocation_count": allocation_count,
        "minimum_supporting_partition_transfer_distance": nearest[0],
        "generic_single_wall_verified": True,
        "only_original_edge_change": [0, 0, True, False],
    }


def audit_unsat_boundary(source_path, normalization_path, cvc5_path):
    source = json.loads(source_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    formula_path = Path(source["smt2_path"])
    normalized_path = Path(normalization["output"])
    if (
        source.get("status") != "UNSAT_CANDIDATE"
        or source.get("minimal_hall_witness_size") != 4
        or source.get("obstructed_transfer_radius") != 2
        or source.get("m") != 7
        or not formula_path.is_file()
        or hashlib.sha256(formula_path.read_bytes()).hexdigest()
        != source["smt2_sha256"]
        or normalization["source_sha256"] != source["smt2_sha256"]
        or not normalized_path.is_file()
        or hashlib.sha256(normalized_path.read_bytes()).hexdigest()
        != normalization["output_sha256"]
        or cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
    ):
        raise AssertionError("dual-solver Hall-size-four boundary chain failed")
    return {
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "z3_status": source["solver_status"],
        "formula_sha256": source["smt2_sha256"],
        "normalization": str(normalization_path),
        "normalization_sha256": hashlib.sha256(
            normalization_path.read_bytes()
        ).hexdigest(),
        "normalized_formula_sha256": normalization["output_sha256"],
        "cvc5": str(cvc5_path),
        "cvc5_sha256": hashlib.sha256(cvc5_path.read_bytes()).hexdigest(),
        "cvc5_status": cvc5["verdict"],
        "cvc5_solver_sha256": cvc5["solver_sha256"],
        "scope": "seven goods, bundle shape 2+2+2+1, Hall size four",
        "excluded_transfer_radius": 2,
    }


def audit_core(core_path, normalization_path, cvc5_path):
    core = json.loads(core_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    core_formula_path = Path(core["core_formula"])
    normalized_path = Path(normalization["output"])
    expected_distances = [1, 1, 1, 2, 2, 2, 2]
    if (
        core.get("status") != "CANDIDATE_CORE_EXTRACTED"
        or core.get("retained_core_size") != 7
        or not core.get("deletion_minimal")
        or [item["transfer_distance"] for item in core["retained_core"]]
        != expected_distances
        or not core_formula_path.is_file()
        or hashlib.sha256(core_formula_path.read_bytes()).hexdigest()
        != core["core_formula_sha256"]
        or normalization["source_sha256"] != core["core_formula_sha256"]
        or not normalized_path.is_file()
        or hashlib.sha256(normalized_path.read_bytes()).hexdigest()
        != normalization["output_sha256"]
        or cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
    ):
        raise AssertionError("seven-partition core audit failed")
    return {
        "source": str(core_path),
        "source_sha256": hashlib.sha256(core_path.read_bytes()).hexdigest(),
        "retained_core_size": core["retained_core_size"],
        "deletion_minimal": core["deletion_minimal"],
        "transfer_distance_census": dict(Counter(expected_distances)),
        "partitions": [item["partition"] for item in core["retained_core"]],
        "core_formula_sha256": core["core_formula_sha256"],
        "normalized_formula_sha256": normalization["output_sha256"],
        "cvc5_status": cvc5["verdict"],
        "cvc5_solver_sha256": cvc5["solver_sha256"],
    }


def audit_genericity_core(core_path, normalization_path, cvc5_path):
    core = json.loads(core_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    source_path = Path(core["source"])
    formula_path = Path(core["core_formula"])
    normalized_path = Path(normalization["output"])
    expected_bounds = {
        ((0, 1, 4), (2,), "wall_epsilon < value_0_4"),
        ((0, 1, 5), (2,), "wall_epsilon < value_0_5"),
    }
    recorded_bounds = {
        (
            tuple(record["left"]),
            tuple(record["right"]),
            record["equivalent_small_step_bound"],
        )
        for record in core.get("canonical_core", ())
    }
    if (
        core.get("status") != "GENERICITY_ASSUMPTION_CORE_EXTRACTED"
        or core.get("n") != 4
        or core.get("m") != 7
        or core.get("candidate_partition_count") != 7
        or core.get("relaxed_status") != "sat"
        or core.get("full_status") != "unsat"
        or core.get("canonical_core_status") != "unsat"
        or core.get("canonical_core_size") != 2
        or not core.get("canonical_core_deletion_minimal")
        or recorded_bounds != expected_bounds
        or core.get("small_step_condition")
        != "0 < wall_epsilon < min(value_0_4, value_0_5)"
        or not source_path.is_file()
        or hashlib.sha256(source_path.read_bytes()).hexdigest()
        != core["source_sha256"]
        or not formula_path.is_file()
        or hashlib.sha256(formula_path.read_bytes()).hexdigest()
        != core["core_formula_sha256"]
        or normalization["source_sha256"] != core["core_formula_sha256"]
        or not normalized_path.is_file()
        or hashlib.sha256(normalized_path.read_bytes()).hexdigest()
        != normalization["output_sha256"]
        or cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
    ):
        raise AssertionError("two-comparison genericity core audit failed")
    return {
        "source": str(core_path),
        "source_sha256": hashlib.sha256(core_path.read_bytes()).hexdigest(),
        "candidate_partition_count": 7,
        "full_genericity_pair_count": core["genericity_pair_count"],
        "canonical_core_size": 2,
        "canonical_core_deletion_minimal": True,
        "small_step_condition": core["small_step_condition"],
        "core_formula_sha256": core["core_formula_sha256"],
        "normalized_formula_sha256": normalization["output_sha256"],
        "cvc5_status": cvc5["verdict"],
        "cvc5_solver_sha256": cvc5["solver_sha256"],
    }


def audit_pair_pivot(source_path, normalization_path, cvc5_path):
    source = json.loads(source_path.read_text())
    normalization = json.loads(normalization_path.read_text())
    cvc5 = json.loads(cvc5_path.read_text())
    formula_path = Path(source["formula"])
    normalized_path = Path(normalization["output"])
    pivots = {
        canonical(tuple(tuple(bundle) for bundle in partition))
        for partition in source.get("pivots", ())
    }
    if (
        source.get("schema")
        != "row-merge-q4-small-step-pair-pivot-lra-v1"
        or source.get("status") != "PAIR_PIVOT_LEMMA_VERIFIED"
        or source.get("solver_status") != "unsat"
        or source.get("n") != 4
        or source.get("m") != 8
        or source.get("minimal_hall_witness_size") != 4
        or source.get("wall_partition")
        != [[0, 1], [2, 3], [4, 5], [6, 7]]
        or source.get("pivot_count") != 11
        or len(pivots) != 11
        or source.get("small_step_goods") != [4, 5, 6, 7]
        or not formula_path.is_file()
        or hashlib.sha256(formula_path.read_bytes()).hexdigest()
        != source["formula_sha256"]
        or normalization["source_sha256"] != source["formula_sha256"]
        or not normalized_path.is_file()
        or hashlib.sha256(normalized_path.read_bytes()).hexdigest()
        != normalization["output_sha256"]
        or cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("formula_sha256") != normalization["output_sha256"]
    ):
        raise AssertionError("four-pair small-step pivot audit failed")
    return {
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "scope": "four agents, eight goods, wall shape 2+2+2+2, Hall size four",
        "pivot_count": 11,
        "small_step_condition": source["small_step_condition"],
        "z3_status": source["solver_status"],
        "formula_sha256": source["formula_sha256"],
        "normalized_formula_sha256": normalization["output_sha256"],
        "cvc5_status": cvc5["verdict"],
        "cvc5_solver_sha256": cvc5["solver_sha256"],
    }


def run(
    sources,
    output,
    unsat_source=None,
    normalization=None,
    cvc5=None,
    core=None,
    core_normalization=None,
    core_cvc5=None,
    genericity_core=None,
    genericity_normalization=None,
    genericity_cvc5=None,
    pair_pivot=None,
    pair_pivot_normalization=None,
    pair_pivot_cvc5=None,
):
    if output.exists():
        raise ValueError("output path already exists")
    records = [audit_source(source) for source in sources]
    boundary_inputs = (unsat_source, normalization, cvc5)
    if any(boundary_inputs) and not all(boundary_inputs):
        raise ValueError("all three UNSAT-boundary inputs are required together")
    unsat_boundary = (
        audit_unsat_boundary(unsat_source, normalization, cvc5)
        if all(boundary_inputs)
        else None
    )
    core_inputs = (core, core_normalization, core_cvc5)
    if any(core_inputs) and not all(core_inputs):
        raise ValueError("all three core inputs are required together")
    core_record = (
        audit_core(core, core_normalization, core_cvc5)
        if all(core_inputs)
        else None
    )
    genericity_inputs = (
        genericity_core,
        genericity_normalization,
        genericity_cvc5,
    )
    if any(genericity_inputs) and not all(genericity_inputs):
        raise ValueError("all three genericity-core inputs are required together")
    genericity_record = (
        audit_genericity_core(*genericity_inputs)
        if all(genericity_inputs)
        else None
    )
    pair_pivot_inputs = (
        pair_pivot,
        pair_pivot_normalization,
        pair_pivot_cvc5,
    )
    if any(pair_pivot_inputs) and not all(pair_pivot_inputs):
        raise ValueError("all three pair-pivot inputs are required together")
    pair_pivot_record = (
        audit_pair_pivot(*pair_pivot_inputs)
        if all(pair_pivot_inputs)
        else None
    )
    result = {
        "schema": SCHEMA,
        "status": "SINGLE_WALL_RADIUS_REFUTATIONS_AUDITED",
        "source_count": len(records),
        "records": records,
        "dual_solver_unsat_boundary": unsat_boundary,
        "dual_solver_seven_partition_core": core_record,
        "dual_solver_two_comparison_core": genericity_record,
        "dual_solver_four_pair_pivot": pair_pivot_record,
        "claim": (
            "Generic essential single-wall failures can defeat fixed radius-two "
            "menus, while the audited Hall-size-four small-step cells admit one "
            "of seven pivots at m=7 and one of eleven pivots at balanced m=8."
        ),
        "claim_boundary": (
            "The m=8 positive result covers only wall shape 2+2+2+2 and a "
            "minimal Hall witness of size four. It does not prove row-merge "
            "continuation or general additive EFX existence."
        ),
    }
    atomic_json(output, result)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, action="append", required=True)
    parser.add_argument("--unsat-source", type=Path)
    parser.add_argument("--normalization", type=Path)
    parser.add_argument("--cvc5", type=Path)
    parser.add_argument("--core", type=Path)
    parser.add_argument("--core-normalization", type=Path)
    parser.add_argument("--core-cvc5", type=Path)
    parser.add_argument("--genericity-core", type=Path)
    parser.add_argument("--genericity-normalization", type=Path)
    parser.add_argument("--genericity-cvc5", type=Path)
    parser.add_argument("--pair-pivot", type=Path)
    parser.add_argument("--pair-pivot-normalization", type=Path)
    parser.add_argument("--pair-pivot-cvc5", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(
        args.source,
        args.output,
        args.unsat_source,
        args.normalization,
        args.cvc5,
        args.core,
        args.core_normalization,
        args.core_cvc5,
        args.genericity_core,
        args.genericity_normalization,
        args.genericity_cvc5,
        args.pair_pivot,
        args.pair_pivot_normalization,
        args.pair_pivot_cvc5,
    )


if __name__ == "__main__":
    main()
