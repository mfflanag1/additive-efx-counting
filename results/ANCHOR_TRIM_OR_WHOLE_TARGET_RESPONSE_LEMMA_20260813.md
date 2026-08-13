# Anchor-trim or proper-target descent lemma

**Date:** 2026-08-13

**Status:** superseded diagnostic. Its proper-response argument is valid,
but its response-side safety branch used post-handoff safety of `E`, which is
not supplied by the sacrifice-handoff premises. Use the minimal-response
peel-or-reselect theorem instead.

## Input

Use the frozen recurrence contract. Put

\[
 B=K\mathbin{\dot\cup}E,
 \qquad x=v_r(X_r),                               \tag{1}
\]

where

\[
 v_r(K)>x,
 \qquad v_r(E)>x.                                \tag{2}
\]

Assume `B` is unsafe. Choose `D subseteq B` from an agent/subset pair of
globally minimum cardinality among all subsets of `B` desired over that
agent's current bundle. Let its source be `i`. Then `D` is safe relative to
the current allocation. In the live mixed case,

\[
 H=D\cap K\ne\varnothing,
 \qquad J=D\cap E\ne\varnothing.                \tag{3}
\]

Write

\[
 K'=K\setminus H,
 \qquad E'=E\setminus J,
 \qquad C=B\setminus D=K'\mathbin{\dot\cup}E'.  \tag{4}
\]

## Properness forced by the wall

The whole-target response is impossible. Since `B` is unsafe, some observer
`a` satisfies

\[
 v_a(U_a)<\tau_a(B).
\]

For a least-`a` good `g` of `B`, the proper deletion `B-g` is desired by
`a`. Global minimum cardinality therefore gives

\[
 |D|\le |B-g|<|B|,
 \qquad D\subsetneq B.                            \tag{5}
\]

In particular `C` is nonempty.

## Exhaustive selector

Exactly one of the following ordered branches applies.

### 1. Old-anchor trim

If

\[
 v_r(K')>x,                                      \tag{6}
\]

then `K'` is still an old base-common-safe desired root core. It is disjoint
from `D`; replacing `K` by `K'` is a valid anchor reselection. Since `H` is
nonempty, `K'` is a strict support trim. If `D` is retained, the universal
overlap reset either preserves `K'`, trims it further, or records capture of
the entire remaining root margin.

### 2. Response-side root core

If (6) fails but

\[
 v_r(E')>x,                                      \tag{7}
\]

then `E'` is a root-desired core disjoint from `D`. Deletion preserves the
current-safety inequalities of `E`. Hence `E'` is a valid current-root core
for the response-compression state, but this alone is not outcome 4 of the
frozen contract. Any base-safety debt remains explicit in the signed observer
budget; `E'` is not silently promoted to an old anchor. Composition must
either discharge that debt or use `E'` only as a temporary response core.

### 3. Paid complementary split

If neither (6) nor (7) holds but

\[
 v_r(C)>x,                                       \tag{8}
\]

assign `D` to its source and `C` to the root. Both are strictly above their
source/base floors, are disjoint, and use exactly `B`. The source's released
old bundle joins the residual pool. An EFX endpoint is a strict
lexicographic improvement. Every failure is a labeled response against a
changed target or from a changed owner. This is an exact localization, not
yet a termination proof for those responses.

### 4. Root capture and support descent

If

\[
 v_r(C)\le x,                                    \tag{9}
\]

then additivity and (2) give

\[
 v_r(D)=v_r(K)+v_r(E)-v_r(C)>x.                  \tag{10}
\]

Thus the same safe target `D` is root-desired over the base. By (5),
replacing `B` by `D` strictly shrinks the physical root target. Pass `C` to
the residual owner or charity with its full signed provenance; label every
resulting wall before another reset.

Force the root self-edge on `D` in the current-safe matching and add `C` to
an excluded-root-support set. To promote this construction to outcome 3, the
composition theorem must prove that every later root-oriented reset first
deletes the excluded support and either preserves a root-desired reduced
target, strictly enlarges the exclusion, or records capture of the entire
remaining root margin. Without that reset lemma, `|D|<|B|` is only a local
descent and an exact later restoration of `B` has not been excluded.

## Consequence

Every mixed response intersecting both `K` and `E` yields a valid old-anchor
trim, a current-safe response-side trim, a paid root/source split, or a
proper root-target replacement. The apparent whole-target two-packet
recurrence was an artifact of forgetting that `D` is extracted from an
actual unsafe target. The latter three branches become closing outcomes only
after their signed debt and reset interfaces are discharged.

## Claim boundary

This lemma proves the exhaustive scalar/support reduction, hereditary safety
of both trims, the paid split, root capture, and properness of every
wall-derived response. It does not by itself prove global retained-support
descent across resets, terminate walls created by the split, eliminate the
root-facing source-inactive loss band or captured-margin handoff, close GG,
or prove four-agent/general additive EFX.
