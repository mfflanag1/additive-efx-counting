#!/usr/bin/env python3
"""Emit an exact parkable-deletion landscape for one valuation matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path

try:
    from .core import landscape, validate_instance
except ImportError:
    from core import landscape, validate_instance


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        help="write the landscape JSON here instead of standard output",
    )
    parser.add_argument(
        "--details",
        type=Path,
        help="optionally write one JSONL record for every EFX0 deletion base",
    )
    parser.add_argument("--sample-limit", type=int, default=32)
    parser.add_argument(
        "--skip-complete-count",
        action="store_true",
        help="skip the separate n^m complete-allocation count",
    )
    args = parser.parse_args()
    artifact_paths = [args.instance.resolve()]
    if args.output is not None:
        artifact_paths.append(args.output.resolve())
    if args.details is not None:
        artifact_paths.append(args.details.resolve())
    if len(artifact_paths) != len(set(artifact_paths)):
        parser.error("instance, output, and details paths must be distinct")

    source = args.instance.read_bytes()
    values = validate_instance(json.loads(source))
    detail_handle = None
    detail_temporary = None
    try:
        if args.details is not None:
            args.details.parent.mkdir(parents=True, exist_ok=True)
            detail_handle = tempfile.NamedTemporaryFile(
                mode="w",
                dir=args.details.parent,
                prefix=f".{args.details.name}.",
                suffix=".tmp",
                delete=False,
            )
            detail_temporary = Path(detail_handle.name)

        def write_detail(record: dict) -> None:
            if detail_handle is not None:
                detail_handle.write(
                    json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
                )

        result = landscape(
            values,
            sample_limit=args.sample_limit,
            detail_sink=write_detail if detail_handle is not None else None,
            include_complete_count=not args.skip_complete_count,
        )
    finally:
        if detail_handle is not None:
            detail_handle.close()
    if args.details is not None:
        assert detail_temporary is not None
        detail_temporary.replace(args.details)
        detail_bytes = args.details.read_bytes()
        detail_records = detail_bytes.count(b"\n")
        if detail_records != result["efx0_base_count"]:
            raise AssertionError("detail record count does not match landscape")
        result["details"] = {
            "path": str(args.details.resolve()),
            "sha256": hashlib.sha256(detail_bytes).hexdigest(),
            "records": detail_records,
        }
    else:
        result["details"] = None

    result["source"] = {
        "path": str(args.instance.resolve()),
        "sha256": hashlib.sha256(source).hexdigest(),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(encoded, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            dir=args.output.parent,
            prefix=f".{args.output.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(encoded)
            temporary = Path(handle.name)
        temporary.replace(args.output)
        print(
            f"PASS {result['n']}x{result['m']}: "
            f"{result['parkable_triple_count']} parkable triples, "
            f"{result['efx0_base_count']} EFX0 deletion bases"
        )


if __name__ == "__main__":
    main()
