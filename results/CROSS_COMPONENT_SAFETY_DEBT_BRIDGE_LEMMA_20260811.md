# Cross-component safety-debt bridge lemma

**Date:** 2026-08-11

**Status:** cap-free bridge from a surplus-decorated response to a physically
connected response, or an exact source-compensation separator

## Decorated response and external observer component

Let `X` be the base EFX allocation and `Y` an all-owner-paid splice.  Suppose
a failed observer inequality has produced the globally minimal current
response

\[
 D\subseteq Y_j,
 \qquad v_s(D)>v_s(Y_s),                           \tag{1}
\]

which is safe relative to the current paid bundles.  Let `h` be an observer
whose base-safety debt is positive:

\[
 \tau_h(D)>v_h(X_h).                               \tag{2}
\]

Assume the signed transfer component containing `h` is physically distinct
from the component containing target `j` and response source `s`.  The
decorated response therefore depends on surplus from another component.

Put

\[
 \mu_s=v_s(D)-v_s(Y_s)>0.                          \tag{3}
\]

## Canonical safety-debt deletion

The finite family

\[
 \mathcal J_h={J\subseteq D:
                 \tau_h(D\setminus J)\le v_h(X_h)}                  \tag{4}
\]

is nonempty: `J=D` leaves the empty target, whose EFX threshold is zero.
Because (2) excludes `J=empty`, every member is nonempty.  Choose

\[
 J_h^*\in\arg\min_{J\in\mathcal J_h}v_s(J).        \tag{5}
\]

Deleting goods cannot increase an additive EFX threshold, so

\[
 \tau_a(D\setminus J_h^*)\le\tau_a(D)             \tag{6}
\]

for every observer `a`.  Thus paying the debt of `h` creates no new observer
debt.

## Exact dichotomy

Exactly one of the following occurs.

1. **One-packet physical bridge.** If

   \[
    v_s(J_h^*)<\mu_s,                              \tag{7}
   \]

   then

   \[
    v_s(D\setminus J_h^*)>v_s(Y_s).               \tag{8}
   \]

   Send `D\setminus J_h^*` to source `s` and send the nonempty packet
   `J_h^*` to observer `h`.  Source `s` still strictly improves relative to
   the current splice, `h` gains a positive packet, (4) removes `h`'s base-
   safety debt, and (6) preserves every other safety inequality previously
   satisfied by `D`.  The packet edge from target component `j` to `h`
   physically merges the two transfer components.
2. **Source-compensation separator.** If (7) fails, then every packet that
   removes `h`'s base-safety debt consumes the source's entire current
   response margin:

   \[
    J\in\mathcal J_h
    \quad\Longrightarrow\quad
    v_s(J)\ge\mu_s.                                \tag{9}
   \]

   Consequently no one-way target-to-observer bridge can preserve the
   current response.  The smallest missing operation is a return packet
   `L` from `h`'s signed transfer component to `s` satisfying

   \[
    v_s(L)>v_s(J_h^*)-\mu_s,                       \tag{10}
   \]

   while retaining enough net gain in `h`'s component to fund its remaining
   observer debts.  The two edges `j -> h:J_h^*` and `h-component -> s:L`
   form the required bridge cycle.

The selector (5) is global over every subpacket of `D`; (9) is therefore an
exact separating certificate, not failure of a greedy deletion.

## Iteration over external components

Apply the dichotomy to one cross-component debt at a time.  Every successful
branch strictly merges two physical transfer components and never increases
any target threshold.  With four owners this can happen only finitely many
times, but the argument itself uses no owner-bundle or item-value cap.  A
failed branch names the precise return-compensation edge required from the
observer component; it must be included in the final surplus-budgeted
connected selector rather than hidden in a response reset.

## Verification and boundary

[`cross_component_safety_debt_bridge_audit.json`](cross_component_safety_debt_bridge_audit.json)
checks nonempty-deletion feasibility, monotonicity of additive EFX thresholds,
the strict surviving-source identity, the global separator implication, and
the exact return-compensation threshold.

This lemma does not force the return packet (10), prove that simultaneous
return packets preserve all donor surpluses, close an exact repeated decorated
response, establish a globally maximal GG countermodel, close GG, or prove
four-agent/general additive EFX.
