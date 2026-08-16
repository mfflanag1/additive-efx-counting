#!/usr/bin/env python3
"""Rebuild and audit a compact adaptive-priority first-agent core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import z3

try:
    from . import core
    from .anneal import atomic_json
    from .lra_master import ParkabilityLRAMaster
    from .normalize_smt2_for_cvc5 import normalize
    from .run_adaptive_priority_cegar import derive_unique_seed_cells
    from .run_lexmax_partial_cegar import (
        add_candidate,
        add_rival_blocker,
        bundles_of,
        subset_sum,
    )
    from .shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )
except ImportError:
    import core
    from anneal import atomic_json
    from lra_master import ParkabilityLRAMaster
    from normalize_smt2_for_cvc5 import normalize
    from run_adaptive_priority_cegar import derive_unique_seed_cells
    from run_lexmax_partial_cegar import (
        add_candidate,
        add_rival_blocker,
        bundles_of,
        subset_sum,
    )
    from shrink_adaptive_priority_inequality_core import (
        assumption_records,
        public_record,
    )


SCHEMA = "adaptive-priority-first-agent-core-audit-v1"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run(
    *,
    seed_path: Path,
    core_path: Path,
    raw_formula_path: Path,
    normalized_formula_path: Path,
    normalization_path: Path,
    cvc5_path: Path,
    inequality_core_path: Path,
    inequality_raw_formula_path: Path,
    inequality_normalized_formula_path: Path,
    inequality_normalization_path: Path,
    inequality_cvc5_path: Path,
    output_path: Path,
    time_limit_s: float,
) -> dict:
    if time_limit_s <= 0:
        raise ValueError("a positive time limit is required")
    raw_seed = json.loads(seed_path.read_text())
    raw_values = raw_seed.get("values", raw_seed.get("candidate_values"))
    if raw_values is None:
        raise ValueError("seed JSON contains no values")
    values = core.validate_values(raw_values, lower=1)
    n = len(values)
    m = len(values[0])

    document = json.loads(core_path.read_text())
    if (
        document.get("schema") != "adaptive-priority-rival-core-v1"
        or document.get("status") != "UNSAT_DELETION_MINIMAL_RIVAL_CORE"
        or document.get("n") != n
        or document.get("m") != m
        or document.get("seed_sha256") != sha256_path(seed_path)
        or not document.get("require_distinct_item_values")
        or not document.get("preserve_rival_dependencies")
    ):
        raise ValueError("compact-core metadata mismatch")

    first_agents = tuple(document.get("first_agent_filter", []))
    if len(first_agents) != len(set(first_agents)) or any(
        not 0 <= agent < n for agent in first_agents
    ):
        raise ValueError("invalid first-agent filter")
    selected = set(first_agents)
    all_cells = derive_unique_seed_cells(values)
    cells = [
        cell
        for cell in all_cells
        if not selected or cell[0][0] in selected
    ]
    unique_candidates = list(dict.fromkeys(candidate for _, candidate in cells))
    if (
        document.get("cell_count") != len(cells)
        or document.get("candidate_count") != len(unique_candidates)
    ):
        raise ValueError("seed-derived cell census mismatch")

    records = document.get("core")
    if not isinstance(records, list) or not records:
        raise ValueError("compact core is empty")
    if any(record.get("kind") != "rival" for record in records):
        raise ValueError("this auditor expects a rival-only compact core")
    dependency_indices = {record.get("candidate_index") for record in records}
    if (
        sorted(dependency_indices)
        != document.get("dependency_candidate_indices")
        or len(dependency_indices)
        != document.get("dependency_closed_candidate_count")
        or len(records) != document.get("deletion_minimal_rival_count")
    ):
        raise ValueError("candidate-dependency census mismatch")

    master = ParkabilityLRAMaster(
        n,
        m,
        require_distinct_item_values=True,
    )
    utilities = {}
    for candidate_index, candidate in enumerate(unique_candidates):
        if candidate_index in dependency_indices:
            utilities[candidate] = add_candidate(master, *candidate)
        else:
            bundles = bundles_of(candidate[1], n)
            utilities[candidate] = tuple(
                subset_sum(master, observer, bundles[observer])
                for observer in range(n)
            )

    seen = set()
    for record in records:
        cell_index = record.get("cell_index")
        candidate_index = record.get("candidate_index")
        if (
            not isinstance(cell_index, int)
            or not 0 <= cell_index < len(cells)
            or not isinstance(candidate_index, int)
            or not 0 <= candidate_index < len(unique_candidates)
        ):
            raise ValueError("invalid compact-core index")
        order, candidate = cells[cell_index]
        if (
            record.get("agent_order") != list(order)
            or unique_candidates[candidate_index] != candidate
        ):
            raise ValueError("compact-core cell identity mismatch")
        rival_document = record.get("rival")
        if not isinstance(rival_document, dict):
            raise ValueError("compact-core rival is missing")
        core.validate_triple(
            {
                "floater": rival_document.get("floater"),
                "base_owner": rival_document.get("base_owner"),
                "host": 0,
            },
            n,
            m,
        )
        rival = (
            rival_document["floater"],
            tuple(rival_document["base_owner"]),
        )
        identity = (cell_index, rival)
        if identity in seen or rival == candidate:
            raise ValueError("duplicate or self-rival compact-core record")
        seen.add(identity)
        add_rival_blocker(
            master,
            utilities[candidate],
            candidate[1],
            rival,
            order,
            "exact",
        )

    solved = master.solve(time_limit_s=time_limit_s)
    if solved.status != "UNSAT":
        raise AssertionError(f"rebuilt compact core is {solved.status}")
    archived_raw = raw_formula_path.read_bytes()
    rebuilt_assertions = master.solver.assertions()
    archived_assertions = z3.parse_smt2_file(str(raw_formula_path))
    mismatch_indices = [
        index
        for index, (rebuilt, archived) in enumerate(
            zip(rebuilt_assertions, archived_assertions)
        )
        if not z3.eq(z3.simplify(rebuilt), z3.simplify(archived))
    ]
    if len(rebuilt_assertions) != len(archived_assertions) or mismatch_indices:
        first_mismatch = mismatch_indices[0] if mismatch_indices else None
        raise AssertionError(
            "rebuilt and archived assertion sequences differ structurally: "
            f"counts={len(rebuilt_assertions)}/{len(archived_assertions)}, "
            f"first_mismatch={first_mismatch}, "
            f"rebuilt={rebuilt_assertions[first_mismatch] if first_mismatch is not None else None}, "
            f"archived={archived_assertions[first_mismatch] if first_mismatch is not None else None}"
        )
    normalized_text, replacement_count = normalize(archived_raw.decode())
    rebuilt_normalized = normalized_text.encode()
    archived_normalized = normalized_formula_path.read_bytes()
    if rebuilt_normalized != archived_normalized:
        raise AssertionError("rebuilt and archived normalized formulas differ")

    normalization = json.loads(normalization_path.read_text())
    if (
        normalization.get("source_sha256") != sha256_bytes(archived_raw)
        or normalization.get("output_sha256")
        != sha256_bytes(archived_normalized)
        or normalization.get("transformation", {}).get(
            "unary_value_sum_identity_replacements"
        )
        != replacement_count
    ):
        raise ValueError("normalization ledger mismatch")
    cvc5 = json.loads(cvc5_path.read_text())
    if (
        cvc5.get("verdict") != "unsat"
        or not cvc5.get("confirmed_expected")
        or cvc5.get("timed_out")
        or cvc5.get("formula_sha256") != sha256_bytes(archived_normalized)
    ):
        raise ValueError("cvc5 replay ledger mismatch")

    inequality_document = json.loads(inequality_core_path.read_text())
    if (
        inequality_document.get("schema")
        != "adaptive-priority-inequality-core-v1"
        or inequality_document.get("status")
        != "UNSAT_DELETION_MINIMAL_INEQUALITY_CORE"
        or inequality_document.get("n") != n
        or inequality_document.get("m") != m
        or inequality_document.get("seed_sha256") != sha256_path(seed_path)
        or inequality_document.get("compact_core_sha256")
        != sha256_path(core_path)
    ):
        raise ValueError("inequality-core metadata mismatch")
    inequality_master = ParkabilityLRAMaster(n, m)
    all_inequality_records = assumption_records(
        inequality_master,
        all_cells,
        document,
    )
    active_inequality_records = inequality_document.get("core")
    if not isinstance(active_inequality_records, list):
        raise ValueError("inequality core is missing")
    for record in active_inequality_records:
        assumption_index = record.get("assumption_index")
        if (
            not isinstance(assumption_index, int)
            or not 0 <= assumption_index < len(all_inequality_records)
        ):
            raise ValueError("invalid inequality-core assumption index")
        source_record = all_inequality_records[assumption_index]
        if {
            key: value
            for key, value in record.items()
            if key != "assumption_index"
        } != public_record(source_record):
            raise ValueError("inequality-core semantic record mismatch")
        inequality_master.solver.add(source_record["expression"])
    inequality_solved = inequality_master.solve(time_limit_s=time_limit_s)
    if inequality_solved.status != "UNSAT":
        raise AssertionError(
            f"rebuilt inequality core is {inequality_solved.status}"
        )
    inequality_raw = inequality_raw_formula_path.read_bytes()
    rebuilt_inequality_assertions = inequality_master.solver.assertions()
    archived_inequality_assertions = z3.parse_smt2_file(
        str(inequality_raw_formula_path)
    )
    if len(rebuilt_inequality_assertions) != len(
        archived_inequality_assertions
    ) or any(
        not z3.eq(z3.simplify(rebuilt), z3.simplify(archived))
        for rebuilt, archived in zip(
            rebuilt_inequality_assertions,
            archived_inequality_assertions,
        )
    ):
        raise AssertionError(
            "rebuilt and archived inequality assertions differ structurally"
        )
    inequality_normalized_text, inequality_replacement_count = normalize(
        inequality_raw.decode()
    )
    inequality_normalized = inequality_normalized_formula_path.read_bytes()
    if inequality_normalized_text.encode() != inequality_normalized:
        raise AssertionError("inequality normalization replay differs")
    inequality_normalization = json.loads(
        inequality_normalization_path.read_text()
    )
    if (
        inequality_normalization.get("source_sha256")
        != sha256_bytes(inequality_raw)
        or inequality_normalization.get("output_sha256")
        != sha256_bytes(inequality_normalized)
        or inequality_normalization.get("transformation", {}).get(
            "unary_value_sum_identity_replacements"
        )
        != inequality_replacement_count
    ):
        raise ValueError("inequality normalization ledger mismatch")
    inequality_cvc5 = json.loads(inequality_cvc5_path.read_text())
    if (
        inequality_cvc5.get("verdict") != "unsat"
        or not inequality_cvc5.get("confirmed_expected")
        or inequality_cvc5.get("timed_out")
        or inequality_cvc5.get("formula_sha256")
        != sha256_bytes(inequality_normalized)
    ):
        raise ValueError("inequality cvc5 replay ledger mismatch")
    inequality_kinds = {
        kind: sum(
            record.get("kind") == kind
            for record in active_inequality_records
        )
        for kind in ("candidate_constraint", "rival_blocker")
    }

    result = {
        "schema": SCHEMA,
        "status": "PASS",
        "meaning": (
            "the 18-rival fixed-cell formula was rebuilt from the seed and "
            "semantic core, matched simplified assertion-for-assertion, and "
            "is UNSAT in both Z3 and the archived cvc5 replay; this does not "
            "cover other candidate identities"
        ),
        "n": n,
        "m": m,
        "first_agent_filter": list(first_agents),
        "cell_count": len(cells),
        "candidate_count": len(unique_candidates),
        "rival_count": len(records),
        "structural_assertion_count": len(rebuilt_assertions),
        "structural_assertion_match": True,
        "z3_status": solved.status.lower(),
        "cvc5_status": cvc5["verdict"],
        "seed_sha256": sha256_path(seed_path),
        "core_sha256": sha256_path(core_path),
        "raw_formula_sha256": sha256_bytes(archived_raw),
        "normalized_formula_sha256": sha256_bytes(archived_normalized),
        "normalization_sha256": sha256_path(normalization_path),
        "cvc5_replay_sha256": sha256_path(cvc5_path),
        "inequality_core": {
            "assumption_count": len(active_inequality_records),
            "candidate_constraint_count": inequality_kinds[
                "candidate_constraint"
            ],
            "rival_blocker_count": inequality_kinds["rival_blocker"],
            "structural_assertion_count": len(
                rebuilt_inequality_assertions
            ),
            "structural_assertion_match": True,
            "z3_status": inequality_solved.status.lower(),
            "cvc5_status": inequality_cvc5["verdict"],
            "core_sha256": sha256_path(inequality_core_path),
            "raw_formula_sha256": sha256_bytes(inequality_raw),
            "normalized_formula_sha256": sha256_bytes(
                inequality_normalized
            ),
            "normalization_sha256": sha256_path(
                inequality_normalization_path
            ),
            "cvc5_replay_sha256": sha256_path(inequality_cvc5_path),
        },
    }
    atomic_json(output_path, result)
    print(json.dumps(result, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--core", type=Path, required=True)
    parser.add_argument("--raw-formula", type=Path, required=True)
    parser.add_argument("--normalized-formula", type=Path, required=True)
    parser.add_argument("--normalization", type=Path, required=True)
    parser.add_argument("--cvc5", type=Path, required=True)
    parser.add_argument("--inequality-core", type=Path, required=True)
    parser.add_argument("--inequality-raw-formula", type=Path, required=True)
    parser.add_argument(
        "--inequality-normalized-formula",
        type=Path,
        required=True,
    )
    parser.add_argument("--inequality-normalization", type=Path, required=True)
    parser.add_argument("--inequality-cvc5", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--time-limit", type=float, default=60.0)
    args = parser.parse_args()
    run(
        seed_path=args.seed,
        core_path=args.core,
        raw_formula_path=args.raw_formula,
        normalized_formula_path=args.normalized_formula,
        normalization_path=args.normalization,
        cvc5_path=args.cvc5,
        inequality_core_path=args.inequality_core,
        inequality_raw_formula_path=args.inequality_raw_formula,
        inequality_normalized_formula_path=(
            args.inequality_normalized_formula
        ),
        inequality_normalization_path=args.inequality_normalization,
        inequality_cvc5_path=args.inequality_cvc5,
        output_path=args.output,
        time_limit_s=args.time_limit,
    )


if __name__ == "__main__":
    main()
