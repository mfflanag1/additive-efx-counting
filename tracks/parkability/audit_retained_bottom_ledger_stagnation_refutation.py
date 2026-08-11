#!/usr/bin/env python3
"""Exact tail lift showing stagnation of the retained-bottom ledger."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

try:
    from .audit_gg_rank_reset_raw_potential_refutation import (
        AGENTS,
        BASE,
        common_safe,
        is_efx,
        maximum_rank,
        response_neighborhood,
        valuation,
        value,
    )
except ImportError:
    from audit_gg_rank_reset_raw_potential_refutation import (
        AGENTS,
        BASE,
        common_safe,
        is_efx,
        maximum_rank,
        response_neighborhood,
        valuation,
        value,
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def subset_sum_injective(row, goods) -> bool:
    seen = set()
    for bits in itertools.product((0, 1), repeat=len(goods)):
        total = sum((row[g] for g, bit in zip(goods, bits) if bit), Fraction())
        if total in seen:
            return False
        seen.add(total)
    return True


def run(root: Path) -> dict:
    old = valuation()
    values = {agent: dict(row) for agent, row in old.items()}
    for index, agent in enumerate(AGENTS):
        h_major = 5 if agent == "r" else (1 if agent == "s" else Fraction(1, 2))
        values[agent]["h"] = h_major + Fraction(1, 1 << (120 + 2 * index))
        values[agent]["k"] = Fraction(3 if agent == "s" else 0) + Fraction(1, 1 << (121 + 2 * index))
    values["r"]["q1"] += 5
    values["r"]["c1"] += 4

    goods = ("r1", "r2", "q1", "q2", "c1", "c2", "s1", "s2", "f", "h", "k")
    base_allocation = {
        "r": BASE["r"] + ("h",),
        "q": BASE["q"],
        "c": BASE["c"],
        "s": BASE["s"] + ("k",),
        "_": ("f",),
    }
    base = {agent: value(values, agent, base_allocation[agent]) for agent in AGENTS}
    assert all(amount > 0 for row in values.values() for amount in row.values())
    assert all(subset_sum_injective(values[agent], goods) for agent in AGENTS)
    assert set().union(*(set(base_allocation[key]) for key in (*AGENTS, "_"))) == set(goods)
    assert is_efx(values, base_allocation)
    assert all(base[agent] >= value(values, agent, base_allocation["_"]) for agent in AGENTS)

    cores = {
        "A_r": ("q1", "c2"),
        "A_c": ("q2", "s2", "f"),
        "A_s": ("r1", "r2", "k"),
        "W": ("c1", "s1"),
    }
    assert all(common_safe(values, base, core) for core in cores.values())
    core_neighborhoods = {
        name: response_neighborhood(values, base, core)
        for name, core in cores.items()
    }
    assert core_neighborhoods == {
        "A_r": ("r",),
        "A_c": ("q", "c"),
        "A_s": ("s",),
        "W": ("r",),
    }
    assert maximum_rank(core_neighborhoods) == 3
    states = []
    residual_history = {"q": set(), "c": set()}
    for root_name in ("A_r", "W"):
        residual_name = "W" if root_name == "A_r" else "A_r"
        targets = {
            root_name: cores[root_name] + ("h",),
            "A_c": cores["A_c"],
            "A_s": cores["A_s"],
            residual_name: cores[residual_name],
        }
        assert set().union(*(set(target) for target in targets.values())) == set(goods)
        assert sum(len(target) for target in targets.values()) == len(goods)

        for ac_source in ("q", "c"):
            hole = "c" if ac_source == "q" else "q"
            allocation = {
                "r": targets[root_name],
                ac_source: targets["A_c"],
                "s": targets["A_s"],
                hole: targets[residual_name],
                "_": (),
            }
            assert not is_efx(values, allocation)
            residual_history[hole].add(residual_name)
            states.append({
                "root_target": root_name,
                "A_c_source": ac_source,
                "hole": hole,
                "residual": residual_name,
                "root_tail": ["h"],
                "selected_root_core_avoids_h": True,
                "efx": False,
            })

    rho = {
        hole: max(
            value(values, hole, cores[name]) / base[hole]
            for name in residual_history[hole]
        )
        for hole in ("q", "c")
    }
    ledger = {
        "retained_top_support_size": 0,
        "historical_maximum_rank": 3,
        "historical_owner_union_size": 4,
        "rho_q": str(rho["q"]),
        "rho_c": str(rho["c"]),
        "rho_s": None,
        "used_residual_supports": ["A_r", "W"],
        "absorbed_bottom_support": ["h"],
        "consumed_bottom_support": [],
    }

    theorem = root / "results/RETAINED_BOTTOM_LEDGER_STAGNATION_REFUTATION_20260811.md"
    script = Path(__file__).resolve()
    source = root / "tracks/parkability/audit_gg_rank_reset_raw_potential_refutation.py"
    return {
        "schema": "retained-bottom-ledger-stagnation-refutation-v1",
        "status": "EXACT_BOTTOM_TAIL_PLATEAU",
        "positive_additive": True,
        "subset_sum_injective": True,
        "base_efx": True,
        "charity_dominated": True,
        "selected_cores_common_safe": True,
        "maximum_response_rank": 3,
        "full_response_sdr": False,
        "response_neighborhoods": {
            name: list(sources) for name, sources in core_neighborhoods.items()
        },
        "states": states,
        "all_states_non_efx": True,
        "expanded_ledger": ledger,
        "ledger_identical_across_all_states": True,
        "support_disjoint": True,
        "claim_boundary": (
            "exact local plateau with fixed absorbed and consumed bottom support; "
            "not global lex maximality, generalized PI-freeness, GG failure, or "
            "an EFX counterexample"
        ),
        "smallest_missing_operation": (
            "current-state selector or surplus-budgeted connected component "
            "splicing the repeated root-facing return with the bottom tail"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "source_script": str(source.relative_to(root)),
            "source_script_sha256": sha256(source),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
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
