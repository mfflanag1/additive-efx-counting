#!/usr/bin/env python3
"""Independent threshold-CNF checker for the bounded full-cell core."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import time
from pathlib import Path
from typing import Sequence

import pysat
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

try:
    from .terminal_cnf import (
        atomic_json,
        decode_values,
        export_dimacs,
        solve_with_timeout,
    )
except ImportError:
    from terminal_cnf import (
        atomic_json,
        decode_values,
        export_dimacs,
        solve_with_timeout,
    )


SCHEMA = "distinct-half-full-cell-threshold-cnf-result-v1"
N = 4
M = 9
FAVORITE = 0


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def perfect_pairings(vertices: Sequence[int]):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_pairings(rest):
            yield (tuple(sorted((first, second))),) + tail


class Encoder:
    def __init__(self, cap: int) -> None:
        self.cap = cap
        self.vpool = IDPool()
        self.cnf = CNF()
        self.value_bits = [
            [
                [
                    self.variable(f"value_{agent}_{good}_ge_{threshold}")
                    for threshold in range(2, cap + 1)
                ]
                for good in range(M)
            ]
            for agent in range(N)
        ]
        self._duplicate_index = 0
        self.counts = {
            "linear_witnesses": 0,
            "hall_witnesses": 0,
            "partition_violation_selectors": 0,
        }
        self.partition_guards = []
        for row in self.value_bits:
            for bits in row:
                for lower, higher in zip(bits, bits[1:]):
                    self.cnf.append([-higher, lower])

    def variable(self, name: str) -> int:
        return self.vpool.id(name)

    def distinct_literals(self, literals: Sequence[int]) -> list[int]:
        seen = set()
        result = []
        for literal in literals:
            if literal not in seen:
                seen.add(literal)
                result.append(literal)
                continue
            clone = self.variable(f"duplicate_literal_{self._duplicate_index}")
            self._duplicate_index += 1
            self.cnf.append([-clone, literal])
            self.cnf.append([clone, -literal])
            result.append(clone)
        return result

    def add_guarded_atleast(
        self,
        guard: int | None,
        literals: Sequence[int],
        bound: int,
    ) -> None:
        literals = self.distinct_literals(literals)
        if bound <= 0:
            return
        if bound > len(literals):
            self.cnf.append([] if guard is None else [-guard])
            return
        encoded = CardEnc.atleast(
            lits=literals,
            bound=bound,
            vpool=self.vpool,
            encoding=EncType.seqcounter,
        )
        for clause in encoded.clauses:
            self.cnf.append(clause if guard is None else [-guard, *clause])

    def sum_literals(
        self,
        agent: int,
        left: Sequence[int],
        right: Sequence[int],
    ) -> list[int]:
        literals = [
            bit for good in left for bit in self.value_bits[agent][good]
        ]
        literals.extend(
            -bit for good in right for bit in self.value_bits[agent][good]
        )
        return literals

    def add_sum_relation(
        self,
        agent: int,
        left: Sequence[int],
        right: Sequence[int],
        *,
        strict: bool,
        guard: int | None = None,
    ) -> None:
        bound = self.cap * len(right) - len(left) + int(strict)
        self.add_guarded_atleast(
            guard,
            self.sum_literals(agent, left, right),
            bound,
        )

    def sum_witness(
        self,
        name: str,
        agent: int,
        left: Sequence[int],
        right: Sequence[int],
        *,
        strict: bool,
    ) -> int:
        witness = self.variable(name)
        self.add_sum_relation(
            agent, left, right, strict=strict, guard=witness
        )
        self.counts["linear_witnesses"] += 1
        return witness


def add_branch(encoder: Encoder) -> None:
    residual = tuple(range(1, M))
    for agent in range(N):
        for good in residual:
            encoder.add_sum_relation(
                agent, (FAVORITE,), (good,), strict=True
            )
        encoder.add_sum_relation(
            agent,
            (agent + 1, agent + 1),
            (FAVORITE,),
            strict=True,
        )

        for four_set in itertools.combinations(residual, 4):
            witnesses = []
            for removed in four_set:
                triple = tuple(good for good in four_set if good != removed)
                witnesses.append(
                    encoder.sum_witness(
                        f"threshold_agent_{agent}_four_{'_'.join(map(str, four_set))}_"
                        f"remove_{removed}",
                        agent,
                        triple,
                        (FAVORITE,),
                        strict=True,
                    )
                )
            encoder.cnf.append(witnesses)

        pair_edges = {}
        for edge in itertools.combinations(residual, 2):
            pair_edges[edge] = encoder.sum_witness(
                f"threshold_agent_{agent}_edge_{edge[0]}_{edge[1]}",
                agent,
                edge,
                (FAVORITE,),
                strict=True,
            )
        degree_six = []
        degree_four = []
        for good in residual:
            incident = [
                pair_edges[tuple(sorted((good, other)))]
                for other in residual
                if other != good
            ]
            six = encoder.variable(f"threshold_agent_{agent}_good_{good}_degree6")
            four = encoder.variable(f"threshold_agent_{agent}_good_{good}_degree4")
            encoder.add_guarded_atleast(six, incident, 6)
            encoder.add_guarded_atleast(four, incident, 4)
            degree_six.append(six)
            degree_four.append(four)
        case_six = encoder.variable(f"threshold_agent_{agent}_degree6_case")
        case_four = encoder.variable(f"threshold_agent_{agent}_degree4_case")
        encoder.add_guarded_atleast(case_six, degree_six, 3)
        encoder.add_guarded_atleast(case_four, degree_four, 4)
        encoder.cnf.append([case_six, case_four])

    for agent in range(N - 1):
        left_bits = encoder.value_bits[agent][FAVORITE]
        right_bits = encoder.value_bits[agent + 1][FAVORITE]
        for left, right in zip(left_bits, right_bits):
            encoder.cnf.append([-right, left])
    for good in range(5, M - 1):
        left_bits = encoder.value_bits[0][good]
        right_bits = encoder.value_bits[0][good + 1]
        for left, right in zip(left_bits, right_bits):
            encoder.cnf.append([-right, left])


def hall_failure_templates(matching):
    yield from (
        tuple((agent, edge) for agent in range(N)) for edge in matching
    )
    for edge_pair in itertools.combinations(matching, 2):
        for possible_neighbor in range(N):
            yield tuple(
                (agent, edge)
                for edge in edge_pair
                for agent in range(N)
                if agent != possible_neighbor
            )
    for possible_neighbors in itertools.combinations(range(N), 2):
        yield tuple(
            (agent, edge)
            for edge in matching
            for agent in range(N)
            if agent not in possible_neighbors
        )


def add_no_full_hall_cell(encoder: Encoder) -> dict:
    rejection = {}
    low_pair_cells = 0
    for lows in itertools.combinations(range(1, M), 2):
        residual = tuple(good for good in range(1, M) if good not in lows)
        for agent in range(N):
            for edge in itertools.combinations(residual, 2):
                for low in lows:
                    rejection[agent, edge, low] = encoder.sum_witness(
                        f"reject_lows_{lows[0]}_{lows[1]}_agent_{agent}_"
                        f"edge_{edge[0]}_{edge[1]}_low_{low}",
                        agent,
                        (FAVORITE, low),
                        edge,
                        strict=True,
                    )

        cell_witnesses = []
        for matching_position, matching in enumerate(perfect_pairings(residual)):
            templates = tuple(hall_failure_templates(matching))
            if len(templates) != 21:
                raise AssertionError("Hall template count changed")
            for template_position, required_rejections in enumerate(templates):
                witness = encoder.variable(
                    f"hall_failure_lows_{lows[0]}_{lows[1]}_"
                    f"matching_{matching_position}_template_{template_position}"
                )
                for agent, edge in required_rejections:
                    encoder.cnf.append(
                        [
                            -witness,
                            rejection[agent, edge, lows[0]],
                            rejection[agent, edge, lows[1]],
                        ]
                    )
                cell_witnesses.append(witness)
                encoder.counts["hall_witnesses"] += 1
        encoder.cnf.append(cell_witnesses)
        low_pair_cells += 1
    return {
        "low_pair_cells": low_pair_cells,
        "rejection_inequality_witnesses": len(rejection),
        "hall_witnesses": encoder.counts["hall_witnesses"],
        "hall_failure_templates_per_pairing": 21,
    }


def add_partition_obstruction(
    encoder: Encoder,
    partition,
    partition_position: int,
    activation: int | None = None,
) -> None:
    violation = {}
    for agent in range(N):
        for own_bundle, own in enumerate(partition):
            comparisons = []
            for target_bundle, target in enumerate(partition):
                if target_bundle == own_bundle:
                    continue
                for removed in target:
                    remainder = tuple(good for good in target if good != removed)
                    comparisons.append(
                        encoder.sum_witness(
                            f"partition_{partition_position}_agent_{agent}_"
                            f"own_{own_bundle}_target_{target_bundle}_remove_{removed}",
                            agent,
                            remainder,
                            own,
                            strict=True,
                        )
                    )
            selector = encoder.variable(
                f"partition_{partition_position}_agent_{agent}_"
                f"bundle_{own_bundle}_violation"
            )
            encoder.cnf.append([-selector, *comparisons])
            violation[agent, own_bundle] = selector
            encoder.counts["partition_violation_selectors"] += 1
    for matching in itertools.permutations(range(N)):
        clause = [violation[agent, matching[agent]] for agent in range(N)]
        encoder.cnf.append(
            clause if activation is None else [-activation, *clause]
        )


def validate_partitions(raw_partitions):
    partitions = []
    for raw in raw_partitions:
        partition = tuple(sorted(tuple(sorted(bundle)) for bundle in raw))
        if (
            tuple(sorted(map(len, partition), reverse=True)) != (3, 2, 2, 2)
            or sorted(good for bundle in partition for good in bundle)
            != list(range(M))
            or len(next(bundle for bundle in partition if FAVORITE in bundle)) != 2
        ):
            raise ValueError("invalid favorite-pair balanced partition")
        partitions.append(partition)
    if len(partitions) != len(set(partitions)):
        raise ValueError("duplicate partition")
    return tuple(partitions)


def build(
    source: dict,
    cap: int,
    fixed_values=None,
    *,
    partition_assumptions: bool = False,
):
    partitions = validate_partitions(source["core_partitions"])
    encoder = Encoder(cap)
    add_branch(encoder)
    full_cell_encoding = add_no_full_hall_cell(encoder)
    for position, partition in enumerate(partitions):
        activation = (
            encoder.variable(f"partition_{position}_activation")
            if partition_assumptions
            else None
        )
        add_partition_obstruction(
            encoder, partition, position, activation=activation
        )
        if activation is not None:
            encoder.partition_guards.append(activation)
    if fixed_values is not None:
        if len(fixed_values) != N or any(len(row) != M for row in fixed_values):
            raise ValueError("fixed values have wrong dimensions")
        for agent, row in enumerate(fixed_values):
            for good, value in enumerate(row):
                if type(value) is not int or not 1 <= value <= cap:
                    raise ValueError("fixed value outside cap")
                for threshold, bit in zip(
                    range(2, cap + 1), encoder.value_bits[agent][good]
                ):
                    encoder.cnf.append([bit if value >= threshold else -bit])
    encoder.cnf.nv = max(encoder.cnf.nv, encoder.vpool.top)
    return encoder, partitions, full_cell_encoding


def run(args):
    started = time.perf_counter()
    source_code = Path(__file__).resolve()
    source = json.loads(args.source.read_text())
    if source.get("cap") != args.cap or not source.get("core_partitions"):
        raise ValueError("source is not a compatible cap core")
    fixed_values = None
    if args.fixed_values is not None:
        fixed_payload = json.loads(args.fixed_values.read_text())
        fixed_values = fixed_payload.get("values", fixed_payload)
    build_started = time.perf_counter()
    encoder, partitions, full_cell_encoding = build(
        source, args.cap, fixed_values=fixed_values
    )
    build_seconds = time.perf_counter() - build_started
    export_dimacs(encoder.cnf, args.export)
    dimacs_hash = sha256(args.export)
    solve_started = time.perf_counter()
    solved, unknown_reason = solve_with_timeout(
        encoder.cnf.clauses, args.solver, args.timeout_seconds
    )
    solve_seconds = time.perf_counter() - solve_started
    status = "UNKNOWN" if solved is None else "SAT" if solved["status"] else "UNSAT"
    result = {
        "schema": SCHEMA,
        "status": status,
        "cap": args.cap,
        "source": str(args.source.resolve()),
        "source_sha256": sha256(args.source),
        "encoder_source_sha256": sha256(source_code),
        "partition_pool_size": len(partitions),
        "fixed_values": str(args.fixed_values.resolve()) if args.fixed_values else None,
        "encoding": {
            "implementation": "independent monotone-threshold CNF",
            "value_bits_per_entry": args.cap - 1,
            "universal_threshold": "four-set and pair-degree witnesses",
            "no_full_cell": full_cell_encoding,
            **encoder.counts,
        },
        "variables": encoder.cnf.nv,
        "clauses": len(encoder.cnf.clauses),
        "dimacs_path": str(args.export.resolve()),
        "dimacs_sha256": dimacs_hash,
        "dimacs_bytes": args.export.stat().st_size,
        "solver": {
            "status": status,
            "requested": args.solver,
            "backend": solved["backend"] if solved else None,
            "statistics": solved["statistics"] if solved else None,
            "cpu_seconds": solved["solver_cpu_seconds"] if solved else None,
            "timeout_seconds": args.timeout_seconds,
        },
        "seconds": {
            "build": round(build_seconds, 6),
            "solve_wall": round(solve_seconds, 6),
            "total": round(time.perf_counter() - started, 6),
        },
        "environment": {
            "python_sat": pysat.__version__,
            "platform": platform.platform(),
        },
    }
    if unknown_reason:
        result["reason_unknown"] = unknown_reason
    if solved and solved["status"]:
        result["values"] = [
            list(row) for row in decode_values(solved["model"], encoder.value_bits)
        ]
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))
    return 2 if status == "UNKNOWN" else 0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--cap", type=int, required=True)
    parser.add_argument("--export", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fixed-values", type=Path)
    parser.add_argument(
        "--solver", choices=("cadical195", "kissat404"), default="cadical195"
    )
    parser.add_argument("--timeout-seconds", type=float, default=600)
    args = parser.parse_args()
    if args.cap < 2 or not math.isfinite(args.timeout_seconds) or args.timeout_seconds < 0:
        parser.error("invalid cap or timeout")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
