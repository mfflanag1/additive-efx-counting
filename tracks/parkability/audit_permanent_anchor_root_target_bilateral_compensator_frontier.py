#!/usr/bin/env python3
"""Audit the permanent-anchor root/source bilateral compensator frontier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import z3


OWNERS = ("q", "d", "s")
H_Q_STATES = ("empty", "proper", "all")


def topology_cases():
    rows = []
    for source in OWNERS:
        for h_r in (False, True):
            for h_q_state in H_Q_STATES:
                if not h_r and h_q_state == "empty":
                    continue
                for d_nonempty in (False, True):
                    supplier = {"yr_res": "r", "i_res": source,
                                "p": "charity"}
                    before = {"r": {"yr_res"}, source: {"i_res"},
                              "charity": {"p"}}
                    h_items = set()
                    if h_r:
                        before["r"].add("hr")
                        supplier["hr"] = "r"
                        h_items.add("hr")
                    if h_q_state in ("proper", "all"):
                        before["r"].add("hq")
                        supplier["hq"] = "q"
                        h_items.add("hq")
                    if h_q_state in ("empty", "proper"):
                        before["r"].add("a_res")
                        supplier["a_res"] = "q"
                    if d_nonempty:
                        before[source].add("d")
                        supplier["d"] = source

                    after = {owner: set(goods) for owner, goods in before.items()}
                    after["r"].difference_update(h_items)
                    after[source].update(h_items)
                    after["r"].add("p")
                    after["charity"].remove("p")
                    if d_nonempty:
                        after[source].remove("d")
                        after["r"].add("d")

                    assert set().union(*before.values()) == set().union(*after.values())
                    edges = {
                        (supplier[item], owner)
                        for owner, goods in after.items()
                        for item in goods
                        if supplier[item] != owner
                    }
                    overflow_formula = (
                        source != "q" and h_r and h_q_state == "proper"
                        and d_nonempty
                    )
                    assert (len(edges) == 5) == overflow_formula
                    rows.append({
                        "source": source,
                        "h_r_nonempty": h_r,
                        "h_q_state": h_q_state,
                        "d_nonempty": d_nonempty,
                        "edges": [list(edge) for edge in sorted(edges)],
                        "edge_count": len(edges),
                        "four_edge_feasible": not overflow_formula,
                    })
    assert len(rows) == 30
    assert sum(row["four_edge_feasible"] for row in rows) == 28
    assert sum(not row["four_edge_feasible"] for row in rows) == 2
    assert max(row["edge_count"] for row in rows if row["four_edge_feasible"]) == 4
    return rows


def algebra_checks():
    br, xr, hp, dr, pr = z3.Reals("br xr hp dr pr")
    delta = br - xr

    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, pr > 0, br - hp + dr + pr > xr,
               hp - dr >= delta + pr)
    root_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(br > xr, pr > 0, hp - dr < delta + pr,
               br - hp + dr + pr <= xr)
    root_reverse = solver.check() == z3.unsat

    old_i, hi, di, new_i = z3.Reals("old_i hi di new_i")
    solver = z3.SolverFor("QF_LRA")
    solver.add(new_i == old_i - di + hi, hi > di, new_i <= old_i)
    source_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(new_i == old_i - di + hi, new_i > old_i, hi <= di)
    source_reverse = solver.check() == z3.unsat

    best_r, other_r = z3.Reals("best_r other_r")
    solver = z3.SolverFor("QF_LRA")
    solver.add(other_r <= best_r,
               best_r <= hp - delta - pr,
               other_r > hp - delta - pr)
    maximizer_propagation = solver.check() == z3.unsat

    solver = z3.SolverFor("QF_LRA")
    solver.add(0 <= hp - delta - pr, hp < delta + pr)
    empty_implies_packet_wall = solver.check() == z3.unsat

    complement = z3.Real("complement")
    solver = z3.SolverFor("QF_LRA")
    solver.add(complement == br - hp,
               hp >= delta + pr, complement + pr > xr)
    complement_safety_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(complement == br - hp,
               complement + pr <= xr, hp < delta + pr)
    complement_safety_reverse = solver.check() == z3.unsat

    # A desired subcore of B_r makes the entire B_r strictly preferred by i.
    e_i, br_i, bi_i = z3.Reals("e_i br_i bi_i")
    solver = z3.SolverFor("QF_LRA")
    solver.add(br_i >= e_i, e_i > bi_i, br_i <= bi_i)
    full_swap_source_strict = solver.check() == z3.unsat

    # Failure of the full swap is exactly root direct safety of B_i+p.
    bi_r = z3.Real("bi_r")
    solver = z3.SolverFor("QF_LRA")
    solver.add(delta == br - xr,
               br - bi_r >= delta + pr,
               bi_r + pr > xr)
    direct_safety_forward = solver.check() == z3.unsat
    solver = z3.SolverFor("QF_LRA")
    solver.add(delta == br - xr,
               bi_r + pr <= xr,
               br - bi_r < delta + pr)
    direct_safety_reverse = solver.check() == z3.unsat

    assert all((root_forward, root_reverse, source_forward, source_reverse,
                maximizer_propagation, empty_implies_packet_wall,
                complement_safety_forward, complement_safety_reverse,
                full_swap_source_strict, direct_safety_forward,
                direct_safety_reverse))
    return {
        "root_payment_equivalence": root_forward and root_reverse,
        "source_strict_equivalence": source_forward and source_reverse,
        "maximizer_propagation": maximizer_propagation,
        "empty_compensator_packet_wall": empty_implies_packet_wall,
        "empty_compensator_complement_safety_equivalence": (
            complement_safety_forward and complement_safety_reverse
        ),
        "full_swap_source_strict": full_swap_source_strict,
        "full_swap_direct_safety_equivalence": (
            direct_safety_forward and direct_safety_reverse
        ),
    }


def local_separator_witness():
    root = {"a": Fraction(6), "b": Fraction(6),
            "c": Fraction(1), "p": Fraction(1)}
    source = {"a": Fraction(2), "b": Fraction(2),
              "c": Fraction(3), "p": Fraction(1, 10)}
    root_goods = ("a", "b")
    source_goods = ("c",)
    x_root = Fraction(10)
    delta = sum(root[g] for g in root_goods) - x_root
    threshold = delta + root["p"]
    rows = []
    successful = []
    for h_size in range(1, len(root_goods) + 1):
        for h in itertools.combinations(root_goods, h_size):
            for d_size in range(len(source_goods) + 1):
                for d in itertools.combinations(source_goods, d_size):
                    source_gain = sum(source[g] for g in h) - sum(
                        source[g] for g in d
                    )
                    root_net_loss = sum(root[g] for g in h) - sum(
                        root[g] for g in d
                    )
                    admissible = source_gain > 0
                    root_strict = root_net_loss < threshold
                    if admissible and root_strict:
                        successful.append((h, d))
                    rows.append({
                        "h": list(h), "d": list(d),
                        "source_gain": str(source_gain),
                        "root_net_loss": str(root_net_loss),
                        "admissible": admissible,
                        "root_strict": root_strict,
                    })
    assert sum(source[g] for g in root_goods) > sum(
        source[g] for g in source_goods
    )
    assert not successful
    assert root["c"] + root["p"] <= x_root
    return {
        "root_values": {g: str(v) for g, v in root.items()},
        "source_values": {g: str(v) for g, v in source.items()},
        "x_root": str(x_root),
        "delta": str(delta),
        "threshold": str(threshold),
        "response": list(root_goods),
        "response_desired": True,
        "successful_admissible_pairs": 0,
        "cases": rows,
        "scope": "local scalar separator only; not a fixed-U/GG countermodel",
    }


def run(root: Path):
    rows = topology_cases()
    checks = algebra_checks()
    witness = local_separator_witness()
    script = Path(__file__).resolve()
    theorem = root / "results" / (
        "PERMANENT_ANCHOR_ROOT_TARGET_BILATERAL_COMPENSATOR_"
        "FRONTIER_LEMMA_20260814.md"
    )
    return {
        "schema": "permanent-anchor-root-target-bilateral-compensator-frontier-v2",
        "status": "EXACT_FOUR_EDGE_BILATERAL_FRONTIER_OR_TWO_ROW_SEPARATOR",
        "case_count": len(rows),
        "four_edge_case_count": sum(row["four_edge_feasible"] for row in rows),
        "overflow_case_count": sum(not row["four_edge_feasible"] for row in rows),
        "maximum_feasible_edge_count": max(
            row["edge_count"] for row in rows if row["four_edge_feasible"]
        ),
        **checks,
        "local_separator_witness": witness,
        "cases": rows,
        "claim_boundary": (
            "cap-free exhaustion of the declared bilateral family; the "
            "two-row separator and decorated-response recurrence remain open"
        ),
        "provenance": {
            "z3": z3.get_version_string(),
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "cases": result["case_count"],
        "four_edge_cases": result["four_edge_case_count"],
        "overflow_cases": result["overflow_case_count"],
        "maximum_feasible_edges": result["maximum_feasible_edge_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
