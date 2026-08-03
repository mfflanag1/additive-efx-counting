#!/usr/bin/env python3
"""Build the standalone eight-fact core for cross-row clause A0."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_minimum_slot_orbit import bundles_from_masks
    from .run_minimum_slot_orbit_cegar import (
        BASE,
        eligible,
        efx_edge,
        theta_upper_bound,
    )
except ImportError:
    from anneal import atomic_json
    from audit_minimum_slot_orbit import bundles_from_masks
    from run_minimum_slot_orbit_cegar import (
        BASE,
        eligible,
        efx_edge,
        theta_upper_bound,
    )


SCHEMA = "pair-hall-cross-row-a0-core-v1"
GLOBAL_STATES = (
    (0, (10, 260, 48, 192)),
    (8, (3, 24, 36, 192)),
    (8, (3, 40, 20, 192)),
)


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(smt2_output: Path, metadata_output: Path):
    if smt2_output.exists() or metadata_output.exists():
        raise ValueError("new output paths required")
    values = [
        [z3.Real(f"v_{agent}_{good}") for good in range(9)]
        for agent in range(4)
    ]
    solver = z3.SolverFor("QF_LRA")
    solver.add(eligible(values, BASE, 8))
    solver.add(values[2][5] < values[2][4])
    solver.add(values[2][3] > 0)

    for host, observer, assigned in ((1, 1, 2), (2, 1, 1)):
        complete = [tuple(bundle) for bundle in BASE]
        complete[host] = tuple(sorted((*complete[host], 8)))
        solver.add(z3.Not(efx_edge(values, complete, observer, assigned)))

    base_theta = z3.Sum(values[0][0], values[1][2], values[2][4], values[3][6])
    for floater, masks in GLOBAL_STATES:
        bundles = bundles_from_masks(masks, 9)
        solver.add(
            z3.Implies(
                eligible(values, bundles, floater),
                theta_upper_bound(values, bundles, base_theta),
            )
        )

    solver.add(values[0][0] < values[0][3])
    solver.add(values[2][2] > values[2][3] + values[2][4])
    smt2_output.write_text(solver.to_smt2())
    verdict = solver.check()
    metadata = {
        "schema": SCHEMA,
        "status": "A0_CORE_UNSAT" if verdict == z3.unsat else "INCOMPLETE",
        "meaning": (
            "Standalone refutation of the negation of cross-row clause A0 "
            "using exactly the eight top-level facts selected by the minimized "
            "structural UNSAT core."
        ),
        "solver": "z3",
        "solver_version": z3.get_version_string(),
        "solver_profile": "qf_lra",
        "verdict": str(verdict),
        "smt2": str(smt2_output),
        "smt2_sha256": sha256(smt2_output),
        "top_level_assertion_count": len(solver.assertions()),
        "global_states": [
            {"floater": floater, "masks": list(masks)}
            for floater, masks in GLOBAL_STATES
        ],
        "structural_core_labels": [
            "base_eligible",
            "owner_2_unique_minimum",
            "positive_2_3",
            "pair_hall_1_1_2",
            "pair_hall_2_1_1",
            "global_0_10_260_48_192",
            "global_8_3_24_36_192",
            "global_8_3_40_20_192"
        ],
        "refuted_conjunction": [
            "v_0_0 < v_0_3",
            "v_2_2 > v_2_3 + v_2_4"
        ]
    }
    atomic_json(metadata_output, metadata)
    return metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smt2-output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    args = parser.parse_args()
    metadata = run(args.smt2_output, args.metadata_output)
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
