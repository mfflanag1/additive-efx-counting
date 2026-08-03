#!/usr/bin/env python3
"""Compare JSON certificates while ignoring checkout-root path prefixes.

The certificate payloads sometimes retain absolute paths to repository inputs.
Those prefixes are provenance metadata, not mathematical content, and differ in
clean CI checkouts.  This comparator removes only the prefix before a known
repository directory; every remaining JSON value is compared exactly.
"""

from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any


REPOSITORY_DIRECTORIES = {
    "artifacts",
    "formal",
    "paper",
    "repro",
    "results",
    "supplement",
    "tracks",
}


def portable_path(value: str) -> str:
    if not value.startswith("/"):
        return value
    parts = PurePosixPath(value).parts
    for index, part in enumerate(parts):
        if part in REPOSITORY_DIRECTORIES:
            return PurePosixPath(*parts[index:]).as_posix()
    return value


def normalize(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, str):
        return portable_path(value)
    return value


def canonical(path: Path) -> str:
    value = normalize(json.loads(path.read_text()))
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: compare_json_portable.py EXPECTED OBSERVED")
    expected_path, observed_path = map(Path, sys.argv[1:])
    expected = canonical(expected_path)
    observed = canonical(observed_path)
    if expected == observed:
        return
    sys.stdout.writelines(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            observed.splitlines(keepends=True),
            fromfile=str(expected_path),
            tofile=str(observed_path),
        )
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
