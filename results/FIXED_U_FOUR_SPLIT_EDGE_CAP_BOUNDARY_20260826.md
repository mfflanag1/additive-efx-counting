# Four-split form-2 conjecture: refuted, and the split phenomenon is a four-edge-cap artifact

**Date:** 2026-08-26  
**Branch:** `cc/efx-four-split-20260826` (from `codex/efx-fixed-u-resume-20260820` @ `69c1dcd`)  
**Status:** exact obstruction to Conjecture F4 as stated (permitted outcome 2), with the
model-boundary verdict of outcome 3: the obstructing realization closes with **zero**
split roles as soon as a fifth support-transfer edge is allowed.  Complete EFX is not
refuted anywhere.  W5_STATUS_PLACEHOLDER

## Conjecture and quantifier discipline

**F4.** Every admissible positive-rational exact-response form-2 totals/minima profile,
and every physical realization consistent with it, admits a complete EFX allocation with
at most four support-transfer edges and at most four split roles.

The allocation may depend on the realization.  The realization class decided here is the
two-good class: every multi-good role (`T > M` for some observer; the master forces
`T >= 2M` for all observers) is realized by two goods, and a *cell* chooses, per role and
per observer, which of the two goods carries that observer's minimum (values `M` and
`T - M`).  Singleton roles (`T = M` for every observer) are one good.  Observer `o`'s EFX
inequalities depend only on `o`'s own side bits; the allocation is common.  A profile is
*closed* at `(split_cap, edge_cap)` when every cell has an allocation; it is *obstructed*
when some cell has none.

## Universal oracle (`tracks/parkability/fixed_u_universal_split.py`)

`universal_decide` is a CEGAR over cells: decide one cell by an integer-owner SMT
(complete allocation of all goods, PbLe edge and split cardinalities, one EFX implication
per observer/target/good), add the allocation to a menu, then ask an exact SMT over the
side bits for a cell that **no** menu allocation closes.  `CLOSED` means that final query
is UNSAT — a proof over all `2^(4·#multiroles)` cells (`2^44` here) — and every menu
allocation is re-audited in exact rationals.  `OBSTRUCTED` returns a cell whose decision is
UNSAT; `escalate` then runs that cell through split caps `0..#multiroles` at edge caps
`4, 5, 6, 8, 16` and cap-free.

## Calibration gates (all pass; `test_fixed_u_universal_split.py`)

| control | expected | oracle |
|---|---|---|
| terminal wild-and-forced profile | closes with one split (split-switching theorem) | `CLOSED` at split cap 1, menu 4, 2 s |
| dynamic-anchor obstruction profile | whole-role UNSAT; one split closes the canonical cell; `{a1,h}` tame menu closes all | `OBSTRUCTED` at caps 0 and 1, `CLOSED` at cap 2 (menu 43) |
| pattern-mixed obstruction profile | product cell needs exactly four splits | `OBSTRUCTED` at cap 3; escalation of the cap-3 cell gives minimal split 4 at edge cap 4 (baseline reproduced) |
| broken oracle (charity edge uncounted) | must wrongly close | pinned cell flips `unsat -> sat` |
| baseline replay | SHA-256 `0237ad9c…` | reproduced byte for byte (`audit_fixed_u_pattern_dependent_mixed_menu`); independent audit reproduced with the exact goal command line |

## Result 1: F4 is false — a cell with no four-edge allocation at any split count

On the pattern-mixed profile (`results/fixed_u_tame_or_anchor_cegar_20260821.json`,
terminal totals/minima), the cell

```text
gq:r=1, h:r=1, j:d=1, j:q=1, l:r=1, m:s=1, all other side bits 0
```

has **no complete EFX allocation with at most four support-transfer edges for any split
cap `0..11`** (all twelve decisions UNSAT), so in particular none with four splits.
Escalation:

| edge cap | minimal split count |
|---|---|
| 4 | none (UNSAT at every split cap) |
| 5 | **0** (a whole-role allocation exists) |
| 6, 8, 16, cap-free | 0 |

Pinned: `results/fixed_u_universal_split_mixed_profile_edge4_20260826.json`.
Independent Boolean piece-placement encoding
(`independently_verify_fixed_u_universal_split_cell.py`, no shared solver code):
`edge4/split0 unsat`, `edge4/split23 unsat`, `edge5/split0 sat` with edges
`charity->r, d->r, q->s, r->d, r->q`, `edge5/split23 sat`.  Every SAT allocation is
re-audited with exact `Fraction` arithmetic.  The realization has 23 physical goods (eleven two-good roles and one singleton), so
the Alkassar–Fouz–Mehlhorn `(4, <=9)` theorem does not apply and is not contradicted;
the cell is not an EFX counterexample (cap-free SAT).

Consequently the earlier ladder (one split, then two, three, four) measured the price of
the **four-edge support cap**, not a split-count phenomenon: with five edges the same
profile is closed universally by a *single whole-role allocation*
(`results/fixed_u_universal_split_mixed_profile_edge5_whole_role_20260826.json`,
menu size 1 — whole-role allocations are realization-independent, so one closing
allocation closes every cell).

## Result 2: census over the 293 ledger profiles

`census_fixed_u_universal_split.py` over the three cut ledgers (205 + 7 + 81 profiles):

- `(split_cap 0, edge_cap 5)`: **293/293 CLOSED, every menu of size 1** — each profile
  has a whole-role five-edge EFX allocation.  The three named profiles (terminal,
  dynamic-anchor, pattern-mixed) likewise close at `(0, 5)` with menu size 1.
- `(split_cap 4, edge_cap 4)`: CENSUS_S4E4_PLACEHOLDER

## Result 3: whole-role CEGAR over the complete form-2 master

`run_fixed_u_whole_role_edge_cegar.py` makes the edge-cap question symbolic: whole-role
EFX conditions are linear in totals/minima, so each closing allocation is an exact cut on
the master; the loop terminates UNSAT (theorem for the whole master) or at a profile with
no whole-role allocation under the cap.

- **Edge cap 4 (control):** 70 of the 296 seed profiles have no whole-role four-edge
  allocation (`SAT_WHOLE_ROLE_OBSTRUCTION_AT_SEED`), i.e. the cap genuinely binds — this is
  the phenomenon the split program was built to work around.  All 95 closing four-edge
  allocations use exactly `3` owner-pair edges plus charity (or fewer).
- **Edge cap 5:** all 296 seeds closed by 101 whole-role allocations; 98 of the first 111
  cuts use exactly four owner-pair edges plus the charity edge.  W5_RESULT_PLACEHOLDER

## Verdict

- Outcome 2: F4 is false as stated; the separating cell is exact and independently
  verified.
- Outcome 3: the separation is a four-edge-cap artifact, not a genuine split-count
  phenomenon — the cell closes with zero splits at edge cap 5, and every audited profile
  closes universally with zero splits at edge cap 5.  The four-edge premise
  ("three owner pairs plus charity") is the model boundary; four owner pairs plus charity
  is the empirically sufficient support.
- Not claimed: any EFX counterexample; universality of the five-edge whole-role closure
  beyond what the CEGAR/census below certify; representation of every saturated fixed-U
  state by form 2.

## Reproduction

```bash
python -m tracks.parkability.fixed_u_universal_split \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json --split-cap 4 --edge-cap 4 \
  --timeout-seconds 60 --escalate --output /tmp/mixed_edge4.json
python -m tracks.parkability.independently_verify_fixed_u_universal_split_cell \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json --cell-json /tmp/mixed_edge4.json \
  --timeout-seconds 300 --output /tmp/mixed_edge4_cell_independent.json
python -m tracks.parkability.fixed_u_universal_split \
  --profile results/fixed_u_tame_or_anchor_cegar_20260821.json --split-cap 0 --edge-cap 5 \
  --output /tmp/mixed_edge5.json
python -m tracks.parkability.census_fixed_u_universal_split \
  --ledger results/fixed_u_multi_split_chart_cuts_20260820.jsonl \
  --ledger results/fixed_u_dynamic_anchor_cuts_20260821.jsonl \
  --ledger results/fixed_u_tame_or_anchor_cuts_20260821.jsonl \
  --split-cap 0 --edge-cap 5 --output /tmp/census_s0_e5.jsonl
python -m tracks.parkability.run_fixed_u_whole_role_edge_cegar --edge-cap 5 \
  --seed-profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --seed-profile results/fixed_u_dynamic_anchor_cegar_20260821.json \
  --seed-profile results/fixed_u_tame_or_anchor_cegar_20260821.json \
  --seed-ledger results/fixed_u_multi_split_chart_cuts_20260820.jsonl \
  --seed-ledger results/fixed_u_dynamic_anchor_cuts_20260821.jsonl \
  --seed-ledger results/fixed_u_tame_or_anchor_cuts_20260821.jsonl \
  --output /tmp/w5.json --cut-ledger /tmp/w5_cuts.jsonl
pytest -q tracks/parkability/test_fixed_u_universal_split.py
```
Solver verdicts (UNSAT/SAT) are deterministic in content but not in wall time; the
obstruction cell is pinned in the test file, and every SAT certificate is re-audited in
exact arithmetic.
