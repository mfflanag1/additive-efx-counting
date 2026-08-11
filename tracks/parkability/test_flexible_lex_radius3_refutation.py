#!/usr/bin/env python3
"""Focused regression for the hardened radius-three flower refutation."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .audit_flexible_lex_radius3_hardened_countermodel import run
except ImportError:
    from audit_flexible_lex_radius3_hardened_countermodel import run


def main():
    root = Path(__file__).resolve().parents[2]
    source = root / "results/flexible_lex_radius3_hardened_countermodel.json"
    lex_escape = root / "results/flexible_lex_radius3_hardened_countermodel_escape.json"
    later_escape = root / "results/flexible_later_radius3_hardened_countermodel_escape.json"
    frozen = root / "results/flexible_lex_radius3_hardened_countermodel_audit.json"
    assert run(source, lex_escape, later_escape) == json.loads(frozen.read_text())
    print("flexible lex radius-three refutation tests passed")


if __name__ == "__main__":
    main()
