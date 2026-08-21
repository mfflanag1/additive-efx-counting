# Fixed-U wild `a1` all-realizations lemma

**Date:** 2026-08-20  
**Status:** exact theorem for the immutable terminal profile; independently
audited; all feasible `a1` cardinalities closed

## Headline

The wild-and-forced terminal profile is not an obstruction once splitting its
wild role `a1` is allowed. One fixed complete allocation is EFX for **every**
positive realization of `a1` having the profile's prescribed observer totals
and minima, while every other role remains in its canonical realization. It
uses exactly four support-transfer edges.

The three-good CEGAR found this allocation after one oracle call and then
proved its realization master `UNSAT`. A separate exact-arithmetic audit shows
why no cardinality-by-cardinality search is needed: the allocation keeps the
entire `a1` realization together, so all EFX inequalities depend only on its
fixed total and minimum.

## Theorem

Fix the terminal profile in
`fixed_u_wild_forced_terminal_profile_20260820.json` and the canonical
realizations of every role other than `a1` in
`fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json`.
Replace `a1` by any finite set of positive goods such that, for every observer
`i`, their values sum to `T_i(a1)` and have minimum `M_i(a1)`.

Then the following allocation is complete and EFX:

```text
d: l:0, l:1, m:0, m:1, gq:0, gq:1, gr:0
q: j:0, j:1, k:0, q0:0, p:0
r: a0:0, a0:1, every a1 good, k:1
s: h:0, e:0, e:1
```

Its support-transfer edges are exactly

```text
charity -> q
q       -> r
r       -> s
s       -> d
```

The minimum EFX slack is `23/1924 > 0`.

## Proof

For additive valuations, a complete allocation `X` is EFX exactly when, for
every ordered pair of distinct agents `(i,j)`,

```text
v_i(X_i) - v_i(X_j) + min_{g in X_j} v_i(g) >= 0.             (1)
```

This is simply the hardest of the individual-good deletion inequalities for
target bundle `X_j`.

In the displayed allocation, all `a1` goods occur in `X_r`. Consequently, for
each observer `i`, their contribution to `v_i(X_r)` is always `T_i(a1)`, and
their least possible deleted-good value is always `M_i(a1)`. Every other
quantity in (1) comes from a frozen canonical good. Thus (1) is invariant under
the cardinality, labels, internal values, and minimum-witness identities of the
`a1` realization.

Direct exact rational evaluation gives the following worst-deletion slacks;
rows are observers and columns are target bundles:

| observer | target `r` | target `q` | target `d` | target `s` |
|---|---:|---:|---:|---:|
| `r` | — | `1923/1924` | `147/296` | `1935/1924` |
| `q` | `23/1924` | — | `5279/11544` | `157/481` |
| `d` | `9/37` | `2857/3848` | — | `6673/7696` |
| `s` | `1843/5772` | `971/2886` | `935/1443` | — |

All twelve are positive, proving EFX. The allocation itself also directly
induces the four listed support-transfer pairs, proving the edge bound.

## Why this closes cardinalities 3 through 7

A positive `k`-good realization with prescribed total `T_i` and minimum `M_i`
requires `k M_i <= T_i` for every observer. Conversely, for `k >= 2`, this
condition is sufficient row by row: take `k-1` entries equal to `M_i` and the
last equal to `T_i-(k-1)M_i`.

For the four `a1` rows, the floors of `T_i/M_i` are

```text
r:  948
q: 3460
d:    7
s:   13
```

Therefore the jointly feasible cardinalities are exactly `2,3,4,5,6,7`.
Cardinality one is impossible because `T_i != M_i`; cardinality eight and
above is impossible already in observer `d`'s row. The theorem hence covers
every physically feasible `a1` cardinality, including all four requested
continuation rungs without further solver calls.

## Reproduction

Run the exhaustive three-good discovery/replay:

```bash
python -m tracks.parkability.run_fixed_u_a1_three_good_cegar \
  --profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --repair results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json \
  --output results/fixed_u_a1_three_good_cegar_20260820.json \
  --ledger results/fixed_u_a1_three_good_cuts_20260820.jsonl \
  --maximum-rounds 500 --master-timeout-seconds 300 \
  --oracle-timeout-seconds 300 --edge-cap 4 --random-seed 820
```

Run the independent cardinality-free arithmetic audit:

```bash
python -m tracks.parkability.audit_fixed_u_a1_three_good_universal_allocation \
  --profile results/fixed_u_wild_forced_terminal_profile_20260820.json \
  --repair results/fixed_u_terminal_profile_unrestricted_physical_decision_20260820.json \
  --ledger results/fixed_u_a1_three_good_cuts_20260820.jsonl \
  --output results/fixed_u_a1_all_cardinalities_independent_audit_20260820.json
```

Focused verification:

```bash
pytest -q \
  tracks/parkability/test_fixed_u_a1_three_good_cegar.py \
  tracks/parkability/test_fixed_u_a1_three_good_independent_audit.py
```

Recorded result hashes:

```text
d242ba0be179ce348a18e69c5192f290439ad49d6f30b361ec9336555a06e6b0  results/fixed_u_a1_three_good_cegar_20260820.json
d13829a7daa0f92909868388c148f6c41180df2c97868f100f68223e72221195  results/fixed_u_a1_three_good_cuts_20260820.jsonl
9693c4753d5abbebb6009f916bcfbb1c8c6f4ae8ceb9d82d88bb0aca906ee94c  results/fixed_u_a1_all_cardinalities_independent_audit_20260820.json
```

## Exact claim boundary

This closes every realization of `a1` in the single immutable terminal profile
and removes that profile as a threat to the active four-edge program. It does
not prove the four-edge theorem for all fixed-`U` states, extend the form-2
chart to every saturated state, or prove general additive EFX existence.

The highest-value next step is no longer a larger `a1` atomization. It is to
extract the unsplit-role aggregate criterion as a reusable selector and prove
that every remaining saturated fixed-`U` separator admits a four-edge
allocation in which each realization-dependent wild role is kept whole, or
else isolate the next profile where every valid allocation necessarily splits
two or more wild roles.
