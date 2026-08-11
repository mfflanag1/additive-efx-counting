#!/usr/bin/env python3
"""Arbitrary-packet audit of the residual-flower candidate core."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3


AGENTS = ("r", "q", "c", "s")
PACKETS = ("k", "j", "br", "tq", "bq", "tc", "bc", "z", "f")
BASE = {
    "r": ("k", "j", "br"),
    "q": ("tq", "bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}
DISPLAYED = {
    "D_r": ("tq", "f"),
    "D_q": ("k", "j", "f"),
    "D_c": ("tc", "f"),
    "A_q": ("tq", "br"),
    "A_r": ("k", "bq"),
    "Z": ("z",),
    **{f"X_{agent}": goods for agent, goods in BASE.items()},
}
DESIRED = {
    "D_r": "r", "D_q": "q", "D_c": "r",
    "A_q": "c", "A_r": "c", "Z": "c",
}
CORE = (
    {"r": ("tc", "f"), "q": ("tq", "bc"), "c": ("k", "bq"),
     "s": ("z",), "_": ("j", "br")},
    {"r": ("tq", "f"), "q": ("k", "j", "br"), "c": ("z",),
     "s": ("bq", "tc"), "_": ("bc",)},
    {"r": ("tc", "f"), "q": ("tq", "bq"), "c": ("z",),
     "s": ("k", "j", "br"), "_": ("bc",)},
    {"r": ("tq", "f"), "q": ("k", "bq"), "c": ("tc", "bc"),
     "s": ("z",), "_": ("j", "br")},
    {"r": ("tc", "f"), "q": ("j", "bq"), "c": ("z",),
     "s": ("tq", "bc"), "_": ("k", "br")},
    {"r": ("k", "j", "br"), "q": ("tq", "bq"), "c": ("z",),
     "s": ("bc", "f"), "_": ("tc",)},
    {"r": ("k", "j", "br"), "q": ("tc", "f"), "c": ("tq", "bq"),
     "s": ("z",), "_": ("bc",)},
    {"r": ("k", "j", "br"), "q": ("bq", "tc"), "c": ("z",),
     "s": ("tq", "bc"), "_": ("f",)},
    {"r": ("k", "j", "f"), "q": ("tq", "bq"), "c": ("tc", "bc"),
     "s": ("z",), "_": ("br",)},
)


def add(entries):
    return z3.Sum(*entries) if entries else z3.RealVal(0)


def minimum(entries):
    entries = tuple(entries)
    result = entries[0]
    for entry in entries[1:]:
        result = z3.If(result <= entry, result, entry)
    return result


def total(value, observer, goods):
    return add(value[observer, packet] for packet in goods)


def tail(value, least, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        if not goods:
            return z3.RealVal(0)
        packet = goods[0]
        return value[observer, packet] - least[observer, packet]
    return total(value, observer, goods) - minimum(
        least[observer, packet] for packet in goods
    )


def lex_greater(left, right):
    return z3.Or(*(
        z3.And(
            *(left[index] == right[index] for index in range(position)),
            left[position] > right[position],
        )
        for position in range(len(left))
    ))


def build(include_core=True):
    value = {
        (agent, packet): z3.Real(f"packet_total_{agent}_{packet}")
        for agent in AGENTS for packet in PACKETS
    }
    least = {
        (agent, packet): z3.Real(f"packet_min_{agent}_{packet}")
        for agent in AGENTS for packet in PACKETS
    }
    solver = z3.Solver()
    multiple = {
        packet: z3.Bool(f"packet_multiple_{packet}")
        for packet in PACKETS
    }
    for agent in AGENTS:
        for packet in PACKETS:
            solver.add(value[agent, packet] > 0)
            solver.add(least[agent, packet] > 0)
            solver.add(least[agent, packet] <= value[agent, packet])
            solver.add(z3.If(
                multiple[packet],
                value[agent, packet] >= 2 * least[agent, packet],
                least[agent, packet] == value[agent, packet],
            ))
    solver.add(z3.Not(multiple["f"]), z3.Not(multiple["z"]))

    base = {agent: total(value, agent, BASE[agent]) for agent in AGENTS}
    for observer in AGENTS:
        for goods in BASE.values():
            solver.add(base[observer] >= tail(value, least, observer, goods))
        solver.add(base[observer] >= value[observer, "f"])
        for goods in DISPLAYED.values():
            solver.add(base[observer] >= tail(value, least, observer, goods))

    for name, source in DESIRED.items():
        solver.add(total(value, source, DISPLAYED[name]) > base[source])
    solver.add(base["r"] > total(value, "r", BASE["q"]))
    solver.add(base["q"] > total(value, "q", BASE["r"]))
    for observer in ("r", "q", "s"):
        solver.add(base[observer] > total(value, observer, BASE["c"]))

    solver.add(value["q", "f"] <= value["q", "bq"])
    solver.add(total(value, "r", BASE["q"]) < base["r"])
    solver.add(total(value, "q", BASE["r"]) <= base["q"])
    solver.add(value["q", "k"] <= value["q", "tq"])

    if include_core:
        base_vector = tuple(base[agent] for agent in AGENTS)
        for allocation in CORE:
            own = {
                agent: total(value, agent, allocation[agent])
                for agent in AGENTS
            }
            efx = []
            for observer in AGENTS:
                for target in AGENTS:
                    efx.append(
                        own[observer]
                        >= tail(value, least, observer, allocation[target])
                    )
                efx.append(
                    own[observer] >= total(value, observer, allocation["_"])
                )
            solver.add(z3.Not(z3.And(
                *efx,
                lex_greater(
                    tuple(own[agent] for agent in AGENTS), base_vector
                ),
            )))
    return solver


def run():
    base_status = str(build(False).check())
    solver = build(True)
    core_status = str(solver.check())
    atomic = build(True)
    atomic.add(*(
        z3.Not(z3.Bool(f"packet_multiple_{packet}"))
        for packet in PACKETS
    ))
    atomic_status = str(atomic.check())
    return {
        "schema": "residual-flower-packet-core-audit-v3",
        "status": (
            "PACKET_LIFT_REFUTED"
            if base_status == "sat" and atomic_status == "unsat"
            and core_status == "sat"
            else "OPEN"
        ),
        "solver": f"Z3 {z3.get_version_string()}",
        "base_status": base_status,
        "atomic_candidate_core_status": atomic_status,
        "candidate_core_status": core_status,
        "packet_count": len(PACKETS),
        "allocation_count": len(CORE),
        "packet_realizability": (
            "each shared packet is either a singleton for every observer or "
            "has total at least twice its minimum for every observer; every "
            "such nonsingleton packet is realizable with two goods"
        ),
        "claim_boundary": (
            "the nine candidates contradict the atomic residual cell but fail "
            "after cap-free packet lifting; the SAT result refutes only this "
            "finite aggregate family and not adaptive item-level completion"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
