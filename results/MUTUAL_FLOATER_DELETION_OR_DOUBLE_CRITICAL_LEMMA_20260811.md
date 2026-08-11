# Mutual-floater deletion or double-critical lemma

**Date:** 2026-08-11

**Status:** cap-free closure of protected q-core availability except for one
exact double-floater-critical separator

## Two canonical cores

At the anchored mixed-margin terminal, the permanent root core and protected
q core are

\[
 A_r=T_q+f,
 \qquad
 D_q=(T_r\setminus U)+f,                          \tag{1}
\]

with

\[
 v_r(A_r)>v_r(X_r),
 \qquad
 v_q(D_q)>v_q(X_q).                               \tag{2}
\]

Both are base-common-safe.  Their non-floater supports are disjoint, so

\[
 A_r\cap D_q=\{f\}.                               \tag{3}
\]

Deleting `f` preserves common safety.

## Exact trichotomy

Exactly one of the following proof branches is available.

### 1. Floater-free protected q core

If

\[
 v_q(T_r\setminus U)>v_q(X_q),                    \tag{4}
\]

then `T_r-U` is a common-safe desired q core disjoint from `A_r`.  In every
anchored pivot where q is distinct from the root, hole, and closing source,
it is physically eligible as the protected third-donor core.  The general
third-owner root-replacement selector applies without duplicating `f`.

### 2. Floater-free root anchor

If (4) fails but

\[
 v_r(T_q)>v_r(X_r),                                \tag{5}
\]

then `T_q` is a common-safe desired root response disjoint from `D_q`.
Replacing `A_r` by `T_q` either records a new exact root-core/release label,
which is permanent response augmentation, or selects an already recorded
floater-free anchor.  In the latter case the full protected core `D_q` is
physically available for the q-donor selector.

### 3. Double-floater-critical separator

If neither (4) nor (5) holds, (2) gives the two exact criticalities

\[
\begin{aligned}
 v_r(T_q)&\le v_r(X_r)<v_r(T_q+f),\\
 v_q(T_r\setminus U)&\le v_q(X_q)
     <v_q((T_r\setminus U)+f).                    \tag{6}
\end{aligned}
\]

Thus the unique floater is simultaneously necessary for both canonical
mutual responses.  No proof may retain both cores or invoke the protected
q-donor theorem without an explicit floater replacement.

The smallest missing packet operation is now exact: find a packet `G`
outside one canonical core that substitutes for `f` in that owner's row
while preserving the other owner's floater-critical core, or release/change
the root/q response.  Failure must certify that every root-paying substitute
captures q's remaining margin and every q-paying substitute exceeds the
root budget at the same globally maximal state.

## Consequence for the anchored role split

For the six q-donor-role-available pivots, arbitrary protected-core
availability is eliminated: branches 1--2 enter the existing donor/response
machinery, and only (6) remains.  For the six q-source-collision pivots,
branches 1--2 remove the physical floater collision but the closing-source
role collision remains; only there is the additional two-core q rerouting
needed.

Hence every stable anchored mixed-margin terminal now contains either a new
floater-free root/q core, or the explicit double-critical inequalities (6).

## Verification and boundary

[`mutual_floater_deletion_or_double_critical_audit.json`](mutual_floater_deletion_or_double_critical_audit.json)
checks support intersection, hereditary safety under deletion, exhaustiveness
of the two deletion branches, and both implications in (6) in exact linear
arithmetic.

This lemma does not produce the substitute packet in the double-critical
branch, eliminate the q-source role collision, discharge the donor selector's
root-concentration/blockade outcomes, produce a globally maximal
countermodel, close GG, or prove four-agent/general additive EFX.
