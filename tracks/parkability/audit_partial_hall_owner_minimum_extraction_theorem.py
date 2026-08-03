#!/usr/bin/env python3
"""Audit the 16 singleton-pattern cases for owner-minimum Hall extraction."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def paths(directory: Path, mask: int) -> tuple[Path, Path]:
    if mask == 0:
        stem = "partial_hall_owner_minimum_ties_extraction_aggregate"
    else:
        stem = f"partial_hall_owner_minimum_ties_singletons_{mask:02d}"
    return directory / f"{stem}.json", directory / f"{stem}.smt2"


def run(directory: Path, output: Path) -> dict:
    cases = []
    for mask in range(16):
        artifact_path, formula_path = paths(directory, mask)
        artifact = json.loads(artifact_path.read_text())
        expected_labels = [bundle for bundle in range(4) if mask & (1 << bundle)]
        formula_hash = sha256(formula_path)
        checks = {
            "solver_unsat": artifact["solver_verdict"] == "unsat",
            "forced_status": artifact["status"]
            == "OWNER_MINIMUM_PAIR_EXTRACTION_FORCED",
            "ties_allowed": artifact["owner_minimum_ties_allowed"] is True,
            "singleton_labels_exact": artifact["singleton_bundle_labels"]
            == expected_labels,
            "formula_hash_exact": artifact["smt2_sha256"] == formula_hash,
        }
        cases.append(
            {
                "singleton_mask": mask,
                "singleton_bundle_labels": expected_labels,
                "singleton_count": len(expected_labels),
                "artifact": str(artifact_path),
                "formula": str(formula_path),
                "formula_sha256": formula_hash,
                "candidate_count": artifact["candidate_count"],
                "checks": checks,
                "passed": all(checks.values()),
            }
        )

    representative_masks = [0, 1, 3, 7, 15]
    independent = []
    for mask in representative_masks:
        artifact_path, formula_path = paths(directory, mask)
        cvc5_path = formula_path.with_name(f"{formula_path.stem}_cvc5.json")
        cvc5 = json.loads(cvc5_path.read_text())
        checks = {
            "cvc5_unsat": cvc5["status"] == "UNSAT",
            "formula_hash_exact": cvc5["source_sha256"] == sha256(formula_path),
        }
        independent.append(
            {
                "singleton_count": mask.bit_count(),
                "representative_mask": mask,
                "cvc5_artifact": str(cvc5_path),
                "solver": cvc5["solver"],
                "solver_version": cvc5["solver_version"],
                "checks": checks,
                "passed": all(checks.values()),
            }
        )

    artifact = {
        "schema": "partial-hall-owner-minimum-extraction-theorem-audit-v1",
        "status": (
            "VERIFIED"
            if all(case["passed"] for case in cases)
            and all(record["passed"] for record in independent)
            else "FAILED"
        ),
        "theorem_boundary": (
            "For four positive-additive agents, every eligible one-floater EFX "
            "state either has an EFX perfect matching after direct insertion or "
            "one owner-minimum transfer, or one candidate graph has a two-agent "
            "Hall witness with exactly one neighbor."
        ),
        "singleton_pattern_cases": cases,
        "independent_cvc5_symmetry_representatives": independent,
        "symmetry_argument": (
            "Simultaneously permuting agent and bundle labels maps singleton "
            "patterns with the same cardinality, so masks 0,1,3,7,15 represent "
            "the five possible singleton counts. All 16 masks were also solved "
            "directly by Z3."
        ),
        "claim_boundary": (
            "This proves pair extraction, not conversion of a pair trap into a "
            "better eligible partial allocation and not complete EFX existence."
        ),
    }
    if artifact["status"] != "VERIFIED":
        raise AssertionError("owner-minimum extraction theorem audit failed")
    atomic_json(output, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, default=Path("results"))
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.directory, args.output), indent=2))


if __name__ == "__main__":
    main()
