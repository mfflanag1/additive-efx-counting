#!/usr/bin/env python3
"""Realize a packet-core model and find its smallest global lex escape."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import z3

try:
    from . import audit_residual_flower_packet_core as packet
except ImportError:
    import audit_residual_flower_packet_core as packet


RECIPIENTS = packet.AGENTS + ("_",)


def rational(model, expression):
    entry = model.eval(expression, model_completion=True)
    return Fraction(entry.numerator_as_long(), entry.denominator_as_long())


def realize(model):
    multiple = {
        name: z3.is_true(model.eval(
            z3.Bool(f"packet_multiple_{name}"), model_completion=True
        ))
        for name in packet.PACKETS
    }
    goods = []
    values = {agent: {} for agent in packet.AGENTS}
    source = {}
    packet_goods = {}
    for name in packet.PACKETS:
        names = (f"{name}0", f"{name}1") if multiple[name] else (name,)
        packet_goods[name] = names
        goods.extend(names)
        owner = next(
            (agent for agent, bundles in packet.BASE.items() if name in bundles),
            "_",
        )
        source.update({good: owner for good in names})
        for agent in packet.AGENTS:
            total = rational(model, z3.Real(f"packet_total_{agent}_{name}"))
            least = rational(model, z3.Real(f"packet_min_{agent}_{name}"))
            if multiple[name]:
                values[agent][names[0]] = least
                values[agent][names[1]] = total - least
            else:
                values[agent][names[0]] = total
    return goods, values, source, packet_goods


def amount(values, owner, observer, recipient, index, goods):
    return z3.Sum(*(
        z3.If(
            owner[good] == index[recipient],
            z3.RealVal(str(values[observer][good])),
            0,
        )
        for good in goods
    ))


def find_escape(goods, values, source, packet_goods):
    index = {recipient: position for position, recipient in enumerate(RECIPIENTS)}
    owner = {good: z3.Int(f"escape_owner_{good}") for good in goods}
    solver = z3.Optimize()
    for good in goods:
        solver.add(owner[good] >= 0, owner[good] < len(RECIPIENTS))

    own = {
        agent: amount(values, owner, agent, agent, index, goods)
        for agent in packet.AGENTS
    }
    for observer in packet.AGENTS:
        for target in packet.AGENTS:
            target_total = amount(values, owner, observer, target, index, goods)
            for good in goods:
                solver.add(z3.Implies(
                    owner[good] == index[target],
                    own[observer]
                    >= target_total - z3.RealVal(str(values[observer][good])),
                ))
        solver.add(
            own[observer]
            >= amount(values, owner, observer, "_", index, goods)
        )

    base = {
        agent: sum((
            values[agent][good]
            for name in packet.BASE[agent]
            for good in packet_goods[name]
        ), Fraction())
        for agent in packet.AGENTS
    }
    solver.add(packet.lex_greater(
        tuple(own[agent] for agent in packet.AGENTS),
        tuple(z3.RealVal(str(base[agent])) for agent in packet.AGENTS),
    ))
    moved = z3.Sum(*(
        z3.If(owner[good] != index[source[good]], 1, 0)
        for good in goods
    ))
    solver.minimize(moved)
    checked = solver.check()
    if checked != z3.sat:
        return {"status": str(checked)}
    model = solver.model()
    allocation = {
        recipient: [
            good for good in goods
            if model.eval(owner[good], model_completion=True).as_long()
            == index[recipient]
        ]
        for recipient in RECIPIENTS
    }
    transfers = [
        f"{source[good]}->{recipient}:{good}"
        for recipient in RECIPIENTS
        for good in allocation[recipient]
        if source[good] != recipient
    ]
    return {
        "status": "SAT_GLOBAL_LEX_ESCAPE",
        "minimum_moved_goods": model.eval(moved).as_long(),
        "allocation": allocation,
        "transfers": transfers,
        "base_utilities": {agent: str(base[agent]) for agent in packet.AGENTS},
        "new_utilities": {
            agent: str(rational(model, own[agent]))
            for agent in packet.AGENTS
        },
    }


def run():
    solver = packet.build(True)
    checked = solver.check()
    result = {
        "schema": "residual-flower-packet-countermodel-analysis-v1",
        "solver": f"Z3 {z3.get_version_string()}",
        "candidate_count": len(packet.CORE),
        "packet_core_status": str(checked),
    }
    if checked != z3.sat:
        result["status"] = "NO_PACKET_COUNTERMODEL"
        return result
    goods, values, source, packet_goods = realize(solver.model())
    result.update({
        "status": "REALIZABLE_PACKET_COUNTERMODEL",
        "good_count": len(goods),
        "packet_goods": {name: list(entries) for name, entries in packet_goods.items()},
        "values": {
            agent: {good: str(value) for good, value in row.items()}
            for agent, row in values.items()
        },
        "smallest_global_escape": find_escape(
            goods, values, source, packet_goods
        ),
        "claim_boundary": (
            "an exact positive additive obstruction to the listed packet-level "
            "candidate family, not to the adaptive flower bridge; the reported "
            "global escape identifies a missing operation"
        ),
    })
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "candidate_count": result["candidate_count"],
        "packet_core_status": result["packet_core_status"],
        "smallest_global_escape": result.get("smallest_global_escape"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
