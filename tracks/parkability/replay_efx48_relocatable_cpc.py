#!/usr/bin/env python3
"""Recheck the frozen EFX(4,8) CPC proofs after audited path relocation.

cvc5 writes absolute signature includes into CPC proofs.  This replay copies
one proof at a time, replaces exactly those two leading include lines with
paths under the supplied package root, preserves every remaining byte, and
checks the relocated proof with the package's pinned Ethos binary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path


SIGNATURES = (
    Path("tools/cvc5-1.3.3-source/proofs/eo/cpc/Cpc.eo"),
    Path("tools/cvc5-1.3.3-source/proofs/eo/cpc/expert/CpcExpert.eo"),
)
EXPECTED_CVC5_SOURCE_TAR_SHA256 = (
    "7eeeb65a6c5bfe985a6b3fc7938b87709bbc0e3f72d661b1d0587d4173ad9b33"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
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


def require_hash(path: Path, expected: str, label: str) -> None:
    if not path.is_file():
        raise ValueError(f"{label} is missing: {path}")
    actual = sha256(path)
    if actual != expected:
        raise ValueError(
            f"{label} hash mismatch: expected {expected}, got {actual}"
        )


def include_target(line: bytes) -> Path:
    prefix = b'(include "'
    suffix = b'")\n'
    if not line.startswith(prefix) or not line.endswith(suffix):
        raise ValueError(f"unexpected CPC include line: {line[:160]!r}")
    return Path(line[len(prefix) : -len(suffix)].decode("utf-8"))


def audit_signature_tree(root: Path) -> dict:
    archive = root / "tools/cvc5-1.3.3-source.tar.gz"
    require_hash(
        archive,
        EXPECTED_CVC5_SOURCE_TAR_SHA256,
        "official cvc5 1.3.3 source archive",
    )
    tree = root / "tools/cvc5-1.3.3-source/proofs/eo/cpc"
    actual_files = {
        path.relative_to(tree): path
        for path in tree.rglob("*.eo")
        if path.is_file()
    }
    archived_hashes: dict[Path, str] = {}
    marker = ("proofs", "eo", "cpc")
    with tarfile.open(archive, "r:gz") as source:
        for member in source.getmembers():
            parts = Path(member.name).parts
            if not member.isfile() or not member.name.endswith(".eo"):
                continue
            try:
                index = next(
                    position
                    for position in range(len(parts) - len(marker) + 1)
                    if parts[position : position + len(marker)] == marker
                )
            except StopIteration:
                continue
            relative = Path(*parts[index + len(marker) :])
            extracted = source.extractfile(member)
            if extracted is None or relative in archived_hashes:
                raise ValueError("malformed cvc5 CPC signature archive")
            archived_hashes[relative] = hashlib.sha256(extracted.read()).hexdigest()
    if set(actual_files) != set(archived_hashes):
        raise ValueError("extracted CPC signature tree differs from official archive")
    actual_hashes = {relative: sha256(path) for relative, path in actual_files.items()}
    mismatches = [
        str(relative)
        for relative in sorted(actual_hashes)
        if actual_hashes[relative] != archived_hashes[relative]
    ]
    if mismatches:
        raise ValueError(f"CPC signature files differ from official archive: {mismatches}")
    digest = hashlib.sha256()
    for relative in sorted(actual_hashes):
        digest.update(str(relative).encode("utf-8"))
        digest.update(b"\0")
        digest.update(actual_hashes[relative].encode("ascii"))
        digest.update(b"\n")
    return {
        "official_source_url": (
            "https://github.com/cvc5/cvc5/archive/refs/tags/"
            "cvc5-1.3.3.tar.gz"
        ),
        "source_archive_sha256": EXPECTED_CVC5_SOURCE_TAR_SHA256,
        "signature_file_count": len(actual_hashes),
        "signature_tree_sha256": digest.hexdigest(),
        "all_files_match_official_archive": True,
    }


def relocate_proof(
    source: Path,
    destination: Path,
    signature_paths: tuple[Path, Path],
) -> dict:
    body_digest = hashlib.sha256()
    body_bytes = 0
    with source.open("rb") as input_handle, destination.open("wb") as output_handle:
        original_includes = (input_handle.readline(), input_handle.readline())
        original_targets = tuple(include_target(line) for line in original_includes)
        if tuple(path.name for path in original_targets) != (
            "Cpc.eo",
            "CpcExpert.eo",
        ):
            raise ValueError(f"{source}: unexpected CPC signature includes")
        for signature in signature_paths:
            output_handle.write(f'(include "{signature}")\n'.encode("utf-8"))
        for block in iter(lambda: input_handle.read(1024 * 1024), b""):
            body_digest.update(block)
            body_bytes += len(block)
            output_handle.write(block)
        output_handle.flush()
        os.fsync(output_handle.fileno())
    return {
        "original_include_targets": [str(path) for path in original_targets],
        "relocated_include_targets": [str(path) for path in signature_paths],
        "preserved_body_bytes": body_bytes,
        "preserved_body_sha256": body_digest.hexdigest(),
        "only_two_leading_include_lines_rewritten": True,
    }


def replay(
    root: Path,
    output: Path,
    temp_parent: Path,
    selected_cells: set[str] | None = None,
) -> dict:
    root = root.resolve()
    summary_path = root / "EIGHT_CELL_CPC_CERTIFICATES.json"
    summary = json.loads(summary_path.read_text())
    if summary.get("all_verified") is not True or len(summary.get("cells", [])) != 8:
        raise ValueError("unexpected EFX(4,8) CPC certificate summary")

    ethos = root / "tools/ethos-0.2.3/ethos"
    signature_paths = tuple((root / relative).resolve() for relative in SIGNATURES)
    signature_tree = audit_signature_tree(root)
    available_cells = {cell["cell"] for cell in summary["cells"]}
    selected_cells = selected_cells or available_cells
    unknown_cells = selected_cells - available_cells
    if unknown_cells:
        raise ValueError(f"unknown cells requested: {sorted(unknown_cells)}")
    records = []
    started = time.monotonic()
    with tempfile.TemporaryDirectory(
        prefix="efx48-relocated-cpc-",
        dir=temp_parent,
    ) as temporary:
        temporary_root = Path(temporary)
        for cell in summary["cells"]:
            name = cell["cell"]
            if name not in selected_cells:
                continue
            certificate = json.loads(
                (root / "proofs" / f"{name}.independent.certificate.json").read_text()
            )
            proof = root / cell["proof"]
            require_hash(proof, cell["proof_sha256"], f"{name} proof")
            require_hash(ethos, certificate["ethos_sha256"], "Ethos")
            require_hash(
                signature_paths[0],
                certificate["cpc_signature_sha256"],
                "CPC signature",
            )
            require_hash(
                signature_paths[1],
                certificate["expert_signature_sha256"],
                "CPC expert signature",
            )

            relocated = temporary_root / f"{name}.relocated.cpc"
            transformation = relocate_proof(
                proof,
                relocated,
                signature_paths,
            )
            checked_at = time.monotonic()
            checked = subprocess.run(
                [str(ethos), str(relocated)],
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            verdict = checked.stdout.strip()
            if checked.returncode != 0 or verdict != "correct":
                raise RuntimeError(
                    f"{name}: relocated Ethos replay failed with "
                    f"{checked.returncode}: {checked.stdout}"
                )
            records.append(
                {
                    "cell": name,
                    "original_proof_sha256": cell["proof_sha256"],
                    "relocated_proof_sha256": sha256(relocated),
                    "ethos_seconds": round(time.monotonic() - checked_at, 6),
                    "ethos_verdict": verdict,
                    **transformation,
                }
            )
            atomic_json(
                output,
                {
                    "schema": "efx48-relocatable-cpc-replay-v1",
                    "status": "in_progress",
                    "package_root": str(root),
                    "summary_sha256": sha256(summary_path),
                    "signature_tree": signature_tree,
                    "cell_count": len(records),
                    "all_eight_cells_checked": False,
                    "all_ethos_correct_so_far": True,
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "records": records,
                },
            )

    payload = {
        "schema": "efx48-relocatable-cpc-replay-v1",
        "status": "verified_relocatable_cpc_replay",
        "package_root": str(root),
        "summary_sha256": sha256(summary_path),
        "signature_tree": signature_tree,
        "cell_count": len(records),
        "all_eight_cells_checked": len(records) == 8,
        "all_ethos_correct": True,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "records": records,
    }
    atomic_json(output, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--temp-parent", default=Path(tempfile.gettempdir()), type=Path)
    parser.add_argument("--cell", action="append", dest="cells")
    args = parser.parse_args()
    payload = replay(
        args.root,
        args.output.resolve(),
        args.temp_parent.resolve(),
        set(args.cells) if args.cells else None,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
