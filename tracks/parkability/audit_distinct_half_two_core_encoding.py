#!/usr/bin/env python3
"""Audit the direct and QF_LRA semantics of the two-core/Tutte gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import z3

try:
    from .anneal import atomic_json
    from .audit_distinct_half_favorite_triple_boundary import (
        VALUES as NO_WITNESS_VALUES,
    )
    from .audit_distinct_half_two_core_boundary import (
        VALUES as WITNESS_VALUES,
    )
    from .audit_distinct_half_canonical_two_core_boundary import (
        VALUES as CANONICAL_BOUNDARY_VALUES,
    )
    from .lra_master import ParkabilityLRAMaster
    from .run_distinct_half_two_core_cegar import (
        M,
        N,
        add_no_two_core,
        add_no_two_core_reified,
        two_core_witnesses,
    )
except ImportError:
    from anneal import atomic_json
    from audit_distinct_half_favorite_triple_boundary import (
        VALUES as NO_WITNESS_VALUES,
    )
    from audit_distinct_half_two_core_boundary import (
        VALUES as WITNESS_VALUES,
    )
    from audit_distinct_half_canonical_two_core_boundary import (
        VALUES as CANONICAL_BOUNDARY_VALUES,
    )
    from lra_master import ParkabilityLRAMaster
    from run_distinct_half_two_core_cegar import (
        M,
        N,
        add_no_two_core,
        add_no_two_core_reified,
        two_core_witnesses,
    )


SCHEMA = "distinct-half-two-core-encoding-audit-v2"
EXPECTED_COUNTS = {
    "encoding": "direct",
    "low_core_cells": 168,
    "lost_core_literals": 5040,
    "bad_perfect_matching_terms": 2520,
}
EXPECTED_REIFIED_COUNTS = {
    "encoding": "reified",
    "accept_literals": 1680,
    "low_core_cells": 168,
    "lost_core_literals": 5040,
    "bad_perfect_matching_terms": 2520,
}


def encoded_status(values, add_encoding, scope="all"):
    master = ParkabilityLRAMaster(N, M, fixed_values=values)
    counts = add_encoding(master, scope)
    return str(master.solver.check()), counts


def audit():
    witnesses = two_core_witnesses(WITNESS_VALUES)
    no_witnesses = two_core_witnesses(NO_WITNESS_VALUES)
    witness_status, witness_counts = encoded_status(
        WITNESS_VALUES, add_no_two_core
    )
    no_witness_status, no_witness_counts = encoded_status(
        NO_WITNESS_VALUES, add_no_two_core
    )
    reified_witness_status, reified_witness_counts = encoded_status(
        WITNESS_VALUES, add_no_two_core_reified
    )
    reified_no_witness_status, reified_no_witness_counts = encoded_status(
        NO_WITNESS_VALUES, add_no_two_core_reified
    )
    canonical_witness_status, canonical_counts = encoded_status(
        WITNESS_VALUES, add_no_two_core, "canonical"
    )
    canonical_no_witness_status, _ = encoded_status(
        NO_WITNESS_VALUES, add_no_two_core, "canonical"
    )
    canonical_reified_witness_status, canonical_reified_counts = (
        encoded_status(
            WITNESS_VALUES, add_no_two_core_reified, "canonical"
        )
    )
    canonical_reified_no_witness_status, _ = encoded_status(
        NO_WITNESS_VALUES, add_no_two_core_reified, "canonical"
    )
    canonical_boundary_witnesses = two_core_witnesses(
        CANONICAL_BOUNDARY_VALUES
    )
    canonical_boundary_canonical_witnesses = two_core_witnesses(
        CANONICAL_BOUNDARY_VALUES, "canonical"
    )
    canonical_boundary_all_status, _ = encoded_status(
        CANONICAL_BOUNDARY_VALUES, add_no_two_core
    )
    canonical_boundary_scope_status, _ = encoded_status(
        CANONICAL_BOUNDARY_VALUES, add_no_two_core, "canonical"
    )
    canonical_boundary_all_reified_status, _ = encoded_status(
        CANONICAL_BOUNDARY_VALUES, add_no_two_core_reified
    )
    canonical_boundary_scope_reified_status, _ = encoded_status(
        CANONICAL_BOUNDARY_VALUES, add_no_two_core_reified, "canonical"
    )
    expected_canonical_counts = {
        "encoding": "direct",
        "low_core_cells": 6,
        "lost_core_literals": 180,
        "bad_perfect_matching_terms": 90,
    }
    expected_canonical_reified_counts = {
        "encoding": "reified",
        "accept_literals": 360,
        "low_core_cells": 6,
        "lost_core_literals": 180,
        "bad_perfect_matching_terms": 90,
    }
    expected_witness = {
        "low_goods": [1, 2],
        "core_agents": [2, 3],
        "bad_edges": [[6, 7]],
    }
    expected_canonical_boundary_witness = {
        "low_goods": [5, 6],
        "core_agents": [1, 3],
        "bad_edges": [[1, 2]],
    }
    if (
        witnesses != [expected_witness]
        or no_witnesses
        or witness_status != str(z3.unsat)
        or no_witness_status != str(z3.sat)
        or witness_counts != EXPECTED_COUNTS
        or no_witness_counts != EXPECTED_COUNTS
        or reified_witness_status != str(z3.unsat)
        or reified_no_witness_status != str(z3.sat)
        or reified_witness_counts != EXPECTED_REIFIED_COUNTS
        or reified_no_witness_counts != EXPECTED_REIFIED_COUNTS
        or canonical_witness_status != str(z3.unsat)
        or canonical_no_witness_status != str(z3.sat)
        or canonical_counts != expected_canonical_counts
        or canonical_reified_witness_status != str(z3.unsat)
        or canonical_reified_no_witness_status != str(z3.sat)
        or canonical_reified_counts != expected_canonical_reified_counts
        or canonical_boundary_witnesses
        != [expected_canonical_boundary_witness]
        or canonical_boundary_canonical_witnesses
        or canonical_boundary_all_status != str(z3.unsat)
        or canonical_boundary_scope_status != str(z3.sat)
        or canonical_boundary_all_reified_status != str(z3.unsat)
        or canonical_boundary_scope_reified_status != str(z3.sat)
    ):
        raise AssertionError("two-core direct/encoding equivalence changed")
    return {
        "schema": SCHEMA,
        "status": "DISTINCT_HALF_TWO_CORE_ENCODING_AUDIT_PASSED",
        "encoding_counts": EXPECTED_COUNTS,
        "reified_encoding_counts": EXPECTED_REIFIED_COUNTS,
        "canonical_encoding_counts": expected_canonical_counts,
        "canonical_reified_encoding_counts": (
            expected_canonical_reified_counts
        ),
        "positive_control": {
            "direct_witnesses": witnesses,
            "no_two_core_formula_status": witness_status,
            "reified_no_two_core_formula_status": reified_witness_status,
        },
        "negative_control": {
            "direct_witnesses": no_witnesses,
            "no_two_core_formula_status": no_witness_status,
            "reified_no_two_core_formula_status": reified_no_witness_status,
        },
        "canonical_scope_control": {
            "unrestricted_direct_witnesses": canonical_boundary_witnesses,
            "canonical_direct_witnesses": (
                canonical_boundary_canonical_witnesses
            ),
            "unrestricted_no_two_core_formula_status": (
                canonical_boundary_all_status
            ),
            "canonical_no_two_core_formula_status": (
                canonical_boundary_scope_status
            ),
            "unrestricted_reified_formula_status": (
                canonical_boundary_all_reified_status
            ),
            "canonical_reified_formula_status": (
                canonical_boundary_scope_reified_status
            ),
        },
        "interpretation": (
            "On a profile with exactly one direct two-core/Tutte witness, "
            "the encoded negation is UNSAT; on a profile with no direct "
            "witness, it is SAT. A third control is SAT in canonical scope "
            "but UNSAT in unrestricted scope. This freezes both polarities "
            "and the scope boundary of the gate."
        ),
        "limitation": (
            "Three fixed controls do not replace an independent symbolic "
            "proof of the quantified encoding, but they catch polarity, "
            "normalization, and perfect-matching mistakes."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
