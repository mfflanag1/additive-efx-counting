# Nonroot singleton-hit safe-envelope descent lemma

**Date:** 2026-08-14

**Status:** cap-free closure of the nonroot-held hitting branch used by the
three-placement relay; no root-holder supplier-star claim is imported

## Input

Let `Z` be a signed response state whose first-priority root is strictly
above the globally maximal base coordinate.  Let a nonroot owner `h` hold a
positive singleton `p`, and suppose an actual response core

\[
 \{p\}\subseteq D\subseteq Z_h                   \tag{1}
\]

is desired by its named source `t` and common-safe at the actual floors:

\[
 v_t(D)>v_t(Z_t),
 \qquad
 \tau_i(D)\le v_i(Z_i)\qquad(i\in N).           \tag{2}
\]

The response is nonself, so `t != h`.

## Root-source branch

If `t` is the root, assigning `D` to the root strictly raises its actual
utility and preserves the immutable strict-base certificate.  The old holder
keeps `Z_h-D`; the root's displaced bundle is recorded as charity/released
support.  This is the strict root response-core/anchor-reselection outcome
excluded by saturation item 9 in the active theorem domain.  The present
lemma does not continue by treating `p` as a root-held retired packet.  No
root-holder supplier-star inference is used.

## Nonroot-source safe sacrifice

Suppose `t` is nonroot.  Give `D` to `t`, leave

\[
 L=Z_h-D
\]

with `h`, move `Z_t` to charity, and leave the root and fourth owner
unchanged.  The root remains strict.  Source `t` strictly improves by (2).

Every unchanged observer is safe against `D` by (2), and `t` owns `D`.
Therefore the only owner who can acquire a new wall **against `D`** is the
sacrificed old holder `h`.  If no such wall exists, every subsequent failed
response is against another target and is disjoint from `p`.  If the wall
exists, a one-good deletion of `D` is desired by `h`; globally minimum
response extraction produces a common-safe desired core

\[
 E\subsetneq D.                                   \tag{3}
\]

If `p notin E`, the singleton hit disappears.  If `p in E`, repeat the same
operation with envelope `E`.  The current holder and source are again
distinct nonroot owners, while the root remains unchanged and strict.

## Termination

Every repeated hit gives a strict chain

\[
 D=D_0\supsetneq D_1\supsetneq\cdots\supseteq\{p\}.
\]

It has length at most `|D|-1`.  At the singleton envelope `{p}`, deleting
its only good leaves the empty bundle, so positivity cannot create a
strong-envy wall.  Hence the nonroot-held, nonroot-sourced hitting branch
terminates with a response disjoint from `p`; a root-sourced hit is the
separately named strict anchor-reselection exit in the saturated target.

## Boundary

This theorem closes only a response core already containing a singleton at
a nonroot holder.  It does not treat an initial root holder, prove that every
failed response hits the singleton, close the subsequent disjoint Hall
branch, prove the fixed-`U` theorem, or prove four-agent/general additive
EFX.
