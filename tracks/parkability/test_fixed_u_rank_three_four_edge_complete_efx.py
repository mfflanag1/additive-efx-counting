from .decide_fixed_u_rank_three_four_edge_complete_efx import (
    allocations_with_at_most_edges,
    provenance_holder,
)
from .run_fixed_u_full_packet_terminal_cegar import SUPPORT_STATE
from .run_fixed_u_rank_three_relation_cegar import (
    build_rank_three_master,
    functional_transfer,
)


def test_declared_atomization_has_twelve_atoms():
    assert len(provenance_holder(SUPPORT_STATE)) == 12


def test_every_enumerated_allocation_is_complete_and_within_bound():
    supplier = provenance_holder(SUPPORT_STATE)
    count = 0
    nonempty_owner_count = 0
    for allocation in allocations_with_at_most_edges():
        count += 1
        nonempty_owner_count += all(allocation[owner] for owner in ("r", "q", "d", "s"))
        seen = [good for goods in allocation.values() for good in goods]
        assert sorted(seen) == sorted(supplier)
        assert not allocation["charity"]
        holder = {
            good: owner for owner, goods in allocation.items() for good in goods
        }
        edges = {
            (supplier[good], holder[good])
            for good in supplier if supplier[good] != holder[good]
        }
        assert len(edges) <= 4
    assert count == 116_596
    assert nonempty_owner_count == 93_480


def test_functional_filter_detects_branching_supplier():
    functional = {
        "r": ["a0", "a1"], "q": ["h", "j", "k", "q0"],
        "d": ["gq", "gr", "m", "p"], "s": ["e", "l"], "charity": [],
    }
    branching = {
        "r": ["a0"], "q": ["h", "j", "k", "q0"],
        "d": ["a1", "gq", "gr", "p"], "s": ["e", "l", "m"], "charity": [],
    }
    assert functional_transfer(functional, SUPPORT_STATE)
    assert not functional_transfer(branching, SUPPORT_STATE)


def test_functional_nonempty_owner_menu_count():
    allocations = (
        allocation for allocation in allocations_with_at_most_edges(4, SUPPORT_STATE)
        if all(allocation[owner] for owner in ("r", "q", "d", "s"))
        and functional_transfer(allocation, SUPPORT_STATE)
    )
    assert sum(1 for _ in allocations) == 76_692


def test_legacy_charity_path_normal_forms_are_excluded_in_canonical_cell():
    solver, _ = build_rank_three_master(
        required_minimal_normal_form=True,
        exclude_self_responses=True,
    )
    solver.set(timeout=30_000)
    assert str(solver.check()) == "unsat"


def test_exact_normal_form_rejects_legacy_self_response_semantics():
    try:
        build_rank_three_master(required_minimal_normal_form=True)
    except ValueError as error:
        assert "nonself responses" in str(error)
    else:
        raise AssertionError("legacy self-response semantics were accepted")


def test_corrected_owner_cycle_master_is_consistent():
    solver, _ = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
    )
    solver.set(timeout=30_000)
    assert str(solver.check()) == "sat"


def test_exact_corrected_owner_cycle_relation_is_consistent():
    solver, _ = build_rank_three_master(
        exclude_self_responses=True,
        required_owner_cycle_form=True,
        exact_owner_cycle_response_relation=True,
    )
    solver.set(timeout=30_000)
    assert str(solver.check()) == "sat"
