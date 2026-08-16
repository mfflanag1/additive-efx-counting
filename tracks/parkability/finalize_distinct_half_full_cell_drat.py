#!/usr/bin/env python3
"""Verify and freeze a DRAT certificate for a bounded full-cell CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import re
import subprocess
import time
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


SCHEMA = "distinct-half-full-cell-drat-verification-v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decompressed_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with lzma.open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def run(args):
    cnf_result = json.loads(args.cnf_result.read_text())
    if (
        cnf_result.get("status") != "UNSAT"
        or cnf_result.get("dimacs_sha256") != sha256(args.cnf)
    ):
        raise ValueError("CNF result does not match the supplied formula")
    proof_hash = sha256(args.proof)
    compressed_hash = sha256(args.compressed_proof)
    if decompressed_sha256(args.compressed_proof) != proof_hash:
        raise AssertionError("compressed proof does not reproduce the DRAT file")

    started = time.time()
    checked = subprocess.run(
        [str(args.checker), str(args.cnf), str(args.proof), "-i"],
        check=False,
        capture_output=True,
        text=True,
        timeout=args.timeout,
    )
    elapsed = time.time() - started
    transcript = checked.stdout + checked.stderr
    if checked.returncode != 0 or "s VERIFIED" not in transcript:
        raise AssertionError("DRAT checker did not verify the proof")

    clauses = re.search(r"(\d+) of (\d+) clauses in core", transcript)
    lemmas = re.search(r"(\d+) of (\d+) lemmas in core", transcript)
    resolutions = re.search(r"using (\d+) resolution steps", transcript)
    if not clauses or not lemmas or not resolutions:
        raise AssertionError("DRAT checker transcript format changed")

    result = {
        "schema": SCHEMA,
        "status": "VERIFIED",
        "claim": (
            f"The cap-{cnf_result['cap']} distinct-half no-full-cell formula with the "
            f"{cnf_result['partition_pool_size']}-partition obstruction "
            "core is unsatisfiable."
        ),
        "cnf": {
            "path": display_path(args.cnf),
            "sha256": sha256(args.cnf),
            "bytes": args.cnf.stat().st_size,
            "variables": cnf_result["variables"],
            "clauses": cnf_result["clauses"],
        },
        "proof": {
            "path": display_path(args.proof),
            "sha256": proof_hash,
            "bytes": args.proof.stat().st_size,
            "compressed_path": display_path(args.compressed_proof),
            "compressed_sha256": compressed_hash,
            "compressed_bytes": args.compressed_proof.stat().st_size,
            "format": "binary DRAT",
        },
        "proof_generator": {
            "name": "CaDiCaL",
            "version": "1.9.5",
            "git_commit": "146207318796f094dcded87349a64f0c6927309e",
            "binary_sha256": sha256(args.generator),
        },
        "proof_checker": {
            "name": "drat-trim",
            "git_commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
            "binary_sha256": sha256(args.checker),
            "source_path": display_path(args.checker_source),
            "source_sha256": sha256(args.checker_source),
            "returncode": checked.returncode,
            "elapsed_seconds": elapsed,
            "core_input_clauses": int(clauses.group(1)),
            "input_clauses": int(clauses.group(2)),
            "core_lemmas": int(lemmas.group(1)),
            "proof_lemmas": int(lemmas.group(2)),
            "resolution_steps": int(resolutions.group(1)),
            "transcript": transcript,
        },
        "cnf_result_sha256": sha256(args.cnf_result),
        "encoder_source_sha256": cnf_result["encoder_source_sha256"],
        "trust_boundary": (
            "The checked proof certifies only the frozen finite "
            f"cap-{cnf_result['cap']} CNF. "
            "The separate semantic audits connect that CNF to the stated "
            "bounded EFX theorem."
        ),
    }
    atomic_json(args.output, result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--cnf-result", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--compressed-proof", type=Path, required=True)
    parser.add_argument("--generator", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--checker-source", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=600)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
