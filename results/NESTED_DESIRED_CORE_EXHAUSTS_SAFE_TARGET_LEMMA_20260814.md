# Nested desired core exhausts a common-safe target

**Date:** 2026-08-14

**Status:** cap-free analytic lemma; closes the parked-singleton inequality in
the allocated-`E` form-0 chart, but not the universal normalization bypass

## Lemma

Let `C subseteq Q` be physical packets, let `i` be an observer, and let `F`
be a floor.  Suppose

\[
                         v_i(C)>F                 \tag{1}
\]

and the whole target `Q` is common-safe at that floor for observer `i`:

\[
                         \tau_i(Q)\le F.          \tag{2}
\]

Then

\[
                         C=Q.                     \tag{3}
\]

Indeed, if `g in Q-C`, then positivity and containment give

\[
                 v_i(Q-g)\ge v_i(C)>F,           \tag{4}
\]

contradicting (2).  No item-count bound or atom compression is used.

## Singleton-charity consequence

Suppose `C` is transferred from current holder `q` to a strict root and the
whole old target `Q=Y_q` satisfies (2).  Lemma (3) leaves `q` with the empty
residual.  For every positive singleton charity `{p}`,

\[
                         v_q(p)>0=v_q(\varnothing). \tag{5}
\]

The singleton `{p}` is automatically common-safe.  Thus any completion that
places `p` at a different nonroot holder has an exact current-safe/current-
desired `q` response hitting the whole singleton.  The "response avoids the
retired packet because `p` is parked for `q`" inequality is impossible in
this branch.

## Application to the 21-role form-0 master

In the allocated-`E` form-0 cell:

- `Q` is a base-common-safe desired target;
- the fixed `r->q` anchor core `C` is desired by `r` above either the base
  floor or the current root bundle, which itself contains the strict packet
  `A`; and
- `C subseteq Q`.

Hence (1)--(3) force the post-anchor `q` residual to be empty.  The optional
anchor-charity bypass master becomes UNSAT from the single added inequality
`v_q(p)<=v_q(Q-C)`.  The named and formula-level cores are recorded in
`allocated_e_form0_anchor_charity_bypass_audit.json`.

## Boundary

This lemma is cap-free, but its application requires the *whole* anchor
target `Q` to be common-safe at the same floor.  The frozen universal
rank-three predicate guarantees that the selected anchor core is
common-safe; it does not currently guarantee that the entire physical
target bundle is.  Therefore the lemma closes the parked inequality in the
declared form-0 chart, not the general nonroot normalization bypass, the
fixed-`U` theorem, or general additive EFX.
