# Degree-zero q split-core root-flip lemma

**Date:** 2026-08-11

**Status:** cap-free removal of degree-zero `q` as an ordinary Hall terminal;
termination after the resulting source-margin capture remains open

## Hidden split-support response

Fix retained support `U subseteq T_r` with live `q` margin

\[
 D(U)=(T_r\setminus U)+f,
 \qquad v_q(D(U))>v_q(X_q).                         \tag{1}
\]

The core `D(U)` is common-safe.  After a complete charity path, its goods
may lie in several current targets: `f` lies in the changed `q` target,
while `T_r\setminus U` may be split between the changed root, an external
sink, and residual packets.  Nevertheless every good remains in the
complete owner union plus charity, and their union is still the physical
bundle (1).

Consequently degree zero for `q` in the ordinary one-target response graph
does **not** mean that `q` has lost every response.  It says only that no
single current target contains a common-safe desired `q` core.  Bundle (1)
is a split-support response hyperedge.

## Root flip

Reassemble (1) and return to the `q`-oriented dual-anchor state.  Apply the
universal retained-support reset against every floater-free core retained
from the detour.  Exactly one of the following happens.

1. The reset preserves (1).
2. Fresh overlap strictly enlarges `U` while the reduced core remains
   desired.
3. Fresh overlap captures the remaining `q` margin and enters the anchored
   residual rotation.

In the first two branches, use the canonical external response core
disjoint from the reduced `D(U')`.  If its complement pays the earlier
root, the dual root-paid selector applies.  It yields an EFX lex endpoint,
a release-compatible response/Hall component, or a root-critical packet,
while `q` is explicitly represented.  Protected-`q` retention prevents a
later top-only reset from silently sacrificing `q` again at the same
retained state.

If the complement does not pay the root, minimal dual-core extraction gives
a packet

\[
 C=C_q\mathbin{\dot\cup}C_a
\]

that restores root payment.  Either both reduced source cores remain
desired, returning to the root-paid selector, or

\[
 v_q(C_q)\ge v_q(D(U'))-v_q(X_q)                   \tag{2}
\]

or the analogous external-source margin is captured.  Thus failure of the
split-core flip is a named physical two-row packet, not another degree-zero
Hall state.

## Consequence

At a sacrificed-`q` boundary, combine this lemma with anchor-constrained
`q`-priority matching.

1. An anchor gap exposes one unit of response-rank growth and its alternating
   path.
2. An anchor-compatible matching represents `q`, and that coverage persists.
3. If ordinary matching leaves `q` with degree zero, the split-support root
   flip gives persistent `q` coverage, strict retained-support growth,
   captured-margin rotation, or the explicit source-capture packet (2).

This removes degree-zero `q` from the list of untyped reset recurrences.  It
also explains why one-target Hall matching alone was too weak: the known
mutual core can straddle the connected transfer component.

## Verification and boundary

[`degree_zero_q_split_core_root_flip_audit.json`](degree_zero_q_split_core_root_flip_audit.json)
records exact hashes and replay status for universal retained support,
canonical external-core selection, the dual root-paid selector, minimal
dual-core extraction, captured-margin rotation, and protected-`q`
retention.

This composition does not terminate a `q`- or external-source margin packet
after (2), prove the anchor-gap path is release-compatible, close every
root-critical/captured-bottom revisit, close GG, or prove four-agent/general
additive EFX.
