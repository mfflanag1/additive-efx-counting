# Root whole-hit global sacrifice-pool or underpayment theorem

**Date:** 2026-08-14

**Status:** verified intermediate theorem, subsumed by
`ROOT_SAFE_WHOLE_HIT_COMPLETE_POOL_REDUCTION_THEOREM_20260814.md` and the
smaller-price retirement-supplier packet-release theorem.

## Root price and compatible pool

Use the balanced root-held safe-response state with named nonroot
source/colliding recipient `t`

\[
 Z_r=D\mathbin{\dot\cup}L,
 \qquad v_r(Z_r)=x+\delta,
 \qquad K\subseteq D,                            \tag{1}
\]

where `D` is safe and assigned only through the actual typed handoff to `t`.
The exact root price for transferring `D` while retaining `L` is

\[
 \pi=v_r(D)-\delta>0.                            \tag{2}
\]

Let `R` be any supplier-closed compatible packet outside `Z_r`, disjoint
from `K` and any support that the chosen release mode must retain. Every
piece of `R` carries its actual current supplier. Other retired support is
canonically cancelled before execution.

## Enlarged-root sacrifice operation

Give `D` to source `t`, give `L+R` to the root, let every nonroot donor keep
the complement of its contribution to `R`, and put the unused part of the
old source bundle `Z_t` into charity so that `t` receives exactly the safe
target `D`. Adjust old charity by removing its contribution to `R`. This is a
physical root-sourced/supplier-star sacrifice allocation.

The exact root margin over the globally maximal base is

\[
 v_r(L+R)-x=v_r(R)-\pi.                          \tag{3}
\]

Therefore

\[
 v_r(R)>\pi                                      \tag{4}
\]

makes the root strict. The protected/collision assignment to `t` is the one
supplied by the exact transition. Every nonroot owner is later than the root
and may be sacrificed; no current improvement of `t` is required for the
strict-root lexicographic endpoint.

## Every retired-packet wall routes

If the sacrifice allocation is EFX, (4) gives a lexicographic contradiction.
Otherwise extract a globally minimum current response at the actual
allocation.

The only allocated target containing `K` is `D`. Owners whose assigned value
did not decrease remain protected against `D` by its current safety. A new
wall against `D` can therefore come only from:

1. the root, whose new bundle remains strictly above `x`; or
2. a sacrificed nonroot donor.

In case 1, a minimum response `E subseteq D` desired by the root satisfies

\[
 v_r(E)>v_r(L+R)>x,                              \tag{5}
\]

and becomes a valid safe root anchor. In case 2, an EFX wall supplies a
proper response `E subsetneq D`; if it contains the whole `K`, the holder of
`K` is now the nonroot source `t`, so the nonroot nested-envelope theorem
terminates the recurrence. A proper/empty intersection immediately reduces
`K` or its hitting multiplicity. Every wall against the enlarged root,
shrunk donor, unchanged target, or charity is disjoint from `K`.

Thus every strictly root-paying compatible pool yields EFX, root-anchor
reselection, proper/zero packet hitting, or the already proved finite
nonroot envelope descent. No safety premise on `R` is required.

## Exact survivor

Let `mathfrak R_r` be the complete finite family of maximal mutually
compatible supplier-closed `K`-free exterior modes. Positivity makes each
mode's full pool its root-value maximum. After the strict branch is
exhausted, the root-held current whole-hit survivor satisfies

\[
 v_r(R)\le\pi
 \qquad(R\in\mathfrak R_r).                     \tag{6}
\]

Strict inequality is aggregate underpayment. Equality is the typed root-
equality sacrifice boundary: the root falls exactly to `x`, so later donor
losses cannot be ignored without a separate priority/base-floor audit.

Equation (6) subsumes the surplus-discounted whole-bundle path cut. If even
the union of every simultaneously compatible exterior packet fails (4), no
whole-bundle permutation can pay the root strictly. The remaining operation
must use equality priority, change/release the anchor without transferring
`D`, or contradict (6) using the originating GG transition.

## Claim boundary

This theorem eliminates the entire strict complete-pool branch and handles
all resulting whole-`K` donor walls. It does not eliminate aggregate
underpayment/equality (6), source-inactive protected-floor debt, incompatible
release modes, other retired support, close `T_{L,times}^*`, or prove
four-agent/general EFX.
