#!/usr/bin/env python3
"""Exhaust desired-side and residual-emptiness masks for one flower cell."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

try:
    from .decide_three_nonsingleton_flower_packet_split_witness import run as run_mask
except ImportError:
    from decide_three_nonsingleton_flower_packet_split_witness import run as run_mask


RESTS = ("tq_rest", "br_rest", "tr_rest", "bq_rest")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid(aq_support: str, ar_support: str, empty_rest: tuple[str, ...]) -> bool:
    present = {
        "aq_tq": aq_support in ("tq", "both"),
        "aq_br": aq_support in ("br", "both"),
        "ar_tr": ar_support in ("tr", "both"),
        "ar_bq": ar_support in ("bq", "both"),
        **{rest: rest not in empty_rest for rest in RESTS},
    }
    return all((
        present["aq_tq"] or present["tq_rest"],
        present["aq_br"] or present["br_rest"],
        present["ar_tr"] or present["tr_rest"],
        present["ar_bq"] or present["bq_rest"],
    ))


def run() -> dict:
    records = []
    for aq_support, ar_support in itertools.product(("tq", "br", "both"), ("tr", "bq", "both")):
        for mask in range(1 << len(RESTS)):
            empty_rest = tuple(
                rest for index, rest in enumerate(RESTS) if mask & (1 << index)
            )
            if not valid(aq_support, ar_support, empty_rest):
                continue
            result = run_mask(2, aq_support, ar_support, empty_rest)
            records.append({
                "aq_support": aq_support,
                "ar_support": ar_support,
                "empty_rest": list(empty_rest),
                "status": result["status"],
            })
    counts = {
        status: sum(record["status"] == status for record in records)
        for status in ("unsat", "sat", "unknown")
    }
    root = Path(__file__).resolve().parents[2]
    script = Path(__file__).resolve()
    dependency = root / "tracks" / "parkability" / "decide_three_nonsingleton_flower_packet_split_witness.py"
    return {
        "schema": "three-nonsingleton-flower-support-mask-audit-v1",
        "status": "ALL_UNSAT" if counts["unsat"] == len(records) else "OPEN",
        "mask_count": len(records),
        "counts": counts,
        "records": records,
        "claim_boundary": (
            "bounded two-good-per-nonempty-component audit of every support mask for A_q,A_r and every "
            "feasible empty/nonempty residual mask in one same-bottom-source flower cell; not a cap-free proof"
        ),
        "provenance": {
            "dependency": str(dependency.relative_to(root)),
            "dependency_sha256": sha256(dependency),
            "script": str(script.relative_to(root)),
            "script_sha256": sha256(script),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, indent=2))


if __name__ == "__main__":
    main()
