# Whole-core return two-hole descent lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of every priority-valid core-side hole
recurrence; residual-side overlap and source-inactive rank descent remain
open

## Setting

Use a rank-three root-anchored compression with missing owner `d`, residual
`W`, and common-safe desired cores `A_k` held by the three represented
sources.  Suppose `d` strongly envies the core `A_j`:

\[
 v_d(W)<\tau_d(A_j),                                 \tag{1}
\]

and is a base-response source for it.  Common-safe target response rigidity
then says that the response is the whole core:

\[
 v_d(A_j)>v_d(X_d),                                  \tag{2}
\]

with no proper desired response subset of `A_j`.

Assume first that `j` is not the anchored root `r`.

## Rank descent

Stop requiring `j` to remain represented.  Keep the two other common-safe
desired cores fixed and release the complete pool

\[
 P=A_j\mathbin{\dot\cup}W                            \tag{3}
\]

between the two holes `d,j`.  Let `d` choose a maximin two-way partition of
`P` and let `j` choose her preferred cell, exactly as in the two-hole
cut-and-choose lemma.

The two holes are mutually EFX.  Moreover (1) gives the strict inherited
potential

\[
 v_d(P_d)>v_d(W).                                    \tag{4}

\]

The anchored root remains represented by a common-safe desired core and is
strictly above base.  Hence an EFX endpoint is a valid strict
lexicographic flower improvement even if either released owner falls below
base.

If the endpoint is not EFX, every remaining wall lies in the two-core,
two-hole response boundary.  The exact 2-by-2 normal form then gives one of:

1. a full response SDR and release-compatible PI component;
2. a cross-block two-owner PI cycle; or
3. an empty-target/source-inactive wall followed by the finite repair
   chain.

Thus a base-active nonroot core wall never needs a hole pivot.  It closes or
strictly descends from three represented cores to two while preserving the
old hole's strict gain.

## Root-facing exception

If `j=r`, releasing the root core by unconstrained cut-and-choose may violate
priority.  This is precisely the root-facing branch.  Use the
root-preserving selector instead when its root-order hypothesis holds; its
critical branch terminates through the root-critical alternating frontier.
Otherwise retain the existing top-exchange/captured-bottom handoff.  No new
root exception is created by the descent theorem.

## Recurrence consequence

Together with response rigidity, this removes core-side dynamic overlap
from the priority-valid recurrence analysis.  A repeated nonroot hole that
tries to traverse a common-safe core is diverted to the two-hole boundary
before it can return.  Proper-subset overlap can survive only through an
evolving residual target or an unsafe-core augmentation.

The remaining rank-two empty-target wall is source-inactive.  Successful
repair strictly raises the active hole's value; exhaustion would release a
second nonroot core and create a one-core/three-hole state.  Constructing a
priority-valid selector for that rank-one boundary is now the exact
dimension-descent gate.

## Verification and claim boundary

[`whole_core_return_two_hole_descent_audit.json`](whole_core_return_two_hole_descent_audit.json)
checks response rigidity, the support partition, strict inherited gain,
priority preservation, and the exhaustive 2-by-2 continuation under Z3
5.0.0 and 4.15.3.

This lemma eliminates priority-valid core-side hole recurrence.  It does not
construct the one-core/three-hole selector, terminate residual-side unsafe
overlap, close root-facing captured-bottom recurrence, close `GG`, or prove
four-agent/general additive EFX.
