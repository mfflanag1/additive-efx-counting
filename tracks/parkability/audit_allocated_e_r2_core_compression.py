#!/usr/bin/env python3
"""Integrity/replay audit of the bounded allocated-E R2 core compression."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import z3

from .run_allocated_e_capture_rank_three_cegar import build_master
from .run_generalized_pi_named_selector_cegar import generalized_pi_cut


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT = ROOT / "results" / "ALLOCATED_E_R2_CORE_COMPRESSION_CHECKPOINT_20260813.md"
RAW = ROOT / "results" / "allocated_e_form0_pi_unsat_core.json"
CORE0 = ROOT / "results" / "allocated_e_form0_pi_greedy_minimal_core.json"
CORE1 = ROOT / "results" / "allocated_e_form0_pi_greedy_minimal_core_seed1.json"
FULL = ROOT / "results" / "allocated_e_form0_full_unsat_core.json"
ANALYSIS = ROOT / "results" / "allocated_e_form0_full_unsat_core_analysis.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    raw = json.loads(RAW.read_text())
    core0 = json.loads(CORE0.read_text())
    core1 = json.loads(CORE1.read_text())
    full = json.loads(FULL.read_text())
    analysis = json.loads(ANALYSIS.read_text())
    assert raw["status"] == "unsat" and raw["core_count"] == 53
    for core in (core0, core1):
        assert core["status"] == "unsat" and core["core_count"] == 32
        assert core["source_sha256"] == sha(RAW)
    indices0 = {row["index"] for row in core0["core"]}
    indices1 = {row["index"] for row in core1["core"]}
    assert indices0 == indices1 and len(indices0) == 32

    solver, value = build_master(0)
    for row in core1["core"]:
        solver.add(generalized_pi_cut(value, row["witness"]))
    solver.set(timeout=600000, random_seed=9137)
    assert solver.check() == z3.unsat

    assert full["status"] == "unsat" and full["core_count"] == 92
    assert full["source_sha256"] == sha(CORE0)
    assert analysis["status"] == "CORE_DECODED"
    assert analysis["source_sha256"] == sha(FULL)
    assert analysis["pi_family_count"] == 55
    assert analysis["numerical_premise_count"] == 37
    assert analysis["pi_family_kind_counts"] == {
        "anchored": 6, "higher": 32, "pair": 7, "self": 10,
    }
    source_sets = Counter(tuple(source for source, _ in row["signature"])
                          for row in core1["core"])
    assert source_sets == Counter({
        ("d", "q", "r", "s"): 14,
        ("q", "r", "s"): 12,
        ("d", "q", "r"): 2,
        ("d", "q", "s"): 2,
        ("d", "r", "s"): 2,
    })
    return {
        "schema": "allocated-e-r2-core-compression-audit-v1",
        "status": "CORE_COMPRESSION_REPLAYED",
        "raw_core_count": 53,
        "stable_higher_order_core_count": 32,
        "full_core_count": 92,
        "pi_family_count": 55,
        "numerical_premise_count": 37,
        "replay_solver": f"Z3 {z3.get_version_string()}",
        "replay_random_seed": 9137,
        "replay_status": "unsat",
        "document_sha256": sha(DOCUMENT),
        "source_code_sha256": sha(Path(__file__)),
        "artifact_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (RAW, CORE0, CORE1, FULL, ANALYSIS)
        },
        "claim_boundary": (
            "Integrity and independent-seed replay of a bounded twelve-good "
            "R2 core. It is not an independent encoding or cap-free proof."
        ),
    }


def main():
    result = audit()
    output = ROOT / "results" / "allocated_e_r2_core_compression_audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "stable_core": result["stable_higher_order_core_count"],
        "full_core": result["full_core_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
