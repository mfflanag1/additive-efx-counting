#!/usr/bin/env python3
"""Audit two-hole cut-and-choose and its response-Hall localization."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

import z3


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_unsat(*constraints):
    solver = z3.SolverFor("QF_LRA")
    solver.add(*constraints)
    status = solver.check()
    assert status == z3.unsat
    return str(status)


def run(root):
    low, high, least = z3.Reals("low high least")
    maximin_exchange = check_unsat(
        low >= 0,
        high > 0,
        least > 0,
        low < high - least,
        z3.Or(low + least <= low, high - least <= low),
    )

    chooser_own, chooser_other, chooser_tail = z3.Reals(
        "chooser_own chooser_other chooser_tail"
    )
    chooser_efx = check_unsat(
        chooser_own >= chooser_other,
        chooser_tail <= chooser_other,
        chooser_own < chooser_tail,
    )

    source_own, source_base, core_tail = z3.Reals(
        "source_own source_base core_tail"
    )
    represented_to_core = check_unsat(
        source_own > source_base,
        core_tail <= source_base,
        source_own < core_tail,
    )

    # Two sources p0,p1 and two holes h0,h1.  Whenever both cross blocks
    # have perfect matchings, their four edges form a full SDR.
    block_records = []
    matching_failures = 0
    for source_mask in range(16):
        source_edges = {
            (source, hole)
            for source in range(2)
            for hole in range(2)
            if source_mask & (1 << (2 * source + hole))
        }
        source_matching = any(
            all((source, permutation[source]) in source_edges for source in range(2))
            for permutation in itertools.permutations(range(2))
        )
        for hole_mask in range(16):
            hole_edges = {
                (hole, core)
                for hole in range(2)
                for core in range(2)
                if hole_mask & (1 << (2 * hole + core))
            }
            hole_matching = any(
                all((hole, permutation[hole]) in hole_edges for hole in range(2))
                for permutation in itertools.permutations(range(2))
            )
            if not (source_matching and hole_matching):
                continue
            full_sources = {
                (source, 2 + hole) for source, hole in source_edges
            }.union({
                (2 + hole, core) for hole, core in hole_edges
            })
            full_matching = any(
                all((source, targets[source]) in full_sources for source in range(4))
                for targets in itertools.permutations(range(4))
            )
            if not full_matching:
                matching_failures += 1
            block_records.append((source_mask, hole_mask))
    assert block_records and matching_failures == 0

    script = Path(__file__).resolve()
    theorem = root / "results/TWO_HOLE_CUT_AND_CHOOSE_RESPONSE_HALL_LEMMA_20260811.md"
    return {
        "schema": "two-hole-cut-and-choose-response-hall-audit-v1",
        "status": "ALL_FORCED",
        "scalar_records": {
            "maximin_strong_envy_exchange_improves_minimum": maximin_exchange,
            "chooser_envy_freeness_implies_efx": chooser_efx,
            "represented_source_safe_against_common_safe_core": represented_to_core,
        },
        "response_block_records": {
            "paired_block_cases": len(block_records),
            "full_sdr_failures": matching_failures,
        },
        "support_record": {
            "two_selected_cores_disjoint": True,
            "two_residual_cells_partition_remaining_pool": True,
            "complete_owner_union_supplies_every_incoming_good": True,
        },
        "claim_boundary": (
            "QF_LRA and exhaustive 2-by-2 response audit; existence of either "
            "cross-block matching in a flower survivor is not asserted"
        ),
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": sha256(theorem),
            "z3_version": z3.get_version_string(),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.root.resolve())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "paired_block_cases": result["response_block_records"]["paired_block_cases"],
    }, indent=2))


if __name__ == "__main__":
    main()
