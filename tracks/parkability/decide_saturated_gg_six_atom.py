#!/usr/bin/env python3
"""Exact adversarial decision for the saturated GG six-atom normal form.

The model symbolically ranges over every base allocation, explicitly blocks
every lex-improving EFX-with-charity allocation, and places no restriction on
the induced packet graph or moved-good radius.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


N = 4
CHARITY = 4
AGENTS = ("r", "q", "c", "s")
ATOMS = ("P", "g", "A_r", "A_q", "A_c", "A_s")
M = len(ATOMS)
# Saturated Hamiltonian path r -> q -> c -> s -> charity.
CURRENT_HOLDER = (0, 0, 1, 2, 3, CHARITY)
PATH_CORE = (2, 3, 4, 5)
D = (0, 1)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(values, observer: int, goods) -> z3.ArithRef:
    goods = tuple(goods)
    return z3.Sum(*(values[observer][good] for good in goods)) if goods else z3.RealVal(0)


def tau(values, observer: int, goods) -> z3.ArithRef:
    goods = tuple(goods)
    if len(goods) <= 1:
        return z3.RealVal(0)
    remainders = [add(values, observer, (good for good in goods if good != removed)) for removed in goods]
    result = z3.Real(f"tau_aux_{observer}_{'_'.join(map(str, goods))}")
    # For additive positive values tau is total minus the least good.  Encode
    # max by a nested If so this helper adds no side constraints.
    result = remainders[0]
    for remainder in remainders[1:]:
        result = z3.If(result >= remainder, result, remainder)
    return result


def lex_gt(left, right) -> z3.BoolRef:
    return z3.Or(
        *(
            z3.And(
                *(left[prefix] == right[prefix] for prefix in range(index)),
                left[index] > right[index],
            )
            for index in range(N)
        )
    )


def bundles(holder) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(g for g, target in enumerate(holder) if target == i) for i in range(5))


def desired_safe(values, own, source: int, goods) -> z3.BoolRef:
    goods = tuple(goods)
    return z3.And(
        add(values, source, goods) > own[source],
        *(own[observer] >= tau(values, observer, goods) for observer in range(N)),
    )


def cycle_orders():
    for length in range(2, N + 1):
        for subset in itertools.combinations(range(N), length):
            anchor = min(subset)
            for tail in itertools.permutations(tuple(x for x in subset if x != anchor)):
                yield (anchor,) + tail


def build() -> tuple[z3.Solver, dict[str, z3.BoolRef], dict]:
    values = tuple(tuple(z3.Real(f"v_{i}_{g}") for g in range(M)) for i in range(N))
    base_holder = tuple(z3.Int(f"base_holder_{g}") for g in range(M))
    own = tuple(
        z3.Sum(*(z3.If(base_holder[g] == i, values[i][g], 0) for g in range(M)))
        for i in range(N)
    )
    charity_value = tuple(
        z3.Sum(*(z3.If(base_holder[g] == CHARITY, values[i][g], 0) for g in range(M)))
        for i in range(N)
    )
    current_bundles = bundles(CURRENT_HOLDER)
    current_utility = tuple(add(values, i, current_bundles[i]) for i in range(N))

    groups: dict[str, list[z3.BoolRef]] = {}
    groups["positive_normalized"] = [
        *(values[i][g] > 0 for i in range(N) for g in range(M)),
        *(z3.Sum(*values[i]) == 1 for i in range(N)),
    ]
    groups["base_allocation"] = [
        *(z3.And(base_holder[g] >= 0, base_holder[g] <= CHARITY) for g in range(M)),
        *(z3.Or(*(base_holder[g] == holder for g in range(M))) for holder in range(5)),
    ]
    groups["base_efx_charity"] = [*(own[i] >= charity_value[i] for i in range(N))]
    for observer in range(N):
        for target in range(N):
            if observer == target:
                continue
            for removed in range(M):
                groups["base_efx_charity"].append(
                    z3.Implies(
                        base_holder[removed] == target,
                        own[observer]
                        >= z3.Sum(
                            *(
                                z3.If(
                                    z3.And(base_holder[g] == target, g != removed),
                                    values[observer][g],
                                    0,
                                )
                                for g in range(M)
                            )
                        ),
                    )
                )

    groups["selected_path_cores"] = [
        desired_safe(values, own, source, (PATH_CORE[source],)) for source in range(N)
    ]
    groups["current_payment"] = [
        *(current_utility[i] >= own[i] for i in range(N)),
        current_utility[0] > own[0],
    ]
    groups["decorated_response"] = [
        add(values, 3, D) > current_utility[3],
        *(current_utility[i] >= tau(values, i, D) for i in range(N)),
        values[0][1] <= values[0][0],
        values[0][0] > values[0][PATH_CORE[0]],
    ]
    groups["observer_surplus"] = [
        *(tau(values, i, D) - own[i] <= current_utility[i] - own[i] for i in range(N)),
        z3.Or(*(tau(values, i, D) > own[i] for i in (1, 2))),
    ]

    # Complete ordinary PI-freeness on this atomization.  An edge i -> j
    # exists if any nonempty desired common-safe subset is wholly held by j.
    edge = {}
    for source in range(N):
        for target in range(N):
            if source == target:
                continue
            candidates = []
            for mask in range(1, 1 << M):
                goods = tuple(g for g in range(M) if mask & (1 << g))
                candidates.append(
                    z3.And(
                        *(base_holder[g] == target for g in goods),
                        desired_safe(values, own, source, goods),
                    )
                )
            edge[source, target] = z3.Or(*candidates)
    groups["complete_ordinary_pi_free"] = [
        z3.Not(
            z3.And(
                *(edge[cycle[index], cycle[(index + 1) % len(cycle)]] for index in range(len(cycle)))
            )
        )
        for cycle in cycle_orders()
    ]

    # Full owner/charity coverage of the signed X -> Y transfer graph.  Every
    # cut is crossed by some atom; no topology or distance bound is imposed.
    vertices = range(5)
    groups["signed_transfer_owner_coverage"] = []
    for mask in range(1, 1 << 4):  # canonical cuts contain vertex 0
        left = {0} | {vertex for vertex in range(1, 5) if mask & (1 << (vertex - 1))}
        if len(left) == 5:
            continue
        groups["signed_transfer_owner_coverage"].append(
            z3.Or(
                *(
                    z3.Or(
                        z3.And(z3.Or(*(base_holder[g] == x for x in left)), CURRENT_HOLDER[g] not in left),
                        z3.And(z3.And(*(base_holder[g] != x for x in left)), CURRENT_HOLDER[g] in left),
                    )
                    for g in range(M)
                )
            )
        )

    # Exact current-response saturation: D is the only current-safe subset
    # of a current target that strictly improves a source's current utility.
    current_edges = []
    for target, target_goods in enumerate(current_bundles):
        if not target_goods:
            continue
        for mask in range(1, 1 << len(target_goods)):
            goods = tuple(target_goods[k] for k in range(len(target_goods)) if mask & (1 << k))
            for source in range(N):
                relation = z3.And(
                    add(values, source, goods) > current_utility[source],
                    *(current_utility[i] >= tau(values, i, goods) for i in range(N)),
                )
                if target == 0 and source == 3 and goods == D:
                    current_edges.append(relation)
                else:
                    current_edges.append(z3.Not(relation))
    groups["response_saturation"] = current_edges

    # Component-wide base-margin separator for observers q,c.  For each
    # deletion J from D and every redistribution of {A_r,A_q}+J between
    # q,c and a return L to source s, debt removal plus protected floors
    # forces loss of the entire base response margin.
    separator = []
    pool = (PATH_CORE[0], PATH_CORE[1])
    mu_base = add(values, 3, D) - own[3]
    for mask in range(1, 1 << len(D)):
        deleted = tuple(D[k] for k in range(len(D)) if mask & (1 << k))
        retained = tuple(g for g in D if g not in deleted)
        universe = pool + deleted
        for assignment in itertools.product((1, 2, 3), repeat=len(universe)):
            if any(
                good in deleted and holder == 3
                for good, holder in zip(universe, assignment, strict=True)
            ):
                # A return packet is physical component stock, not the same
                # deletion packet passed through and immediately returned.
                continue
            zq = tuple(g for g, holder in zip(universe, assignment, strict=True) if holder == 1)
            zc = tuple(g for g, holder in zip(universe, assignment, strict=True) if holder == 2)
            returned = tuple(g for g, holder in zip(universe, assignment, strict=True) if holder == 3)
            antecedent = z3.And(
                *(tau(values, observer, retained) <= own[observer] for observer in (1, 2)),
                add(values, 1, zq) >= own[1],
                add(values, 2, zc) >= own[2],
                add(values, 1, zq) >= tau(values, 1, retained + returned),
                add(values, 2, zc) >= tau(values, 2, retained + returned),
            )
            separator.append(
                z3.Implies(
                    antecedent,
                    add(values, 3, deleted) - add(values, 3, returned) >= mu_base,
                )
            )
    groups["source_margin_separator"] = separator

    # Failure of the direct deletion-return candidate before charity repair.
    deletion_return = ((0,), (3,), (4,), (5,), (1, 2))
    dr_util = tuple(add(values, i, deletion_return[i]) for i in range(N))
    dr_efx = [dr_util[i] >= add(values, i, deletion_return[4]) for i in range(N)]
    for i in range(N):
        for j in range(N):
            if i != j:
                dr_efx.append(dr_util[i] >= tau(values, i, deletion_return[j]))
    groups["failed_direct_charity_safety"] = [z3.Not(z3.And(*dr_efx))]

    # Exhaustive global-lex premise.  Each of the 5^6 final atom assignments
    # induces its unrestricted net packet graph relative to symbolic X.
    global_blockers = []
    allocation_count = 0
    noncomplete_count = 0
    for rival_holder in itertools.product(range(5), repeat=M):
        allocation_count += 1
        rival = bundles(rival_holder)
        if not rival[CHARITY]:
            continue
        noncomplete_count += 1
        rival_utility = tuple(add(values, i, rival[i]) for i in range(N))
        efx = [rival_utility[i] >= add(values, i, rival[CHARITY]) for i in range(N)]
        for i in range(N):
            for j in range(N):
                if i != j:
                    efx.append(rival_utility[i] >= tau(values, i, rival[j]))
        global_blockers.append(z3.Or(z3.Not(z3.And(*efx)), z3.Not(lex_gt(rival_utility, own))))
    groups["global_lex_all_allocations"] = global_blockers

    solver = z3.Solver()
    solver.set(unsat_core=True)
    labels = {}
    for name, formulas in groups.items():
        label = z3.Bool(f"premise__{name}")
        labels[name] = label
        solver.add(z3.Implies(label, z3.And(*formulas)))
    metadata = {
        "values": values,
        "base_holder": base_holder,
        "own": own,
        "current_utility": current_utility,
        "groups": groups,
        "allocation_count": allocation_count,
        "noncomplete_allocation_count": noncomplete_count,
    }
    return solver, labels, metadata


def run(root: Path) -> dict:
    solver, labels, metadata = build()
    checked = solver.check(*labels.values())
    if checked == z3.sat:
        status = "SAT_SIX_ATOM_COUNTERMODEL"
        core = []
    elif checked == z3.unsat:
        status = "UNSAT_SIX_ATOM_SEPARATOR"
        # Use the shortest analytically transparent core and verify deletion
        # minimality directly.  Other incomparable minimal cores can exist;
        # relying on Z3's noncanonical initial core made replay output vary.
        core = [
            "positive_normalized",
            "current_payment",
            "response_saturation",
            "global_lex_all_allocations",
        ]
        assert solver.check(*(labels[name] for name in core)) == z3.unsat
        for removed in core:
            assert solver.check(
                *(labels[name] for name in core if name != removed)
            ) == z3.sat
    else:
        raise RuntimeError(solver.reason_unknown())

    script = Path(__file__).resolve()
    return {
        "schema": "saturated-gg-six-atom-decision-v1",
        "status": status,
        "atomization": {
            "atoms": list(ATOMS),
            "current_holder": list(CURRENT_HOLDER),
            "hamiltonian_path": ["r", "q", "c", "s", "charity"],
            "path_cores_are_single_atoms": True,
        },
        "premise_groups": {name: len(formulas) for name, formulas in metadata["groups"].items()},
        "allocation_count": metadata["allocation_count"],
        "noncomplete_allocation_count": metadata["noncomplete_allocation_count"],
        "packet_graph_scope": "every induced net atom-transfer graph; no topology or moved-radius restriction",
        "deletion_minimal_group_core": core,
        "candidate_universal_inequality": (
            "In the six-atom Hamiltonian normal form, exact current-response "
            "saturation implies u_i(Y_i) >= max{v_i(P),v_i(g),v_i(A_s)} "
            "for every owner i.  Every other owner target is a singleton, so Y "
            "is EFX with charity; weak payment and one strict first-row payment "
            "then contradict global lex maximality."
        ),
        "claim_boundary": (
            "exact UNSAT theorem for the declared six-atom singleton-core normal "
            "form only; complete generalized release-compatible PI was not separately "
            "encoded because the deletion-minimal UNSAT relaxation omits every PI "
            "constraint, so adding that stronger premise cannot restore SAT; this is "
            "not cap-free and does not exclude split or multi-good path cores"
        ),
        "provenance": {
            "python": __import__("platform").python_version(),
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
