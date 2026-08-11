# Flower three-rotation polarity lemma

**Date:** 2026-08-10

**Status:** cap-free analytic reduction; the final opposite-sign wall remains
open

## Statement

Let `(X,{f})` be a positive additive partial EFX allocation with unenvied
charity, and suppose a mutual genuine `f`-champion cycle decomposes

\[
X_r=T_r\mathbin{\dot\cup}B_r,
\qquad
X_q=T_q\mathbin{\dot\cup}B_q,
\]

with nonempty top and bottom packets.  Assume the desired bundles

\[
D_r=T_q+f,
\qquad D_q=T_r+f
\]

are common-safe and are strictly desired by `r,q`, respectively.

Then either there is an EFX-with-charity allocation `Y` with `r` weakly
nonworse and `q` strictly better, or all three inequalities

\[
v_r(f)>v_r(B_q), \tag{R}
\]

\[
v_q(B_q)\ge v_q(f), \tag{Q1}
\]

\[
v_q(T_r)>v_q(T_q),
\qquad
v_q(B_q)>v_q(B_r) \tag{Q2}
\]

hold simultaneously.

The result is independent of the numbers of goods in the four packets.

## Proof

Every packet used as charity below is dominated by every base owner.  For
example, choosing any `t in T_q` in the base EFX inequality against `X_q`
gives `v_i(X_i)>=v_i(B_q)`; choosing a good of `T_r` similarly gives
`v_i(X_i)>=v_i(B_r)`.

Consider the following three disjoint allocations:

\[
Y^{(1)}=(X_r,\ T_q+f,\ X_c,\ X_s;\ B_q),
\]

\[
Y^{(2)}=(T_q+B_q,\ T_r+f,\ X_c,\ X_s;\ B_r),
\]

\[
Y^{(3)}=(T_q+f,\ T_r+B_r,\ X_c,\ X_s;\ B_q).
\]

All assigned bundles in these allocations are common-safe: they are base
bundles or one of `D_r,D_q`.  Therefore each allocation is EFX with charity
as soon as its two changed recipients are paid.

1. In `Y^(1)`, `r` is fixed.  If `v_q(f)>v_q(B_q)`, then `q` improves and
   the theorem closes.  Failure forces (Q1).
2. In `Y^(2)`, `q` receives `D_q` and improves.  If `r` weakly prefers
   `X_q=T_q+B_q` to `X_r`, the theorem closes.  Otherwise, since `r`
   strictly prefers `T_q+f` to `X_r`, subtraction gives (R).
3. In `Y^(3)`, `r` receives `D_r` and improves.  If `q` strictly prefers
   `X_r` to `X_q`, the theorem closes.  Otherwise, `q`'s strict preference
   for `T_r+f` over `X_q`, together with (Q1), gives
   `v_q(T_r)>v_q(T_q)`.  Combining this with
   `v_q(T_r+B_r)<=v_q(T_q+B_q)` gives
   `v_q(B_q)>v_q(B_r)`.

Thus simultaneous failure of all three rotations forces (R), (Q1), and
(Q2).  \(\square\)

## Interaction with the residual-top gate

The lemma applies before choosing an external bottom edge.  Combining it
with the dual-full-capture escape theorem shows that every surviving
flexible `GG` obstruction has both:

1. a payment-critical residual `J=T_r\(A_r\cap T_r)` omitted by the external
   `(B_q|B_r)` desired bundle; and
2. an opposite ranking of the same floater/bottom pair in the two mutual
   owners' rows, together with `q`'s strict top/bottom orientation (Q2).

This is the correct input for a residual recapture operation: transferring
`B_q` toward `r` pays in `r`'s row only after it is replaced by `f`, while
`q` needs value from the omitted part of `T_r` to surrender `B_q`.

The three scalar implications replay as QF_LRA-UNSAT in
[`flower_three_rotation_polarity_audit.json`](flower_three_rotation_polarity_audit.json).

All seven previously frozen flexible-completion profiles fail at least one
of the three rotations or the retained-top payment extension; none reaches
the live polarity cell.  The same census also shows why simply demanding a
new champion source is not a valid general argument: outside the live cell,
three profiles have only the original external source `c` for the
residual-augmented target, and one has no desired subset retaining a residual
good at all.  See
[`residual_top_champion_source_census.json`](residual_top_champion_source_census.json).
These are adversarial regressions, not a cap-free exhaustion.

## Claim boundary

This lemma does not prove that the opposite-sign wall is inconsistent.  It
does not close the full `GG` flower or four-agent additive EFX.  Its gain is
to replace an unrestricted adaptive-completion search by one explicit
aggregate orientation that every remaining countermodel must satisfy.
