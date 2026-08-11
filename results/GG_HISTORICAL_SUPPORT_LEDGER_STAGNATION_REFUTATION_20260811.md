# GG historical-support-ledger stagnation refutation

**Date:** 2026-08-11

**Status:** exact refutation of the corrected ledger as a strict termination
potential; global component extraction remains open

## Corrected candidate

After raw cross-owner residual value was refuted, the proposed fixed-`U`
state history was

\[
 (|U|,R^*,|V^*|,\rho_q,\rho_c,\rho_s,H),             \tag{1}
\]

where `R*` is historical maximum response rank, `V*` the accumulated
supplier union, each `rho_i` the maximum normalized residual value seen
while `i` was a hole, and `H` the set of residual-side physical supports
already used.

All coordinates in (1) are scale invariant or combinatorial, and none
decreases.  That is not enough: the same exact bounded witness used to
refute raw residual comparison contains a saturated plateau of (1).

## Four-state plateau

Use the pairwise-disjoint common-safe partition

\[
 A_r,\ A_c,\ A_s,\ W
\]

with response neighborhoods

\[
 N(A_r)=\{r\},\qquad N(A_c)=\{q,c\},\qquad
 N(A_s)=\{s\},\qquad N(W)=\{r\}.                    \tag{2}
\]

The maximum response rank is three and the represented owner union is all
four owners.  There are four natural maximum-rank compressions: choose
either `A_r` or `W` for `r`, choose either `q` or `c` for `A_c`, fix `A_s`
at `s`, and give the remaining root-neighborhood bundle to the remaining
hole.  Explicitly, their `(root target, A_c source, hole, residual)` labels
are

\[
 (A_r,q,c,W),\quad(A_r,c,q,W),\quad
 (W,q,c,A_r),\quad(W,c,q,A_r).                      \tag{3}
\]

All four complete allocations are non-EFX.  There is no full response SDR,
because both `A_r` and `W` have the unique source `r`.

After a history has visited the two possible residual supports for each
possible hole, `R*=3`, `V*` contains all owners, `H={A_r,W}`, and

\[
 \rho_q=\max\{v_q(A_r),v_q(W)\}/v_q(X_q),
 \qquad
 \rho_c=\max\{v_c(A_r),v_c(W)\}/v_c(X_c).           \tag{4}
\]

Every later move among the four states in (3) leaves every coordinate of
(1) unchanged.  The states remain distinct and non-EFX, so (1) is not a
strict state ranking and finiteness plus historical maxima cannot by itself
exclude recurrence.

## Consequence

Adding further monotone “ever seen” maxima has the same structural problem:
once their finite domains saturate, they no longer orient transitions among
the remaining compressed allocations.  A valid closure therefore needs at
least one of the following.

1. A deterministic current-state ranking that is proved to decrease under
   every permitted reset, not merely a historical envelope.
2. A theorem converting a repeated plateau state directly into a
   release-compatible generalized PI component.
3. A surplus-budgeted connected transfer operation that exits the entire
   four-state compression family at once.

The third option matches the exact hard flower geometry: its first EFX
escape is a branching four-owner component, not another rank-three
recompression.

## Claim boundary

The exact audit proves plateau equality for the displayed local response
system.  It does not prove that every transition in an arbitrary flower
repair algorithm may traverse the four states in the displayed cyclic
order.  A deterministic selector with an additional current-state invariant
could still terminate.  The witness does not assert global lex maximality or
generalized PI-freeness, and it is not a counterexample to `GG` closure or
four-agent additive EFX.
