# Root-anchored one-head two-hole selector lemma

**Date:** 2026-08-13

**Status:** cap-free conversion of the sole root-facing one-head acceptance
row into a two-hole response boundary or an exact anchor/root-critical good

## Root-facing one-head state

Let `Z` be a paid residual-completed mixed-cycle candidate with sole blocker
`h != r`.  Suppose its protected acceptance row is exactly

\[
 N(h)=\{r\}.                                      \tag{1}

The root is a nonhead, so with

\[
 A=Z_r,
 \qquad W=Z_h,
\]

we have

\[
 v_r(A)>v_r(X_r),
 \qquad v_r(A)\ge\tau_r(W).                       \tag{2}

Let `K_r subseteq A` be the permanent root anchor.  Keep the other two
nonhead bundles fixed.  Only the pool

\[
 P=A\mathbin{\dot\cup}W                           \tag{3}

is repartitioned between `r` and `h`.

## Anchor-preserving root-EFX selector

Among all partitions

\[
 P=H\mathbin{\dot\cup}L                           \tag{4}

satisfying

\[
 K_r\subseteq H,
 \qquad v_r(H)\ge v_r(A),
 \qquad v_r(H)\ge\tau_r(L),                       \tag{5}

choose one maximizing `v_h(L)`, with deterministic tie-breaking.  The
family is nonempty: `(H,L)=(A,W)` satisfies (5) by (2).  Thus the permanent
anchor remains with the root, the root stays strictly above the globally
maximal base, and the root is EFX-safe against the head cell.

## Exact least-good dichotomy

If

\[
 v_h(L)\ge\tau_h(H),                              \tag{6}

then the two holes are mutually EFX.  Together with the two fixed protected
cores, every remaining wall is either a hole against a fixed core or a
represented source against `H` or `L`.  This is exactly the two-core/two-
residual response-Hall normal form, and every EFX endpoint is a strict
lexicographic improvement because the root satisfies (2) and (5).

Otherwise, let `g` be a least-`h` good of `H`.  Strong envy gives

\[
 v_h(L)<v_h(H\setminus\{g\}).                     \tag{7}

If every least-`h` good of `H` lies in `K_r`, then (7) is an exact
**anchor-critical** certificate: every elementary maximin repair would cut
the permanent anchor.

If some least-`h` good `g` lies outside `K_r`, move it from `H` to `L`.
Both new cells are strictly better than the old head cell in row `h`, so the
maximal choice of `L` implies that at least one root constraint fails:

\[
 v_r(H\setminus\{g\})<v_r(A),                    \tag{8}

or

\[
 v_r(H\setminus\{g\})
 <\tau_r(L\mathbin{\dot\cup}\{g\}).              \tag{9}

Thus every nonanchor transferable least good is root-floor-critical or
root-EFX-critical.  No anonymous root-facing payment failure remains.

## Consequence

The only one-head row excluded by the nonroot compression-star handoff,
`N(h)={r}`, has exactly three outcomes:

1. an anchor-preserving mutually EFX two-hole partition entering the
   existing `2 x 2` response-Hall boundary;
2. an anchor-critical least-good response/anchor hitting set; or
3. a nonanchor least good satisfying the root-critical polarity (8) or
   (9).

The selector is cap-free and does not require `v_r(A)>v_r(W)`; the weaker
candidate-EFX inequality in (2) is sufficient for nonemptiness.  This is
important because total-value dominance of the root cell is not implied by
the one-head premises.

## Claim boundary

This lemma proves selector nonemptiness, permanent-anchor retention, root
priority, mutual-hole EFX or exact least-good criticality, and wall
localization.  It does not reverse (8)--(9), eliminate the anchor-critical
branch, terminate the resulting two-hole/response recurrence, eliminate
root-sourced complete-residual-pool capture, close GG, or prove four-agent/
general additive EFX.

