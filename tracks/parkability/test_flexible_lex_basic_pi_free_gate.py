#!/usr/bin/env python3
"""Focused regression for the basic-PI-free radius-three obstruction."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .audit_flexible_lex_basic_pi_free_hardened_countermodel import run
except ImportError:
    from audit_flexible_lex_basic_pi_free_hardened_countermodel import run


def main():
    root = Path(__file__).resolve().parents[2]
    source = root / "results/flexible_lex_basic_pi_free_hardened_countermodel.json"
    escape = root / "results/flexible_lex_basic_pi_free_hardened_later_escape.json"
    response = (
        root
        / "results/flexible_lex_basic_pi_free_hardened_later_escape_response_hall.json"
    )
    frozen = (
        root / "results/flexible_lex_basic_pi_free_hardened_countermodel_audit.json"
    )
    assert run(source, escape, response) == json.loads(frozen.read_text())
    print("flexible lex basic-PI-free gate tests passed")


if __name__ == "__main__":
    main()
