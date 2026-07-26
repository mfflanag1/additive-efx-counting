#!/usr/bin/env python3
"""Run three independent exact counters on the paper's six witness matrices."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))

import fast_verify  # noqa: E402
import verify  # noqa: E402
import verify2  # noqa: E402


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_record(record: dict) -> dict:
    path = ROOT / record["path"]
    assert sha256(path) == record["sha256"], f"hash mismatch: {path}"
    instance = json.loads(path.read_text())
    n, m, values = instance["n"], instance["m"], instance["values"]
    expected = record["expected_efx0_count"]

    started = time.time()
    first = verify.enumerate_all(n, m, values)
    first_seconds = time.time() - started

    started = time.time()
    second = verify2.run_instance(n, m, values)
    second_seconds = time.time() - started

    started = time.time()
    fast_efx0, fast_efxplus, _ = fast_verify.count_both(
        values, chunk=1 << 20
    )
    vector_seconds = time.time() - started

    counts = {
        "verify.py": first["efx0_count"],
        "verify2.py": second["efx0_count"],
        "fast_verify.py": fast_efx0,
    }
    positive_counts = {
        "verify.py": first["efxplus_count"],
        "verify2.py": second["efxplus_count"],
        "fast_verify.py": fast_efxplus,
    }
    assert set(counts.values()) == {expected}, (record["id"], counts, expected)
    assert positive_counts == counts, (record["id"], positive_counts, counts)
    return {
        "id": record["id"],
        "n": n,
        "m": m,
        "allocation_space": n**m,
        "expected_efx0_count": expected,
        "counts": counts,
        "efxplus_counts": positive_counts,
        "seconds": {
            "verify.py": round(first_seconds, 3),
            "verify2.py": round(second_seconds, 3),
            "fast_verify.py": round(vector_seconds, 3),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", action="append", default=[], metavar="ID")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads((HERE / "instances.json").read_text())
    for relative, expected_hash in manifest["verifiers"].items():
        path = ROOT / relative
        assert sha256(path) == expected_hash, f"verifier hash mismatch: {path}"

    requested = set(args.only)
    records = [
        record
        for record in manifest["instances"]
        if not requested or record["id"] in requested
    ]
    assert {record["id"] for record in records} == (
        requested or {record["id"] for record in manifest["instances"]}
    )

    results = []
    for record in records:
        result = run_record(record)
        results.append(result)
        print(
            f"PASS {result['id']} ({result['n']},{result['m']}): "
            f"count={result['expected_efx0_count']} across "
            f"{result['allocation_space']:,} allocations",
            flush=True,
        )

    output = {
        "schema": 1,
        "status": "PASS",
        "environment": {
            "python": platform.python_version(),
            "numpy": fast_verify.np.__version__,
            "platform": platform.platform(),
        },
        "results": results,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2) + "\n")
    print(f"PASS all {len(results)} count-n witness checks", flush=True)


if __name__ == "__main__":
    main()
