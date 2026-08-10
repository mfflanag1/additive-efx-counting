#!/usr/bin/env python3
"""Exact two-good-per-component witness for an atomic-UNSAT flower cell."""

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
    "D_r": ("aq_tq", "tq_rest", "f"),
    "D_q": ("ar_tr", "tr_rest", "f"),
    "D_c": ("tc", "f"),
    "X_r": ("ar_tr", "tr_rest", "aq_br", "br_rest"),
    "X_q": ("aq_tq", "tq_rest", "ar_bq", "bq_rest"),
    "X_c": ("tc", "bc"),
    "Z": ("z",),
}
COMPONENTS = tuple(dict.fromkeys(
    component for components in COMPONENT_BUNDLES.values() for component in components
))
KEY = {
    "arm_source": "r",
    "singleton_envier": "c",
    "left_bottom_source": "c",
    "right_bottom_source": "c",
    "priority_order": ("r", "q", "c", "s"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def minimum(values):
    result = values[0]
    for value in values[1:]:
        result = z3.If(result <= value, result, value)
    return result


def run(
    copies: int = 2,
    aq_support: str = "both",
    ar_support: str = "both",
    empty_rest: tuple[str, ...] = (),
) -> dict:
    excluded = set()
    if aq_support == "tq":
        excluded.add("aq_br")
    elif aq_support == "br":
        excluded.add("aq_tq")
    if ar_support == "tr":
        excluded.add("ar_bq")
    elif ar_support == "bq":
        excluded.add("ar_tr")
    excluded.update(empty_rest)
    atom_names = {
        component: (
            ()
            if component in excluded
            else
            (component,)
            if component in ("f", "z")
            else tuple(f"{component}_{index}" for index in range(copies))
        )
        for component in COMPONENTS
    }
    atoms = tuple(atom for names in atom_names.values() for atom in names)
    bundle_atoms = {
        bundle: tuple(
            atom
            for component in components
            for atom in atom_names[component]
        )
        for bundle, components in COMPONENT_BUNDLES.items()
    }
    value = {
        (atom, agent): z3.Real(f"split_{atom}_{agent}")
        for atom in atoms
        for agent in AGENTS
    }
    total = {
        (bundle, agent): z3.Sum(*(value[atom, agent] for atom in bundle_atoms[bundle]))
        for bundle in bundle_atoms
        for agent in AGENTS
    }
    tail = {
        (bundle, agent): (
            z3.RealVal(0)
            if len(bundle_atoms[bundle]) == 1
            else total[bundle, agent] - minimum([value[atom, agent] for atom in bundle_atoms[bundle]])
        )
        for bundle in bundle_atoms
        for agent in AGENTS
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

    desired = {
        "D_r": "r",
        "D_q": "q",
        "D_c": KEY["arm_source"],
        "Z": KEY["singleton_envier"],
        "A_q": KEY["left_bottom_source"],
        "A_r": KEY["right_bottom_source"],
    }
    for bundle, source in desired.items():
        solver.add(total[bundle, source] > base[source])

    covers = candidate_covers(
        KEY["arm_source"], KEY["singleton_envier"],
        KEY["left_bottom_source"], KEY["right_bottom_source"],
        KEY["priority_order"],
    )
    one_unpaid = [cover for cover in covers if cover["unpaid_agent"] is not None]
    assert one_unpaid and not any(cover["unpaid_agent"] is None for cover in covers)
    for cover in one_unpaid:
        unpaid = cover["unpaid_agent"]
        payment = cover["assignment"][unpaid]
        solver.add(z3.Or(*(
            total[payment, unpaid] < tail[cover["assignment"][target], unpaid]
            for target in AGENTS
            if target != unpaid
        )))

    checked = solver.check()
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    result = {
        "schema": "three-nonsingleton-flower-packet-split-witness-v1",
        "status": str(checked),
        "copies_per_nonsingleton_component": copies,
        "aq_support": aq_support,
        "ar_support": ar_support,
        "empty_rest": sorted(empty_rest),
        "source_order_key": {**KEY, "priority_order": list(KEY["priority_order"])},
        "cover_count": len(one_unpaid),
        "claim_boundary": (
            "exact positive additive realization with true minimum-good tails for one source/order cell; "
            "SAT shows only that simultaneous failure of the current common-safe cover family returns "
            "after packet splitting, not that the state is globally maximal or lacks EFX"
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
            agent: {
                atom: str(model.eval(value[atom, agent], model_completion=True))
                for atom in atoms
            }
            for agent in AGENTS
        }
        result["bundle_totals"] = {
            agent: {
                bundle: str(model.eval(total[bundle, agent], model_completion=True))
                for bundle in bundle_atoms
            }
            for agent in AGENTS
        }
        result["bundle_tails"] = {
            agent: {
                bundle: str(model.eval(tail[bundle, agent], model_completion=True))
                for bundle in bundle_atoms
            }
            for agent in AGENTS
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--copies", type=int, default=2)
    parser.add_argument("--aq-support", choices=("tq", "br", "both"), default="both")
    parser.add_argument("--ar-support", choices=("tr", "bq", "both"), default="both")
    parser.add_argument("--empty-rest", default="")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    empty_rest = tuple(part for part in args.empty_rest.split(",") if part)
    result = run(args.copies, args.aq_support, args.ar_support, empty_rest)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "covers": result["cover_count"]}, indent=2))


if __name__ == "__main__":
    main()
