#!/usr/bin/env python3
"""Exact global-lex CEGAR for the minimal residual-top GG flower cell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from . import run_minimal_flower_global_lex_cegar as base_cegar
except ImportError:
    import run_minimal_flower_global_lex_cegar as base_cegar


def configure_residual_cell():
    base_cegar.GOODS = (
        "k", "j", "br", "tq", "bq", "tc", "bc", "z", "f",
    )
    base_cegar.BASE_BUNDLES = {
        "r": ("k", "j", "br"),
        "q": ("tq", "bq"),
        "c": ("tc", "bc"),
        "s": ("z",),
    }
    base_cegar.DISPLAYED_BUNDLES = {
        "D_r": ("tq", "f"),
        "D_q": ("k", "j", "f"),
        "D_c": ("tc", "f"),
        "A_q": ("tq", "br"),
        "A_r": ("k", "bq"),
        "Z": ("z",),
        **{
            f"X_{agent}": goods
            for agent, goods in base_cegar.BASE_BUNDLES.items()
        },
    }


def install_live_master():
    original = base_cegar.build_master

    def build_master():
        solver, value, base = original()
        amount = base_cegar.amount
        solver.add(value["q", "f"] <= value["q", "bq"])
        solver.add(
            amount(value, "r", base_cegar.BASE_BUNDLES["q"]) < base["r"]
        )
        solver.add(
            amount(value, "q", base_cegar.BASE_BUNDLES["r"]) <= base["q"]
        )
        solver.add(value["q", "k"] <= value["q", "tq"])
        return solver, value, base

    base_cegar.build_master = build_master


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-iterations", type=int, default=10000)
    parser.add_argument("--time-limit", type=float, default=1800)
    parser.add_argument("--rivals-per-iteration", type=int, default=128)
    args = parser.parse_args()
    configure_residual_cell()
    install_live_master()
    result = base_cegar.run(
        args.max_iterations,
        args.time_limit,
        args.rivals_per_iteration,
        "global-lex",
    )
    result["schema"] = "residual-flower-global-lex-cegar-v1"
    result["cell"] = {
        "base_bundles": {
            agent: list(goods)
            for agent, goods in base_cegar.BASE_BUNDLES.items()
        },
        "residual_top": "j",
        "retained_top": "k",
        "live_gate": [
            "q(f)<=q(B_q)",
            "r(X_q)<r(X_r)",
            "q(X_r)<=q(X_q)",
            "q(K)<=q(T_q)",
        ],
    }
    result["claim_boundary"] = (
        "an EXACT_BRIDGE_COUNTEREXAMPLE is a positive nondegenerate additive "
        "residual-top GG flower whose displayed allocation is globally "
        "lex-maximal among every EFX-with-charity allocation; it exactly refutes "
        "the flexible completion bridge but does not refute complete EFX existence. "
        "UNSAT proves only this nine-good symbolic residual cell"
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "iterations": result["iterations"],
        "rival_pool_size": result["rival_pool_size"],
        "nondegeneracy_constraints": result["nondegeneracy_constraints"],
        "elapsed_seconds": result["elapsed_seconds"],
        "solver": f"Z3 {z3.get_version_string()}",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
