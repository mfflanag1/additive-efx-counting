#!/usr/bin/env python3
"""Normalize archived Z3 SMT-LIB into strict QF_LRA/QF_LIA for cvc5."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path


UNARY_VALUE_SUM = re.compile(r"\(\+\s+(value_\d+_\d+)\s*\)")
ANY_UNARY_ATOM_SUM = re.compile(r"\(\+\s+[^()\s]+\s*\)")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def normalize(source: str) -> tuple[str, int]:
    if "(set-logic " in source:
        raise ValueError("source already declares a logic")
    if source.count("(check-sat)") != 1:
        raise ValueError("source must contain exactly one check-sat command")
    if "(_ at-most" in source or "(_ at-least" in source:
        raise ValueError("source contains a nonstandard Z3 cardinality operator")
    normalized, replacement_count = UNARY_VALUE_SUM.subn(r"\1", source)
    remaining = ANY_UNARY_ATOM_SUM.search(normalized)
    if remaining is not None:
        raise ValueError(f"unsupported unary sum remains: {remaining.group(0)}")
    lines = normalized.splitlines(keepends=True)
    insertion = 1 if lines and lines[0].startswith(";") else 0
    logic = (
        "QF_LIA"
        if re.search(r"\(declare-fun\s+\S+\s+\(\)\s+Int\)", source)
        else "QF_LRA"
    )
    lines.insert(insertion, f"(set-logic {logic})\n")
    return "".join(lines), replacement_count


def run(*, source_path: Path, output_path: Path, metadata_path: Path) -> dict:
    if (
        not source_path.is_file()
        or output_path.exists()
        or metadata_path.exists()
        or output_path.resolve() == metadata_path.resolve()
    ):
        raise ValueError("existing source and distinct new outputs are required")
    source_bytes = source_path.read_bytes()
    source = source_bytes.decode("utf-8")
    normalized, replacement_count = normalize(source)
    normalized_bytes = normalized.encode("utf-8")
    metadata = {
        "schema": "strict-smt2-normalization-v1",
        "source": str(source_path.resolve()),
        "source_sha256": sha256(source_bytes),
        "output": str(output_path.resolve()),
        "output_sha256": sha256(normalized_bytes),
        "transformation": {
            "inserted_logic": (
                "QF_LIA"
                if re.search(
                    r"\(declare-fun\s+\S+\s+\(\)\s+Int\)",
                    source,
                )
                else "QF_LRA"
            ),
            "unary_value_sum_identity_replacements": replacement_count,
        },
        "meaning": (
            "syntax-only normalization: every (+ value_i_g) is replaced by "
            "the identical term value_i_g"
        ),
    }
    atomic_write(output_path, normalized_bytes)
    atomic_write(
        metadata_path,
        (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode(),
    )
    print(json.dumps(metadata, indent=2, sort_keys=True), flush=True)
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    args = parser.parse_args()
    run(
        source_path=args.source,
        output_path=args.output,
        metadata_path=args.metadata,
    )


if __name__ == "__main__":
    main()
