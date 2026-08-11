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

## Exact dichotomy

The twelve stable pivots divide evenly.

### 1. q is not the closing source

There are six pivots with `a != q`.  In every one,

\[
 q\notin\{r,t,a\}.
\]

Thus `q` is the unique named protected donor candidate outside the
root/hole/source roles.  Their cycle lengths are two cases of length three
and four cases of length four.  Conditional on making `D(U)` physically
available without restoring retained support, the third-owner
root-replacement selector applies with donor `b=q`.  Fork success pays the
component; strict q-donor blockade enters captured-q-margin handoff; aggregate
root concentration enters the existing bottom-absorption rotation.

This branch therefore has no anonymous donor choice.  Its sole unresolved
premise is **q-core availability**: reassemble or substitute the protected
split-support core while respecting the exact signed transfers and retained
support.

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
protected split-support core `D(U)`, while returning the unused core's
physical packet through the anchored component.  Success must either free a
third-owner replacement packet, change the closing source/core, or pay q
while preserving the critical-top-up repair.  Failure must separate all
three q-core choices at the same globally maximal state.

This operation is strictly smaller than another unrestricted component
selector: all other owners' pools and floors have already been exhausted,
and the only unresolved collision is that `q` is both proposed donor and
closing source.

## Consequence

The anchor-containing critical-top-up separator has two, not one, physical
interfaces:

1. six **q-donor-available** pivots, whose remaining gate is protected
   split-core availability; and
2. six **q-source-collision** pivots, whose remaining gate is the two-core q
   rerouting selector.

Accordingly, root/q reservoir inequalities alone cannot be applied as a
scalar payment bound.  They must first be accompanied by a support-conserving
q-core selection theorem.  Any claimed mixed-margin closure that applies the
q-donor blockade to all twelve pivots skips the six role-collision cases.

## Verification and boundary

[`anchored_q_donor_or_source_collision_audit.json`](anchored_q_donor_or_source_collision_audit.json)
replays the six anchored Hamiltonian paths, the eighteen nonself hole pivots,
and the twelve stable anchor cycles.  It verifies the 6/6 role split, all
cycle-length counts, and distinct-donor eligibility in every non-q-source
case.

This is a graph/role reduction.  It does not prove physical availability of
`D(U)`, construct the two-core q rerouting, eliminate either payment
separator, produce a globally maximal countermodel, close GG, or prove
four-agent/general additive EFX.
