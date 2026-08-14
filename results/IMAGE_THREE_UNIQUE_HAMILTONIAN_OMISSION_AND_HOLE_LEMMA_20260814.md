# Image-three unique Hamiltonian omission and hole lemma

**Date:** 2026-08-14

**Status:** cap-free exact owner-graph normal form; the only remaining local
obligation is payment/safety of the missing-source path endpoint under mixed
frozen provenance

## Source-map normal form

Let `f:N->N` be nonself on four owners with image size three.  Let `m` be
the missing source, `a` the duplicated source, and let `u,v` be the two
targets satisfying `f(u)=f(v)=a`.

Exactly one of the two omissions `u` or `v` has the following property: the
three remaining undirected response edges form a spanning Hamiltonian path
on all four owners.  With their response orientation, that path is

\[
                 m=t_0\longrightarrow t_1
                  \longrightarrow t_2\longrightarrow t_3,    \tag{1}
\]

where `t_3` is the omitted target.  The represented response sources are
exactly `t_1,t_2,t_3`.

## Proof of existence and uniqueness

The complete four-edge owner graph is connected by
`IMAGE_THREE_FULL_OWNER_CONNECTED_RANK_DEFECT_LEMMA_20260814.md`.  Each
duplicated-source omission leaves a partial nonself map with three distinct
targets and three distinct sources.

The functional graph of `f` has one directed cycle.  The two incoming edges
to duplicated source `a` consist of one cycle/tree-continuation edge and one
branch-closing edge.  Deleting the branch-closing edge breaks the unique
cycle/branch and leaves the spanning path (1).  Deleting the other incoming
edge leaves either the directed cycle or a degree-three branch.  Hence the
Hamiltonian omission is unique.

Equivalently, exhaustive classification of all 48 maps finds exactly one
valid omission in every case.  A direct four-vertex proof follows by checking
the only possible functional shapes: a two-cycle with two attached vertices,
or a three-cycle with one attached vertex.

## Hamiltonian response allocation

Choose common-safe desired cores on the three path edges and reverse them.
Give singleton charity `p` to the missing source `m`.  At the current-holder
level this is the four-edge path

\[
            charity\longrightarrow m=t_0
             \longrightarrow t_1\longrightarrow t_2
             \longrightarrow t_3.               \tag{2}
\]

Every represented source `t_1,t_2,t_3` receives a desired core and is
strictly paid relative to its response floor.  The unique possible payment
hole is `m`: its target core on the first path edge is removed, and charity
need not cover that loss or its base deficit.

At later probes a path core may contain goods from several frozen-`Y`
suppliers.  Thus (2) counts current-holder edges, not automatically the
objective's original-supplier pairs.  The exact physical pair set must still
retain every supplier represented in every selected core.

## Complementary omission

The other duplicated-source omission preserves the short functional cycle
or branch.  In the missing-supplies-duplicate class, omitting target `m`
lets `m` retain its whole current bundle plus charity and therefore closes
owner payment, but sacrifices the Hamiltonian path.  This is the exact
tradeoff behind the earlier duplicate-omission and path constructions:

1. Hamiltonian omission: three represented sources paid, one missing-owner
   hole;
2. missing-target omission when available: all owners paid, but cyclic and
   potentially mixed-support edge overflow.

## Consequence and boundary

Owner topology and response rank are no longer ambiguous.  Every image-three
fan contains one canonical spanning response path.  The universal theorem
reduces locally to repairing its single missing-owner hole while retaining
mixed frozen provenance, or converting failure into the saturated
base-margin/decorated-response terminal.

Proved: existence and uniqueness of the Hamiltonian omission for all 48
maps, its oriented endpoints, and the single-hole payment identity.  Not
proved: payment of `m`, frozen-supplier four-edge compression, observer EFX
safety, terminal admission, or the fixed-`U` theorem.
