#!/usr/bin/env python3
"""Validate the exact-real manifest, campaign lineage, and semantic trace cuts."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


TRACE_SPECS = [
    (
        "results/countcegar_real_4x7_slots_60s.jsonl",
        "results/countpool_K4_complete.json",
        "results/countpool_real_4x7_slots.json",
        "results/countcegar_real_4x7_slots_60s.json",
    ),
    (
        "results/countcegar_real_4x7_cardinality_60s.jsonl",
        "results/countpool_K4_complete.json",
        "results/countpool_real_4x7_cardinality.json",
        "results/countcegar_real_4x7_cardinality_60s.json",
    ),
    (
        "results/countcegar_real_4x7_union_slots.jsonl",
        "results/countpool_real_4x7_union.json",
        "results/countpool_real_4x7_union_slots.json",
        "results/countcegar_real_4x7_union_slots.json",
    ),
    (
        "results/countcegar_real_4x7_union_cardinality.jsonl",
        "results/countpool_real_4x7_union.json",
        "results/countpool_real_4x7_union_cardinality.json",
        "results/countcegar_real_4x7_union_cardinality.json",
    ),
    (
        "results/countcegar_real_4x7_long_cardinality.jsonl",
        "results/countpool_real_4x7_checkpoint.json",
        "results/countpool_real_4x7_long_cardinality.json",
        "results/countcegar_real_4x7_long_cardinality.json",
    ),
    (
        "results/countcegar_real_4x7_final_slots.jsonl",
        "results/countpool_real_4x7_long_cardinality.json",
        "results/countpool_real_4x7_final_slots.json",
        "results/countcegar_real_4x7_final_slots.json",
    ),
    (
        "results/countcegar_real_4x7_final_cardinality.jsonl",
        "results/countpool_real_4x7_final_slots.json",
        "results/countpool_real_4x7_final_cardinality.json",
        "results/countcegar_real_4x7_final_cardinality.json",
    ),
]

REQUIRED_FILES = {
    "repro/countcegar_real/README.md",
    "repro/countcegar_real/countcegar_real.py",
    "repro/countcegar_real/requirements.txt",
    "repro/countcegar_real/test_countcegar_real.py",
    "repro/countcegar_real/validate_manifest.py",
    "verify.py",
    "verify2.py",
    "results/t47.json",
    "results/countpool_K4_complete.json",
    "results/countpool_real_4x7_slots.json",
    "results/countpool_real_4x7_cardinality.json",
    "results/countpool_real_4x7_union.json",
    "results/countpool_real_4x7_union_slots.json",
    "results/countpool_real_4x7_union_cardinality.json",
    "results/countpool_real_4x7_checkpoint.json",
    "results/countpool_real_4x7_long_cardinality.json",
    "results/countpool_real_4x7_final_slots.json",
    "results/countpool_real_4x7_final_cardinality.json",
    "results/countcegar_real_4x7_slots_60s.json",
    "results/countcegar_real_4x7_slots_60s.jsonl",
    "results/countcegar_real_4x7_slots_60s.smt2",
    "results/countcegar_real_4x7_cardinality_60s.json",
    "results/countcegar_real_4x7_cardinality_60s.jsonl",
    "results/countcegar_real_4x7_cardinality_60s.smt2",
    "results/countcegar_real_4x7_union_slots.json",
    "results/countcegar_real_4x7_union_slots.jsonl",
    "results/countcegar_real_4x7_union_cardinality.json",
    "results/countcegar_real_4x7_union_cardinality.jsonl",
    "results/countcegar_real_4x7_long_cardinality.json",
    "results/countcegar_real_4x7_long_cardinality.jsonl",
    "results/countcegar_real_4x7_long_cardinality.smt2",
    "results/countcegar_real_4x7_final_slots.json",
    "results/countcegar_real_4x7_final_slots.jsonl",
    "results/countcegar_real_4x7_final_slots.smt2",
    "results/countcegar_real_4x7_final_cardinality.json",
    "results/countcegar_real_4x7_final_cardinality.jsonl",
    "results/countcegar_real_4x7_final_cardinality.smt2",
    "results/countcegar_real_4x7_best8.json",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def digest(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def canonical_pool_bytes(pool: list[list[int]]) -> bytes:
    return (json.dumps(pool, indent=2) + "\n").encode()


def load_json(relative: str):
    return json.loads((ROOT / relative).read_text())


def validate_pool(relative: str) -> list[list[int]]:
    pool = load_json(relative)
    if not isinstance(pool, list):
        fail(f"{relative}: pool is not a list")
    seen = set()
    for index, assignment in enumerate(pool):
        if (
            not isinstance(assignment, list)
            or len(assignment) != 7
            or any(type(owner) is not int or not 0 <= owner < 4 for owner in assignment)
        ):
            fail(f"{relative}: invalid allocation {index}")
        key = tuple(assignment)
        if key in seen:
            fail(f"{relative}: duplicate allocation {index}")
        seen.add(key)
    return pool


def validate_file_inventory(manifest: dict) -> None:
    entries = manifest.get("files")
    if not isinstance(entries, list):
        fail("manifest files is not a list")
    paths = [entry.get("path") for entry in entries]
    if len(paths) != len(set(paths)):
        fail("manifest contains duplicate file paths")
    missing = sorted(REQUIRED_FILES - set(paths))
    if missing:
        fail(f"manifest omits required files: {missing}")
    for entry in entries:
        path = ROOT / entry["path"]
        contents = path.read_bytes()
        if len(contents) != entry["bytes"]:
            fail(f"{entry['path']}: byte count mismatch")
        if digest(contents) != entry["sha256"]:
            fail(f"{entry['path']}: SHA-256 mismatch")


def validate_candidate(candidate: dict) -> set[tuple[int, ...]]:
    values = candidate["integer_values"]
    if (
        len(values) != 4
        or any(len(row) != 7 for row in values)
        or any(type(value) is not int or value <= 0 for row in values for value in row)
    ):
        fail("trace candidate is not a positive integer 4x7 matrix")
    survivors = set()
    for assignment in itertools.product(range(4), repeat=7):
        bundles = [[] for _ in range(4)]
        for good, owner in enumerate(assignment):
            bundles[owner].append(good)
        is_efx0 = True
        for observer in range(4):
            own = sum(values[observer][good] for good in bundles[observer])
            for owner in range(4):
                if observer == owner:
                    continue
                for removed_good in bundles[owner]:
                    target = sum(
                        values[observer][good]
                        for good in bundles[owner]
                        if good != removed_good
                    )
                    if own < target:
                        is_efx0 = False
                        break
                if not is_efx0:
                    break
            if not is_efx0:
                break
        if is_efx0:
            survivors.add(assignment)
    if len(survivors) != candidate["efx0_count"]:
        fail("trace candidate EFX0 count mismatch")
    return survivors


def validate_trace(
    trace_path: str, seed_path: str, output_path: str, result_path: str
) -> int:
    pool = validate_pool(seed_path)
    known = {tuple(assignment) for assignment in pool}
    records = [
        json.loads(line)
        for line in (ROOT / trace_path).read_text().splitlines()
        if line
    ]
    last_checked_size = None
    last_checked_hash = None
    for cumulative_round, record in enumerate(records, 1):
        last_checked_size = len(pool)
        last_checked_hash = digest(canonical_pool_bytes(pool))
        survivors = validate_candidate(record["candidate"])
        pooled = sum(tuple(assignment) in survivors for assignment in pool)
        if pooled != record["candidate"]["pooled_efx0_count"]:
            fail(f"{trace_path}:{cumulative_round}: pooled count mismatch")
        additions = record["added"]
        if len(additions) != len({tuple(assignment) for assignment in additions}):
            fail(f"{trace_path}:{cumulative_round}: duplicate additions")
        for assignment in additions:
            key = tuple(assignment)
            if key in known:
                fail(f"{trace_path}:{cumulative_round}: cut was already pooled")
            if key not in survivors:
                fail(f"{trace_path}:{cumulative_round}: cut is not EFX0")
            known.add(key)
            pool.append(assignment)
        if record["pool_size"] != len(pool):
            fail(f"{trace_path}:{cumulative_round}: pool size mismatch")
        if record["pool_sha256"] != digest(canonical_pool_bytes(pool)):
            fail(f"{trace_path}:{cumulative_round}: pool hash mismatch")
        if "cumulative_round" in record and record["cumulative_round"] != cumulative_round:
            fail(f"{trace_path}:{cumulative_round}: cumulative round mismatch")

    if pool != validate_pool(output_path):
        fail(f"{trace_path}: reconstructed output pool mismatch")
    result = load_json(result_path)
    if result["pool_size"] != len(pool):
        fail(f"{result_path}: result pool size mismatch")
    if result["pool_sha256"] != digest((ROOT / output_path).read_bytes()):
        fail(f"{result_path}: result pool hash mismatch")
    if "checked_pool_size" in result and (
        result["checked_pool_size"] != last_checked_size
        or result["checked_pool_sha256"] != last_checked_hash
        or result["cuts_added_after_last_check"] != len(records[-1]["added"])
        or result["export_formula_checked"] is not False
        or result["export_formula_stage"] != "post_cut_pool"
        or result["last_candidate"] != records[-1]["candidate"]
    ):
        fail(f"{result_path}: checked/post-cut provenance mismatch")
    return len(records)


def validate_union(left: str, right: str, union: str) -> None:
    expected = {
        tuple(assignment)
        for path in (left, right)
        for assignment in validate_pool(path)
    }
    actual = {tuple(assignment) for assignment in validate_pool(union)}
    if actual != expected:
        fail(f"{union}: is not the exact set union of its branch pools")


def validate_best8() -> None:
    artifact = load_json("results/countcegar_real_4x7_best8.json")
    provenance = artifact["provenance"]
    trace_path = ROOT / provenance["trace"]
    if digest(trace_path.read_bytes()) != provenance["trace_sha256"]:
        fail("best8 trace hash mismatch")
    matches = []
    for line in trace_path.read_text().splitlines():
        record = json.loads(line)
        if (
            record["round"] == provenance["trace_round"]
            and record["pool_size"] == provenance["pool_size_after_cut"]
            and record["pool_sha256"] == provenance["pool_sha256_after_cut"]
            and record["candidate"]["integer_values"] == artifact["values"]
        ):
            matches.append(record)
    if len(matches) != 1:
        fail("best8 provenance does not identify exactly one trace record")
    candidate = {
        "integer_values": artifact["values"],
        "efx0_count": artifact["efx0_count"],
    }
    survivors = validate_candidate(candidate)
    if survivors != {tuple(assignment) for assignment in artifact["efx0_allocations"]}:
        fail("best8 allocation list mismatch")


def main() -> None:
    manifest = load_json("repro/countcegar_real/MANIFEST.json")
    validate_file_inventory(manifest)
    total_rounds = sum(validate_trace(*spec) for spec in TRACE_SPECS)
    if total_rounds != 80:
        fail(f"retained trace count is {total_rounds}, not 80")
    if manifest["campaign"]["retained_sat_refinement_rounds"] != total_rounds:
        fail("manifest retained-round count mismatch")
    validate_union(
        "results/countpool_real_4x7_slots.json",
        "results/countpool_real_4x7_cardinality.json",
        "results/countpool_real_4x7_union.json",
    )
    validate_union(
        "results/countpool_real_4x7_union_slots.json",
        "results/countpool_real_4x7_union_cardinality.json",
        "results/countpool_real_4x7_checkpoint.json",
    )
    validate_best8()
    final_pool = validate_pool(manifest["campaign"]["final_pool_path"])
    if len(final_pool) != manifest["campaign"]["final_pool_size"]:
        fail("manifest final pool size mismatch")
    if (
        digest((ROOT / manifest["campaign"]["final_pool_path"]).read_bytes())
        != manifest["campaign"]["final_pool_sha256"]
    ):
        fail("manifest final pool hash mismatch")
    print(
        "PASS exact-real closure: "
        f"{len(manifest['files'])} files, {total_rounds} semantic trace "
        f"recounts, final pool {len(final_pool)}"
    )


if __name__ == "__main__":
    main()
