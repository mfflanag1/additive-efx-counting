# Rank-three disjoint-double-core complete four-edge lemma

**Date:** 2026-08-13

**Status:** abstract cap-free conditional graph construction; not applicable
to the canonical paid singleton-charity state, which excludes the required
response edge into charity

**Correction (2026-08-13):** the three forms below came from the abstract
five-target response census.  Each requires a desired response into charity.
For a base-safe singleton charity at a paid state, such an edge is impossible.
Accordingly this remains a correct conditional conservation lemma but is not
the physical normal form of the present fixed-`U` gate.  The corrected graph
interface is in
[`PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md`](PAID_SINGLETON_CHARITY_RANK_THREE_OWNER_CYCLE_LEMMA_20260813.md).

## The exact construction

Every minimum root-facing rank-three response normal form has three selected
matching edges and the unmatched sacrificed-owner response `c -> q`.  Up to
the three forms in the exact graph census, the four response edges are

\[
 q\to c_0,\quad r\to q,\quad s\to r\text{ or }c,
 \quad c\to q,
\]

or

\[
 q\to s,\quad r\to q,\quad s\to c_0,
 \quad c\to q,                                      \tag{1}
\]

where `c_0` is charity.  Thus every owner is the source of one response, the
charity is the target of one response, and `q` is the unique target of two
responses.

For each response `i -> j`, let `D[i->j]` be its nonempty physical desired
core inside target bundle `Y_j`.  Assume only that the two cores inside
`Y_q`, namely `D[r->q]` and `D[c->q]`, are disjoint.  Cores in all other
targets are automatically disjoint because their target bundles are
disjoint.  Give every source `i` its core `D[i->j]` and leave every target's
complementary residual with that target.

The charity target is the singleton packet `{p}`.  Its unique nonempty core
is therefore all of `{p}`, so the final charity is empty.  The only active
support-provenance transfers are the four reversed responses

\[
 j\longrightarrow i\qquad\text{for each }i\to j.  \tag{2}
\]

They conserve every physical good and use exactly four edges, independent of
the cardinality of any core or residual packet.

## Why the functional restriction is not the proof

In every form, `q` supplies `D[r->q]` to `r` and `D[c->q]` to `c`.  Hence the
canonical response-reversal construction is connected but nonfunctional:
one physical supplier has two recipients.  The observed functional
four-edge completions remain useful evidence, but proving their universal
existence would be a stronger and potentially unnecessary detour.

## Exact remaining obstruction

The cap-free universal theorem is now localized to two tasks:

1. **Shared-target overlap.** Derive disjoint payment-capable cores for the
   anchor response `r -> q` and root-facing response `c -> q`, or show how to
   repair their overlap without creating a fifth support edge.
2. **Endpoint inequalities.** Prove from the full signed source margins and
   saturated observer-surplus records that each bundle constructed above
   pays its owner and is EFX-safe against every other final owner bundle.

The first task is the physical content of the captured-support polarity in
the rank-three global residual-split lemma.  If the cores are disjoint, no
additional topology problem remains: (2) is already a complete four-edge
allocation.  If they overlap, a repeated atom cannot be sent to two owners,
so graph saturation alone is insufficient.

## Verification and boundary

[`audit_rank_three_disjoint_double_core_four_edge.py`](../tracks/parkability/audit_rank_three_disjoint_double_core_four_edge.py)
independently instantiates all three normal forms.  Treating every desired
core and residual as an arbitrary packet atom, it verifies disjoint
conservation, empty final charity, connectedness, and exactly four reversed
support edges.  This proves the graph/conservation lemma for unrestricted
packet sizes.

The lemma is conditional and its response-to-charity premise is excluded in
the canonical paid singleton-charity cell. It does not derive disjointness,
owner payment, or observer safety from saturation and does not prove the
universal four-edge theorem, fixed-`U` termination, or additive EFX.
