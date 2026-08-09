# Critical-minimum contraction lemma

**Date:** 2026-08-09
**Status:** cap-free analytic lemma
**Scope:** additive valuations; arbitrary agents, goods, and packet sizes

## Lemma

Let `Y` be an allocation and let `Z=Y_j` be one of its nonempty bundles.
For each observer `i`, choose a good

\[
m_i\in\arg\min_{g\in Z}v_i(g).
\]

Let `H` be a subset of `Z` containing at least two goods and no selected
`m_i`.  Replace all goods in `H` by a supergood `h` with

\[
v_i(h)=v_i(H)\qquad\text{for every }i.
\]

Then contraction preserves every agent's utility and every EFX comparison
to `Z`.  Equivalently, expanding `h` back into `H` also preserves EFX.
The same conclusion holds for an external observer whose fixed bundle is
not changed.

## Proof

For additive valuations, observer `i`'s strongest deletion comparison to
`Z` is

\[
\max_{g\in Z}v_i(Z\setminus\{g\})
=v_i(Z)-\min_{g\in Z}v_i(g).
\tag{1}
\]

Contraction does not change `v_i(Z)`.  Since `m_i` remains outside `H`, it
is still an item in the contracted bundle.  Moreover, by nonnegativity,

\[
v_i(h)=\sum_{g\in H}v_i(g)\ge v_i(g)\ge v_i(m_i)
\qquad(g\in H).
\]

Thus the minimum item value in the contracted bundle remains
`v_i(m_i)`.  Both terms on the right of (1) are unchanged, so all deletion
comparisons to `Z` are unchanged.  Bundle totals, and hence the recipient's
utility and every lexicographic utility coordinate, are unchanged as well.
\(\square\)

## Consequence for packet lifting

For one fixed candidate allocation, at most one critical minimum per
observer must be retained in each mixed bundle.  With four observers, any
bundle containing at least six goods has two noncritical goods that can be
merged while preserving that allocation's EFX status exactly.

For the alternating external-observer proof this converts the vague
"expansion creates more inequalities" issue into a precise obstruction:

> A minimal counterexample to a proposed rival menu can resist contraction
> only when every pair of goods that is merged contains a minimum-deletion
> witness for some observer in some candidate bundle.

The remaining combinatorial gate is to show that the four alternating
packets cannot all be covered by such critical witnesses without either
creating one of the six atomic wall contradictions or a compatible desired
family.  The corrected `(2,2,2,2)` cell is exactly the smallest cell in
which every packet can be fully covered this way.

## Boundary

This lemma preserves a specified allocation or a specified finite family of
allocations when the chosen minima are retained for each one.  By itself it
does not preserve the absence of every possible compatible family under
contraction, and therefore does not yet prove the arbitrary-packet rooted
escape theorem.
