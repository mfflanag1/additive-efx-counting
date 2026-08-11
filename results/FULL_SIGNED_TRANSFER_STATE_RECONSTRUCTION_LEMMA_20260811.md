# Full signed-transfer state reconstruction lemma

**Date:** 2026-08-11

**Status:** cap-free closure of the physical-label persistence interface;
observer-safe payment of the reconstructed cycle remains open

## Canonical full decoration

Fix a base allocation `(X,P)` of the finite ground set `G`, with one bundle
`X_i` for each owner and charity `P`.  For any later allocation `(Y,P')`
define, for every owner—not only owners carrying positive observer debt—

\[
 I_i=Y_i\setminus X_i,
 \qquad O_i=X_i\setminus Y_i.                    \tag{1}
\]

The **full signed decoration** is the vector

\[
 \Sigma_X(Y)=((I_i,O_i))_{i\in N}.               \tag{2}
\]

This is physical packet data.  It records no historical scalar potential.

## Reconstruction

For every owner,

\[
 Y_i=(X_i\setminus O_i)\mathbin\cup I_i.         \tag{3}
\]

Because allocations are disjoint and conserve `G`, charity is then forced:

\[
 P'=G\setminus\bigcup_{i\in N}Y_i.               \tag{4}
\]

Consequently two allocations with the same base and the same full signed
decoration are identical, including charity.  Their moved-good supplier
graph, connected components, owner surpluses, and every physical target
support are identical as well.

## Complete repeated-response state

At a paid splice, attach to (2):

1. the unmatched target or charity hole `H`;
2. the selected rank-four response matching;
3. for every selected edge, its source, physical target support, desired
   core, incoming packet, and released packet; and
4. the paid anchor and consumed support named by the recurrence.

Call the resulting finite record `R`.  If `R` repeats, (3)--(4) force the
same allocation and charity, while the edge portion of `R` forces the same
physical response and release labels.  Thus the fixed-state premise of the
charity-augmented five-target hole-cycle lemma is automatic at an exact
repeat of `R`.

If the coarse tuple `(hole, paid anchor, consumed support)` returns but `R`
does not, then at least one exact signed transfer, target support, desired
core, matching edge, or release label is new.  Recording that finite object
is permanent response/support augmentation.  Since `G` is finite, this
branch cannot occur indefinitely without an exact repetition.

The complete record is essential.  Keeping only `(I_i,O_i)` for observers
with positive base-safety debt does not determine the bundles of zero-debt
owners and therefore cannot justify physical-label persistence.

## Consequence for repeated support

Dynamic GG resets no longer create a separate label-persistence gate.  A
return either changes the complete physical record and is permanent finite
augmentation, or repeats it exactly and exposes the verified alternating
charity/owner-target cycle.  What remains is not state identification but
payment: show that the cycle's released packets preserve the observer
surplus inequalities, or obtain an exact globally maximal separator.

## Verification and boundary

[`full_signed_transfer_state_reconstruction_audit.json`](full_signed_transfer_state_reconstruction_audit.json)
exhausts every pair of base and candidate allocations of four labeled goods
among four owners and charity (390,625 pairs), verifies reconstruction and
injectivity of the signed decoration for each base, and checks that charity
is uniquely recovered by conservation.

This lemma does not force a response edge into every successive hole, pay an
alternating cycle, establish the universal connected-splice theorem, close
GG, or prove four-agent/general additive EFX.
