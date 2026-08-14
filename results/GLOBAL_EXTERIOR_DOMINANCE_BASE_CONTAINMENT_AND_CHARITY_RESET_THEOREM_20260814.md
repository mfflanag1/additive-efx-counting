# Global-exterior dominance, base containment, and charity reset theorem

**Date:** 2026-08-14

**Supersession (2026-08-14):** under the full anchored `GG` interface, the
input exterior-dominance face is empty by
`GG_OLD_ROOT_CORE_EXCLUDES_EXTERIOR_DOMINANT_PACKET_THEOREM_20260814.md`.
The theorem below remains a valid conditional reduction.

**Status:** cap-free reduction of every recurrent root-held retired packet to
the exterior-dominant base-contained one-good response normal form; the final
on-good loss band and off-good/base-root response remain

## Input and the exact exterior identity

Let `X` be the positive, bundle-nondegenerate, globally fixed-priority
lexicographically maximal one-charity EFX base.  Let the current first-priority
root target and named nonempty retired packet satisfy

\[
 Z_r=K\mathbin{\dot\cup}H,
 \qquad v_r(Z_r)=x+\delta,
 \qquad x=v_r(X_r),\quad\delta>0.              \tag{1}
\]

Put

\[
 S^+=Z_r\setminus X_r,
 \qquad S^-=X_r\setminus Z_r,
 \qquad E=G\setminus Z_r,
 \qquad O=G\setminus X_r.                     \tag{2}
\]

Then `S^- subseteq E`, and the following are disjoint identities:

\[
 O=S^+\mathbin{\dot\cup}(E-S^-),
 \qquad
 \delta=v_r(S^+)-v_r(S^-).
\]

Consequently

\[
 \delta+v_r(E)=v_r(O).                         \tag{3}
\]

## Complete-current-exterior dominance forces base containment

The global-exterior subpacket-sacrifice theorem proves, at every recurrent
root-held packet state,

\[
 v_r(k)>\delta+v_r(E)\qquad(k\in K).            \tag{4}
\]

By (3), this is exactly

\[
 v_r(k)>v_r(O)\qquad(k\in K).                  \tag{5}
\]

If some `k in K cap S^+`, then `k in O`; positivity and additivity give
`v_r(k)<=v_r(O)`, contradicting (5).  Since `K subseteq Z_r`, every atom of
`K` not in `S^+` lies in `X_r`.  Therefore

\[
 \varnothing\ne K\subseteq X_r.                \tag{6}
\]

Thus no signed missing-base return is needed to obtain base containment.
There is no compatibility-blocker or multi-label-charge alternative in this
step.

## Supplier-free charity reset

Let `f` be the unique charity good in the base.  Test the complete allocation

\[
 A_r=X_r+f,
 \qquad A_i=X_i\quad(i\ne r),                  \tag{7}
\]

with empty charity.  This moves only `f`, whose current supplier is charity;
all owner bundles remain at their base targets.  Hence the operation requires
neither a historical reversal nor a compatibility assumption.  Positivity
gives

\[
 v_r(A_r)=x+v_r(f)>x.                           \tag{8}
\]

If (7) is EFX, it contradicts global lexicographic maximality.  Otherwise
every new wall is against `X_r+f`: the other targets and their owners are
unchanged from the EFX base, while the root only improves.  Extract a globally
minimum safe response `D subsetneq X_r+f` from that unsafe target.

If `K` is not contained in `D`, the named packet intersection is proper or
empty.  Otherwise put

\[
 L=X_r\setminus D.
\]

There are exactly two support forms.

### On-charity-good response

If `f in D`, then properness of `D` forces

\[
 \varnothing\ne L\subseteq X_r\setminus K,
 \qquad D=(X_r\setminus L)+f.                  \tag{9}
\]

Bundle nondegeneracy makes `v_r(D)` unequal to `x`.  If `v_r(D)>x`, the safe
response is a valid root-anchor reselection.  Otherwise

\[
 v_r(D)<x
 \quad\Longleftrightarrow\quad
 v_r(L)>v_r(f).                                \tag{10}
\]

### Off-charity-good response

If `f notin D`, then

\[
 L\subseteq X_r\setminus K,
 \qquad D=X_r\setminus L.                     \tag{11}
\]

For nonempty `L`, positivity gives `v_r(D)<x`.  For `L=empty`, the response is
exactly `D=X_r`, the source-inactive base-root repeat.

## Composed recurrent normal form

Unless a permitted packet reduction or root-anchor reselection has already
occurred, every recurrent root-held retired packet has all of the following:

1. `K` is nonempty and base-contained as in (6);
2. every atom satisfies the exterior-dominance inequality (5);
3. the charity-reset allocation (7) has a safe whole-`K` response of form
   (9) or (11); and
4. the nonroot base envy graph has source set `{c,q}` or `{c,s}`, with exact
   root-threshold debt. The one-source set `{c}` closes by CGM Corollary 7.

The signed missing-base operation remains a valid optional transition, but it
is no longer a premise of the normal form and its failure is no longer a live
charge branch.

## Claim boundary

This theorem proves unconditional base containment and the supplier-free
charity one-good reset.  It does not eliminate the on-good loss band (10), the
off-good/base-root response (11), identify and route the response source
through the retirement supplier or threshold-debt owner, close
`T_{L,times}^*`, GG, four-agent EFX, or general additive EFX.
