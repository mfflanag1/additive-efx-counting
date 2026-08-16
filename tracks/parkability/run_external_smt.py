#!/usr/bin/env python3
"""Run a frozen SMT-LIB formula with a pinned external solver binary."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(document, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def run(
    *,
    solver_path: Path,
    formula_path: Path,
    result_path: Path,
    time_limit_s: float,
    solver_args: tuple[str, ...],
    expected: str | None,
    interface: str,
    quiet: bool = False,
) -> dict:
    if (
        not solver_path.is_file()
        or not formula_path.is_file()
        or result_path.exists()
        or time_limit_s <= 0
        or expected not in {None, "sat", "unsat", "unknown"}
        or interface not in {"cvc5", "z3"}
    ):
        raise ValueError("valid binary, formula, timeout, and new result are required")
    version_option = "--version" if interface == "cvc5" else "-version"
    version = subprocess.run(
        [str(solver_path), version_option],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if interface == "cvc5":
        command = [
            str(solver_path),
            "--lang=smt2",
            f"--tlimit={round(time_limit_s * 1000)}",
            *solver_args,
            str(formula_path),
        ]
    else:
        command = [
            str(solver_path),
            f"-T:{round(time_limit_s)}",
            *solver_args,
            str(formula_path),
        ]
    started_at = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    timed_out = False
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=time_limit_s + 60,
        )
        returncode = completed.returncode
        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()
    except subprocess.TimeoutExpired as error:
        timed_out = True
        returncode = None
        stdout = (
            error.stdout.decode() if isinstance(error.stdout, bytes) else error.stdout
        ) or ""
        stderr = (
            error.stderr.decode() if isinstance(error.stderr, bytes) else error.stderr
        ) or ""
        stdout = stdout.strip()
        stderr = stderr.strip()
    elapsed = time.monotonic() - started
    verdict_lines = [
        line.strip()
        for line in stdout.splitlines()
        if line.strip() in {"sat", "unsat", "unknown"}
    ]
    verdict = verdict_lines[-1] if verdict_lines else None
    confirmed = (
        not timed_out
        and returncode == 0
        and verdict == expected
        if expected is not None
        else None
    )
    document = {
        "schema": "external-smt-replay-v1",
        "started_at_utc": started_at,
        "elapsed_seconds": round(elapsed, 6),
        "command": command,
        "solver": str(solver_path.resolve()),
        "solver_interface": interface,
        "solver_sha256": file_sha256(solver_path),
        "solver_version_stdout": version.stdout.strip(),
        "solver_version_stderr": version.stderr.strip(),
        "formula": str(formula_path.resolve()),
        "formula_sha256": file_sha256(formula_path),
        "time_limit_seconds": time_limit_s,
        "timed_out": timed_out,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "verdict": verdict,
        "expected": expected,
        "confirmed_expected": confirmed,
        "host": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
    }
    atomic_json(result_path, document)
    if not quiet:
        print(json.dumps(document, indent=2, sort_keys=True), flush=True)
    if expected is not None and not confirmed:
        raise SystemExit(2)
    return document


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, required=True)
    parser.add_argument("--interface", choices=["cvc5", "z3"], default="cvc5")
    parser.add_argument("--solver-arg", action="append", default=[])
    parser.add_argument("--expect", choices=["sat", "unsat", "unknown"])
    args = parser.parse_args()
    run(
        solver_path=args.solver,
        formula_path=args.formula,
        result_path=args.result,
        time_limit_s=args.time_limit,
        solver_args=tuple(args.solver_arg),
        expected=args.expect,
        interface=args.interface,
    )


if __name__ == "__main__":
    main()
