import hashlib
import json
from fractions import Fraction
from pathlib import Path

from .decide_fixed_u_mixed_anchor_menu import audit_mixed
from .independently_verify_fixed_u_mixed_and_four_split import (
    audit_physical_allocation,
    load_rows,
    physical_witness,
)
from .run_fixed_u_multi_split_chart_theorem import exact_audit


ROOT = Path(__file__).resolve().parents[2]
PROFILE = ROOT / "results/fixed_u_tame_or_anchor_cegar_20260821.json"
PRIMARY = ROOT / "results/fixed_u_pattern_dependent_mixed_menu_obstruction_20260821.json"
INDEPENDENT = ROOT / "results/fixed_u_pattern_mixed_four_split_independent_audit_20260821.json"
AGGREGATE = ROOT / "results/fixed_u_two_anchor_obstruction_aggregate_20260821.json"


def profile_rows():
    raw = json.loads(PROFILE.read_text())
    return raw, load_rows(raw, "totals"), load_rows(raw, "minima")


def test_pattern_dependent_audit_covers_every_tame_cell():
    raw = json.loads(PRIMARY.read_text())
    assert raw["status"] == "SAT_PATTERN_DEPENDENT_MIXED_MENU_OBSTRUCTION"
    assert raw["cell_count"] == 64
    assert raw["sat_cell_count"] + raw["unsat_cell_count"] == 64
    assert raw["unknown_cell_count"] == 0
    assert len(raw["tame_roles"]) == 8
    for role in raw["tame_roles"]:
        cells = [cell for cell in raw["cells"] if cell["tame_role"] == role]
        assert len(cells) == 8
        assert len({cell["pattern"] for cell in cells}) == 8
        assert raw["failing_patterns_by_tame_role"][role]


def test_every_positive_mixed_cell_replays_in_exact_arithmetic():
    _, totals, minima = profile_rows()
    raw = json.loads(PRIMARY.read_text())
    for cell in raw["cells"]:
        if cell["status"] != "sat":
            continue
        role, bits = cell["pattern"].split(":")
        vector = {role: dict(zip(("r", "q", "d", "s"), map(int, bits)))}
        if cell["kind"] == "tame":
            exact_audit(cell["allocation"], totals, minima, (role,), vector, 4)
        else:
            edges, slack = audit_mixed(
                cell["allocation"], totals, minima, role, vector,
                cell["anchor_role"], cell["anchor_observer"], 4,
            )
            assert edges == cell["edges"]
            assert str(slack) == cell["minimum_certified_slack"]


def test_independent_audit_fixes_exact_four_split_threshold():
    profile_raw, totals, minima = profile_rows()
    raw = json.loads(INDEPENDENT.read_text())
    assert raw["status"] == (
        "AUDIT_PASS_MIXED_MENU_REFUTED_FOUR_SPLITS_NECESSARY_AND_SUFFICIENT"
    )
    assert raw["profile_sha256"] == hashlib.sha256(PROFILE.read_bytes()).hexdigest()
    assert raw["split_attempts"] == [
        {"split_cap": 0, "status": "unsat"},
        {"split_cap": 1, "status": "unsat"},
        {"split_cap": 2, "status": "unsat"},
        {"split_cap": 3, "status": "unsat"},
        {"split_cap": 4, "status": "sat"},
    ]
    values, role_goods = physical_witness(
        totals, minima, raw["global_product_cell"]
    )
    assert raw["physical_witness_side_patterns"] == raw["global_product_cell"]
    stored = {
        observer: {good: Fraction(value) for good, value in row.items()}
        for observer, row in raw["physical_values"].items()
    }
    assert stored == {
        observer: {
            good: values[observer, good]
            for role in role_goods for good in role_goods[role]
        } for observer in stored
    }
    certificate = raw["four_split_certificate"]
    edges, split_roles = audit_physical_allocation(
        certificate["allocation"], values, role_goods, 4
    )
    assert [list(edge) for edge in edges] == certificate["edges"]
    assert split_roles == certificate["split_roles"]
    assert len(split_roles) == 4
    assert profile_raw["status"] == "SAT_TAME_MENU_OR_DYNAMIC_ANCHOR_OBSTRUCTION"


def test_independent_mixed_witnesses_cover_all_conditioning_roles():
    primary = json.loads(PRIMARY.read_text())
    raw = json.loads(INDEPENDENT.read_text())
    assert {row["tame_role"] for row in raw["mixed_witnesses"]} == set(
        primary["tame_roles"]
    )
    assert raw["independent_mixed_anchor_lane_count"] == 8 * 40
    assert all(row["tame_status"] == "unsat" for row in raw["mixed_witnesses"])
    assert all(row["anchor_lane_count"] == 40 for row in raw["mixed_witnesses"])
    assert raw["global_product_cell"] == {
        row["tame_role"]: row["pattern"] for row in raw["mixed_witnesses"]
    }


def test_two_anchor_shards_cover_the_full_pair_observer_product():
    raw = json.loads(AGGREGATE.read_text())
    assert raw["status"] == "UNSAT_NO_UNIVERSAL_TWO_ANCHOR_CERTIFICATE"
    assert raw["role_pair_count"] == 55
    assert raw["anchor_observer_pair_count_per_role_pair"] == 16
    assert raw["expected_lane_count"] == raw["audited_lane_count"] == 880
    assert raw["sat_count"] == raw["unknown_count"] == 0
    for shard in raw["shards"]:
        path = ROOT / shard["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == shard["sha256"]
