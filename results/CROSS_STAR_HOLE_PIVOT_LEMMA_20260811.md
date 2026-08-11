# Cross-star hole-pivot lemma

**Date:** 2026-08-11

**Status:** cap-free analytic component operation; source-inactive,
root-facing, and cyclic hole-pivot termination remain open

## Compressed state

Let `X` be the base partial EFX allocation.  In a four-owner response
compression, let `d` be the unique missing source.  Every other owner
`k != d` holds a pairwise-disjoint common-safe desired core `A_k`, while
`d` holds the residual `W`.  The cores and `W` partition all currently
assigned goods.

Suppose two distinct nonmissing owners `i,j` form a cross-star pair:

1. `i` responds to the residual with a common-safe desired core
   \(D_i\subseteq W\); and
2. `d` is a **base-response source** for `j`'s core, with a common-safe
   desired core
   \(C_d\subseteq A_j\).

The indices are genuinely crossed: `i != j`.  The aligned case `i=j` is
already handled by the monotone recapture lemma.

## Hole pivot

Define

\[
 Z'_i=D_i,
 \qquad Z'_d=C_d,
 \qquad Z'_k=A_k\quad(k\notin\{d,i,j\}),                 \tag{1}
\]

and give the new residual

\[
 W'=(W\setminus D_i)\mathbin{\dot\cup}A_i
       \mathbin{\dot\cup}(A_j\setminus C_d)             \tag{2}
\]

to owner `j`.

Then (1)--(2) form a complete allocation of exactly the same goods.  Every
owner other than `j` receives a common-safe bundle she strictly prefers to
her base bundle.  Thus the unmatched source has moved from `d` to `j`; no
packet-size bound is used.

## Exact wall localization

If the pivoted allocation is not EFX, every failed comparison has one of
two forms:

1. the new missing owner `j` strongly envies one of the three selected
   cores; or
2. one of the three represented sources strongly envies `W'`.

Indeed, each represented source is strictly above her base utility and
every selected core is common-safe at the base, so represented-source to
core comparisons cannot fail.  The missing owner is automatically safe
against her own residual bundle.  These exhaust all ordered pairs.

Consequently a disjoint cross-star whose core wall is also a base response
is not terminal.  It is an alternating matching pivot which changes the
missing source and recreates the same three-core/one-residual normal form.

This base-response qualification is essential.  Strong envy by the
sacrificed owner is measured from `W`, while a response source must prefer a
subset to her original bundle `X_d`.  The former does not imply the latter.

## Priority consequence for the flower

In the root-anchored flower compression, `r` is always represented by the
common-safe desired core `T_q+f`; hence the current missing source is never
`r`.  If the pivot also has `j != r`, an EFX pivoted allocation closes the
flower leaf:

- when `j` is external, both `r` and `q` receive desired cores, giving the
  requested flexible improvement;
- when `j=q`, every owner preceding the possibly losing `q`, including
  `r`, receives a desired core, so the allocation is a strict improvement
  in the fixed priority in which `r` precedes `q`.

The only priority-invalid pivot is therefore a pivot whose new hole is the
earlier mutual owner `r`.

## Alternating-path interpretation

Before the pivot, the response edges are

\[
 i\longrightarrow W_d,
 \qquad d\longrightarrow A_j.
\]

They are the two edges of an alternating path through the unmatched target
`d`; applying the path frees target `j`.  Formula (2) is the exact
owner-union residual produced by that augmentation.  This is the operation
missing from aligned recapture: a disjoint response/core wall should move
the matching hole, not be treated as a scalar contradiction.

## New terminal boundary

Close the finite family of compressed states under both aligned recapture
and priority-valid base-response hole pivots.  Aligned recaptures terminate
by the strict missing-owner residual potential.  At any source-active
two-sided cross-star, the lemma either closes by EFX or moves the hole.

If `d` strongly envies `A_j` but is not a base-response source for it, then
common safety and nondegeneracy force the exact strict loss band

\[
 v_d(W)<\tau_d(A_j)<v_d(A_j)<v_d(X_d).                  \tag{3}
\]

Indeed, strong envy gives the first inequality, positivity gives the
second, and `v_d(A_j)>v_d(X_d)` would make the whole common-safe core a
desired response for `d`.  Equality with the distinct base bundle is
excluded in the nondegenerate normal form.

Hence a surviving closed class must contain one of:

1. a **source-inactive star**, carrying the strict loss band (3);
2. a **root-facing star**, in which every pivotable envied core is the
   anchored `r` core; or
3. a **hole-pivot recurrence**, in which the missing source revisits an
   owner through different desired cores/residuals.

This is strictly narrower than the former arbitrary disjoint cross-star.
The remaining termination argument must show that a recurrence supplies a
release-compatible generalized PI cycle or that one of its strict packet
orders cannot repeat; alternatively a root flip must eliminate the
root-facing star.

## Verification and claim boundary

[`cross_star_hole_pivot_audit.json`](cross_star_hole_pivot_audit.json)
checks the set partition, strict improvement of every represented source,
the exhaustive two-sided wall localization, the source-inactive loss band,
and the flower priority split.
The scalar implications replay under Z3 5.0.0 and 4.15.3.

The lemma proves a new cap-free adaptive component operation.  It does not
eliminate source-inactive or root-facing stars or hole-pivot recurrences,
prove that every response matching produced after a pivot is
release-compatible, close the `GG` flower class, or prove four-agent
additive EFX.
