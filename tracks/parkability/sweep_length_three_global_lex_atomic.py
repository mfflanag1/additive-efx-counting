#!/usr/bin/env python3
"""Sweep all atomic source/priority types for length-three motif discovery."""

from __future__ import annotations

import argparse
import contextlib
import itertools
import json
from pathlib import Path

try:
    from .extract_length_three_atomic_core import extract
    from .run_alternating_global_lex_cegar import atomic_json
    from .run_length_three_global_lex_atomic_cegar import AGENTS, run
except ImportError:
    from extract_length_three_atomic_core import extract
    from run_alternating_global_lex_cegar import atomic_json
    from run_length_three_global_lex_atomic_cegar import AGENTS, run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    records = []
    for source in range(3):
        for order in itertools.permutations(range(4)):
            stem = f"source-{AGENTS[source]}-order-{'-'.join(AGENTS[a] for a in order)}"
            pool = args.work / f"{stem}-pool.json"
            result_path = args.work / f"{stem}-result.json"
            if result_path.exists():
                result = json.loads(result_path.read_text())
            else:
                with open(args.work / f"{stem}.log", "w") as sink, contextlib.redirect_stdout(sink):
                    result = run(
                        source,
                        order,
                        pool,
                        result_path,
                        args.iterations,
                        256,
                        args.timeout_seconds,
                    )
            record = {
                "singleton_champion_source": source,
                "singleton_champion_source_name": AGENTS[source],
                "agent_order": list(order),
                "agent_order_names": [AGENTS[agent] for agent in order],
                "status": result["status"],
                "iterations": result["iterations"],
                "pool_size": result["pool_size"],
            }
            if result["status"] == "UNSAT_ATOMIC_SOURCE_ORDER_CELL":
                core = extract(source, order, pool)
                record["core_size"] = core["core_size"]
                record["core_bundles"] = [rival["bundles"] for rival in core["rivals"]]
            records.append(record)
            print(
                f"source={AGENTS[source]} order={record['agent_order_names']} "
                f"status={record['status']} core={record.get('core_size')}",
                flush=True,
            )
    payload = {
        "schema": "length-three-global-lex-atomic-sweep-v1",
        "records": records,
        "claim_boundary": "atomic motif discovery only; no packet theorem",
    }
    atomic_json(args.output, payload)


if __name__ == "__main__":
    main()
