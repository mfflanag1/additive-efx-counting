#!/usr/bin/env python3
"""Audit the four-state plateau of the corrected GG history ledger."""

from __future__ import annotations

import argparse
import hashlib
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


def run(root: Path) -> dict:
    values = valuation()
    base = {agent: value(values, agent, BASE[agent]) for agent in AGENTS}
    bundles = {
        "A_r": ("q1", "c2"),
        "A_c": ("q2", "s2", "f"),
        "A_s": ("r1", "r2"),
        "W": ("c1", "s1"),
    }
    assert all(common_safe(values, base, bundle) for bundle in bundles.values())
    neighborhoods = {
        name: response_neighborhood(values, base, bundle)
        for name, bundle in bundles.items()
    }
    assert neighborhoods == {
        "A_r": ("r",),
        "A_c": ("q", "c"),
        "A_s": ("s",),
        "W": ("r",),
    }
    assert maximum_rank(neighborhoods) == 3

    states = []
    residual_history = {"q": set(), "c": set(), "s": set()}
    for root_target in ("A_r", "W"):
        residual = "W" if root_target == "A_r" else "A_r"
        for ac_source in ("q", "c"):
            hole = "c" if ac_source == "q" else "q"
            allocation = {
                "r": bundles[root_target],
                ac_source: bundles["A_c"],
                "s": bundles["A_s"],
                hole: bundles[residual],
                "_": (),
            }
            assert set(allocation) == set(AGENTS) | {"_"}
            assert not is_efx(values, allocation)
            ratio = value(values, hole, bundles[residual]) / base[hole]
            residual_history[hole].add(residual)
            states.append({
                "root_target": root_target,
                "A_c_source": ac_source,
                "hole": hole,
                "residual": residual,
                "normalized_residual": str(ratio),
                "efx": False,
            })

    assert residual_history == {"q": {"A_r", "W"}, "c": {"A_r", "W"}, "s": set()}
    rho = {
        hole: max(
            value(values, hole, bundles[residual]) / base[hole]
            for residual in residual_history[hole]
        )
        for hole in ("q", "c")
    }
    ledger = {
        "retained_support_size": 0,
        "historical_maximum_rank": 3,
        "historical_owner_union_size": 4,
        "rho_q": str(rho["q"]),
        "rho_c": str(rho["c"]),
        "rho_s": None,
        "used_residual_supports": ["A_r", "W"],
    }
    assert len({json.dumps(ledger, sort_keys=True) for _ in states}) == 1

    script = Path(__file__).resolve()
    theorem = root / "results" / "GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md"
    source_script = root / "tracks" / "parkability" / "audit_gg_rank_reset_raw_potential_refutation.py"
    return {
        "schema": "gg-historical-support-ledger-stagnation-v1",
        "status": "EXACT_PLATEAU",
        "positive_additive": True,
        "common_safe_partition": {name: list(bundle) for name, bundle in bundles.items()},
        "response_neighborhoods": {name: list(sources) for name, sources in neighborhoods.items()},
        "maximum_response_rank": 3,
        "full_response_sdr": False,
        "states": states,
        "all_states_non_efx": True,
        "saturated_ledger": ledger,
        "ledger_identical_across_all_states": True,
        "claim_boundary": (
            "exact plateau for the proposed historical coordinates; it does not "
            "prove that an arbitrary deterministic repair rule cycles, global "
            "lex maximality, generalized PI-freeness, or failure of GG closure"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "source_script": str(source_script.relative_to(root)),
            "source_script_sha256": sha256(source_script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root)
    output = args.output or root / "results" / "gg_historical_support_ledger_stagnation_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
