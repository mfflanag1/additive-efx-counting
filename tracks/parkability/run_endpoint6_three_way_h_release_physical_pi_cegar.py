#!/usr/bin/env python3
"""Physical subpacket-PI CEGAR for the endpoint-6 three-way H release."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import z3

from .audit_allocated_e_physical_packet_counterprofile import (
    find_closed_disjoint_families,
    find_four_edge_efx,
)
from .decide_allocated_e_seven_endpoint_packet_lift import (
    ROOT,
    build_packet_master,
    endpoint_efx,
    response,
    total,
)
from .run_allocated_e_root_retention_new_debt_cegar import RETAINED
from .run_allocated_e_seven_endpoint_physical_pi_cegar import (
    all_self_pi_witnesses,
    explicit_model,
    physical_self_pi_witnesses,
    signatures_from_result,
    symbolic_pi_cut,
    witness_signature,
)
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


def run(
    core_source: Path,
    endpoint_source: Path,
    output: Path,
    timeout_seconds: int,
    random_seed: int,
    maximum_iterations: int,
    maximum_pi_families_per_round: int,
    preseed_all_self_pi: bool = False,
    resume: Path | None = None,
    resume_through_iteration: int | None = None,
    fixed_cardinality_source: Path | None = None,
    fixed_cardinality_iteration: int | None = None,
):
    core_source = core_source.resolve()
    endpoint_source = endpoint_source.resolve()
    core = json.loads(core_source.read_text())
    endpoint6 = json.loads(endpoint_source.read_text())["allocations"][5]
    retained = RETAINED[6]
    whole_signatures = tuple(
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    )
    allocations = tuple(core["allocations"])

    solver, value, least = build_packet_master()
    singleton = {piece: z3.Bool(f"h_release_cegar_singleton_{piece}") for piece in GOODS}
    for piece in GOODS:
        for observer in OWNERS:
            solver.add(z3.If(
                singleton[piece],
                value[piece, observer] == least[piece, observer],
                value[piece, observer] >= 2 * least[piece, observer],
            ))
    solver.add(singleton["p"])
    fixed_cardinality_class = None
    if fixed_cardinality_source is not None:
        if fixed_cardinality_iteration is None:
            raise ValueError("fixed cardinality iteration is required")
        fixed_cardinality_source = fixed_cardinality_source.resolve()
        cardinality_payload = json.loads(fixed_cardinality_source.read_text())
        fixed_cardinality_class = cardinality_payload["iterations"][
            fixed_cardinality_iteration
        ]["packet_cardinality_class"]
        if set(fixed_cardinality_class) != set(GOODS):
            raise ValueError("fixed cardinality class does not cover all pieces")
        for piece, kind in fixed_cardinality_class.items():
            solver.add(singleton[piece] if kind == "singleton" else z3.Not(singleton[piece]))
    solver.add(
        endpoint_efx(value, least, endpoint6),
        total(value, "q", endpoint6["q"]) >= 1,
        total(value, "s", endpoint6["s"]) >= 1,
        total(value, "q", retained["q"]) < 1,
    )
    for signature in whole_signatures:
        solver.add(z3.Or(*(
            z3.Not(response(value, least, source, pieces))
            for source, pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(endpoint_efx(value, least, allocation)))

    signatures = set()
    preseeded_self_pi_cut_count = 0
    if preseed_all_self_pi:
        for witness in all_self_pi_witnesses():
            signature = witness_signature(witness)
            signatures.add(signature)
            solver.add(symbolic_pi_cut(value, least, singleton, witness))
            preseeded_self_pi_cut_count += 1
    restored = set()
    if resume is not None:
        resume = resume.resolve()
        payload = json.loads(resume.read_text())
        if payload["core_source_sha256"] != hashlib.sha256(core_source.read_bytes()).hexdigest():
            raise ValueError("resume core source does not match")
        if resume_through_iteration is not None:
            payload = dict(payload)
            payload["iterations"] = payload["iterations"][:resume_through_iteration + 1]
        restored = signatures_from_result(payload)
        for signature in sorted(restored):
            if signature in signatures:
                continue
            signatures.add(signature)
            solver.add(symbolic_pi_cut(value, least, singleton, {
                source: list(names) for source, names in signature
            }))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    result = {
        "schema": "endpoint6-three-way-h-release-physical-pi-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "endpoint_source": str(endpoint_source.relative_to(ROOT)),
        "endpoint_source_sha256": hashlib.sha256(endpoint_source.read_bytes()).hexdigest(),
        "whole_packet_pi_clause_count": len(whole_signatures),
        "release_allocation_count": len(allocations),
        "preseed_all_self_pi": preseed_all_self_pi,
        "preseeded_self_pi_cut_count": preseeded_self_pi_cut_count,
        "restored_physical_pi_cut_count": len(restored),
        "restored_physical_pi_signatures": [
            [[source, list(names)] for source, names in signature]
            for signature in sorted(restored)
        ],
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "maximum_pi_families_per_round": maximum_pi_families_per_round,
        "resume": None if resume is None else str(resume.relative_to(ROOT)),
        "resume_through_iteration": resume_through_iteration,
        "fixed_cardinality_source": (
            None if fixed_cardinality_source is None
            else str(fixed_cardinality_source.relative_to(ROOT))
        ),
        "fixed_cardinality_source_sha256": (
            None if fixed_cardinality_source is None
            else hashlib.sha256(fixed_cardinality_source.read_bytes()).hexdigest()
        ),
        "fixed_cardinality_iteration": fixed_cardinality_iteration,
        "fixed_cardinality_class": fixed_cardinality_class,
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Exact CEGAR over every physically realizable singleton/two-good "
            "refinement of the twelve pieces in the declared endpoint-6 debt "
            "chart. Terminal UNSAT proves this two-slot physical chart; terminal "
            "SAT without PI still requires unrestricted packet and premise audits."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["physical_subpacket_pi_cut_count"] = len(signatures)
        result["dynamic_physical_subpacket_pi_cut_count"] = (
            len(signatures) - result["preseeded_self_pi_cut_count"]
        )
        result["new_physical_subpacket_pi_cut_count_this_run"] = (
            len(signatures)
            - result["preseeded_self_pi_cut_count"]
            - result["restored_physical_pi_cut_count"]
        )
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        row = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PHYSICAL_PI_OR_THREE_WAY_H_RELEASE_EFX"
            result["iterations"].append(row)
            checkpoint()
            break
        if status == z3.unknown:
            row["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(row)
            checkpoint()
            break

        goods, exact_values, base, support, classes = explicit_model(
            solver.model(), value, least, singleton,
        )
        self_witnesses = physical_self_pi_witnesses(exact_values, base)
        fresh_self = [
            witness for witness in self_witnesses
            if witness_signature(witness) not in signatures
        ]
        if fresh_self:
            for witness in fresh_self:
                signature = witness_signature(witness)
                signatures.add(signature)
                solver.add(symbolic_pi_cut(value, least, singleton, witness))
            row.update({
                "packet_cardinality_class": classes,
                "physical_good_count": len(goods),
                "batch_self_pi_count": len(self_witnesses),
                "fresh_batch_self_pi_cut_count": len(fresh_self),
                "batch_physical_pi_signatures": [
                    [[source, list(names)] for source, names in witness_signature(witness)]
                    for witness in fresh_self
                ],
            })
            result["iterations"].append(row)
            checkpoint()
            continue
        witnesses, counts = find_closed_disjoint_families(
            exact_values,
            goods,
            base,
            minimum_size=2,
            maximum=maximum_pi_families_per_round,
        )
        fresh = [
            witness for witness in witnesses
            if witness_signature(witness) not in signatures
        ]
        row.update({
            "packet_cardinality_class": classes,
            "physical_good_count": len(goods),
            "minimal_common_safe_desired_core_counts": counts,
            "batch_multiowner_pi_count": len(witnesses),
            "fresh_batch_multiowner_pi_cut_count": len(fresh),
        })
        if fresh:
            for witness in fresh:
                signature = witness_signature(witness)
                signatures.add(signature)
                solver.add(symbolic_pi_cut(value, least, singleton, witness))
            row["batch_physical_pi_signatures"] = [
                [[source, list(names)] for source, names in witness_signature(witness)]
                for witness in fresh
            ]
            result["iterations"].append(row)
            checkpoint()
            continue

        efx_status, efx = find_four_edge_efx(
            exact_values, goods, support, timeout_seconds, random_seed,
        )
        row["unrestricted_four_edge_efx_status"] = efx_status
        row["unrestricted_four_edge_efx_witness"] = efx
        result["status"] = (
            "SAT_PI_FREE_WITH_OTHER_FOUR_EDGE_EFX" if efx is not None
            else "SAT_PI_FREE_NO_FOUR_EDGE_EFX" if efx_status == "unsat"
            else "SAT_PI_FREE_EFX_UNKNOWN"
        )
        result["iterations"].append(row)
        checkpoint()
        break
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--endpoint-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=86028163)
    parser.add_argument("--maximum-iterations", type=int, default=200)
    parser.add_argument("--maximum-pi-families-per-round", type=int, default=1000)
    parser.add_argument("--preseed-all-self-pi", action="store_true")
    parser.add_argument("--resume", type=Path)
    parser.add_argument("--resume-through-iteration", type=int)
    parser.add_argument("--fixed-cardinality-source", type=Path)
    parser.add_argument("--fixed-cardinality-iteration", type=int)
    args = parser.parse_args()
    result = run(
        args.core_source,
        args.endpoint_source,
        args.output,
        args.timeout_seconds,
        args.random_seed,
        args.maximum_iterations,
        args.maximum_pi_families_per_round,
        args.preseed_all_self_pi,
        args.resume,
        args.resume_through_iteration,
        args.fixed_cardinality_source,
        args.fixed_cardinality_iteration,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
        "physical_pi_cuts": result["physical_subpacket_pi_cut_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
