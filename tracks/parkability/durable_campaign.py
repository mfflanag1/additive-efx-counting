#!/usr/bin/env python3
"""Run the fixed K=4 parkability campaign with an auditable resume chain."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import AbstractContextManager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


CAMPAIGN_SCHEMA = "parkability-durable-campaign-v1"
SESSION_START_SCHEMA = "parkability-durable-session-start-v1"
SESSION_PROCESS_SCHEMA = "parkability-durable-session-process-v1"
SESSION_END_SCHEMA = "parkability-durable-session-end-v1"
POOL_SCHEMA = "parkable-deletion-pool-v1"
RESULT_SCHEMA = "parkable-deletion-cegar-result-v1"
PROPERTY = "zero_parkable_deletion_triples"
TERMINAL_CHILD_STATUSES = frozenset({"UNSAT_CANDIDATE", "ZERO_PARKABLE_TRIPLES"})
KNOWN_CHILD_STATUSES = TERMINAL_CHILD_STATUSES | frozenset(
    {"MASTER_UNKNOWN", "ITERATION_LIMIT"}
)
FIXED_CONFIG: dict[str, object] = {
    "n": 4,
    "m": 8,
    "lower": 1,
    "upper": 4,
    "symmetry": "none",
    "add_per_iteration": 32,
    "time_limit_seconds_per_master": 3600.0,
    "workers": 6,
    "random_seed": 1,
    "max_iterations": 0,
}
ROOT_ENTRIES = frozenset({".campaign.lock", "campaign.json", "pool.json", "sessions"})
SESSION_ENTRIES = frozenset(
    {
        "start.json",
        "process.json",
        "end.json",
        "pool.before.json",
        "pool.after.json",
        "result.json",
        "trace.jsonl",
        "child.log",
    }
)
ARTIFACT_NAMES = {
    "pool_before": "pool.before.json",
    "pool_after": "pool.after.json",
    "process": "process.json",
    "result": "result.json",
    "trace": "trace.jsonl",
    "log": "child.log",
}


class CampaignError(RuntimeError):
    """The campaign archive or requested execution is invalid."""


class CampaignAlreadyRunning(CampaignError):
    """Another process holds the campaign lock."""


class TerminalCampaign(CampaignError):
    """A terminal CEGAR result already exists."""


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .isoformat(timespec="microseconds")
        .replace("+00:00", "Z")
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def _regular_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise CampaignError(f"expected a regular file: {path}")
    return path.read_bytes()


def artifact_record(path: Path) -> dict[str, object] | None:
    if not path.exists():
        if path.is_symlink():
            raise CampaignError(f"artifact is a dangling symlink: {path}")
        return None
    payload = _regular_bytes(path)
    return {
        "path": path.name,
        "size_bytes": len(payload),
        "sha256": sha256_bytes(payload),
    }


def atomic_write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="wb",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    temporary.replace(path)


def atomic_write_json(path: Path, value: object) -> None:
    atomic_write_bytes(path, json_bytes(value))


def atomic_snapshot(source: Path, destination: Path) -> None:
    atomic_write_bytes(destination, _regular_bytes(source))


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(_regular_bytes(path))
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise CampaignError(f"invalid JSON in {path}: {error}") from error
    if not isinstance(value, dict):
        raise CampaignError(f"expected a JSON object in {path}")
    return value


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def validate_pool_document(document: dict[str, Any]) -> None:
    expected = {
        "schema": POOL_SCHEMA,
        "property": PROPERTY,
        "n": FIXED_CONFIG["n"],
        "m": FIXED_CONFIG["m"],
        "lower": FIXED_CONFIG["lower"],
        "upper": FIXED_CONFIG["upper"],
        "symmetry": FIXED_CONFIG["symmetry"],
    }
    expected_fields = set(expected) | {"triples"}
    if set(document) != expected_fields:
        raise CampaignError(
            "pool fields differ from the exact schema: "
            f"{sorted(set(document) ^ expected_fields)}"
        )
    for field, expected_value in expected.items():
        if document[field] != expected_value:
            raise CampaignError(
                f"pool field {field!r} is {document[field]!r}, "
                f"expected {expected_value!r}"
            )
    triples = document["triples"]
    if not isinstance(triples, list):
        raise CampaignError("pool triples must be a JSON list")
    seen: set[tuple[int, tuple[int | None, ...], int]] = set()
    for index, triple in enumerate(triples):
        if not isinstance(triple, dict) or set(triple) != {
            "floater",
            "base_owner",
            "host",
        }:
            raise CampaignError(f"pool triple {index} has invalid fields")
        floater = triple["floater"]
        host = triple["host"]
        owners = triple["base_owner"]
        if not _is_int(floater) or not 0 <= floater < 8:
            raise CampaignError(f"pool triple {index} has invalid floater")
        if not _is_int(host) or not 0 <= host < 4:
            raise CampaignError(f"pool triple {index} has invalid host")
        if not isinstance(owners, list) or len(owners) != 8:
            raise CampaignError(f"pool triple {index} has invalid base_owner")
        for good, owner in enumerate(owners):
            if good == floater:
                if owner is not None:
                    raise CampaignError(
                        f"pool triple {index} is not null at its floater"
                    )
            elif not _is_int(owner) or not 0 <= owner < 4:
                raise CampaignError(
                    f"pool triple {index} has invalid owner at good {good}"
                )
        key = (floater, tuple(owners), host)
        if key in seen:
            raise CampaignError(f"pool triple {index} is duplicated")
        seen.add(key)


def read_valid_pool(path: Path) -> dict[str, Any]:
    document = read_json(path)
    validate_pool_document(document)
    return document


def empty_pool_document() -> dict[str, object]:
    return {
        "schema": POOL_SCHEMA,
        "property": PROPERTY,
        "n": FIXED_CONFIG["n"],
        "m": FIXED_CONFIG["m"],
        "lower": FIXED_CONFIG["lower"],
        "upper": FIXED_CONFIG["upper"],
        "symmetry": FIXED_CONFIG["symmetry"],
        "triples": [],
    }


def _run_text(command: list[str], cwd: Path | None = None) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", None) or str(error)
        raise CampaignError(f"command failed: {command!r}: {detail.strip()}") from error
    return completed.stdout.strip()


def _redact_remote(remote: str) -> str:
    parsed = urlsplit(remote)
    if not parsed.scheme or parsed.hostname is None:
        return remote
    host = parsed.hostname
    if parsed.port is not None:
        host = f"{host}:{parsed.port}"
    return urlunsplit((parsed.scheme, host, parsed.path, "", ""))


def resolve_interpreter(interpreter: Path | str) -> Path:
    raw = os.fspath(interpreter)
    resolved = shutil.which(raw) if os.sep not in raw else None
    # Preserve virtual-environment launcher symlinks: resolving one selects the
    # base interpreter and silently drops the environment's site-packages.
    path = Path(resolved or raw).expanduser().absolute()
    if not path.is_file():
        raise CampaignError(f"Python interpreter does not exist: {path}")
    return path


def collect_runtime_identity(
    repo_root: Path,
    runner_path: Path,
    interpreter: Path | str,
) -> dict[str, object]:
    repo_root = repo_root.resolve()
    runner_path = runner_path.resolve()
    interpreter_path = resolve_interpreter(interpreter)
    discovered_root = Path(
        _run_text(["git", "rev-parse", "--show-toplevel"], cwd=repo_root)
    ).resolve()
    if discovered_root != repo_root:
        raise CampaignError(
            f"repo root is {repo_root}, but git reports {discovered_root}"
        )
    if not runner_path.is_relative_to(repo_root):
        raise CampaignError("the CEGAR runner must be inside the source repository")
    runner_payload = _regular_bytes(runner_path)
    dirty = _run_text(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=repo_root,
    )
    if dirty:
        raise CampaignError("source repository is not clean")
    commit = _run_text(["git", "rev-parse", "HEAD"], cwd=repo_root)
    remote = _run_text(["git", "remote", "get-url", "origin"], cwd=repo_root)
    probe = """
import importlib.metadata as metadata
import json
import platform
import sys

def version(name):
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None

print(json.dumps({
    "executable": sys.executable,
    "implementation": platform.python_implementation(),
    "python_version": platform.python_version(),
    "platform": platform.platform(),
    "dependencies": {
        "ortools": version("ortools"),
        "python-sat": version("python-sat"),
    },
}, sort_keys=True))
"""
    try:
        interpreter_data = json.loads(
            _run_text([str(interpreter_path), "-c", probe], cwd=repo_root)
        )
    except json.JSONDecodeError as error:
        raise CampaignError(
            "interpreter metadata probe returned invalid JSON"
        ) from error
    if interpreter_data["dependencies"]["ortools"] is None:
        raise CampaignError("campaign interpreter does not provide ortools")
    return {
        "source": {
            "repo_root": str(repo_root),
            "commit_sha": commit,
            "remote": _redact_remote(remote),
            "clean": True,
        },
        "runner": {
            "path": str(runner_path.relative_to(repo_root)),
            "sha256": sha256_bytes(runner_payload),
        },
        "interpreter": {
            "path": str(interpreter_path),
            "reported_executable": interpreter_data["executable"],
            "implementation": interpreter_data["implementation"],
            "python_version": interpreter_data["python_version"],
            "platform": interpreter_data["platform"],
        },
        "dependencies": interpreter_data["dependencies"],
    }


def _ensure_external_root(root: Path, repo_root: Path) -> None:
    root = root.resolve()
    repo_root = repo_root.resolve()
    if (
        root == repo_root
        or root.is_relative_to(repo_root)
        or repo_root.is_relative_to(root)
    ):
        raise CampaignError("campaign root must be external to the source repository")


class CampaignLock(AbstractContextManager["CampaignLock"]):
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.handle: Any = None

    def __enter__(self) -> CampaignLock:
        self.root.mkdir(parents=True, exist_ok=True)
        lock_path = self.root / ".campaign.lock"
        if lock_path.is_symlink():
            raise CampaignError("campaign lock path cannot be a symlink")
        self.handle = lock_path.open("a+")
        try:
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            self.handle.close()
            self.handle = None
            raise CampaignAlreadyRunning(
                f"campaign is already running: {self.root}"
            ) from error
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        del exc_type, exc, traceback
        assert self.handle is not None
        fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        self.handle.close()
        self.handle = None


def _campaign_paths(root: Path) -> dict[str, Path]:
    return {
        "metadata": root / "campaign.json",
        "pool": root / "pool.json",
        "sessions": root / "sessions",
    }


def initialize_campaign(
    root: Path,
    repo_root: Path,
    runner_path: Path,
    interpreter: Path | str,
) -> dict[str, Any]:
    root = root.resolve()
    repo_root = repo_root.resolve()
    _ensure_external_root(root, repo_root)
    paths = _campaign_paths(root)
    if paths["metadata"].exists():
        return read_json(paths["metadata"])
    unexpected = {path.name for path in root.iterdir()} - {".campaign.lock"}
    if unexpected:
        raise CampaignError(
            f"refusing to initialize nonempty campaign root: {sorted(unexpected)}"
        )
    identity = collect_runtime_identity(repo_root, runner_path, interpreter)
    paths["sessions"].mkdir()
    atomic_write_json(paths["pool"], empty_pool_document())
    initial_pool = artifact_record(paths["pool"])
    assert initial_pool is not None
    campaign = {
        "schema": CAMPAIGN_SCHEMA,
        "property": PROPERTY,
        "created_at_utc": utc_now(),
        "config": FIXED_CONFIG,
        "identity": identity,
        "initial_pool": initial_pool,
    }
    atomic_write_json(paths["metadata"], campaign)
    return campaign


def validate_campaign_metadata(campaign: dict[str, Any]) -> None:
    expected_fields = {
        "schema",
        "property",
        "created_at_utc",
        "config",
        "identity",
        "initial_pool",
    }
    if set(campaign) != expected_fields:
        raise CampaignError("campaign metadata fields differ from the exact schema")
    if campaign["schema"] != CAMPAIGN_SCHEMA or campaign["property"] != PROPERTY:
        raise CampaignError("campaign metadata schema or property is invalid")
    if campaign["config"] != FIXED_CONFIG:
        raise CampaignError("campaign fixed configuration changed")
    identity = campaign["identity"]
    if not isinstance(identity, dict) or set(identity) != {
        "source",
        "runner",
        "interpreter",
        "dependencies",
    }:
        raise CampaignError("campaign runtime identity is invalid")
    source = identity["source"]
    runner = identity["runner"]
    interpreter = identity["interpreter"]
    dependencies = identity["dependencies"]
    if (
        not isinstance(source, dict)
        or set(source) != {"repo_root", "commit_sha", "remote", "clean"}
        or source["clean"] is not True
        or not isinstance(runner, dict)
        or set(runner) != {"path", "sha256"}
        or not isinstance(interpreter, dict)
        or set(interpreter)
        != {
            "path",
            "reported_executable",
            "implementation",
            "python_version",
            "platform",
        }
        or not isinstance(dependencies, dict)
        or set(dependencies) != {"ortools", "python-sat"}
    ):
        raise CampaignError("campaign runtime identity fields are invalid")
    expected_initial_payload = json_bytes(empty_pool_document())
    expected_initial = {
        "path": "pool.json",
        "size_bytes": len(expected_initial_payload),
        "sha256": sha256_bytes(expected_initial_payload),
    }
    if campaign["initial_pool"] != expected_initial:
        raise CampaignError("campaign initial pool binding is invalid")


def _verify_artifact_record(
    directory: Path,
    label: str,
    record: object,
    required: bool,
) -> Path | None:
    expected_path = directory / ARTIFACT_NAMES[label]
    if record is None:
        if required:
            raise CampaignError(f"required {label} artifact is absent")
        if expected_path.exists() or expected_path.is_symlink():
            raise CampaignError(f"unrecorded {label} artifact is present")
        return None
    if not isinstance(record, dict) or set(record) != {
        "path",
        "size_bytes",
        "sha256",
    }:
        raise CampaignError(f"{label} artifact record is invalid")
    path_name = record["path"]
    if path_name != ARTIFACT_NAMES[label]:
        raise CampaignError(f"{label} artifact path is invalid")
    path = expected_path
    actual = artifact_record(path)
    if actual != record:
        raise CampaignError(f"{label} artifact hash or size mismatch")
    return path


def validate_child_result(
    path: Path,
    pool_snapshot_path: Path,
    trace_path: Path,
    starting_pool_size: int,
    recorded_pool_path: Path | None = None,
) -> dict[str, Any]:
    result = read_json(path)
    required = {
        "schema": RESULT_SCHEMA,
        "property": PROPERTY,
        "n": FIXED_CONFIG["n"],
        "m": FIXED_CONFIG["m"],
        "lower": FIXED_CONFIG["lower"],
        "upper": FIXED_CONFIG["upper"],
        "symmetry": FIXED_CONFIG["symmetry"],
    }
    for field, expected in required.items():
        if result.get(field) != expected:
            raise CampaignError(
                f"child result field {field!r} is invalid: {result.get(field)!r}"
            )
    status = result.get("status")
    if status not in KNOWN_CHILD_STATUSES:
        raise CampaignError(f"child result has unknown status: {status!r}")
    pool_payload = _regular_bytes(pool_snapshot_path)
    if result.get("pool_sha256") != sha256_bytes(pool_payload):
        raise CampaignError("child result does not bind the current pool bytes")
    result_pool_path = result.get("pool_path")
    expected_recorded_pool_path = recorded_pool_path or pool_snapshot_path
    if (
        not isinstance(result_pool_path, str)
        or Path(result_pool_path).resolve() != expected_recorded_pool_path.resolve()
    ):
        raise CampaignError("child result records a different pool path")
    trace_record = artifact_record(trace_path)
    expected_trace_hash = trace_record["sha256"] if trace_record is not None else None
    if result.get("trace_sha256") != expected_trace_hash:
        raise CampaignError("child result trace hash is invalid")
    expected_trace_path = (
        str(trace_path.resolve()) if trace_record is not None else None
    )
    if result.get("trace_path") != expected_trace_path:
        raise CampaignError("child result trace path is invalid")
    pool_document = read_valid_pool(pool_snapshot_path)
    if result.get("pool_size") != len(pool_document["triples"]):
        raise CampaignError("child result pool size is invalid")
    if not _is_int(result.get("iterations")) or result["iterations"] < 1:
        raise CampaignError("child result iteration count is invalid")
    run_config = result.get("run_config")
    expected_run_config = {
        "add_per_iteration": FIXED_CONFIG["add_per_iteration"],
        "time_limit_seconds_per_master": FIXED_CONFIG["time_limit_seconds_per_master"],
        "workers": FIXED_CONFIG["workers"],
        "random_seed": FIXED_CONFIG["random_seed"],
        "max_iterations": FIXED_CONFIG["max_iterations"],
        "starting_pool_size": starting_pool_size,
    }
    if not isinstance(run_config, dict):
        raise CampaignError("child result run_config is missing")
    for field, expected in expected_run_config.items():
        if run_config.get(field) != expected:
            raise CampaignError(
                f"child run_config field {field!r} is invalid: "
                f"{run_config.get(field)!r}"
            )
    return result


def _session_directories(sessions_path: Path) -> list[Path]:
    if sessions_path.is_symlink() or not sessions_path.is_dir():
        raise CampaignError("campaign sessions path is not a regular directory")
    entries = sorted(sessions_path.iterdir())
    for path in entries:
        if path.is_symlink() or not path.is_dir():
            raise CampaignError(f"invalid entry in sessions directory: {path.name}")
    expected_names = [f"{index:06d}" for index in range(1, len(entries) + 1)]
    if [path.name for path in entries] != expected_names:
        raise CampaignError("campaign session numbering is not contiguous")
    return entries


def inspect_campaign(
    root: Path, *, allow_incomplete_final: bool = False
) -> dict[str, Any]:
    root = root.resolve()
    paths = _campaign_paths(root)
    actual_root_entries = {path.name for path in root.iterdir()}
    if actual_root_entries != ROOT_ENTRIES:
        raise CampaignError(
            "campaign root entries differ from the exact archive layout: "
            f"{sorted(actual_root_entries ^ ROOT_ENTRIES)}"
        )
    campaign = read_json(paths["metadata"])
    validate_campaign_metadata(campaign)
    read_valid_pool(paths["pool"])
    campaign_hash = sha256_bytes(_regular_bytes(paths["metadata"]))
    previous_pool = campaign["initial_pool"]
    previous_end_hash: str | None = None
    summaries: list[dict[str, Any]] = []
    all_directories = _session_directories(paths["sessions"])
    incomplete_directory: Path | None = None
    if all_directories and not (all_directories[-1] / "end.json").exists():
        if not allow_incomplete_final:
            raise CampaignError(f"session {all_directories[-1].name} is incomplete")
        incomplete_directory = all_directories[-1]
        directories = all_directories[:-1]
    else:
        directories = all_directories
    for index, directory in enumerate(directories, 1):
        present = {path.name for path in directory.iterdir()}
        if (
            not {"start.json", "end.json", "pool.before.json", "pool.after.json"}
            <= present
        ):
            raise CampaignError(f"session {directory.name} is incomplete")
        if not present <= SESSION_ENTRIES:
            raise CampaignError(f"session {directory.name} has unexpected artifacts")
        start = read_json(directory / "start.json")
        end = read_json(directory / "end.json")
        if set(start) != {
            "schema",
            "session_id",
            "session_index",
            "started_at_utc",
            "supervisor_pid",
            "campaign_sha256",
            "source_commit_sha",
            "previous_end_sha256",
            "pool_before",
            "starting_pool_size",
            "command",
            "cwd",
        }:
            raise CampaignError(f"session {directory.name} start fields are invalid")
        if (
            start.get("schema") != SESSION_START_SCHEMA
            or start.get("session_index") != index
            or start.get("session_id") != directory.name
            or not _is_int(start.get("supervisor_pid"))
            or start.get("campaign_sha256") != campaign_hash
            or start.get("previous_end_sha256") != previous_end_hash
            or start.get("source_commit_sha")
            != campaign["identity"]["source"]["commit_sha"]
            or start.get("cwd") != campaign["identity"]["source"]["repo_root"]
        ):
            raise CampaignError(f"session {directory.name} start record is invalid")
        if set(end) != {
            "schema",
            "session_id",
            "session_index",
            "finished_at_utc",
            "duration_seconds",
            "supervisor_pid",
            "child_pid",
            "start_sha256",
            "status",
            "recovered",
            "returncode",
            "signal",
            "launch_error",
            "pool_error",
            "result_error",
            "child_result_status",
            "terminal",
            "artifacts",
        }:
            raise CampaignError(f"session {directory.name} end fields are invalid")
        if (
            end.get("schema") != SESSION_END_SCHEMA
            or end.get("session_index") != index
            or end.get("session_id") != directory.name
            or end.get("start_sha256")
            != sha256_bytes(_regular_bytes(directory / "start.json"))
            or not _is_int(end.get("supervisor_pid"))
            or end.get("supervisor_pid") != start["supervisor_pid"]
            or not isinstance(end.get("recovered"), bool)
            or (end.get("child_pid") is not None and not _is_int(end.get("child_pid")))
            or (
                end.get("duration_seconds") is None and end.get("recovered") is not True
            )
        ):
            raise CampaignError(f"session {directory.name} end record is invalid")
        artifacts = end.get("artifacts")
        if not isinstance(artifacts, dict) or set(artifacts) != {
            "pool_before",
            "pool_after",
            "process",
            "result",
            "trace",
            "log",
        }:
            raise CampaignError(f"session {directory.name} artifact ledger is invalid")
        pool_before = _verify_artifact_record(
            directory, "pool_before", artifacts["pool_before"], True
        )
        pool_after = _verify_artifact_record(
            directory, "pool_after", artifacts["pool_after"], True
        )
        process_path = _verify_artifact_record(
            directory, "process", artifacts["process"], False
        )
        _verify_artifact_record(directory, "result", artifacts["result"], False)
        _verify_artifact_record(directory, "trace", artifacts["trace"], False)
        _verify_artifact_record(directory, "log", artifacts["log"], True)
        assert pool_before is not None and pool_after is not None
        if end["child_pid"] is not None:
            if process_path is None:
                raise CampaignError(f"session {directory.name} has no process record")
            process = read_json(process_path)
            if (
                set(process)
                != {
                    "schema",
                    "session_id",
                    "supervisor_pid",
                    "child_pid",
                    "spawned_at_utc",
                }
                or process.get("schema") != SESSION_PROCESS_SCHEMA
                or process.get("session_id") != directory.name
                or process.get("supervisor_pid") != end["supervisor_pid"]
                or process.get("child_pid") != end["child_pid"]
            ):
                raise CampaignError(
                    f"session {directory.name} process record is invalid"
                )
        pool_before_document = read_valid_pool(pool_before)
        read_valid_pool(pool_after)
        if artifacts["pool_before"]["sha256"] != previous_pool["sha256"]:
            raise CampaignError(
                f"session {directory.name} does not continue the pool chain"
            )
        if start.get("pool_before") != artifacts["pool_before"]:
            raise CampaignError(
                f"session {directory.name} start pool binding is invalid"
            )
        if start.get("starting_pool_size") != len(pool_before_document["triples"]):
            raise CampaignError(
                f"session {directory.name} starting pool size is invalid"
            )
        expected_command = _child_command(
            campaign["identity"]["interpreter"]["path"],
            Path(campaign["identity"]["source"]["repo_root"]),
            campaign["identity"]["runner"]["path"],
            paths["pool"],
            directory / "trace.jsonl",
            directory / "result.json",
        )
        if start.get("command") != expected_command:
            raise CampaignError(f"session {directory.name} command is invalid")
        child_status = end.get("child_result_status")
        terminal = child_status in TERMINAL_CHILD_STATUSES
        if end.get("terminal") is not terminal:
            raise CampaignError(f"session {directory.name} terminal flag is invalid")
        if child_status is not None:
            result_path = directory / "result.json"
            result = validate_child_result(
                result_path,
                pool_after,
                directory / "trace.jsonl",
                start["starting_pool_size"],
                recorded_pool_path=paths["pool"],
            )
            if result.get("status") != child_status:
                raise CampaignError(
                    f"session {directory.name} child status binding is invalid"
                )
            ordinary = (
                end.get("status") == "CHILD_RESULT_RECORDED"
                and end.get("recovered") is False
                and end.get("returncode") == 0
                and end.get("launch_error") is None
            )
            recovered = (
                end.get("status") == "RECOVERED_CHILD_RESULT"
                and end.get("recovered") is True
                and end.get("returncode") is None
                and isinstance(end.get("launch_error"), dict)
                and end["launch_error"].get("type") == "SupervisorInterrupted"
            )
            if (
                not (ordinary or recovered)
                or end.get("pool_error") is not None
                or end.get("result_error") is not None
            ):
                raise CampaignError(
                    f"session {directory.name} completion fields are inconsistent"
                )
        elif end.get("status") in {
            "CHILD_RESULT_RECORDED",
            "RECOVERED_CHILD_RESULT",
        }:
            raise CampaignError(
                f"session {directory.name} lacks its recorded child result"
            )
        elif end.get("recovered") is True and (
            end.get("status") != "SUPERVISOR_INTERRUPTED"
            or end.get("returncode") is not None
            or not isinstance(end.get("launch_error"), dict)
            or end["launch_error"].get("type") != "SupervisorInterrupted"
        ):
            raise CampaignError(
                f"session {directory.name} recovery fields are inconsistent"
            )
        if terminal and index != len(directories):
            raise CampaignError(
                f"terminal session {directory.name} is not the final session"
            )
        previous_pool = artifacts["pool_after"]
        previous_end_hash = sha256_bytes(_regular_bytes(directory / "end.json"))
        summaries.append(
            {
                "session_id": directory.name,
                "status": end.get("status"),
                "child_result_status": child_status,
                "terminal": terminal,
                "pool_sha256": artifacts["pool_after"]["sha256"],
            }
        )
    central_pool = artifact_record(paths["pool"])
    if central_pool is None:
        raise CampaignError("authoritative pool is absent")
    if (
        incomplete_directory is None
        and central_pool["sha256"] != previous_pool["sha256"]
    ):
        raise CampaignError("authoritative pool does not match the resume chain")
    latest = summaries[-1] if summaries else None
    return {
        "campaign": campaign,
        "campaign_sha256": campaign_hash,
        "session_count": len(summaries),
        "sessions": summaries,
        "latest": latest,
        "terminal": bool(latest and latest["terminal"]),
        "pool": central_pool,
        "pool_chain_tail": previous_pool,
        "previous_end_sha256": previous_end_hash,
        "incomplete_session": (
            incomplete_directory.name if incomplete_directory is not None else None
        ),
    }


def recover_incomplete_session(root: Path) -> dict[str, Any] | None:
    root = root.resolve()
    state = inspect_campaign(root, allow_incomplete_final=True)
    session_id = state["incomplete_session"]
    if session_id is None:
        return None
    if state["terminal"]:
        raise CampaignError("an incomplete session follows a terminal result")

    paths = _campaign_paths(root)
    directory = paths["sessions"] / session_id
    present = {path.name for path in directory.iterdir()}
    if not {"start.json", "pool.before.json"} <= present:
        raise CampaignError(f"incomplete session {session_id} lacks its start snapshot")
    if not present <= SESSION_ENTRIES:
        raise CampaignError(f"incomplete session {session_id} has unexpected artifacts")

    start_path = directory / "start.json"
    start = read_json(start_path)
    expected_start_fields = {
        "schema",
        "session_id",
        "session_index",
        "started_at_utc",
        "supervisor_pid",
        "campaign_sha256",
        "source_commit_sha",
        "previous_end_sha256",
        "pool_before",
        "starting_pool_size",
        "command",
        "cwd",
    }
    expected_index = state["session_count"] + 1
    if set(start) != expected_start_fields or (
        start.get("schema") != SESSION_START_SCHEMA
        or start.get("session_id") != session_id
        or start.get("session_index") != expected_index
        or not _is_int(start.get("supervisor_pid"))
        or start.get("campaign_sha256") != state["campaign_sha256"]
        or start.get("source_commit_sha")
        != state["campaign"]["identity"]["source"]["commit_sha"]
        or start.get("previous_end_sha256") != state["previous_end_sha256"]
        or start.get("cwd") != state["campaign"]["identity"]["source"]["repo_root"]
    ):
        raise CampaignError(f"incomplete session {session_id} has an invalid start")

    pool_before_path = directory / "pool.before.json"
    pool_before = artifact_record(pool_before_path)
    if (
        pool_before is None
        or start.get("pool_before") != pool_before
        or pool_before["sha256"] != state["pool_chain_tail"]["sha256"]
    ):
        raise CampaignError(
            f"incomplete session {session_id} breaks the incoming pool chain"
        )
    pool_before_document = read_valid_pool(pool_before_path)
    if start.get("starting_pool_size") != len(pool_before_document["triples"]):
        raise CampaignError(
            f"incomplete session {session_id} has a wrong starting pool size"
        )
    expected_command = _child_command(
        state["campaign"]["identity"]["interpreter"]["path"],
        Path(state["campaign"]["identity"]["source"]["repo_root"]),
        state["campaign"]["identity"]["runner"]["path"],
        paths["pool"],
        directory / "trace.jsonl",
        directory / "result.json",
    )
    if start.get("command") != expected_command:
        raise CampaignError(
            f"incomplete session {session_id} has a wrong child command"
        )

    process_path = directory / "process.json"
    child_pid: int | None = None
    if process_path.exists() or process_path.is_symlink():
        process = read_json(process_path)
        if (
            set(process)
            != {
                "schema",
                "session_id",
                "supervisor_pid",
                "child_pid",
                "spawned_at_utc",
            }
            or process.get("schema") != SESSION_PROCESS_SCHEMA
            or process.get("session_id") != session_id
            or process.get("supervisor_pid") != start["supervisor_pid"]
            or not _is_int(process.get("child_pid"))
        ):
            raise CampaignError(
                f"incomplete session {session_id} has an invalid process record"
            )
        child_pid = process["child_pid"]

    pool_after_path = directory / "pool.after.json"
    central_pool = artifact_record(paths["pool"])
    assert central_pool is not None
    if pool_after_path.exists() or pool_after_path.is_symlink():
        pool_after = artifact_record(pool_after_path)
        if pool_after is None or pool_after["sha256"] != central_pool["sha256"]:
            raise CampaignError(
                f"incomplete session {session_id} has a stale pool-after snapshot"
            )
    else:
        atomic_snapshot(paths["pool"], pool_after_path)
    read_valid_pool(pool_after_path)

    log_path = directory / "child.log"
    if log_path.is_symlink():
        raise CampaignError(f"incomplete session {session_id} log is a symlink")
    if not log_path.exists():
        atomic_write_bytes(log_path, b"")
    trace_path = directory / "trace.jsonl"
    result_path = directory / "result.json"
    child_result: dict[str, Any] | None = None
    result_error: str | None = None
    try:
        child_result = validate_child_result(
            result_path,
            pool_after_path,
            trace_path,
            start["starting_pool_size"],
            recorded_pool_path=paths["pool"],
        )
    except CampaignError as error:
        result_error = str(error)

    artifacts = {
        "pool_before": artifact_record(pool_before_path),
        "pool_after": artifact_record(pool_after_path),
        "process": artifact_record(process_path),
        "result": artifact_record(result_path),
        "trace": artifact_record(trace_path),
        "log": artifact_record(log_path),
    }
    child_status = child_result["status"] if child_result is not None else None
    end = {
        "schema": SESSION_END_SCHEMA,
        "session_id": session_id,
        "session_index": expected_index,
        "finished_at_utc": utc_now(),
        "duration_seconds": None,
        "supervisor_pid": start["supervisor_pid"],
        "child_pid": child_pid,
        "start_sha256": sha256_bytes(_regular_bytes(start_path)),
        "status": (
            "RECOVERED_CHILD_RESULT"
            if child_result is not None
            else "SUPERVISOR_INTERRUPTED"
        ),
        "recovered": True,
        "returncode": None,
        "signal": None,
        "launch_error": {
            "type": "SupervisorInterrupted",
            "message": (
                "the prior supervisor ended without an end ledger; "
                "recovery ran only after the inherited campaign lock released"
            ),
        },
        "pool_error": None,
        "result_error": result_error,
        "child_result_status": child_status,
        "terminal": child_status in TERMINAL_CHILD_STATUSES,
        "artifacts": artifacts,
    }
    atomic_write_json(directory / "end.json", end)
    inspect_campaign(root)
    return end


def _assert_current_identity(
    campaign: dict[str, Any],
    repo_root: Path,
    runner_path: Path,
    interpreter: Path | str,
) -> dict[str, object]:
    current = collect_runtime_identity(repo_root, runner_path, interpreter)
    if current != campaign["identity"]:
        raise CampaignError("current source, interpreter, or dependencies changed")
    return current


def _child_command(
    interpreter_path: str,
    repo_root: Path,
    runner_relative: str,
    pool_path: Path,
    trace_path: Path,
    result_path: Path,
) -> list[str]:
    return [
        interpreter_path,
        str(repo_root / runner_relative),
        "--K",
        str(FIXED_CONFIG["upper"]),
        "--add",
        str(FIXED_CONFIG["add_per_iteration"]),
        "--time-limit",
        str(FIXED_CONFIG["time_limit_seconds_per_master"]),
        "--workers",
        str(FIXED_CONFIG["workers"]),
        "--random-seed",
        str(FIXED_CONFIG["random_seed"]),
        "--symmetry",
        str(FIXED_CONFIG["symmetry"]),
        "--max-iterations",
        str(FIXED_CONFIG["max_iterations"]),
        "--pool",
        str(pool_path),
        "--trace",
        str(trace_path),
        "--result",
        str(result_path),
    ]


def _run_child(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
    log_handle: Any,
    lock_fd: int,
    on_spawn: Any,
) -> tuple[int, int]:
    child: subprocess.Popen[bytes] | None = None
    pending_signals: list[int] = []
    forwarded_signals = (signal.SIGINT, signal.SIGTERM)
    previous_handlers: dict[int, Any] = {}
    can_forward = threading.current_thread() is threading.main_thread()

    def forward(signum: int, frame: object) -> None:
        del frame
        if child is None:
            pending_signals.append(signum)
        elif child.poll() is None:
            os.killpg(child.pid, signum)

    if can_forward:
        for signum in forwarded_signals:
            previous_handlers[signum] = signal.getsignal(signum)
            signal.signal(signum, forward)
    try:
        child = subprocess.Popen(
            command,
            cwd=cwd,
            env=environment,
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            pass_fds=(lock_fd,),
        )
        try:
            on_spawn(child.pid)
        except BaseException:
            os.killpg(child.pid, signal.SIGTERM)
            child.wait()
            raise
        for signum in pending_signals:
            if child.poll() is None:
                os.killpg(child.pid, signum)
        return child.pid, child.wait()
    finally:
        if can_forward:
            for signum, handler in previous_handlers.items():
                signal.signal(signum, handler)


def run_campaign_session(
    root: Path,
    repo_root: Path,
    runner_path: Path,
    interpreter: Path | str,
) -> dict[str, Any]:
    root = root.resolve()
    repo_root = repo_root.resolve()
    runner_path = runner_path.resolve()
    _ensure_external_root(root, repo_root)
    with CampaignLock(root) as campaign_lock:
        campaign = initialize_campaign(root, repo_root, runner_path, interpreter)
        validate_campaign_metadata(campaign)
        paths = _campaign_paths(root)
        recover_incomplete_session(root)
        state = inspect_campaign(root)
        if state["terminal"]:
            latest_status = state["latest"]["child_result_status"]
            raise TerminalCampaign(
                f"campaign already ended with terminal status {latest_status}"
            )
        identity = _assert_current_identity(
            campaign, repo_root, runner_path, interpreter
        )
        session_index = state["session_count"] + 1
        session_id = f"{session_index:06d}"
        session_path = paths["sessions"] / session_id
        session_path.mkdir()
        pool_before_path = session_path / "pool.before.json"
        pool_after_path = session_path / "pool.after.json"
        trace_path = session_path / "trace.jsonl"
        result_path = session_path / "result.json"
        log_path = session_path / "child.log"
        start_path = session_path / "start.json"
        process_path = session_path / "process.json"
        end_path = session_path / "end.json"
        atomic_snapshot(paths["pool"], pool_before_path)
        pool_before = artifact_record(pool_before_path)
        assert pool_before is not None
        starting_pool_size = len(read_valid_pool(pool_before_path)["triples"])
        previous_end_hash = (
            sha256_bytes(
                _regular_bytes(
                    paths["sessions"] / f"{session_index - 1:06d}" / "end.json"
                )
            )
            if session_index > 1
            else None
        )
        command = _child_command(
            identity["interpreter"]["path"],
            repo_root,
            identity["runner"]["path"],
            paths["pool"],
            trace_path,
            result_path,
        )
        start = {
            "schema": SESSION_START_SCHEMA,
            "session_id": session_id,
            "session_index": session_index,
            "started_at_utc": utc_now(),
            "supervisor_pid": os.getpid(),
            "campaign_sha256": state["campaign_sha256"],
            "source_commit_sha": identity["source"]["commit_sha"],
            "previous_end_sha256": previous_end_hash,
            "pool_before": pool_before,
            "starting_pool_size": starting_pool_size,
            "command": command,
            "cwd": str(repo_root),
        }
        atomic_write_json(start_path, start)
        started = time.monotonic()
        returncode: int | None = None
        child_pid: int | None = None
        launch_error: dict[str, str] | None = None

        def record_process(pid: int) -> None:
            atomic_write_json(
                process_path,
                {
                    "schema": SESSION_PROCESS_SCHEMA,
                    "session_id": session_id,
                    "supervisor_pid": os.getpid(),
                    "child_pid": pid,
                    "spawned_at_utc": utc_now(),
                },
            )

        try:
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment["PYTHONUNBUFFERED"] = "1"
            with log_path.open("xb") as log_handle:
                child_pid, returncode = _run_child(
                    command,
                    cwd=repo_root,
                    environment=environment,
                    log_handle=log_handle,
                    lock_fd=campaign_lock.handle.fileno(),
                    on_spawn=record_process,
                )
        except BaseException as error:
            launch_error = {
                "type": type(error).__name__,
                "message": str(error),
            }
            if not log_path.exists():
                atomic_write_bytes(log_path, b"")

        pool_error: str | None = None
        if paths["pool"].exists() and not paths["pool"].is_symlink():
            try:
                atomic_snapshot(paths["pool"], pool_after_path)
                read_valid_pool(pool_after_path)
            except CampaignError as error:
                pool_error = str(error)
        else:
            pool_error = "authoritative pool is missing or is a symlink"

        child_result: dict[str, Any] | None = None
        result_error: str | None = None
        if returncode == 0:
            try:
                child_result = validate_child_result(
                    result_path,
                    paths["pool"],
                    trace_path,
                    starting_pool_size,
                )
            except CampaignError as error:
                result_error = str(error)

        if launch_error is not None:
            supervisor_status = "CHILD_LAUNCH_ERROR"
        elif returncode is not None and returncode < 0:
            supervisor_status = "CHILD_SIGNAL"
        elif returncode != 0:
            supervisor_status = "CHILD_NONZERO"
        elif pool_error is not None:
            supervisor_status = "POOL_CORRUPTED"
        elif result_error is not None:
            supervisor_status = "INVALID_CHILD_RESULT"
        else:
            supervisor_status = "CHILD_RESULT_RECORDED"

        artifacts = {
            "pool_before": artifact_record(pool_before_path),
            "pool_after": artifact_record(pool_after_path),
            "process": artifact_record(process_path),
            "result": artifact_record(result_path),
            "trace": artifact_record(trace_path),
            "log": artifact_record(log_path),
        }
        child_status = child_result["status"] if child_result is not None else None
        end = {
            "schema": SESSION_END_SCHEMA,
            "session_id": session_id,
            "session_index": session_index,
            "finished_at_utc": utc_now(),
            "duration_seconds": round(time.monotonic() - started, 6),
            "supervisor_pid": os.getpid(),
            "child_pid": child_pid,
            "start_sha256": sha256_bytes(_regular_bytes(start_path)),
            "status": supervisor_status,
            "recovered": False,
            "returncode": returncode,
            "signal": (
                signal.Signals(-returncode).name
                if returncode is not None and returncode < 0
                else None
            ),
            "launch_error": launch_error,
            "pool_error": pool_error,
            "result_error": result_error,
            "child_result_status": child_status,
            "terminal": child_status in TERMINAL_CHILD_STATUSES,
            "artifacts": artifacts,
        }
        atomic_write_json(end_path, end)
        if supervisor_status == "CHILD_RESULT_RECORDED":
            inspect_campaign(root)
        return end


def _lock_is_held(root: Path) -> bool:
    lock_path = root / ".campaign.lock"
    if not lock_path.exists():
        return False
    if lock_path.is_symlink():
        return False
    with lock_path.open("a+") as handle:
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    return False


def campaign_status(root: Path) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists() or not (root / "campaign.json").exists():
        return {
            "schema": CAMPAIGN_SCHEMA,
            "root": str(root),
            "status": "NOT_INITIALIZED",
            "lock_held": _lock_is_held(root) if root.exists() else False,
        }
    lock_held = _lock_is_held(root)
    if lock_held:
        sessions_path = root / "sessions"
        session_names = (
            sorted(path.name for path in sessions_path.iterdir())
            if sessions_path.is_dir()
            else []
        )
        return {
            "schema": CAMPAIGN_SCHEMA,
            "root": str(root),
            "status": "RUNNING",
            "lock_held": True,
            "session_count_started": len(session_names),
            "active_session": session_names[-1] if session_names else None,
        }
    try:
        state = inspect_campaign(root)
    except CampaignError as error:
        try:
            partial = inspect_campaign(root, allow_incomplete_final=True)
        except CampaignError:
            partial = None
        if partial is not None and partial["incomplete_session"] is not None:
            return {
                "schema": CAMPAIGN_SCHEMA,
                "root": str(root),
                "status": "RECOVERY_REQUIRED",
                "lock_held": False,
                "incomplete_session": partial["incomplete_session"],
                "pool": partial["pool"],
            }
        return {
            "schema": CAMPAIGN_SCHEMA,
            "root": str(root),
            "status": "CORRUPT",
            "lock_held": False,
            "error": str(error),
        }
    return {
        "schema": CAMPAIGN_SCHEMA,
        "root": str(root),
        "status": "TERMINAL" if state["terminal"] else "READY",
        "lock_held": False,
        "session_count": state["session_count"],
        "latest": state["latest"],
        "pool": state["pool"],
        "source_commit_sha": state["campaign"]["identity"]["source"]["commit_sha"],
        "config": state["campaign"]["config"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--root", type=Path, required=True)
    default_repo = Path(__file__).resolve().parents[2]
    run_parser.add_argument("--repo-root", type=Path, default=default_repo)
    run_parser.add_argument(
        "--runner",
        type=Path,
        default=default_repo / "tracks" / "parkability" / "run_cegar.py",
    )
    run_parser.add_argument("--python", type=Path, default=Path(sys.executable))
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "status":
        print(json.dumps(campaign_status(args.root), indent=2, sort_keys=True))
        return
    try:
        result = run_campaign_session(
            args.root,
            args.repo_root,
            args.runner,
            args.python,
        )
    except CampaignError as error:
        parser.exit(2, f"error: {error}\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "CHILD_RESULT_RECORDED":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
