# Anchored q-donor or source-collision reduction

**Date:** 2026-08-11

**Status:** cap-free role classification of the stable anchored mixed-margin
terminal; physical two-core q rerouting remains open

## Setting

Use the permanent anchored Hamiltonian owner path with edge

\[
 r\longrightarrow q.
\]

An old decorated response from owner `a` into the owner hole `t` closes a
prefix cycle.  The anchored-terminal classification leaves exactly twelve
stable pivots: the prefix cycle contains both `r` and `q`, the hole is in
`{r,c,s}`, and `a` is not `r`.

The final third-owner fork needs a protected donor distinct from the root,
the hole/captured target, and the closing response source.  The GG chain has
a distinguished protected donor candidate `q`, together with the known
split-support desired core

\[
 D(U)=(T_r\setminus U)+f.
\]

The permanent root response core is

\[
 A_r=T_q+f.
\]

Because the base bundles `T_r` and `T_q` are disjoint and `f` is the unique
charity good,

\[
 D(U)\cap A_r=\{f\}.                              \tag{1}
\]

Thus role eligibility is not yet physical donor availability: the canonical
protected q-core can never be retained disjointly beside the permanent root
anchor.

## Exact dichotomy

The twelve stable pivots divide evenly.

### 1. q is not the closing source

There are six pivots with `a != q`.  In every one,

\[
 q\notin\{r,t,a\}.
\]

Thus `q` is the unique named protected donor candidate outside the
root/hole/source roles.  Their cycle lengths are two cases of length three
and four cases of length four.  If a floater-free desired q-subcore is
available, the third-owner root-replacement selector applies to it with
donor `b=q`.  Otherwise (1) forces an explicit floater substitution or root-
anchor release before the protected `D(U)` donor theorem can be used.  After
that support operation, fork success pays the component; strict q-donor
blockade enters captured-q-margin handoff; aggregate root concentration
enters the existing bottom-absorption rotation.

This branch therefore has no anonymous donor choice.  Floater-compatible
q-core availability is now supplied by the canonical `B_q` substitution:
`(T_r-U)+B_q` is desired by q and disjoint from the anchor; minimal response
extraction gives a nonroot rank-two edge or a root-source anchor return.  See
[`RETAINED_Q_BQ_FLOATER_SUBSTITUTION_HANDOFF_LEMMA_20260811.md`](RETAINED_Q_BQ_FLOATER_SUBSTITUTION_HANDOFF_LEMMA_20260811.md).

### 2. q is the closing source

There are six pivots with `a=q`: two cycles of each length two, three, and
four.  Here `q` is already the owner receiving the recurrent decorated core
from the hole, so it cannot simultaneously be treated as a distinct third
donor in the existing fork theorem.  Invoking the q-donor blockade lemma in
this branch would identify two logical roles and is invalid.

The path matching nevertheless records a second q-response object: the core
assigned to `q` before the pivot into the hole.  The smallest operation not
covered by the current selectors is consequently a **two-core q rerouting**:
globally select between the closing core, q's displaced path core, and the
protected split-support core `D(U)`, while simultaneously substituting for
the shared floater or releasing the root anchor and returning the unused
core's physical packet through the component.  Success must either free a
third-owner replacement packet, change the closing source/core/root, or pay
q while preserving the critical-top-up repair.  Failure must separate all
three q-core choices and the floater substitution at the same globally
maximal state.

This operation is strictly smaller than another unrestricted component
selector: all other owners' pools and floors have already been exhausted,
and the only unresolved collision is that `q` is both proposed donor and
closing source.

This role collision is now eliminated without duplicating q.  Return a
least-t deletion remainder `D-g` to the hole owner, keep q on its displaced
path core, and add the residual released by the incoming anchor `r -> q`.
Residual success pays q against the smaller target; residual failure forces
the incoming q-target core to be a strict q self-response.  See
[`Q_CLOSING_SOURCE_RESIDUAL_REASSIGNMENT_LEMMA_20260811.md`](Q_CLOSING_SOURCE_RESIDUAL_REASSIGNMENT_LEMMA_20260811.md).

## Consequence

The anchor-containing critical-top-up separator has two, not one, physical
interfaces:

1. six **q-donor-role-available** pivots, whose shared-floater conflict is
   removed by the `B_q` substitution and whose continuation is the existing
   donor/rank-two machinery; and
2. six **q-source-collision** pivots, now eliminated by deletion-remainder
   return plus the incoming-anchor residual dichotomy.

Accordingly, the root/q reservoir does close the physical floater conflict,
but it does not identify q's two logical roles.  Any claimed mixed-margin
closure that applies the q-donor blockade directly skips the mandatory
intersection (1); after the `B_q` repair, applying it to all twelve pivots
still skips the six source-role collisions.

## Verification and boundary

[`anchored_q_donor_or_source_collision_audit.json`](anchored_q_donor_or_source_collision_audit.json)
replays the six anchored Hamiltonian paths, the eighteen nonself hole pivots,
and the twelve stable anchor cycles.  It verifies the 6/6 role split, all
cycle-length counts, distinct-donor role eligibility in every non-q-source
case, and the exact singleton-floater intersection (1).

This is a graph/role reduction.  The cited `B_q` and q-source residual lemmas
supply the physical floater and role repairs.  The remaining non-q-source
donor/rank-two continuation, globally maximal countermodel alternative, GG,
and four-agent/general additive EFX remain open.
