#!/usr/bin/env python3
"""Independent replay for the physical-subpacket PI CEGAR certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3

from .decide_allocated_e_seven_endpoint_packet_lift import build_packet_master
from .run_allocated_e_capture_rank_three_cegar import ALLOCATED_E_BASE
from .run_fixed_u_full_packet_terminal_cegar import GOODS, OWNERS


ROOT = Path(__file__).resolve().parents[2]


def minimum(expressions):
    result = expressions[0]
    for expression in expressions[1:]:
        result = z3.If(expression < result, expression, result)
    return result


def slot_expression(value, least, name, observer):
    piece, slot_text = name.rsplit(".", 1)
    slot = int(slot_text)
    if slot == 0:
        return least[piece, observer]
    if slot == 1:
        return value[piece, observer] - least[piece, observer]
    raise AssertionError(f"invalid slot: {name}")


def literal_whole_response(value, source, pieces):
    pieces = tuple(pieces)
    return z3.And(
        z3.Sum(*(value[piece, source] for piece in pieces)) > 1,
        *(
            z3.Sum(*(value[piece, observer] for piece in pieces if piece != removed)) <= 1
            for observer in OWNERS for removed in pieces
        ),
    )


def direct_physical_endpoint(value, least, allocation):
    rows = []
    for observer in OWNERS:
        own = z3.Sum(*(value[piece, observer] for piece in allocation[observer]))
        for target in OWNERS:
            if target == observer:
                continue
            target_pieces = tuple(allocation[target])
            target_total = z3.Sum(*(value[piece, observer] for piece in target_pieces))
            rows.extend(
                own >= target_total - least[piece, observer]
                for piece in target_pieces
            )
    return z3.And(*rows)


def independent_pi_cut(value, least, singleton, signature):
    actives = []
    relations = []
    for source, names in signature:
        rows = {observer: [] for observer in OWNERS}
        for name in names:
            piece, slot_text = name.rsplit(".", 1)
            if int(slot_text) == 1:
                actives.append(z3.Not(singleton[piece]))
            for observer in OWNERS:
                rows[observer].append(slot_expression(value, least, name, observer))
        relations.append(z3.And(
            z3.Sum(*rows[source]) > 1,
            *(
                z3.Sum(*rows[observer]) - minimum(rows[observer]) <= 1
                for observer in OWNERS
            ),
        ))
    return z3.Not(z3.And(*actives, *relations))


def preseed_signatures():
    charity = tuple(ALLOCATED_E_BASE["charity"])
    for source in OWNERS:
        pieces = (*ALLOCATED_E_BASE[source], *charity)
        names = tuple(
            f"{piece}.{slot}"
            for piece in pieces
            for slot in ((0,) if piece == "p" else (0, 1))
        )
        for size in range(1, len(names) + 1):
            for subset in itertools.combinations(names, size):
                yield ((source, tuple(sorted(subset))),)


def learned_signatures(payload):
    signatures = set(preseed_signatures()) if payload.get("preseed_all_self_pi") else set()
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


def validate_signature(signature):
    sources = {source for source, _ in signature}
    assert sources and sources <= set(OWNERS)
    allowed = set(ALLOCATED_E_BASE["charity"])
    for source in sources:
        allowed.update(ALLOCATED_E_BASE[source])
    used = set()
    for source, names in signature:
        assert names
        for name in names:
            piece, slot_text = name.rsplit(".", 1)
            assert piece in allowed
            assert slot_text in {"0", "1"}
            assert name != "p.1"
            assert name not in used
            used.add(name)


def run(source: Path, output: Path, timeout_seconds: int, random_seed: int):
    source = source.resolve()
    payload = json.loads(source.read_text())
    assert payload["status"] == "UNSAT_PI_OR_SEVEN_ENDPOINT_EFX"
    core_path = ROOT / payload["core_source"]
    core = json.loads(core_path.read_text())
    assert hashlib.sha256(core_path.read_bytes()).hexdigest() == payload["core_source_sha256"]

    signatures = learned_signatures(payload)
    assert len(signatures) == payload["physical_subpacket_pi_cut_count"]
    for signature in signatures:
        validate_signature(signature)

    solver, value, least = build_packet_master()
    singleton = {piece: z3.Bool(f"audit_singleton_{piece}") for piece in GOODS}
    for piece in GOODS:
        for observer in OWNERS:
            solver.add(z3.If(
                singleton[piece],
                value[piece, observer] == least[piece, observer],
                value[piece, observer] >= 2 * least[piece, observer],
            ))
    solver.add(singleton["p"])
    for signature in core["pi_signatures"]:
        solver.add(z3.Or(*(
            z3.Not(literal_whole_response(value, source_name, pieces))
            for source_name, pieces in signature
        )))
    for allocation in core["allocations"]:
        solver.add(z3.Not(direct_physical_endpoint(value, least, allocation)))
    for signature in signatures:
        solver.add(independent_pi_cut(value, least, singleton, signature))

    solver.set(timeout=timeout_seconds * 1000, random_seed=random_seed)
    status = solver.check()
    result = {
        "schema": "allocated-e-physical-pi-cegar-unsat-audit-v1",
        "status": "AUDIT_PASSED" if status == z3.unsat else "AUDIT_FAILED",
        "solver_status": str(status),
        "producer": str(source.relative_to(ROOT)),
        "producer_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "core_source_sha256": hashlib.sha256(core_path.read_bytes()).hexdigest(),
        "replayed_physical_pi_cut_count": len(signatures),
        "independent_whole_response_encoding": "literal deletion tails",
        "independent_endpoint_encoding": "direct least-piece inequalities",
        "independent_subpacket_encoding": "nested minimum",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Independent formula replay of the exact one/two-good-per-piece "
            "UNSAT certificate. It is not by itself a proof for packets with "
            "more than two physical goods."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1800)
    parser.add_argument("--random-seed", type=int, default=104729)
    args = parser.parse_args()
    print(json.dumps(run(
        args.source, args.output, args.timeout_seconds, args.random_seed,
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
