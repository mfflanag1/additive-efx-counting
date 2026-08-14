# R3 later-source root-preserving star frontier

**Date:** 2026-08-14

**Status:** cap-free reduction of the two later-source represented stars to a
priority-valid four-edge absorption or full permanent-anchor-margin capture

## Root-critical stars

In the residual form-R3 represented star, let the common source be
`x in {q,s}`.  Its two response targets are the first-priority root `r` and
the remaining represented owner `y`.  Write

\[
 B_r=R_r\mathbin{\dot\cup}C_r,
 \qquad B_y=R_y\mathbin{\dot\cup}C_y,             \tag{1}
\]

and let `A subseteq C_r` be the permanent root anchor with

\[
                         v_r(A)>v_r(X_r).          \tag{2}
\]

Choose simultaneous universally safe current-desired star cores
`E_r subseteq B_r` and `E_y subseteq B_y` at a singleton placement away from
`x`.

## Root-preserving absorption

At the nonroot target `y`, enlarge `E_y` by its entire incoming matching
packet `C_y`.  At the root target, move only `E_r`: do **not** complete the
unused part of `C_r`.  Give charity to `y` and retain every unselected good.

The partial root packet leaves its old supplier-to-root pair active, but
completion at `y` deletes the other old R3 cycle edge.  Direct signed-edge
enumeration gives at most three owner-transfer pairs in every case—whether
`E_r` uses none, a proper part, or all of `C_r`, and whether either response
uses retained support.  Charity is therefore the fourth edge.

The root retains at least

\[
                         A\setminus E_r.           \tag{3}

If

\[
                 v_r(A\setminus E_r)>v_r(X_r),    \tag{4}

the first-priority root remains strict.  The double-absorption continuation
is then priority-valid: repeated responses by `x` into the two depleted
targets reuse the same three owner pairs and strictly shrink their residual
union.  A new response coordinate is saturation progress; a response
involving `d` recruits the full-owner component.

## Exact capture alternative

If (4) fails, additivity gives

\[
\begin{aligned}
 v_r(E_r\cap A)
 &=v_r(A)-v_r(A\setminus E_r)\\
 &\ge v_r(A)-v_r(X_r)>0.                          \tag{5}
\end{aligned}

Thus failure of the priority-valid absorption is not an untyped root loss:
the later-source response captures the **entire strict permanent-anchor
margin**.  Equation (5) is cap-free and holds for an arbitrary physical
intersection packet.

The same dichotomy applies cumulatively if several same-source residual
cores are absorbed: either the retained anchor complement stays strict at
every step, or the union of moved anchor pieces reaches the full margin in
(5).

## Consequence

Together with the root-source three-edge absorption, the represented-star
frontier now has only one scalar terminal:

> a current-safe later-source response into the root contains a physical
> subpacket of the permanent anchor whose root value covers the entire
> strict anchor margin.

The remaining theorem must convert that captured anchor packet into a
release-compatible PI/full-owner exchange, or replace the anchor while
preserving first-priority strictness.  Merely leaving the captured packet in
the later source's bundle is not sufficient.

## Claim boundary

Proved: the exact at-most-four-edge root-preserving support identity and the
full-margin capture inequality (5).

Not proved: conversion of the captured anchor packet, unconditional closure
of the later-source stars, the complete fixed-U four-edge theorem, or general
additive EFX.
