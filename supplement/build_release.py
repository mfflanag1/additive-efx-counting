#!/usr/bin/env python3
"""Build and verify the deterministic main-paper supplementary archive."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import subprocess
import tarfile
import tempfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = "efx-paper-supplement"
MANIFEST_MEMBER = f"{ARCHIVE_ROOT}/RELEASE_MANIFEST.json"
PROFILE_DIRS = (
    "repro/counting_witnesses",
    "artifacts/generalized_parking",
    "repro/countcegar_k4",
)
PROFILE_TREE_FILES = (
    "artifacts/generalized_parking/README.md",
    "artifacts/generalized_parking/certificates.json",
    "artifacts/generalized_parking/verify_certificates.py",
    "repro/countcegar_k4/MANIFEST.json",
    "repro/countcegar_k4/README.md",
    "repro/countcegar_k4/certificates/DRAT_CERTIFICATE.json",
    "repro/countcegar_k4/certificates/cadical-1.9.5.solve.log",
    "repro/countcegar_k4/certificates/countcegar_K4_sat.cadical-1.9.5.binary.drat.xz",
    "repro/countcegar_k4/certificates/drat-trim.verify.log",
    "repro/countcegar_k4/check_sat.py",
    "repro/countcegar_k4/check_z3.py",
    "repro/countcegar_k4/make_manifest.py",
    "repro/countcegar_k4/reconstruct.py",
    "repro/countcegar_k4/replay_sat.py",
    "repro/countcegar_k4/requirements.txt",
    "repro/countcegar_k4/test_sat_differential.py",
    "repro/countcegar_k4/test_slot_boundary.py",
    "repro/countcegar_k4/verify_drat.py",
    "repro/counting_witnesses/README.md",
    "repro/counting_witnesses/instances.json",
    "repro/counting_witnesses/last_run.json",
    "repro/counting_witnesses/requirements.txt",
    "repro/counting_witnesses/verify_all.py",
)
PROFILE_REFERENCE_FILES = (
    "cegar.py",
    "countcegar.py",
    "fast_verify.py",
    "repro/countcegar_k4/README.md",
    "repro/countcegar_k4/certificates/DRAT_CERTIFICATE.json",
    "repro/countcegar_k4/certificates/cadical-1.9.5.solve.log",
    "repro/countcegar_k4/certificates/countcegar_K4_sat.cadical-1.9.5.binary.drat.xz",
    "repro/countcegar_k4/certificates/drat-trim.verify.log",
    "repro/countcegar_k4/check_sat.py",
    "repro/countcegar_k4/check_z3.py",
    "repro/countcegar_k4/make_manifest.py",
    "repro/countcegar_k4/reconstruct.py",
    "repro/countcegar_k4/replay_sat.py",
    "repro/countcegar_k4/requirements.txt",
    "repro/countcegar_k4/test_sat_differential.py",
    "repro/countcegar_k4/test_slot_boundary.py",
    "repro/countcegar_k4/verify_drat.py",
    "results/ch5_A.json",
    "results/countcegar_K4.json",
    "results/countcegar_K4.log",
    "results/countcegar_K4_complete.smt2",
    "results/countcegar_K4_complete_model.pbtxt",
    "results/countcegar_K4_complete_response.pbtxt",
    "results/countcegar_K4_complete_stats.txt",
    "results/countcegar_K4_reconstructed.json",
    "results/countcegar_K4_reconstruction.jsonl",
    "results/countcegar_K4_reconstruction_run.json",
    "results/countcegar_K4_sat.cnf",
    "results/countcegar_K4_sat.json",
    "results/countcegar_K4_sat_differential.json",
    "results/countcegar_K4_sat_replay.json",
    "results/countcegar_K4_z3.json",
    "results/countcegar_slot_boundary.json",
    "results/countpool_K4.json",
    "results/countpool_K4_complete.json",
    "results/t47.json",
    "results/tb4.json",
    "results/tb4b.json",
    "results/tight410_witness.json",
    "results/tight49_witness.json",
    "results/tight69_witness.json",
    "verify.py",
    "verify2.py",
)
PROFILE_FILES = (
    "paper/main.tex",
    "paper/main.pdf",
    "supplement/README.md",
    "supplement/build_release.py",
    "supplement/test_build_release.py",
)
PROFILE_PATHS = tuple(
    sorted(
        set(PROFILE_TREE_FILES)
        | set(PROFILE_REFERENCE_FILES)
        | set(PROFILE_FILES)
    )
)
IGNORED_NAMES = {".DS_Store", "__pycache__"}
IGNORED_SUFFIXES = {".pyc"}
RELEASE_SCOPE = (
    "paper/main.tex and paper/main.pdf; the count-n witnesses; "
    "generalized-parking certificates; and the bounded K=4 "
    "counting-CEGAR result"
)
EXCLUDED_SCRATCH = [
    "repro/countcegar_real",
    "artifacts/efx_chambers",
    "artifacts/multifloater_parking",
]
MANIFEST_NOTE = (
    "RELEASE_MANIFEST.json inventories every other regular archive "
    "member and is excluded from its own non-recursive file list"
)
EXPECTED_EXTERNAL_TOOLS = {
    "proof_generator": {
        "name": "CaDiCaL",
        "version": "1.9.5",
        "repository": "https://github.com/arminbiere/cadical.git",
        "tag": "rel-1.9.5",
        "commit": "146207318796f094dcded87349a64f0c6927309e",
    },
    "proof_checker": {
        "name": "drat-trim",
        "repository": "https://github.com/marijnheule/drat-trim.git",
        "commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
    },
    "python_requirements": [
        "repro/counting_witnesses/requirements.txt",
        "repro/countcegar_k4/requirements.txt",
    ],
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def snapshot_payloads(paths: list[str]) -> dict[str, bytes]:
    return {relative: (ROOT / relative).read_bytes() for relative in paths}


def git_blob_hash(data: bytes, object_format: str) -> str:
    if object_format not in {"sha1", "sha256"}:
        raise ValueError(f"unsupported Git object format: {object_format}")
    digest = hashlib.new(object_format)
    digest.update(f"blob {len(data)}\0".encode())
    digest.update(data)
    return digest.hexdigest()


def snapshot_index_mismatches(
    payloads: dict[str, bytes],
    provenance: dict,
) -> list[str]:
    object_format = provenance.get("git_object_format")
    index_blobs = provenance.get("selected_index_blobs")
    if not isinstance(index_blobs, dict) or not isinstance(object_format, str):
        return sorted(payloads)
    return sorted(
        relative
        for relative, data in payloads.items()
        if index_blobs.get(relative) != git_blob_hash(data, object_format)
    )


def relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe release path: {value}")
    resolved = (ROOT / path).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError as error:
        raise ValueError(f"release path escapes repository: {value}") from error
    return path


def validate_file_record(record: dict) -> str:
    relative = relative_path(record["path"])
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.stat().st_size != record["bytes"]:
        raise ValueError(f"byte-size mismatch for {relative.as_posix()}")
    if sha256_file(path) != record["sha256"]:
        raise ValueError(f"SHA-256 mismatch for {relative.as_posix()}")
    return relative.as_posix()


def recorded_files(value) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        if {"path", "bytes", "sha256"} <= value.keys():
            paths.add(validate_file_record(value))
        for child in value.values():
            paths.update(recorded_files(child))
    elif isinstance(value, list):
        for child in value:
            paths.update(recorded_files(child))
    return paths


def validate_sha_path(path_value: str, expected_hash: str) -> str:
    relative = relative_path(path_value)
    path = ROOT / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    if sha256_file(path) != expected_hash:
        raise ValueError(f"SHA-256 mismatch for {relative.as_posix()}")
    return relative.as_posix()


def manifest_references() -> set[str]:
    paths: set[str] = set()

    k4_path = ROOT / "repro/countcegar_k4/MANIFEST.json"
    paths.update(recorded_files(json.loads(k4_path.read_text())))

    witness_path = ROOT / "repro/counting_witnesses/instances.json"
    witnesses = json.loads(witness_path.read_text())
    for verifier, expected_hash in witnesses["verifiers"].items():
        paths.add(validate_sha_path(verifier, expected_hash))
    for instance in witnesses["instances"]:
        paths.add(validate_sha_path(instance["path"], instance["sha256"]))

    parking_path = ROOT / "artifacts/generalized_parking/certificates.json"
    parking = json.loads(parking_path.read_text())
    for witness in parking["witnesses"]:
        paths.add(
            validate_sha_path(witness["source"], witness["source_sha256"])
        )
    return paths


def tree_files(relative_directory: str) -> set[str]:
    directory = ROOT / relative_path(relative_directory)
    if not directory.is_dir():
        raise FileNotFoundError(directory)
    if directory.is_symlink():
        raise ValueError(f"profile directory is a symlink: {directory}")
    paths: set[str] = set()
    for path in directory.rglob("*"):
        if any(part in IGNORED_NAMES for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix in IGNORED_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"symlinks are not allowed in release: {path}")
        if path.is_file():
            paths.add(path.relative_to(ROOT).as_posix())
    return paths


def selected_paths() -> list[str]:
    expected_tree = set(PROFILE_TREE_FILES)
    actual_tree: set[str] = set()
    for directory in PROFILE_DIRS:
        actual_tree.update(tree_files(directory))
    if actual_tree != expected_tree:
        raise ValueError(
            "claim-bearing tree differs from the release profile: "
            f"missing={sorted(expected_tree - actual_tree)}, "
            f"unexpected={sorted(actual_tree - expected_tree)}"
        )

    references = manifest_references()
    expected_references = set(PROFILE_REFERENCE_FILES)
    if references != expected_references:
        raise ValueError(
            "nested manifests differ from the release profile: "
            f"missing={sorted(expected_references - references)}, "
            f"unexpected={sorted(references - expected_references)}"
        )

    paths = set(PROFILE_FILES) | actual_tree | references
    if paths != set(PROFILE_PATHS):
        raise AssertionError("internal release-profile inconsistency")
    for value in PROFILE_PATHS:
        path = ROOT / relative_path(value)
        if not path.is_file():
            raise FileNotFoundError(path)
        if path.is_symlink():
            raise ValueError(f"release file is a symlink: {path}")
    return list(PROFILE_PATHS)


def git_provenance(paths: list[str]) -> dict:
    try:
        head = subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        object_format = subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "rev-parse",
                "--show-object-format",
            ],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        status = subprocess.check_output(
            [
                "git",
                "-C",
                str(ROOT),
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                *paths,
            ],
            text=True,
        ).splitlines()
        tracked = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "--", *paths],
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        stage_lines = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "--stage", "--", *paths],
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        working_hashes = subprocess.check_output(
            ["git", "-C", str(ROOT), "hash-object", "--", *paths],
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return {
            "available": False,
            "head": None,
            "selected_status": None,
            "all_selected_tracked": None,
            "untracked_selected": None,
            "index_matches_worktree": None,
            "index_mismatches": None,
            "git_object_format": None,
            "selected_index_blobs": None,
        }
    untracked = sorted(set(paths) - set(tracked))
    if len(working_hashes) != len(paths):
        raise RuntimeError("Git did not hash every selected release path")
    index_blobs = {}
    for line in stage_lines:
        metadata, path = line.split("\t", 1)
        _mode, blob, stage = metadata.split()
        if stage == "0":
            index_blobs[path] = blob
    working_blobs = dict(zip(paths, working_hashes))
    mismatches = sorted(
        path
        for path in paths
        if index_blobs.get(path) != working_blobs[path]
    )
    return {
        "available": True,
        "head": head,
        "selected_status": status,
        "all_selected_tracked": not untracked,
        "untracked_selected": untracked,
        "index_matches_worktree": not mismatches,
        "index_mismatches": mismatches,
        "git_object_format": object_format,
        "selected_index_blobs": {
            path: index_blobs[path]
            for path in paths
            if path in index_blobs
        },
    }


def external_tools() -> dict:
    certificate = json.loads(
        (
            ROOT
            / "repro/countcegar_k4/certificates/DRAT_CERTIFICATE.json"
        ).read_text()
    )
    generator = certificate["generator"]
    checker = certificate["checker"]
    result = {
        "proof_generator": {
            key: generator[key]
            for key in ("name", "version", "repository", "tag", "commit")
        },
        "proof_checker": {
            key: checker[key] for key in ("name", "repository", "commit")
        },
        "python_requirements": [
            "repro/counting_witnesses/requirements.txt",
            "repro/countcegar_k4/requirements.txt",
        ],
    }
    if result != EXPECTED_EXTERNAL_TOOLS:
        raise ValueError("certificate tool pins differ from the release profile")
    return result


def release_manifest(
    paths: list[str],
    provenance: dict,
    payloads: dict[str, bytes],
) -> dict:
    if paths != list(PROFILE_PATHS):
        raise ValueError("release paths do not match the main-paper profile")
    if list(payloads) != paths:
        raise ValueError("payload snapshot does not match release paths")
    records = []
    for relative in paths:
        data = payloads[relative]
        records.append(
            {
                "path": relative,
                "bytes": len(data),
                "sha256": sha256_bytes(data),
            }
        )
    return {
        "schema": 1,
        "profile": "main-paper",
        "archive_root": ARCHIVE_ROOT,
        "scope": RELEASE_SCOPE,
        "excluded_scratch": EXCLUDED_SCRATCH,
        "manifest_note": MANIFEST_NOTE,
        "git": provenance,
        "external_tools": external_tools(),
        "files": records,
    }


def manifest_bytes(manifest: dict) -> bytes:
    return (
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True) + "\n"
    ).encode()


def validate_release_manifest(manifest: object) -> list[dict]:
    if not isinstance(manifest, dict) or set(manifest) != {
        "schema",
        "profile",
        "archive_root",
        "scope",
        "excluded_scratch",
        "manifest_note",
        "git",
        "external_tools",
        "files",
    }:
        raise ValueError("unexpected release-manifest fields")
    if (
        manifest["schema"] != 1
        or manifest["profile"] != "main-paper"
        or manifest["archive_root"] != ARCHIVE_ROOT
        or manifest["scope"] != RELEASE_SCOPE
        or manifest["excluded_scratch"] != EXCLUDED_SCRATCH
        or manifest["manifest_note"] != MANIFEST_NOTE
    ):
        raise ValueError("release manifest does not name the expected profile")
    provenance = manifest["git"]
    if not isinstance(provenance, dict) or set(provenance) != {
        "available",
        "head",
        "selected_status",
        "all_selected_tracked",
        "untracked_selected",
        "index_matches_worktree",
        "index_mismatches",
        "git_object_format",
        "selected_index_blobs",
    }:
        raise ValueError("invalid Git provenance record")
    if (
        type(provenance["available"]) is not bool
        or (
            provenance["head"] is not None
            and type(provenance["head"]) is not str
        )
        or (
            provenance["selected_status"] is not None
            and (
                not isinstance(provenance["selected_status"], list)
                or any(
                    type(value) is not str
                    for value in provenance["selected_status"]
                )
            )
        )
        or (
            provenance["all_selected_tracked"] is not None
            and type(provenance["all_selected_tracked"]) is not bool
        )
        or (
            provenance["untracked_selected"] is not None
            and (
                not isinstance(provenance["untracked_selected"], list)
                or any(
                    type(value) is not str
                    for value in provenance["untracked_selected"]
                )
            )
        )
        or (
            provenance["index_matches_worktree"] is not None
            and type(provenance["index_matches_worktree"]) is not bool
        )
        or (
            provenance["index_mismatches"] is not None
            and (
                not isinstance(provenance["index_mismatches"], list)
                or any(
                    type(value) is not str
                    for value in provenance["index_mismatches"]
                )
            )
        )
        or (
            provenance["git_object_format"] is not None
            and provenance["git_object_format"] not in {"sha1", "sha256"}
        )
        or (
            provenance["selected_index_blobs"] is not None
            and (
                not isinstance(provenance["selected_index_blobs"], dict)
                or any(
                    type(path) is not str
                    or type(blob) is not str
                    or len(blob)
                    not in {
                        40,
                        64,
                    }
                    for path, blob in provenance[
                        "selected_index_blobs"
                    ].items()
                )
            )
        )
    ):
        raise ValueError("invalid Git provenance values")
    if manifest["external_tools"] != EXPECTED_EXTERNAL_TOOLS:
        raise ValueError("release manifest has unexpected external-tool pins")
    records = manifest["files"]
    if not isinstance(records, list):
        raise ValueError("manifest files must be a list")
    paths = []
    for record in records:
        if not isinstance(record, dict) or set(record) != {
            "path",
            "bytes",
            "sha256",
        }:
            raise ValueError(f"invalid manifest record: {record}")
        if (
            type(record["path"]) is not str
            or type(record["bytes"]) is not int
            or record["bytes"] < 0
            or type(record["sha256"]) is not str
            or len(record["sha256"]) != 64
            or any(
                character not in "0123456789abcdef"
                for character in record["sha256"]
            )
        ):
            raise ValueError(f"invalid manifest record: {record}")
        paths.append(record["path"])
    if paths != list(PROFILE_PATHS):
        raise ValueError(
            "manifest inventory does not equal the main-paper profile"
        )
    return records


def add_bytes(archive: tarfile.TarFile, name: str, data: bytes) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = 0o644
    info.mtime = 0
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    archive.addfile(info, io.BytesIO(data))


def write_archive(
    path: Path,
    paths: list[str],
    release_bytes: bytes,
    payloads: dict[str, bytes],
) -> None:
    if list(payloads) != paths:
        raise ValueError("payload snapshot does not match release paths")
    with tarfile.open(
        path,
        mode="w:xz",
        format=tarfile.PAX_FORMAT,
        preset=9,
    ) as archive:
        add_bytes(archive, MANIFEST_MEMBER, release_bytes)
        for relative in paths:
            add_bytes(
                archive,
                f"{ARCHIVE_ROOT}/{relative}",
                payloads[relative],
            )


def safe_member_name(name: str) -> bool:
    if "\\" in name or "\x00" in name:
        return False
    raw_parts = name.split("/")
    if any(part in {"", ".", ".."} for part in raw_parts):
        return False
    path = PurePosixPath(name)
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and path.parts
        and path.parts[0] == ARCHIVE_ROOT
    )


def verify_archive(path: Path, expected_manifest: bytes) -> dict:
    manifest = json.loads(expected_manifest)
    records = validate_release_manifest(manifest)
    expected_records = {}
    for record in records:
        relative = PurePosixPath(record["path"])
        if (
            relative.is_absolute()
            or ".." in relative.parts
            or not relative.parts
        ):
            raise ValueError(f"invalid manifest record: {record}")
        member_name = f"{ARCHIVE_ROOT}/{relative.as_posix()}"
        if member_name in expected_records:
            raise ValueError(f"duplicate manifest path: {record['path']}")
        expected_records[member_name] = record
    expected_order = [MANIFEST_MEMBER] + [
        f"{ARCHIVE_ROOT}/{relative}" for relative in PROFILE_PATHS
    ]
    expected_names = set(expected_order)
    seen: set[str] = set()
    seen_order = []
    with tarfile.open(path, mode="r:xz") as archive:
        for member in archive:
            if not safe_member_name(member.name):
                raise ValueError(f"unsafe archive member: {member.name}")
            if (
                len(seen_order) >= len(expected_order)
                or member.name != expected_order[len(seen_order)]
            ):
                raise ValueError(
                    f"non-canonical archive member order: {member.name}"
                )
            if member.name in seen:
                raise ValueError(f"duplicate archive member: {member.name}")
            seen.add(member.name)
            seen_order.append(member.name)
            if member.type != tarfile.REGTYPE:
                raise ValueError(f"non-regular archive member: {member.name}")
            if (
                member.mtime != 0
                or member.uid != 0
                or member.gid != 0
                or member.mode != 0o644
                or member.uname != ""
                or member.gname != ""
                or member.linkname != ""
                or member.devmajor != 0
                or member.devminor != 0
                or member.pax_headers
            ):
                raise ValueError(f"non-canonical metadata: {member.name}")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise ValueError(f"cannot read archive member: {member.name}")
            data = extracted.read()
            if member.name == MANIFEST_MEMBER:
                if data != expected_manifest:
                    raise ValueError("embedded and sidecar manifests differ")
                continue
            record = expected_records.get(member.name)
            if record is None:
                raise ValueError(f"unmanifested archive member: {member.name}")
            if len(data) != record["bytes"]:
                raise ValueError(f"byte-size mismatch: {member.name}")
            if sha256_bytes(data) != record["sha256"]:
                raise ValueError(f"SHA-256 mismatch: {member.name}")
    if seen != expected_names:
        missing = sorted(expected_names - seen)
        extra = sorted(seen - expected_names)
        raise ValueError(f"archive inventory mismatch: missing={missing}, extra={extra}")
    if seen_order != expected_order:
        raise ValueError("archive member order is incomplete")
    return {
        "status": "PASS",
        "archive": str(path),
        "archive_bytes": path.stat().st_size,
        "archive_sha256": sha256_file(path),
        "payload_files": len(expected_records),
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
        os.replace(temporary, path)
    except BaseException:
        os.unlink(temporary)
        raise


def build(args) -> None:
    archive_path = args.archive.resolve()
    manifest_path = args.manifest.resolve()
    if archive_path == manifest_path:
        raise ValueError("archive and manifest output paths must differ")
    root = ROOT.resolve()
    if (
        archive_path == root
        or root in archive_path.parents
        or manifest_path == root
        or root in manifest_path.parents
    ):
        raise ValueError("release outputs must be outside the source tree")
    paths = selected_paths()
    provenance = git_provenance(paths)
    if not args.allow_dirty:
        if not provenance["available"]:
            raise RuntimeError(
                "git provenance is unavailable; use --allow-dirty only for "
                "an explicitly non-release development build"
            )
        if provenance["selected_status"] or not provenance[
            "all_selected_tracked"
        ] or not provenance[
            "index_matches_worktree"
        ]:
            details = list(provenance["selected_status"])
            if provenance["untracked_selected"]:
                details.append(
                    "not tracked: "
                    + ", ".join(provenance["untracked_selected"])
                )
            if provenance["index_mismatches"]:
                details.append(
                    "differs from index: "
                    + ", ".join(provenance["index_mismatches"])
                )
            raise RuntimeError(
                "selected release files are modified, deleted, or untracked:\n"
                + "\n".join(details)
            )
    payloads = snapshot_payloads(paths)
    if not args.allow_dirty:
        snapshot_mismatches = snapshot_index_mismatches(
            payloads,
            provenance,
        )
        if snapshot_mismatches:
            raise RuntimeError(
                "payload snapshot differs from the initial Git index: "
                + ", ".join(snapshot_mismatches)
            )
    manifest = release_manifest(paths, provenance, payloads)
    release_bytes = manifest_bytes(manifest)

    archive_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=archive_path.name + ".", dir=archive_path.parent
    )
    os.close(descriptor)
    temporary_path = Path(temporary)
    try:
        write_archive(temporary_path, paths, release_bytes, payloads)
        result = verify_archive(temporary_path, release_bytes)
        final_paths = selected_paths()
        if final_paths != paths:
            raise RuntimeError("release profile changed during build")
        if not args.allow_dirty:
            final_provenance = git_provenance(paths)
            if final_provenance != provenance or final_provenance[
                "selected_status"
            ] or not final_provenance[
                "all_selected_tracked"
            ] or not final_provenance["index_matches_worktree"]:
                raise RuntimeError(
                    "selected release files or Git provenance changed during build"
                )
        os.replace(temporary_path, archive_path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
    atomic_write(manifest_path, release_bytes)
    result["archive"] = str(archive_path)
    result["manifest"] = str(manifest_path)
    result["selected_git_clean"] = bool(
        provenance.get("available")
        and not provenance.get("selected_status")
        and provenance.get("all_selected_tracked")
        and provenance.get("index_matches_worktree")
    )
    print(json.dumps(result, indent=2, sort_keys=True))


def verify(args) -> None:
    expected_manifest = args.manifest.read_bytes()
    manifest = json.loads(expected_manifest)
    validate_release_manifest(manifest)
    print(
        json.dumps(
            verify_archive(args.archive, expected_manifest),
            indent=2,
            sort_keys=True,
        )
    )


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--archive", type=Path, required=True)
    build_parser.add_argument("--manifest", type=Path, required=True)
    build_parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="permit a development archive from modified or untracked inputs",
    )
    build_parser.set_defaults(function=build)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--archive", type=Path, required=True)
    verify_parser.add_argument("--manifest", type=Path, required=True)
    verify_parser.set_defaults(function=verify)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    try:
        arguments.function(arguments)
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        raise SystemExit(f"ERROR: {error}") from error
