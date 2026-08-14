# Paid-singleton-charity rank-three owner-cycle lemma

**Date:** 2026-08-13

**Status:** cap-free correction of the rank-three graph interface; physical
overlap/release compatibility remains

## No response into a safe singleton charity

Let `{p}` be the current charity packet. Assume it is safe at the GG base,

\[
 v_i(p)\le v_i(X_i),                               \tag{1}
\]

and a represented response source `i` is paid,

\[
 v_i(Y_i)\ge v_i(X_i).                             \tag{2}
\]

Then `p` is neither base-desired nor current-desired by any owner:

\[
 v_i(p)\le v_i(X_i)\le v_i(Y_i).                  \tag{3}
\]

Consequently no paid represented source has a live base/current response
edge into charity. The sacrificed source may lie below base and is not
covered by this assertion, but it is not part of the selected rank-three
matching. In the canonical packet cell, (1) follows because `p` lies in the
two-good base bundle `{e,p}`: base EFX bounds each observer's value for `p`,
while its base owner has positive value for `e` and normalized total one.

This invalidates using the abstract five-target Hamiltonian-to-charity forms
as the selected rank-three normal form of this paid singleton-charity state.
Those forms require the paid represented source `q` or `s` to point to
charity, which the exact packet premises forbid.

## The corrected rank-three graph

The selected matching represents `r,q,s`, contains the permanent anchor
`r -> q`, and the unmatched sacrificed source has the recurrent edge
`d -> q`. In addition, the literal strong-envy wall against the root core
`A subseteq Y_r` forces a second sacrificed-source response `d -> r`.
This distinction was missed in the first graph transcription. Since charity
is unavailable as a response target, the other two
matching edges point to distinct owner targets. Exhausting the four
possibilities shows that these five response edges always contain a directed
owner cycle: two forms contain a two-cycle and two have shortest cycle three.
Equivalently, the cases close through one of

\[
 r\leftrightarrow q,\qquad r\leftrightarrow d,
 \qquad q\leftrightarrow d,\qquad
 r\to q\to s\to r,\qquad d\to q\to s\to d.     \tag{4}
\]

No item or packet-size bound is used.

## Consequence

The live rank-three gate is not a two-hole Hamiltonian charity path. It has
five nonself response edges containing a forced two- or three-owner cycle,
plus the separate physical
singleton-charity transfer. If the cycle cores are disjoint and internally
released, the generalized-PI machinery closes the saturated state. If an
incoming packet has an outside supplier, physical owner coverage grows.
Thus the only genuine survivor is the overlap/full-margin-capture polarity
(or a changed supplier/release label), now on a cycle of length at most three.

## Verification and boundary

[`audit_paid_singleton_charity_rank_three_owner_cycle.py`](../tracks/parkability/audit_paid_singleton_charity_rank_three_owner_cycle.py)
proves (3) for a paid represented source in QF-LRA and independently
enumerates the four matching forms, obtaining two shortest cycles of each
length two and three.

The lemma does not reverse the overlap polarity, prove that an owner cycle is
release-compatible, allocate the singleton charity, or finish the universal
complete-EFX theorem.
