#!/usr/bin/env python3
"""Hash and optionally verify a parkability terminal DRAT certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
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


def require_hash(path: Path, expected: str | None, label: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(path)
    actual = terminal_cnf.sha256(path)
    if expected is not None and actual != expected:
        raise ValueError(f"{label} SHA-256 is {actual}, expected {expected}")
    return actual


def decompress_xz(source: Path, target: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with lzma.open(source, "rb") as compressed, target.open("wb") as output:
        for chunk in iter(lambda: compressed.read(1 << 20), b""):
            output.write(chunk)
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def run(args: argparse.Namespace) -> int:
    started = time.perf_counter()
    source_path = Path(__file__).resolve()
    source_hash = terminal_cnf.sha256(source_path)
    dimacs_hash = require_hash(args.dimacs, args.expect_dimacs_sha256, "DIMACS")
    if not args.terminal_result.is_file():
        raise FileNotFoundError(args.terminal_result)
    terminal_result_bytes = args.terminal_result.read_bytes()
    terminal_result_hash = hashlib.sha256(terminal_result_bytes).hexdigest()
    terminal_result = json.loads(terminal_result_bytes)
    if (
        not isinstance(terminal_result, dict)
        or terminal_result.get("schema") != "parkability-terminal-cnf-result-v1"
        or terminal_result.get("status") != "UNSAT_SOLVER_RESULT"
        or terminal_result.get("solver", {}).get("status") != "UNSAT"
    ):
        raise ValueError("terminal result is not an independent UNSAT result")
    if (
        terminal_result.get("dimacs_sha256") != dimacs_hash
        or terminal_result.get("dimacs_bytes") != args.dimacs.stat().st_size
    ):
        raise ValueError("terminal result does not bind the supplied DIMACS")
    proof_source_hash = require_hash(
        args.proof, args.expect_proof_sha256, "proof source"
    )

    with tempfile.TemporaryDirectory(
        prefix="parkability-terminal-drat-"
    ) as directory_name:
        if args.proof.suffix == ".xz":
            proof = Path(directory_name) / "proof.drat"
            proof_bytes, proof_hash = decompress_xz(args.proof, proof)
            compression = "xz"
        else:
            proof = args.proof
            proof_bytes = proof.stat().st_size
            proof_hash = terminal_cnf.sha256(proof)
            compression = "none"
        if (
            args.expect_uncompressed_sha256 is not None
            and proof_hash != args.expect_uncompressed_sha256
        ):
            raise ValueError(
                "uncompressed proof SHA-256 is "
                f"{proof_hash}, expected "
                f"{args.expect_uncompressed_sha256}"
            )
        if (
            args.expect_uncompressed_bytes is not None
            and proof_bytes != args.expect_uncompressed_bytes
        ):
            raise ValueError(
                f"uncompressed proof has {proof_bytes} bytes, "
                f"expected {args.expect_uncompressed_bytes}"
            )

        result = {
            "schema": "parkability-terminal-drat-check-v1",
            "status": "HASHES_PASS",
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
                "bytes": args.dimacs.stat().st_size,
                "sha256": dimacs_hash,
            },
            "proof": {
                "path": str(args.proof.resolve()),
                "compression": compression,
                "source_bytes": args.proof.stat().st_size,
                "source_sha256": proof_source_hash,
                "uncompressed_bytes": proof_bytes,
                "uncompressed_sha256": proof_hash,
                "format": "binary DRAT" if args.binary else "text DRAT",
            },
        }
        if not args.hash_only:
            expected_checker_hash = getattr(args, "expect_checker_sha256", None)
            if expected_checker_hash is None:
                raise ValueError("proof checking requires an expected checker SHA-256")
            checker = shutil.which(args.checker)
            if checker is None:
                checker_path = Path(args.checker)
                if not checker_path.is_file():
                    raise FileNotFoundError(
                        f"drat-trim executable not found: {args.checker}"
                    )
                checker = str(checker_path.resolve())
            checker_path = Path(checker)
            checker_hash = require_hash(checker_path, expected_checker_hash, "checker")
            checker_snapshot = Path(directory_name) / "drat-trim.snapshot"
            shutil.copyfile(checker_path, checker_snapshot)
            os.chmod(checker_snapshot, 0o700)
            if terminal_cnf.sha256(checker_snapshot) != checker_hash:
                raise RuntimeError("checker snapshot differs from its source")
            if terminal_cnf.sha256(checker_path) != checker_hash:
                raise RuntimeError("checker changed while it was snapshotted")
            command = [
                str(checker_snapshot),
                str(args.dimacs.resolve()),
                str(proof.resolve()),
            ]
            if args.binary:
                command.append("-i")
            command.extend(["-t", str(args.timeout_seconds)])
            checked = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=args.timeout_seconds + 60,
                check=False,
            )
            transcript = checked.stdout + checked.stderr
            if checked.returncode != 0 or "s VERIFIED" not in transcript:
                raise RuntimeError("drat-trim did not verify the proof\n" + transcript)
            if terminal_cnf.sha256(checker_snapshot) != checker_hash:
                raise RuntimeError("executed checker snapshot changed")
            if terminal_cnf.sha256(checker_path) != checker_hash:
                raise RuntimeError("checker source changed during proof checking")
            if terminal_cnf.sha256(args.dimacs) != dimacs_hash:
                raise RuntimeError("DIMACS changed during DRAT checking")
            if terminal_cnf.sha256(args.proof) != proof_source_hash:
                raise RuntimeError("proof source changed during DRAT checking")
            if (
                hashlib.sha256(args.terminal_result.read_bytes()).hexdigest()
                != terminal_result_hash
            ):
                raise RuntimeError("terminal result changed during DRAT checking")
            result.update(
                {
                    "status": "VERIFIED_DRAT",
                    "checker": {
                        "path": str(checker_path.resolve()),
                        "sha256": checker_hash,
                        "execution": "private byte-identical snapshot",
                        "exit_code": checked.returncode,
                        "reported_verified": True,
                        "command": command,
                        "transcript": transcript,
                    },
                }
            )
        result["seconds"] = round(time.perf_counter() - started, 6)
        if terminal_cnf.sha256(source_path) != source_hash:
            raise RuntimeError("proof verifier source changed during checking")
        result["command"] = sys.argv
        result["source_sha256"] = source_hash
        result["environment"] = {
            "python": platform.python_version(),
            "platform": platform.platform(),
        }
        terminal_cnf.atomic_json(args.result_out, result)
        print(json.dumps(result, indent=2), flush=True)
        return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dimacs", type=Path, required=True)
    parser.add_argument("--terminal-result", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--result-out", type=Path, required=True)
    parser.add_argument("--expect-dimacs-sha256")
    parser.add_argument("--expect-proof-sha256")
    parser.add_argument("--expect-uncompressed-sha256")
    parser.add_argument("--expect-uncompressed-bytes", type=int)
    parser.add_argument("--checker", default="drat-trim")
    parser.add_argument("--expect-checker-sha256")
    parser.add_argument("--timeout-seconds", type=int, default=10800)
    parser.add_argument("--binary", action="store_true")
    parser.add_argument("--hash-only", action="store_true")
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("timeout-seconds must be positive")
    if not args.hash_only and args.expect_checker_sha256 is None:
        parser.error("non-hash-only checking requires --expect-checker-sha256")
    paths = [
        args.dimacs.resolve(),
        args.terminal_result.resolve(),
        args.proof.resolve(),
        args.result_out.resolve(),
    ]
    if len(paths) != len(set(paths)):
        parser.error(
            "DIMACS, terminal result, proof, and check result paths must be distinct"
        )
    return args


if __name__ == "__main__":
    raise SystemExit(run(parse_args()))
