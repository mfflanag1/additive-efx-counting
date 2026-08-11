# Cross-component return-compensation selector lemma

**Date:** 2026-08-11

**Status:** cap-free completion of the two-owner payment layer for a safety-
debt bridge; multi-donor continuation and final observer safety remain open

## Bridge state and utility floors

Use a surplus-decorated current response

\[
 D\subseteq Y_j,
 \qquad \mu_s=v_s(D)-v_s(Y_s)>0,                  \tag{1}
\]

and an observer `h` in a different physical transfer component with

\[
 \tau_h(D)>v_h(X_h).                               \tag{2}
\]

Let `b_h` be the utility floor that `h` must retain.  It includes base
payment, every already protected final comparison, and the appropriate
strict priority floor when `h` is priority-critical.  The current paid
candidate has slack

\[
 \sigma_h=v_h(Y_h)-b_h\ge0.                       \tag{3}

\]

Let `P_h` be the finite packet pool currently held by `h` that may be sent
directly to response source `s` without changing another owner's bundle.

## Joint bridge selector

For a debt-removing packet

\[
 J\subseteq D,
 \qquad \tau_h(D\setminus J)\le v_h(X_h),         \tag{4}

\]

send `J` from target component `j` to `h`.  For a return packet `L subseteq
P_h`, send `L` from `h` to `s`.  Owner `h` retains her floor exactly when

\[
 v_h(L)\le \sigma_h+v_h(J).                       \tag{5}

\]

The response source strictly improves relative to the current splice exactly
when

\[
 v_s(D\setminus J+L)>v_s(Y_s),                    \tag{6}
\]

or equivalently

\[
 v_s(L)-v_s(J)>-\mu_s.                            \tag{7}

\]

The family of pairs `(J,L)` satisfying (4)--(5) is nonempty: take `J=D` and
`L=empty`.  Choose a pair maximizing

\[
 \Omega(J,L)=v_s(L)-v_s(J),                       \tag{8}

\]

with deterministic physical tie-breaking.

## Exact dichotomy

1. **Paid component bridge.** If the maximum in (8) is greater than
   `-mu_s`, then (5) retains every requirement summarized by `b_h`, (7)
   strictly improves `s`, and (4) removes `h`'s base-safety debt against the
   trimmed old response core.  The nonempty edge `j -> h:J`, together with
   `h -> s:L` when `L` is nonempty and `j -> s:D-J` when that packet is
   nonempty, forms one physical component on the participating owners.
   Deleting `J` cannot increase any old threshold.  Any new failure caused
   by attaching `L` to `s` is therefore a named surplus-decorated current
   response, not a payment failure or an untyped reset.
2. **Exact return separator.** If the maximum is at most `-mu_s`, then every
   direct two-edge bridge satisfies

   \[
   \begin{split}
    &\tau_h(D\setminus J)\le v_h(X_h),\\
    &v_h(L)\le\sigma_h+v_h(J)
   \end{split}
   \quad\Longrightarrow\quad
   v_s(J)-v_s(L)\ge\mu_s.                         \tag{9}
   \]

   Thus no debt-removing packet and no return packet from `h`'s entire
   direct pool can simultaneously retain `h`'s protected floor and preserve
   the current response of `s`.  The smallest remaining operation must
   recruit another owner on `h`'s existing signed-transfer component, relax
   `s` from current improvement to an explicitly priority-valid base floor,
   or replace the response core.

This selector subsumes the uncompensated bridge: `L=empty` succeeds exactly
when some debt-removing `J` has `v_s(J)<mu_s`.

## Verification and boundary

[`cross_component_return_compensation_selector_audit.json`](cross_component_return_compensation_selector_audit.json)
checks both payment identities, nonempty selector feasibility, the direct-
bridge specialization, and the global failure certificate.

This lemma does not force the success branch, preserve observer safety after
`L` is attached to the source target, terminate the multi-donor chain in
branch 2, establish a globally maximal GG countermodel, close GG, or prove
four-agent/general additive EFX.
