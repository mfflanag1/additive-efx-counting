# GG rank-reset monotonicity objective resolution

**Date:** 2026-08-11

**Status:** the requested four-coordinate theorem is exactly refuted; the
broader corrected GG closure remains open

## Requested statement

The proposed cap-free potential was

\[
 \Phi=(|U|,R,|V|,v_d(W)),                           \tag{1}
\]

where `U` is retained support, `R` is current maximum response-matching
rank, `V` is the represented owner union, and `d,W` are the current missing
owner and residual.  The objective required every surviving root-monopoly
or sacrificed-`q` Hall reset to increase (1), or to close by EFX, a
lexicographic improvement, or a release-compatible Pareto improvement.

That statement is false.  The failure is exact and cap-free; it is not a
timeout, a bounded-cell gap, or a numerical approximation.

## Structural no-go theorem

Every premise used to define a positive-additive EFX response state is
invariant under independent positive rescaling of each valuation row:

\[
 v_i\mapsto \lambda_i v_i,\qquad \lambda_i>0.       \tag{2}
\]

This preserves EFX comparisons, desired sets, common safety, response
edges, matching rank, represented owners, retained support, and the fixed-
priority lexicographic order of allocations.  If a reset changes the hole
from `d` to `e` while the first three coordinates tie, its proposed last
comparison is

\[
 v_e(W')\mathrel{?}v_d(W).                          \tag{3}
\]

Rescaling row `e` reverses (3) without changing any structural premise or
the reset.  Therefore raw residual utilities belonging to different owners
cannot be a global monotonicity coordinate.  Global lex maximality cannot
repair this dimensional defect because row scaling preserves every within-
row lexicographic comparison as well.

## Exact positive-additive countermodel

[`GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md`](GG_RANK_RESET_RAW_POTENTIAL_REFUTATION_20260811.md)
gives a nine-good, four-agent positive and subset-sum-injective instance.
Its common-safe response partition has neighborhoods

\[
 N(A_r)=\{r\},\quad N(W)=\{r\},\quad
 N(A_c)=\{q,c\},\quad N(A_s)=\{s\}.                \tag{4}
\]

Thus `A_r,W` are the surviving root-monopoly pair, maximum rank is three,
and the represented owner union has size four.  One non-EFX compression
has sacrificed hole `q`; the exact cross-star reset changes the hole to `c`
while retained support, rank, and owner union remain tied.  In the original
rows

\[
 v_c(A_r)<v_q(W),                                   \tag{5}
\]

but multiplying only row `c` by two reverses (5), preserves (4), and leaves
both displayed states non-EFX.  The exact audit enumerates all subset sums
and response matchings.

This countermodel refutes the monotonicity theorem (1), not GG closure.  A
separate exhaustive `5^9` allocation census confirms that the displayed
base is not itself globally lex maximal.  That limitation is stated rather
than hidden: the row-scaling theorem rules out the coordinate, while the
finite witness proves the offending root-monopoly/hole-changing transition
is nonvacuous in the exact positive-additive response geometry.

## Why the obvious repair is still insufficient

Replacing (3) by owner-indexed normalized residual maxima and replacing
current rank/coverage by historical envelopes removes the scaling defect.
It does not yield a strict potential.  The same exact instance contains a
four-state non-EFX plateau with identical retained support, historical rank,
owner coverage, owner-indexed residual ledger, and residual-support history;
see
[`GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md`](GG_HISTORICAL_SUPPORT_LEDGER_STAGNATION_REFUTATION_20260811.md).
An eleven-good positive lift also keeps absorbed and consumed bottom-support
coordinates fixed across the plateau; see
[`RETAINED_BOTTOM_LEDGER_STAGNATION_REFUTATION_20260811.md`](RETAINED_BOTTOM_LEDGER_STAGNATION_REFUTATION_20260811.md).

Consequently no collection of monotone “ever seen” versions of the four
requested coordinates supplies the missing strictness after saturation.

## Smallest additional operation

The smallest successful repair is operational, not another cross-owner
scalar:

1. choose the anchor-compatible maximum matching with deterministic current-
   state source priority;
2. retain physical support consumed from the current paid anchor; and
3. when the same `(hole,anchor,support)` state returns, splice the repeated
   root-facing return and residual compensation as one surplus-budgeted
   connected component, rather than recompressing once more.

The exact plateau has an EFX exit of precisely this three-owner cycle-splice
form.  Current work proves the matching selector and monotonic paid-anchor
consumption/reset, but universal feasibility and observer safety of the
connected splice remain open.  Those are the correct next GG theorem, not
the false potential (1).

## Claim boundary

This resolves the stated rank-reset objective by exact refutation and
identifies the smallest missing operation.  It does **not** prove the
corrected connected-splice theorem, close the `GG` flower, close the other
three-nonsingleton classes, handle the four-nonsingleton or degeneracy
wrappers, or prove four-agent/general additive EFX.

[`gg_rank_reset_monotonicity_objective_resolution_audit.json`](gg_rank_reset_monotonicity_objective_resolution_audit.json)
replays every fact used in this resolution against the authoritative exact
audits.
