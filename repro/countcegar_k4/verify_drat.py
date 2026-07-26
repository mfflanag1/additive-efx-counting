#!/usr/bin/env python3
"""Check the archived compressed DRAT proof, optionally with drat-trim."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
METADATA = (
    ROOT
    / "repro/countcegar_k4/certificates/DRAT_CERTIFICATE.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_file_record(path: Path, record: dict, prefix: str = "") -> None:
    expected_bytes = record[f"{prefix}bytes"]
    expected_hash = record[f"{prefix}sha256"]
    if not path.is_file():
        raise FileNotFoundError(path)
    if path.stat().st_size != expected_bytes:
        raise ValueError(f"size mismatch for {path}")
    if sha256(path) != expected_hash:
        raise ValueError(f"SHA-256 mismatch for {path}")


def decompress_and_hash(source: Path, target: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with lzma.open(source, "rb") as compressed, target.open("wb") as output:
        for chunk in iter(lambda: compressed.read(1 << 20), b""):
            output.write(chunk)
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--checker",
        default="drat-trim",
        help="drat-trim executable or path",
    )
    parser.add_argument("--timeout-seconds", type=int, default=10800)
    parser.add_argument(
        "--hash-only",
        action="store_true",
        help="check and decompress the archive without checking the proof",
    )
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("timeout must be positive")

    metadata = json.loads(METADATA.read_text())
    if metadata.get("schema") != 1 or metadata.get("status") != "VERIFIED":
        raise ValueError("unexpected certificate metadata")
    cnf = ROOT / metadata["input"]["path"]
    archive = ROOT / metadata["proof"]["path"]
    require_file_record(cnf, metadata["input"])
    require_file_record(archive, metadata["proof"], "compressed_")

    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="countcegar-k4-drat-") as directory:
        proof = Path(directory) / "proof.binary.drat"
        proof_bytes, proof_hash = decompress_and_hash(archive, proof)
        if proof_bytes != metadata["proof"]["uncompressed_bytes"]:
            raise ValueError("uncompressed proof size mismatch")
        if proof_hash != metadata["proof"]["uncompressed_sha256"]:
            raise ValueError("uncompressed proof SHA-256 mismatch")

        result = {
            "schema": 1,
            "status": "HASHES_PASS",
            "cnf_sha256": sha256(cnf),
            "compressed_proof_sha256": sha256(archive),
            "uncompressed_proof_sha256": proof_hash,
            "uncompressed_proof_bytes": proof_bytes,
        }
        if not args.hash_only:
            checker = shutil.which(args.checker)
            if checker is None:
                checker_path = Path(args.checker)
                if not checker_path.is_file():
                    raise FileNotFoundError(
                        f"drat-trim executable not found: {args.checker}"
                    )
                checker = str(checker_path.resolve())
            command = [
                checker,
                str(cnf),
                str(proof),
                "-i",
                "-t",
                str(args.timeout_seconds),
            ]
            checked = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=args.timeout_seconds + 60,
                check=False,
            )
            transcript = checked.stdout + checked.stderr
            if checked.returncode != 0 or "s VERIFIED" not in transcript:
                raise RuntimeError(
                    "drat-trim did not verify the proof\n" + transcript
                )
            result.update(
                {
                    "status": "VERIFIED",
                    "checker": checker,
                    "checker_exit_code": checked.returncode,
                    "checker_reported_verified": True,
                }
            )
        result["seconds"] = round(time.perf_counter() - started, 6)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
