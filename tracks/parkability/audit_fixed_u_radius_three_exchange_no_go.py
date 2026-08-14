#!/usr/bin/env python3
"""Independent exact audit of the fixed-U radius-three exchange no-go."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


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
    "W": ("m", "gq", "gr"),
    "M": ("m",),
    "Gq": ("gq",),
    "Gr": ("gr",),
    "P": ("p",),
}
SPLIT = {
    "r": ("a0", "a1", "gr"),
    "q": ("j", "q0", "gq"),
    "d": ("k", "h", "l"),
    "s": ("e", "m"),
    "charity": ("p",),
}
REASSEMBLY = {
    "r": SPLIT["r"],
    "q": SPLIT["q"],
    "d": ("k", "h", "m"),
    "s": ("l", "e"),
    "charity": ("p",),
}


def total(values, observer, goods):
    return sum((values[observer][good] for good in goods), Fraction(0))


def tail(values, observer, goods):
    goods = tuple(goods)
    if len(goods) <= 1:
        return Fraction(0)
    return total(values, observer, goods) - min(values[observer][good] for good in goods)


def holder_map(allocation):
    return {good: recipient for recipient, goods in allocation.items() for good in goods}


def lex_improves(own):
    for position, owner in enumerate(OWNERS):
        if all(own[OWNERS[index]] == 1 for index in range(position)):
            if own[owner] > 1:
                return True
        if own[owner] != 1:
            return False
    return False


def efx_lex(values, allocation):
    if not allocation["charity"]:
        return False
    own = {owner: total(values, owner, allocation[owner]) for owner in OWNERS}
    if not lex_improves(own):
        return False
    for observer in OWNERS:
        if own[observer] < total(values, observer, allocation["charity"]):
            return False
        for target in OWNERS:
            if target != observer and own[observer] < tail(values, observer, allocation[target]):
                return False
    return True


def check_premises(values):
    checks = {}
    for owner in OWNERS:
        checks[f"positive_{owner}"] = all(0 < values[owner][good] < 16 for good in GOODS)
        checks[f"base_normalized_{owner}"] = total(values, owner, BASE[owner]) == 1
        checks[f"base_charity_safe_{owner}"] = total(values, owner, BASE["charity"]) <= 1
        for target in OWNERS:
            if target != owner:
                checks[f"base_efx_{owner}_{target}"] = tail(values, owner, BASE[target]) <= 1

    checks["root_desires_A"] = total(values, "r", PACKETS["A"]) > 1
    checks["q_desires_Q"] = total(values, "q", PACKETS["Q"]) > 1
    checks["s_desires_E"] = total(values, "s", PACKETS["E"]) > 1
    checks["d_desires_Q"] = total(values, "d", PACKETS["Q"]) > 1
    checks["K_restores_d"] = total(values, "d", ("j", "k", "h")) > 1
    checks["K_minimal_drop_j"] = total(values, "d", ("j", "h")) <= 1
    checks["K_minimal_drop_k"] = total(values, "d", ("k", "h")) <= 1

    mu_q = total(values, "q", PACKETS["Q"]) - 1
    checks["strict_q_budget_separator"] = (
        total(values, "q", PACKETS["K"]) - total(values, "q", PACKETS["W"]) > mu_q
    )
    theta_q = total(values, "q", PACKETS["K"]) - mu_q - total(values, "q", PACKETS["W"])
    checks["J_meets_q_threshold"] = total(values, "q", PACKETS["J"]) >= theta_q
    nu_d = total(values, "d", ("j", "k", "h")) - 1
    checks["L_substitutes_for_J"] = (
        nu_d + total(values, "d", PACKETS["L"])
        - total(values, "d", PACKETS["J"]) > 0
    )
    B_q = mu_q + total(values, "q", PACKETS["W"]) - total(values, "q", PACKETS["K_minus_J"])
    checks["nonnegative_q_residual_budget"] = B_q >= 0
    mu_s = total(values, "s", PACKETS["E"]) - 1
    kappa_s = total(values, "s", PACKETS["L"]) - mu_s
    checks["positive_s_compensation_threshold"] = kappa_s > 0
    for size in range(len(PACKETS["W"]) + 1):
        for subset in itertools.combinations(PACKETS["W"], size):
            if total(values, "q", subset) <= B_q:
                checks[f"residual_failure_{'_'.join(subset) or 'empty'}"] = (
                    total(values, "s", subset) < kappa_s
                )

    split_u = {owner: total(values, owner, SPLIT[owner]) for owner in OWNERS}
    reassembly_u = {owner: total(values, owner, REASSEMBLY[owner]) for owner in OWNERS}
    checks.update({
        "split_r_strict": split_u["r"] > 1,
        "split_q_paid": split_u["q"] >= 1,
        "split_d_strict": split_u["d"] > 1,
        "split_s_fails": split_u["s"] < 1,
        "reassembly_r_strict": reassembly_u["r"] > 1,
        "reassembly_q_paid": reassembly_u["q"] >= 1,
        "reassembly_s_strict": reassembly_u["s"] > 1,
        "reassembly_d_fails": reassembly_u["d"] < 1,
    })
    return checks


def enumerate_escapes(values, maximum_radius):
    base_holder = holder_map(BASE)
    counts = {}
    witnesses = {}
    examined = {}
    escape_keys = {}
    for radius in range(maximum_radius + 1):
        count = 0
        checked = 0
        first = None
        keys = set()
        for moved in itertools.combinations(GOODS, radius):
            choices = [tuple(recipient for recipient in RECIPIENTS if recipient != base_holder[good])
                       for good in moved]
            for destinations in itertools.product(*choices):
                checked += 1
                holder = dict(base_holder)
                holder.update(zip(moved, destinations))
                allocation = {recipient: [] for recipient in RECIPIENTS}
                for good in GOODS:
                    allocation[holder[good]].append(good)
                for goods in allocation.values():
                    goods.sort()
                if efx_lex(values, allocation):
                    count += 1
                    keys.add(json.dumps(allocation, sort_keys=True))
                    if first is None:
                        first = allocation
        counts[str(radius)] = count
        examined[str(radius)] = checked
        escape_keys[str(radius)] = keys
        if first is not None:
            witnesses[str(radius)] = first
    return counts, examined, witnesses, escape_keys


def audit(source: Path, iteration: int):
    payload = json.loads(source.read_text())
    record = next(record for record in payload["rounds"] if record["iteration"] == iteration)
    values = {
        owner: {good: Fraction(amount) for good, amount in row.items()}
        for owner, row in record["values"].items()
    }
    checks = check_premises(values)
    counts, examined, witnesses, escape_keys = enumerate_escapes(values, 4)
    recorded = record["blocking_allocations"]
    recorded_set = {json.dumps(allocation, sort_keys=True) for allocation in recorded}
    exact_radius_four = escape_keys["4"] == recorded_set
    result = {
        "schema": "fixed-u-radius-three-exchange-no-go-audit-v1",
        "source": f"results/{source.name}",
        "source_iteration_sha256": hashlib.sha256(
            json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "source_iteration": iteration,
        "premise_checks": checks,
        "all_premises_hold": all(checks.values()),
        "allocations_examined_by_exact_radius": examined,
        "efx_lex_escapes_by_exact_radius": counts,
        "first_witness_by_radius": witnesses,
        "recorded_radius_four_menu_size": len(recorded_set),
        "recorded_menu_matches_exact_radius_four_set": exact_radius_four,
        "radius_three_no_go_verified": (
            all(counts[str(radius)] == 0 for radius in range(4))
            and counts["4"] > 0
            and exact_radius_four
            and all(checks.values())
        ),
        "claim_boundary": (
            "exact positive-rational no-go for EFX lex improvements moving at most "
            "three goods in one twelve-atom named-packet cell; it refutes a universal "
            "radius-three selector but does not encode response saturation or refute "
            "a cap-free connected packet exchange or fixed-U termination"
        ),
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=10)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.source, args.iteration)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "all_premises_hold": result["all_premises_hold"],
        "escape_counts": result["efx_lex_escapes_by_exact_radius"],
        "radius_three_no_go_verified": result["radius_three_no_go_verified"],
    }, indent=2))


if __name__ == "__main__":
    main()
