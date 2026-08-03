#!/usr/bin/env python3
"""Verify and hash-bind the eight independent cvc5/CPC/Ethos certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path


CELLS = (
    "favorite-211",
    "favorite-31",
    "favorite-22",
    "top4-second1111",
    "top4-second4",
    "top4-second31",
    "top4-second22",
    "top4-second211",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def resolve_record_path(root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
        return path.resolve()
    resolved = path.resolve()
    try:
        resolved.relative_to(root)
        return resolved
    except ValueError:
        pass
    for marker in ("independent-formulas", "proofs", "tools"):
        if marker not in resolved.parts:
            continue
        suffix = resolved.parts[resolved.parts.index(marker):]
        relocated = root.joinpath(*suffix).resolve()
        if relocated.is_file():
            return relocated
    return resolved


def require_hash(path: Path, expected: str, label: str) -> str:
    if not path.is_file():
        raise ValueError(f"{label} is missing: {path}")
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"{label} hash mismatch: expected {expected}, got {actual}"
        )
    return actual


def relative_to_root(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError as error:
        raise ValueError(f"certificate dependency escapes root: {path}") from error


def verify_cell(root: Path, cell: str) -> tuple[dict, set[Path]]:
    certificate_path = root / "proofs" / f"{cell}.independent.certificate.json"
    if not certificate_path.is_file():
        raise ValueError(f"missing certificate for {cell}: {certificate_path}")
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("schema") != "cvc5-cpc-ethos-certificate-v1":
        raise ValueError(f"{cell}: unexpected certificate schema")
    if certificate.get("verified") is not True:
        raise ValueError(f"{cell}: certificate is not marked verified")
    solve = certificate.get("solve", {})
    check = certificate.get("check", {})
    if (
        solve.get("returncode") != 0
        or solve.get("timed_out") is not False
        or check.get("returncode") != 0
        or check.get("timed_out") is not False
        or check.get("status") != "correct"
        or check.get("stdout", "").strip() != "correct"
    ):
        raise ValueError(f"{cell}: solver/checker result is not successful")

    dependencies = {certificate_path.resolve()}
    fields = (
        ("formula", "formula_sha256"),
        ("proof", "proof_sha256"),
        ("cvc5", "cvc5_sha256"),
        ("ethos", "ethos_sha256"),
        ("cpc_signature", "cpc_signature_sha256"),
        ("expert_signature", "expert_signature_sha256"),
    )
    resolved = {}
    for path_field, hash_field in fields:
        path = resolve_record_path(root, certificate[path_field])
        require_hash(path, certificate[hash_field], f"{cell} {path_field}")
        dependencies.add(path)
        resolved[path_field] = relative_to_root(root, path)

    proof = resolve_record_path(root, certificate["proof"])
    if proof.stat().st_size != certificate["proof_bytes"]:
        raise ValueError(f"{cell}: proof byte count mismatch")
    with proof.open("rb") as handle:
        proof_steps = sum(
            1
            for line in handle
            if b"(step " in line or b"(assume " in line
        )
    if proof_steps != certificate["proof_step_lines"]:
        raise ValueError(f"{cell}: proof step-line count mismatch")

    formula_metadata_path = (
        root / "independent-formulas" / f"{cell}.independent.json"
    )
    formula_metadata = json.loads(formula_metadata_path.read_text())
    if formula_metadata.get("formula_sha256") != certificate["formula_sha256"]:
        raise ValueError(f"{cell}: formula metadata/certificate hash mismatch")
    dependencies.add(formula_metadata_path.resolve())

    summary = {
        "cell": cell,
        "formula": resolved["formula"],
        "formula_sha256": certificate["formula_sha256"],
        "proof": resolved["proof"],
        "proof_sha256": certificate["proof_sha256"],
        "proof_bytes": certificate["proof_bytes"],
        "proof_step_lines": certificate["proof_step_lines"],
        "solve_elapsed_seconds": solve["elapsed_seconds"],
        "check_elapsed_seconds": check["elapsed_seconds"],
        "check_status": check["status"],
        "verified": True,
    }
    return summary, dependencies


def finalize(root: Path) -> dict:
    root = root.resolve()
    summaries = []
    dependencies: set[Path] = set()
    for cell in CELLS:
        summary, cell_dependencies = verify_cell(root, cell)
        summaries.append(summary)
        dependencies.update(cell_dependencies)

    for relative in (
        "independent-generator-audit/audit.json",
        "independent-generator-audit/cell-preambles.json",
        "independent-generator-audit/semantic-binding.json",
        "rebuilt-formulas-isolated-v2/rebuild-audit.json",
        "z3-replay/partition-top4-second4.z3.json",
    ):
        path = (root / relative).resolve()
        if not path.is_file():
            raise ValueError(f"missing supporting audit: {path}")
        dependencies.add(path)

    semantic_path = (
        root / "independent-generator-audit" / "semantic-binding.json"
    )
    semantic = json.loads(semantic_path.read_text())
    if (
        semantic.get("schema")
        != "independent-formula-semantic-binding-v1"
        or semantic.get("all_passed") is not True
        or semantic.get("cell_count") != len(CELLS)
        or semantic.get("partition_universe_count") != 1701
        or semantic.get("lean_constant_binding", {}).get("all_passed")
        is not True
    ):
        raise ValueError("semantic formula binding audit is incomplete")
    semantic_records = {
        record["cell"]: record for record in semantic.get("records", [])
    }
    if set(semantic_records) != set(CELLS):
        raise ValueError("semantic formula binding cell set mismatch")
    summary_by_cell = {summary["cell"]: summary for summary in summaries}
    for cell in CELLS:
        semantic_record = semantic_records[cell]
        if (
            semantic_record.get("passed") is not True
            or semantic_record.get("partition_count") != 1701
            or semantic_record.get("formula_sha256")
            != summary_by_cell[cell]["formula_sha256"]
            or semantic_record.get(
                "all_24_matchings_checked_per_partition"
            )
            is not True
        ):
            raise ValueError(f"{cell}: semantic formula binding mismatch")

    semantic_checker = (
        Path(__file__).with_name(
            "audit_independent_formula_semantics.py"
        ).resolve()
    )
    require_hash(
        semantic_checker,
        semantic["checker_sha256"],
        "semantic formula binding checker",
    )

    published_path = root / "literature" / "PUBLISHED_INPUT_AUDIT.json"
    if not published_path.is_file():
        raise ValueError(
            f"missing published-input audit: {published_path}"
        )
    dependencies.add(published_path.resolve())
    published = json.loads(published_path.read_text())
    if (
        published.get("schema") != "efx48-published-input-audit-v1"
        or published.get("all_passed") is not True
        or len(published.get("papers", [])) != 2
    ):
        raise ValueError("published-input audit is incomplete")
    expected_variant_checks = {
        "complete_allocation": True,
        "efx_any_target_good": True,
        "additive_three_agent_input": True,
        "four_agent_seven_good_is_n_plus_three": True,
        "strict_positivity_is_a_valid_restriction": True,
        "paper_theorems_formalized_in_lean": False,
    }
    if published.get("variant_checks") != expected_variant_checks:
        raise ValueError("published-input variant checks are incomplete")
    for record in published["papers"]:
        if (
            record.get("hash_matches") is not True
            or record.get("all_fragments_found") is not True
            or not all(
                fragment.get("found") is True
                for fragment in record.get("required_fragments", [])
            )
        ):
            raise ValueError(
                f"{record.get('key')}: published-input record failed"
            )
        paper = (root / record["path"]).resolve()
        require_hash(
            paper,
            record["sha256"],
            f"{record['key']} paper",
        )
        dependencies.add(paper)

    published_checker = (
        Path(__file__).with_name("audit_published_inputs.py").resolve()
    )
    require_hash(
        published_checker,
        published["checker_sha256"],
        "published-input checker",
    )
    lean_root = Path(__file__).resolve().parents[2] / "formal" / "efx48"
    for record in published.get("lean_sources", []):
        require_hash(
            lean_root / record["path"],
            record["sha256"],
            f"published-input Lean source {record['path']}",
        )

    total_proof_bytes = sum(item["proof_bytes"] for item in summaries)
    total_proof_steps = sum(item["proof_step_lines"] for item in summaries)
    result = {
        "schema": "efx48-eight-cell-cpc-certificate-set-v1",
        "claim": (
            "all eight independently generated residual canonical-cell "
            "QF_LRA formulas are unsatisfiable"
        ),
        "cell_count": len(summaries),
        "all_verified": all(item["verified"] for item in summaries),
        "total_proof_bytes": total_proof_bytes,
        "total_proof_step_lines": total_proof_steps,
        "semantic_binding": relative_to_root(root, semantic_path),
        "semantic_binding_sha256": sha256(semantic_path),
        "semantic_binding_all_passed": True,
        "published_input_audit": relative_to_root(
            root, published_path
        ),
        "published_input_audit_sha256": sha256(published_path),
        "published_input_audit_all_passed": True,
        "cells": summaries,
    }
    summary_path = root / "EIGHT_CELL_CPC_CERTIFICATES.json"
    atomic_write(
        summary_path,
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode(),
    )
    dependencies.add(summary_path.resolve())

    manifest_lines = []
    for path in sorted(
        dependencies,
        key=lambda item: relative_to_root(root, item),
    ):
        manifest_lines.append(
            f"{sha256(path)}  {relative_to_root(root, path)}"
        )
    manifest_path = root / "EIGHT_CELL_CPC_MANIFEST.sha256"
    atomic_write(
        manifest_path,
        ("\n".join(manifest_lines) + "\n").encode(),
    )
    result["summary"] = str(summary_path)
    result["manifest"] = str(manifest_path)
    result["manifest_entry_count"] = len(manifest_lines)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(finalize(args.root), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
