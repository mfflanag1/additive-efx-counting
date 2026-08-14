from fractions import Fraction

from .run_allocated_e_form0_role_split_pi_cegar import (
    BASE, GOODS, OWNERS, find_closed_family, find_complete_efx_four_edge,
    find_complete_efx_four_edge_endpoints, verify_complete_efx_endpoint,
)


def test_oracle_finds_selected_closed_family_when_all_owners_allowed():
    values = {
        owner: {good: Fraction(1, 100) for good in GOODS}
        for owner in OWNERS
    }
    # Give each owner a disjoint desired copy of its own base support. The
    # union is closed by construction and every deletion tail stays <= 1.
    for owner in OWNERS:
        for good in BASE[owner]:
            values[owner][good] = Fraction(3, len(BASE[owner]))
    family = find_closed_family(values)
    assert family is not None
    assert set(family) <= set(OWNERS)


def test_oracle_rejects_when_no_bundle_is_desired():
    values = {
        owner: {good: Fraction(1, 1000) for good in GOODS}
        for owner in OWNERS
    }
    assert find_closed_family(values) is None


def test_four_edge_oracle_completes_a_single_charity_good():
    values = {
        owner: {good: Fraction(1, 100) for good in GOODS}
        for owner in OWNERS
    }
    result = find_complete_efx_four_edge(values, ("p",))
    assert result is not None
    assert len(result["transfer_edges"]) == 1

    endpoints = find_complete_efx_four_edge_endpoints(values, ("p",), maximum=10)
    assert len(endpoints) == 4
    assert all(
        verify_complete_efx_endpoint(values, ("p",), endpoint)
        for endpoint in endpoints
    )
