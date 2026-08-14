# R2 response-role critical compression lemma

**Date:** 2026-08-14

**Status:** cap-free premise compression and exact physical-lift dichotomy;
hidden-minimum split conversion remains open

## Input

Use the saturated root-facing form-R2 support state with the twelve named
base/current provenance regions

\[
 a0,a1,h,j,k,q0,l,e,m,gq,gr,p.
\]

Fix one actual response witness for each of the three numerical-core edges

\[
 r\to q,\qquad q\to r,\qquad s\to d.            \tag{1}
\]

Thus the first witness lies in `Q`, the second in `A+H`, and the third in
`W`.  No cardinality bound is imposed on any named region or witness.

## At most twenty-two critical roles

Split every base/current provenance region in the three response targets at
membership in its witness from (1).  There are nine such regions:

\[
 (a0,a1,h),\qquad(j,k,q0),\qquad(m,gq,gr).
\]

Each creates at most an inside and an outside cell.  The unaffected regions
`l,e,p` create three more cells.  Hence response membership and physical
provenance require at most

\[
                         2\cdot9+3=21             \tag{2}
\]

nonempty roles.

Choose a physical good `z` minimizing row `d` on the root packet `A` and
retain it as a singleton.  If its response/provenance cell contains other
goods, split that cell once more.  Contract every remaining nonempty cell to
one supergood whose value vector is the coordinatewise sum of its physical
goods.  The resulting instance has at most twenty-two goods.

## Premise preservation

The contraction preserves exactly every total of:

- a base bundle;
- a current support bundle;
- a named packet `A,H,Q,E,W,P`; and
- any of the three fixed response witnesses.

It therefore preserves all strict desire and normalization premises.

For an observer `i`, let `T` be the total value of a physical bundle,
`m_G` its least physical-good value, and `m_C` its least contracted-atom
value.  Every contracted atom is a sum of positive goods, so

\[
                         m_C\ge m_G.
\]

Consequently

\[
                         T-m_C\le T-m_G.          \tag{3}
\]

Every weak base-EFX, common-safety, current-safety, and nonroot-wall
inequality used by the R2 numerical core is therefore preserved from the
physical state to the contraction.

The only strict tail premise points in the opposite direction:

\[
                         v_d(W)<\operatorname{tail}_d(A).       \tag{4}
\]

Because the chosen `d`-minimum `z` remains a singleton, and every contracted
atom has row-`d` value at least `v_d(z)`, the contracted minimum of `A` is
still exactly `v_d(z)`.  Thus its contracted and physical tails agree, so
(4) is preserved exactly.  This is why the twenty-second critical role is
needed.

## Exact lift dichotomy

Suppose the contracted instance has a closed pairwise-disjoint family of
common-safe desired cores.  Expand every selected supergood back to its
physical cell.  Additivity preserves desire, disjointness, and base-owner
closure.

For each expanded core, either:

1. every physical deletion tail remains safe, in which case all expanded
   cores form a physical generalized PI family; or
2. some observer has a physical least good `g` hidden inside a nonsingleton
   selected supergood and

   \[
      m_G<T-b\le m_C,                            \tag{5}
   \]

   where `b` is that observer's base floor.  Separating `g` is a proper
   physical split of one of the at most twenty-two roles.

Thus arbitrary packet cardinality creates no third obstruction:

> every physical R2 survivor compresses to a twenty-two-good numerical-core
> state, and every contracted generalized PI either lifts to physical PI or
> exposes a strict hidden-minimum split.

## Computational interface

`run_allocated_e_form0_role_split_pi_cegar.py` searches the twenty-one-role
cell before the optional critical singleton is added.  It quantifies over
which inside/outside cells are nonempty and uses a binary-LRA oracle for
closed disjoint desired-core families; it does not enumerate `2^21`
bundles.  Any eventual UNSAT result for that driver is still a bounded
split-cell theorem, not the cap-free conclusion of this lemma.

## Remaining claim boundary

This lemma proves a lossless compression of the R2 **premises** and the exact
PI-versus-hidden-minimum lift dichotomy.  It does not prove that the current
twenty-one-role CEGAR terminates UNSAT, cover the optional twenty-second
critical split computationally, convert a hidden minimum into an admissible
four-edge transfer, or prove the active fixed-`U` theorem.

The smallest remaining analytic step is now precise: show that the proper
split in (5), under saturated root-facing R2 premises, enters the retired-
packet collision terminal or directly yields an observer-safe four-edge
allocation.
