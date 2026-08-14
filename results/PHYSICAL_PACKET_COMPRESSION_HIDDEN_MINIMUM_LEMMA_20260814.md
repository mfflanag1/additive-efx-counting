# Physical packet-compression hidden-minimum lemma

**Date:** 2026-08-14

**Status:** cap-free algebraic lemma; split-conversion gate remains open

## Theorem

Let a physical bundle `S` be partitioned into nonempty compressed atoms
`C_1,...,C_t`.  Fix an additive observer `i` and a safety threshold `b`.  Put

\[
T=v_i(S),\qquad m_C=\min_j v_i(C_j),\qquad
m_G=\min_{g\in S}v_i(g).
\]

If `S` is EFX-tail safe when every `C_j` is treated as one atom but is unsafe
under physical single-good deletion, then

\[
T-m_C\le b<T-m_G,
\]

and therefore

\[
m_G<T-b\le m_C. \tag{1}
\]

In particular, a least physical good witnessing the failure cannot itself be
a singleton compressed atom.  It lies strictly inside a nonsingleton atom,
and separating it from that atom is a proper physical packet split.

The statement is independent of the number of goods in any packet.

## Consequence for a compressed generalized PI

Expand every compressed core in a pairwise-disjoint desired-core family back
to its physical goods.  Source desire is unchanged by additivity, and the
expanded cores remain pairwise disjoint.  For each expanded core exactly one
of the following occurs:

1. every observer's physical deletion tail is safe, so that core is already
   a valid physical common-safe desired core; or
2. some observer supplies a strict hidden-minimum witness satisfying (1),
   inside a selected nonsingleton residual atom.

Thus packet cardinality cannot create any third failure mode.  Lifting the
seven-endpoint bounded dichotomy is reduced to converting these proper
hidden-minimum splits, with their supplier and priority decorations, into
physical PI, a valid anchor change, response-rank progress, or a complete EFX
endpoint.

## Proof

Compressed safety and physical unsafety give

\[
T-m_C\le b \quad\text{and}\quad T-m_G>b.
\]

Rearranging yields `m_G<T-b<=m_C`.  If a least physical good were a singleton
compressed atom, then its value would be one of the quantities minimized in
`m_C`, giving `m_C<=m_G`, contrary to (1).  Hence the witness is contained in
a nonsingleton compressed atom.  Removing that one good from its containing
atom produces two nonempty physical pieces.  No cardinality bound was used.

## Exact audit

`tracks/parkability/audit_packet_compression_hidden_minimum.py` independently
asks Z3 to refute each implication for 1 through 12 compressed atoms.  For
every arity, the negation of strict hidden-minimum separation, the possibility
that the hidden minimum is a singleton atom, and the negation of the full
margin chain are all UNSAT.  The generated record is
`results/packet_compression_hidden_minimum_audit.json`.

## Claim boundary

Proved: a cap-free and observer-wise classification of every discrepancy
between compressed and physical EFX tails.

Not proved: that every hidden-minimum split is recipient-feasible, that its
supplier component preserves every protected floor, that the remaining
root/base-restoration hitting cut converts to PI, or that every saturated
root-facing rank-three fixed-`U` state has a four-edge complete EFX allocation.
