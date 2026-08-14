#!/usr/bin/env python3
"""Physical two-slot packet CEGAR for seven endpoints versus full PI."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from fractions import Fraction
from pathlib import Path

import z3

from .audit_allocated_e_physical_packet_counterprofile import (
    find_closed_disjoint_family,
    find_closed_disjoint_families,
    find_four_edge_efx,
)
from .decide_allocated_e_seven_endpoint_packet_lift import (
    ROOT,
    build_packet_master,
    endpoint_efx,
    minimum,
    response,
)
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS, SUPPORT_STATE


def rational(model, expression):
    return Fraction(str(model.eval(expression, model_completion=True)))


def slot_name(piece, slot):
    return f"{piece}.{slot}"


def slot_piece(name):
    piece, slot = name.rsplit(".", 1)
    return piece, int(slot)


def slot_expression(value, least, piece, slot, observer):
    return least[piece, observer] if slot == 0 else value[piece, observer] - least[piece, observer]


def explicit_model(model, value, least, singleton):
    expansion = {}
    values = {owner: {} for owner in OWNERS}
    for piece in GOODS:
        is_singleton = z3.is_true(model.eval(singleton[piece], model_completion=True))
        names = (slot_name(piece, 0),) if is_singleton else (
            slot_name(piece, 0), slot_name(piece, 1),
        )
        expansion[piece] = names
        for observer in OWNERS:
            for name in names:
                _, slot = slot_piece(name)
                values[observer][name] = rational(
                    model, slot_expression(value, least, piece, slot, observer)
                )
    base = {
        owner: tuple(good for piece in pieces for good in expansion[piece])
        for owner, pieces in ALLOCATED_E_BASE.items()
    }
    support = {
        owner: tuple(good for piece in pieces for good in expansion[piece])
        for owner, pieces in SUPPORT_STATE.items()
    }
    goods = tuple(good for piece in GOODS for good in expansion[piece])
    classes = {piece: "singleton" if len(expansion[piece]) == 1 else "two"
               for piece in GOODS}
    return goods, values, base, support, classes


def symbolic_pi_cut(value, least, singleton, witness):
    active = []
    relations = []
    for source, names in sorted(witness.items()):
        expressions = {observer: [] for observer in OWNERS}
        for name in names:
            piece, slot = slot_piece(name)
            if slot == 1:
                active.append(z3.Not(singleton[piece]))
            for observer in OWNERS:
                expressions[observer].append(
                    slot_expression(value, least, piece, slot, observer)
                )
        # Use the literal deletion-tail expansion rather than a nested minimum
        # ITE.  For additive values, tail(B)<=1 iff B-g<=1 for every atomic
        # member g of B.  This is formula-equivalent and substantially cheaper
        # when all 1,372 closed self cores are preseeded.
        relations.append(z3.And(
            z3.Sum(*expressions[source]) > 1,
            *(
                z3.Sum(*(amount for index, amount in enumerate(expressions[observer])
                         if index != removed)) <= 1
                for observer in OWNERS
                for removed in range(len(expressions[observer]))
            ),
        ))
    return z3.Not(z3.And(*active, *relations))


def witness_signature(witness):
    return tuple(sorted((source, tuple(sorted(names))) for source, names in witness.items()))


def signatures_from_result(payload):
    signatures = set()
    for signature in payload.get("restored_physical_pi_signatures", []):
        signatures.add(tuple(
            (source, tuple(sorted(names))) for source, names in signature
        ))
    for record in payload["iterations"]:
        for signature in record.get("batch_physical_pi_signatures", []):
            signatures.add(tuple(
                (source, tuple(sorted(names))) for source, names in signature
            ))
        signature = record.get("physical_pi_signature")
        if signature is not None:
            signatures.add(tuple(
                (source, tuple(sorted(names))) for source, names in signature
            ))
    return signatures


def all_self_pi_witnesses():
    """Enumerate every closed one-owner core in the physical two-slot model.

    A one-owner generalized PI may use only that owner's base goods and the
    charity goods.  Every named piece has a minimum slot and a residual slot,
    except ``p``, which the master fixes to be a singleton.  Enumerating these
    subsets is small (1,372 witnesses) and prevents the lazy loop from learning
    elementary self-PI cuts one model at a time.
    """
    charity = tuple(ALLOCATED_E_BASE["charity"])
    for source in OWNERS:
        pieces = (*ALLOCATED_E_BASE[source], *charity)
        names = tuple(
            slot_name(piece, slot)
            for piece in pieces
            for slot in ((0,) if piece == "p" else (0, 1))
        )
        for size in range(1, len(names) + 1):
            for subset in itertools.combinations(names, size):
                yield {source: list(subset)}


def physical_self_pi_witnesses(values, base):
    """Return every inclusion-minimal closed self core in an exact model."""
    charity = tuple(base["charity"])
    witnesses = []
    for source in OWNERS:
        universe = (*tuple(base[source]), *charity)
        for mask in range(1, 1 << len(universe)):
            names = tuple(
                name for index, name in enumerate(universe)
                if mask & (1 << index)
            )
            source_total = sum((values[source][name] for name in names), Fraction(0))
            if source_total <= 1:
                continue
            safe = True
            for observer in OWNERS:
                amounts = [values[observer][name] for name in names]
                if sum(amounts, Fraction(0)) - min(amounts) > 1:
                    safe = False
                    break
            if not safe:
                continue
            if any(source_total - values[source][name] > 1 for name in names):
                continue
            witnesses.append({source: list(names)})
    return witnesses


def run(core_source: Path, output: Path, timeout_seconds: int,
        random_seed: int, maximum_iterations: int,
        preseed_all_self_pi: bool = False,
        batch_all_model_self_pi: bool = False,
        batch_all_model_pi: bool = False,
        maximum_pi_families_per_round: int = 1000,
        resume: Path | None = None):
    core_source = core_source.resolve()
    core = json.loads(core_source.read_text())
    whole_signatures = [
        tuple((source, tuple(pieces)) for source, pieces in signature)
        for signature in core["pi_signatures"]
    ]
    allocations = core["allocations"]
    solver, value, least = build_packet_master()
    singleton = {piece: z3.Bool(f"cegar_singleton_{piece}") for piece in GOODS}
    for piece in GOODS:
        for observer in OWNERS:
            solver.add(z3.If(
                singleton[piece],
                value[piece, observer] == least[piece, observer],
                value[piece, observer] >= 2 * least[piece, observer],
            ))
    solver.add(singleton["p"])
    for signature in whole_signatures:
        solver.add(z3.Or(*(
            z3.Not(response(value, least, source, pieces))
            for source, pieces in signature
        )))
    for allocation in allocations:
        solver.add(z3.Not(endpoint_efx(value, least, allocation)))
    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)

    signatures = set()
    preseeded_self_pi_cut_count = 0
    if preseed_all_self_pi:
        for witness in all_self_pi_witnesses():
            signature = witness_signature(witness)
            signatures.add(signature)
            solver.add(symbolic_pi_cut(value, least, singleton, witness))
            preseeded_self_pi_cut_count += 1
    restored_signatures = set()
    resume_payload = None
    if resume is not None:
        resume = resume.resolve()
        resume_payload = json.loads(resume.read_text())
        if resume_payload["core_source_sha256"] != hashlib.sha256(core_source.read_bytes()).hexdigest():
            raise ValueError("resume core source does not match")
        restored_signatures = signatures_from_result(resume_payload)
        for signature in sorted(restored_signatures):
            if signature in signatures:
                continue
            signatures.add(signature)
            solver.add(symbolic_pi_cut(value, least, singleton, {
                source: list(names) for source, names in signature
            }))
    result = {
        "schema": "allocated-e-seven-endpoint-physical-subpacket-pi-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "whole_packet_pi_clause_count": len(whole_signatures),
        "endpoint_count": len(allocations),
        "timeout_seconds_per_check": timeout_seconds,
        "random_seed": random_seed,
        "maximum_iterations": maximum_iterations,
        "preseed_all_self_pi": preseed_all_self_pi,
        "preseeded_self_pi_cut_count": preseeded_self_pi_cut_count,
        "batch_all_model_self_pi": batch_all_model_self_pi,
        "batch_all_model_pi": batch_all_model_pi,
        "maximum_pi_families_per_round": maximum_pi_families_per_round,
        "resume": None if resume is None else str(resume.relative_to(ROOT)),
        "resume_sha256": None if resume is None else hashlib.sha256(resume.read_bytes()).hexdigest(),
        "restored_physical_pi_cut_count": len(restored_signatures),
        "restored_physical_pi_signatures": [
            [[source, list(names)] for source, names in signature]
            for signature in sorted(restored_signatures)
        ],
        "iterations": [],
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "physical_pi_oracle_source_sha256": hashlib.sha256(
            (ROOT / "tracks/parkability/audit_allocated_e_physical_packet_counterprofile.py").read_bytes()
        ).hexdigest(),
        "claim_boundary": (
            "Exact CEGAR over physically realizable one/two-good refinements of "
            "the twelve named pieces. It separates every generalized PI over "
            "physical subgoods. Terminal SAT without PI refutes the seven-endpoint "
            "selector only; a full theorem countermodel would additionally require "
            "no unrestricted four-edge EFX allocation and every saturation premise."
        ),
    }
    started = time.monotonic()

    def checkpoint():
        result["physical_subpacket_pi_cut_count"] = len(signatures)
        result["dynamic_physical_subpacket_pi_cut_count"] = (
            len(signatures) - preseeded_self_pi_cut_count
        )
        result["elapsed_seconds"] = time.monotonic() - started
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    for iteration in range(maximum_iterations):
        status = solver.check()
        record = {"iteration": iteration, "solver_status": str(status)}
        if status == z3.unsat:
            result["status"] = "UNSAT_PI_OR_SEVEN_ENDPOINT_EFX"
            result["iterations"].append(record)
            checkpoint()
            break
        if status == z3.unknown:
            record["reason_unknown"] = solver.reason_unknown()
            result["status"] = "UNKNOWN"
            result["iterations"].append(record)
            checkpoint()
            break
        model = solver.model()
        goods, exact_values, base, support, classes = explicit_model(
            model, value, least, singleton,
        )
        if batch_all_model_self_pi:
            model_self_witnesses = physical_self_pi_witnesses(exact_values, base)
            fresh_self_witnesses = [
                witness for witness in model_self_witnesses
                if witness_signature(witness) not in signatures
            ]
            if fresh_self_witnesses:
                for witness in fresh_self_witnesses:
                    signature = witness_signature(witness)
                    signatures.add(signature)
                    solver.add(symbolic_pi_cut(value, least, singleton, witness))
                record["packet_cardinality_class"] = classes
                record["physical_good_count"] = len(goods)
                record["batch_self_pi_count"] = len(model_self_witnesses)
                record["fresh_batch_self_pi_cut_count"] = len(fresh_self_witnesses)
                record["batch_physical_pi_signatures"] = [
                    [
                        [source, list(names)]
                        for source, names in witness_signature(witness)
                    ]
                    for witness in fresh_self_witnesses
                ]
                result["iterations"].append(record)
                checkpoint()
                continue
        if batch_all_model_pi:
            witnesses, counts = find_closed_disjoint_families(
                exact_values, goods, base, minimum_size=2,
                maximum=maximum_pi_families_per_round,
            )
            fresh_witnesses = [
                witness for witness in witnesses
                if witness_signature(witness) not in signatures
            ]
            if fresh_witnesses:
                for witness in fresh_witnesses:
                    signature = witness_signature(witness)
                    signatures.add(signature)
                    solver.add(symbolic_pi_cut(value, least, singleton, witness))
                record["packet_cardinality_class"] = classes
                record["physical_good_count"] = len(goods)
                record["minimal_common_safe_desired_core_counts"] = counts
                record["batch_multiowner_pi_count"] = len(witnesses)
                record["fresh_batch_multiowner_pi_cut_count"] = len(fresh_witnesses)
                record["batch_physical_pi_signatures"] = [
                    [[source, list(names)] for source, names in witness_signature(witness)]
                    for witness in fresh_witnesses
                ]
                result["iterations"].append(record)
                checkpoint()
                continue
            witness = None
        else:
            witness, counts = find_closed_disjoint_family(exact_values, goods, base)
        record["packet_cardinality_class"] = classes
        record["physical_good_count"] = len(goods)
        record["minimal_common_safe_desired_core_counts"] = counts
        if witness is None:
            efx_status, efx = find_four_edge_efx(
                exact_values, goods, support, timeout_seconds, random_seed,
            )
            record["unrestricted_four_edge_efx_status"] = efx_status
            record["unrestricted_four_edge_efx_witness"] = efx
            result["status"] = (
                "SAT_PI_FREE_WITH_OTHER_FOUR_EDGE_EFX" if efx is not None
                else "SAT_PI_FREE_NO_FOUR_EDGE_EFX" if efx_status == "unsat"
                else "SAT_PI_FREE_EFX_UNKNOWN"
            )
            result["iterations"].append(record)
            checkpoint()
            break
        signature = witness_signature(witness)
        if signature in signatures:
            raise AssertionError("physical PI oracle returned no fresh witness")
        signatures.add(signature)
        solver.add(symbolic_pi_cut(value, least, singleton, witness))
        record["physical_pi_witness"] = witness
        record["physical_pi_signature"] = [
            [source, list(names)] for source, names in signature
        ]
        result["iterations"].append(record)
        checkpoint()
    else:
        result["status"] = "ITERATION_LIMIT"
        checkpoint()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--random-seed", type=int, default=524287)
    parser.add_argument("--maximum-iterations", type=int, default=500)
    parser.add_argument("--preseed-all-self-pi", action="store_true")
    parser.add_argument("--batch-all-model-self-pi", action="store_true")
    parser.add_argument("--batch-all-model-pi", action="store_true")
    parser.add_argument("--maximum-pi-families-per-round", type=int, default=1000)
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    result = run(
        args.core_source, args.output, args.timeout_seconds,
        args.random_seed, args.maximum_iterations, args.preseed_all_self_pi,
        args.batch_all_model_self_pi,
        args.batch_all_model_pi, args.maximum_pi_families_per_round,
        args.resume,
    )
    print(json.dumps({
        "status": result["status"],
        "iterations": len(result["iterations"]),
        "physical_pi_cuts": result["physical_subpacket_pi_cut_count"],
        "elapsed_seconds": result["elapsed_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
