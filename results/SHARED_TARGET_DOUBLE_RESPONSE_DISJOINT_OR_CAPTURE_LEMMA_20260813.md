# Shared-target double-response disjoint-or-capture lemma

**Date:** 2026-08-13

**Status:** cap-free exact reduction of the shared-target overlap; reversal of
the captured-margin branch remains open

## Setting

Let `A` and `C` be two current response cores contained in the same physical
target `T`.  Core `A` is reserved for the permanent anchor source, while `C`
is desired by the unmatched root-facing source `c`.  Write that source's
protected utility floor as `F_c` and its strict response margin as

\[
 \mu_c=v_c(C)-F_c>0.                               \tag{1}
\]

Assume `C` is common-safe at the relevant current observer floors.  Every
subbundle of `C` is then common-safe: for positive additive values, the EFX
tail of a subbundle cannot exceed the tail of its containing bundle.

## Dichotomy

Put

\[
 C_0=C\setminus A,
 \qquad H=C\cap A.                                \tag{2}
\]

If

\[
 v_c(C_0)>F_c,                                    \tag{3}
\]

choose an inclusion-minimal desired subbundle `D subseteq C_0`.  It is
common-safe, is disjoint from `A`, and remains a response for `c`.  The
disjoint-double-core four-edge lemma therefore removes the physical overlap
obstruction.

If (3) fails, additivity gives

\[
 v_c(H)=v_c(C)-v_c(C_0)
       \ge v_c(C)-F_c=\mu_c.                      \tag{4}
\]

Thus the shared support captures the entire strict response margin.  If
`v_c(C_0)<F_c`, the inequality in (4) is strict.  These alternatives are
exhaustive and use no bound on goods or packet sizes.

## Consequence for the four-edge theorem

Combined with the exact three-form response census and the disjoint-core
response reversal, the topology/conservation part of the universal theorem
now has one scalar obstruction:

> the permanent anchor overlap captures the whole unmatched source margin.

There is no separate arbitrary packet-graph search in the disjoint branch.
At a genuinely saturated fixed-`U` state, the remaining proof must show that
the capture in (4) triggers retained-support growth, response replacement,
a release-compatible PI component, or a four-edge payment-preserving
rerouting.  Alternatively, a countermodel must satisfy (4) together with all
signed recurrence and observer-surplus premises while defeating every such
rerouting.

## Verification and boundary

[`audit_shared_target_double_response_overlap.py`](../tracks/parkability/audit_shared_target_double_response_overlap.py)
checks the exact packet partition and proves both weak and strict versions of
(4) by independent QF-LRA contradiction.  The inheritance of common safety
under deletion is the standard positive-additive tail monotonicity argument.

This lemma does not reverse (4), derive owner payment or observer safety, or
finish the universal four-edge extraction theorem.
