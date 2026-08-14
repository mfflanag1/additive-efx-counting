# Permanent-anchor same-source root-response replacement lemma

**Date:** 2026-08-14

**Status:** cap-free elimination of exact same-source residual recurrence;
different-source recurrence and root capture remain open

## Bilateral probe and residual response

Use an admissible permanent-anchor bilateral probe

\[
\begin{aligned}
 C_r&=(B_r\setminus H)\mathbin{\dot\cup}D
                         \mathbin{\dot\cup}\{p\},\\
 C_i&=(B_i\setminus D)\mathbin{\dot\cup}H,       \tag{1}
\end{aligned}
\]

where `i` is nonroot,

\[
 v_i(H)>v_i(D),\qquad
 v_r(H)-v_r(D)<\delta_r+v_r(p),                  \tag{2}
\]

and (1) uses at most four physical supplier pairs.  Suppose a non-EFX probe
has a new root-target response `F` with the **same source** `i`, and suppose
the incoming-cell and singleton branches have already been removed:

\[
 \varnothing\ne F\subseteq B_r\setminus H,
 \qquad v_i(F)>v_i(C_i).                          \tag{3}
\]

Thus `F` lies entirely in residual support from the original physical root
bundle and is disjoint from the old moved packet.

## Replace rather than accumulate

Return `H` to the root and give `F` to `i`, retaining the compensator `D` and
charity placement.  Relative to the fixed partial allocation `B`, this is
exactly the bilateral candidate `(F,D)`:

\[
 C'_r=(B_r\setminus F)\mathbin{\dot\cup}D
                         \mathbin{\dot\cup}\{p\},
 \qquad
 C'_i=(B_i\setminus D)\mathbin{\dot\cup}F.       \tag{4}
\]

Equations (2)--(3) give both

\[
                         v_i(F)>v_i(D)             \tag{5}
\]

and strict same-source progress

\[
                         v_i(C'_i)>v_i(C_i).       \tag{6}
\]

Indeed `C_i` contains `H`, so (3) gives `v_i(F)>v_i(H)>v_i(D)`, and replacing
`H` by `F` strictly raises the source bundle.

The root remains strictly above base exactly when

\[
                         v_r(F)-v_r(D)<\delta_r+v_r(p).           \tag{7}
\]

## Exact edge alternative

Write `F_r=F\cap Y_r` and `F_q=F\cap A`.  By the exact bilateral edge
criterion, `(F,D)` exceeds four pairs only in the signature

\[
 i\ne q,quad D\ne\varnothing,quad F_r\ne\varnothing,
 quad\varnothing\ne F_q\subsetneq A.             \tag{8}
\]

Outside (8), (7) gives a priority-valid at-most-four-edge probe with strict
same-source progress.  If (7) fails, the exact residual-response capture is

\[
                         v_r(F)-v_r(D)\ge\delta_r+v_r(p).         \tag{9}
\]

In signature (8), put

\[
                         G=F\mathbin{\dot\cup}(A\setminus F_q).  \tag{10}

The packet `G` exhausts the anchor, so `(G,D)` is edge-feasible.  Positivity
preserves (5)--(6).  It gives a priority-valid progress probe unless

\[
                         v_r(G)-v_r(D)\ge\delta_r+v_r(p).         \tag{11}

Thus topology is never a terminal: its sole overflow is converted by anchor
completion into a four-edge probe or the typed capture (11).

## Consequence

At a saturated permanent-anchor probe, a root response confined to untouched
original-root support cannot recur with the same source unless (9) or (11)
holds.  Otherwise the explicit replacement probe has a strictly larger bundle
for the identical source.  If it is EFX, it is the desired endpoint; if it is
non-EFX, its first appearance or its higher same-source utility is exact
history/record progress.

After combining with incoming-cell diversion, the unresolved root-target
response types are therefore:

1. a different response source;
2. simultaneous incoming-cell/root-residual margin capture; or
3. a singleton-hit changed-state continuation.

## Claim boundary

Proved: source admissibility and strict progress, exact root payment, the
if-and-only-if overflow signature, and anchor-completion repair.  Not proved:
contradiction of (9) or (11), closure of a different-source response, semantic
admission of every first-history transition in the global GG policy, the
singleton-hit changed-state continuation, the fixed-`U` theorem, or general
EFX.
