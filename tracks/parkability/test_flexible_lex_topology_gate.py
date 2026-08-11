#!/usr/bin/env python3
"""Focused regression for the frozen mechanism-independent flower gate."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

try:
    from .analyze_flexible_lex_topology_shapes import run as run_shapes
    from .audit_flexible_lex_topology_seed import run as run_seed_audit
    from .export_flexible_lex_topology_gate import run as run_export
except ImportError:
    from analyze_flexible_lex_topology_shapes import run as run_shapes
    from audit_flexible_lex_topology_seed import run as run_seed_audit
    from export_flexible_lex_topology_gate import run as run_export


ROOT = Path(__file__).resolve().parents[2]


def main():
    seed = ROOT / "results" / "flexible_lex_topology_cegar_seed37.json"
    seed_audit = json.loads(
        (ROOT / "results" / "flexible_lex_topology_cegar_seed37_audit.json").read_text()
    )
    assert run_seed_audit(seed) == seed_audit
    shapes = json.loads(
        (ROOT / "results" / "flexible_lex_topology_shape_census.json").read_text()
    )
    assert run_shapes(seed) == shapes
    assert shapes["later_compatible_topology_class_count"] == 17
    assert shapes["later_compatible_allocation_count"] == 1294
    assert shapes["earlier_only_topology_class_count"] == 20
    assert shapes["earlier_only_allocation_count"] == 1220
    export = json.loads(
        (ROOT / "results" / "flexible_lex_gate37_live_export.json").read_text()
    )
    with tempfile.TemporaryDirectory() as directory:
        replay = run_export(
            seed,
            Path(directory) / "gate.smt2",
            atom_order_symmetry=True,
            live_polarity=True,
        )
    assert replay == export
    portfolio = json.loads(
        (ROOT / "results" / "flexible_lex_gate37_live_solver_portfolio.json").read_text()
    )
    assert portfolio["status"] == "OPEN"
    assert portfolio["gate"]["smt2_sha256"] == export["smt2_sha256"]
    assert portfolio["gate"]["global_item_symmetry_constraints"] == 8
    print("flexible lex topology gate tests passed")


if __name__ == "__main__":
    main()
