# Alternating two-safe-bundle binary theorem

**Date:** 2026-08-09
**Status:** exact Z3 QF_LRA theorem; independent encoding audit pending
**Cell:** `(2,2,2,2)` and priority order `(p,s,r,q)`

## Theorem

In every strict valuation profile satisfying the corrected alternating
structural premises in the full binary packet cell, there are disjoint
bundles `D,Q` such that:

1. `D` is a desired set for `s` or `r` at the base allocation;
2. `Q` is deletion-safe for every base observer; and
3. `v_q(Q) >= tau_q(D)`.

Consequently there is an external-observer-safe EFX allocation fixing
`p={x}` whose utility vector lexicographically improves the base vector in
order `(p,s,r,q)`.

## Exact decision

There are nine residual goods besides `x,y`.  The decision procedure
enumerates every nonempty candidate `D`, every disjoint candidate `Q`, and
both possible recipients `s,r`.  Empty `Q` is omitted only when `|D|>1`,
where strict positivity makes `v_q(Q)>=tau_q(D)` impossible.  This leaves
37,338 symbolic pairs.

For each pair the solver asserts the negation of the three conditions above,
in addition to the complete corrected structural cell.  Z3 5.0.0 returns
`unsat`:

- [`alternating_two_safe_bundle_gate_2222.json`](alternating_two_safe_bundle_gate_2222.json)
- [`decide_alternating_two_safe_bundle_gate.py`](../tracks/parkability/decide_alternating_two_safe_bundle_gate.py)

The cap-free
[`two-safe-bundle reduction`](ALTERNATING_TWO_SAFE_BUNDLE_REDUCTION.md)
proves directly that every surviving pair yields the required EFX
lexicographic allocation.  Thus the solver theorem is not relying on a
post-hoc empirical correlation between pairs and allocations.

Together with the fourteen previously proved proper faces and the atomic
cell, this settles every packet-size vector in `{1,2}^4` for the surviving
order.  Half-turn relabeling gives the corresponding bounded theorem for
`(s,p,q,r)`.

## False strengthenings found en route

Three smaller base-remainder claims are exactly refuted in the same strict
cell.  They successively require `Q=X_q\D` and:

1. `D` to be a common base-safe desired set;
2. safety only for the fixed observers and the recipient-facing remainder;
3. no extra condition beyond the resulting allocation being EFX.

Each refuting profile still has hundreds of broader singleton-return
escapes, and each has many two-safe-bundle pairs.  The countermodels are:

- [`alternating_base_q_remainder_gate_2222.json`](alternating_base_q_remainder_gate_2222.json)
- [`alternating_base_q_remainder_recipient_relaxed_gate_2222.json`](alternating_base_q_remainder_recipient_relaxed_gate_2222.json)
- [`alternating_base_q_remainder_exact_efx_gate_2222.json`](alternating_base_q_remainder_exact_efx_gate_2222.json)

These refutations show that an arbitrary disjoint safe `Q`, rather than the
remainder of `q`'s original bundle, is essential.

## Verification boundary and cap-free gate

The UNSAT status currently comes from one direct generator and one exact
solver implementation.  The frozen-profile analyzer independently checks
the semantic pair conditions on all recorded SAT models, but it is not an
independent proof of UNSAT.  A second generator/solver replay or a checked
certificate remains required before referee-grade bounded publication.

The theorem is finite: it does not establish the safe-pair packing lemma for
packets larger than two.  The next analytic step is to extract a small core
of the 37,338 pair blockers and prove that any minimal counterexample with a
larger packet admits a critical-minimum contraction or the same finite wall
contradiction.
