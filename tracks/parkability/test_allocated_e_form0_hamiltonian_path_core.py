from .audit_allocated_e_form0_hamiltonian_path_core import (
    validate_closed_core_witness,
)


def test_closed_core_witness_semantics():
    witness = {
        "cycle": ["r", "q"],
        "edges": [
            {
                "source": "r", "target": "q",
                "desired_core": ["a1", "m"],
                "incoming": ["m"], "released": ["gq", "j"],
            },
            {
                "source": "q", "target": "r",
                "desired_core": ["gq", "a0"],
                "incoming": ["gq"], "released": ["m"],
            },
        ],
    }
    result = validate_closed_core_witness(witness)
    assert result["cycle_length"] == 2
    assert result["incoming_allocated_count"] == 2
