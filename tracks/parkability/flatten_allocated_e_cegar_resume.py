#!/usr/bin/env python3
"""Flatten a hash-linked allocated-E CEGAR resume chain without losing cuts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from .run_generalized_pi_named_selector_cegar import cycle_signature


ROOT = Path(__file__).resolve().parents[2]


def load_chain(path: Path, seen_paths=None):
    path = path.resolve()
    seen_paths = set() if seen_paths is None else seen_paths
    resolved = path.resolve()
    if resolved in seen_paths:
        raise ValueError("resume cycle")
    seen_paths.add(resolved)
    payload = json.loads(path.read_text())
    chain = []
    resume = payload.get("resume")
    if resume:
        prior = (ROOT / resume["source"]).resolve()
        actual = hashlib.sha256(prior.read_bytes()).hexdigest()
        if actual != resume["source_sha256"]:
            raise ValueError((prior, actual, resume["source_sha256"]))
        chain.extend(load_chain(prior, seen_paths))
    chain.append((path, payload))
    return chain


def witnesses(payload):
    for record in payload.get("iterations", []):
        rows = record.get("pi_witnesses")
        if rows is None:
            one = record.get("pi_witness")
            rows = () if one is None else (one,)
        yield from rows


def run(source: Path, output: Path):
    source = source.resolve()
    chain = load_chain(source)
    unique = {}
    for _, payload in chain:
        for witness in witnesses(payload):
            unique.setdefault(cycle_signature(witness), witness)
    final = chain[-1][1]
    result = {
        "schema": "allocated-e-capture-rank-three-generalized-pi-cegar-v1",
        "status": "FLATTENED_RESUME",
        "solver": final.get("solver"),
        "form_index": final["form_index"],
        "base": final.get("base"),
        "support": final.get("support"),
        "negate_named_selector": final.get("negate_named_selector", False),
        "allocation_count": final.get("allocation_count", 0),
        "generalized_pi_cut_count": len(unique),
        "resume": None,
        "iterations": [{
            "iteration": 0,
            "solver_status": "not_run_flattened_resume",
            "pi_witnesses": list(unique.values()),
            "pi_cycle_count": len(unique),
            "fresh_cut_count": len(unique),
        }],
        "source_chain": [{
            "source": str(path.relative_to(ROOT)),
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "declared_cut_count": payload.get("generalized_pi_cut_count"),
        } for path, payload in chain],
        "source_code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "claim_boundary": (
            "Lossless deduplicated cut payload for resuming one bounded "
            "allocated-E CEGAR chain. It records no new mathematical verdict."
        ),
    }
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.source, args.output)
    print(json.dumps({
        "status": result["status"],
        "chain_length": len(result["source_chain"]),
        "cut_count": result["generalized_pi_cut_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
