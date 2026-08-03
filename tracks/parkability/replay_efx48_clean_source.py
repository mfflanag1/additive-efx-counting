#!/usr/bin/env python3
"""Replay the EFX(4,8) package from its frozen source archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import stat
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path, PurePosixPath


EXPECTED_AXIOMS = "[propext, Classical.choice, Quot.sound]"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> dict:
    started = time.monotonic()
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    record = {
        "command": command,
        "returncode": result.returncode,
        "seconds": round(time.monotonic() - started, 6),
        "stdout": result.stdout,
    }
    if result.returncode != 0:
        raise RuntimeError(json.dumps(record, indent=2))
    return record


def safe_extract(archive_path: Path, destination: Path) -> list[str]:
    names = []
    with zipfile.ZipFile(archive_path) as archive:
        for info in archive.infolist():
            relative = PurePosixPath(info.filename)
            mode = info.external_attr >> 16
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or stat.S_ISLNK(mode)
                or info.is_dir()
            ):
                raise ValueError(f"unsafe source-archive member: {info.filename}")
            names.append(info.filename)
        archive.extractall(destination)
    return sorted(names)


def verify_manifest(root: Path, manifest: Path) -> dict:
    entries = []
    for line_number, line in enumerate(manifest.read_text().splitlines(), start=1):
        expected, separator, relative = line.partition("  ")
        if not separator:
            raise ValueError(f"malformed manifest line {line_number}")
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as error:
            raise ValueError(f"manifest path escapes root: {relative}") from error
        actual = sha256(path)
        if actual != expected:
            raise ValueError(f"manifest mismatch for {relative}")
        entries.append(relative)
    return {
        "entry_count": len(entries),
        "all_hashes_match": True,
        "manifest_sha256": sha256(manifest),
    }


def validate_semantic_audit(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != "independent-formula-semantic-binding-v1"
        or payload.get("all_passed") is not True
        or payload.get("cell_count") != 8
        or payload.get("partition_universe_count") != 1_701
        or payload.get("lean_constant_binding", {}).get("all_passed") is not True
    ):
        raise ValueError("clean semantic audit did not pass")
    return {
        "all_passed": True,
        "cell_count": 8,
        "partition_universe_count": 1_701,
        "output_sha256": sha256(path),
    }


def validate_published_audit(path: Path) -> dict:
    payload = json.loads(path.read_text())
    if (
        payload.get("schema") != "efx48-published-input-audit-v1"
        or payload.get("all_passed") is not True
        or len(payload.get("papers", [])) != 2
    ):
        raise ValueError("clean published-input audit did not pass")
    return {
        "all_passed": True,
        "paper_count": 2,
        "output_sha256": sha256(path),
    }


def recheck_ethos(root: Path) -> list[dict]:
    summary = json.loads((root / "EIGHT_CELL_CPC_CERTIFICATES.json").read_text())
    ethos = root / "tools" / "ethos-0.2.3" / "ethos"
    records = []
    for cell in summary["cells"]:
        proof = root / cell["proof"]
        if sha256(proof) != cell["proof_sha256"]:
            raise ValueError(f"{cell['cell']}: proof hash mismatch")
        checked = run([str(ethos), str(proof)], cwd=root)
        verdict = checked["stdout"].strip()
        if verdict != "correct":
            raise ValueError(f"{cell['cell']}: Ethos returned {verdict!r}")
        records.append(
            {
                "cell": cell["cell"],
                "proof_sha256": cell["proof_sha256"],
                "seconds": checked["seconds"],
                "verdict": verdict,
            }
        )
    return records


def replay(
    *,
    root: Path,
    shared_packages: Path,
    output: Path,
    temp_parent: Path,
    check_ethos: bool,
) -> dict:
    root = root.resolve()
    shared_packages = shared_packages.resolve()
    certificate = json.loads(
        (root / "EFX48_END_TO_END_CERTIFICATE.json").read_text()
    )
    archive = root / certificate["lean"]["source_archive"]
    if sha256(archive) != certificate["lean"]["source_archive_sha256"]:
        raise ValueError("source archive does not match the end-to-end certificate")
    if not shared_packages.is_dir():
        raise ValueError("shared Lean package checkout is missing")

    started = time.monotonic()
    with tempfile.TemporaryDirectory(
        prefix="efx48-clean-source-",
        dir=temp_parent,
    ) as temporary:
        project_root = Path(temporary)
        members = safe_extract(archive, project_root)
        lean_root = project_root / "formal" / "efx48"
        if (lean_root / ".lake").exists():
            raise ValueError("source archive unexpectedly contains a build directory")
        (lean_root / ".lake").mkdir()
        (lean_root / ".lake" / "packages").symlink_to(
            shared_packages,
            target_is_directory=True,
        )

        semantic_output = project_root / "semantic-clean.json"
        semantic_run = run(
            [
                "python3.10",
                "tracks/parkability/audit_independent_formula_semantics.py",
                "--root",
                str(root),
                "--lean-root",
                str(lean_root),
                "--output",
                str(semantic_output),
            ],
            cwd=project_root,
        )
        semantic = validate_semantic_audit(semantic_output)

        published_output = project_root / "published-clean.json"
        published_run = run(
            [
                "python3.10",
                "tracks/parkability/audit_published_inputs.py",
                "--root",
                str(root),
                "--lean-root",
                str(lean_root),
                "--output",
                str(published_output),
            ],
            cwd=project_root,
        )
        published = validate_published_audit(published_output)

        elan_home = root / "tools" / "elan"
        lake = elan_home / "bin" / "lake"
        environment = os.environ.copy()
        environment["ELAN_HOME"] = str(elan_home)
        version = run(
            [str(lake), "env", "lean", "--version"],
            cwd=lean_root,
            env=environment,
        )
        build = run(
            [str(lake), "build"],
            cwd=lean_root,
            env=environment,
        )
        axiom = run(
            [str(lake), "env", "lean", "AxiomAudit.lean"],
            cwd=lean_root,
            env=environment,
        )
        if (
            EXPECTED_AXIOMS not in axiom["stdout"]
            or "sorryAx" in axiom["stdout"]
            or "native_decide" in axiom["stdout"]
            or "ofReduceBool" in axiom["stdout"]
        ):
            raise ValueError("clean-source axiom audit failed")

        payload = {
            "schema": "efx48-clean-source-replay-v1",
            "status": "verified_clean_source_replay",
            "scope": (
                "fresh extraction and fresh project build on the original macOS "
                "host; pinned dependency checkouts are reused by path"
            ),
            "not_claimed": (
                "this is not a second-machine or cross-operating-system replay"
            ),
            "host": {
                "machine": platform.machine(),
                "platform": platform.platform(),
                "python": platform.python_version(),
            },
            "source_archive": str(archive),
            "source_archive_sha256": sha256(archive),
            "source_member_count": len(members),
            "source_archive_excluded_build_directory": True,
            "fresh_project_build_directory": True,
            "shared_packages": str(shared_packages),
            "lake_manifest_sha256": sha256(lean_root / "lake-manifest.json"),
            "end_to_end_manifest": verify_manifest(
                root,
                root / "EFX48_END_TO_END_MANIFEST.sha256",
            ),
            "semantic_audit": semantic,
            "semantic_seconds": semantic_run["seconds"],
            "published_input_audit": published,
            "published_seconds": published_run["seconds"],
            "lean": {
                "version": version["stdout"].strip(),
                "build_returncode": build["returncode"],
                "build_seconds": build["seconds"],
                "axiom_audit_seconds": axiom["seconds"],
                "axioms": [
                    "propext",
                    "Classical.choice",
                    "Quot.sound",
                ],
            },
            "ethos_rechecked": check_ethos,
            "ethos": recheck_ethos(root) if check_ethos else [],
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    atomic_json(output, payload)
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--shared-packages", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--temp-parent", type=Path, default=Path("/private/tmp"))
    parser.add_argument("--recheck-ethos", action="store_true")
    args = parser.parse_args()
    payload = replay(
        root=args.root,
        shared_packages=args.shared_packages,
        output=args.output,
        temp_parent=args.temp_parent,
        check_ethos=args.recheck_ethos,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
