# Simultaneous hidden-minimum matching-or-capture lemma

**Date:** 2026-08-14

**Status:** cap-free physical-lift trichotomy; Hall-deficiency and captured
owner packets still require four-edge conversion

## Contracted family and unsafe slots

Let `(D_i)_{i in V}` be a closed pairwise-disjoint desired-core family in a
contracted R2 instance.  Let `I subseteq V` be exactly the indices whose
expanded physical cores are not common safe, and put

\[
                         S=V\setminus I.          \tag{1}
\]

The cores indexed by `S` are already physical common-safe desired cores and
will be retained.

For each `i in I`, physical unsafety supplies an observer and a deleted good
for which `D_i-g` is desired.  Choose any globally minimum-cardinality
desired subcore inside such a deletion.  Global minimality makes it physical
common safe.  More generally, let `N(i)` contain every owner

\[
                         b\in N\setminus S        \tag{2}
\]

for which some physical common-safe desired core `F_{i,b}` is contained in a
one-good deletion of `D_i`.  Sources in `S` are excluded because their safe
cores are already retained.

## Matching branch

Suppose the bipartite graph from unsafe slots `I` to available sources
`N-S` has a matching `mu` covering `I`.  Retain `D_j` for `j in S` and use

\[
                         F_{i,\mu(i)}\subset D_i  \qquad(i\in I).            \tag{3}

\]

All selected cores are nonempty, physical common safe, desired by distinct
sources, and pairwise disjoint.  Disjointness is automatic because the
original `D_i` are disjoint and each replacement stays inside its own slot.

Let

\[
                         W=S\cup\mu(I).           \tag{4}

\]

The selected family has one core per source in `W`.  Every selected good had
base owner in `V` or charity.  Therefore:

1. if no selected good is base-owned by an owner in `V-W`, the family is
   closed on `W` and yields a physical generalized PI;
2. otherwise its union contains a concrete packet base-owned by an owner in
   `V-W`.  This is a **dropped-owner capture certificate**.

The matching branch is cap-free and uses no valuation bound.

## Deficiency branch

If no matching covers `I`, Hall's theorem gives a nonempty set

\[
                         J\subseteq I,
             \qquad |N(J)|<|J|.                 \tag{5}

\]

This includes the case `N(i)=emptyset`: every globally minimal physical
response inside slot `i` uses a source in the already-retained set `S`, so
the obstruction is an explicit stable-source collision.

Thus expansion of a contracted closed family has exactly three outcomes:

1. a physical generalized PI family;
2. a matched physical family carrying base support of a dropped owner; or
3. a Hall-deficient set of unsafe slots competing for too few unoccupied
   physical response sources.

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
