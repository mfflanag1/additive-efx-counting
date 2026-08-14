import json

from .audit_allocated_e_physical_pi_cegar_unsat import (
    learned_signatures,
    preseed_signatures,
    validate_signature,
)


def test_preseed_signature_census_and_validation():
    signatures = set(preseed_signatures())
    assert len(signatures) == 1372
    for signature in signatures:
        validate_signature(signature)


def test_batch_and_single_signatures_reconstruct_losslessly():
    payload = {
        "preseed_all_self_pi": False,
        "restored_physical_pi_signatures": [
            [["s", ["e.0", "gr.0"]]],
        ],
        "iterations": [
            {"batch_physical_pi_signatures": [
                [["r", ["a0.0", "gr.1"]]],
                [["q", ["a1.0", "j.1"]]],
            ]},
            {"physical_pi_signature": [
                ["d", ["h.0", "gr.0"]],
                ["r", ["a0.0", "m.1"]],
            ]},
        ],
    }
    signatures = learned_signatures(payload)
    assert len(signatures) == 4
    for signature in signatures:
        validate_signature(signature)
