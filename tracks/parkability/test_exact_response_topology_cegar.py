import json
from pathlib import Path

from .decide_exact_response_functional_cover_family import (
    FUNCTIONAL_COVER_TOPOLOGIES,
)
from .run_exact_response_topology_cegar import functional, normalize


def test_initial_functional_cover_matches_frozen_census():
    result = json.loads(Path(
        "results/fixed_u_exact_owner_cycle_relation_topology_cover_round24.json"
    ).read_text())
    expected = {normalize(topology) for topology in result["functional_topology_cover"]}
    actual = {normalize(topology) for topology in FUNCTIONAL_COVER_TOPOLOGIES}
    assert actual == expected
    assert len(actual) == 4
    assert all(len(topology) == 4 and functional(topology) for topology in actual)
