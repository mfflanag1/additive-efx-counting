# Handoff — four-split session (2026-08-26)

Branch `cc/efx-four-split-20260826` from `codex/efx-fixed-u-resume-20260820` @ `69c1dcd`.

## What changed
- `tracks/parkability/fixed_u_universal_split.py`: universal k-split oracle over every two-good
  realization cell of a profile (CEGAR: integer-owner cell decision + exact SMT uncovered-cell query),
  with escalation (split cap x edge cap x cap-free) and a `--negative-control drop-charity-edge` switch.
- `tracks/parkability/independently_verify_fixed_u_universal_split_cell.py`: Boolean piece-placement
  re-decision of one cell (no shared solver code).
- `tracks/parkability/census_fixed_u_universal_split.py`: multi-process census over the cut ledgers.
- `tracks/parkability/run_fixed_u_whole_role_edge_cegar.py`: symbolic whole-role CEGAR over the
  form-2 master at a given edge cap (cuts = linear whole-role EFX conditions; `--resume-cuts`).
- `tracks/parkability/test_fixed_u_universal_split.py`: calibration gates + pinned obstruction cell.
- Pinned artifacts `results/fixed_u_universal_split_*_20260826.json`; write-up
  `results/FIXED_U_FOUR_SPLIT_EDGE_CAP_BOUNDARY_20260826.md`.

## Verdict so far
F4 is FALSE as stated (exact cell, independently verified), and the split ladder was an artifact of the
four-edge support cap: the cell and all 293 ledger profiles close with ZERO splits at five edges.
Whether the five-edge whole-role closure is a theorem for the whole form-2 master is decided by the
W5 CEGAR (`run_fixed_u_whole_role_edge_cegar.py --edge-cap 5`); see the write-up's status line.

## Laws
- Quantify per cell: the allocation may depend on the realization; the selector theorems of Aug 20-21
  were refuted because they fixed a rule across realizations.
- Whole-role allocations are realization-independent, so a whole-role closure of one cell closes all cells
  and becomes a symbolic linear cut on the master.
- Run every obstruction through the widest oracle (split cap x edge cap x cap-free) before naming it.
- Under machine load >100 z3 timeouts masquerade as UNKNOWN; profile 192 of the multi-split ledger
  needed 600 s to close at (4,4).
- zsh does not word-split `$VAR` in command position: use `${=VAR}`.
