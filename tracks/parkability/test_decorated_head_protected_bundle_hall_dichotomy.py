from pathlib import Path

from .audit_decorated_head_protected_bundle_hall_dichotomy import run


ROOT = Path(__file__).resolve().parents[2]


def test_all_protected_graphs_match_or_have_head_defect() -> None:
    result = run(ROOT)
    assert result["status"] == "ALL_PROTECTED_GRAPHS_MATCH_OR_HAVE_HEAD_DEFICIENCY_ONE"
    assert result["one_head"]["relation_count"] == 3584
    assert result["two_head"]["relation_count"] == 3136
    for branch in (result["one_head"], result["two_head"]):
        assert branch["perfect_matching_count"] + branch["deficient_relation_count"] == branch["relation_count"]
        assert branch["deficient_relation_count"] == len(branch["deficient_records"])


def test_every_minimal_defect_contains_head_and_has_deficiency_one() -> None:
    result = run(ROOT)
    for branch in (result["one_head"], result["two_head"]):
        heads = set(branch["heads"])
        for record in branch["deficient_records"]:
            for witness in record["minimal_witnesses"]:
                assert set(witness["sources"]) & heads
                assert len(witness["neighbors"]) == len(witness["sources"]) - 1
