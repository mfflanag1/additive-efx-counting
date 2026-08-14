# Simultaneous hidden-minimum matching-or-capture lemma

**Date:** 2026-08-14

**Status:** cap-free physical-lift trichotomy; Hall-deficiency and captured
owner packets still require four-edge conversion

## Contracted family and physical slot responses

Let `(D_i)_{i in V}` be a closed pairwise-disjoint desired-core family in a
contracted R2 instance.  Treat every expanded `D_i` as one physical **slot**.

If `D_i` remains physical common safe, the slot has at least its old source
`i`, using `F_{i,i}=D_i`.  If it is unsafe, some observer desires a one-good
deletion `D_i-g`; a globally minimum-cardinality desired subcore inside such
a deletion is physical common safe.  Let `N(i)` contain every owner `b` for
which a physical common-safe desired core

\[
                         F_{i,b}\subseteq D_i      \tag{1}
\]

has been extracted.  Thus every slot has a nonempty neighborhood.  Safe
slots are not frozen: a matching may displace their old sources, which is
the required alternating-core freedom.

## Matching branch

Suppose the bipartite graph from all slots `V` to all owners `N` has a
matching `mu` covering `V`.  Use

\[
                         F_{i,\mu(i)}\subseteq D_i \qquad(i\in V).           \tag{2}

\]

All selected cores are nonempty, physical common safe, desired by distinct
sources, and pairwise disjoint.  Disjointness is automatic because the
original `D_i` are disjoint and each replacement stays inside its own slot.

Let

\[
                         W=\mu(V).                 \tag{3}

\]

The selected family has one core per source in `W`.  Every selected good had
base owner in `V` or charity.  Therefore:

1. if no selected good is base-owned by an owner in `V-W`, the family is
   closed on `W` and yields a physical generalized PI;
2. otherwise its union contains a concrete packet base-owned by an owner in
   `V-W`.  This is a **dropped-owner capture certificate**.

The matching branch is cap-free and uses no valuation bound.

## Deficiency branch

If no matching covers `V`, Hall's theorem gives a nonempty set

\[
                         J\subseteq V,
             \qquad |N(J)|<|J|.                 \tag{4}

\]

Every individual `N(i)` is nonempty, so a minimal deficient set has at least
two slots.  The obstruction is a genuine simultaneous-source collision, not
an artifact of freezing an already-safe source.

Thus expansion of a contracted closed family has exactly three outcomes:

1. a physical generalized PI family;
2. a matched physical family carrying base support of a dropped owner; or
3. a Hall-deficient set of physical slots competing for too few response
   sources.

There is no fourth packet-cardinality failure mode.

## Relation to R2 termination

The first outcome contradicts generalized-PI-freeness.  Outcomes 2 and 3
are the precise cap-free survivors:

- dropped-owner capture identifies the owner label and the actual physical
  support packet that must be returned or retired;
- Hall deficiency identifies the colliding response source set that must be
  rerouted, sacrificed, or promoted into the retired-packet terminal.

For four owners all bipartite deficiency types are finite, but finiteness of
the type graph is not termination of the signed packet process.  A repeated
owner/Hall label must still be shown to repeat or strictly reduce an actual
packet intersection while preserving the root certificate and the
four-edge budget.

## Claim boundary

This lemma proves the full cap-free combinatorial lift trichotomy for any
fixed contracted closed family.  It does not prove that a dropped-owner
packet is returned whole, that a Hall-deficient collision satisfies the
`T_{L,times}^*` retired-packet premises, that observer-surplus rows survive a
rerouting, or that the active fixed-`U` theorem follows.
