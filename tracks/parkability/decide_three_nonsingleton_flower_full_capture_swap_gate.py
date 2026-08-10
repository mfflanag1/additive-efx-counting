#!/usr/bin/env python3
"""Exact full-capture cell with every bottom-crossing swap blocked."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, BASE, candidate_covers
except ImportError:
    from decide_three_nonsingleton_flower_one_unpaid_cover import AGENTS, BASE, candidate_covers


COMPONENT_BUNDLES = {
    "A_q": ("aq_tq", "aq_br"),
    "A_r": ("ar_tr", "ar_bq"),
    "D_r": ("aq_tq", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "X_q": ("aq_tq", "ar_bq"),
    "X_c": ("tc", "bc"),
    "Z": ("z",),
}
COMPONENTS = tuple(dict.fromkeys(
    component for components in COMPONENT_BUNDLES.values() for component in components
))
OLD_BUNDLES = {
    "r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "q": ("aq_tq", "ar_bq"),
    "c": ("tc", "bc"),
    "s": ("z",),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum(values):
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def true_tail(values):
    if len(values) <= 1:
        return z3.RealVal(0)
    return z3.Sum(*values) - minimum(values)


def run(require_source_safe: bool = False, block_pair_exchanges: bool = False) -> dict:
    atom_names = {
        component: (
            (component,) if component in ("f", "z")
            else tuple(f"{component}_{index}" for index in range(2))
        )
        for component in COMPONENTS
    }
    atoms = tuple(atom for names in atom_names.values() for atom in names)
    bundle_atoms = {
        bundle: tuple(atom for component in components for atom in atom_names[component])
        for bundle, components in COMPONENT_BUNDLES.items()
    }
    old_atoms = {
        agent: tuple(atom for component in components for atom in atom_names[component])
        for agent, components in OLD_BUNDLES.items()
    }
    value = {
        (atom, agent): z3.Real(f"gate_{atom}_{agent}")
        for atom in atoms for agent in AGENTS
    }
    total = {
        (bundle, agent): z3.Sum(*(value[atom, agent] for atom in names))
        for bundle, names in bundle_atoms.items() for agent in AGENTS
    }
    tail = {
        (bundle, agent): true_tail([value[atom, agent] for atom in names])
        for bundle, names in bundle_atoms.items() for agent in AGENTS
    }
    base = {agent: total[BASE[agent], agent] for agent in AGENTS}
    solver = z3.SolverFor("QF_LRA")
    for atom in atoms:
        for agent in AGENTS:
            solver.add(value[atom, agent] > 0)
    for agent in AGENTS:
        for bundle in bundle_atoms:
            solver.add(tail[bundle, agent] <= base[agent])
        solver.add(value["f", agent] <= base[agent])
        solver.add(total["X_c", agent] <= base[agent])
    for bundle, source in {
        "D_r": "r", "D_q": "q", "D_c": "r",
        "Z": "c", "A_q": "c", "A_r": "c",
    }.items():
        solver.add(total[bundle, source] > base[source])

    def efx_failures(allocation):
        failures = []
        for observer in AGENTS:
            own_total = z3.Sum(*(value[atom, observer] for atom in allocation[observer]))
            for target in AGENTS:
                failures.append({
                    "observer": observer,
                    "target": target,
                    "formula": own_total < true_tail([
                        value[atom, observer] for atom in allocation[target]
                    ]),
                })
        return failures

    # A globally lex-maximal state cannot admit an EFX insertion of f, an
    # owner-improving f-for-item swap, or a one-good transfer from a later
    # owner to an earlier owner.  These radius-one moves were already blocked
    # in the atomic flower audit and are needed here to prevent spurious wall
    # models from escaping before the bottom-crossing gate is reached.
    for owner in AGENTS:
        inserted = dict(old_atoms)
        inserted[owner] = old_atoms[owner] + ("f",)
        solver.add(z3.Or(*(failure["formula"] for failure in efx_failures(inserted))))
        if owner == "s":
            continue
        for released in old_atoms[owner]:
            swapped = dict(old_atoms)
            swapped[owner] = tuple(
                atom for atom in old_atoms[owner] if atom != released
            ) + ("f",)
            solver.add(z3.Or(
                value["f", owner] <= value[released, owner],
                *(failure["formula"] for failure in efx_failures(swapped)),
            ))

    priority = tuple(AGENTS)
    for receiver in AGENTS:
        for source in AGENTS:
            if priority.index(receiver) >= priority.index(source):
                continue
            for transferred in old_atoms[source]:
                moved = dict(old_atoms)
                moved[receiver] = old_atoms[receiver] + (transferred,)
                moved[source] = tuple(
                    atom for atom in old_atoms[source] if atom != transferred
                )
                solver.add(z3.Or(*(
                    failure["formula"] for failure in efx_failures(moved)
                )))

    if block_pair_exchanges:
        for receiver in AGENTS:
            for donor in AGENTS:
                if priority.index(receiver) >= priority.index(donor):
                    continue
                for incoming in old_atoms[donor]:
                    for released in old_atoms[receiver]:
                        improves = value[incoming, receiver] > value[released, receiver]
                        for return_released in (False, True):
                            exchanged = dict(old_atoms)
                            exchanged[receiver] = tuple(
                                atom for atom in old_atoms[receiver] if atom != released
                            ) + (incoming,)
                            exchanged[donor] = tuple(
                                atom for atom in old_atoms[donor] if atom != incoming
                            ) + ((released,) if return_released else ())
                            solver.add(z3.Or(
                                z3.Not(improves),
                                *(failure["formula"] for failure in efx_failures(exchanged)),
                            ))

    covers = candidate_covers("r", "c", "c", "c", tuple(AGENTS))
    one_unpaid = [cover for cover in covers if cover["unpaid_agent"] is not None]
    for cover in one_unpaid:
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS if target != unpaid
        )))

    pairs = []
    for h in atom_names["aq_br"]:
        for b in atom_names["ar_bq"]:
            new_atoms = dict(old_atoms)
            new_atoms["r"] = tuple(atom for atom in old_atoms["r"] if atom != h) + (b,)
            new_atoms["q"] = tuple(atom for atom in old_atoms["q"] if atom != b) + (h,)
            failures = efx_failures(new_atoms)
            improves_r = value[b, "r"] > value[h, "r"]
            source_safe = value[h, "q"] >= value[b, "q"]
            solver.add(z3.Or(z3.Not(improves_r), *(failure["formula"] for failure in failures)))
            pairs.append({
                "h": h,
                "b": b,
                "improves_r": improves_r,
                "source_safe": source_safe,
                "failures": failures,
            })
    solver.add(z3.Or(*(pair["improves_r"] for pair in pairs)))
    if require_source_safe:
        solver.add(z3.Or(*(
            z3.And(pair["improves_r"], pair["source_safe"])
            for pair in pairs
        )))

    checked = solver.check()
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    result = {
        "schema": "three-nonsingleton-flower-full-capture-swap-gate-v1",
        "status": str(checked),
        "source_order_key": {
            "arm_source": "r",
            "singleton_envier": "c",
            "left_bottom_source": "c",
            "right_bottom_source": "c",
            "priority_order": list(AGENTS),
        },
        "require_source_safe_improving_pair": require_source_safe,
        "block_priority_directed_pair_exchanges": block_pair_exchanges,
        "pair_count": len(pairs),
        "claim_boundary": (
            "exact two-good-per-component full-X_q capture cell with every priority-directed bottom swap "
            "blocked after excluding EFX f-insertions, owner-improving f-for-item swaps, and "
            "priority-directed one-good transfers; SAT is proof-mining evidence, not a globally maximal "
            "state or an EFX counterexample"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "z3_version": z3.get_version_string(),
        },
    }
    if checked == z3.sat:
        model = solver.model()
        result["values"] = {
            agent: {atom: str(model.eval(value[atom, agent], model_completion=True)) for atom in atoms}
            for agent in AGENTS
        }
        result["pair_diagnostics"] = []
        for pair in pairs:
            improves = z3.is_true(model.eval(pair["improves_r"], model_completion=True))
            safe = z3.is_true(model.eval(pair["source_safe"], model_completion=True))
            blockers = [
                {"observer": failure["observer"], "target": failure["target"]}
                for failure in pair["failures"]
                if z3.is_true(model.eval(failure["formula"], model_completion=True))
            ]
            result["pair_diagnostics"].append({
                "h": pair["h"], "b": pair["b"],
                "improves_r": improves,
                "source_safe": safe,
                "blockers": blockers,
            })
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-source-safe", action="store_true")
    parser.add_argument("--block-pair-exchanges", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.require_source_safe, args.block_pair_exchanges)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "pairs": result["pair_count"]}, indent=2))


if __name__ == "__main__":
    main()
