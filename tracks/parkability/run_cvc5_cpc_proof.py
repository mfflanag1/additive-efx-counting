#!/usr/bin/env python3
"""Generate a cvc5 CPC proof and check it with the separate Ethos binary."""

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


def transform_cpc_output(
    *,
    raw_path: Path,
    proof_path: Path,
    cpc_signature: Path,
    expert_signature: Path,
) -> int:
    if proof_path.exists():
        raise ValueError("proof output already exists")
    descriptor, temporary = tempfile.mkstemp(
        dir=proof_path.parent,
        prefix=f".{proof_path.name}.",
    )
    proof_step_lines = 0
    try:
        with raw_path.open("rb") as source, os.fdopen(descriptor, "wb") as output:
            first = source.readline()
            second = source.readline()
            if first.strip() != b"unsat" or second.strip() != b"(":
                raise ValueError(
                    "unexpected cvc5 CPC preamble: "
                    f"{first[:100]!r}, {second[:100]!r}"
                )
            output.write(
                f'(include "{cpc_signature.resolve()}")\n'.encode()
            )
            output.write(
                f'(include "{expert_signature.resolve()}")\n'.encode()
            )
            previous = source.readline()
            if not previous:
                raise ValueError("cvc5 emitted an empty CPC proof")
            for line in source:
                output.write(previous)
                if b"(step " in previous or b"(assume " in previous:
                    proof_step_lines += 1
                previous = line
            if previous.strip() != b")":
                raise ValueError(
                    f"unexpected cvc5 CPC closing line: {previous[:100]!r}"
                )
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, proof_path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    return proof_step_lines


def run(
    *,
    cvc5_path: Path,
    ethos_path: Path,
    signature_dir: Path,
    formula_path: Path,
    proof_path: Path,
    result_path: Path,
    solve_time_limit_s: float,
    check_time_limit_s: float,
) -> dict:
    cpc_signature = signature_dir / "Cpc.eo"
    expert_signature = signature_dir / "expert" / "CpcExpert.eo"
    if (
        not cvc5_path.is_file()
        or not ethos_path.is_file()
        or not cpc_signature.is_file()
        or not expert_signature.is_file()
        or not formula_path.is_file()
        or proof_path.exists()
        or result_path.exists()
        or solve_time_limit_s <= 0
        or check_time_limit_s <= 0
    ):
        raise ValueError("valid new proof outputs and pinned tool inputs are required")
    proof_path.parent.mkdir(parents=True, exist_ok=True)
    raw_descriptor, raw_name = tempfile.mkstemp(
        dir=proof_path.parent,
        prefix=f".{proof_path.name}.raw.",
    )
    stderr_descriptor, stderr_name = tempfile.mkstemp(
        dir=proof_path.parent,
        prefix=f".{proof_path.name}.stderr.",
    )
    os.close(raw_descriptor)
    os.close(stderr_descriptor)
    raw_path = Path(raw_name)
    stderr_path = Path(stderr_name)
    command = [
        str(cvc5_path),
        "--lang=smt2",
        f"--tlimit={round(solve_time_limit_s * 1000)}",
        "--safe-mode=safe",
        "--dump-proofs",
        str(formula_path),
    ]
    started_at = datetime.now(timezone.utc).isoformat()
    solve_started = time.monotonic()
    solve_timed_out = False
    try:
        with raw_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            try:
                completed = subprocess.run(
                    command,
                    check=False,
                    stdout=stdout,
                    stderr=stderr,
                    timeout=solve_time_limit_s + 60,
                )
                solve_returncode = completed.returncode
            except subprocess.TimeoutExpired:
                solve_timed_out = True
                solve_returncode = None
        solve_seconds = time.monotonic() - solve_started
        solve_stderr = stderr_path.read_text(errors="replace").strip()
        proof_step_lines = None
        transform_error = None
        if not solve_timed_out and solve_returncode == 0:
            try:
                proof_step_lines = transform_cpc_output(
                    raw_path=raw_path,
                    proof_path=proof_path,
                    cpc_signature=cpc_signature,
                    expert_signature=expert_signature,
                )
            except (OSError, ValueError) as error:
                transform_error = str(error)

        check_command = [str(ethos_path), str(proof_path)]
        check_started = time.monotonic()
        check_timed_out = False
        if proof_path.is_file() and transform_error is None:
            try:
                checked = subprocess.run(
                    check_command,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=check_time_limit_s,
                )
                check_returncode = checked.returncode
                check_stdout = checked.stdout.strip()
                check_stderr = checked.stderr.strip()
            except subprocess.TimeoutExpired as error:
                check_timed_out = True
                check_returncode = None
                check_stdout = (
                    error.stdout.decode()
                    if isinstance(error.stdout, bytes)
                    else error.stdout
                ) or ""
                check_stderr = (
                    error.stderr.decode()
                    if isinstance(error.stderr, bytes)
                    else error.stderr
                ) or ""
                check_stdout = check_stdout.strip()
                check_stderr = check_stderr.strip()
        else:
            check_returncode = None
            check_stdout = ""
            check_stderr = ""
        check_seconds = time.monotonic() - check_started
        proof_status = (
            "correct"
            if "correct" in check_stdout.splitlines()
            else "incomplete"
            if "incomplete" in check_stdout.splitlines()
            else None
        )
        verified = (
            not solve_timed_out
            and solve_returncode == 0
            and transform_error is None
            and not check_timed_out
            and check_returncode == 0
            and proof_status == "correct"
        )
        document = {
            "schema": "cvc5-cpc-ethos-certificate-v1",
            "started_at_utc": started_at,
            "verified": verified,
            "formula": str(formula_path.resolve()),
            "formula_sha256": file_sha256(formula_path),
            "cvc5": str(cvc5_path.resolve()),
            "cvc5_sha256": file_sha256(cvc5_path),
            "ethos": str(ethos_path.resolve()),
            "ethos_sha256": file_sha256(ethos_path),
            "cpc_signature": str(cpc_signature.resolve()),
            "cpc_signature_sha256": file_sha256(cpc_signature),
            "expert_signature": str(expert_signature.resolve()),
            "expert_signature_sha256": file_sha256(expert_signature),
            "proof": str(proof_path.resolve()) if proof_path.exists() else None,
            "proof_sha256": (
                file_sha256(proof_path) if proof_path.exists() else None
            ),
            "proof_bytes": proof_path.stat().st_size if proof_path.exists() else None,
            "proof_step_lines": proof_step_lines,
            "solve": {
                "command": command,
                "time_limit_seconds": solve_time_limit_s,
                "elapsed_seconds": round(solve_seconds, 6),
                "timed_out": solve_timed_out,
                "returncode": solve_returncode,
                "stderr": solve_stderr,
                "transform_error": transform_error,
            },
            "check": {
                "command": check_command,
                "time_limit_seconds": check_time_limit_s,
                "elapsed_seconds": round(check_seconds, 6),
                "timed_out": check_timed_out,
                "returncode": check_returncode,
                "stdout": check_stdout,
                "stderr": check_stderr,
                "status": proof_status,
            },
            "host": {
                "platform": platform.platform(),
                "machine": platform.machine(),
                "python": platform.python_version(),
            },
        }
        atomic_json(result_path, document)
        print(json.dumps(document, indent=2, sort_keys=True), flush=True)
        if not verified:
            raise SystemExit(2)
        return document
    finally:
        raw_path.unlink(missing_ok=True)
        stderr_path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--ethos", type=Path, required=True)
    parser.add_argument("--signature-dir", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--solve-time-limit", type=float, required=True)
    parser.add_argument("--check-time-limit", type=float, required=True)
    args = parser.parse_args()
    run(
        cvc5_path=args.cvc5,
        ethos_path=args.ethos,
        signature_dir=args.signature_dir,
        formula_path=args.formula,
        proof_path=args.proof,
        result_path=args.result,
        solve_time_limit_s=args.solve_time_limit,
        check_time_limit_s=args.check_time_limit,
    )


if __name__ == "__main__":
    main()
