# Protected-q response-retention lemma

**Date:** 2026-08-11

**Status:** cap-free persistence of the protected-source matching coordinate;
degree-zero `q` recurrence and physical anchor-gap closure remain open

## Root-oriented state

Use an anchor-compatible maximum response matching containing the permanent
root edge into the changed `q` target.  Its selected root core is

\[
 D_r=T_q+f.                                         \tag{1}
\]

Suppose the `q`-priority selector also represents `q` by a common-safe
desired core `A_q` in another target.  Selected matching cores lie in
distinct allocation targets and are pairwise disjoint.  Since (1) already
contains the unique charity good,

\[
 f\notin A_q.                                       \tag{2}
\]

Thus protected `q` coverage never creates a second floater-consuming core
inside the anchored matching.

## Orientation reset

If the proof stays root-oriented, retain `A_q`; `q` remains represented.
If it returns to the `q`-oriented mutual core, use

\[
 D(U)=(T_r\setminus U)+f.
\]

Apply the universal retained-support reset to every floater-free core that
must survive the detour, including `A_q` when it is retained physically.
Let `K` be their fresh overlap with `T_r\setminus U` and put `U'=U+K`.
Exactly one of the following occurs.

1. `K` is empty: `D(U)` remains disjoint and desired by `q`.
2. `K` is nonempty and `D(U')` remains desired: retained support strictly
   grows and `q` remains represented by `D(U')`.
3. `D(U')` is no longer desired: `K` captures the whole remaining `q`
   response margin and enters the anchored captured-margin handoff.

Hence, after the anchor-constrained selector first represents `q`, a later
top-only reset cannot silently return to a degree-zero sacrificed-`q`
matching at the same retained state.  It preserves protected `q` coverage,
strictly enlarges `U`, or exposes the named margin-capture packet.

## Plateau consequence

This persistence is the current-state information missing from the
historical ledger.  On the exact four-state plateau, anchor selection and
`q` priority pick the unique matching label `(A_r,q,c,W)`.  Equation (2) and
the reset trichotomy prevent a later orientation change from replacing it
by either state in which `q` is again the hole without recording fresh
support or captured margin.

## Verification and boundary

[`protected_q_response_retention_audit.json`](protected_q_response_retention_audit.json)
checks the forced floater exclusion and the exhaustive scalar reset
trichotomy, reusing the exact universal-retained-support audit for support
partition and margin identities.

This lemma proves persistence only after `q` has a response core.  It does
not eliminate a state in which `q` has degree zero from the outset, preserve
an improved unrepresented `q` residual through every rank-two/rank-one
repartition, make the anchor-gap alternating path release-compatible, close
GG, or prove four-agent/general additive EFX.
