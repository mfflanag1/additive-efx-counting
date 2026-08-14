#!/usr/bin/env python3
"""Audit the chained 20,000-cut role-split R2 checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .run_allocated_e_form0_role_split_pi_cegar import BASE_OWNER, GOODS, OWNERS


def signature(family):
    return tuple(
        (source, tuple(goods)) for source, goods in sorted(family.items())
    )


def run(root, source):
    chain = []
    seen_paths = set()

    def load(path):
        path = path.resolve()
        assert path not in seen_paths
        seen_paths.add(path)
        payload = json.loads(path.read_text())
        parent = (payload.get("resume") or {}).get("source")
        if parent:
            parent_path = root / parent
            expected = payload["resume"]["source_sha256"]
            assert hashlib.sha256(parent_path.read_bytes()).hexdigest() == expected
            load(parent_path)
        chain.append((path, payload))

    load(source)
    families = {}
    structural_checks = 0
    for _, payload in chain:
        assert payload["goods"] == list(GOODS)
        for record in payload.get("iterations", ()):
            rows = record.get("closed_families")
            if rows is None:
                row = record.get("closed_family")
                rows = () if row is None else (row,)
            for family in rows:
                normalized = {
                    owner: tuple(goods) for owner, goods in family.items()
                }
                sources = set(normalized)
                assert sources and sources <= set(OWNERS)
                used = set()
                for owner, core in normalized.items():
                    assert core
                    assert len(core) == len(set(core))
                    assert set(core) <= set(GOODS)
                    assert used.isdisjoint(core)
                    used.update(core)
                    assert all(
                        BASE_OWNER[good] in sources | {"charity"}
                        for good in core
                    )
                families[signature(normalized)] = normalized
                structural_checks += 1

    terminal = chain[-1][1]
    assert terminal["status"] == "UNKNOWN"
    assert terminal["generalized_pi_cut_count"] == len(families) == 20000
    theorem = root / "results/R2_ROLE_SPLIT_20000_CUT_CHECKPOINT_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "allocated-e-form0-role-split-checkpoint-audit-v1",
        "status": "ROLE_SPLIT_20000_CUT_CHAIN_VERIFIED",
        "chain": [
            {
                "source": str(path.relative_to(root)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "status": payload["status"],
                "iteration_count": len(payload.get("iterations", ())),
            }
            for path, payload in chain
        ],
        "raw_family_records_checked": structural_checks,
        "distinct_family_count": len(families),
        "checks": {
            "resume_hashes_match": True,
            "all_families_nonempty_disjoint_and_closed": True,
            "terminal_is_fail_closed_unknown": True,
            "terminal_cut_count_matches_deduplicated_chain": True,
        },
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "Integrity and structural-validity audit of 20,000 installed PI "
            "cuts; no SAT, UNSAT, cap-free, or fixed-U conclusion."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root, args.source)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "distinct_family_count": result["distinct_family_count"],
        "raw_family_records_checked": result["raw_family_records_checked"],
    }, indent=2))


if __name__ == "__main__":
    main()
