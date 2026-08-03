# Heavy-token matching lemma and three-case residual

## Canonical theorem

Work in the cyclic pair-Hall cell with base

\[
01\mid23\mid45\mid67;\qquad f=8.
\]

Let owner \(i\)'s core be \(c_i=2i\).  Put a strict heavy edge from owner
\(i\) to token \(t\in\{1,3,5,7,8\}\) when

\[
v_i(t)>v_i(c_i).
\]

The proved owner walls remove each owner's own token, the floater, and the
preceding token from this graph.  The rotating-token lemma permits the cyclic
canonicalization \(v_0(3)\le v_0(0)\).  Only seven heavy edges can then remain:

\[
(0,5),(1,5),(1,7),(2,7),(2,1),(3,1),(3,3).
\]

Under the archived 159 global cuts, 78 matching cuts, 38 whole-orbit blockers,
the pair-Hall cell, both owner walls, all eight cross-row clauses, and the
canonical next-token inequality, this seven-edge graph has matching number at
most one.

Equivalently, any two strict heavy edges must share their owner or their token.
Adding the negation of this statement makes the exact QF_LRA formula UNSAT.
Arithmetic-solver-2 Z3 returned UNSAT in 89.38 seconds.  A tracked replay
returned UNSAT with a 120-label core.  cvc5 1.3.3 timed out at 300 seconds, so
the theorem is currently Z3-confirmed rather than independently
solver-confirmed.

An exact 128-pattern sign cover gives a second proof route.  Every one of the
114 patterns with matching number at least two is UNSAT under a ten-second
arithmetic-solver-2 bound.  The remaining fourteen patterns have matching
number zero or one; four are also UNSAT and ten remain undecided at that
bound.  This cover proves the matching-number statement even though it does
not decide the full source.

## Cyclic compression to three cases

The theorem can be reapplied after any valid cyclic re-canonicalization of a
hypothetical full antecedent.  Two additional representative exclusions are
exactly UNSAT:

- owner 1 cannot have both heavy edges \((1,5)\) and \((1,7)\); and
- token 7 cannot have both heavy edges \((1,7)\) and \((2,7)\).

The arithmetic-solver-2 direct checks took 33.51 and 107.31 seconds.  Cyclic
re-canonicalization maps any two-edge owner-star or token-star to one of these
representatives.  Hence a genuine surviving obstruction has at most one
heavy edge in total.

There are consequently only three global residual types:

1. no heavy edge;
2. one next-token heavy edge; or
3. one opposite-token heavy edge.

Inside the canonical formula these have representatives with seven-bit masks
0, 2, and 1, respectively.

## Full-orbit gate

All 120 exact token-orbit completion obstructions have now been preloaded.
The first combined solve produced a finite-pool SAT valuation, but exact
global audit proved that its base was not threshold-maximal and supplied four
cyclic global cuts, increasing the pool from 159/78/120 to 163/78/120.

The two nonzero representatives are now closed.  The single opposite-token
case (mask 1) first produced a finite-pool SAT valuation, but exact global
audit supplied four more maximality cuts.  The resulting 167/78/120 formula
is UNSAT.  The single next-token case (mask 2) is UNSAT at 163/78/120 under
QF_LRA.

The zero-edge representative remains open, but its boundary is now much
sharper. A witness-cut CEGAR pool contains 167 global cuts and 4,084 exact
completion-witness cuts. Splitting the seven weak token/core comparisons
into equality versus strict cases gives an exact 128-case cover:

- 127 cases are UNSAT;
- only the all-strict case remains UNKNOWN.

The all-strict source was then split into 16 exhaustive literal cubes. Two
leaves (7 and 9) are UNSAT and fourteen time out at 300 seconds under
arithmetic-solver-2. A fresh rerun reproduces the same 2/14 verdict
histogram. Neither run finds a SAT valuation.

This is a stopping boundary, not a closure claim. Additional witness-cut
harvesting has diminishing value, so the active proof route moves to the
cap-free bottleneck Hall-cut and charity/minimum exchange lemmas. UNSAT of
all fourteen surviving leaves would close the zero-heavy representative and
hence the cyclic pair-Hall branch, but not the arbitrary-core four-agent
theorem.

Durable artifacts:

- minimum_slot_orbit_pair_hall_zero_heavy_pool2099.json;
- minimum_slot_orbit_pair_hall_zero_heavy_equalities_arith2_240.json;
- minimum_slot_orbit_pair_hall_zero_heavy_pool4084.json;
- minimum_slot_orbit_pair_hall_zero_heavy_strict_export.json;
- minimum_slot_orbit_pair_hall_zero_heavy_strict_cover_d4.json;
- minimum_slot_orbit_pair_hall_zero_heavy_strict_cover_d4_arith2_300.json;
  and
- minimum_slot_orbit_pair_hall_zero_heavy_strict_cover_d4_arith2_300_replay.json.

Both strict-cover decisions use source SHA-256
0186b57a1d71ca99b5e1d06b6668fbe872c79b5f81391a16a6087d79180d23cc.

## Claim boundary

The heavy-token matching theorem is a new structural reduction inside the
cyclic pair-Hall branch.  Neither that branch, four-agent complete EFX, nor
general additive EFX is yet proved by this checkpoint.
