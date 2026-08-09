# Alternating singleton-return target

**Date:** 2026-08-09
**Status:** proved in the full binary cell through the two-safe-bundle theorem; cap-free lift open
**Order:** `(p,s,r,q)` with `p` fixed at `{x}`

## Candidate

In the alternating state, an external-observer-safe rooted lexicographic
escape exists in at least one of two families:

1. **Return `r` to `{y}`:** keep `p={x}` and `r={y}`, and repartition any
   subcollection of the remaining goods between `s`, `q`, and charity.
2. **Anchor `s` at `{y}`:** keep `p={x}` and `s={y}`, and repartition any
   subcollection of the remaining goods between `r`, `q`, and charity.

This is a genuine two-active-agent repartition statement. It does not
prescribe which top or bottom packet supplies an exchanged good.

## Why the target has this form

Three narrower menus have now been decided exactly in the corrected full
binary `(2,2,2,2)` cell.

### Selected-root plus bottom transfer: refuted

A 112-allocation menu allowed:

- `s` to receive only the selected block `T_q+f`, with `q` restricted to a
  subset of `X_r+B_q`; or
- a nonempty subset of `B_q` to move to `r`, with arbitrary release from
  `X_r`.

Z3 found an exact strict structural countermodel. It has 11,330 rooted EFX
allocations and 2,022 rooted lexicographic escapes, but none in the menu.
Its smallest escape gives `s` a proper subset such as `{bq0,f}`. See
[`alternating_bottom_partition_dichotomy_2222_audit.json`](alternating_bottom_partition_dichotomy_2222_audit.json).

### Any root-offer subset plus bottom transfer: refuted

Allowing `s` every nonempty subset of `X_q` together with `f` expands the
menu to 1,088 allocations. A second exact countermodel blocks all of them
but has 2,568 rooted lexicographic escapes. Its smallest escape transfers a
good from `T_q`, not `B_q`, to `r`. See
[`alternating_any_root_subset_dichotomy_2222_audit.json`](alternating_any_root_subset_dichotomy_2222_audit.json).

### Any root-offer subset plus any cross transfer: refuted

Allowing every nonempty incoming subset of all `X_q` and every release from
`X_r` gives a 1,280-allocation menu. A third exact countermodel blocks it but
has 1,252 rooted lexicographic escapes. Its smallest escapes instead give
`s` mixed subsets using goods from `X_r`. See
[`alternating_any_cross_subset_dichotomy_2222_audit.json`](alternating_any_cross_subset_dichotomy_2222_audit.json).

These profiles refute restrictions on the packet origin of the moved goods;
none refutes the external-observer lemma. Every profile has an escape in the
singleton-return union above.

## Bounded full-binary test

The singleton-return family contains exactly 39,366 distinct allocations in
the eleven-good cell. A targeted exact CEGAR seeded by the three adversarial
profiles processed 12 further exact models. Every model had a
singleton-return escape. The preserved pool has 1,513 valid blockers.

The terminal master returned `unknown` at 120 seconds:

- [`alternating_singleton_return_0213_session1.json`](alternating_singleton_return_0213_session1.json)
- [`alternating_singleton_return_0213_pool.json`](alternating_singleton_return_0213_pool.json)
- [`run_alternating_singleton_return_cegar.py`](../tracks/parkability/run_alternating_singleton_return_cegar.py)

That CEGAR run was neither an UNSAT theorem nor a SAT refutation. A later,
more structured direct formula proved the full binary cell: every profile
has two disjoint base-safe bundles satisfying the
[`two-safe-bundle reduction`](ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md).
The exact theorem is
[`ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md`](ALTERNATING_TWO_SAFE_BUNDLE_BINARY_THEOREM.md).
No further blind pool growth is needed.

## Analytic route

The target separates the active problem into a common downward-closed
safe-set system. The binary theorem finds disjoint safe bundles `D,Q`, with
`D` desired by `s` or `r` and `q(Q)>=tau_q(D)`. The analytic reduction then
constructs one of the two singleton-return allocations. For any proposed
bundle, EFX against an observer is controlled by its total value and its
minimum-value deletion good.

The cap-free
[`critical-minimum contraction lemma`](EFX_CRITICAL_MINIMUM_CONTRACTION_LEMMA.md)
therefore reduces the proof obligation to the case where every possible
merge destroys a critical minimum in at least one of the two families. The
next lemma should show that simultaneous critical coverage in both families
creates either:

1. one of the six atomic wall contradictions;
2. a forbidden compatible desired family; or
3. a safe exchange between the two active agents.

The exact
[`atomic wall lemma`](ALTERNATING_EXTERNAL_OBSERVER_ATOMIC_WALL_LEMMA.md)
already supplies alternatives 1--2 when every packet is atomic.

## Claim boundary

The six other hard external-observer orders remain exactly refuted by strict
seven-good profiles. The singleton-return target concerns only the surviving
order `(p,s,r,q)` and, by half-turn symmetry, `(s,p,q,r)`. Both are now
proved throughout the bounded packet grid `{1,2}^4`, but neither is proved
for arbitrary packet sizes. Complete four-agent additive EFX is not proved.
