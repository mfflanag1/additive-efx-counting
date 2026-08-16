#!/usr/bin/env python3
"""Build and hash-bind the complete hybrid Lean/SMT EFX(4,8) proof package."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ESSENTIAL_FILES = (
    "Makefile",
    "requirements.txt",
    "tracks/parkability/core.py",
    "tracks/parkability/independent.py",
    "tracks/parkability/lra_master.py",
    "tracks/parkability/run_lra_cegar.py",
    "tracks/parkability/run_efx_lra_cegar.py",
    "tracks/parkability/run_partition_core.py",
    "tracks/parkability/independent_lra_generator.py",
    "tracks/parkability/audit_independent_lra_generator.py",
    "tracks/parkability/audit_independent_cell_preambles.py",
    "tracks/parkability/audit_independent_formula_semantics.py",
    "tracks/parkability/audit_cpc_formula_assumptions.py",
    "tracks/parkability/audit_published_inputs.py",
    "tracks/parkability/run_cvc5_cpc_proof.py",
    "tracks/parkability/normalize_smt2_for_cvc5.py",
    "tracks/parkability/run_external_smt.py",
    "tracks/parkability/run_direct_cell_lra.py",
    "tracks/parkability/run_direct_all_cells.py",
    "tracks/parkability/shrink_partition_core.py",
    "tracks/parkability/analyze_shrunk_core.py",
    "tracks/parkability/analyze_core_deletion_witnesses.py",
    "tracks/parkability/analyze_hall_witness_patterns.py",
    "tracks/parkability/finalize_cpc_certificates.py",
    "tracks/parkability/finalize_efx48_end_to_end.py",
    "tracks/parkability/replay_efx48_clean_source.py",
    "tracks/parkability/replay_efx48_relocatable_cpc.py",
    "ACCOMPLISHMENTS.md",
    "results/README.md",
    "results/PUBLISHED_INPUT_AUDIT.md",
    "results/EFX48_PROOF_GUIDE.md",
    "results/CORE_200_STRUCTURE.md",
    "results/BROADER_GENERALIZATION_MAP.md",
    "results/NOVELTY_AUDIT_20260729.md",
    "results/EXPERT_REVIEW_CHECKLIST.md",
    "results/EFX48_REVIEWER_HANDOFF.md",
    "results/EFX48_REMAINING_GATES_20260730.md",
    "results/EFX48_BREAKTHROUGH_CONVERSION_20260730.md",
    "results/SESSION_REVIEW_CURRENT_20260729.md",
    "paper/efx48/README.md",
    "paper/efx48/main.tex",
    "paper/efx48/submission.tex",
)

FORBIDDEN_LEAN = re.compile(
    r"\bsorry\b|^\s*axiom\s|^\s*opaque\s",
    re.MULTILINE,
)

DIRECT_CELLS = {
    "favorite-211",
    "favorite-31",
    "favorite-22",
    "top4-second1111",
    "top4-second4",
    "top4-second31",
    "top4-second22",
    "top4-second211",
}


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


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise ValueError(f"{label} is missing: {path}")
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"{label} hash mismatch: expected {expected}, got {actual}"
        )


def verify_manifest(root: Path, manifest: Path) -> set[Path]:
    dependencies = {manifest.resolve()}
    for line_number, line in enumerate(
        manifest.read_text().splitlines(),
        start=1,
    ):
        expected, separator, relative = line.partition("  ")
        if not separator or not expected or not relative:
            raise ValueError(
                f"{manifest}:{line_number}: malformed manifest line"
            )
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ValueError(
                f"{manifest}:{line_number}: path escapes root"
            ) from error
        require_hash(path, expected, f"manifest entry {relative}")
        dependencies.add(path)
    return dependencies


def lean_source_files(lean_root: Path) -> list[Path]:
    files = []
    for path in lean_root.rglob("*"):
        if not path.is_file() or ".lake" in path.parts:
            continue
        if (
            path.suffix in {".lean", ".toml", ".json"}
            or path.name == "lean-toolchain"
        ):
            files.append(path)
    return sorted(files)


def audit_lean_sources(
    lean_root: Path,
) -> tuple[list[Path], list[str]]:
    sources = lean_source_files(lean_root)
    violations = []
    for path in sources:
        if path.suffix != ".lean":
            continue
        text = path.read_text(encoding="utf-8")
        for match in FORBIDDEN_LEAN.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            violations.append(
                f"{path.relative_to(lean_root)}:{line}:{match.group(0)}"
            )
    if violations:
        raise ValueError(
            "forbidden Lean declarations found: "
            + ", ".join(violations)
        )

    entrypoint = lean_root / "EFX48.lean"
    entrypoint_text = entrypoint.read_text(encoding="utf-8")
    imports = {
        line.removeprefix("import ").strip()
        for line in entrypoint_text.splitlines()
        if line.startswith("import ")
    }
    expected_imports = {
        f"EFX48.{path.stem}"
        for path in (lean_root / "EFX48").glob("*.lean")
    }
    missing_imports = sorted(expected_imports - imports)
    if missing_imports:
        raise ValueError(
            "Lean entry point misses modules: "
            + ", ".join(missing_imports)
        )

    lifting = (
        lean_root / "EFX48" / "PublishedLifting.lean"
    ).read_text(encoding="utf-8")
    theorem = "admitsEFX_4x8_of_standard_published_inputs_nonnegative"
    if f"theorem {theorem}" not in lifting:
        raise ValueError(f"final Lean theorem is missing: {theorem}")
    return sources, sorted(imports)


def deterministic_source_archive(
    project_root: Path,
    lean_sources: list[Path],
    destination: Path,
) -> str:
    entries = list(lean_sources)
    for relative in ESSENTIAL_FILES:
        path = project_root / relative
        if not path.is_file():
            raise ValueError(f"proof-package source is missing: {path}")
        entries.append(path)

    descriptor, temporary_name = tempfile.mkstemp(
        dir=destination.parent,
        prefix=f".{destination.name}.",
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in sorted(
                set(entries),
                key=lambda item: str(item.relative_to(project_root)),
            ):
                relative = str(path.relative_to(project_root))
                info = zipfile.ZipInfo(
                    relative,
                    date_time=(1980, 1, 1, 0, 0, 0),
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes())
        os.replace(temporary, destination)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise
    return sha256(destination)


def run_checked(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"command failed with {result.returncode}: {command}\n"
            f"{result.stdout}"
        )
    return result


def finalize(root: Path, project_root: Path) -> dict:
    root = root.resolve()
    project_root = project_root.resolve()
    lean_root = project_root / "formal" / "efx48"

    terminal_summary_path = root / "EIGHT_CELL_CPC_CERTIFICATES.json"
    terminal_manifest_path = root / "EIGHT_CELL_CPC_MANIFEST.sha256"
    if not terminal_summary_path.is_file():
        raise ValueError(
            "eight-cell certificate summary has not been finalized"
        )
    terminal_summary = json.loads(terminal_summary_path.read_text())
    if (
        terminal_summary.get("all_verified") is not True
        or terminal_summary.get("cell_count") != 8
        or terminal_summary.get("semantic_binding_all_passed") is not True
        or terminal_summary.get("published_input_audit_all_passed")
        is not True
    ):
        raise ValueError("eight-cell certificate summary is incomplete")
    dependencies = verify_manifest(root, terminal_manifest_path)

    direct_summary_path = (
        root
        / "direct-allocation-crosscheck"
        / "DIRECT_ALLOCATION_CROSSCHECK.json"
    )
    if not direct_summary_path.is_file():
        raise ValueError("direct-allocation crosscheck is missing")
    direct = json.loads(direct_summary_path.read_text())
    if (
        direct.get("schema")
        != "direct-all-eight-cells-crosscheck-v1"
        or set(direct.get("requested_cells", [])) != DIRECT_CELLS
        or direct.get("completed_cell_count") != 8
        or direct.get("all_requested_completed") is not True
        or direct.get("all_completed_unsat") is not True
        or direct.get("pool_universe_exact") is not True
        or direct.get("allocation_count_per_cell") != 40_824
    ):
        raise ValueError("direct-allocation crosscheck is incomplete")
    records = {
        record["cell"]: record for record in direct.get("records", [])
    }
    if set(records) != DIRECT_CELLS:
        raise ValueError("direct-allocation cell set mismatch")
    direct_directory = direct_summary_path.parent
    dependencies.add(direct_summary_path.resolve())
    for cell, record in records.items():
        if (
            record.get("status")
            not in {"UNSAT_CANDIDATE", "UNSAT_CVC5_REPLAY"}
            or record.get("solver_status") != "unsat"
        ):
            raise ValueError(f"{cell}: direct crosscheck is not UNSAT")
        formula = (direct_directory / record["formula"]).resolve()
        result_record = (direct_directory / record["result"]).resolve()
        try:
            formula.relative_to(direct_directory)
            result_record.relative_to(direct_directory)
        except ValueError as error:
            raise ValueError(
                f"{cell}: direct artifact path escapes its directory"
            ) from error
        require_hash(
            formula,
            record["formula_sha256"],
            f"{cell} direct formula",
        )
        require_hash(
            result_record,
            record["result_sha256"],
            f"{cell} direct result",
        )
        dependencies.update({formula, result_record})
        auxiliary = record.get("auxiliary_artifacts", [])
        if record.get("status") == "UNSAT_CVC5_REPLAY" and len(auxiliary) != 3:
            raise ValueError(f"{cell}: incomplete cvc5 replay evidence")
        auxiliary_by_role = {
            artifact["role"]: artifact for artifact in auxiliary
        }
        auxiliary_paths = {}
        for artifact in auxiliary:
            auxiliary_path = (
                direct_directory / artifact["path"]
            ).resolve()
            try:
                auxiliary_path.relative_to(direct_directory)
            except ValueError as error:
                raise ValueError(
                    f"{cell}: auxiliary path escapes direct directory"
                ) from error
            require_hash(
                auxiliary_path,
                artifact["sha256"],
                f"{cell} {artifact['role']}",
            )
            dependencies.add(auxiliary_path)
            auxiliary_paths[artifact["role"]] = auxiliary_path
        if record.get("status") == "UNSAT_CVC5_REPLAY":
            expected_roles = {
                "cvc5_normalized_formula",
                "cvc5_normalization_record",
                "cvc5_replay_record",
            }
            if set(auxiliary_by_role) != expected_roles:
                raise ValueError(f"{cell}: invalid cvc5 evidence roles")
            normalized = auxiliary_paths["cvc5_normalized_formula"]
            normalization = json.loads(
                auxiliary_paths[
                    "cvc5_normalization_record"
                ].read_text()
            )
            replay = json.loads(
                auxiliary_paths["cvc5_replay_record"].read_text()
            )
            replay_solver = Path(replay.get("solver", "")).resolve()
            replay_solver_hash = replay.get("solver_sha256")
            solver_dependency_matches = [
                dependency
                for dependency in dependencies
                if (
                    dependency.is_file()
                    and dependency.name == replay_solver.name
                    and sha256(dependency) == replay_solver_hash
                )
            ]
            if (
                normalization.get("schema")
                != "strict-smt2-normalization-v1"
                or normalization.get("source_sha256")
                != record["formula_sha256"]
                or normalization.get("output_sha256")
                != sha256(normalized)
                or replay.get("schema") != "external-smt-replay-v1"
                or replay.get("solver_interface") != "cvc5"
                or replay.get("timed_out") is not False
                or replay.get("returncode") != 0
                or replay.get("verdict") != "unsat"
                or replay.get("confirmed_expected") is not True
                or replay.get("formula_sha256") != sha256(normalized)
                or not solver_dependency_matches
            ):
                raise ValueError(f"{cell}: invalid cvc5 replay chain")
    direct_pool = (
        direct_directory / "complete-onto-allocations.json"
    ).resolve()
    require_hash(
        direct_pool,
        direct["pool_sha256"],
        "direct-allocation universe",
    )
    dependencies.add(direct_pool)

    semantic_command = [
        "python3.10",
        str(
            project_root
            / "tracks/parkability/audit_independent_formula_semantics.py"
        ),
        "--root",
        str(root),
        "--lean-root",
        str(lean_root),
    ]
    run_checked(semantic_command, cwd=project_root)
    published_command = [
        "python3.10",
        str(
            project_root
            / "tracks/parkability/audit_published_inputs.py"
        ),
        "--root",
        str(root),
        "--lean-root",
        str(lean_root),
        "--output",
        "literature/PUBLISHED_INPUT_AUDIT.json",
    ]
    run_checked(published_command, cwd=project_root)
    dependencies.update(
        verify_manifest(root, terminal_manifest_path)
    )

    lean_sources, imports = audit_lean_sources(lean_root)
    elan_home = root / "tools" / "elan"
    lake = elan_home / "bin" / "lake"
    environment = os.environ.copy()
    environment["ELAN_HOME"] = str(elan_home)
    version = run_checked(
        [str(lake), "env", "lean", "--version"],
        cwd=lean_root,
        environment=environment,
    )
    build = run_checked(
        [str(lake), "build"],
        cwd=lean_root,
        environment=environment,
    )
    axiom_audit = run_checked(
        [str(lake), "env", "lean", "AxiomAudit.lean"],
        cwd=lean_root,
        environment=environment,
    )
    forbidden_axioms = (
        "sorryAx",
        "native_decide",
        "ofReduceBool",
    )
    if (
        "depends on axioms: "
        "[propext, Classical.choice, Quot.sound]"
        not in axiom_audit.stdout
        or any(
            forbidden in axiom_audit.stdout
            for forbidden in forbidden_axioms
        )
    ):
        raise ValueError(
            "unexpected axiom dependency in final Lean theorem:\n"
            + axiom_audit.stdout
        )
    build_log_path = root / "EFX48_LEAN_BUILD.log"
    build_log = (
        "$ lake env lean --version\n"
        + version.stdout
        + "\n$ lake build\n"
        + build.stdout
        + "\n$ lake env lean AxiomAudit.lean\n"
        + axiom_audit.stdout
    )
    atomic_write(build_log_path, build_log.encode())
    dependencies.add(build_log_path.resolve())

    archive_path = root / "EFX48_PROOF_SOURCES.zip"
    archive_hash = deterministic_source_archive(
        project_root,
        lean_sources,
        archive_path,
    )
    dependencies.add(archive_path.resolve())

    terminal_summary_hash = sha256(terminal_summary_path)
    dependencies.add(terminal_summary_path.resolve())
    result = {
        "schema": "efx48-end-to-end-hybrid-proof-v2",
        "claim": (
            "Every nonnegative additive valuation instance with "
            "four agents and eight goods admits a complete EFX allocation."
        ),
        "formal_theorem": (
            "EFX48.admitsEFX_4x8_of_standard_published_inputs_nonnegative"
        ),
        "status": "verified_hybrid_proof_package",
        "lean": {
            "build_returncode": build.returncode,
            "build_log": str(build_log_path.relative_to(root)),
            "build_log_sha256": sha256(build_log_path),
            "version": version.stdout.strip(),
            "source_archive": str(archive_path.relative_to(root)),
            "source_archive_sha256": archive_hash,
            "source_file_count": len(lean_sources),
            "entrypoint_import_count": len(imports),
            "forbidden_declaration_count": 0,
            "axioms": [
                "propext",
                "Classical.choice",
                "Quot.sound",
            ],
            "native_decide_axiom_dependency": False,
        },
        "terminal_certificates": {
            "summary": str(terminal_summary_path.relative_to(root)),
            "summary_sha256": terminal_summary_hash,
            "manifest": str(terminal_manifest_path.relative_to(root)),
            "all_eight_ethos_checked": True,
            "semantic_binding_all_passed": True,
        },
        "published_inputs": {
            "audit": "literature/PUBLISHED_INPUT_AUDIT.json",
            "audit_sha256": sha256(
                root / "literature" / "PUBLISHED_INPUT_AUDIT.json"
            ),
            "exact_variants_match": True,
            "formalized_from_paper_proofs": False,
        },
        "direct_allocation_crosscheck": {
            "summary": str(direct_summary_path.relative_to(root)),
            "summary_sha256": sha256(direct_summary_path),
            "all_eight_unsat": True,
            "z3_unsat_count": sum(
                record["status"] == "UNSAT_CANDIDATE"
                for record in records.values()
            ),
            "cvc5_replay_unsat_count": sum(
                record["status"] == "UNSAT_CVC5_REPLAY"
                for record in records.values()
            ),
            "onto_allocation_count_per_cell": 40_824,
            "pool_universe_exact": True,
        },
        "deduction_chain": [
            (
                "Mahara Theorem 3 supplies complete EFX for four "
                "agents and seven goods."
            ),
            (
                "Chaudhury-Garg-Mehlhorn Theorem 20 supplies complete "
                "EFX for three additive agents and seven goods."
            ),
            (
                "Lean reduces any nonnegative counterexample to a positive "
                "one by uniform perturbation."
            ),
            (
                "Lean lifts the published inputs and reduces any positive "
                "4x8 counterexample to one of eight terminal cells."
            ),
            (
                "The semantic audit binds each exact SMT formula to its "
                "Lean terminal-cell specification."
            ),
            (
                "cvc5 CPC proofs checked by Ethos establish all eight "
                "terminal formulas unsatisfiable."
            ),
        ],
        "remaining_trust_boundary": [
            "the published mathematical proofs in the two pinned papers",
            "the Lean kernel, pinned toolchain, and mathlib",
            "the Ethos CPC checker implementation",
            (
                "the parser-based semantic binding between SMT syntax "
                "and the Lean terminal specifications"
            ),
        ],
    }
    summary_path = root / "EFX48_END_TO_END_CERTIFICATE.json"
    manifest_path = root / "EFX48_END_TO_END_MANIFEST.sha256"
    result.update(
        {
            "summary": summary_path.name,
            "manifest": manifest_path.name,
            "manifest_entry_count": len(dependencies) + 1,
        }
    )
    atomic_write(
        summary_path,
        (json.dumps(result, indent=2, sort_keys=True) + "\n").encode(),
    )
    dependencies.add(summary_path.resolve())

    manifest_lines = []
    for path in sorted(
        dependencies,
        key=lambda item: str(item.relative_to(root)),
    ):
        manifest_lines.append(
            f"{sha256(path)}  {path.relative_to(root)}"
        )
    atomic_write(
        manifest_path,
        ("\n".join(manifest_lines) + "\n").encode(),
    )
    if result["manifest_entry_count"] != len(manifest_lines):
        raise AssertionError("end-to-end manifest entry count changed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    args = parser.parse_args()
    print(
        json.dumps(
            finalize(args.root, args.project_root),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
