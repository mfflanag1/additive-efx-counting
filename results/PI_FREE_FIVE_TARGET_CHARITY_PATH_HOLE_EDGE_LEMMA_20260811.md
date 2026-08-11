# PI-free five-target charity-path hole-edge lemma

**Date:** 2026-08-11

**Status:** cap-free graph-level collapse of rank-four five-target recurrence
to one Hamiltonian charity path; decorated payment remains open

## Five-target matching

Let the four response sources be the owners `N`, and let the five physical
targets be the four owner targets together with charity `c`.  A rank-four
matching `M` selects one target for every source and leaves a unique target
`H` unmatched.  Draw every selected response as a directed edge from its
source owner to its target; charity has no outgoing edge.

### Charity is the hole

If `H=c`, every owner has indegree and outdegree one.  The matching is a
disjoint union of directed owner cycles.  Whenever their exact generalized-
response labels are internally supplied, they are BCFF Pareto-improvable
components.  Thus a PI-free physically closed state cannot have charity as
its matching hole.

### An owner is the hole

Let `H=h in N`.  Owner `h` has indegree zero, each other owner has indegree
one, every owner has outdegree one, and charity has indegree one and
outdegree zero.  Hence the graph is the disjoint union of:

1. one directed path starting at `h` and ending at charity; and
2. zero or more directed owner cycles.

If owner cycles are excluded, the path contains all four owners and is
Hamiltonian:

\[
 h\longrightarrow i_1\longrightarrow i_2
 \longrightarrow i_3\longrightarrow c.           \tag{1}
\]

There is no other cycle-free rank-four form.

## One edge into the hole

Suppose an exact response edge `i -> h` is available while (1) is selected.
Replace `i`'s old matched edge by `i -> h`.  If `i` occupies position `t`
on (1), the prefix from `h` through `i`, followed by the new edge, is a
directed owner cycle of length `t+1`.  The old target of `i` becomes the new
hole.  Thus one pivot—not a repeated five-step pigeonhole argument—exposes
the exact cycle.

If the response/release label on `i -> h` is new, it is permanent response
augmentation.  If it is old and every incoming packet on the prefix cycle
is unallocated at the base or released by another cycle edge, the cycle is
PI.  Otherwise an unreleased incoming packet names its base supplier outside
the cycle and strictly grows the connected physical owner component.  At a
full four-owner cycle, conservation and stable full labels leave no outside
supplier; every incoming packet is internally released.

For a surplus-decorated current response, the graph conclusion is unchanged,
but BCFF common safety cannot be inferred.  Its signed compensation packets
must additionally satisfy the surplus-budgeted component inequalities.  A
failed inequality is precisely the mixed old/new margin separator of the
current-safe full-response endpoint lemma.

## Consequence

The returning-hole part of the repeated-support theorem is no longer a free
matching recurrence.  At a PI-free exact state it has only three outcomes:

1. a new physical response/release label;
2. strict connected-component growth from an outside supplier; or
3. the Hamiltonian charity path plus one directed owner cycle whose only
   unresolved premise is decorated observer payment.

No item, packet, path-length, or value cap is used.

## Verification and boundary

[`pi_free_five_target_charity_path_hole_edge_audit.json`](pi_free_five_target_charity_path_hole_edge_audit.json)
exhausts all 120 rank-four matchings.  Twenty-four leave charity unmatched
and contain owner cycles; 72 owner-hole matchings contain an owner cycle;
the remaining 24 are the six Hamiltonian charity paths for each owner hole.
It also checks all 96 possible pivots into a surviving owner hole and obtains
cycle lengths one through four exactly 24 times each.

This lemma proves graph decomposition and the one-pivot cycle.  It does not
prove observer-safe payment of a surplus-decorated cycle, force internal
release before component saturation, close the repeated-support theorem,
close GG, or prove four-agent/general additive EFX.
