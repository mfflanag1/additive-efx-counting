# Form-2 six-branch payment-compression lemma

**Date:** 2026-08-14

**Status:** cap-free exact compression of six owner-payment tests to three;
shared-target uncrossing and observer continuation remain separate gates

## Inputs

Let the represented form-2 response cycle have physical cores

\[
 R\subseteq B_q\quad(r\text{ receives}),\qquad
 Q\subseteq B_s\quad(q\text{ receives}),\qquad
 S\subseteq B_r\quad(s\text{ receives}).          \tag{1}
\]

Let `D_r subseteq B_r` and `D_q subseteq B_q` be the unmatched owner's two
responses.  On the disjoint branch assume

\[
                 D_r\cap S=\varnothing,
                 \qquad D_q\cap R=\varnothing.     \tag{2}
\]

Choose one of `D_r,D_q`, omit one of `R,Q,S`, reverse the other two cycle
cores, return the chosen `d` core, and send singleton charity `p` to the
omitted cycle source.  These are exactly the six branches of
`THREE_CYCLE_SIX_BRANCH_CHARITY_COMPLETION_LEMMA_20260813.md`.  Every branch
uses two cycle edges, one `d` edge, and one charity edge.  All owners except
the omitted cycle source receive a desired response and are strictly paid.

## Six tests collapse to three

Write `Delta_i=v_i(B_i)-v_i(X_i)`.  For the two branches omitting `r`, the
packets supplied by the omitted owner are respectively

\[
                         S,\qquad S\mathbin{\dot\cup}D_r.
\]

Because values are nonnegative, both branches fail owner payment exactly
when the cheaper one fails:

\[
                         v_r(S)>\Delta_r+v_r(p).   \tag{3}
\]

Likewise, the two branches omitting `q` lose respectively `R` and
`R\mathbin{\dot\cup}D_q`, so both fail exactly when

\[
                         v_q(R)>\Delta_q+v_q(p).   \tag{4}
\]

Both branches omitting `s` lose exactly `Q`, hence both fail exactly when

\[
                         v_s(Q)>\Delta_s+v_s(p).   \tag{5}
\]

Consequently simultaneous owner-payment failure of all six branches is
equivalent to the three-cycle supplier-capture system (3)--(5).  It is not a
six-inequality terminal.

Two of the six paths do not use a shared target at all: `D_q` with omitted
`r`, and `D_r` with omitted `s`.  Thus (3) and (5) are unavoidable even
before any uncrossing.  The only missing payment coordinate on the overlap
branch is (4), or else a full-margin capture at `B_q`; the analogous root
overlap has already been isolated by the form-2 root-star lemma.

## Consequence

The cap-free analytic target is now shorter:

> Either one of the six response branches pays every owner, a shared-target
> uncrossing fails with a certified double-margin packet, or every physical
> cycle supplier values its outgoing response core above its entire current
> base margin plus charity as in (3)--(5).

Any paid but non-EFX branch produces a paid decorated response.  Eliminating
the three supplier-capture inequalities must use generalized PI, signed
support drainage, or saturation; scalar nonnegativity alone does not do it.

## Claim boundary

Proved: conservation/edge count inherited from the six branches and the
exact equivalence between their six owner-payment failures and (3)--(5) on
the disjoint branch, for arbitrary packet sizes.

Not proved: universal shared-target disjointness, observer safety, a
contradiction from (3)--(5), the fixed-`U` theorem, or general EFX.
