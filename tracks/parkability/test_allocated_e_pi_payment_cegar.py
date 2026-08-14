#!/usr/bin/env python3
"""Calibration checks for the allocated-E PI/payment CEGAR."""

from .decide_three_candidate_functional_payment_skeleton import TOPOLOGIES
from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical


def test_paid_matching_menus_are_complete():
    expected = {0: 188, 2: 720}
    for form, count in expected.items():
        allocations = {
            canonical(allocation)
            for topology in TOPOLOGIES[form]
            for allocation in allocations_supported_by(topology)
        }
        assert len(allocations) == count
