# Component-wide current-or-base-floor handoff lemma

**Date:** 2026-08-11

**Status:** cap-free use of the response source's realized surplus in the
component-wide bridge; sacrifice/direct-safety after the base separator
remains open

## Two source margins

Use the component-wide return selector with current response

\[
 v_s(D)>v_s(Y_s)\ge v_s(X_s).                     \tag{1}

\]

The current-response and base-response margins are

\[
 \mu_s^{\rm cur}=v_s(D)-v_s(Y_s)>0,               \tag{2}

\]

and

\[
 \mu_s^{\rm base}=v_s(D)-v_s(X_s)
 =\mu_s^{\rm cur}+Delta_s,
 \qquad
 \Delta_s=v_s(Y_s)-v_s(X_s)\ge0.                 \tag{3}

\]

Thus the surplus already realized by `s` is an exact additional bridge
budget.  Requiring every return to preserve `v_s(Y_s)` discards `Delta_s`
and is unnecessarily strong for a globally lex-valid endpoint.

Let `Omega_C` be the maximum of `v_s(L)-v_s(J)` over every debt-removing
packet and every component-wide floor-preserving redistribution from the
component-wide selector.

## Exact trichotomy

Exactly one of the following occurs.

1. **Current-source improvement.** If

   \[
    \Omega_C>-\mu_s^{\rm cur},                    \tag{4}
   \]

   the connected bridge strictly improves `s` relative to her current
   splice bundle.  This is the strongest branch already proved by the
   component-wide selector.
2. **Base-paid priority handoff.** If

   \[
    -\mu_s^{\rm base}<\Omega_C
    \le-\mu_s^{\rm cur},                          \tag{5}
   \]

   then the selected bridge may lower `s` relative to `Y_s`, but

   \[
    v_s(D-J+L)>v_s(X_s).                          \tag{6}
   \]

   Every observer-component owner retains her protected floor, and the
   original splice's earlier strict root gain is unchanged.  Once the final
   observer-surplus checks hold, the allocation is therefore an EFX
   lexicographic improvement.  Any failed check again yields a decorated
   current response.  No reset is justified merely because `s` failed to
   preserve her intermediate utility.
3. **Base-margin separator.** If

   \[
    \Omega_C\le-\mu_s^{\rm base},                 \tag{7}
   \]

   every component-wide bridge retaining the other owners' floors satisfies

   \[
    v_s(J)-v_s(L)\ge\mu_s^{\rm base}.             \tag{8}
   \]

   Hence no internal donor ordering can even keep `s` above her original GG
   base, after crediting her entire realized splice surplus.  The remaining
   operation must use the priority-valid sacrificed-source direct-safety
   branch, recruit an outside physical component, or replace `D`.

The inequalities in (4)--(7) are disjoint and exhaustive.  Equality belongs
to the lower branch because desired/base payment is strict in the
nondegenerate response normal form; a weakly paid variant replaces the two
strict signs consistently.

## Consequence

The repeated-support proof may not treat loss relative to an intermediate
splice as a failure.  At a globally lex-maximal base, the only relevant
payment threshold for a non-earlier response source is her base utility (or,
if explicitly sacrificed, her final direct-safety floor).  This consumes all
available same-row surplus before opening another component or response
reset.

## Verification and boundary

[`component_wide_current_or_base_floor_handoff_audit.json`](component_wide_current_or_base_floor_handoff_audit.json)
checks the margin decomposition, exhaustive interval trichotomy, current and
base payment identities, and the global base-separator implication.

This lemma does not discharge final observer safety, prove the sacrificed-
source direct-safety branch, force outside-component recruitment, establish a
globally maximal GG countermodel, close GG, or prove four-agent/general
additive EFX.
