# Disjoint compressed-core physical Hall-lift lemma

**Date:** 2026-08-14

**Status:** cap-free reduction to physical PI, external response, or an exact
Hall-deficient response family

## Input

Let `P` be a set of `k` owners, where `k` is three or four.  Suppose
`(S_t)_{t in P}` is a family of pairwise-disjoint physical bundles such that

\[
v_t(S_t)>v_t(X_t)=1 \qquad(t\in P),              \tag{1}
\]

and every good in their union is base-owned by an owner in `P` or by base
charity.  The bundles may have arbitrary finite cardinalities.  They need
not yet be physically common-safe.

For each bundle `S_t`, define its internal response-neighbor set

\[
N(t)=\{h\in P:\text{some }D\subseteq S_t
\text{ is common-safe and }v_h(D)>1\}.           \tag{2}
\]

Record an **external response** if the same property holds for an owner
`h notin P`.

## Globally minimal extraction

For fixed `t`, the finite family

\[
\{(h,D):h\in N,\ D\subseteq S_t,\ v_h(D)>1\}
\]

is nonempty by (1).  Choose a pair `(h_t,D_t)` with inclusion-minimal
support.  For every owner `i` and every `g in D_t`,

\[
v_i(D_t-g)\le1,                                  \tag{3}
\]

because otherwise `(i,D_t-g)` would be a strictly smaller member of the
family.  Hence `D_t` is a physical common-safe desired core.  Therefore each
bundle has either a neighbor in `P` or an external response source.

## Hall trichotomy

Exactly one of the following structural outcomes is available.

1. **External response.** Some `S_t` has a common-safe desired core sourced
   by an owner outside `P`.  This is a new source/component coordinate for
   the closed `P` family.
2. **Physical generalized PI.** The bipartite graph from bundles `t` to
   internal sources `N(t)` has a perfect matching.  Choose a core realizing
   each matched edge.  The sources are then exactly the owners in `P`; the
   chosen cores are pairwise disjoint because the `S_t` are disjoint; and
   all chosen goods are base-owned by `P` or charity.  The closed disjoint-
   core characterization gives a physical generalized PI.
3. **Hall deficiency.** There is a nonempty `J subseteq P` with

   \[
   \left|\bigcup_{t\in J}N(t)\right|<|J|.        \tag{4}
   \]

Hall's theorem proves that outcome 3 is exactly the obstruction after
outcome 1 is excluded and outcome 2 is unavailable.

## Minimal deficiency is a one-hole normal form

Choose `J` inclusion-minimal subject to (4). Every proper subset of `J`
satisfies Hall. Removing any one target `t` therefore leaves `J-{t}`
matchable to distinct sources. Moreover,

\[
|N(J)|=|J|-1.                                    \tag{5}
\]

Indeed `N(J-{t}) subseteq N(J)` and Hall on the proper subset gives
`|N(J)|>=|J|-1`, while (4) gives the reverse inequality. Thus a minimal
physical-core Hall obstruction is not an arbitrary many-hole graph. It is a
near-perfect response assignment plus one unmatched bundle. For at most four
owners this uses at most three distinct response-source edges; adding one
charity packet remains within the four-edge budget.

This closes only the topology count. Paying the unmatched owner, satisfying
all observers, and making the selected cores supplier-compatible are the
substantive remaining obligations.

## Consequence for the seven-endpoint certificate

Every PI clause in the minimized allocated-`E` certificate has three or four
compressed sources.  Expanding such a clause physically therefore never
leaves an untyped “tail mismatch.”  It gives physical generalized PI,
external response augmentation, or the explicit owner-side Hall deficiency
(4).  Arbitrary packet cardinality disappears from this branch.

This complements the hidden-minimum lemma: the latter identifies the exact
least-good split inside an unsafe compressed core, while the present lemma
extracts the globally minimal physical response and records the only reason
that the disjoint family may fail to close.

## Exact audit

`tracks/parkability/audit_disjoint_compressed_core_hall_lift.py` exhausts all
nonempty three-by-three and four-by-four response-incidence graphs.  For each
graph it independently verifies that a perfect matching exists exactly when
no Hall-deficient target subset exists. For every inclusion-minimal
deficiency it also verifies (5) and a matching after deletion of each chosen
target. The result is recorded in
`results/disjoint_compressed_core_hall_lift_audit.json`.

## Claim boundary

Proved: the cap-free physical lift of every three-/four-core compressed PI
clause to physical PI, an external response, or a precise Hall deficiency.

Not proved: that saturation excludes every external response at the same
fixed record, that the Hall-deficient cores are supplier-compatible, that
the deficiency converts to the companion two-creditor/base-restoration
operation, or the universal four-edge/general EFX theorem.
