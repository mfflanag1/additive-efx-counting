# GG rank-reset raw-potential refutation

**Date:** 2026-08-11

**Status:** exact refutation of the proposed raw residual coordinate; the
corrected scale-invariant support-ledger termination theorem remains open

## Proposed coordinate

The connected-path checkpoint proposed the lexicographic state value

\[
 (|U|,\ \operatorname{rank},\ |V|,\ v_d(W)),       \tag{1}
\]

where `d` is the current missing source and `W` is her residual.  The first
three coordinates are combinatorial.  The last is not a valid global state
coordinate when a hole pivot changes `d`.

## Scale obstruction

All additive-EFX, common-safety, desired-response, flower, and fixed-priority
lex-maximality premises compare values within one agent's row.  They are
therefore unchanged by independent positive row scaling

\[
 v_i\longmapsto \lambda_i v_i\qquad(\lambda_i>0).   \tag{2}
\]

Suppose a priority-valid pivot changes the missing owner from `d` to `e`
while retaining `U`, response rank, and owner union.  The last comparison in
(1) is then

\[
 v_e(W')\mathrel{?}v_d(W).                          \tag{3}
\]

Scaling only row `e` changes either direction of (3) without changing any
premise or response edge.  Consequently no theorem derived from the
scale-invariant GG premises can force raw cross-owner residual monotonicity.
Global lex maximality does not repair the issue: multiplying one fixed
lexicographic coordinate by a positive constant preserves all comparisons
between allocations in that coordinate.

There is a second definitional failure.  A rank-three all-owner compression
has one missing owner, but its canonical rank-two reset has two.  Thus the
fourth coordinate of (1) ceases to be single-valued precisely at the reset
that it was intended to control.  In addition, instantaneous response rank
drops from three to two, so putting current rank before every residual
coordinate makes the reset lexicographically smaller regardless of a
strict residual gain.

## Exact positive additive witness

The audit
[`gg_rank_reset_raw_potential_refutation_audit.json`](gg_rank_reset_raw_potential_refutation_audit.json)
uses nine goods and four positive, subset-sum-injective additive rows.  Its
base allocation is EFX and dominates the charity good.  Four pairwise
disjoint common-safe targets have response neighborhoods

\[
 N(A_r)=\{r\},\quad N(A_c)=\{q,c\},\quad
 N(A_s)=\{s\},\quad N(W)=\{r\}.                    \tag{4}
\]

The maximum response rank is exactly three.  Selecting `c` for `A_c`
leaves `q` as the residual owner.  The proved cross-star pivot selects `q`
for `A_c`, moves `r` to `W`, and leaves `c` as the residual owner.  The
retained support, maximum rank, and four-owner union are unchanged, while

\[
 v_c(A_r)<v_q(W).                                   \tag{5}
\]

Both displayed allocations are non-EFX.  Multiplying only `c`'s row by two
preserves (4), base EFX, common safety, every desired comparison, and both
allocations' EFX status, but reverses (5).  The replay uses exact
`Fraction` arithmetic and exhausts all response matchings and all subset
sums.

This witness refutes (1) as a potential across the already proved
hole-changing operation.  It is not a counterexample to GG closure: it does
not assert global lex maximality or absence of every larger generalized PI
component.

The complete exact globality census
[`gg_rank_reset_raw_potential_globality_gap_audit.json`](gg_rank_reset_raw_potential_globality_gap_audit.json)
checks all `5^9` allocations, including charity, and all 24 priority orders.
There are 4,126 EFX-with-charity allocations, and the displayed base is not
globally lex maximal under any priority.  Thus this witness cannot be promoted
to a counterexample to the full GG bridge; its valid claim is exactly the
scale obstruction to the raw cross-owner coordinate.

## Smallest viable repair

Two changes are forced rather than optional.

1. Replace the raw scalar `v_d(W)` by the owner-indexed, scale-invariant
   residual ratios

   \[
   \rho_i=\max\{v_i(W_i)/v_i(X_i):
   i\text{ has occurred as a hole at the retained state}\}.             \tag{6}
   \]

   Keep the entire fixed-order vector `(rho_q,rho_c,rho_s)`; never compare
   utilities belonging to different rows.
2. Replace current rank and current owner union by the historical envelope
   `(R^*,V^*)`: the maximum response rank and accumulated physical supplier
   set reached since the last strict enlargement of `U`.  A rank-two reset
   then cannot erase earlier rank-three progress.

The corrected candidate is

\[
 (|U|,R^*,|V^*|,\rho_q,\rho_c,\rho_s,H),             \tag{7}
\]

where `H` is the finite set of residual-side physical supports already used.
The support ledger is necessary only when a hole repeats: a repeated owner
with fresh disjoint support grows `H`, while a repeated support must close a
release-compatible cycle or enter the existing hitting-set polarity.  Thus
the smallest missing *operation* is the already identified
support-sensitive recurrence closure; another scalar weighted-Hall
inequality cannot repair (1).

## Remaining theorem

To close GG, one must still prove that every sacrificed-`q` reset either
increases a coordinate of (7), closes by EFX/PI, or turns a repeated
`(owner,support)` pair into the retained-support/hitting-set handoff.  The
present result removes the false raw potential from that obligation; it
does not prove the corrected monotonicity theorem, close GG, or prove
four-agent additive EFX.
