#!/usr/bin/env python3
"""Solver-free exact audit of the residual-flower packet countermodel."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from . import audit_residual_flower_packet_core as packet
except ImportError:
    import audit_residual_flower_packet_core as packet


RECIPIENTS = packet.AGENTS + ("_",)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def amount(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction())


def tail(values, observer, goods):
    goods = tuple(goods)
    return amount(values, observer, goods) - min(
        (values[observer][good] for good in goods), default=Fraction()
    )


def is_efx(values, allocation):
    return all(
        amount(values, observer, allocation[observer])
        >= tail(values, observer, allocation[target])
        for observer in packet.AGENTS for target in packet.AGENTS
    ) and all(
        amount(values, observer, allocation[observer])
        >= amount(values, observer, allocation["_"])
        for observer in packet.AGENTS
    )


def lex_vector(values, allocation):
    return tuple(
        amount(values, agent, allocation[agent]) for agent in packet.AGENTS
    )


def expand(allocation, packet_goods):
    return {
        recipient: tuple(
            good
            for name in allocation[recipient]
            for good in packet_goods[name]
        )
        for recipient in RECIPIENTS
    }


def subset_sum_injective(row, goods):
    seen = set()
    for mask in range(1 << len(goods)):
        value = sum((
            row[good] for index, good in enumerate(goods)
            if mask & (1 << index)
        ), Fraction())
        if value in seen:
            return False
        seen.add(value)
    return True


def one_move_allocations(base, goods):
    source = {
        good: recipient
        for recipient, bundle in base.items()
        for good in bundle
    }
    yield base
    for good in goods:
        old = source[good]
        for new in RECIPIENTS:
            if new == old:
                continue
            candidate = {recipient: list(bundle) for recipient, bundle in base.items()}
            candidate[old].remove(good)
            candidate[new].append(good)
            yield {recipient: tuple(bundle) for recipient, bundle in candidate.items()}


def run(source_path):
    payload = json.loads(source_path.read_text())
    packet_goods = {
        name: tuple(goods) for name, goods in payload["packet_goods"].items()
    }
    values = {
        agent: {good: Fraction(value) for good, value in row.items()}
        for agent, row in payload["values"].items()
    }
    goods = tuple(next(iter(values.values())))
    assert all(set(row) == set(goods) for row in values.values())
    assert set(itertools.chain.from_iterable(packet_goods.values())) == set(goods)
    assert all(value > 0 for row in values.values() for value in row.values())

    base = expand({**packet.BASE, "_": ("f",)}, packet_goods)
    displayed = {
        name: tuple(good for part in parts for good in packet_goods[part])
        for name, parts in packet.DISPLAYED.items()
    }
    assert is_efx(values, base)
    assert all(
        amount(values, observer, base[observer]) >= values[observer][packet_goods["f"][0]]
        for observer in packet.AGENTS
    )
    assert all(
        amount(values, observer, base[observer])
        >= tail(values, observer, bundle)
        for observer in packet.AGENTS for bundle in displayed.values()
    )
    assert all(
        amount(values, source, displayed[name])
        > amount(values, source, base[source])
        for name, source in packet.DESIRED.items()
    )
    assert amount(values, "r", base["r"]) > amount(values, "r", base["q"])
    assert amount(values, "q", base["q"]) > amount(values, "q", base["r"])
    assert all(
        amount(values, observer, base[observer])
        > amount(values, observer, base["c"])
        for observer in ("r", "q", "s")
    )
    assert amount(values, "q", packet_goods["f"]) <= amount(values, "q", packet_goods["bq"])
    assert amount(values, "q", packet_goods["k"]) <= amount(values, "q", packet_goods["tq"])
    assert amount(values, "q", packet_goods["k"] + packet_goods["j"]) > amount(values, "q", packet_goods["tq"])

    base_vector = lex_vector(values, base)
    candidates = [expand(allocation, packet_goods) for allocation in packet.CORE]
    blocked = [
        not (is_efx(values, allocation) and lex_vector(values, allocation) > base_vector)
        for allocation in candidates
    ]
    assert all(blocked)

    escape = {
        recipient: tuple(goods_) for recipient, goods_ in
        payload["smallest_global_escape"]["allocation"].items()
    }
    assert is_efx(values, escape)
    assert lex_vector(values, escape) > base_vector
    source = {
        good: recipient
        for recipient, bundle in base.items()
        for good in bundle
    }
    moved = sum(
        source[good] != recipient
        for recipient, bundle in escape.items() for good in bundle
    )
    assert moved == payload["smallest_global_escape"]["minimum_moved_goods"] == 2
    assert not any(
        is_efx(values, allocation) and lex_vector(values, allocation) > base_vector
        for allocation in one_move_allocations(base, goods)
    )

    injective = {
        agent: subset_sum_injective(values[agent], goods)
        for agent in packet.AGENTS
    }
    assert all(injective.values())
    script = Path(__file__).resolve()
    root = script.parents[2]
    try:
        source_display = str(source_path.relative_to(root))
    except ValueError:
        source_display = str(source_path)
    return {
        "schema": "residual-flower-packet-countermodel-audit-v1",
        "status": "EXACT_NONDEGENERATE_REFUTATION_OF_PACKET_CANDIDATES",
        "positive": True,
        "base_efx_with_charity": True,
        "displayed_common_safe": True,
        "desired_relations": True,
        "live_residual_polarity": True,
        "candidate_count": len(candidates),
        "all_candidates_blocked": all(blocked),
        "subset_sum_injective": injective,
        "displayed_escape_efx_and_lex_better": True,
        "minimum_moved_goods": moved,
        "one_move_allocations_excluded": 1 + len(goods) * (len(RECIPIENTS) - 1),
        "claim_boundary": (
            "solver-free exact-Fraction refutation of the nine packet-level "
            "candidates in one nondegenerate residual flower state; the "
            "two-good escape shows the missing item-level component and does "
            "not refute the adaptive flower bridge"
        ),
        "provenance": {
            "source": source_display,
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
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
