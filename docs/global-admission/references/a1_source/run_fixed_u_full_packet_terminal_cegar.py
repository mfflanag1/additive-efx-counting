#!/usr/bin/env python3
"""Exact CEGAR for a full named-packet fixed-U terminal atomization."""

from __future__ import annotations

import argparse
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("r", "q", "d", "s")
RECIPIENTS = (*OWNERS, "charity")
GOODS = ("a0", "a1", "h", "j", "k", "q0", "l", "e", "m", "gq", "gr", "p")
BASE = {
    "r": ("a0", "m"),
    "q": ("q0", "a1"),
    "d": ("h", "k", "gq"),
    "s": ("e", "p"),
    "charity": ("j", "l", "gr"),
}
PACKETS = {
    "A": ("a0", "a1"),
    "H": ("h",),
    "Q": ("j", "k", "q0"),
    "K": ("j", "k"),
    "J": ("j",),
    "K_minus_J": ("k",),
    "E": ("l", "e"),
    "L": ("l",),
    "E_minus_L": ("e",),
    "W": ("m", "gq", "gr"),
    "M": ("m",),
    "Gq": ("gq",),
    "Gr": ("gr",),
    "P": ("p",),
}
SUPPORT_STATE = {
    "r": (*PACKETS["A"], *PACKETS["H"]),
    "q": PACKETS["Q"],
    "d": PACKETS["W"],
    "s": PACKETS["E"],
    "charity": PACKETS["P"],
}
SPLIT_STATE = {
    "r": (*PACKETS["A"], *PACKETS["Gr"]),
    "q": ("j", "q0", "gq"),
    "d": ("k", "h", "l"),
    "s": ("e", "m"),
    "charity": PACKETS["P"],
}
REASSEMBLY_STATE = {
    "r": SPLIT_STATE["r"],
    "q": SPLIT_STATE["q"],
    "d": ("k", "h", "m"),
    "s": PACKETS["E"],
    "charity": PACKETS["P"],
}


def total(value, observer, goods):
    goods = tuple(goods)
    return z3.Sum(*(value[good, observer] for good in goods)) if goods else z3.RealVal(0)


def tail(value, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return z3.RealVal(0)
    entries = [value[good, observer] for good in goods]
    minimum = entries[0]
    for entry in entries[1:]:
        minimum = z3.If(minimum <= entry, minimum, entry)
    return z3.Sum(*entries) - minimum


def build_master():
    value = {
        (good, observer): z3.Real(f"v_{good}_{observer}")
        for good in GOODS for observer in OWNERS
    }
    solver = z3.SolverFor("QF_LRA")
    for variable in value.values():
        solver.add(variable > 0, variable < 16)
    base = {owner: total(value, owner, BASE[owner]) for owner in OWNERS}
    for owner in OWNERS:
        solver.add(base[owner] == 1)
        solver.add(total(value, owner, BASE["charity"]) <= 1)
        for target in OWNERS:
            if target != owner:
                solver.add(tail(value, owner, BASE[target]) <= 1)

    A = lambda owner: total(value, owner, PACKETS["A"])
    Q = lambda owner: total(value, owner, PACKETS["Q"])
    E = lambda owner: total(value, owner, PACKETS["E"])
    K = lambda owner: total(value, owner, PACKETS["K"])
    W = lambda owner: total(value, owner, PACKETS["W"])
    solver.add(A("r") > 1, Q("q") > 1, E("s") > 1, Q("d") > 1)

    # Inclusion-minimal K for restoring d using H.
    solver.add(total(value, "d", ("j", "k", "h")) > 1)
    solver.add(total(value, "d", ("j", "h")) <= 1)
    solver.add(total(value, "d", ("k", "h")) <= 1)

    mu_q = Q("q") - 1
    solver.add(K("q") - W("q") > mu_q)
    theta_q = K("q") - mu_q - W("q")
    solver.add(total(value, "q", PACKETS["J"]) >= theta_q)

    nu_d = total(value, "d", ("j", "k", "h")) - 1
    solver.add(
        nu_d + total(value, "d", PACKETS["L"])
        - total(value, "d", PACKETS["J"]) > 0
    )
    B_q = mu_q + W("q") - total(value, "q", PACKETS["K_minus_J"])
    solver.add(B_q >= 0)
    mu_s = E("s") - 1
    kappa_s = total(value, "s", PACKETS["L"]) - mu_s
    solver.add(kappa_s > 0)

    # Full residual-selector failure, not merely failure of displayed M.
    for mask in range(1 << len(PACKETS["W"])):
        subset = tuple(
            good for index, good in enumerate(PACKETS["W"])
            if mask & (1 << index)
        )
        solver.add(z3.Implies(
            total(value, "q", subset) <= B_q,
            total(value, "s", subset) < kappa_s,
        ))

    # The displayed canonical q split pays q; root/d are strict. The fourth
    # owner fails before reassembly, while after reassembly s is strict and d
    # is genuinely sacrificed.
    split_u = {
        owner: total(value, owner, SPLIT_STATE[owner]) for owner in OWNERS
    }
    re_u = {
        owner: total(value, owner, REASSEMBLY_STATE[owner]) for owner in OWNERS
    }
    solver.add(split_u["r"] > 1, split_u["q"] >= 1, split_u["d"] > 1)
    solver.add(split_u["s"] < 1)
    solver.add(re_u["r"] > 1, re_u["q"] >= 1, re_u["s"] > 1)
    solver.add(re_u["d"] < 1)
    return solver, value


def lex_improves(utility):
    clauses = []
    for position, owner in enumerate(OWNERS):
        clauses.append(z3.And(
            *(utility[OWNERS[index]] == 1 for index in range(position)),
            utility[owner] > 1,
        ))
    return z3.Or(*clauses)


def allocation_formula(allocation, value, mode):
    utility = {
        owner: total(value, owner, allocation[owner]) for owner in OWNERS
    }
    if mode == "efx_lex":
        conditions = [bool(allocation["charity"]), lex_improves(utility)]
        for observer in OWNERS:
            for target in OWNERS:
                if target != observer:
                    conditions.append(
                        utility[observer] >= tail(value, observer, allocation[target])
                    )
            conditions.append(
                utility[observer] >= total(value, observer, allocation["charity"])
            )
        return z3.And(*conditions)
    if mode == "complete_efx":
        conditions = [not bool(allocation["charity"])]
        for observer in OWNERS:
            for target in OWNERS:
                if target != observer:
                    conditions.append(
                        utility[observer] >= tail(value, observer, allocation[target])
                    )
        return z3.And(*conditions)
    if mode == "pareto":
        return z3.And(
            *(utility[owner] >= 1 for owner in OWNERS),
            z3.Or(*(utility[owner] > 1 for owner in OWNERS)),
        )
    raise ValueError(mode)


def fractions(model, value):
    return {
        observer: {
            good: Fraction(str(model.eval(value[good, observer], model_completion=True)))
            for good in GOODS
        }
        for observer in OWNERS
    }


def oracle(values, mode):
    holder = {good: z3.Int(f"{mode}_holder_{good}") for good in GOODS}
    solver = z3.Optimize()
    for variable in holder.values():
        solver.add(variable >= 0, variable < len(RECIPIENTS))
    if mode == "efx_lex":
        solver.add(z3.Or(*(holder[good] == 4 for good in GOODS)))
    elif mode == "complete_efx":
        solver.add(*(holder[good] < 4 for good in GOODS))

    utility = {}
    for observer in OWNERS:
        for index, recipient in enumerate(RECIPIENTS):
            utility[observer, recipient] = z3.Sum(*(
                z3.If(
                    holder[good] == index,
                    z3.RealVal(str(values[observer][good])),
                    0,
                ) for good in GOODS
            ))
    own = {owner: utility[owner, owner] for owner in OWNERS}
    if mode == "efx_lex":
        solver.add(lex_improves(own))
        for observer in OWNERS:
            for target_index, target in enumerate(OWNERS):
                if target == observer:
                    continue
                for good in GOODS:
                    solver.add(z3.Implies(
                        holder[good] == target_index,
                        own[observer] >= utility[observer, target]
                        - z3.RealVal(str(values[observer][good])),
                    ))
            solver.add(own[observer] >= utility[observer, "charity"])
    elif mode == "complete_efx":
        for observer in OWNERS:
            for target_index, target in enumerate(OWNERS):
                if target == observer:
                    continue
                for good in GOODS:
                    solver.add(z3.Implies(
                        holder[good] == target_index,
                        own[observer] >= utility[observer, target]
                        - z3.RealVal(str(values[observer][good])),
                    ))
    else:
        solver.add(*(own[owner] >= 1 for owner in OWNERS))
        solver.add(z3.Or(*(own[owner] > 1 for owner in OWNERS)))

    base_holder = {
        good: RECIPIENTS.index(recipient)
        for recipient, goods in BASE.items() for good in goods
    }
    solver.minimize(z3.Sum(*(
        z3.If(holder[good] == base_holder[good], 0, 1) for good in GOODS
    )))
    if solver.check() != z3.sat:
        return None
    model = solver.model()
    allocation = {recipient: [] for recipient in RECIPIENTS}
    for good in GOODS:
        allocation[RECIPIENTS[model.eval(holder[good]).as_long()]].append(good)
    for goods in allocation.values():
        goods.sort()
    return allocation


def checkpoint(path, result):
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def run(output, maximum_iterations, timeout_seconds, resume):
    master, value = build_master()
    master.set(timeout=timeout_seconds * 1000)
    old = json.loads(output.read_text()) if resume and output.exists() else None
    iterations = list(old.get("iterations", [])) if old else []
    for record in iterations:
        if "blocking_allocation" in record:
            master.add(z3.Not(allocation_formula(
                record["blocking_allocation"], value, record["mode"]
            )))
    result = {
        "schema": "fixed-u-full-packet-terminal-cegar-v1",
        "status": "RUNNING",
        "solver": f"Z3 {z3.get_version_string()}",
        "goods": list(GOODS),
        "base": {key: list(goods) for key, goods in BASE.items()},
        "packets": {key: list(goods) for key, goods in PACKETS.items()},
        "support_state": {key: list(goods) for key, goods in SUPPORT_STATE.items()},
        "split_state": {key: list(goods) for key, goods in SPLIT_STATE.items()},
        "reassembly_state": {key: list(goods) for key, goods in REASSEMBLY_STATE.items()},
        "iterations": iterations,
        "claim_boundary": (
            "exact twelve-atom decision for the named A,H,Q,W,K,J,L,M packet "
            "premises, global EFX-lex maximality, and the stronger absence of "
            "any Pareto-improving allocation; response saturation, fixed-U reset "
            "reachability, and a genuine repeated transition cycle are not yet encoded"
        ),
    }
    checkpoint(output, result)
    for iteration in range(len(iterations), maximum_iterations):
        status = master.check()
        record = {"iteration": iteration, "master_status": str(status)}
        iterations.append(record)
        if status != z3.sat:
            result["status"] = str(status)
            if status == z3.unknown:
                result["reason_unknown"] = master.reason_unknown()
            checkpoint(output, result)
            return result
        values = fractions(master.model(), value)
        found = None
        for mode in ("complete_efx", "efx_lex", "pareto"):
            allocation = oracle(values, mode)
            if allocation is not None:
                found = mode, allocation
                break
        if found is None:
            result["status"] = "sat_packet_terminal_obstruction"
            result["countermodel_iteration"] = iteration
            result["values"] = {
                owner: {good: str(amount) for good, amount in row.items()}
                for owner, row in values.items()
            }
            checkpoint(output, result)
            return result
        mode, allocation = found
        record["mode"] = mode
        record["blocking_allocation"] = allocation
        master.add(z3.Not(allocation_formula(allocation, value, mode)))
        checkpoint(output, result)
        print(json.dumps({"iteration": iteration, "mode": mode, "allocation": allocation}), flush=True)
    result["status"] = "iteration_limit"
    checkpoint(output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = run(args.output, args.maximum_iterations, args.timeout_seconds, args.resume)
    print(json.dumps({"status": result["status"], "iterations": len(result["iterations"])}, indent=2))


if __name__ == "__main__":
    main()
