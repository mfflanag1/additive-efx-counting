#!/usr/bin/env python3
"""Compose nested exact SMT cube covers into one auditable leaf manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

try:
    from .anneal import atomic_json
except ImportError:
    from anneal import atomic_json


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_cover(path):
    cover = json.loads(path.read_text())
    if (
        cover.get("schema") != "smt2-cube-cover-v1"
        or cover.get("status") != "EXACT_CUBE_COVER"
        or cover.get("branch_count") != len(cover.get("branches", ()))
    ):
        raise ValueError(f"invalid exact cube cover: {path}")
    return cover


def compose(parent_path, child_paths):
    parent = load_cover(parent_path)
    if len(child_paths) != parent["branch_count"]:
        raise ValueError("one child cover is required for every parent branch")
    leaves = []
    child_records = []
    for parent_branch, child_path in zip(parent["branches"], child_paths):
        child = load_cover(child_path)
        parent_formula = Path(parent_branch["path"])
        child_source = Path(child["source"])
        if child_source.resolve() != parent_formula.resolve():
            raise ValueError(f"child source path mismatch: {child_path}")
        if child["source_sha256"] != parent_branch["sha256"]:
            raise ValueError(f"child source hash mismatch: {child_path}")
        if sha256(parent_formula) != parent_branch["sha256"]:
            raise ValueError(f"parent branch file hash mismatch: {parent_formula}")
        child_records.append(
            {
                "parent_branch": parent_branch["branch"],
                "manifest": str(child_path),
                "manifest_sha256": sha256(child_path),
                "branch_count": child["branch_count"],
            }
        )
        for child_branch in child["branches"]:
            leaf_path = Path(child_branch["path"])
            if sha256(leaf_path) != child_branch["sha256"]:
                raise ValueError(f"leaf file hash mismatch: {leaf_path}")
            leaves.append(
                {
                    "leaf": len(leaves),
                    "parent_branch": parent_branch["branch"],
                    "child_branch": child_branch["branch"],
                    "path": str(leaf_path),
                    "sha256": child_branch["sha256"],
                    "cube": parent_branch["cube"] + child_branch["cube"],
                }
            )
    return {
        "schema": "smt2-composed-cube-cover-v1",
        "status": "EXACT_COMPOSED_CUBE_COVER",
        "meaning": (
            "Every child exactly covers its parent branch and the parent "
            "exactly covers the source. Therefore the listed leaves exactly "
            "cover the source: SAT of one leaf is SAT of the source, while "
            "UNSAT of every leaf is UNSAT of the source."
        ),
        "source": parent["source"],
        "source_sha256": parent["source_sha256"],
        "parent_manifest": str(parent_path),
        "parent_manifest_sha256": sha256(parent_path),
        "children": child_records,
        "leaf_count": len(leaves),
        "leaves": leaves,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--child", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compose(args.parent, args.child)
    atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
