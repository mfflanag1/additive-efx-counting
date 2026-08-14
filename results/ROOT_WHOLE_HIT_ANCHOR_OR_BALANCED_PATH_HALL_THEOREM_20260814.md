# Root whole-hit anchor or balanced path-Hall theorem

**Date:** 2026-08-14

**Status:** verified intermediate theorem, superseded by the global
sacrifice-pool and retirement-supplier subpacket-release theorems, which test
strict payment without preserving every later owner's utility.

## Root-held current response

Let the current holder be the protected first-priority root `r`, with

\[
 Z_r=D\mathbin{\dot\cup}L,
 \qquad v_r(Z_r)=x+\delta,
 \qquad \delta>0,                                \tag{1}
\]

where `x=v_r(X_r)` is the globally maximal base-root value. Let `D` be a
current-safe/current-desired response of nonroot source `t` containing the
whole named retired packet `K`.

## Two direct anchor branches

If

\[
 v_r(D)>x,                                       \tag{2}
\]

retain `D` at the root and release `L` with its signed provenance. The root
stays strictly above base and `D` is safe, so this is a valid root-preserving
current-anchor reselection.

Suppose instead that

\[
 v_r(L)>x.                                       \tag{3}
\]

Give `D` to its current-response source `t`, retain `L` at the root, and
release `Z_t` to charity. The root remains strictly above base and `t`
strictly improves. The target `D` was current-safe before the root's utility
fell. Thus only the root can acquire a new wall against `D`. If it does, a
globally minimum current response `E subseteq D` in the root row satisfies

\[
 v_r(E)>v_r(L)>x,                                \tag{4}
\]

and is a safe current anchor after minimum-response extraction. Hence that
wall gives root-anchor reselection. Every other new response avoids `K`.
Therefore (3) also yields EFX, ledger-free/proper-packet progress, or a valid
root anchor.

## Exact balanced survivor

After (2)--(3) fail, bundle nondegeneracy makes both inequalities strict:

\[
 v_r(D)<x,
 \qquad v_r(L)<x.                                \tag{5}
\]

Using (1), each side must nevertheless pay at least the root surplus:

\[
 \delta<v_r(D)<x,
 \qquad \delta<v_r(L)<x,                         \tag{6}
\]

where strict lower bounds follow from the strict upper bound on the
complement. Thus neither side alone is a base-paying anchor, but neither is
small enough for the ordinary complement-sacrifice branch. This is the exact
balanced root band.

## Surplus-discounted composition with all current-bundle paths

In the balanced band, define the root's strict compensation price

\[
 \pi_r(D)=v_r(D)-\delta.                         \tag{7}
\]

Equation (6) gives `0<pi_r(D)<x-delta`. Route `Z_t` through any of the five
simple current-bundle compensation paths back to the root, assigning the
last old bundle `Z_j` together with `L` to `r`. The exact root margin is

\[
 v_r(L+Z_j)-x=v_r(Z_j)-\pi_r(D).                \tag{8}
\]

Thus a terminal path edge is **strictly paid** exactly when
`v_r(Z_j)>pi_r(D)`. Such a supplier cycle transfers `D` to `t` while leaving
the root strictly above the globally maximal base; the only new mixed target
is `L+Z_j`, which is disjoint from `K`. Equality
`v_r(Z_j)=pi_r(D)` is retained as the typed root-equality boundary rather
than promoted to a strict endpoint.

If no path is strictly paid, the same five Boolean path clauses as in the
four-owner path-Hall theorem hold, but every terminal edge `j->r` is now the
strict test `v_r(Z_j)>pi_r(D)`. Its negation is

\[
 v_r(Z_j)\le\pi_r(D).                            \tag{9}
\]

This surplus-discounted cut is strictly stronger than demanding root
nondecrease, whose sink benchmark would be `v_r(D)`.

Consequently the current root-held whole-hit survivor is not an arbitrary
holder-price wall. It is the conjunction of:

1. the balanced root band (6);
2. the surplus-discounted five-path current-bundle Hall cut; and
3. any separately normalized other-retired-support/release separator.

## Relationship to root atomwise criticality

If the current root support has already been minimized among safe subsets
strictly above `x`, every proper subset has root value at most `x`, so (5) is
automatic. The new content is the lower half of (6) and its exact
composition with every whole-current-bundle compensation route. A remaining
proof must split an old bundle, use a GG-specific anchor exchange, or
contradict the combined inequalities.

## Claim boundary

This theorem closes both root-high sides and isolates the balanced
root/path-Hall conjunction. It does not contradict that conjunction or its
root-equality boundary, handle source-inactive protected-floor debt, clear other retired support, close
`T_{L,times}^*`, or prove four-agent/general EFX.
