# Evolved-target minimal-source trichotomy lemma

**Date:** 2026-08-11

**Status:** cap-free elimination of an unnamed unsafe evolved-target branch;
the resulting canonical root/external/Hall terminals remain open

## Global minimal response core

Use the anchored residual rotation

\[
 D_r=T_q+f,
 \qquad W=B_q+L,
 \qquad R=(T_r\setminus L)+B_r.
\]

If the proposed allocation is not EFX, its sole possible wall is against
`W`.  Therefore the finite family

\[
 \mathcal D(W)={D\subseteq W:
   v_i(D)>v_i(X_i)\text{ for at least one owner }i\}
\]

is nonempty.  Choose an inclusion-minimal member `D` and one source `i`
that desires it.

The selected core is common-safe.  Indeed, for every `g in D`, the proper
subset `D-g` is not in `D(W)`.  Hence for every observer `k`,

\[
 v_k(D-g)\le v_k(X_k).
\]

Taking the maximum over deleted goods gives

\[
 \tau_k(D)\le v_k(X_k)\qquad(k\in\{r,q,c,s\}).      \tag{1}
\]

Thus unsafe deletion never creates an untyped target: global minimality
returns a common-safe desired core with one of four named sources.

## Exhaustive source routing

Exactly one of the following source types applies.

### 1. Later mutual source `i=q`

Regard `D` as a response into the evolved `q` slot.  Its incoming goods are
contained in `L`, and its release contains `T_q`.  The root edge into
`D_r=T_q+f` releases all of `L+R`, while `f` is charity.  Hence the root
edge and the `q` self-response have disjoint, internally supplied incoming
sets and form a release-compatible two-target PI component.

### 2. External source `i in {c,s}`

This is precisely the external response input of the ordinary/complement
return augmentation.  A `q` return closes PI; otherwise the component adds
the other external owner or reaches its already named low-return/minimal
Hall-defect boundary.  No new unsafe-core case remains.

### 3. Root source `i=r`

Because (1) makes `D` common-safe and the source condition gives

\[
 v_r(D)>v_r(X_r),
\]

`D` belongs to the broadened canonical root-response family.  The
two-stage root selector therefore yields a paying anchor return, a paying
floater substitution, or its canonical joint-critical nonempty `B_q`
packet.

These three cases exhaust all four owners.

## Composition consequence

An unsafe evolved target is not a fourth continuation type.  Global
minimal-core extraction routes it into exactly one of:

1. an immediate root/`q` PI component;
2. the finite external return/Hall component; or
3. the canonical root-response selector and its joint packet.

The same argument applies whenever a later operation produces an unsafe
desired subset contained in the current evolved target and retains the
same root release labels.  Operations with different physical release
labels still require an explicit support audit before this routing can be
reused.

## Verification and claim boundary

[`evolved_target_minimal_source_trichotomy_audit.json`](evolved_target_minimal_source_trichotomy_audit.json)
checks the minimality-to-common-safety implication, exhaustiveness of the
four source labels, and the root-source base-payment threshold under Z3
5.0.0.  Release compatibility of the root/`q` and external return edges is
the previously audited two-root residual-split support identity.

This lemma removes the unnamed unsafe evolved-target branch.  It does not
show that every later unsafe target has the same release labels, terminate
the external minimal Hall defect, eliminate the canonical joint packet,
close `GG`, or prove four-agent/general additive EFX.
