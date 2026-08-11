# Universal paid-anchor support-reset lemma

**Date:** 2026-08-11

**Status:** cap-free monotonicity of every reset after paid-anchor consumption;
termination after captured hole-payment margin remains open

## Consumed paid-anchor support

Let `Y_d` be the paid pre-compression target of the current missing owner,
and let

\[
 T\subseteq Y_d                                    \tag{1}
\]

record goods already committed to retained response cores. The live anchor
part held inside the hole residual is

\[
 P(T)=Y_d\setminus T,                              \tag{2}
\]

with payment margin

\[
 \eta_d(T)=v_d(P(T))-v_d(X_d)\ge0.                 \tag{3}
\]

## Canonical overlap update

Suppose a reset must retain pairwise-disjoint response cores
`A_1,...,A_m`. Their fresh overlap with the live paid anchor is

\[
 K=\left(\bigcup_h A_h\right)\cap P(T).            \tag{4}
\]

Set

\[
 T'=T\cup K.                                       \tag{5}
\]

Then `P(T')=P(T)\setminus K` is disjoint from every retained core and

\[
 \eta_d(T')=\eta_d(T)-v_d(K).                      \tag{6}
\]

Exactly one of the following occurs.

1. **Preserved paid anchor.** `K=empty`. The physical paid anchor and support
   coordinate are unchanged.
2. **Fresh paid-anchor consumption.** `K` is nonempty and
   `v_d(K)<=eta_d(T)`. Then `d` remains weakly paid and
   \[
   T\subsetneq T'.                                 \tag{7}
   \]
3. **Captured hole-payment margin.** `v_d(K)>eta_d(T)`. The overlap captures
   more than the hole's entire remaining payment margin. Retain `T'`, stop
   requiring `d` to be paid by the reduced anchor, and enter the priority-
   valid sacrificed-owner residual/repair machinery with the explicit packet
   `K`.

Positivity makes branch 2 strict in support whenever `K` is nonempty. Since
`Y_d` is finite, branch 2 occurs only finitely often for a fixed physical
anchor.

## No silent restoration

A later orientation that wishes to restore a good of `T` to the hole while
also retaining the core that uses it is physically infeasible. If that core
is released first, its source and released packet form an explicit connected
return handoff. Thus the canonical reset never decreases `T`: it preserves
the retained core and shrinks the live anchor, or routes the source release
as a named component.

Combined with least-good anchor consumption, every fixed-hole paid-anchor
wall now yields represented-source utility growth, unsafe augmentation,
strict growth of `T`, or captured hole-payment margin. The former unrecorded
anchor restoration is eliminated.

## Verification and boundary

[`universal_paid_anchor_support_reset_audit.json`](universal_paid_anchor_support_reset_audit.json)
checks support partition, exact margin loss, exhaustive reset trichotomy, and
nested support monotonicity.

This lemma does not terminate the sacrificed-owner machinery after captured
margin, prove every explicitly released core gives an SDR, handle a change of
the physical paid anchor, close GG, or prove four-agent/general additive EFX.
