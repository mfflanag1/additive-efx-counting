#!/usr/bin/env python3
"""Generate a binary DRAT proof for a frozen parkability terminal DIMACS."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:
    from . import terminal_cnf
except ImportError:
    import terminal_cnf


CADICAL_COMMIT = "146207318796f094dcded87349a64f0c6927309e"


def atomic_bytes(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(contents)
        temporary.replace(path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def git_output(source: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(source), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise ValueError(
            f"git {' '.join(arguments)} failed for {source}: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def validate_terminal_result(
    contents: bytes, dimacs_hash: str, dimacs_bytes: int
) -> dict:
    value = json.loads(contents)
    if (
        not isinstance(value, dict)
        or value.get("schema") != "parkability-terminal-cnf-result-v1"
        or value.get("status") != "UNSAT_SOLVER_RESULT"
        or value.get("solver", {}).get("status") != "UNSAT"
    ):
        raise ValueError("terminal result is not an independent UNSAT result")
    if (
        value.get("dimacs_sha256") != dimacs_hash
        or value.get("dimacs_bytes") != dimacs_bytes
    ):
        raise ValueError("terminal result does not bind the supplied DIMACS")
    return value


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    source_path = Path(__file__).resolve()
    source_hash = terminal_cnf.sha256(source_path)
    for path in (args.proof_out, args.log_out, args.result_out):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite output: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
    if not args.cadical.is_file():
        raise FileNotFoundError(args.cadical)
    cadical_hash = terminal_cnf.sha256(args.cadical)
    if cadical_hash != args.expect_cadical_sha256:
        raise ValueError(
            f"CaDiCaL SHA-256 is {cadical_hash}, expected {args.expect_cadical_sha256}"
        )
    source_commit = git_output(args.cadical_source, "rev-parse", "HEAD")
    if source_commit != CADICAL_COMMIT:
        raise ValueError(
            f"CaDiCaL source commit is {source_commit}, expected {CADICAL_COMMIT}"
        )
    if args.cadical.resolve() != (args.cadical_source / "build" / "cadical").resolve():
        raise ValueError("CaDiCaL executable is not the pinned checkout's build output")
    tracked_dirty = git_output(
        args.cadical_source,
        "status",
        "--porcelain",
        "--untracked-files=no",
    )
    if tracked_dirty:
        raise ValueError("CaDiCaL tracked source files are not clean")
    terminal_result_bytes = args.terminal_result.read_bytes()
    terminal_result_hash = hashlib.sha256(terminal_result_bytes).hexdigest()
    dimacs_hash = terminal_cnf.sha256(args.dimacs)
    dimacs_bytes = args.dimacs.stat().st_size
    terminal_result = validate_terminal_result(
        terminal_result_bytes, dimacs_hash, dimacs_bytes
    )

    with tempfile.TemporaryDirectory(
        prefix="parkability-cadical-snapshot-"
    ) as directory_name:
        cadical_snapshot = Path(directory_name) / "cadical"
        shutil.copyfile(args.cadical, cadical_snapshot)
        os.chmod(cadical_snapshot, 0o700)
        if terminal_cnf.sha256(cadical_snapshot) != cadical_hash:
            raise RuntimeError("CaDiCaL snapshot differs from its source")
        if terminal_cnf.sha256(args.cadical) != cadical_hash:
            raise RuntimeError("CaDiCaL changed while it was snapshotted")
        version = subprocess.run(
            [str(cadical_snapshot), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        command = [
            str(cadical_snapshot),
            "--binary=true",
            "--stats",
            "-t",
            str(args.timeout_seconds),
            "-n",
            str(args.dimacs.resolve()),
            str(args.proof_out.resolve()),
        ]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                timeout=args.timeout_seconds + 60,
                check=False,
            )
            return_code = completed.returncode
            transcript = completed.stdout + completed.stderr
        except subprocess.TimeoutExpired as error:
            return_code = None
            stdout = error.stdout or b""
            stderr = error.stderr or b""
            if isinstance(stdout, str):
                stdout = stdout.encode()
            if isinstance(stderr, str):
                stderr = stderr.encode()
            transcript = stdout + stderr + b"\nwrapper wall-clock timeout\n"
        if terminal_cnf.sha256(cadical_snapshot) != cadical_hash:
            raise RuntimeError("executed CaDiCaL snapshot changed")
    atomic_bytes(args.log_out, transcript)
    if terminal_cnf.sha256(args.dimacs) != dimacs_hash:
        raise RuntimeError("DIMACS changed during proof generation")
    if terminal_cnf.sha256(args.cadical) != cadical_hash:
        raise RuntimeError("CaDiCaL source changed during proof generation")
    if args.terminal_result.read_bytes() != terminal_result_bytes:
        raise RuntimeError("terminal result changed during proof generation")
    if terminal_cnf.sha256(source_path) != source_hash:
        raise RuntimeError("proof generator source changed during execution")

    text = transcript.decode(errors="replace")
    if return_code == 20 and "s UNSATISFIABLE" in text:
        status = "UNSAT_PROOF_GENERATED"
    elif return_code == 10 and "s SATISFIABLE" in text:
        status = "SAT"
    else:
        status = "UNKNOWN"
    proof = (
        {
            "path": str(args.proof_out.resolve()),
            "bytes": args.proof_out.stat().st_size,
            "sha256": terminal_cnf.sha256(args.proof_out),
            "format": "binary DRAT",
        }
        if args.proof_out.is_file()
        else None
    )
    if status == "UNSAT_PROOF_GENERATED" and (proof is None or proof["bytes"] == 0):
        raise RuntimeError("CaDiCaL reported UNSAT without a nonempty proof")

    result = {
        "schema": "parkability-terminal-drat-generation-v1",
        "status": status,
        "target_claim": "the exact terminal DIMACS is unsatisfiable",
        "terminal_result": {
            "path": str(args.terminal_result.resolve()),
            "bytes": args.terminal_result.stat().st_size,
            "sha256": terminal_result_hash,
            "pool_sha256": terminal_result["pool_sha256"],
            "pool_canonical_sha256": terminal_result["pool_canonical_sha256"],
            "pool_size": terminal_result["pool_size"],
        },
        "input": {
            "path": str(args.dimacs.resolve()),
            "bytes": dimacs_bytes,
            "sha256": dimacs_hash,
        },
        "proof": proof,
        "generator": {
            "name": "CaDiCaL",
            "version": (version.stdout + version.stderr).strip(),
            "repository": git_output(
                args.cadical_source, "remote", "get-url", "origin"
            ),
            "commit": source_commit,
            "executable_path": str(args.cadical.resolve()),
            "executable_sha256": cadical_hash,
            "execution": "private byte-identical snapshot",
            "command": command,
            "exit_code": return_code,
            "log": {
                "path": str(args.log_out.resolve()),
                "bytes": args.log_out.stat().st_size,
                "sha256": terminal_cnf.sha256(args.log_out),
            },
        },
        "seconds": round(time.perf_counter() - started, 6),
        "command": sys.argv,
        "source_sha256": source_hash,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }
    terminal_cnf.atomic_json(args.result_out, result)
    print(json.dumps(result, indent=2), flush=True)
    if args.expect is not None and status != args.expect:
        return 1
    return 0 if status == "UNSAT_PROOF_GENERATED" else 2


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimacs", type=Path, required=True)
    parser.add_argument("--terminal-result", type=Path, required=True)
    parser.add_argument("--proof-out", type=Path, required=True)
    parser.add_argument("--log-out", type=Path, required=True)
    parser.add_argument("--result-out", type=Path, required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--cadical-source", type=Path, required=True)
    parser.add_argument("--expect-cadical-sha256", required=True)
    parser.add_argument("--timeout-seconds", type=int, default=10800)
    parser.add_argument(
        "--expect",
        choices=("UNSAT_PROOF_GENERATED", "SAT", "UNKNOWN"),
    )
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("timeout-seconds must be positive")
    inputs = {
        args.dimacs.resolve(),
        args.terminal_result.resolve(),
        args.cadical.resolve(),
    }
    outputs = {
        args.proof_out.resolve(),
        args.log_out.resolve(),
        args.result_out.resolve(),
    }
    if len(outputs) != 3 or inputs & outputs:
        parser.error("proof, log, and result outputs must be distinct and new")
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
