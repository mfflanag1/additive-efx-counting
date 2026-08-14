from .decide_three_candidate_functional_payment_skeleton import TOPOLOGIES
from .decide_two_survivor_named_topology_family import allocations_supported_by, canonical


def test_three_candidate_payment_menu_counts():
    expected = {0: 188, 2: 720}
    for form_index, topologies in TOPOLOGIES.items():
        allocations = {
            canonical(allocation)
            for topology in topologies
            for allocation in allocations_supported_by(topology)
        }
        assert len(allocations) == expected[form_index]
