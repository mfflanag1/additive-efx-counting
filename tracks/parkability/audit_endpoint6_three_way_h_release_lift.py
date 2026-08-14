#!/usr/bin/env python3
"""Audit the physical packet interpretation of the endpoint-6 release core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .run_allocated_e_endpoint6_root_fixed_completion_cegar import support_edges


ROOT = Path(__file__).resolve().parents[2]

EXPECTED = (
    {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["h", "l", "m", "gq", "gr"],
        "s": ["e", "p"],
        "charity": [],
    },
    {
        "r": ["a0", "a1"],
        "q": ["j", "k", "q0"],
        "d": ["l", "m", "gq", "gr"],
        "s": ["h", "e", "p"],
        "charity": [],
    },
    {
        "r": ["a0", "a1"],
        "q": ["h", "k", "q0", "m", "p"],
        "d": ["j", "gq", "gr"],
        "s": ["l", "e"],
        "charity": [],
    },
)

PACKET_FORMS = (
    "(A,Q,H+L+W,(E-L)+P)",
    "(A,Q,L+W,H+(E-L)+P)",
    "(A,H+(Q-J)+M+P,J+(W-M),E)",
)


def canonical(allocation):
    return {
        owner: list(allocation[owner])
        for owner in ("r", "q", "d", "s", "charity")
    }


def run(core_source: Path, independent_source: Path, output: Path):
    core_source = core_source.resolve()
    independent_source = independent_source.resolve()
    core = json.loads(core_source.read_text())
    independent = json.loads(independent_source.read_text())
    assert core["status"] == "UNSAT_CORE_EXTRACTED"
    assert independent["status"] == "AUDIT_PASSED"
    assert independent["core_source_sha256"] == hashlib.sha256(
        core_source.read_bytes()
    ).hexdigest()
    allocations = tuple(canonical(row) for row in core["allocations"])
    assert allocations == EXPECTED

    rows = []
    for packet_form, allocation in zip(PACKET_FORMS, allocations):
        edges = tuple(sorted(support_edges(allocation)))
        assert allocation["r"] == ["a0", "a1"]
        assert "h" not in allocation["r"]
        assert len(edges) <= 4
        rows.append({
            "packet_form": packet_form,
            "support_edges": [list(edge) for edge in edges],
            "support_edge_count": len(edges),
        })

    result = {
        "schema": "endpoint6-three-way-h-release-lift-audit-v1",
        "status": "AUDIT_PASSED",
        "core_source": str(core_source.relative_to(ROOT)),
        "core_source_sha256": hashlib.sha256(core_source.read_bytes()).hexdigest(),
        "independent_source": str(independent_source.relative_to(ROOT)),
        "independent_source_sha256": hashlib.sha256(
            independent_source.read_bytes()
        ).hexdigest(),
        "pi_clause_count": core["core_pi_clause_count"],
        "allocation_count": len(allocations),
        "root_packet_preserved": "A",
        "root_packet_released": "H",
        "rows": rows,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Audits only the exact packet identities and support-edge counts of "
            "the dual-verified bounded core. The physical lift additionally uses "
            "the separately proved hidden-minimum and Hall-lift lemmas."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-source", type=Path, required=True)
    parser.add_argument("--independent-source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(
        args.core_source, args.independent_source, args.output
    ), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
