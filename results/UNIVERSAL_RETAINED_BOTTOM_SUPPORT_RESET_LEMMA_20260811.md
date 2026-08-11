# Universal retained-bottom-support reset lemma

**Date:** 2026-08-11

**Status:** cap-free monotonicity for every response compression that consumes
already absorbed root-bottom support; the support-disjoint repeated-bottom
Hall recurrence remains open

## Two bottom-support coordinates

Let `V subseteq B_r` be the historical set of bottom goods absorbed by the
root-concentration rotation.  Let `S subseteq V` be the subset subsequently
committed to disjoint retained response cores.  The live root anchor is

\[
 A(V,S)=T_q+f+(V\setminus S),                       \tag{1}
\]

with positive root response margin

\[
 \eta(V,S)=v_r(A(V,S))-v_r(X_r)>0.                 \tag{2}
\]

The pair `(V,S)`, rather than the currently held bottom packet alone, records
both irreversible events: first absorption and later consumption by a
retained core.

## Canonical overlap update

Suppose a response/Hall detour selects pairwise-disjoint common-safe desired
cores `A_1,...,A_m` that must survive the return to the bottom-root
orientation.  First route every core meeting `T_q+f` through the existing
top-overlap or floater-consuming handoff.  In the branch considered here,
each retained core is disjoint from `T_q+f`.  Their fresh overlap with the
live bottom tail is

\[
 K=\left(\bigcup_h A_h\right)\cap(V\setminus S).    \tag{3}
\]

Set

\[
 S'=S\cup K.                                       \tag{4}
\]

The reduced root anchor

\[
 A(V,S')=A(V,S)\setminus K                         \tag{5}
\]

is disjoint from every retained core, and its exact response margin is

\[
 \eta(V,S')=\eta(V,S)-v_r(K).                      \tag{6}
\]

Exactly one of the following occurs.

1. **Preserved bottom reset.** `K` is empty.  The live root anchor and both
   bottom coordinates are unchanged.
2. **Fresh bottom-consumption progress.** `K` is nonempty and
   `v_r(K)<eta(V,S)`.  The reduced anchor remains desired and common-safe,
   while `S` strictly grows inside the fixed finite set `V`.
3. **Captured root-margin handoff.** `v_r(K)>=eta(V,S)`.  The fresh overlap
   captures the entire remaining root response margin.  It enters the
   root-critical compensator/third-owner packet frontier; the proof may not
   restore the old anchor without recording the reverse physical transfer.

Deletion preserves common safety, and `S subseteq S' subseteq V`, so the
update is cap-free and finite.

## Interaction with fresh absorption

The root-concentration rotation updates `V'=V union H`.  Combining that
update with (3)--(6) gives a nested support potential

\[
 (|V|,|S|).                                        \tag{7}
\]

A packet `H` containing a good outside `V` increases the first coordinate.
At fixed `V`, a retained response core that consumes a live good of
`V\setminus S` increases the second coordinate or captures the root margin.
Therefore a repeated-bottom state can remain unclassified only if

\[
 H\subseteq V\setminus S
 \quad\text{and every retained response core avoids }V\setminus S.      \tag{8}

If a proposed repetition instead reabsorbs a good of `S`, it reverses a
previous physical commitment and must be analyzed as a connected return
component, not counted as a fresh absorption.

Thus the former undifferentiated case `H subseteq V` shrinks to the
**support-disjoint repeated-bottom Hall gate** (8), plus an explicit reverse-
support component when `H` meets `S`.

## Verification and boundary

[`universal_retained_bottom_support_reset_audit.json`](universal_retained_bottom_support_reset_audit.json)
checks the support partition, exact margin identity, exhaustive reset
trichotomy, nested-set monotonicity, and the two-coordinate progress
classification symbolically.

This lemma does not terminate a top/floater overlap (it delegates that case
to the named earlier handoffs), prove that a reverse-support component is
release-compatible, terminate the support-disjoint gate (8), discharge
successful-fork surplus budgets, close `GG`, or prove four-agent/general
additive EFX.
