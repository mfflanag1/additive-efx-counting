#!/usr/bin/env python3
"""Regression checks for the flower dual-full-capture escape theorem."""

import json
from pathlib import Path

import z3

try:
    from .audit_flower_dual_full_escape import run as run_scalar_audit
    from .audit_flower_three_rotation_polarity import run as run_rotation_audit
    from .audit_minimal_flower_flexible_gate import run as run_core_audit
    from .analyze_residual_top_champion_sources import run as run_source_census
    from .run_minimal_flower_global_lex_cegar import build_master, rival_blocker
except ImportError:
    from audit_flower_dual_full_escape import run as run_scalar_audit
    from audit_flower_three_rotation_polarity import run as run_rotation_audit
    from audit_minimal_flower_flexible_gate import run as run_core_audit
    from analyze_residual_top_champion_sources import run as run_source_census
    from run_minimal_flower_global_lex_cegar import build_master, rival_blocker


ROOT = Path(__file__).resolve().parents[2]


def main():
    scalar_path = ROOT / "results" / "flower_dual_full_capture_escape_audit.json"
    scalar = json.loads(scalar_path.read_text())
    scalar_replay = run_scalar_audit()
    assert scalar_replay["status"] == scalar["status"]
    assert scalar_replay["records"] == scalar["records"]
    assert scalar["status"] == "ALL_FORCED"
    assert {record["status"] for record in scalar["records"]} == {"unsat"}

    rotation_path = ROOT / "results" / "flower_three_rotation_polarity_audit.json"
    rotation = json.loads(rotation_path.read_text())
    rotation_replay = run_rotation_audit()
    assert rotation_replay["status"] == rotation["status"] == "ALL_FORCED"
    assert rotation_replay["records"] == rotation["records"]

    gate_path = ROOT / "results" / "minimal_flower_flexible_completion_gate.json"
    core_path = ROOT / "results" / "minimal_flower_flexible_completion_audit.json"
    core = json.loads(core_path.read_text())
    core_replay = run_core_audit(gate_path)
    for key in (
        "status",
        "full_replay_status",
        "without_nondegeneracy_status",
        "recorded_rival_count",
        "core_rival_count",
        "core",
        "deletion_check_statuses",
    ):
        assert core_replay[key] == core[key]
    assert core["status"] == "DELETION_MINIMAL_UNSAT_CORE"
    assert core["without_nondegeneracy_status"] == "unsat"
    assert {entry["topology"] for entry in core["core"]} == {
        "_->q:f;q->_:bq",
        "_->r:f;q->r:tq;r->_:br;r->q:tr",
    }

    _, value, base = build_master()
    q_fixed = {
        "r": ("tr", "f"),
        "q": ("tq", "bq"),
        "c": ("tc", "bc"),
        "s": ("z",),
        "_": ("br",),
    }
    assert z3.is_true(z3.simplify(rival_blocker(value, base, q_fixed, "flexible")))

    theorem = (
        ROOT / "results" / "FLOWER_DUAL_FULL_CAPTURE_ESCAPE_LEMMA_20260810.md"
    ).read_text()
    assert "arbitrary-packet" in theorem
    assert "residual top packet `J`" in theorem
    assert "does **not** force" in theorem
    rotation_theorem = (
        ROOT / "results" / "FLOWER_THREE_ROTATION_POLARITY_LEMMA_20260810.md"
    ).read_text()
    assert "independent of the numbers of goods" in rotation_theorem
    assert "opposite ranking" in rotation_theorem

    source_path = ROOT / "results" / "residual_top_champion_source_census.json"
    source_census = json.loads(source_path.read_text())
    assert run_source_census(ROOT) == source_census
    assert len(source_census["records"]) == 7
    assert not any(
        record["survives_live_rotation_gate"]
        for record in source_census["records"]
    )
    print("flower dual-full-capture theorem tests passed")


if __name__ == "__main__":
    main()
