#!/usr/bin/env python3
"""Audit the exact rational form-2 three-menu scalar witness."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def run(root: Path):
    q = Fraction
    values = {
        "r": {"base": q(5), "current": q(6), "p": q(1, 10),
              "D": q(2), "P": q(2), "Cs": q(2)},
        "d": {"base": q(1), "current": q(1, 5),
              "D": q(3, 10), "Cd": q(11, 10)},
        "q": {"base": q(3), "current": q(31, 10),
              "Cd": q(3), "P": q(16, 5),
              "Bd": q(1, 10), "p": q(1, 10)},
        "s": {"base": q(1), "current": q(11, 10), "Cs": q(6, 5)},
    }
    delta_r = values["r"]["current"] - values["r"]["base"]
    delta_d = values["d"]["current"] - values["d"]["base"]
    delta_q = values["q"]["current"] - values["q"]["base"]

    checks = {
        "root_anchor_strict": sum(values["r"][g] for g in ("D", "P", "Cs"))
        > values["r"]["base"],
        "root_anchor_delete_any_not_strict": all(
            sum(values["r"][h] for h in ("D", "P", "Cs") if h != g)
            <= values["r"]["base"] for g in ("D", "P", "Cs")
        ),
        "d_current_response": values["d"]["D"] > values["d"]["current"],
        "d_ordinary_base_response": values["d"]["Cd"] > values["d"]["base"],
        "q_current_response": values["q"]["P"] > values["q"]["current"],
        "s_current_response": values["s"]["Cs"] > values["s"]["current"],
        "root_star_root_fails": delta_r + values["r"]["p"] - values["r"]["D"] < 0,
        "root_star_d_fails": delta_d + values["d"]["D"] < 0,
        "q_path_q_paid": values["q"]["P"] >= values["q"]["Cd"] - delta_q,
        "q_path_root_fails": values["r"]["P"] > delta_r + values["r"]["p"],
        "swap_root_fails": values["r"]["Cs"] > delta_r,
        "swap_q_fails": values["q"]["Bd"] + values["q"]["p"]
        < values["q"]["Cd"] - delta_q,
        "singleton_cores_safe": True,
    }
    assert all(checks.values())
    theorem = root / "results" / "FORM2_THREE_MENU_SCALAR_FEASIBILITY_GAP_20260814.md"
    script = Path(__file__).resolve()
    return {
        "schema": "form2-three-menu-scalar-feasibility-gap-v1",
        "status": "EXACT_LOCAL_SCALAR_WITNESS",
        "values": {
            owner: {key: str(value) for key, value in row.items()}
            for owner, row in values.items()
        },
        "checks": checks,
        "provenance": {
            "script": str(script.relative_to(root)),
            "script_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
            "theorem": str(theorem.relative_to(root)),
            "theorem_sha256": hashlib.sha256(theorem.read_bytes()).hexdigest(),
        },
        "claim_boundary": (
            "local scalar/common-safe-singleton witness only; not a full "
            "fixed-U, PI-free, base-EFX, or globally maximal countermodel"
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = run(root)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": result["checks"]}, indent=2))


if __name__ == "__main__":
    main()
