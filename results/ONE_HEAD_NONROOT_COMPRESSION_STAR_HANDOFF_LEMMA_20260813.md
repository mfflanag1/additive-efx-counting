# One-head nonroot compression-star handoff lemma

**Date:** 2026-08-13

**Status:** cap-free elimination of the one-head simultaneous-payment gate;
only a root-facing acceptance row or the existing compressed-star recurrence
survives

## Paid one-head candidate

Let `X` be the fixed-priority globally maximal partial EFX base, with the
earlier root `r` first in the priority.  Let

\[
 Z=(Z_i)_{i\in N}
\]

be a residual-completed mixed-cycle candidate whose bundles partition the
current physical pool and satisfy

\[
 v_i(Z_i)>v_i(X_i)\qquad(i\in N).                 \tag{1}
\]

Suppose the decorated-head localization has left exactly one blocking row
`h`.  Put

\[
 \lambda_i=\max\{v_i(X_i),\max_j\tau_i(Z_j)\}.   \tag{2}
\]

Every nonhead pays its protected threshold:

\[
 v_i(Z_i)\ge\lambda_i\qquad(i\ne h).             \tag{3}
\]

The head blocks at least one target, so

\[
 \lambda_h>v_h(Z_h)>v_h(X_h).                    \tag{4}

Assume the protected acceptance row of `h` contains a nonroot target `a`:

\[
 a\ne h,r,
 \qquad v_h(Z_a)\ge\lambda_h.                    \tag{5}

Choose an inclusion-minimal packet `P subseteq Z_a` with

\[
 v_h(P)\ge\lambda_h.                             \tag{6}

Downward threshold monotonicity gives, for every observer `i`,

\[
 \tau_i(P)\le\tau_i(Z_a)\le\lambda_i.            \tag{7}

## Root-covered response compression

Assign

\[
 U_h=P,
 \qquad U_i=Z_i\quad(i\notin\{h,a\}),
 \qquad U_a=W:=(Z_a\setminus P)\mathbin{\dot\cup}Z_h. \tag{8}

The three displayed cores `P` and `Z_i` for `i notin {h,a}` are pairwise
disjoint, and `W` is their exact complement in the candidate pool.  Thus
(8) is a complete allocation of the same goods.  The unique missing response
source is the displaced target owner `a`.

Because `a != r`, the earlier root is represented.  If `r=h`, (4)--(6)
strictly improve the root.  If `r!=h`, then `r notin {h,a}` and the root
keeps `Z_r`, which is strictly above `X_r` by (1).  Hence every EFX
allocation in (8) is a strict fixed-priority lexicographic improvement over
`X`, irrespective of the utility of the sacrificed owner `a`.  In
particular, paying `a` is not a prerequisite for closing this branch.

## Exact wall star

Every represented owner pays every selected core.  For the head this follows
from (6)--(7).  For a represented nonhead it follows from (3), (7), and the
definition of `lambda_i`.  The missing owner `a` is automatically EFX-safe
against her own residual `W`.

Consequently, if (8) is not EFX, every failed comparison has exactly one of
the following forms:

1. `a` strongly envies one of the three selected cores; or
2. one of the three represented sources strongly envies `W`.

There are no other walls.  This is precisely the two-sided
three-core/one-residual compression star.  It may be closed by an aligned
recapture, a priority-valid hole pivot, a release-compatible PI component,
or the already-recorded recurrence analysis.  The one-head protected
capture inequality is therefore only a diagnosis of why the direct
two-bundle payment failed; it is not a separate terminal after
priority-valid sacrifice is allowed.

## Exact surviving one-head boundary

The protected head row is nonempty and contains no identity edge.  If it
contains any target other than `r`, the handoff above applies.  Therefore the
only one-head acceptance pattern not covered by (8) is

\[
 h\ne r,
 \qquad N(h)=\{r\}.                              \tag{9}

That is a genuinely **root-facing** star: every protected packet capable of
paying the head lies in the root target, so the elementary compression would
make `r` the missing source or cut the protected root bundle.  Across the
four possible head identities and all nonempty nonidentity acceptance rows,
the exact graph census has 25 nonroot handoff rows and three root-facing
rows, one for each `h != r`.

## Claim boundary

This lemma proves the physical compression, root coverage, lexicographic
endpoint, exhaustive wall localization, and exact one-head root-facing
boundary without an item or value cap.  It does not terminate the resulting
two-sided compression star, eliminate (9), prove the corresponding
two-head Hall handoff, eliminate root-sourced complete-residual-pool capture,
close GG, or prove four-agent/general additive EFX.

