# Base-charity collision supplier-recruitment lemma

**Date:** 2026-08-14

**Status:** cap-free fixed-`U` provenance reduction; internal-supplier
collision remains open

## Setting

Use the saturated allocated-`E` physical chart.  The old/base charity packet
is `G_r`, but the current support allocation is

\[
Y=(A+H,Q,W,E;P),
\qquad G_r\subseteq W.
\]

Thus every physical good of `G_r` is currently supplied by sacrificed owner
`d`; current charity is the distinct singleton packet `P`.

Let a directed owner cycle of globally minimal desired cores be obtained from
the self-core/charity-collision lemma.  Its noncharity supports are disjoint,
and suppose two selected cores overlap in a nonempty packet
`T subseteq G_r`.

## Theorem

Exactly one of the following occurs.

1. The selected cycle cores are pairwise disjoint and form a physical
   generalized PI.
2. Their overlap contains a nonempty current-`d`-supplied packet `T`.  If
   `d` is outside the cycle owner set, every physical activation using `T`
   strictly grows the represented supplier/owner component by adjoining
   `d`.
3. The collision is already supplier-internal: `d` belongs to the cycle.

At a saturated fixed-`U` record, alternative 2 is a named strict component/
supplier-progress exit.  Consequently every non-PI charity-collision
survivor is a two-, three-, or four-owner cycle containing `d`, with all
overlap confined to pivotal current-`d` subpackets of `G_r`.

## Proof

Alternative 1 is the disjoint-cycle conclusion of the preceding lemma.  In
the remaining case, every overlap is in base charity and hence in `G_r`.
Choose a nonempty shared physical subpacket `T`.

Support provenance in the fixed-`U` gate assigns each moved packet to its
current physical supplier.  Since `T subseteq G_r subseteq Y_d`, any response,
PI rotation, or charity-exchange operation that assigns `T` away from its
current holder uses an edge with source `d`.  If `d` was not represented in
the cycle component, adjoining that edge increases its owner/supplier union
by one.  This is precisely the strict component-growth coordinate recorded
by saturation.  If `d` was already represented, no new owner is added and
the collision is internal.  These cases are exhaustive and use no packet-
cardinality bound.

## Relation to the physical search

The first self-PI-free endpoint-6 model contained 1,000 physical generalized
PI families.  Of these, 630 were completely base-charity-free and therefore
already lie in alternative 1; 370 used a `G_r` subgood.  The dominant owner
set was `{d,q,r}` (918 families), consistent with supplier `d` already being
internalized.  The sparse continuation found charity-free `{q,r}` cycles,
also alternative 1.

This explains why the computational frontier moves from self cores directly
to `{q,r}` or `{d,q,r}`: a collision outside `d` is not a terminal at a
saturated record—it recruits `d`.

## Exact audit and boundary

`audit_charity_collision_supplier_recruitment.py` enumerates every directed
cycle on two through four owners and verifies that using a `d`-supplied
collision packet increases the represented owner count exactly when `d` is
outside the cycle.

Proved: the cap-free supplier-recruitment classification and elimination of
outside-`d` collisions at a saturated record.

Not proved: closure of a pivotal collision when `d` is already on the cycle;
the owner-payment and observer-surplus inequalities for that internal case;
the universal saturated rank-three fixed-`U` four-edge theorem; or general
additive EFX.
